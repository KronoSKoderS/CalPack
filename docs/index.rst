.. CalPack documentation master file, created by
   sphinx-quickstart on Sun Aug 20 23:51:09 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CalPack: Packets in Python Simplified
=====================================
CalPack is the only package you'll need to create, generate and parse packets in an easy to use way.  This module wraps
the :code:`ctypes` module into an easier to use interface and enabling more features specific to working with Packets.

.. image:: http://assets.amuniversal.com/8d40c700deba01317193005056a9545d
   :target: http://www.gocomics.com/calvinandhobbes/1987/03/23
   :alt: Calvin and Hobbes - Transmorgrifier

Examples
--------
Creating a new packet is as simple as creating a python class::
    
    from calpack import models

    class UDP(models.Packet):
        source_port = models.IntField()
        dest_port = models.IntField()
        length = models.IntField()
        checksum = models.IntField()


Since :code:`calpak` is a wrapper to :code:`ctypes`, the above class is equivalent to the following 
:code:`ctypes.Structure`::

    import ctypes

    class UDP(ctypes.Structure):
        _fields_ = [
            ('source_port', ctypes.c_uint),
            ('dest_port', ctypes.c_uint),
            ('length', ctypes.c_uint),
            ('checksum', ctypes.c_uint),
        ]

Interacting with the packet and it's field is also simple::

    p = UDP()
    p.source_port = 80
    p.dest_port = 80
    p.length = 8

.. Features
   --------


User Guide
----------
Here you'll find an extensive guide on how to use :code:`calpack`.  

.. toctree::
   :maxdepth: 2

   user/intro_and_install_doc
   user/packets_basics_doc
   user/packets_adv_doc
   user/fields_builtin_doc
   user/fields_custom_doc

CalPack documentation
---------------------
If you're looking for detailed documenation for CalPack's classes and modules then look no further!  You found it!

.. toctree::
   :maxdepth: 2

   modules/models_doc

Contributing
------------
If you're interested in contributing to CalPack here is where you can learn how

.. toctree::
   :maxdepth: 2

   dev/intro_dev_doc
   dev/tools_doc
   dev/contributions_doc


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
