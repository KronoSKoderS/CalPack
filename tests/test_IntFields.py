import unittest
import ctypes
from calpack import models


class Test_IntField(unittest.TestCase):
    def setUp(self):
        class two_int_field_packet(models.Packet):
            int_field = models.IntField()
            int_field_signed = models.IntField(signed=True)

        self.two_int_field_packet = two_int_field_packet

    def test_intfield_set_valid_values(self):
        """
        This test verifies that setting an integer field of a packet is done
        correctly. This also verifies that the internal c structure is properly
        setup as well.
        """
        p = self.two_int_field_packet()

        v1 = 100
        v2 = -100

        p.int_field = v1
        p.int_field_signed = v2

        self.assertEqual(p.int_field, v1)
        self.assertEqual(p._Packet__c_pkt.int_field, v1)

        self.assertEqual(p.int_field_signed, v2)
        self.assertEqual(p._Packet__c_pkt.int_field_signed, v2)

    def test_intfield_raises_TypeError_when_setting_non_int_value(self):
        """
        This test verifies that a "TypeError" is raised when setting a value
        other than an integer for the IntField. The following types are checked

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
        This test verifies that a "TypeError" is raised when setting a
        non-signed value to a signed value.
        """
        p = self.two_int_field_packet()

        with self.assertRaises(TypeError):
            p.int_field = -123

    def test_intfield_set_valid_value_from_other_field(self):
        """
        This test verifies that setting an integer field from another field is
        done properly and doesn't change the field type.
        """
        p = self.two_int_field_packet()
        p2 = self.two_int_field_packet()

        v1 = 123

        p.int_field = v1

        p2.int_field = p.int_field

        self.assertEqual(p.int_field, p2.int_field)
        self.assertEqual(p2._Packet__c_pkt.int_field, v1)

    def test_intfield_with_variable_bit_length(self):
        """
        This test verifies that setting an integer value of variable size is
        correctly exported to the to_bytes function.  This also tests the
        ability to set a value for the packet upon instantiation.
        """
        class int_packet_with_varied_sized_int_fields(models.Packet):
            int_field = models.IntField()
            int_field_signed = models.IntField(signed=True)
            int_field_4_bits = models.IntField16(bit_len=4)
            int_field_12_bits = models.IntField16(bit_len=12)

        pkt = int_packet_with_varied_sized_int_fields(
            int_field=0xbeef,
            int_field_signed=0xdead,
            int_field_4_bits=0xa,
            int_field_12_bits=0xbc
        )

        class c_pkt_struct(ctypes.Structure):
            _pack_ = 1
            _fields_ = (
                ('int_field', ctypes.c_uint),
                ('int_field_signed', ctypes.c_int),
                ('int_field_4_bits', ctypes.c_uint16, 4),
                ('int_field_12_bits', ctypes.c_uint16, 12),
            )

        c_pkt = c_pkt_struct()
        c_pkt.int_field = 0xbeef
        c_pkt.int_field_signed = 0xdead
        c_pkt.int_field_4_bits = 0xa
        c_pkt.int_field_12_bits = 0xbc

        b_str = ctypes.string_at(ctypes.addressof(c_pkt), ctypes.sizeof(c_pkt))

        self.assertEqual(b_str, pkt.to_bytes())

    def test_intfield_raises_ValueError_with_invalid_bit_len(self):
        with self.assertRaises(ValueError):
            int_field = models.IntField(bit_len=0)

        with self.assertRaises(ValueError):
            int_field = models.IntField(bit_len=-1)

        with self.assertRaises(ValueError):
            int_field = models.IntField(bit_len=65)

    def test_intfield_multi_int_fields(self):
        class all_int_fields(models.Packet):
            int_field = models.IntField()
            int_field8 = models.IntField8()
            int_field16 = models.IntField16()
            int_field32 = models.IntField32()
            int_field64 = models.IntField64()

        pkt = all_int_fields()
        pkt.int_field = 1
        pkt.int_field8 = 2
        pkt.int_field16 = 3
        pkt.int_field32 = 4
        pkt.int_field64 = 5

        self.assertEqual(pkt.int_field, 1)
        self.assertEqual(pkt._Packet__c_pkt.int_field, 1)
        self.assertEqual(pkt.int_field8, 2)
        self.assertEqual(pkt._Packet__c_pkt.int_field8, 2)
        self.assertEqual(pkt.int_field16, 3)
        self.assertEqual(pkt._Packet__c_pkt.int_field16, 3)
        self.assertEqual(pkt.int_field32, 4)
        self.assertEqual(pkt._Packet__c_pkt.int_field32, 4)
        self.assertEqual(pkt.int_field64, 5)
        self.assertEqual(pkt._Packet__c_pkt.int_field64, 5)


if __name__ == '__main__':
    unittest.main()
