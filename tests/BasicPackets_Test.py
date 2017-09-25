import unittest
import struct

from random import randint

from calpack import models


class TestSimplePackets(unittest.TestCase):
    def setUp(self):
        class simple_pkt(models.Packet):
            field1 = models.IntField()
            field2 = models.IntField(unsigned=True)

        self.simple_pkt = simple_pkt

    def test_set_simple_int_fields(self):
        p = self.simple_pkt()

        v1 = randint(-32768, 32767)
        v2 = randint(0, 65536)

        p.field1 = v1
        p.field2 = v2

        self.assertEqual(p.field1, v1)
        self.assertEqual(p.field2, v2)

    def test_set_invalid_int_field(self):
        p = self.simple_pkt()
        
        with self.assertRaises(TypeError):
            p.field1 = ""

    def test_set_valid_from_other_field(self):
        p = self.simple_pkt()
        p2 = self.simple_pkt()

        v1 = randint(-32768, 32767)
        
        p.field1 = v1

        p2.field1 = p.field1

        self.assertEqual(p.field1, p2.field1)


    def test_from_binary(self):
        v1 = randint(-32768, 32767)
        v2 = randint(0, 65536)
        vals = [v1, v2]
        b_val = struct.pack('hH', *vals)

        p = self.simple_pkt.from_bytes(b_val)

        self.assertEquals(p.field1, vals[0])
        self.assertEquals(p.field2, vals[1])

    def test_to_binary(self):
        v1 = randint(-32768, 32767)
        v2 = randint(0, 65536)
        vals = [v1, v2]
        b_val = struct.pack('hH', *vals)

        p = self.simple_pkt()
        p.field1 = vals[0]
        p.field2 = vals[1]

        pkt_bin = p.to_bytes()

        self.assertEquals(pkt_bin, b_val)

    def test_to_from_binary(self):
        vals = [randint(0, 100) for i in range(2)]

        p = self.simple_pkt()
        p.field1 = vals[0]
        p.field2 = vals[1]

        p2 = self.simple_pkt.from_bytes(p.to_bytes())

        self.assertEquals(p.field1, p2.field1)
        self.assertEquals(p.field2, p2.field2)


    def test_invalid_key_words(self):
        with self.assertRaises(KeyError):
            class invalid_pkt(models.Packet):
                inv_field = models.IntField(keyword_that_dont_exist=100)


## TDD: Prototyping for encapsulated packets.
# class TestAdvancedPackets(unittest.TestCase):
#     def setUp(self):
#         pass
#
#     def test_encapsulated_pkt(self):
#         class simple_pkt(models.Packet):
#             field1 = models.IntField(num_words=10)
#
#         class adv_pkt(models.Packet):
#             field2 = simple_pkt
#
#         p = adv_pkt()
#
#         # Verify abilily to access and set encap packets fields
#         p.field2.field1 = 100
#
#         self.assertEquals(p.field2.field1, 100)
#
#         sp = simple_pkt()
#         sp.field1 = 200
#
#         p.field2 = sp
#
#         self.assertEquals(p.field2.field1, 200)


if __name__ == '__main__':
    unittest.main()
