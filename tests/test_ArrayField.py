import unittest
from calpack import models
from calpack.utils import InvalidArrayFieldSizeError


class Test_ArrayField(unittest.TestCase):
    def test_arrayfield_create_packet_with_array_field(self):
        """
        This test verifies that a packet can be created with an `ArrayField` of `IntField`'s and
        that the fields can be set and accessed.
        """

        class multi_int_field_packet(models.Packet):
            arr_int_field = models.ArrayField(models.IntField(), 10)

        expected_vals = tuple(range(10))
        p = multi_int_field_packet()
        p.arr_int_field = expected_vals

        self.assertEqual(p.arr_int_field, expected_vals)
        self.assertEqual(tuple(p._Packet__c_pkt.arr_int_field[:]), expected_vals)

    def test_arrayfield_set_invalid_type_multi_field(self):
        """
        This test verifies that attempting to set an invalid value (non list) to an array field
        will raise a TypeError.
        """

        class multi_int_field_packet(models.Packet):
            arr_int_field = models.ArrayField(models.IntField(), 10)

        p = multi_int_field_packet()

        with self.assertRaises(TypeError):
            p.arr_int_field = 100

        with self.assertRaises(TypeError):
            p.arr_int_field = 3.4

        with self.assertRaises(TypeError):
            p.arr_int_field = "smallstrin"

    def test_arrayfield_raises_invalidarrayfieldsize_for_invalid_val_size(self):
        """
        This test verifies that a list of the proper type but invalid size (too big or too small)
        raises a InvalidArrayFieldSizeError.
        """
        class multi_int_field_packet(models.Packet):
            arr_int_field = models.ArrayField(models.IntField(), 10)

        p = multi_int_field_packet()

        with self.assertRaises(InvalidArrayFieldSizeError):
            p.arr_int_field = list(range(11))

        with self.assertRaises(InvalidArrayFieldSizeError):
            p.arr_int_field = list(range(9))

    def test_arrayfield_access_individual_members(self):
        """
        This test verifies that individual values of an ArrayField can be accessed.
        """
        class multi_int_field_packet(models.Packet):
            arr_int_field = models.ArrayField(models.IntField(), 10)

        expected_vals = tuple(range(10))
        p = multi_int_field_packet()
        p.arr_int_field = expected_vals

        for i, val in enumerate(expected_vals):
            self.assertEqual(p.arr_int_field[i], val)
            self.assertEqual(p._Packet__c_pkt.arr_int_field[i], val)

    def test_arrayfield_compare_two_arrayfields(self):
        """
        This test verifies that comparing two `ArrayFields` returns the proper results
        """
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
        """
        This test verifies that an `ArrayField` can be used to set the values of another
        `ArrayField`.
        """
        class multi_int_field_packet(models.Packet):
            arr_int_field = models.ArrayField(models.IntField(), 10)

        expected_vals = tuple(range(10))

        p1 = multi_int_field_packet(arr_int_field=expected_vals)

        p2 = multi_int_field_packet()
        p2.arr_int_field = p1.arr_int_field

        self.assertEquals(p2.arr_int_field, expected_vals)

    def test_arrayfield_raise_typeerror_non_byte_aligned_int_field(self):
        """
        This test verifies that `IntFields` using the `bit_len` param will raise a TypeError.  We
        don't know how to handle this functionality at this time, so make sure we raise the error.
        """
        with self.assertRaises(TypeError):
            class multi_int_field(models.Packet):
                arr_int_field = models.ArrayField(models.IntField(bit_len=4), 10)


if __name__ == '__main__':
    unittest.main()
