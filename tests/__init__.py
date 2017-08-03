import unittest

from tests.runtests import BasicPackets

def get_tests():
    return full_suite()


def full_suite():
    
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(BasicPackets),
    ])