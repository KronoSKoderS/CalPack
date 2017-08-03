import unittest

def get_tests():
    return full_suite()


def full_suite():

    from .runtests import BasicPackets

    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(BasicPackets),
    ])