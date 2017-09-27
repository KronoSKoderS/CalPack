# CalPack
Packets in Python Simplified.  

This package is intended to make creating and/or parsing packets on the fly quick and easy.  This is a wrapper around the `cytpes` modules built-in to python. 
This package is designed with influence from Django's modeling and will look familar to those that have used it. 

## Installation

This package is maintained in [GitHub](https://github.com/KronoSKoderS/CalPack) and packaged for deployment on [PyPi](https://pypi.python.org/pypi/calpack).  

Simply using `pip install calpack` will get this installed.  
 
## Examples
### Creating Custom Packets
    
    from calpack import models
    
    
    class my_pkt(models.Packet):
        field1 = models.IntField()
        field2 = models.IntField(signed=True)


    pkt = my_pkt()

    pkt.field1 = 12
    pkt.field2 = -12


### Converting to bytes

    b_str = pkt.to_bytes()
    print(b_str)

### Parsing a byte string into a packet

    pkt2 = my_pkt.from_bytes(b_str)

    print(pkt2.field1)  # 12
    print(pkt2.field2)  # -12



## Upcoming Features:

The following list is a set of major features that is planned to be worked on.  For a more exhautive list, view the issues page, or if you have ZenHub
installed, view our current board. 

- Ability to create a field with multiple words (i.e. a Data Array Field)
- Set the specific bitfield length for the `IntField` (in progress)
- Ability to compare packets for equality
- Ability to set an already defined packet as a field for another packet
- Builtin packet for commonly used packets, such as TCP/IP, UDP, etc,.
- Adding other Field types (Float, String, etc,.)