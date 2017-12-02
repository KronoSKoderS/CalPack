"""
A collection of classes and function for creating custom :code:`Packet`s.
"""
import ctypes

from collections import OrderedDict

from calpack import PY2
from calpack.models.utils import typed_property
from calpack.models.fields import Field


__all__ = ['Packet']


# This was taken from the six.py source code.  Reason being that I only needed a small part of six
#   and didn't want to rely on the third-party installation just for this package.  I highly
#   recommend looking at them for Python 2/3 compatible coding:  https://github.com/benjaminp/six
#
# WARNING: When I finally decide to migrate away from Python 2 this will be removed.
def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper


class _MetaPacket(type):
    """
    _MetaPacket - A class used to generate the classes defined by the user into a usable class.

    This class is the magic for Turning the :code:`Packet` class definitions into actual operating
    packets.

    The process of how this all works is a little convoluted, however here is a basic overview:

        1. A User has defined a packet through subclassing the `Packet` class
        2. For each `Field` child class:
            - The ctype is created based on bit width and ctypes type
            - The order in which it was defined is saved
            - The bit width of the field is summed
        3. A `ctypes.Structure` is created with :code:`_fields_` in order and type of the Fields.

    In order for this to work, the following are assumed about the defined :code:`Field` classes:

        * c_type is defined with a `ctypes.c_<type>`
        * bit_len
        * create_field_c_tuple
        * py_to_c
        * c_to_py
    """
    def __new__(mcs, clsname, bases, clsdict):
        class_dict = dict(clsdict)

        order = []
        fields_tuple = []

        fields = [
            (field_name, clsdict.get(field_name))
            for field_name, obj in clsdict.items()
            if isinstance(obj, Field)
        ]

        if PY2:
            fields.sort(lambda x, y: cmp(x[1].creation_counter, y[1].creation_counter))

        # for each 'Field' type we're gonna save the order and prep for the c struct
        for name, obj in fields:
            order.append(name)

            obj.field_name = name

            field_tuple = obj.create_field_c_tuple()

            fields_tuple.append(field_tuple)
            class_dict[name] = obj

        # Here we save the order
        class_dict['fields_order'] = order

        # Here we create the internal structure
        class Cstruct(ctypes.Structure):
            pass

        Cstruct._fields_ = fields_tuple
        class_dict['_Packet__c_struct'] = Cstruct

        return type.__new__(mcs, clsname, bases, class_dict)

    @classmethod
    def __prepare__(mcs, clsname, bases, **kwargs):
        return OrderedDict()


@add_metaclass(_MetaPacket)
class Packet(object):
    """
    A super class that custom packet classes MUST inherit from.  This class is NOT intended to be
    used directly, but as a super class.

    Example::

        class Header(models.Packet):
            source = models.IntField()
            dest = models.IntField()
            data1 = models.IntField()
            data2 = models.IntField()


    :param c_pkt: (Optional) a :code:`ctypes.Structure` object that will be used at the internal c
        structure.  This MUST have the same :code:`_fields_` as the Packet would normally have in
        order for it to work properly.
    """
    word_size = typed_property('word_size', int, 16)
    fields_order = []
    bit_len = 0

    __c_struct = ctypes.Structure

    def __init__(self, c_pkt=None, **kwargs):
        # create an internal c structure instance for us to interface with.
        self.__c_pkt = c_pkt
        if c_pkt is  None:
            self.__c_pkt = self.__c_struct()

        # This allows for pre-definition of a field value after packet definition.  We only do this
        #   if the packet isn't from another packet instantiation (i.e. c_pkt was already defined).
        if c_pkt is None:
            for name in self.fields_order:
                d_val = getattr(self.__class__.__dict__[name], 'default_val', None)
                if d_val is not None:
                    setattr(self, name, d_val)

        # This allows for pre-definition of a field value at instantiation.  Note this DOES
        #   overwrite any values passed in from c_pkt
        for key, val in kwargs.items():
            # Only set the keyword args associated with fields.  If it isn't found, then we'll
            #   process like normal.
            if key in self.fields_order:
                setattr(self, key, val)

    @property
    def c_pkt(self):
        """returns the internal c structure object being used"""
        return self.__c_pkt

    def to_bytes(self):
        """
        Converts the packet into a bytes string

        :return: the packet as a byte string
        :rtype: bytes
        """
        return ctypes.string_at(ctypes.addressof(self.__c_pkt), ctypes.sizeof(self.__c_struct))

    @classmethod
    def from_bytes(cls, buf):
        """
        Creates a Packet from a bytes string

        :param bytes buf: the bytes buffer that will be used to create the packet
        :returns: an Instance of the Packet as parsed from the bytes string
        """
        cstring = ctypes.create_string_buffer(buf)
        c_pkt = ctypes.cast(ctypes.pointer(cstring), ctypes.POINTER(cls.__c_struct)).contents
        pkt = cls(c_pkt)

        return pkt

    def __eq__(self, other):
        # if it's not the same packet type
        if not isinstance(other, type(self)):
            return False

        return self.to_bytes() == other.to_bytes()

    def set_c_field(self, field_name, val):
        """
        sets the value of the internal c structure.

        :param str field_name: the name of the field to set
        :param val: a cytpes compatible value to set the field to
        """
        if field_name not in self.fields_order:
            raise AttributeError("'{o}' does not contain field '{n}'".format(o=self, n=field_name))

        setattr(self.__c_pkt, field_name, val)


    def get_c_field(self, field_name):
        """
        gets the value of the field value of the internal c structure.
        :param str field_name: the name of the field to get
        :returns: the field value
        """
        return getattr(self.__c_pkt, field_name)
