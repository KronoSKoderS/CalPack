import ctypes

_no_type = object()

def typed_property(name, expected_type):
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


class __MetaPacket(type):
    pass

class Packet():
    __metaclass__ = __MetaPacket
    pass


class Field():
    _acceptable_params = ['bit_len', 'num_words']
    _c_type = None
    _type = _no_type
    def __init__(self, **kwargs):
        for k, v, in kwargs.items():
            if k not in self._acceptable_params:
                raise KeyError("`{k}` is not an accepted parameter for {cls}".format(k=k, cls=self.__class__))


class IntField(Field):
    _unsigned = typed_property('unsigned', bool)
    _little_endian = typed_property('little_endian', bool)

    def __init__(self, **kwargs):
        self._acceptable_params += ['little_endian', 'unsigned']
        super(IntField, self).__init__(**kwargs)

        self._little_endian = kwargs.get('little_endian', False)
        self._unsigned = kwargs.get('unsigned', False)
        if self._unsigned:
            self._c_type = ctypes.c_uint64
        else:
            self._c_type = ctypes.c_int64


class ReservedField(Field):
    pass