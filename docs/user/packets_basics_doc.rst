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

In this section we cover the basics of how to create a packet and manipulate it contents.

Creating a Packet
-----------------
Creating a custom packet requires inheriting the :code:`Packet` class and then defining the Fields within the order 
they are expected to be seen::

    >>> from calpack import models

    >>> class UDP_Header(models.Packet):
    >>>    source_port = models.IntField16()
    >>>    dest_port = models.IntField16()
    >>>    length = models.IntField16()
    >>>    checksum = models.IntField16()

.. Note:: The order in which the fields are defined is also the order in which the fields are set within the internal c
          structure.

If you desired to have a default value for a particular field, simply use the :code:`default_val` param for the Field::

    >>> class UDP_Header(models.Packet):
    >>>     source_port = models.IntField16(default_val=8888)
    >>>     dest_port = models.IntField16(default_val=8000)
    >>>     length = models.IntField16()
    >>>     checksum = models.IntField16()

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

    >>> my_pkt = UDP_Header(source_port=8080, dest_port=8080, length=0x2, checksum=0x0)

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
