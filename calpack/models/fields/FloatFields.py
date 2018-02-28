"""
"""

__all__ = [
    'FloatField', 'DoubleField', 'LongDoubleField'
]

import ctypes
from calpack.models.fields.Fields import Field

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