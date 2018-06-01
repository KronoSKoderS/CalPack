"""
example.py

This is a simple example of how to create and send a raw packet using Python's scoket networking
module and 
"""

import socket

from calpack import models


class WashingMachineTelemetry(models.Packet):
    status = models.BoolField()
    num_loads = models.IntField16()


tlm = WashingMachineTelemetry(
    status=False,
    num_loads=0
)


# Client code.  Comment the server code and run this first.
client = socket.socket(socket.AF_INET, socket.SOCK_RAW)
client.connect(("127.0.0.1", 8080))
client.recv(4096)

# Server code.  Comment the client code and run this second.
server = socket.socket(socket.AF_INET, socket.SOCK_RAW)
server.connect(("127.0.0.1", 8080))
server.send(tlm.to_bytes())


# Here's an example of appending the custom packet with the UDP Header

from calpack.common.ip import UDP_HEADER

class WashingMachinePacket(models.Packet):
    udp_header = models.PacketField(UDP_HEADER)
    telem = models.PacketField(WashingMachineTelemetry)

tlm_pkt = WashingMachinePacket()
tlm_pkt.udp_header.source_port = 8080
tlm_pkt.udp_header.dest_port = 8080
tlm_pkt.udp_header.length = len(tlm)

# We directly set the tlm packet we used previously
tlm_pkt.telem = tlm