from setuptools import setup, find_packages


version = "2018.5.1"

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    long_description="""
This package is intended to make creating and/or parsing packets (structured bytecode) on the fly quick and easy.  This is a wrapper around
the .. _ctypes module: https://docs.python.org/dev/library/ctypes.html built-in to python. This package is designed
with influence from Django's modeling and will look familiar to those that have used it.
    """

setup(
    name='calpack',
    version=version,
    description='Packets in Python made Simple',
    long_description=long_description,
    url='https://github.com/KronosKoderS/CalPack',
    download_url='https://github.com/KronosKoderS/CalPack/tarball/v' + version,
    author='KronoSKoderS',
    author_email='superuser.kronos@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',

        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',

        'Natural Language :: English',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        'Topic :: Utilities',
    ],
    test_suite="tests.get_tests",
    packages=find_packages(exclude=['tests', 'docs'])
)
