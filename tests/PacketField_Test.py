import unittest

class Test_PacketField(unittest.TestCase):
    def test_encapsulated_pkt(self):
         class simple_pkt(models.Packet):
             field1 = models.IntField()

         class adv_pkt(models.Packet):
             field2 = models.PacketField(simple_pkt)

         p = adv_pkt()

         # Verify abilily to access and set encap packets fields
         p.field2.field1 = 100

         self.assertEquals(p.field2.field1, 100)
         self.assertTrue(isinstance(p.field2, models.Packet))
         self.assertEquals(type(p.field2.field1), models.IntField)

         sp = simple_pkt()
         sp.field1 = 200

         p.field2 = sp

         self.assertEquals(p.field2.field1, 200)
         self.assertTrue(isinstance(p.field2, models.Packet))
         self.assertEquals(type(p.field2.field1), models.IntField)

if __name__ == '__main__':
    unittest.main()
