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

But why CalPack?  My first born is named Calvin and I wanted to name something after him as a
tribute to him.  Secondly, typing out :code:`transmogrifier` is a nightmare.  Finally, who
doesn't like Calvin and Hobbes?


Installation
============
CalPack is hosted on pypi and can be installed by simply using :code:`pypi`::

    >>> pypi install CalPack

You can also install from the GitHub repo source::

    >>> git clone https://github.com/KronoSKoderS/CalPack.git
    >>> cd CalPack
    >>> python setup.py install
