Packet Basics
=============
In this section we cover the basics of how to create a packet and manipulate it contents.

.. todo:: explain differences between python 2 and python 3 ctypes exporting of unsigned integers

Creating a Packet
-----------------
Creating a custom packet requires inheriting the :code:`Packet` class and then defining the Fields within the order 
they are expected to be seen::
    
    from calpack import models

    class Header(models.Packet):
        source = models.IntField()
        dest = models.IntField()
        data1 = models.IntField()
        data2 = models.IntField()

.. Note:: The order in which the fields are set is also the order in which the fields are set within the internal c 
          structure.

Once a packet is defined, creating an instance of that packet allows you to manipulate it::

    my_pkt = Header()

    my_pkt.source = 123
    my_pkt.dest = 456
    my_pkt.data1 = 789

    print(my_pkt.source)
    123

A packet can also be created with fields already populated::

    my_pkt = Header(
        source = 1,
        dest = 2, 
        data1 = 3,
        data2 = 4
    )

    print(my_pkt.source, my_pkt.dest, my_pkt.data1, my_pkt.data2)
    (1, 2, 3, 4)

A packet can then be converted into a byte string::

    my_pkt.to_bytes()
    b'{\x00\xc8\x01\x15\x03\x00\x00'

In reverse, a packet can be created from a byte string array::

    my_parsed_pkt = Header.from_bytes(b'{\x00\xc8\x01\x15\x03\x00\x00')
    print(my_parsed_pkt.source)
    123

    print(my_parsed_pkt.dest)
    456

    my_parsed_pkt == my_pkt
    True

    # Shows that the packets are two different objects
    my_parsed_pkt is my_pkt
    False

Packet fields can be easily copied from and/or compared to other packets of the same Packet subclass::

    my_pkt2 = Header()
    my_pkt2.source = my_pkt.source
    my_pkt2.dest = 654

    my_pkt.source == my_pkt2.source
    True
    
    my_pkt.dest == my_pkt2.dest
    False

Packets themselves can also be compared::

    my_pkt = Header()
    my_pkt.source = 123
    my_pkt.dest = 456
    my_pkt.data1 = 789

    my_pkt2 = Header()
    my_pkt2.source = 123
    my_pkt2.dest = 456
    my_pkt2.data1 = 123

    my_pkt == my_pkt2
    False
    
    my_pkt2.data1 = 789
    my_pkt == my_pkt2 
    True

.. Note:: Comparing two packets that are different classes but may have the same byte output will result in :code:`False`