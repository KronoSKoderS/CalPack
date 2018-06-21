"""
"""

__all__ = [
    'Field'
]


class Field(object):
    """
    A Super class that all other fields inherit from.  This class is NOT intended for direct use.
    Custom Fields MUST inherit from this class.

    When creating a custom field you MUST define the :code:`c_type` property with a valid
    :code:`ctypes` data class.

    :param default_val: the default value of the field.  This is set at instantiation of the Field
    """
    c_type = None
    field_name = None

    creation_counter = 0

    def __init__(self, default_val=None):
        super(Field, self).__init__()
        self.default_val = default_val

        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1

    def __get__(self, instance, cls):
        from calpack.models import Packet
        # If being called from a parent "Packet" class, then we actually want to get the internal
        # field value
        if isinstance(instance, Packet):
            return self.c_to_py(instance.get_c_field(self.field_name))
        return self

    def __set__(self, instance, val):
        from calpack.models import Packet
        if isinstance(instance, Packet):
            c_val = self.py_to_c(val)
            instance.set_c_field(self.field_name, c_val)

    def py_to_c(self, val):
        """
        py_to_c - A function used to convert a python object into a valid ctypes assignable object.
        As a default this function simply returns :code:`val`.  It's up to the other subclassesed
        :code:`Field` to define this if further formatting is required in order to set the internal
        structure of the packet.

        :param val: the value the user is attempting to set the packet field to.  This can be any
            python object.
        """
        return val

    def c_to_py(self, c_field):
        """
        c_to_py - A function used to convert the ctypes object into a python object.  As a default
        this function simply returns :code:`c_field` directly from the ctypes.Structure object.
        It's up to the other :code:`Field`'s to define this if further formatting is required in
        order to turn the ctypes value into something user friendly.

        :param c_field: a ctypes object from the packet's internal :code:`ctypes.Structure` object
        """
        return c_field

    def create_field_c_tuple(self):
        """
        create_field_c_tuple - A function used to create the required an field in the
        :code:`ctypes.Structure._fields_` tuple.  This must return a tuple that is acceptable for
        one of the items in the :code:`_fields_` list of the :code:`ctypes.Structure`.

        The first value in the tuple MUST be :code:`self.field_name` as this is used to access the
            internal c structure.
        """
        return (self.field_name, self.c_type)
