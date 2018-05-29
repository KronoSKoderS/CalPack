import unittest
import struct

from calpack.common.ip import *


class Test_UDP_HEADER(unittest.TestCase):
    def test_udp_header_native(self):
        """
        This test verifies the proper structuring of the UDP Header Packet for native endian
        formatting.
        """
        header = UDP_HEADER(
            source_port = 8080,
            dest_port = 8080,
            length = 2,
            checksum = 0xbeef
        )

        expected_val = struct.pack('HHHH', 8080, 8080, 2, 0xbeef)

        self.assertEqual(header.to_bytes(), expected_val)

    def test_udp_header_big(self):
        header = UDP_HEADER_BIG()
        header.source_port = 8080
        header.dest_port = 8080
        header.length = 2
        header.checksum = 0xbeef

        expected_val = struct.pack('>HHHH', 8080, 8080, 2, 0xbeef)

        self.assertEqual(header.to_bytes(), expected_val)

    def test_udp_header_little(self):
        header = UDP_HEADER_LITTLE(
            source_port = 8080,
            dest_port = 8080,
            length = 2,
            checksum = 0xbeef
        )

        expected_val = struct.pack('<HHHH', 8080, 8080, 2, 0xbeef)

        self.assertEqual(header.to_bytes(), expected_val)