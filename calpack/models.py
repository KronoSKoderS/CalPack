"""
models - a collection of classes and function to create new custom packets.
===========================================================================
"""

import ctypes

from collections import OrderedDict
from math import ceil

_no_type = object()


def typed_property(name, expected_type, default_val = None):
    """
    Simple function used to ensure a specific type for a property defined within a 
    class. 
    """
    if default_val is not None:
        if not isinstance(default_val, expected_type):
            raise TypeError("{v} must be of type {t}".format(v=default_val, t=expected_type))

    storage_name = '_internal_' + name

    @property
    def prop(self):
        val = getattr(self, storage_name, None)
        return val if val is not None else default_val

    @prop.setter
    def prop(self, value):
        if not isinstance(value, expected_type):
            raise TypeError("{v} must be of type {t}".format(v=value, t=expected_type))
        setattr(self, storage_name, value)

    return prop


def _field_property(field_name, field):
    """
    Simple function used to allow for setting fields directly, and returning the class
    of the fields. 

    This is the "magic" of the Fields and Packet Interface.  This allows the user to 
    set and get the field as if it were the type of field being used.  

    For example `packet.field1 = 10` would use the `@prop.setter` part of this function
    definition.  

    Note that this can ONLY be used within a class definition since there's the use of 
    the `self` class call.  
    """
    @property
    def prop(self):
        return getattr(self._c_pkt, '_' + field_name)

    @prop.setter
    def prop(self, value):
        # Ensuring the type if it's set
        if field._type is not _no_type and not isinstance(value, field._type):
            raise TypeError("{v} must be of type {t1} or {t2}".format(v=value, t1=field._type, t2=type(field)))

        # Sets the internal value of the field
        setattr(self._c_pkt, '_' + field_name, value)

    return prop


class Field():
    """
    A Super class that all other fields inherit from.
    """
    
    num_words = typed_property('num_words', int)
    _acceptable_params = set(['bit_len', 'num_words'])
    _c_type = None
    _type = _no_type

    def __init__(self, **kwargs):
        for k, v, in kwargs.items():
            if k not in self._acceptable_params:
                raise KeyError("`{k}` is not an accepted parameter for {cls}".format(k=k, cls=self.__class__))

            # set the user defined keyword args.  
            setattr(self, k, v)


class IntField(Field):
    """
    An Integer field.  

    valid keyword arguments:

    - bit_len = the length in bits of the integer.  Max value of 64. (default 16)
    - unsigned = wheter to treat the int as an unsigned integer or signed integer (default unsigned)
    - little_endian = wheter to treate the int as a little endian or big endian integer (default os preference)
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
    """
    def __new__(cls, clsname, bases, clsdict):
        d = dict(clsdict)
        
        order = []
        fields = []

        num_bits_used = 0

        # for each 'Field' type we're gonna save the order and prep for the c struct
        for name, value in clsdict.items():

            if isinstance(value, Field):
                fields.append(('_' + name, value._c_type, value.bit_len))

                num_bits_used += value.bit_len

                order.append(name)
                d[name] = _field_property(name, value)

        # Here we save the order
        d['_fields_order'] = order

        # Here we create the internal structure
        class c_struct(ctypes.Structure):
            pass
        
        c_struct._fields_ = fields
        d['_c_struct'] = c_struct

        # finally we store the number of words
        d['_num_bits_used'] = num_bits_used

        return type.__new__(cls, clsname, bases, d)

    @classmethod
    def __prepare__(metacls, clsname, bases, **kwargs):
        return OrderedDict()


class Packet(metaclass=_MetaPacket):
    word_size = typed_property('word_size', int, 16)

    def __init__(self):
        # create an internal c structure instance for us to interface with.  
        self._c_pkt = self._c_struct()

    @property
    def num_words(self):
        return ceil(self._num_bits_used / self.word_size)

    @property
    def byte_size(self):
        return ceil(self._num_bits_used / 8)
    
    def to_bytes(self):
        return ctypes.string_at(ctypes.addressof(self._c_pkt), self.byte_size)

    @classmethod
    def from_bytes(cls, buf):
        cstring = ctypes.create_string_buffer(buf)
        c_pkt = ctypes.cast(ctypes.pointer(cstring), ctypes.POINTER(cls._c_struct)).contents
        pkt = cls()
        pkt._c_pkt = c_pkt

        return pkt
