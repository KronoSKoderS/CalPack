"""
A collection of common IP headers (i.e. TCP and UDP) created using the calpack.Packet class.
"""

from calpack import models
from calpack.utils import PYPY

if PYPY:
    PacketBigEndian = models.Packet
    PacketLittleEndian = models.Packet
else:
    PacketBigEndian = models.PacketBigEndian
    PacketLittleEndian = models.PacketLittleEndian

__all__ = ['UDP_HEADER', 'TCP_HEADER']

if not PYPY:
    __all__ += ['UDP_HEADER_BIG', 'UDP_HEADER_LITTLE', 'TCP_HEADER_BIG', 'TCP_HEADER_LITTLE']


class UDP_HEADER(models.Packet):
    """
    UDP HEADER class.  A simple packet class representing the UDP Header.  This packet uses native
    byte ordering.
    """
    source_port = models.IntField16()
    dest_port = models.IntField16()
    length = models.IntField16()
    checksum = models.IntField16()


class UDP_HEADER_BIG(UDP_HEADER, PacketBigEndian):
    """
    UDP HEADER class.  A simple packet class representing the UDP Header.  This packet uses big
    endian byte ordering.
    """
    pass


class UDP_HEADER_LITTLE(UDP_HEADER, PacketLittleEndian):
    """
    UDP HEADER class.  A simple packet class representing the UDP Header.  This packet uses little
    endian byte ordering.
    """
    pass


class TCP_HEADER(models.Packet):
    """
    UDP HEADER class.  A simple packet class representing the UDP Header.  This packet uses native
    byte ordering.
    """
    source_port = models.IntField16()
    dest_port = models.IntField16()
    seq_num = models.IntField32()
    ack_num = models.IntField32()
    data_offset = models.IntField8(bit_len=4)
    reserved = models.IntField8(bit_len=3)
    flag_ns = models.IntField8(bit_len=1)
    flag_cwr = models.IntField8(bit_len=1)
    flag_ece = models.IntField8(bit_len=1)
    flag_urg = models.IntField8(bit_len=1)
    flag_ack = models.IntField8(bit_len=1)
    flag_psh = models.IntField8(bit_len=1)
    flag_rst = models.IntField8(bit_len=1)
    flag_syn = models.IntField8(bit_len=1)
    flag_fin = models.IntField8(bit_len=1)
    window_size = models.IntField16()
    checksum = models.IntField16()


class TCP_HEADER_BIG(TCP_HEADER, PacketBigEndian):
    """
    UDP HEADER class.  A simple packet class representing the UDP Header.  This packet uses big
    byte ordering.
    """
    pass


class TCP_HEADER_LITTLE(TCP_HEADER, PacketLittleEndian):
    """
    UDP HEADER class.  A simple packet class representing the UDP Header.  This packet uses little
    byte ordering.
    """
    pass
