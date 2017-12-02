"""
fields
======

A collection of built-in :code:`Field`'s for creating packets.  This module also contains the
building blocks for creating custom FieldTypes as well.
"""

import ctypes

from calpack.models.utils import typed_property

__all__ = [
    'Field',
    'IntField', 'IntField8', 'IntField16', 'IntField32', 'IntField64',
    'ArrayField',
    'PacketField',
    'FlagField',
    'FloatField', 'DoubleField', 'LongDoubleField',
    'BoolField',
]

BYTE_SIZE = 8

class Field(object):
    """
    A Super class that all other fields inherit from.  This class is NOT intended for direct use.
    Custom Fields MUST inherit from this class.

    When creating a custom field you MUST define the :code:`c_type` property with a valid
    :code:`ctypes` data class.

    :param default_val: the default value of the field.  This is set at instantiation of the Field
    """
    c_type = None
    field_name = None

    creation_counter = 0

    def __init__(self, default_val=None):
        super(Field, self).__init__()
        self.default_val = default_val

        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1

    def __get__(self, instance, cls):
        from calpack.models import Packet
        # If being called from a parent "Packet" class, then we actually want to get the internal
        # field value
        if isinstance(instance, Packet):
            return self.c_to_py(instance.get_c_field(self.field_name))
        return self

    def __set__(self, instance, val):
        from calpack.models import Packet
        if isinstance(instance, Packet):
            c_val = self.py_to_c(val)
            instance.set_c_field(self.field_name, c_val)

    def py_to_c(self, val):
        """
        py_to_c - A function used to convert a python object into a valid ctypes assignable object.
        As a default this function simply returns :code:`val`.  It's up to the other subclassesed
        :code:`Field` to define this if further formatting is required in order to set the internal
        structure of the packet.

        :param val: the value the user is attempting to set the packet field to.  This can be any
            python object.
        """
        return val

    def c_to_py(self, c_field):
        """
        c_to_py - A function used to convert the ctypes object into a python object.  As a default
        this function simply returns :code:`c_field` directly from the ctypes.Structure object.
        It's up to the other :code:`Field`'s to define this if further formatting is required in
        order to turn the ctypes value into something user friendly.

        :param c_field: a ctypes object from the packet's internal :code:`ctypes.Structure` object
        """
        return c_field

    def create_field_c_tuple(self):
        """
        create_field_c_tuple - A function used to create the required an field in the
        :code:`ctypes.Structure._fields_` tuple.  This must return a tuple that is acceptable for
        one of the items in the :code:`_fields_` list of the :code:`ctypes.Structure`.

        The first value in the tuple MUST be :code:`self.field_name` as this is used to access the
            internal c structure.
        """
        return (self.field_name, self.c_type)


class IntField(Field):
    """
    An Integer field.  This field can be configured to be signed or unsigned.  It's bit length can
    also be set, however the max bit length for this field is
    :code:`ctypes.sizeof(ctypes.c_int) * 8`.  This wraps around the :code:`ctypes.c_int` or
    :code:`ctypes.c_uint` data type.

    .. warning:: A word of caution when using the :code:`bit_len`.  If the combination of IntFields
        with the bit_len set are not byte aligned, there is the possibility of "spare" bits not
        accessible but used in the overall strucuture.  See :ref:`Unused Bits`
        for more information

    :param int bit_len: the length in bits of the integer.
    :param bool signed: whether to treat the int as an signed integer or unsigned integer (default
        unsigned)
    :param int default_val: the default value of the field (default 0)
    :raises ValueError: if the :code:`bit_len` is less than or equal to 0 or greater than
        :code:`ctypes.sizeof(ctypes.c_int) * 8`
    """

    signed = typed_property('signed', bool, False)
    _c_types = (ctypes.c_uint, ctypes.c_int)

    def __init__(self, bit_len=None, signed=False, default_val=0):
        super(IntField, self).__init__(default_val)

        self.signed = signed
        self.c_type = self._c_types[int(self.signed)]

        self.bit_len = bit_len
        if bit_len is None:
            self.bit_len = ctypes.sizeof(self.c_type) * BYTE_SIZE
        if self.bit_len <= 0 or self.bit_len > ctypes.sizeof(self.c_type) * BYTE_SIZE:
            raise ValueError("bit_len must be between 1 and {max_val}".format(
                max_val=ctypes.sizeof(self.c_type) * BYTE_SIZE)
            )

    def py_to_c(self, val):
        if not self.signed and val < 0:
            raise TypeError("Signed valued cannot be set for an unsigned IntField!")
        return val

    def create_field_c_tuple(self):
        if self.bit_len < ctypes.sizeof(self.c_type) * BYTE_SIZE:
            return (self.field_name, self.c_type, self.bit_len)

        return (self.field_name, self.c_type)


