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


def field_property(field_name, field):
    """
    Simple function used to allow for setting fields directly, and returning the class
    of the fields. 
    """
    @property
    def prop(self):
        return field

    @prop.setter
    def prop(self, value):
        setattr(field, '_val', value)

    return prop


class Field():
    """
    A Super class that all other fields inherit from.  When creating a new field, the
    following is required:

    1. Add to _acceptable_params for any new keyword arguments
    2. define __lt__
    3. define _c_type
    4. define _type
    """

    _bit_len = typed_property('bit_len', int)
    _num_words = typed_property('num_words', int)
    _acceptable_params = ['bit_len', 'num_words']
    _c_type = None
    _type = _no_type
    _val = None

    def __init__(self, **kwargs):
        for k, v, in kwargs.items():
            if k not in self._acceptable_params:
                raise KeyError("`{k}` is not an accepted parameter for {cls}".format(k=k, cls=self.__class__))

        self._bit_len = kwargs.get('bit_len', 16)
        self._num_words = kwargs.get('num_words', 1)

    def __eq__(self, other):
        if isinstance(other, Field):
            return self._val == other._val
        return self._val == other

    def __lt__(self, other):
        if isinstance(other, Field):
            return self._val < other._val
        return self._val < other

    def __gt__(self, other):
        if isinstance(other, Field):
            return self._val > other._val
        return self._val > other

    def __ne__(self, other):
        return not self == other

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not other < self
        


class IntField(Field):
    _unsigned = typed_property('unsigned', bool)
    _little_endian = typed_property('little_endian', bool)

    def __init__(self, **kwargs):
        self._acceptable_params += ['little_endian', 'unsigned', 'initial_value']
        super(IntField, self).__init__(**kwargs)

        self._little_endian = kwargs.get('little_endian', False)
        self._unsigned = kwargs.get('unsigned', False)
        if self._unsigned:
            self._c_type = ctypes.c_uint64
        else:
            self._c_type = ctypes.c_int64

        self._val = kwargs.get('initial_value', 0)

    

class ReservedField(Field):
    pass


class _MetaPacket(type):
    def __new__(cls, clsname, bases, clsdict):
        d = dict(clsdict)
        
        order = []
        fields = []

        # for each 'Field' type we're gonna save the order and prep for the c struct
        for name, value in clsdict.items():
            if isinstance(value, Field):
                order.append(name)
                d[name] = field_property(name, value)

                if value._num_words > 0:

                    class _field(ctypes.Structure):
                        _fields_ = [('value', value._c_type)]

                    fields.append(('_' + name, _field * value._num_words))
                else:
                    fields.append(('_' + name, value._c_type, value._bit_len))
                

        # Here we save the order
        d['_order'] = order

        # Here we save the structure
        class c_struct(ctypes.Structure):
            pass
        
        c_struct._fields_ = fields
        d['_c_struct'] = c_struct

        return type.__new__(cls, clsname, bases, d)

    @classmethod
    def __prepare__(metacls, clsname, bases, **kwargs):
        return OrderedDict()


class Packet(metaclass=_MetaPacket):
    
    def pack(self):
        return ctypes.string_at(ctypes.byref(self._c_struct), ctypes.sizeof(self._c_struct))

    @classmethod
    def unpack(cls, buf):
        cstring = ctypes.create_string_buffer(buf)
        return ctypes.cast(ctypes.pointer(cstring), ctypes.POINTER(cls._c_struct)).contents