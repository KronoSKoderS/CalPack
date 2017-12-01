.. CalPack documentation master file, created by
   sphinx-quickstart on Sun Aug 20 23:51:09 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CalPack: Packets in Python Simplified
=====================================
CalPack is a module that makes creating and parsing packets easy to do.  This module wraps the 
:code:`ctypes` module into an easier to use interface and enabling more features specific to 
working with Packets.  Think of it as a way to "Transmogrify" your byte data into Packets and 
vice versa:

.. image:: http://assets.amuniversal.com/8d40c700deba01317193005056a9545d
   :target: http://www.gocomics.com/calvinandhobbes/1987/03/23
   :alt: Calvin and Hobbes - Transmorgrifier

Examples
--------
Creating a new packet is as simple as creating a python class::
    
    >>> from calpack import models

    >>> class UDP(models.Packet):
    >>>     source_port = models.IntField()
    >>>     dest_port = models.IntField()
    >>>     length = models.IntField()
    >>>     checksum = models.IntField()


Since :code:`calpak` is a wrapper to :code:`ctypes`, the above class is equivalent to the following 
:code:`ctypes.Structure`::

    >>> import ctypes

    >>> class UDP(ctypes.Structure):
    >>>     _fields_ = [
    >>>         ('source_port', ctypes.c_uint),
    >>>         ('dest_port', ctypes.c_uint),
    >>>         ('length', ctypes.c_uint),
    >>>         ('checksum', ctypes.c_uint),
    >>>     ]

Interacting with the packet and it's field is also simple::

    >>> p = UDP()
    >>> p.source_port = 80
    >>> p.dest_port = 80
    >>> p.length = 8

.. Features
   --------


User Guide
----------
If you've found yourself to be in a bind while using CalPack here is where you want to start.  This is a set of guides
on how to get and use CalPack.  

:doc:`user/index`

CalPack documentation
---------------------
If you're looking for detailed documenation for CalPack's classes and modules then look no further!  You found it!

:doc:`modules/index`
   

Contributing
------------
If you're interested in contributing to CalPack here is where you can learn how

:doc:`dev/index`


Table of Contents
=================
.. toctree::
   :maxdepth: 1

   user/index
   modules/index
   dev/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
