import unittest

def get_tests():
    return full_suite()


def full_suite():

    from .BasicPackets import Test_SimplePackets, Test_AdvancedPackets

    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(Test_SimplePackets),
        unittest.TestLoader().loadTestsFromTestCase(Test_AdvancedPackets),
    ])