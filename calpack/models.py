"""
=======================================================================================================================
models - a collection of classes and functions to create new custom packets.
=======================================================================================================================

This module is the building blocks for creating packets.  It also provides the ability for users to create custom
fields for their packets.

Creating and working with Custom ``Packet``s
--------------------------------------------

Creating a custom packet requires inheriting the `Packet` class and then defining the Field within the order they are
expected to be seen::
    
    from calpack import models

    class Header(models.Packet):
        source = models.IntField()
        dest = models.IntField()
        data1 = models.IntField()
        data2 = models.IntField()

Once the packet is defined, creating an instance of that packet allows you to manipulate it.  Fields are automatically
set to a 'default' zero'd value::

    my_pkt = Header()

    my_pkt.source = 123
    my_pkt.dest = 456
    my_pkt.data1 = 789

    print(my_pkt.source)  # 123

Packet fields can be easily copied and compared to other packets::

    my_pkt2 = Header()
    my_pkt2.source = my_pkt.source
    my_pkt2.dest = 654

    my_pkt.source == my_pkt2.source  # True
    my_pkt.dest == my_pkt2.dest  # False


Code
----
"""
from collections import OrderedDict
from math import ceil

import ctypes

_NO_TYPE = object()


def typed_property(name, expected_type, default_val=None):
    """
    Simple function used to ensure a specific type for a property defined within a class.  This can ONLY be used
    within a class definition as the `self` keyword is used.

    :param str name: the name of the variable.  This can be anything, but cannot be already in use.
    :param type expected_type: the expected type.  When setting this property at the class level, if the types
        do not match, a `TypeError` is raised.
    :param default_val: (Optional) the default value for the property.  If not set, then `None` is used.  This
        MUST be of the same type as `expected_type` or a `TypeError` is raised.
    :return: the property
    :raises TypeError: if the `default_val` or property's set value is not of type `expected_type`
    """
    if default_val is not None and not isinstance(default_val, expected_type):
        raise TypeError("{v} must be of type {t}".format(v=default_val, t=expected_type))

    storage_name = '_internal_' + name

    @property
    def prop(self):
        # Return the set value.  If the property hasn't been set yet then use the default value
        return getattr(self, storage_name, default_val)

    @prop.setter
    def prop(self, value):
        # Raise an error if `value` is not of the expected type.  This ensure proper type setting.
        if not isinstance(value, expected_type):
            raise TypeError("{v} must be of type {t}".format(v=value, t=expected_type))
        setattr(self, storage_name, value)

    return prop


def _field_property(field_name, field):
    """
    Simple function used to allow for setting fields directly, and returning the class of the fields.

    This is the "magic" of the Fields and Packet Interface.  This allows the user to set and get the field as if it
    were the type of field being used.

    For example `packet.field1 = 10` would use the `@prop.setter` part of this function definition.

    Note that this can ONLY be used within a class definition since there's the use of the `self` class call.

    This is different from `typed_property` in that it assumes were within a `Packet` class with the _c_pkt property
    already defined.  This function is for internal use only within the `MetaPacket` definition and is NOT exppected
    to be used by the user.  THAT MEANS YOU!
    """
    @property
    def prop(self):
        field._val = getattr(self._c_pkt, '_' + field_name)
        return field

    @prop.setter
    def prop(self, value):
        set_val = value
        if isinstance(value, type(field)):
            set_val = value._val

        # Ensuring the type if it's set
        if field._type is not _NO_TYPE and not isinstance(set_val, field._type):
            raise TypeError("{v} must be of type {t1} or {t2}".format(v=value, t1=field._type, t2=type(field)))

        # Sets the internal value of the field
        setattr(self._c_pkt, '_' + field_name, set_val)

    return prop


class Field():
    """
    A Super class that all other fields inherit from.  Any class that inherits from this class will be restricted
    to instantiation with keywords as defined in the `_acceptable_params` property which is a `set`.  Update this
    `set` first in the `__init__`

    This class is NOT intended for direct use.  Custom Fields MUST inherit from this class.

    When creating a custom field the following MUST be defined:

        * c_type - A ctypes.c_<type> class that can be used within the ctypes.Structure class.
        * type - A Python type that is used to ensure type setting.

    Furthermore, `_accetable_params` (a set of strings) must be updated.  This list is used to limit the keyword
    arguments for __init__.  In order to allow the user to use keyword arguments, you MUST update this property.
    futher more, any allowed keyword arguments passed in by the user, are automatically set as properties for the
    class.

    Example field creation::

        class MyCustomInt(Field):
            type = int
            c_type = ctypes.c_int16

            def __init__(self, **kwargs):
                self._acceptable_params.update(["one", "two"]
                super(MyCustomInt, self).__init__(**kwargs)

        f = MyCustomInt(one=1)
        print(f.one)  # '1'
    """
    
    array_size = typed_property('array_size', int, 0)
    _acceptable_params = set(['array_size', 'default_val'])
    _c_type = None
    _type = _NO_TYPE
    _val = None

    def __init__(self, **kwargs):
        for key, val, in kwargs.items():
            if key not in self._acceptable_params:
                raise KeyError("`{k}` is not an accepted parameter for {cls}".format(k=key, cls=self.__class__))

            # set the user defined keyword args.
            setattr(self, key, val)

    def __eq__(self, other):
        return self._val == other


