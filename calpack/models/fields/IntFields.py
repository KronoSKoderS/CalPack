"""
"""

import ctypes

from calpack.models.fields import Field, BYTE_SIZE
from calpack.utils import typed_property

__all__ = [
    'IntField', 'IntField8', 'IntField16', 'IntField32', 'IntField64'
]

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
