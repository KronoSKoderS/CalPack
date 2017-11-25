[![Build Status](https://travis-ci.org/KronoSKoderS/CalPack.svg?branch=prod)](https://travis-ci.org/KronoSKoderS/CalPack) 
[![Coverage Status](https://coveralls.io/repos/github/KronoSKoderS/CalPack/badge.svg?branch=prod)](https://coveralls.io/github/KronoSKoderS/CalPack?branch=dev) 
[![Documentation Status](https://readthedocs.org/projects/concorde/badge/?version=latest)](http://concorde.readthedocs.io/en/latest/?badge=latest)

# CalPack
Packets in Python Simplified.  

This python package is everything you need to transmorgrify your packets:  

[![Calvin and Hobbes Strip](http://assets.amuniversal.com/8d40c700deba01317193005056a9545d)](http://www.gocomics.com/calvinandhobbes/1987/03/23)

This package is intended to make creating and/or parsing packets on the fly quick and easy.  This is a wrapper around 
the [`ctypes` module](https://docs.python.org/dev/library/ctypes.html) built-in to python. This package is designed 
with influence from Django's modeling and will look familiar to those that have used it.

## Why `CalPack`?

Because `Transmorgrifier` takes a REALLY long time to type out.  

## Installation

This package is maintained in [GitHub](https://github.com/KronoSKoderS/CalPack) and packaged for deployment on [PyPi](https://pypi.python.org/pypi/calpack).  

Simply using `pip install calpack` will get this installed.
 
## Examples
### Creating Custom Packets

Creating custom packets is as easy as defining the fields:
    
    from calpack import models
    
    class my_pkt(models.Packet):
        field1 = models.IntField()
        field2 = models.IntField(signed=True)

    pkt = my_pkt()
    pkt.field1 = 12
    pkt.field2 = -12

    # OR directly set the field values:
    other_pkt = my_pkt(
        field1 = 12,
        field2 = -12
    )

### Converting to bytes

    b_str = pkt.to_bytes()
    print(b_str)

### Parsing a byte string into a packet

    pkt2 = my_pkt.from_bytes(b_str)

    print(pkt2.field1)  # 12
    print(pkt2.field2)  # -12

## SHOW ME THE DOCS!
Documentation is host on [read the docs](https://readthedocs.org/projects/concorde/)


## Upcoming Features:
The following list is a set of major features that is planned to be worked on.  For a more exhaustive list, view the
issues page, or if you have ZenHub installed, view our current board. 

- [x] Ability to create a field with multiple words (i.e. a Data Array Field)
- [x] Set the specific bitfield length for the `IntField` (in progress)
- [x] Ability to compare packets for equality
- [x] Ability to set an already defined packet as a field for another packet
- [ ] Builtin packet for commonly used packets, such as TCP/IP, UDP, etc,.
- [ ] Adding other Field types (Float, String, etc,.)


## Python 2 and 3
Currently this module is designed to work for both Python 2.7+ and 3.3+, however, with the term of life for Python 2 in the 
near future, further development of this package will eventually port entirely over to Python 3.
