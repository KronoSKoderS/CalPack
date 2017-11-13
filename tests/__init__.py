import unittest
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

def get_tests():
    return full_suite()


def full_suite():

    from .IntField_Test import Test_IntField
    from .BasicPackets_Test import Test_BasicPacket
    from .ArrayField_Test import Test_ArrayField
    from .PacketField_Test import Test_PacketField

    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(Test_BasicPacket),
        unittest.TestLoader().loadTestsFromTestCase(Test_IntField),
        unittest.TestLoader().loadTestsFromTestCase(Test_ArrayField),
        unittest.TestLoader().loadTestsFromTestCase(Test_PacketField)
    ])

if __name__ == "__main__":
    unittest.main()