# Concorde
Packets in Python Simplified without compromising speed.

This package is intended to make creating and/or parsing packets on the fly quick and easy.  This is a wrapper around the `cytpes` modules built-in to python.  

## Examples

### Creating a predefined packet:

    import concorde
    
    udp_pkt = concorde.ipv4.udp(
        source_ip = '192.168.0.1',
        dest_ip = '192.168.0.2',
        source_port = 8080,
        dest_port = 8080,
        data = range(100)
    )
    
### Creating Custom Packets
    
    from concorde import packets
    
    
    class my_pkt(packets.Packet):
        _word_size = 32  # default value is 32
        _endian = packets.ENDIAN_BIG
        
        # Word 0
        field0 = packets.uint32()
        
        # Word 1
        field1 = packets.uint16()
        field2 = packets.uint16(bit_len=4)
        field3 = packets.uint16(bit_len=12)
        
        # Words 2 & 3
        field4 = packets.uint64()
        
        # Words 4-10
        field5 = packets.muint32(num_words=7)        
        
### Encapsulating Custom Packets
        
    class my_small_pkt(packet.Packet):
        _word_size = 16
        field1 = packets.uint16()
        field2 = packets.uint16()
        
    class my_big_pkt(packet.Packet):
        _word_size = 32
        field1 = packets.uint32()
        field2 = packets.uint32()
        field3 = my_small_pkt
        
       
You can even mix 'endianess' of the encapsulated packet.
       
    class my_small_pkt(packet.Packet):
        _word_size = 16
        _endian = packets.ENDIAN_LITTLE
        field1 = packets.uint16()
        field2 = packets.uint16()
        
    class my_big_pkt(packet.Packet):
        _word_size = 32
        _endian = packets.ENDIAN_BIG
        field1 = packets.uint32()
        field2 = packets.uint32()
        field3 = my_small_pkt
        