class IntField(Field):
    """
    An Integer field.

    valid keyword arguments:

    - bit_len: the length in bits of the integer.  Max value of 64. (default 16)
    - signed: wheter to treat the int as an signed integer or unsigned integer (default unsigned)
    - little_endian: wheter to treate the int as a little endian or big endian integer (default os preference)
    """
    _type = int
    bit_len = typed_property('bit_len', int, 16)
    signed = typed_property('signed', bool, False)
    little_endian = typed_property('little_endian', bool)
    
    def __init__(self, **kwargs):
        self._acceptable_params.update(['bit_len', 'little_endian', 'signed', 'initial_value'])
        super(IntField, self).__init__(**kwargs)

        if self.signed:
            self._c_type = ctypes.c_int64
        else:
            self._c_type = ctypes.c_uint64


class _MetaPacket(type):
    """
    _MetaPacket - A class used to generate the classes defined by the user into a usable class.

    This class is the magic for Turning the ``Packet`` class definitions into actual operating packets.

    The process of how this all works is a little convoluted, however here is a basic overview:

        1. A User has defined a packet through subclassing the `Packet` class
        2. For each `Field` child class:
            - The ctype is created based on bit width and ctypes type
            - The order in which it was defined is saved
            - The bit width of the field is summed
            - A `_field_property` is created.  This function, monkey pactches the class
                to enable setting the value directly (i.e. pkt.field = some_val) while
                still enabling access to the other Field methods and properties.  
        3. A `ctypes.Structure` is created with `_fields_` in order and type of the Fields.

    In order for this to work, the following are assumed about the defined `Field` classes:

        * c_type is defined with a `ctypes.c_<type>` 
        * type is defined with a Python object type
    """
    def __new__(mcs, clsname, bases, clsdict):
        class_dict = dict(clsdict)
        
        order = []
        fields = []

        num_bits_used = 0

        # for each 'Field' type we're gonna save the order and prep for the c struct
        for name, value in clsdict.items():

            if isinstance(value, Field):
                if isinstance(value, IntField):
                    field_tuple = (('_' + name, value._c_type, value.bit_len))

                    num_bits_used += value.bit_len

                    order.append(name)
                    f_prop = _field_property(name, value)

                ## Default Field processing
                #elif isinstance(value, Field):
                #    fields.append(('_' + name, value._c_type))

                #    num_bits_used += value.bit_len

                #    order.append(name)
                #    class_dict[name] = _field_property(name, value)


                if value.array_size > 0:
                    field_tuple = list(field_tuple)
                    field_tuple[1] * value.array_size
                    field_tuple = tuple(field_tuple)
                    f_prop = (f_prop, ) * value.array_size

                fields.append(field_tuple)
                class_dict[name] = f_prop

        # Here we save the order
        class_dict['_fields_order'] = order

        # Here we create the internal structure
        class Cstruct(ctypes.Structure):
            pass
        
        Cstruct._fields_ = fields
        class_dict['_c_struct'] = Cstruct

        # finally we store the number of words
        class_dict['_num_bits_used'] = num_bits_used

        return type.__new__(mcs, clsname, bases, class_dict)

    @classmethod
    def __prepare__(mcs, clsname, bases, **kwargs):
        return OrderedDict()


class Packet(metaclass=_MetaPacket):
    """
    A super class that custom packet classes MUST inherit from.  This class is NOT intended to be used directly, but
    as a super class.

    Example::

        class Header(models.Packet):
            source = models.IntField()
            dest = models.IntField()
            data1 = models.IntField()
            data2 = models.IntField()
    """
    word_size = typed_property('word_size', int, 16)

    def __init__(self, **kwargs):
        # create an internal c structure instance for us to interface with.
        self._c_pkt = self._c_struct()

        # This allows for pre-definition of a field value after packet definition
        for name in self._fields_order:
            d_val = getattr(getattr(self, name), 'default_val', None)
            if d_val is not None:
                setattr(self, name, d_val)

        # This allows for pre-definition of a field value at instantiation
        for key, val in kwargs.items():
            # Only set the keyword args associated with fields.  If it isn't found, then we'll process like normal.
            if key in self._fields_order:
                setattr(self, key, val)

    @property
    def num_words(self):
        return ceil(self._num_bits_used / self.word_size)

    @property
    def byte_size(self):
        return ceil(self._num_bits_used / 8)
    
    def to_bytes(self):
        """Converts the packet into a byte string."""
        return ctypes.string_at(ctypes.addressof(self._c_pkt), self.byte_size)

    @classmethod
    def from_bytes(cls, buf):
        """Creates a Packet from a byte string"""
        cstring = ctypes.create_string_buffer(buf)
        c_pkt = ctypes.cast(ctypes.pointer(cstring), ctypes.POINTER(cls._c_struct)).contents
        pkt = cls()
        pkt._c_pkt = c_pkt

        return pkt
