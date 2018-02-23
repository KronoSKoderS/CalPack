import unittest

from calpack import models


class Test_Repr(unittest.TestCase):

    def test_simple_repr(self):
        class two_int_pkt(models.Packet):
            field1 = models.IntField()
            field2 = models.IntField()

        pkt = two_int_pkt()

        expected = "two_int_pkt(field1=0, field2=0)"
        self.assertEqual(repr(pkt), expected)

        pkt.field1 = 1234
        pkt.field2 = 5678

        expected = "two_int_pkt(field1=1234, field2=5678)"
        self.assertEqual(repr(pkt), expected)
