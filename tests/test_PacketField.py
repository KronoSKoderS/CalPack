import unittest
from calpack import models


class Test_PacketField(unittest.TestCase):
    def test_pktfield_encapsulated_pkt(self):
        class simple_pkt(models.Packet):
            field1 = models.IntField()

        class adv_pkt(models.Packet):
            field2 = models.PacketField(simple_pkt)

        p = adv_pkt()

        # Verify ability to access and set encap packets fields
        p.field2.field1 = 100

        self.assertEqual(p.field2.field1, 100)
        self.assertEqual(p._Packet__c_pkt.field2.field1, 100)

        sp = simple_pkt()
        sp.field1 = 200

        p.field2 = sp

        self.assertEqual(p.field2.field1, 200)

    def test_pktfield_raises_typeerror_when_not_pktclas(self):
        class simple_pkt(models.Packet):
            field1 = models.IntField()

        class adv_pkt(models.Packet):
            field2 = models.PacketField(simple_pkt)

        p = adv_pkt()

        with self.assertRaises(TypeError):
            p.field2 = 100


if __name__ == '__main__':
    unittest.main()
