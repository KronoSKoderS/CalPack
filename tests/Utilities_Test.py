import unittest
from calpack import models


class Test_Utilities(unittest.TestCase):
    def test_util_invalid_typed_property(self):
        with self.assertRaises(TypeError):
            class temp(models.Field):
                meh = models.typed_property('meh', str, 123)

        class temp2(models.Field):
            meh = models.typed_property('meh', str)

            def __init__(otherself, **kwargs):
                super(temp2, otherself).__init__(**kwargs)

                with self.assertRaises(TypeError):
                    otherself.meh = 123

        test = temp2()
        with self.assertRaises(TypeError):
            test.meh = 123


if __name__ == '__main__':
    unittest.main()
