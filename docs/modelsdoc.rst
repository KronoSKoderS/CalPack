=======================================================================================================================
models - a collection of classes and functions to create new custom packets.
=======================================================================================================================

This module is the building blocks for creating packets.  It also provides the ability for users to create custom
fields for their packets.

Creating and working with Custom :code:`Packet`'s
------------------------------------------------

Creating a custom packet requires inheriting the :code:`Packet` class and then defining the Field within the order they are
expected to be seen::
    
    from calpack import models

    class Header(models.Packet):
        source = models.IntField()
        dest = models.IntField()
        data1 = models.IntField()
        data2 = models.IntField()

Once the packet is defined, creating an instance of that packet allows you to manipulate it.  Fields are automatically
set to a 'default' zero'd value::

    my_pkt = Header()

    my_pkt.source = 123
    my_pkt.dest = 456
    my_pkt.data1 = 789

    print(my_pkt.source)  # 123

Packet fields can be easily copied and compared to other packets::

    my_pkt2 = Header()
    my_pkt2.source = my_pkt.source
    my_pkt2.dest = 654

    my_pkt.source == my_pkt2.source  # True
    my_pkt.dest == my_pkt2.dest  # False


Packets themself can also be campared::

    my_pkt = Header()
    my_pkt.source = 123
    my_pkt.dest = 456
    my_pkt.data1 = 789

    my_pkt2 = Header()
    my_pkt2.source = 123
    my_pkt2.dest = 456
    my_pkt2.data1 = 123

    my_pkt == my_pkt2 # False
    my_pkt2.data1 = 789

    my_pkt == my_pkt2 # True

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