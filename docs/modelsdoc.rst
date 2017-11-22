models - a collection of classes and functions to create new custom packets.
=======================================================================================================================

2. Built-in Fields
    - IntField
    - ArrayField
    - PacketField
3. Creating Custom Fields
    - required class properties
    - the python and c interface
    - 

This module is the building blocks for creating packets by using builtin and custom fields.  It also provides the 
ability for users to create custom fields for their packets.

Packet Basics
-------------
Creating a custom packet requires inheriting the :code:`Packet` class and then defining the Fields within the order 
they are expected to be seen::
    
    from calpack import models

    class Header(models.Packet):
        source = models.IntField()
        dest = models.IntField()
        data1 = models.IntField()
        data2 = models.IntField()

Once a packet is defined, creating an instance of that packet allows you to manipulate it::

    my_pkt = Header()

    my_pkt.source = 123
    my_pkt.dest = 456
    my_pkt.data1 = 789

    print(my_pkt.source)
    123

A packet can then be converted into a byte string::

    my_pkt.to_bytes()
    b'{\x00\xc8\x01\x15\x03\x00\x00'

Further more a packet can be created from a byte string array::

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

Packet fields can be easily copied and compared to other packets::

    my_pkt2 = Header()
    my_pkt2.source = my_pkt.source
    my_pkt2.dest = 654

    my_pkt.source == my_pkt2.source
    True
    
    my_pkt.dest == my_pkt2.dest
    False

Packets themself can also be compared::

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


Advanced Packet Concepts
------------------------
2. Advanced Packet Concepts
    - Using the ArrayField 
    - Creating encapsulated packets

Creating simple packets with the basic :code:`Fields` one thing but typically packets are more complex.  For example, 
one might want to create a packet with an array of fields, or even encapsulating a packet within another as a field.  
This is easy to do within :code:`calpack` through the use of the :code:`ArrayField` or :code:`PacketField` Fields.  

Creating an Array of :code:`IntField`'s
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Given the following packet::

    class my_long_packet(models.Packet):
        data1 = models.IntField()
        data2 = models.IntField()
        data3 = models.IntField()
        data4 = models.IntField()
        data5 = models.IntField()
        data6 = models.IntField()
        data7 = models.IntField()
        data8 = models.IntField()

This can be simplified by using the following syntax::

    class my_array_packet(models.Packet):
        data = models.ArrayField(models.IntField(), 8)



Creating Custom :code:`Field`'s
---------------------------------
Within your custom  :code:`Field` you can customize the following functions:

        * create_field_c_tuple
        * bit_len
        * py_to_c
        * c_to_py

:code:`create_field_c_tuple`

.. TODO:: Update section

:code:`bit_len`

.. TODO:: Update section

:code:`py_to_c`

.. TODO:: Update section

:code:`c_to_py`

.. TODO:: Update section

Class/Function specific Docs
----------------------------

.. automodule:: models
   :members: