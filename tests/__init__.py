import unittest


def get_tests():
    return full_suite()


def full_suite():

    from .BasicPackets_Test import TestSimplePackets#, TestAdvancedPackets

    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestSimplePackets),
#        unittest.TestLoader().loadTestsFromTestCase(Test_AdvancedPackets),
    ])

if __name__ == "__main__":
    unittest.main()