Creating a Custom :code:`Field`
===============================
Creating a custom :code:`Field` is done by first subclassing the :code:`Field` class from :code:`calpack.models`.
There are a few things to consider before creating a custom Field:

    1. There are specific properties that **must** be defined within the class
    2. Any methods defined must be a class method and cannot be used as an instance method
    3. You must have a basic understanding of the :code:`ctypes` module specifically how to use the
        :code:`ctypes.Structure` class.  

It is recommended that you study the way that `Structures <https://docs.python.org/3/library/ctypes.html#structures-and-unions/>`_
are created if you are looking to create a custom Field.

With that said, defining a custom Field is actually quite simple.  The following properties **must** be defined
at either the class level or in a custom :code:`__init__`:

    * c_type - a :code:`ctypes` class to be used within the internal :code:`ctypes.Structure` instance.


Field Function Overrides
------------------------

Within your custom  :code:`Field` you can customize the following functions which are further defined in 
subsequent sections:

        * create_field_c_tuple
        * py_to_c
        * c_to_py

:code:`create_field_c_tuple`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This function is used to create the tuple that will go into the :code:`_fields_` property of the Packet's internal 
:code:`ctypes.Structure`.  It's also important to note that the first elements in the tuple **must** be the property 
:code:`self.field_name`.  CalPack will automatically populate this property for the Field class.  

As a default, CalPack's :code:`Field` super class defines :code:`create_field_c_tuple` as the following:

    def create_field_c_tuple(self):
        return (self.field_name, ctypes.c_int)

However this can be customized to suit the needs of the custom field.  Since this will be directly used to create the
:code:`ctypes.Structure._fields_` anything that is appropriate in creating the structure can be used here::

    def create_field_c_tuple(self):
        # return a c_int with only 4 bits as a field tuple.  Note: this is similar to how
        # we set the bit length of the IntField class.
        return (self.field_name, ctypes.c_int, 4)

    def create_field_c_tuple(self):
        # return a c_int Array as a field tuple.  Note: this is similar to how we set the 
        # array size of the ArrayField class.  
        return (self.field_name, ctypes.c_int * 10)

.. Warning:: If the first element in the field tuple **is not** :code:`self.field_name` then access to the internal 
    c structure will be broken and the packets will not be accessible properly.

:code:`py_to_c`
^^^^^^^^^^^^^^^
When setting a packet field to a value, that python object must be converted to a value that can be set for the 
internal :code:`ctypes.Structure` object of the packet.  Most occasions the value of the python object is already
appropriate.  By default this function does exactly that::

    def py_to_c(self, val):
        return val

However in certain cases additional formatting, transformation or validation might be required.  Use this function
to override the behavior as needed.  

:code:`c_to_py`
^^^^^^^^^^^^^^^
Similar to going from python objects to c, the reverse of going from c to python might need to be configured properly.  
Most occasions the value of the c object is already appropriate.  By default this function does exactly that::

    def c_to_py(self, c_field):
        return c_field

However in certain cases additional formatting, transformation or validation might be required.  Use this function
to override the behavior as needed.  

Full Example of Creating a Custom Field
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The following is a quick example of how to create a custom Field within CalPack::

    from calpack import models
    import ctypes 

    class UInt30(models.Field):
        c_type = ctypes.c_uint32
        bit_len = 30

        def __init__(self):
            super(UInt30, self).__init__()
            self.max_size = (2 << self.bit_len) - 1

        def create_field_c_tuple(self):
            return (self.field_name, self.c_type, self.bit_len)

        def py_to_c(self, val):
            if val < 0:
                raise ValueError("UInt30 must be a positive number!")

            if val > self.max_size:
                raise ValueError("UInt30 cannot be greater than {}".format(self.max_size))

            return val