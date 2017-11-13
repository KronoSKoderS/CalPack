import unittest
import struct

from random import randint

from tests import PY2, PY3
from calpack import models


class Test_IntField(unittest.TestCase):
    def setUp(self):
        class two_int_field_packet(models.Packet):
            int_field = models.IntField()
            int_field_signed = models.IntField(signed=True)

        self.two_int_field_packet = two_int_field_packet

    def test_intfield_set_valid_values(self):
        """
        This test verifies that setting an integer field of a packet is done correctly.  This
        also tests the comparison operator `__eq__`.  Finally, it checks that the types of the
        field isn't altered.  
        """
        p = self.two_int_field_packet()

        v1 = randint(0, 65535)
        v2 = randint(-32768, 32767)

        p.int_field = v1
        p.int_field_signed = v2

        self.assertEqual(p.int_field, v1)
        self.assertEqual(p.int_field_signed, v2)

        self.assertEqual(type(p.int_field), models.IntField)
        self.assertEqual(type(p.int_field), models.IntField)

    def test_intfield_raises_TypeError_when_setting_non_int_value(self):
        """
        This test verifies that a "TypeError" is raised when setting a value other than
        an integer for the IntField.  The following types are checked:

            * String
            * Float
            * list
        """
        p = self.two_int_field_packet()
        
        with self.assertRaises(TypeError):
            p.int_field = ""

        with self.assertRaises(TypeError):
            p.int_field_signed = 3.14

        with self.assertRaises(TypeError):
            p.int_field = [0] * 12


    def test_intfield_raises_TypeError_when_setting_signed_to_nonsigned(self):
        """
        This test verifies that a "TypeErorr" is raised when setting a non-signed value to a
        signed value.  
        """
        p = self.two_int_field_packet()

        with self.assertRaises(TypeError):
            p.int_field = -123

    def test_intfield_set_valid_value_from_other_field(self):
        """
        This test verifies that setting an integer field from another field is done properly
        and doesn't change the field type.  
        """
        p = self.two_int_field_packet()
        p2 = self.two_int_field_packet()

        v1 = randint(0, 65535)
        
        p.int_field = v1

        p2.int_field = p.int_field

        self.assertEqual(p.int_field, p2.int_field)

        self.assertEqual(type(p.int_field), models.IntField)

    def test_intfield_with_variable_bit_lenth(self):
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

        if PY3:
            b_str = b'd\x00\x9c\xff\x0f\x00\xff\x03'
        else:
            b_str = b'd\x00\x0f\x00\x9c\xff\xff\x03'

        self.assertEquals(b_str, pkt.to_bytes())

    def test_intfield_comparitors(self):
        p = self.two_int_field_packet()

        p.field1 = 10
        p.field2 = -10

        self.assertTrue(p.field1 < 100)
        self.assertTrue(p.field1 > 0)
        self.assertTrue(p.field1 != 100)
        self.assertTrue(p.field1 <= 10)
        self.assertTrue(p.field1 >= 10)
        self.assertTrue(p.field1 == 10)
        self.assertTrue(p.field1 <= 11)
        self.assertTrue(p.field1 >= 9)

        self.assertTrue(p.field2 < 0)
        self.assertTrue(p.field2 > -100)
        self.assertTrue(p.field2 != 100)
        self.assertTrue(p.field2 <= -10)
        self.assertTrue(p.field2 <= -9)
        self.assertTrue(p.field2 >= -10)
        self.assertTrue(p.field2 >= -11)
        self.assertTrue(p.field2 == -10)


if __name__ == '__main__':
    unittest.main()
