Introduction (A Brief History)
==============================
.. image:: http://assets.amuniversal.com/cc713730deb701317193005056a9545d
   :target: http://www.gocomics.com/calvinandhobbes/1985/11/18
   :alt: Calvin and Hobbes humble beginnings (Tiger Trap)

CalPack was created out of necessity for creating a way to parse custom packets in the space 
industry.  These packets, typically stored in binary data files, would come from multiple 
unique interfaces (e.g. 1553) or common ones (e.g. UDP) with very custom data structures.  

Naturally, :code:`ctypes` was the first place I went to, but inspecting packet definitions 
using the syntax that :code:`ctypes` used was confusing and not easy to use.  Autocompletion
of IDE's didn't pick up the field names and the reader had to have a basic knowledge of 
:code:`ctypes`.  And then CalPack was born.  

But why call it CalPack?  My first born is named Calvin and I wanted to name something after 
him as a tribute to him.  Secondly, I'm a huge Calvin and Hobbes fan.  Finally, typing out 
:code:`transmogrifier` is a nightmare.

An Example
----------

If you're not familiar with custom packets and why CalPack was needed, here's a quick example.
Let's imagine we want to "smartify" your washing machine.  If you're like me, there are probably
multiple times where you've forgotten about the laundry load, opened it to load a new load and 
realized the load was sour.  Wouldn't it be nice to have an app to send you a notification when 
a load is done, and another at a preset time to remind you it might start getting sour?

For this example, we won't worry about the actual app or the monitoring hardward, but to 
communicate between the two, we're going to need to send some custom packets to do the following:
    
    * Packets sent to the machine called 'commands':
        * Set the 'preset' time for warning that a load might go sour
        * Query 'status' of the machine
    * Return packets:
        * Confirmation a command was accepted
        * 'Status' or telemetry from the machine


Let's also assume we use the .. _User Datagram Protocol (UDP): https://en.wikipedia.org/wiki/User_Datagram_Protocol#Packet_structure
for structuring our packets.  This means we'll have a header that looks like this:

+-------------------------------------------------------------------------------------------------------------------------------+
|                                                          UDP Packet Header                                                    |
+-------------------------------+-----------------------------------------------------------------------------------------------+
|           Byte 0              |           Byte 1              |           Byte 2              |           Byte 3              |
+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+
| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                   Source Port                                 |                   Dest Port                                   |
+---------------------------------------------------------------+---------------------------------------------------------------+
|                   Length                                      |                   Checksum                                    |
+---------------------------------------------------------------+---------------------------------------------------------------+
|                                                             Data 1                                                            |
+-------------------------------------------------------------------------------------------------------------------------------+
|                                                              ...                                                              |
+-------------------------------------------------------------------------------------------------------------------------------+
|                                                             Data N                                                            |
+-------------------------------------------------------------------------------------------------------------------------------+


Now let's fill in the Data words with things that have more meaning to our particular case.  Let's define 

Installation
============
CalPack is hosted on pypi and can be installed by simply using :code:`pypi`::

    >>> pypi install CalPack

You can also install from the GitHub repo source::

    >>> git clone https://github.com/KronoSKoderS/CalPack.git
    >>> cd CalPack
    >>> python setup.py install
