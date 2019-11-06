import unittest

from calpack import models

class Test_FlagField(unittest.TestCase):
    def test_flagfield_set_val(self):
        class flagged_packet(models.Packet):
            flag = models.FlagField()

        pkt = flagged_packet()
        pkt.flag = False

        self.assertEqual(pkt.flag, False)
        self.assertEqual(pkt._Packet__c_pkt.flag, 0)

        pkt.flag = True

        self.assertEqual(pkt.flag, True)
        self.assertEqual(pkt._Packet__c_pkt.flag, 1)

    def test_flagfield_set_invalid_val_raise_error(self):
        class flagged_packet(models.Packet):
            flag = models.FlagField()

        pkt = flagged_packet()

        with self.assertRaises(TypeError):
            pkt.flag = -1

        with self.assertRaises(TypeError):
            pkt.flag = 2

        with self.assertRaises(TypeError):
            pkt.flag = "a"

if __name__ == '__main__':
    unittest.main()
