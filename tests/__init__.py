import unittest
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

def get_tests():
    return full_suite()


def full_suite():

    from tests.test_IntFields import Test_IntField
    from tests.test_BasicPackets import Test_BasicPacket, Test_EndianPacket
    from tests.test_ArrayField import Test_ArrayField
    from tests.test_PacketField import Test_PacketField
    from tests.test_Utilities import Test_Utilities
    from tests.test_AdvancedPackets import Test_AdvancedPacket
    from tests.test_FlagField import Test_FlagField
    from tests.test_FloatFields import Test_FloatField, Test_DoubleField, Test_LongDoubleField
    from tests.test_BoolField import Test_BoolField
    from tests.test_Repr import Test_Repr

    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(Test_BasicPacket),
        unittest.TestLoader().loadTestsFromTestCase(Test_EndianPacket),
        unittest.TestLoader().loadTestsFromTestCase(Test_IntField),
        unittest.TestLoader().loadTestsFromTestCase(Test_ArrayField),
        unittest.TestLoader().loadTestsFromTestCase(Test_PacketField),
        unittest.TestLoader().loadTestsFromTestCase(Test_Utilities),
        unittest.TestLoader().loadTestsFromTestCase(Test_AdvancedPacket),
        unittest.TestLoader().loadTestsFromTestCase(Test_FlagField),
        unittest.TestLoader().loadTestsFromTestCase(Test_FloatField),
        unittest.TestLoader().loadTestsFromTestCase(Test_DoubleField),
        unittest.TestLoader().loadTestsFromTestCase(Test_LongDoubleField),
        unittest.TestLoader().loadTestsFromTestCase(Test_BoolField),
        unittest.TestLoader().loadTestsFromTestCase(Test_Repr)
    ])

if __name__ == "__main__":
    unittest.main()
