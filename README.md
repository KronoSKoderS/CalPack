[![Build Status](https://travis-ci.org/KronoSKoderS/CalPack.svg?branch=prod)](https://travis-ci.org/KronoSKoderS/CalPack)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d9b9123821ad408aaf1bd09ba15bbe6c)](https://www.codacy.com/app/kronoskoders/CalPack?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=KronoSKoderS/CalPack&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/KronoSKoderS/CalPack/badge.svg?branch=prod)](https://coveralls.io/github/KronoSKoderS/CalPack?branch=dev)
[![Documentation Status](https://readthedocs.org/projects/concorde/badge/?version=latest)](http://concorde.readthedocs.io/en/latest/?badge=latest)

# CalPack

Packets in Python Simplified.

This python package is everything you need to "transmorgrify" your packets:

[![Calvin and Hobbes Strip](http://assets.amuniversal.com/8d40c700deba01317193005056a9545d.png)](http://www.gocomics.com/calvinandhobbes/1987/03/23)

This package is intended to make creating and/or parsing packets (structured bytecode) on the fly quick and easy.  This is a wrapper around
the [`ctypes` module](https://docs.python.org/dev/library/ctypes.html) built-in to python. This package is designed
with influence from Django's modeling and will look familiar to those that have used it.

## A quick explanation of Packets and how to use them

Packets are structured bytecode used for passing information from one place to another.  The most common example is
that of a TCP/IP Packet, but isn't necessarily limited to networking packets.  Here's a quick example.  Let's say we
want to make a "smart" washing machine by attaching a [Raspberry Pi](https://www.raspberrypi.org/) that then talks to your other smart devices and alerts
you when a load of laundry is done and how many loads of laundry you've done that day.

![Example Diagram](https://i.imgur.com/EcRl4HP.png)

One way to communicate between the Raspberry Pi and your other devices is to send status "packets" or byte data
across a network.  Let's say we want to know the following in our packet:

* Status - a Boolean that represents whether the Washing Machine is running or stopped
* Number of Loads - an Integer that represents the number of loads done that day

To create this packet in `CalPack` is simple:

```python
from calpack import models

class MachineStatus(models.Packet):
    Status = models.BooleanField()
    Num_Loads = models.IntField()
```

On our monitoring device (the Raspberry Pi), we can easily create the byte data for the packet by using our new packet:

```python
status_pkt = MachineStatus(
    Status=True,
    Num_Loads=12
)

# Send the byte data using an assumed custom `send` funcion
send(status_pkt.to_bytes())
```

And converting the recieved byte data is simple as well:

```python
# assuming a `receive` function and returns the byte data of the sent packet
received_data = MachineSatus.from_bytes(receive())
print(received_data.status)
```

## Installation

This package is maintained in [GitHub](https://github.com/KronoSKoderS/CalPack) and packaged for deployment on [PyPi](https://pypi.python.org/pypi/calpack).

Simply using `pip install calpack` will get this installed.

## SHOW ME THE DOCS

Documentation is host on [read the docs](https://readthedocs.org/projects/concorde/)

## Python 2 and 3

Currently this module is designed to work for both Python 2.7+ and 3.3+, however, with the term of life for Python 2 nearing,
this package will eventually port entirely over to Python 3.
