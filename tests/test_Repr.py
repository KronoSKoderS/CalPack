import unittest

from calpack import models
from calpack.utils import PY2, PYPY


class Test_Repr(unittest.TestCase):

    def test_simple_repr(self):
        class two_int_pkt(models.Packet):
            field1 = models.IntField()
            field2 = models.IntField()

        pkt = two_int_pkt()

        expected_py3 = "two_int_pkt(field1=0, field2=0)"
        expected_py2 = "two_int_pkt(field1=0L, field2=0L)"
        self.assertEqual(repr(pkt), expected_py2 if PY2 and not PYPY else expected_py3)

        pkt.field1 = 1234
        pkt.field2 = 5678

        expected_py3 = "two_int_pkt(field1=1234, field2=5678)"
        expected_py2 = "two_int_pkt(field1=1234L, field2=5678L)"
        self.assertEqual(repr(pkt), expected_py2 if PY2 and not PYPY else expected_py3)
