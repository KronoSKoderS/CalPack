"""
fields
======

A collection of built-in :code:`Field`'s for creating packets.  This module also contains the
building blocks for creating custom FieldTypes as well.
"""

BYTE_SIZE = 8

from calpack.models.fields.Fields import *
from calpack.models.fields.ArrayFields import *
from calpack.models.fields.BooleanFields import *
from calpack.models.fields.FloatFields import *
from calpack.models.fields.IntFields import *
from calpack.models.fields.PacketFields import *


from calpack.models.fields.Fields import __all__ as fields_all
from calpack.models.fields.ArrayFields import __all__ as array_all
from calpack.models.fields.BooleanFields import __all__ as bool_all
from calpack.models.fields.FloatFields import __all__ as float_all
from calpack.models.fields.IntFields import __all__ as int_all
from calpack.models.fields.PacketFields import __all__ as packet_all


__all__ = [
    'BYTE_SIZE',
]

__all__ += fields_all
__all__ += array_all
__all__ += bool_all
__all__ += float_all
__all__ += int_all
__all__ += packet_all
