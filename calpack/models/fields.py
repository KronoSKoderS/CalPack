import ctypes

from calpack.models.utils import typed_property

__all__ = ['Field', 'IntField', 'ArrayField', 'PacketField']

class Field(object):
    """
    A Super class that all other fields inherit from.  This class is NOT intended for direct use.  Custom Fields MUST 
    inherit from this class.

    When creating a custom field you MUST define the :code:`c_type` property with a valid :code:`ctypes` data class.  
    """
    c_type = None
    field_name = None
    val = None

    creation_counter = 0
    
    bit_len = typed_property('bit_len', int, 16)

    def __init__(self, default_val=None):
        super(Field, self).__init__()
        self.default_val = default_val

        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1

    def __get__(self, instance, cls):
        if instance is None:
            return self
        return self.c_to_py(instance._get_c_field(self.field_name))

    def __set__(self, instance, val):
        c_val = self.py_to_c(val)
        instance._set_c_field(self.field_name, c_val)

    def py_to_c(self, val):
        """
        py_to_c - A function used to convert a python object into a valid ctypes assignable object.  As a default 
        this function simply returns `val`.  It's up to the other `Field`'s to define this if further formating
        is reuqired in order to set the internal structure of the packet.  

        :param val: the value the user is attempting to set the packet field to.  This can be any python object
        """
        return val

    def c_to_py(self, c_field):
        """
        c_to_py - A function used to convert the cytpes object into a python object.  As a default this function
        simply returns `c_field` directly from the ctypes.Structure object.  It's up to the other `Field`'s to 
        define this if further formating is required in order to turn the cyptes value into something user friendly.

        :param c_field: a ctypes object from the packet's internal `ctypes.Structure` object
        """
        return c_field

    def create_field_c_tuple(self, name):
        """
        create_field_c_tuple - A function used to create the required an field in the `ctypes.Structure._fields_` 
        tuple.  This must return a tuple that is acceptable for one of the items in the `_fields_` list of the
        `cytpes.Structure`.  
        """
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

        self.default_val = default_val
        self.bit_len = bit_len
        self.little_endian = little_endian
        self.signed = signed

        if self.signed:
            self.c_type = ctypes.c_int64
        else:
            self.c_type = ctypes.c_uint64

    def py_to_c(self, val):
        if not self.signed and val < 0:
            raise TypeError("Signed valued cannot be set for an unsiged IntField!")
        return val

    def create_field_c_tuple(self, name):
        return (name, self.c_type, self.bit_len)


class PacketField(Field):
    """A custom field for handling another packet as a field."""

    packet_cls = None

    def __init__(self, packet_cls):
        super(PacketField, self).__init__()

        self.packet_cls = packet_cls
        self.packet = packet_cls()

    @property
    def bit_len(self):
        return self.packet_cls.bit_len

    def create_field_c_tuple(self, name):
        return (name, self.packet_cls._Packet__c_struct)

    def __setattr__(self, arg, value):
        if self.packet_cls is not None and arg in self.packet_cls.fields_order:
            setattr(self.packet_cls, arg, value)
        else:
            super(PacketField, self).__setattr__(arg, value)

    def py_to_c(self, val):
        if not isinstance(val, self.packet_cls):
            raise TypeError("Must be of type {p}".format(type(p=self.packet_cls)))
        return val.c_pkt


class ArrayField(Field, list):
    """A custom field for handling an array of fields"""
    def __init__(self, array_cls, array_size, default_val=None):
        super(ArrayField, self).__init__(default_val)
        self.array_cls = array_cls()
        self.array_size = array_size
        self.c_type = (self.array_cls.c_type * self.array_size)

    @property
    def bit_len(self):
        return self.array_cls.bit_len * self.array_size

    def c_to_py(self, c_field):
        return c_field[:]

    def py_to_c(self, val):
        if not isinstance(val, ArrayField) and not isinstance(val, list):
            raise TypeError("Must be of type ArrayField or list")

        return self.c_type(*val)

    def create_field_c_tuple(self, name):
        return (name, self.array_cls.c_type * self.array_size)
