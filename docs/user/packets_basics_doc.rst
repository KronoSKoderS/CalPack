Packet Basics
=============

.. testsetup:: basic, bytes

    from calpack import models

    class UDP_Header(models.Packet):
        source_port = models.IntField16()
        dest_port = models.IntField16()
        length = models.IntField16()
        checksum = models.IntField16()

    my_pkt = UDP_Header(
        source_port = 8080,
        dest_port = 8080, 
        length = 0x2,
        checksum = 0x0
    )

    class BigUDP_Header(models.PacketBigEndian):
        source_port = models.IntField16()
        dest_port = models.IntField16()
        length = models.IntField16()
        checksum = models.IntField16()

    my_big_pkt = BigUDP_Header(
        source_port = 8080,
        dest_port = 8080,
        length = 0x2,
        checksum = 0x0
    )

    class LittleUDP_Header(models.PacketLittleEndian):
        source_port = models.IntField16()
        dest_port = models.IntField16()
        length = models.IntField16()
        checksum = models.IntField16()
        

    my_little_pkt = LittleUDP_Header(
        source_port = 8080,
        dest_port = 8080,
        length = 0x2,
        checksum = 0x0
    )

In this section we cover the basics of how to create a packet and manipulate it contents.

Creating a Packet
-----------------
Creating a custom packet requires inheriting the :code:`Packet` class and then defining the Fields within the order 
they are expected to be seen

.. doctest:: basic

    >>> from calpack import models

    >>> class UDP_Header(models.Packet):
    ...    source_port = models.IntField16()
    ...    dest_port = models.IntField16()
    ...    length = models.IntField16()
    ...    checksum = models.IntField16()

.. Note:: The order in which the fields are defined is also the order in which the fields are set within the internal c
          structure.

If you desired to have a default value for a particular field, simply use the :code:`default_val` param for the Field

.. doctest:: basic

    >>> class UDP_Header(models.Packet):
    ...     source_port = models.IntField16(default_val=8888)
    ...     dest_port = models.IntField16(default_val=8000)
    ...     length = models.IntField16()
    ...     checksum = models.IntField16()

Upon creation of the Packet instance, any fields that haven't been set but have a default value will be automatically set 
to that default value.  

Accessing and Manipulating the Fields
-------------------------------------

Once a packet is defined, creating an instance of that packet allows you to manipulate it.

.. doctest:: basic

    >>> my_pkt = UDP_Header()

    >>> my_pkt.source_port = 8080
    >>> my_pkt.dest_port = 8080
    >>> my_pkt.length = 0x2
    >>> my_pkt.checksum = 0x0

    >>> print(my_pkt.source_port)
    8080

An instance of a packet can also be created with fields already populated

.. doctest:: basic

    >>> my_pkt = UDP_Header(
    ...     source_port=8080, 
    ...     dest_port=8080, 
    ...     length=0x2, 
    ...     checksum=0x0
    ... )

    >>> print(my_pkt.source_port, my_pkt.dest_port, my_pkt.length, my_pkt.checksum)
    8080 8080 2 0

.. note:: This is different than the :code:`default_val` param.  This value will overwrite that default value.

Packet fields can be easily copied from and/or compared to other packets of the same Packet subclass

.. doctest:: basic

    >>> my_pkt2 = UDP_Header()
    >>> my_pkt2.source_port = my_pkt.source_port
    >>> my_pkt2.dest_port = 8888

    >>> my_pkt.source_port == my_pkt2.source_port
    True

    >>> my_pkt.dest_port == my_pkt2.dest_port
    False

Packets themselves can also be compared

.. doctest:: basic

    >>> my_pkt = UDP_Header()
    >>> my_pkt.source_port = 123
    >>> my_pkt.dest_port = 456
    >>> my_pkt.length = 789

    >>> my_pkt2 = UDP_Header()
    >>> my_pkt2.source_port = 123
    >>> my_pkt2.dest_port = 456
    >>> my_pkt2.length = 123

    >>> my_pkt == my_pkt2
    False

    >>> my_pkt2.length = 789
    >>> my_pkt == my_pkt2
    True

.. Note:: Comparing two packets that are different classes but may have the same byte output will result in :code:`False`

Packets and Byte Strings
------------------------

A packet instance can then be converted into a byte string

.. doctest:: bytes

    >>> my_pkt.to_bytes()
    b'\x90\x1f\x90\x1f\x02\x00\x00\x00'

In reverse, a packet can be created from a byte string array

.. doctest:: bytes

    >>> my_parsed_pkt = UDP_Header.from_bytes(b'\x90\x1f\x90\x1f\x02\x00\x00\x00')
    >>> print(my_parsed_pkt.source_port)
    8080

    >>> print(my_parsed_pkt.dest_port)
    8080

    >>> my_parsed_pkt == my_pkt
    True

    >>> # Show that the packets are two different objects
    >>> my_parsed_pkt is my_pkt
    False


Packet Endianess
----------------

By default, Packets will parse and generate byte data based on the system endianess.  If a specific endianess is
desired, then :code:`PacketBigEndian` or :code:`PacketLittleEndian` can be used to force that endianess.  

Defining a Packet for a particular Endianness is the same as defining a typical Packet, with the exception of using
the desired Endian Packet.  For example:

.. doctest:: bytes

    >>> class BigUDP_Header(models.PacketBigEndian):
    ...     source_port = models.IntField16()
    ...     dest_port = models.IntField16()
    ...     length = models.IntField16()
    ...     checksum = models.IntField16()

    >>> class LittleUDP_Header(models.PacketLittleEndian):
    ...     source_port = models.IntField16()
    ...     dest_port = models.IntField16()
    ...     length = models.IntField16()
    ...     checksum = models.IntField16()


Using the :code:`from_bytes` and :code:`to_bytes` can be used as well.  However, they are now tied to the specific
endianess defined and NOT the system default.  

.. doctest:: bytes

    >>> my_big_pkt = BigUDP_Header(
    ...     source_port = 8080,
    ...     dest_port = 8080,
    ...     length = 0x2,
    ...     checksum = 0x0
    ... )

    >>> my_big_pkt.to_bytes()
    b'\x1f\x90\x1f\x90\x00\x02\x00\x00'

    >>> my_little_pkt = LittleUDP_Header.from_bytes(b'\x90\x1f\x90\x1f\x02\x00\x00\x00')
    >>> my_little_pkt.source_port == 8080
    True

    >>> my_little_pkt.dest_port == 8080
    True

    >>> my_little_pkt.length
    2    

    >>> my_little_pkt.to_bytes()
    b'\x90\x1f\x90\x1f\x02\x00\x00\x00'
