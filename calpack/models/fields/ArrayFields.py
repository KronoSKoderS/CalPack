"""
"""

__all__ = [
    'ArrayField'
]

from calpack.models.fields.Fields import Field

class ArrayField(Field):
    """
    A custom field for handling an array of fields.  Only tuples or other ArrayFields can be written to the

    :param array_cls: a :code:`calpack.models.Field` subclass **object** that represent the Field
        the array will be filled with.
    :param int array_size: the length of the array.
    """
    def __init__(self, array_cls, array_size, default_val=None):
        super(ArrayField, self).__init__(default_val)
        self.array_cls = array_cls
        self.array_size = array_size

        array_cls_tuple = self.array_cls.create_field_c_tuple()
        if len(array_cls_tuple) == 3:
            raise TypeError(
                "ArrayField does not support Fields with non-byte aligned field tuples!"
            )
        self.c_type = (array_cls_tuple[1] * self.array_size)

    def c_to_py(self, c_field):
        return tuple(c_field[:])

    def py_to_c(self, val):
        if not isinstance(val, ArrayField) and not isinstance(val, tuple) and not isinstance(val, list):
            raise TypeError("Must be of type ArrayField or list")

        if len(val) != self.array_size:
            raise ValueError("The length of val must be {}!".format(self.array_size))

        return self.c_type(*val)

    def __len__(self):
        return self.array_size