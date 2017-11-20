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


Packets themself can also be campared:

    my_pkt = Header()
    my_pkt.source = 123
    my_pkt.dest = 456
    my_pkt.data1 = 789

    my_pkt2 = Header()
    my_pkt2.source = 123
    my_pkt2.dest = 456
    my_pkt2.data1 = 123

    my_pkt == my_pkt2 # False
    my_pkt2.data1 = 789

    my_pkt == my_pkt2 # True

Class/Function specific Docs
----------------------------
"""
from __future__ import print_function
from collections import OrderedDict
from math import ceil

import sys
import ctypes
import copy


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

_NO_TYPE = object()

# This was taken from the six.py source code.  Reason being that I only needed a small part of six
#   and didn't want to rely on the third-party installation just for this package.  I highly recommend
#   looking at them for Python 2/3 compatible coding:  https://github.com/benjaminp/six
def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper


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


class Field(object):
    """
    A Super class that all other fields inherit from.  This class is NOT intended for direct use.  Custom Fields MUST 
    inherit from this class.

    When creating a custom field you MUST define the `c_type` property with a valid `ctypes` data class.  

    The following sections describe further details when customizing the following:

        * __init__
        * create_field_c_tuple
        * bit_len

    ## `__init__`

    TODO: Update section

    ## `create_field_c_tuple`

    TODO: Update section

    ## `bit_len`

    TODO: Update section
    """
    c_type = None
    field_name = None
    val = None

    creation_counter = 0
    
    bit_len = typed_property('bit_len', int, 16)

    def __init__(self, default_val=None):
        self.default_val = default_val

        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1

    def __eq__(self, other):
        if isinstance(other, Field):
            return self.val == other.val
        return self.val == other

    def __ne__(self, other):
        if isinstance(other, Field):
            return self.val != other.val
        return self.val != other

    def __lt__(self, other):
        if isinstance(other, Field):
            return self.val < other.val
        return self.val < other

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not other < self

    def __get__(self, obj, objowner):
        if isinstance(obj, Packet):
            self.val = self.get_c_field_val(obj._get_c_field(self.field_name))
        return self

    def __set__(self, obj, val):
        new_val = val
        if isinstance(val, Field):
            new_val = obj.val

        obj._set_c_field(self.field_name, new_val)

    def set_c_field_val(self, val):
        return val

    def get_c_field_val(self, c_field):
        return c_field

    def create_field_c_tuple(self, name):
        return (name, self.c_type)


class IntField(Field):
    """
    An Integer field.

    valid keyword arguments:

    - bit_len: the length in bits of the integer.  Max value of 64. (default 16)
    - signed: whether to treat the int as an signed integer or unsigned integer (default unsigned)
    """

    signed = typed_property('signed', bool, False)

    # TODO: Implement endianess processing
    little_endian = typed_property('little_endian', bool)
    
    def __init__(self, bit_len=16, signed=False, default_val=0, little_endian=False):
        super(IntField, self).__init__(default_val)

        self.bit_len = bit_len
        self.little_endian = little_endian
        self.signed = signed

        if self.signed:
            self.c_type = ctypes.c_int64
        else:
            self.c_type = ctypes.c_uint64

    def set_c_field_value(self, val):
        if not self.signed and val < 0:
            raise TypeError("Signed valued cannot be set for an unsiged IntField!")
        return val

    def create_field_c_tuple(self, name):
        return (name, self.c_type, self.bit_len)


class PacketField(Field):
    """A custom field for handling another packet as a field."""

    def __init__(self, packet_cls):
        super(PacketField, self).__init__()

        self.packet_cls = packet_cls

    @property
    def bit_len(self):
        return self.packet_cls.bit_len

    def create_field_c_tuple(self, name):
        return (name, self.packet_cls._c_struct)

    def get_c_field_val(self, c_field):
        return self.packet_cls(c_pkt = c_pkt)

class ArrayField(Field):
    """A custom field for handling an array of fields"""
    def __init__(self, array_cls, array_size, default_val=None):
        super(ArrayField, self).__init__(default_val)
        self.array_cls = array_cls()
        self.array_size = array_size
        self.c_type = (self.array_cls.c_type * self.array_size)

    @property
    def bit_len(self):
        return self.array_cls.bit_len * self.array_size

    def get_c_field_val(self, c_field):
        return c_field[:]

    def set_c_field_val(self, val):
        if not isinstance(val, ArrayField) and not isinstance(val, list):
            raise TypeError("Must be of type ArrayField or list")

        return self.c_type(*val)

    def create_field_c_tuple(self, name):
        return (name, self.array_cls.c_type * self.array_size)


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
        * bit_len
        * create_field_c_tuple
    """
    def __new__(mcs, clsname, bases, clsdict):
        class_dict = dict(clsdict)
        
        order = []
        fields_tuple = []

        num_bits_used = 0

        fields = [(field_name, clsdict.get(field_name)) for field_name, obj in clsdict.items() if isinstance(obj, Field)]

        if PY2:
            fields.sort(lambda x, y: cmp(x[1].creation_counter, y[1].creation_counter))

        # for each 'Field' type we're gonna save the order and prep for the c struct
        for name, obj in fields:
            order.append(name)

            obj.field_name = name

            field_tuple = obj.create_field_c_tuple(name)
            num_bits_used += obj.bit_len

            fields_tuple.append(field_tuple)
            class_dict[name] = obj

        # Here we save the order
        class_dict['fields_order'] = order

        # Here we create the internal structure
        class Cstruct(ctypes.Structure):
            pass
        
        Cstruct._fields_ = fields_tuple
        class_dict['_Packet__c_struct'] = Cstruct

        # finally we store the number of words
        class_dict['bit_len'] = num_bits_used

        return type.__new__(mcs, clsname, bases, class_dict)

    @classmethod
    def __prepare__(mcs, clsname, bases, **kwargs):
        return OrderedDict()


