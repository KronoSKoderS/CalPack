import unittest

class Test_ArrayField(unittest.TestCase):
    def test_create_packet_with_multi_field(self):

        class multi_int_field_packet(models.Packet):
            list_int_field = models.ArrayField(models.IntField(), 10)

        expected_vals = list(range(10))
        p = multi_int_field_packet()
        p.list_int_field = expected_vals

        self.assertEqual(p.list_int_field, expected_vals)

        self.assertEqual(type(p.list_int_field), models.ArrayField)

if __name__ == '__main__':
    unittest.main()
