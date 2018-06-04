import unittest
import struct

from calpack.common.ip import *
from calpack.utils import PYPY


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
        if PYPY:
            return True
            
        header = UDP_HEADER_BIG()
        header.source_port = 8080
        header.dest_port = 8080
        header.length = 2
        header.checksum = 0xbeef

        expected_val = struct.pack('>HHHH', 8080, 8080, 2, 0xbeef)

        self.assertEqual(header.to_bytes(), expected_val)

    def test_udp_header_little(self):
        if PYPY: 
            return True

        header = UDP_HEADER_LITTLE(
            source_port = 8080,
            dest_port = 8080,
            length = 2,
            checksum = 0xbeef
        )

        expected_val = struct.pack('<HHHH', 8080, 8080, 2, 0xbeef)

        self.assertEqual(header.to_bytes(), expected_val)


class Test_TCP_HEADER(unittest.TestCase):
    def test_tcp_header_native(self):
        """
        This test verifies the proper structuring of the TCP Header Packet for native endian
        formatting.
        """
        header = TCP_HEADER(
            source_port = 8080,
            dest_port = 8080,
            seq_num = 0xbeefcafe,
            ack_num = 0xcafebeef,
            data_offset = 0xf,
            flag_ns = 1,
            flag_cwr = 1,
            flag_ece = 1,
            flag_urg = 1,
            flag_ack = 1,
            flag_psh = 1,
            flag_rst = 1,
            flag_syn = 1,
            flag_fin = 1,
            window_size = 12,
            checksum = 0xffff
        )

        expected_data = [
            8080, 8080, 0xbeefcafe, 0xcafebeef, int('10001111', 2), 0xff, 12, 0xffff
        ]

        expected_val = struct.pack('HHIIBBHH', *expected_data)

        self.assertEqual(header.to_bytes(), expected_val)


    def test_tcp_header_big(self):
        if PYPY:
            return True

        header = TCP_HEADER_BIG(
            source_port = 8080,
            dest_port = 8080,
            seq_num = 0xbeefcafe,
            ack_num = 0xcafebeef,
            data_offset = 0xf,
            flag_ns = 1,
            flag_cwr = 1,
            flag_ece = 1,
            flag_urg = 1,
            flag_ack = 1,
            flag_psh = 1,
            flag_rst = 1,
            flag_syn = 1,
            flag_fin = 1,
            window_size = 12,
            checksum = 0xffff
        )

        expected_data = [
            8080, 8080, 0xbeefcafe, 0xcafebeef, int('11110001', 2), 0xff, 12, 0xffff
        ]

        expected_val = struct.pack('>HHIIBBHH', *expected_data)

        self.assertEqual(header.to_bytes(), expected_val)

    def test_tcp_header_little(self):
        if PYPY:
            return True

        header = TCP_HEADER_LITTLE(
            source_port = 8080,
            dest_port = 8080,
            seq_num = 0xbeefcafe,
            ack_num = 0xcafebeef,
            data_offset = 0xf,
            flag_ns = 1,
            flag_cwr = 1,
            flag_ece = 1,
            flag_urg = 1,
            flag_ack = 1,
            flag_psh = 1,
            flag_rst = 1,
            flag_syn = 1,
            flag_fin = 1,
            window_size = 12,
            checksum = 0xffff
        )

        expected_data = [
            8080, 8080, 0xbeefcafe, 0xcafebeef, int('10001111', 2), 0xff, 12, 0xffff
        ]

        expected_val = struct.pack('<HHIIBBHH', *expected_data)

        self.assertEqual(header.to_bytes(), expected_val)
