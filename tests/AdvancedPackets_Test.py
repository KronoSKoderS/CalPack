from random import randint
from calpack import models

from tests import PY2, PY3

import unittest
import struct


class Test_AdvancedPacket(unittest.TestCase):

    def test_advpkt_enc_array_pkts(self):
        class Point(models.Packet):
            x = models.IntField()
            y = models.IntField()

        class EncArray(models.Packet):
            points = models.ArrayField(
                models.PacketField(Point),
                10
            )

        pkt = EncArray()

        for i, point in enumerate(pkt.points):
            point.x = 100
            point.y = 50

            self.assertEqual(pkt.points[i].x, 100)
            self.assertEqual(pkt._Packet__c_pkt.points[i].x, 100)

            self.assertEqual(pkt.points[i].y, 50)
            self.assertEqual(pkt._Packet__c_pkt.points[i].y, 50)


    def test_advpkt_inception_enc_pkt(self):
        class Point(models.Packet):
            x = models.IntField()
            y = models.IntField()

        class TenPoints(models.Packet):
            points = models.ArrayField(
                models.PacketField(Point),
                8
            )

        class TwoTenPoints(models.Packet):
            points_one = models.PacketField(TenPoints)
            points_two = models.PacketField(TenPoints)


        pkt = TwoTenPoints()

        for i, point in enumerate(pkt.points_one.points):
            point.x = 100
            point.y = 50

            self.assertEqual(pkt.points_one.points[i].x, 100)
            self.assertEqual(pkt._Packet__c_pkt.points_one.points[i].x, 100)

            self.assertEqual(pkt.points_one.points[i].y, 50)
            self.assertEqual(pkt._Packet__c_pkt.points_one.points[i].y, 50)

        for i, point in enumerate(pkt.points_two.points):
            point.x = 100
            point.y = 50

            self.assertEqual(pkt.points_two.points[i].x, 100)
            self.assertEqual(pkt._Packet__c_pkt.points_two.points[i].x, 100)

            self.assertEqual(pkt.points_two.points[i].y, 50)
            self.assertEqual(pkt._Packet__c_pkt.points_two.points[i].y, 50)

    def test_verify_AttributeError_invalid_field_name_set_c_field(self):
        class Point(models.Packet):
            x = models.IntField()
            y = models.IntField()

        p = Point()
        with self.assertRaises(AttributeError):
            p.set_c_field('bad_name', 100)


