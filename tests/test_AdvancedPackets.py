from calpack import models
from calpack.utils import FieldNameError
import unittest
import ctypes


class Test_AdvancedPacket(unittest.TestCase):

    def test_advpkt_enc_array_pkts(self):
        """
        This test verifies that multiple Packet classes can be "encapsulated" within another packet
        using the `PacketField` class and the `ArrayField` class.  Multiple 
        """
        class Point(models.Packet):
            """
            A simple `Packet` class to be encapsulated within another `Packet` class
            """
            x = models.IntField()
            y = models.IntField()

        class EncArray(models.Packet):
            """
            A `Packet` class that will encapsulate the `Point` class.
            """
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
        """
        This test verifies the functionality of encapsulating multiple `Packet` classes down to
        3 level (Parent --> Child 1 --> Child 2).  Further more, the encapsulation at level 2
        (Child 1) will encapsulate level 3 (Child 2) using an `ArrayField` class.
        """
        class Point(models.Packet):
            """
            A simple `Packet` class intended to be encapsulated within another `Packet` class
            """
            x = models.IntField()
            y = models.IntField()

        class TenPoints(models.Packet):
            """
            A `Packet` class that will encapsulate the `Point` class and intended to be
            encapsulated within another `Packet` class.
            """
            points = models.ArrayField(
                models.PacketField(Point),
                8
            )

        class TwoTenPoints(models.Packet):
            """
            A `Packet` class that will encapsulate the `TenPoints` class.
            """
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

    def test_advpkt_verify_AttributeError_invalid_field_name_set_c_field(self):
        """
        This test verifies the internal `set_c_field` function to verify that attempting to set
        an internal c_pkt field that doesn't exist will raise an AttributeError
        """
        class Point(models.Packet):
            """
            A simple `Packet` class.  It's contents doesn't matter as long as none of the fields
            have a name called 'bad_name'.
            """
            x = models.IntField()
            y = models.IntField()

        p = Point()
        with self.assertRaises(FieldNameError):
            p.set_c_field('bad_name', 100)

    def test_advpkt_create_complex_packet(self):
        """
        This test verifies that creating a packet that contains all the known built-in fields and
        ensures that the packet is correctly created and parsed back in.  This test will create a
        CalPack `Packet` class that will contain all field types (including the `PacketField), set
        values for each of the fields, export to bytes and compare those values to that of a ctypes
        Structure class using the same field definitions.
        """

        class Point(models.Packet):
            """
            A simple `Packet` class to be used for encapsulation
            """
            x = models.IntField8()
            y = models.IntField8()

        class PrimaryPacket(models.Packet):
            """
            A `Packet` class used to contain all fields types (including the `PacketField`)
            """
            int_field = models.IntField()
            float_field = models.FloatField()
            double_field = models.DoubleField()
            long_double_field = models.LongDoubleField()
            pkt_field = models.PacketField(Point)
            bool_field = models.BoolField()

        class c_Point(ctypes.Structure):
            """
            A ctypes.Structure class that will mimic the `Point` class
            """
            _fields_ = (
                ('x', ctypes.c_uint8),
                ('y', ctypes.c_uint8)
            )

        class c_PrimaryPacket(ctypes.Structure):
            """
            A ctypes.Structure class that will mimc the `PrimaryPacket` class
            """
            _fields_ = (
                ('int_field', ctypes.c_uint),
                ('float_field', ctypes.c_float),
                ('double_field', ctypes.c_double),
                ('long_double_field', ctypes.c_longdouble),
                ('pkt_field', c_Point),
                ('bool_field', ctypes.c_bool)
            )

        pkt = PrimaryPacket(
            int_field=3,
            float_field=3.14,
            double_field=-3.14,
            long_double_field=123.456,
            bool_field=True
        )

        c_pkt = c_PrimaryPacket()
        c_pkt.int_field = 3
        c_pkt.float_field = 3.14
        c_pkt.double_field = -3.14
        c_pkt.long_double_field = 123.456
        c_pkt.bool_field = True

        b_str = pkt.to_bytes()
        c_b_str = ctypes.string_at(ctypes.addressof(c_pkt), ctypes.sizeof(c_PrimaryPacket))

        self.assertEqual(b_str, c_b_str)

        parsed_pkt = PrimaryPacket.from_bytes(c_b_str)

        self.assertEqual(parsed_pkt.int_field, 3)
        self.assertAlmostEqual(parsed_pkt.float_field, 3.14, places=5)
        self.assertAlmostEqual(parsed_pkt.double_field, -3.14, places=5)
        self.assertAlmostEqual(parsed_pkt.long_double_field, 123.456, places=5)
        self.assertEqual(parsed_pkt.bool_field, True)

    def test_advpkt_inheritance(self):
        """
        This test verifies the functionality of Class Inheritance for Packets.
        See also GitHub Issue #84 (https://github.com/KronoSKoderS/CalPack/issues/84)
        """

        class TemplatePacket(models.Packet):
            PKT_UID = 0x00

            ID = models.IntField8()
            TYPE = models.IntField8()
            reserved0 = models.IntField16(bit_len=7)
            length = models.IntField16(bit_len=9)
            reserved1 = models.IntField32(bit_len=4)
            utcTimeUpper = models.IntField32(bit_len=28)
            utcTimeLower = models.IntField32()
            PacketStatus = models.IntField32()
            padding = models.IntField32()   
        
        class MyPacket(TemplatePacket): 
            PKT_UID = 0x0E


        t_pkt = TemplatePacket()
        m_pkt = MyPacket()

        # First let's check the original issue of the packet length:
        self.assertEqual(len(t_pkt), len(m_pkt))

        # Next, let's for sure verify that the fields are there:
        self.assertEqual(t_pkt.ID, m_pkt.ID)
        self.assertEqual(t_pkt.length, m_pkt.length)

        # Next, let's verify that the packets are indeed different:
        t_pkt.PacketStatus = 0xbeefcafe
        m_pkt.PacketStatus = 0xdeadbeef
        self.assertNotEqual(t_pkt.PacketStatus, m_pkt.PacketStatus)

        m_pkt.PacketStatus = 0xbeefcafe

        # check to make sure the output of the byte data
        # is the same
        self.assertEqual(t_pkt.to_bytes(), m_pkt.to_bytes())


        # Check to make sure the PKT_UID's remain correct
        self.assertEqual(t_pkt.PKT_UID, 0x00)
        self.assertEqual(m_pkt.PKT_UID, 0x0E)


    def test_advpkt_inheritance_with_additional_fields(self):
        """
        This test verifies that a `Packet` class can inherit from another class and have additional
        fields defined within it.
        """
        class MyPacketTemplate(models.Packet):
            PKT_TYPE = 0x0
            int_field = models.IntField()

        class MyPacket(MyPacketTemplate):
            PKT_TYPE = 0xE
            int_field2 = models.IntField()

        pkt = MyPacket()

        exptected_fields = ['int_field', 'int_field2']
        self.assertEqual(pkt.fields_order, exptected_fields)

        pkt.int_field = 1
        pkt.int_field2 = 2

        self.assertEqual(pkt.int_field, 1)
        self.assertEqual(pkt.int_field2, 2)

        class c_MyPacket(ctypes.Structure):
            _fields_ = (
                ('int_field', ctypes.c_uint),
                ('int_field2', ctypes.c_uint)
            )

        c_pkt = c_MyPacket()
        c_pkt.int_field = 1
        c_pkt.int_field2 = 2

        b_str = pkt.to_bytes()
        c_b_str = ctypes.string_at(ctypes.addressof(c_pkt), ctypes.sizeof(c_MyPacket))

        self.assertEqual(b_str, c_b_str)
