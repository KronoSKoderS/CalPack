"""
"""

__all__ = [
    'PacketField'
]

from calpack.models.fields.Fields import Field

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