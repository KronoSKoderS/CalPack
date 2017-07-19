from concorde import packets as pkts
from concorde import packets as pkts


class IPv4(pkts.Packet):
    _word_length = 32
    
    # Word 0
    source_addr = pkts.IntField(size=32)

    # Word 1
    dest_addr = pkts.IntField(size=32)

    # Word 2
    reserved_1 = pkts.IntField(size=8, is_reserved=True, val=0)
    protocol = pkts.IntField(size=8)
    length = pkts.IntField(size=16)


class UDPv4(IPv4):
    """description of class"""

    # Header:
    # Word 3
    source_port = pkts.IntField(size=16)
    dest_port = pkts.IntField(size=16)

    # Word 4
    length = pkts.IntField(size=16)

    # TODO: Add Checksum Field?
    checksum = pkts.IntField(size=16)

    # Word 5