class IntField8(IntField):
    """
    An Integer field.  This field can be configured to be signed or unsigned.  It's bit length can
    also be set, however the max bit length for this field is 8.  This wraps around the
    :code:`ctypes.c_int8` or :code:`ctypes.c_uint8` data type.

    .. warning:: A word of caution when using the :code:`bit_len`.  If the combination of IntFields
        with the bit_len set are not byte aligned, there is the possibility of "spare" bits not
        accessible but used in the overall strucuture.  See :ref:`Unused Bits`
        for more information

    :param int bit_len: the length in bits of the integer.
    :param bool signed: whether to treat the int as an signed integer or unsigned integer (default
        unsigned)
    :param int default_val: the default value of the field (default 0)
    :raises ValueError: if the :code:`bit_len` is less than or equal to 0 or greater than 8
    """
    _c_types = (ctypes.c_uint8, ctypes.c_int8)


class IntField16(IntField):
    """
    An Integer field.  This field can be configured to be signed or unsigned.  It's bit length can
    also be set, however the max bit length for this field is 16.  This wraps around the
    :code:`ctypes.c_int16` or :code:`ctypes.c_uint16` data type.

    .. warning:: A word of caution when using the :code:`bit_len`.  If the combination of IntFields
        with the bit_len set are not byte aligned, there is the possibility of "spare" bits not
        accessible but used in the overall strucuture.  See :ref:`Unused Bits`
        for more information

    :param int bit_len: the length in bits of the integer.
    :param bool signed: whether to treat the int as an signed integer or unsigned integer (default
        unsigned)
    :param int default_val: the default value of the field (default 0)
    :raises ValueError: if the :code:`bit_len` is less than or equal to 0 or greater than 16
    """
    _c_types = (ctypes.c_uint16, ctypes.c_int16)


class IntField32(IntField):
    """
    An Integer field.  This field can be configured to be signed or unsigned.  It's bit length can
    also be set, however the max bit length for this field is 32.  This wraps around the
    :code:`ctypes.c_int32` or :code:`ctypes.c_uint32` data type.

    .. warning:: A word of caution when using the :code:`bit_len`.  If the combination of IntFields
        with the bit_len set are not byte aligned, there is the possibility of "spare" bits not
        accessible but used in the overall strucuture.  See :ref:`Unused Bits`
        for more information

    :param int bit_len: the length in bits of the integer.
    :param bool signed: whether to treat the int as an signed integer or unsigned integer (default
        unsigned)
    :param int default_val: the default value of the field (default 0)
    :raises ValueError: if the :code:`bit_len` is less than or equal to 0 or greater than 32
    """
    _c_types = (ctypes.c_uint32, ctypes.c_int32)


class IntField64(IntField):
    """
    An Integer field.  This field can be configured to be signed or unsigned.  It's bit length can
    also be set, however the max bit length for this field is 64.  This wraps around the
    :code:`ctypes.c_int64` or :code:`ctypes.c_uint64` data type.

    .. warning:: A word of caution when using the :code:`bit_len`.  If the combination of IntFields
        with the bit_len set are not byte aligned, there is the possibility of "spare" bits not
        accessible but used in the overall strucuture.  See :ref:`Unused Bits`
        for more information

    :param int bit_len: the length in bits of the integer.
    :param bool signed: whether to treat the int as an signed integer or unsigned integer (default
        unsigned)
    :param int default_val: the default value of the field (default 0)
    :raises ValueError: if the :code:`bit_len` is less than or equal to 0 or greater than 64
    """
    _c_types = (ctypes.c_uint64, ctypes.c_int64)


