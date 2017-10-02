.. CalPack documentation master file, created by
   sphinx-quickstart on Sun Aug 20 23:51:09 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CalPack: Packets Made Simple
============================
CalPack is the only package you'll need to create, generate and parse packets in an easy to use way.  


Examples
--------
Creating a new packet is as simple as creating a python class::
    
    from calpack import models

    class UDP(models.Packet):
        source_port = models.IntField()
        dest_port = models.IntField()
        length = models.IntField()
        checksum = models.IntField()

Interactiong with the packet and it's field is also simple::

    p = UDP()
    p.source_port = 80
    p.dest_port = 80
    p.length = 8

.. Features
   --------


Index
-----

.. toctree::
   :maxdepth: 2


   modelsdoc


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
