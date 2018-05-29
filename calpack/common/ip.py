from calpack import models

__all__ = [
    'UDP_HEADER', 'UDP_HEADER_BIG', 'UDP_HEADER_LITTLE'
]

class UDP_HEADER(models.Packet):
    """
    UDP HEADER class.  A simple packet class representing the UDP Header.
    """
    source_port = models.IntField16()
    dest_port = models.IntField16()
    length = models.IntField16()
    checksum = models.IntField16()


class UDP_HEADER_BIG(UDP_HEADER, models.PacketBigEndian):
    pass


class UDP_HEADER_LITTLE(UDP_HEADER, models.PacketLittleEndian):
    pass
#class TCP_HEADER(models.Packet):
#    _word_size = 32

#    # Word 0
#    source_port = models.IntField(bit_len=16)
#    dest_port = models.IntField(bit_len=16)
    
#    # Word 1
#    seq_num = models.IntField()
    
#    # Word 2
#    ack = models.IntField()
    
#    # Word 3
#    data_offset = models.IntField(bit_len=4)
#    reserved = models.ReservedField(bit_len=3)
#    ns = models.BoolField()
#    cwr = models.BoolField()
#    ece = models.BoolField()
#    urg = models.BoolField()
#    ack = models.BoolField()
#    psh = models.BoolField()
#    rst = models.BoolField()
#    syn = models.BoolField()
#    fin = models.BoolField()
#    windows_size = models.IntField(bit_len=16)

#    # Word 4
#    checksum = models.ChecksumField(bit_len=16)
#    urg_pointer = models.IntField(bit_len=16)


#class IPv4(models.Packet):
#    _word_length = 32
    
#    # Word 0
#    source_addr = pkts.IntField(size=32)

#    # Word 1
#    dest_addr = pkts.IntField(size=32)

#    # Word 2
#    reserved_1 = pkts.IntField(size=8, is_reserved=True, val=0)
#    protocol = pkts.IntField(size=8)
#    length = pkts.IntField(size=16)


#class UDPv4(IPv4):
#    """description of class"""

#    # Header:
#    # Word 3
#    source_port = pkts.IntField(size=16)
#    dest_port = pkts.IntField(size=16)

#    # Word 4
#    length = pkts.IntField(size=16)

#    # TODO: Add Checksum Field?
#    checksum = pkts.IntField(size=16)

#    # Word 5



