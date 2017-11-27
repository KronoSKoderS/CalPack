import unittest
from calpack import models


class Test_ArrayField(unittest.TestCase):
    def test_arrayfield_create_packet_with_array_field(self):

        class multi_int_field_packet(models.Packet):
            list_int_field = models.ArrayField(models.IntField(), 10)

        expected_vals = list(range(10))
        p = multi_int_field_packet()
        p.list_int_field = expected_vals

        self.assertEqual(p.list_int_field, expected_vals)
        self.assertEqual(p._Packet__c_pkt.list_int_field[:], expected_vals)

    def test_arrayfield_set_invalid_type_multi_field(self):

        class multi_int_field_packet(models.Packet):
            list_int_field = models.ArrayField(models.IntField(), 10)

        # expected_vals = list(range(10))
        p = multi_int_field_packet()

        with self.assertRaises(TypeError):
            p.list_int_field = 100

    def test_arrayfield_access_individual_members(self):
        class multi_int_field_packet(models.Packet):
            list_int_field = models.ArrayField(models.IntField(), 10)

        expected_vals = list(range(10))
        p = multi_int_field_packet()
        p.list_int_field = expected_vals

        for i, val in enumerate(expected_vals):
            self.assertEqual(p.list_int_field[i], val)
            self.assertEqual(p._Packet__c_pkt.list_int_field[i], val)

    def test_arrayfield_compare_two_arrayfields(self):
        class multi_int_field_packet(models.Packet):
            list_int_field = models.ArrayField(models.IntField(), 10)

        class multi_int_field_packet2(models.Packet):
            list_int_field = models.ArrayField(models.IntField(), 10)

        expected_vals = list(range(10))

        p1 = multi_int_field_packet()
        p1.list_int_field = expected_vals

        p2 = multi_int_field_packet2()
        p2.list_int_field = list(reversed(expected_vals))

        self.assertNotEqual(p1.list_int_field, p2.list_int_field)

        p2.list_int_field = expected_vals

        self.assertEqual(p1.list_int_field, p2.list_int_field)



    def test_arrayfield_set_val_from_other_arrayfield(self):
        class multi_int_field_packet(models.Packet):
            list_int_field = models.ArrayField(models.IntField(), 10)

        expected_vals = list(range(10))

        p1 = multi_int_field_packet(list_int_field=expected_vals)

        p2 = multi_int_field_packet()
        p2.list_int_field = p1.list_int_field

        self.assertEquals(p2.list_int_field, expected_vals)

if __name__ == '__main__':
    unittest.main()
