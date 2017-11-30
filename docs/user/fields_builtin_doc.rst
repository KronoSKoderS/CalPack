Packet Fields
=============
:code:`calpack` comes with some built-in :code:`Field` classes that can be used right away.

.. todo:: Update fields with newly created fields

:code:`IntField`
----------------
The :code:`IntField` is used to represent an integer.  In the backend, this field uses the :code:`ctypes.c_int64` or 
:code:`ctypes.c_uint64` depending on whether the field is configured as signed or not.  This is done by passing the 
:code:`signed` parameter to the :code:`IntField`::

    int_field = models.IntField(signed=True)

.. Note:: :code:`IntField` is unsigned as a default. 
.. Warning:: If a signed value is set to an unsigned value (e.g any value less than 0) a :code:`TypeError` will be raised.
.. Warning:: although the example above defines a field outside of a Packet, this **cannot** be done in practice as each field
    within the packet **must** be a new instance of a Field.  

If a specific bit length is desired, passing the :code:`bit_len` parameter to the desired length::

    int_field = models.IntField(bit_len=8)

.. Note:: the default value for :code:`bit_len` is 16
.. Warning:: If bit_len is less than or equal 0 or greater than 64 a :code:`ValueError` will be raised.  
.. Warning:: although the example above defines a field outside of a Packet, this **cannot** be done in practice as each field
    within the packet **must** be a new instance of a Field. 

:code:`ArrayField`
------------------

.. todo:: Warn user that certain types of fields can't be used in an ArrayField
.. todo:: explain the workaround for the fields that can't be used
.. todo:: update example with a valid one

The :code:`ArrayField` is used to create an array of fields.  When creating the :code:`ArrayField` two parameters must
be passed:

    1. An instance of the Field to be used
    2. The size of the Array

Example::

    array_field = models.ArrayField(
        # Note that this is an **instance** of the IntField
        models.IntField(bit_len=8, signed=True)  
        12
    )

.. Note:: It's important to that the first argument is an **instance** of the Field and not the class
.. Warning:: although the example above defines a field outside of a Packet, this **cannot** be done in practice as each field
    within the packet **must** be a new instance of a Field. 

Interacting with the :code:`ArrayField` is similar to that of a python list where :code:`len` and individual member 
access can be done.  The Field instance for the first parameter of the :code:`ArrayField` can also be a 
:code:`PacketField`::

    class Point(models.Packet):
        x = models.IntField(bit_len=8)
        y = models.IntField(bit_len=8)

    class ArrayPacket(models.Packet):
        points = models.ArrayField(
            models.PacketField(Point),
            8
        )

    pkt = ArrayPacket()

    for i, point in enumerate(pkt.points):
        point.x = i
        point.y = len(pkt.points) - 1

    print([pkt.points[i].x, pkt.points[i].y for i in range(len(pkt.points))])
    [(0, 8), (1, 7), (2, 6), (3, 5), (4, 4), (5, 3), (6, 2), (7, 1)]

Accessing the members of an :code:`ArrayField` with a :code:`PacketField` as the field type will be accessing instances
of those packets::

    class ArrayPacket(models.Packet):
        points = array_field


    pkt = ArrayPacket()
    pkt.points[0].x = 100
    print(pkt.points[0].x)
    100

    print(pkt.points[0].y)
    0  # default value of IntField

:code:`PacketField`
-------------------
The :code:`PacketField` is used to encapsulate another already defined packet.  The encapsulation of packets can be 
done multiple times as well::

    class Point(models.Packet):
        x = models.IntField(bit_len=8)
        y = models.IntField(bit_len=8)

    class Rectangle(models.Packet):
        top_left = models.PacketField(Point)
        top_right = models.PacketField(Point)
        bot_left = models.PacketField(Point)
        bot_right = models.PacketField(Point)

    class TwoRectangles(models.Packet):
        first_rect = models.PacketField(Rectangle)
        second_rect = models.PacketField(Rectangle)