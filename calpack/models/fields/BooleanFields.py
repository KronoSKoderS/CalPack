"""
"""

__all__ = [
    'FlagField', 'BoolField'
]

import ctypes

from calpack.models.fields.Fields import Field

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
