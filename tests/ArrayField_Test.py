import unittest
import struct

from random import randint

from tests import PY2, PY3
from calpack import models


class Test_ArrayField(unittest.TestCase):
    def test_arrayfield_create_packet_with_array_field(self):

        class multi_int_field_packet(models.Packet):
            list_int_field = models.ArrayField(models.IntField, 10)

        expected_vals = list(range(10))
        p = multi_int_field_packet()
        p.list_int_field = expected_vals

        self.assertEqual(p.list_int_field, expected_vals)

        self.assertEqual(type(p.list_int_field), models.ArrayField)

    def test_arrayfield_set_invalid_type_multi_field(self):

        class multi_int_field_packet(models.Packet):
            list_int_field = models.ArrayField(models.IntField, 10)

        expected_vals = list(range(10))
        p = multi_int_field_packet()

        with self.assertRaises(TypeError):
            p.list_int_field = 100


    def test_arrayfield_access_individual_members(self):
        class multi_int_field_packet(models.Packet):
            list_int_field = models.ArrayField(models.IntField, 10)

        expected_vals = list(range(10))
        p = multi_int_field_packet()
        p.list_int_field = expected_vals

        for i, val in enumerate(expected_vals):
            self.assertEquals(p.list_int_field[i], val)

if __name__ == '__main__':
    unittest.main()
