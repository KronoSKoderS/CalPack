import unittest

from calpack import models

class Test_FloatField(unittest.TestCase):
    def test_floatfield_set_val(self):
        class float_packet(models.Packet):
            f_field = models.FloatField()

        f = float_packet()

        f.f_field = 3.14

        self.assertAlmostEquals(f.f_field, 3.14, places=5)
        self.assertAlmostEquals(f._Packet__c_pkt.f_field, 3.14, places=5)

        f.f_field = -3.14

        self.assertAlmostEquals(f.f_field, -3.14, places=5)
        self.assertAlmostEquals(f._Packet__c_pkt.f_field, -3.14, places=5)

        f.f_field = 3

        self.assertAlmostEquals(f.f_field, 3, places=5)
        self.assertAlmostEquals(f._Packet__c_pkt.f_field, 3, places=5)

        f.f_field = -3

        self.assertAlmostEquals(f.f_field, -3, places=5)
        self.assertAlmostEquals(f._Packet__c_pkt.f_field, -3, places=5)

    def test_floatfield_set_invalid_val_raises_type_error(self):
        class float_packet(models.Packet):
            f_field = models.FloatField()

        f = float_packet()

        with self.assertRaises(TypeError):
            f.f_field = 's'

        with self.assertRaises(TypeError):
            f.f_field = list(range(10))


class Test_DoubleField(unittest.TestCase):
    def test_doublefield_set_valid_vals(self):
        class double_packet(models.Packet):
            d_field = models.DoubleField()

        f = double_packet()
        f.d_field = 3.14

        self.assertAlmostEquals(f.d_field, 3.14, places=5)
        self.assertAlmostEquals(f._Packet__c_pkt.d_field, 3.14, places=5)

        f.d_field = -3.14

        self.assertAlmostEquals(f.d_field, -3.14, places=5)
        self.assertAlmostEquals(f._Packet__c_pkt.d_field, -3.14, places=5)

        f.d_field = 3

        self.assertAlmostEquals(f.d_field, 3, places=5)
        self.assertAlmostEquals(f._Packet__c_pkt.d_field, 3, places=5)

        f.d_field = -3

        self.assertAlmostEquals(f.d_field, -3, places=5)
        self.assertAlmostEquals(f._Packet__c_pkt.d_field, -3, places=5)

    def test_doublefield_set_invalid_val_raises_type_error(self):
        class double_packet(models.Packet):
            f_field = models.DoubleField()

        f = double_packet()

        with self.assertRaises(TypeError):
            f.f_field = 's'

        with self.assertRaises(TypeError):
            f.f_field = list(range(10))


class Test_LongDoubleField(unittest.TestCase):
    def test_doublefield_set_valid_vals(self):
        class double_packet(models.Packet):
            d_field = models.LongDoubleField()

        f = double_packet()
        f.d_field = 3.14

        self.assertAlmostEquals(f.d_field, 3.14, places=5)
        self.assertAlmostEquals(f._Packet__c_pkt.d_field, 3.14, places=5)

        f.d_field = -3.14

        self.assertAlmostEquals(f.d_field, -3.14, places=5)
        self.assertAlmostEquals(f._Packet__c_pkt.d_field, -3.14, places=5)

        f.d_field = 3

        self.assertAlmostEquals(f.d_field, 3, places=5)
        self.assertAlmostEquals(f._Packet__c_pkt.d_field, 3, places=5)

        f.d_field = -3

        self.assertAlmostEquals(f.d_field, -3, places=5)
        self.assertAlmostEquals(f._Packet__c_pkt.d_field, -3, places=5)

    def test_doublefield_set_invalid_val_raises_type_error(self):
        class double_packet(models.Packet):
            f_field = models.LongDoubleField()

        f = double_packet()

        with self.assertRaises(TypeError):
            f.f_field = 's'

        with self.assertRaises(TypeError):
            f.f_field = list(range(10))


if __name__ == '__main__':
    unittest.main()
