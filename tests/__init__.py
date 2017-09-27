import unittest


def get_tests():
    return full_suite()


def full_suite():

    from .BasicPackets_Test import TestIntField, TestSimplePackets
    from .Utilities_Test import Test_Utilities_Test

    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestIntField),
        unittest.TestLoader().loadTestsFromTestCase(TestSimplePackets),
        untitest.TestLoader().loadtestsFromTestCase(Test_Utilities_Test),
    ])

if __name__ == "__main__":
    unittest.main()