import unittest


def get_tests():
    return full_suite()


def full_suite():

    from .BasicPackets_Test import TestSimplePackets

    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestSimplePackets),
    ])

if __name__ == "__main__":
    unittest.main()