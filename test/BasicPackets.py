import unittest

from concorde import models

class Test_SimplePackets(unittest.TestCase):
    def setup(self):
        class simple_pkt(models.Packet):
            field1 = models.IntField()
            field2 = models.IntField()

        self.simple_pkt = simple_pkt

    def test_set_simeple_fields(self):
        p = self.simple_pkt()
        p.field1 = 1
        p.field2 = 2

        self.assertEqual(p.field1, 1)
        self.assertEqual(p.field2, 2)

    def test_set_invalid_fields(self):
        p = self.simple_pkt()
        
        with self.assertRaises(TypeError):
            p.field1 = ""



class Test_AdvancedPackets(unittest.TestCase):
    def setup(self):
        class adv_pkt(models.Packet):
            field1 = models.IntField(num_words=10)

        self.adv_pkt = adv_pkt

    def test_set_array_field(self):
        p = self.adv_pkt()
        p.field1 = range(10)
        self.assertEqual(p.field1, list(range(10)))


if __name__ == '__main__':
    unittest.main()