class PacketField(Field):
    """
    A custom Field for handling another packet as a field.

    :param packet_cls: A :code:`calpack.models.Packet` subclass that represents another packet
    """
    packet_cls = None

    def __init__(self, packet_cls):
        super(PacketField, self).__init__()

        self.packet_cls = packet_cls
        self.packet = packet_cls()
        self.c_type = self.packet._Packet__c_struct

    def create_field_c_tuple(self):
        return (self.field_name, self.packet_cls._Packet__c_struct)

    def __setattr__(self, arg, value):
        if self.packet_cls is not None and arg in self.packet_cls.fields_order:
            setattr(self.packet_cls, arg, value)
        else:
            super(PacketField, self).__setattr__(arg, value)

    def py_to_c(self, val):
        if not isinstance(val, self.packet_cls):
            raise TypeError("Must be of type {p}".format(p=type(self.packet_cls)))
        return val.c_pkt


class ArrayField(Field):
    """
    A custom field for handling an array of fields.  Only tuples or other ArrayFields can be written to the

    :param array_cls: a :code:`calpack.models.Field` subclass **object** that represent the Field
        the array will be filled with.
    :param int array_size: the length of the array.
    """
    def __init__(self, array_cls, array_size, default_val=None):
        super(ArrayField, self).__init__(default_val)
        self.array_cls = array_cls
        self.array_size = array_size

        array_cls_tuple = self.array_cls.create_field_c_tuple()
        if len(array_cls_tuple) == 3:
            raise TypeError(
                "ArrayField does not support Fields with non-byte aligned field tuples!"
            )
        self.c_type = (array_cls_tuple[1] * self.array_size)

    def c_to_py(self, c_field):
        return tuple(c_field[:])

    def py_to_c(self, val):
        if not isinstance(val, ArrayField) and not isinstance(val, tuple) and not isinstance(val, list):
            raise TypeError("Must be of type ArrayField or list")

        if len(val) != self.array_size:
            raise ValueError("The length of val must be {}!".format(self.array_size))

        return self.c_type(*val)

    def __len__(self):
        return self.array_size


class FlagField(Field):
    """
    A custom field for handling single bit 'flags'.

    :param bool default_val: the default value of the field (default False)
    """
    c_type = ctypes.c_uint8

    def __init__(self, default_val=False):
        super(FlagField, self).__init__(default_val)

    def c_to_py(self, c_field):
        return bool(c_field)

    def py_to_c(self, val):
        if not isinstance(val, FlagField) and not isinstance(val, bool):
            raise TypeError("Must be of type `FlagField` or `bool`")

        return int(val)

    def create_field_c_tuple(self):
        return (self.field_name, self.c_type, 1)


class FloatField(Field):
    """
    A custom field for handling floating point numbers.
    """
    c_type = ctypes.c_float

    def __init__(self, default_val=0.0):
        super(FloatField, self).__init__(default_val)


class DoubleField(FloatField):
    """
    A custom field for handling double floating point numbers
    """
    c_type = ctypes.c_double


class LongDoubleField(FloatField):
    """
    A custom field for handling long double floating point numbers
    """
    c_type = ctypes.c_longdouble


class BoolField(Field):
    """
    A custom field for handling Boolean types
    """
    c_type = ctypes.c_bool

    def __init__(self, default_val=False):
        super(BoolField, self).__init__(default_val)

        self.bit_len = ctypes.sizeof(self.c_type)


    def py_to_c(self, val):
        if not isinstance(val, bool) and not isinstance(val, BoolField):
            raise TypeError("Must be of type `bool` or `BoolField`!")

        return super(BoolField, self).py_to_c(val)
