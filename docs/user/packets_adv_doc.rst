Advanced Packet Concepts
========================
Creating simple packets with the basic :code:`Fields` one thing but typically packets are more complex.  For example, 
one might want to create a packet with an array of fields, or even encapsulating a packet within another as a field.  
This is easy to do within :code:`calpack` through the use of the :code:`ArrayField` or :code:`PacketField` Fields.  

Creating an Array of :code:`IntField`'s
---------------------------------------
When deal with a lot of fields that are the same it can become a bear to create each field::

    class my_long_packet(models.Packet):
        data1 = models.IntField()
        data2 = models.IntField()
        data3 = models.IntField()
        data4 = models.IntField()
        data5 = models.IntField()
        data6 = models.IntField()
        data7 = models.IntField()
        data8 = models.IntField()

This can be simplified by using the :code:`models.ArrayField`::

    class ArrayPacket(models.Packet):
        data = models.ArrayField(models.IntField(), 8)


Accessing the elements in the ArrayField is similar to that of a python list::

    my_array_pkt = ArrayPacket()
    my_array_pkt.data[0] = 123
    print(my_array_pkt.data[0])
    123

    my_array_pkt.data = list(range(8))
    print(my_array_pkt.data)
    [0, 1, 2, 3, 4, 5, 6, 7]

    for val in my_array_pkt.data:
        val = 100

    print(my_array_pkt.data)
    [100, 100, 100, 100, 100, 100, 100, 100]

Encapsulating another Packet within a Packet
--------------------------------------------
Sometimes you might want to encapsulate another packet within a packet as a field.  This can be done by using the 
:code:`models.PacketField`::

    class Header(models.Packet):
        source = models.IntField()
        destination = models.IntField()

    class CustomPacket(models.Packet):
        header = models.PacketField(Header)
        spare = models.IntField()
        body = models.ArrayField(models.IntField(), 28)

Access to the fields within the encapsulated packet is as simple as calling that packets members::

    pkt = CustomPacket()
    pkt.header.source = 1
    pkt.header.destination = 2