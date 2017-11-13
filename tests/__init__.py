import unittest
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

def get_tests():
    return full_suite()


def full_suite():

    from .IntField_Test import TestIntField
    from .BasicPackets_Test import TestSimplePacket

    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestIntField),
        unittest.TestLoader().loadTestsFromTestCase(TestSimplePacket),
    ])

if __name__ == "__main__":
    unittest.main()