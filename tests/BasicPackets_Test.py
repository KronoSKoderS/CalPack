import unittest
import struct

from random import randint

from calpack import models


class TestSimplePackets(unittest.TestCase):
    def setUp(self):
        class two_int_field_packet(models.Packet):
            int_field = models.IntField()
            int_field_signed = models.IntField(signed=True)

        self.two_int_field_packet = two_int_field_packet

    def test_set_simple_int_fields(self):
        p = self.two_int_field_packet()

        v1 = randint(0, 65536)
        v2 = randint(-32768, 32767)

        p.int_field = v1
        p.int_field_signed = v2

        self.assertEqual(p.int_field, v1)
        self.assertEqual(p.int_field_signed, v2)

    def test_field_raises_TypeError_when_setting_non_int_value(self):
        p = self.two_int_field_packet()
        
        with self.assertRaises(TypeError):
            p.int_field = ""

    def test_set_valid_from_other_field(self):
        p = self.two_int_field_packet()
        p2 = self.two_int_field_packet()

        v1 = randint(0, 65536)
        
        p.int_field = v1

        p2.int_field = p.int_field

        self.assertEqual(p.int_field, p2.int_field)


    def test_create_class_from_bytes_string(self):
        v1 = randint(0, 65536)
        v2 = randint(-32768, 32767)
        vals = [v1, v2]
        b_val = struct.pack('Hh', *vals)

        p = self.two_int_field_packet.from_bytes(b_val)

        self.assertEquals(p.int_field, vals[0])
        self.assertEquals(p.int_field_signed, vals[1])

    def test_export_to_bytes_string(self):
        v1 = randint(0, 65536)
        v2 = randint(-32768, 32767)
        vals = [v1, v2]
        b_val = struct.pack('Hh', *vals)

        p = self.two_int_field_packet()
        p.int_field = vals[0]
        p.int_field_signed = vals[1]

        pkt_bin = p.to_bytes()

        self.assertEquals(pkt_bin, b_val)

    def test_to_bytes_string_then_import_from_binary(self):
        v1 = randint(0, 65536)
        v2 = randint(-32768, 32767)
        vals = [v1, v2]

        p = self.two_int_field_packet()
        p.int_field = vals[0]
        p.int_field_signed = vals[1]

        p2 = self.two_int_field_packet.from_bytes(p.to_bytes())

        self.assertEquals(p.int_field, p2.int_field)
        self.assertEquals(p.int_field_signed, p2.int_field_signed)


    def test_class_raises_KeyError_when_using_invalid_key_words(self):
        with self.assertRaises(KeyError):
            class invalid_pkt(models.Packet):
                inv_field = models.IntField(keyword_that_dont_exist=100)

    def test_check_word_size(self):
        p = self.two_int_field_packet()
        self.assertEquals(p.num_words, 2)


## TDD: Prototyping for encapsulated packets.
# class TestAdvancedPackets(unittest.TestCase):
#     def setUp(self):
#         pass
#
#     def test_encapsulated_pkt(self):
#         class simple_pkt(models.Packet):
#             field1 = models.IntField(num_words=10)
#
#         class adv_pkt(models.Packet):
#             field2 = simple_pkt
#
#         p = adv_pkt()
#
#         # Verify abilily to access and set encap packets fields
#         p.field2.field1 = 100
#
#         self.assertEquals(p.field2.field1, 100)
#
#         sp = simple_pkt()
#         sp.field1 = 200
#
#         p.field2 = sp
#
#         self.assertEquals(p.field2.field1, 200)


if __name__ == '__main__':
    unittest.main()
