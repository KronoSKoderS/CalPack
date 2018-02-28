"""
a set of utility functions for use within the models module.
"""
import sys

_NO_TYPE = object()


def typed_property(name, expected_type, default_val=None):
    """
    Simple function used to ensure a specific type for a property defined within a class.  This can ONLY be used
    within a class definition as the `self` keyword is used.

    :param str name: the name of the variable.  This can be anything, but cannot be already in use.
    :param type expected_type: the expected type.  When setting this property at the class level, if the types
        do not match, a :code:`TypeError` is raised.
    :param default_val: (Optional) the default value for the property.  If not set, then :code:`None` is used.  This
        MUST be of the same type as `expected_type` or a :code:`TypeError` is raised.
    :return: the property
    :raises TypeError: if the :code:`default_val` or property's set value is not of type :code:`expected_type`
    """
    if default_val is not None and not isinstance(default_val, expected_type):
        raise TypeError("{v} must be of type {t}".format(v=default_val, t=expected_type))

    storage_name = '_internal_' + name

    @property
    def prop(self):
        # Return the set value.  If the property hasn't been set yet then use the default value
        return getattr(self, storage_name, default_val)

    @prop.setter
    def prop(self, value):
        # Raise an error if `value` is not of the expected type.  This ensure proper type setting.
        if not isinstance(value, expected_type):
            raise TypeError("{v} must be of type {t}".format(v=value, t=expected_type))
        setattr(self, storage_name, value)

    return prop

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PYPY = "PyPy" in sys.version
