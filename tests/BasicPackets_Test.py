import unittest
import struct

from random import randint

from calpack import models


class TestIntField(unittest.TestCase):
    def setUp(self):
        class two_int_field_packet(models.Packet):
            int_field = models.IntField()
            int_field_signed = models.IntField(signed=True)

        self.two_int_field_packet = two_int_field_packet

    def test_set_valid_values_int_fields(self):
        p = self.two_int_field_packet()

        v1 = randint(0, 65535)
        v2 = randint(-32768, 32767)

        p.int_field = v1
        p.int_field_signed = v2

        self.assertEqual(p.int_field, v1)
        self.assertEqual(p.int_field_signed, v2)

    def test_field_raises_TypeError_when_setting_non_int_value(self):
        p = self.two_int_field_packet()
        
        with self.assertRaises(TypeError):
            p.int_field = ""

    def test_set_valid_value_from_other_field(self):
        p = self.two_int_field_packet()
        p2 = self.two_int_field_packet()

        v1 = randint(0, 65535)
        
        p.int_field = v1

        p2.int_field = p.int_field

        self.assertEqual(p.int_field, p2.int_field)

    def test_create_class_from_bytes_string(self):
        v1 = randint(0, 65535)
        v2 = randint(-32768, 32767)
        vals = [v1, v2]
        b_val = struct.pack('Hh', *vals)

        p = self.two_int_field_packet.from_bytes(b_val)

        self.assertEquals(p.int_field, vals[0])
        self.assertEquals(p.int_field_signed, vals[1])

    def test_export_to_bytes_string(self):
        v1 = randint(0, 65535)
        v2 = randint(-32768, 32767)
        vals = [v1, v2]
        b_val = struct.pack('Hh', *vals)

        p = self.two_int_field_packet()
        p.int_field = vals[0]
        p.int_field_signed = vals[1]

        pkt_bin = p.to_bytes()

        self.assertEquals(pkt_bin, b_val)

    def test_to_bytes_string_then_import_from_binary(self):
        v1 = randint(0, 65535)
        v2 = randint(-32768, 32767)
        vals = [v1, v2]

        p = self.two_int_field_packet()
        p.int_field = vals[0]
        p.int_field_signed = vals[1]

        p2 = self.two_int_field_packet.from_bytes(p.to_bytes())

        self.assertEquals(p.int_field, p2.int_field)
        self.assertEquals(p.int_field_signed, p2.int_field_signed)

    def test_int_field_raises_KeyError_when_using_invalid_key_words(self):
        with self.assertRaises(KeyError):
            class invalid_pkt(models.Packet):
                inv_field = models.IntField(keyword_that_dont_exist=100)

    def test_int_field_with_variable_bit_lenth(self):
        class int_packet_with_varied_sized_int_fields(models.Packet):
            int_field = models.IntField()
            int_field_signed = models.IntField(signed=True)
            int_field_4_bits = models.IntField(bit_len=4)
            int_field_12_bits = models.IntField(bit_len=12)

        pkt = int_packet_with_varied_sized_int_fields()
        pkt.int_field = 100
        pkt.int_field_signed = -100
        pkt.int_field_4_bits = 15
        pkt.int_field_12_bits = 1023

        b_str = b'd\x00\x9c\xff\xff?'

        self.assertEquals(b_str, pkt.to_bytes())

class TestSimplePacket(unittest.TestCase):

    def test_check_word_size(self):
        
        class two_int_field_packet(models.Packet):
            int_field = models.IntField()
            int_field_signed = models.IntField(signed=True)

        p = two_int_field_packet()
        self.assertEquals(p.num_words, 2)


    def test_create_packet_object_with_defined_values(self):
        class two_int_field_packet(models.Packet):
            int_field = models.IntField()
            int_field_signed = models.IntField(signed=True)

        p = two_int_field_packet(int_field=12, int_field_signed=-12)
        self.assertEquals(p.int_field, 12)
        self.assertEquals(p.int_field_signed, -12)


    def test_create_packet_with_default_field_value(self):
        class two_int_field_packet(models.Packet):
            int_field = models.IntField(default_val=12)
            int_field_signed = models.IntField(signed=True, default_val=-12)


        p = two_int_field_packet()
        self.assertEquals(p.int_field, 12)
        self.assertEquals(p.int_field_signed, -12)

    def test_create_packet_with_multi_field(self):

        class multi_int_field_packet(models.Packet):
            list_int_field = models.IntField(array_size=10)

        expected_vals = list(range(10))
        p = multi_int_field_packet()
        p.list_int_field = expected_vals

        self.assertEqual(p.list_int_field, expected_vals)

    def test_compare_two_same_packets(self):

        class two_int_field_packet(models.Packet):
            int_field = models.IntField()
            int_field_signed = models.IntField(signed=True)

        pkt1 = two_int_field_packet(int_field=1, int_field_signed=-1)
        pkt2 = two_int_field_packet(int_field=1, int_field_signed=-1)

        self.assertEquals(pkt1, pkt2)

    def test_compare_two_different_packets(self):

        class two_int_field_packet(models.Packet):
            int_field = models.IntField()
            int_field_signed = models.IntField(signed=True)

        class two_int_field_packet_2(models.Packet):
            int_field = models.IntField()
            int_field_signed = models.IntField(signed=True)


        pkt_orig = two_int_field_packet(int_field=1, int_field_signed=-1)
        pkt_different_class_same_byte_out = two_int_field_packet_2(int_field=1, int_field_signed=-1)

        # even though these packets will generate the same byte output and the fields are the same, this should raise
        #   an error as their classes are not the same.  
        self.assertFalse(pkt_orig == pkt_different_class_same_byte_out)

        class three_int_field_packet(models.Packet):
            int_field = models.IntField()
            int_field_2 = models.IntField()
            int_field_3 = models.IntField()

        pkt_different_class_different_byte_out = three_int_field_packet(int_field=1, int_field_2=2, int_field_3=3)
        self.assertFalse(pkt_orig == pkt_different_class_different_byte_out)

        pkt_same_class_different_values = two_int_field_packet(int_field=1, int_field_signed=2)
        self.assertFalse(pkt_orig == pkt_same_class_different_values)



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
