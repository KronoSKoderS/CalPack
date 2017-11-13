from random import randint
from calpack import models

from tests import PY2, PY3

import unittest
import struct

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
            list_int_field = models.ArrayField(models.IntField(), 10)

        expected_vals = list(range(10))
        p = multi_int_field_packet()
        p.list_int_field = expected_vals

        self.assertEqual(p.list_int_field, expected_vals)

        self.assertEqual(type(p.list_int_field), models.ArrayField)

    def test_set_invalid_type_multi_field(self):

        class multi_int_field_packet(models.Packet):
            list_int_field = models.ArrayField(models.IntField(), 10)

        expected_vals = list(range(10))
        p = multi_int_field_packet()

        with self.assertRaises(TypeError):
            p.list_int_field = 100

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

class TestAdvancedPackets(unittest.TestCase):

     def test_encapsulated_pkt(self):
         class simple_pkt(models.Packet):
             field1 = models.IntField()

         class adv_pkt(models.Packet):
             field2 = models.PacketField(simple_pkt)

         p = adv_pkt()

         # Verify abilily to access and set encap packets fields
         p.field2.field1 = 100

         self.assertEquals(p.field2.field1, 100)
         self.assertTrue(isinstance(p.field2, models.Packet))
         self.assertEquals(type(p.field2.field1), models.IntField)

         sp = simple_pkt()
         sp.field1 = 200

         p.field2 = sp

         self.assertEquals(p.field2.field1, 200)
         self.assertTrue(isinstance(p.field2, models.Packet))
         self.assertEquals(type(p.field2.field1), models.IntField)


if __name__ == '__main__':
    unittest.main()