@add_metaclass(_MetaPacket)
class Packet():
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
    fields_order = None

    __c_struct = None

    @classmethod
    def get_field_instance(cls, field_name):
        return getattr(cls, field_name)

    def __new__(cls, *args, **kwargs):
        obj = super(Packet, cls).__new__(cls, *args, **kwargs)

        for field_name in obj.fields_order:
            setattr(obj, field_name, copy.deepcopy(getattr(cls, field_name)))

        return obj

    def __init__(self, c_pkt = None, **kwargs):

        # create an internal c structure instance for us to interface with.
        self.__c_pkt = self.__c_struct()
        if c_pkt is not None:
            self.__c_pkt = c_pkt

        # This allows for pre-definition of a field value after packet definition.  We only do this
        #   if the packet isn't from another packet instantiation (i.e. c_pkt was already defined).  
        if c_pkt is None:
            for name in self.fields_order:
                d_val = getattr(getattr(self, name), 'default_val', None)
                if d_val is not None:
                    setattr(self, name, d_val)

        # This allows for pre-definition of a field value at instantiation
        for key, val in kwargs.items():
            # Only set the keyword args associated with fields.  If it isn't found, then we'll process like normal.
            if key in self.fields_order:
                setattr(self, key, val)

    @property
    def c_pkt(self):
        return self.__c_pkt

    @property
    def num_words(self):
        return ceil(self.bit_len / self.word_size)

    @property
    def byte_size(self):
        return int(ceil(self.bit_len / 8))
    
    def to_bytes(self):
        """Converts the packet into a byte string."""
        return ctypes.string_at(ctypes.addressof(self.__c_pkt), self.byte_size)

    @classmethod
    def from_bytes(cls, buf):
        """Creates a Packet from a byte string"""
        cstring = ctypes.create_string_buffer(buf)
        c_pkt = ctypes.cast(ctypes.pointer(cstring), ctypes.POINTER(cls.__c_struct)).contents
        pkt = cls(c_pkt)

        return pkt

    def __eq__(self, other):
        # if it's not the same packet type
        if not isinstance(other, type(self)):
            return False

        return self.to_bytes() == other.to_bytes()

    def _set_c_field(self, field_name, val):
        try:
            setattr(self.__c_pkt, field_name, val)
        except AttributeError as e:
            raise AttributeError("'{o}' does not contain field '{n}'".format(o=self, n=field_name))

    def _get_c_field(self, field_name):
        getattr(self.__c_pkt, field_name)
