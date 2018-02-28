import unittest

from calpack import models

class Test_BoolField(unittest.TestCase):
    def test_boolfield_set_valid_vals(self):
        class bool_packet(models.Packet):
            b_field=models.BoolField()

        b_packet = bool_packet()

        b_packet.b_field = True

        self.assertEqual(b_packet.b_field, True)
        self.assertEqual(b_packet._Packet__c_pkt.b_field, True)

        b_packet.b_field = False

        self.assertEqual(b_packet.b_field, False)
        self.assertEqual(b_packet._Packet__c_pkt.b_field, False)

    def test_boolfield_raises_typeerror_invalid_vals(self):
        class bool_packet(models.Packet):
            b_field=models.BoolField()

        b_packet = bool_packet()
        
        with self.assertRaises(TypeError):
            b_packet.b_field = 120

        with self.assertRaises(TypeError):
            b_packet.b_field = "WRONG!"

        with self.assertRaises(TypeError):
            b_packet.b_field = [1, 2, 3, 4]

        with self.assertRaises(TypeError):
            b_packet.b_field = 3.14
