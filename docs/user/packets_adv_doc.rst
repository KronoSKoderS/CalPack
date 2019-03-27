Advanced Packet Concepts
========================

.. testsetup:: adv_pkt

    from calpack import models

    class ArrayPacket(models.Packet):
        data = models.ArrayField(models.IntField(), 8)

    my_array_pkt = ArrayPacket()

Creating simple packets with the basic :code:`Fields` one thing but typically packets are more complex.  For example, 
one might want to create a packet with an array of fields, or even encapsulating a packet within another as a field.  
This is easy to do within :code:`calpack` through the use of the :code:`ArrayField` or :code:`PacketField` Fields.  

Creating an Array of :code:`IntField`'s
---------------------------------------
When dealing with a lot of fields that are the same it can become a bear to create each field

.. doctest:: adv_pkt

    >>> class my_long_packet(models.Packet):
    ...     data1 = models.IntField()
    ...     data2 = models.IntField()
    ...     data3 = models.IntField()
    ...     data4 = models.IntField()
    ...     data5 = models.IntField()
    ...     data6 = models.IntField()
    ...     data7 = models.IntField()
    ...     data8 = models.IntField()

This can be simplified by using the :code:`models.ArrayField`

.. doctest:: adv_pkt

    >>> class ArrayPacket(models.Packet):
    ...     data = models.ArrayField(models.IntField(), 8)


Writing to the array requires writing the entire list to the array

.. doctest:: adv_pkt

    >>> my_array_pkt = ArrayPacket()
    >>> my_array_pkt.data = list(range(8))
    >>> my_array_pkt.data
    (0, 1, 2, 3, 4, 5, 6, 7)


Access to individual member is currently readonly

.. doctest:: adv_pkt

    >>> my_array_pkt.data[1] = 12
    Traceback (most recent call last):
      File "<doctest adv_pkt[0]>", line 1, in <module>
        my_array_pkt.data[1] = 12
    TypeError: 'tuple' object does not support item assignment

    >>> print(my_array_pkt.data[1])
    1

Iterating over the field using the for loop is also readonly as well. 

.. doctest:: adv_pkt

    >>> for val in my_array_pkt.data:
    ...     val = 100
    >>> print(my_array_pkt.data)
    (0, 1, 2, 3, 4, 5, 6, 7)

    >>> for i, val in my_array_pkt.data:
    ...     my_array_pkt.data[i] = val * 2
    Traceback (most recent call last):
      File "<doctest adv_pkt[0]>", line 1, in <module>
        my_array_pkt.data[1] = val * 2
    TypeError: 'tuple' object does not support item assignment

Encapsulating another Packet within a Packet
--------------------------------------------
Sometimes you might want to encapsulate another packet within a packet as a field.  This can be done by using the 
:code:`models.PacketField`

.. doctest:: adv_pkt

    >>> class Header(models.Packet):
    ...     source = models.IntField()
    ...     destination = models.IntField()

    >>> class CustomPacket(models.Packet):
    ...     header = models.PacketField(Header)
    ...     spare = models.IntField()
    ...     body = models.ArrayField(models.IntField(), 28)

Access to the fields within the encapsulated packet is as simple as calling that packets members

.. doctest:: adv_pkt

    >>> pkt = CustomPacket()
    >>> pkt.header.source = 1
    >>> pkt.header.source == 1
    True
    >>> pkt.header.destination = 2
    >>> print(pkt.header.destination)
    2