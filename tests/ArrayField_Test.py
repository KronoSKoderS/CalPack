import unittest
from calpack import models


class Test_ArrayField(unittest.TestCase):
    def test_arrayfield_create_packet_with_array_field(self):

        class multi_int_field_packet(models.Packet):
            arr_int_field = models.ArrayField(models.IntField(), 10)

        expected_vals = tuple(range(10))
        p = multi_int_field_packet()
        p.arr_int_field = expected_vals

        self.assertEqual(p.arr_int_field, expected_vals)
        self.assertEqual(tuple(p._Packet__c_pkt.arr_int_field[:]), expected_vals)

    def test_arrayfield_set_invalid_type_multi_field(self):

        class multi_int_field_packet(models.Packet):
            arr_int_field = models.ArrayField(models.IntField(), 10)

        p = multi_int_field_packet()

        with self.assertRaises(TypeError):
            p.arr_int_field = 100

    def test_arrayfield_raises_valueerror_invalid_val_size(self):
        class multi_int_field_packet(models.Packet):
            arr_int_field = models.ArrayField(models.IntField(), 10)

        p = multi_int_field_packet()

        with self.assertRaises(ValueError):
            p.arr_int_field = list(range(11))

        with self.assertRaises(ValueError):
            p.arr_int_field = list(range(9))

    def test_arrayfield_access_individual_members(self):
        class multi_int_field_packet(models.Packet):
            arr_int_field = models.ArrayField(models.IntField(), 10)

        expected_vals = tuple(range(10))
        p = multi_int_field_packet()
        p.arr_int_field = expected_vals

        for i, val in enumerate(expected_vals):
            self.assertEqual(p.arr_int_field[i], val)
            self.assertEqual(p._Packet__c_pkt.arr_int_field[i], val)

    def test_arrayfield_compare_two_arrayfields(self):
        class multi_int_field_packet(models.Packet):
            arr_int_field = models.ArrayField(models.IntField(), 10)

        class multi_int_field_packet2(models.Packet):
            arr_int_field = models.ArrayField(models.IntField(), 10)

        expected_vals = tuple(range(10))

        p1 = multi_int_field_packet()
        p1.arr_int_field = expected_vals

        p2 = multi_int_field_packet2()
        p2.arr_int_field = tuple(reversed(expected_vals))

        self.assertNotEqual(p1.arr_int_field, p2.arr_int_field)

        p2.arr_int_field = expected_vals

        self.assertEqual(p1.arr_int_field, p2.arr_int_field)

    def test_arrayfield_set_val_from_other_arrayfield(self):
        class multi_int_field_packet(models.Packet):
            arr_int_field = models.ArrayField(models.IntField(), 10)

        expected_vals = tuple(range(10))

        p1 = multi_int_field_packet(arr_int_field=expected_vals)

        p2 = multi_int_field_packet()
        p2.arr_int_field = p1.arr_int_field

        self.assertEquals(p2.arr_int_field, expected_vals)

    def test_arrayfield_raise_typeerror_non_byte_aligned_int_field(self):
        with self.assertRaises(TypeError):
            class multi_int_field(models.Packet):
                arr_int_field = models.ArrayField(models.IntField(bit_len=4), 10)


if __name__ == '__main__':
    unittest.main()
