"""
models - a collection of classes and function to create new custom packets.
===========================================================================
"""

import ctypes

from collections import OrderedDict

_no_type = object()


def typed_property(name, expected_type):
    """
    Simple function used to ensure a specific type for a property defined within a 
    class. 
    """
    storage_name = '_internal_' + name

    @property
    def prop(self):
        return getattr(self, storage_name)

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
        return getattr(self._c_struct, '_' + field_name)

    @prop.setter
    def prop(self, value):
        # Ensuring the type if it's set
        if field._type is not _no_type and not isinstance(value, field._type):
            raise TypeError("{v} must be of type {t1} or {t2}".format(v=value, t1=field._type, t2=type(field)))

        # Sets the internal value of the field
        setattr(self._c_struct, '_' + field_name, value)

    return prop


class Field():
    """
    A Super class that all other fields inherit from.
    """
    
    _num_words = typed_property('num_words', int)
    _acceptable_params = set(['bit_len', 'num_words'])
    _c_type = None
    _type = _no_type

    def __init__(self, **kwargs):
        for k, v, in kwargs.items():
            if k not in self._acceptable_params:
                raise KeyError("`{k}` is not an accepted parameter for {cls}".format(k=k, cls=self.__class__))

        self._num_words = kwargs.get('num_words', 1)


class ListField(Field):
    
    _type = list

    def __init__(self):
        super(ListField, self).__init__(**kwargs)


class IntField(Field):
    """
    An Integer field.  
    """
    _bit_len = typed_property('bit_len', int)
    _unsigned = typed_property('unsigned', bool)
    _little_endian = typed_property('little_endian', bool)
    _type = int

    def __init__(self, **kwargs):
        self._acceptable_params.update(['bit_len', 'little_endian', 'unsigned', 'initial_value'])
        super(IntField, self).__init__(**kwargs)

        self._bit_len = kwargs.get('bit_len', 16)
        self._little_endian = kwargs.get('little_endian', False)
        self._unsigned = kwargs.get('unsigned', False)
        if self._unsigned:
            self._c_type = ctypes.c_uint64
        else:
            self._c_type = ctypes.c_int64


# The following are intended for future use.  
#class ReservedField(Field):
#    pass


#class EncapsulatedPacketField(Field):
#    def __init__(self, packet, **kwargs):
#        pass


class _MetaPacket(type):
    """
    _MetaPacket - A class used to generate the classes defined by the user into a usable class.
    """
    def __new__(cls, clsname, bases, clsdict):
        d = dict(clsdict)
        
        order = []
        fields = []

        # for each 'Field' type we're gonna save the order and prep for the c struct
        for name, value in clsdict.items():

            if isinstance(value, Field):
                if value._num_words > 1:
                    value._type = list

                    # arrays will need to have a custom class underneath
                    class _field(ctypes.Structure):
                        _fields_ = [('value', value._c_type, value._bit_len)]

                    fields.append(('_' + name, _field * value._num_words))
                else:
                    fields.append(('_' + name, value._c_type, value._bit_len))

                order.append(name)
                d[name] = _field_property(name, value)

            # This hasn't been tested and won't be included in the release just yet.  
            ## Encapsulated Packet are different.  They're already created packets.  
            #elif isinstance(value, _MetaPacket):
            #    raise NotImplementedError()
            #    value._type = value
            #    fields.append(('_' + name, value._c_struct))
            #    order.append(name)
            #    d[name] = _field_property(name, value)

        # Here we save the order
        d['_fields_order'] = order

        # Here we create the internal structure
        class c_struct(ctypes.Structure):
            pass
        
        c_struct._fields_ = fields
        d['_c_struct'] = c_struct

        return type.__new__(cls, clsname, bases, d)

    @classmethod
    def __prepare__(metacls, clsname, bases, **kwargs):
        return OrderedDict()


class Packet(metaclass=_MetaPacket):
    
    def to_bytes(self):
        c_pkt = self._c_struct()
        for f_name in self._fields_order:
            setattr(c_pkt, "_" + f_name, getattr(self, f_name)._val)

        return ctypes.string_at(ctypes.byref(c_pkt), ctypes.sizeof(c_pkt))

    @classmethod
    def from_bytes(cls, buf):
        cstring = ctypes.create_string_buffer(buf)
        c_pkt = ctypes.cast(ctypes.pointer(cstring), ctypes.POINTER(cls._c_struct)).contents
        pkt = cls()
        pkt._c_struct = c_pkt

        return pkt
