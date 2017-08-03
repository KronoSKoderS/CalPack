from setuptools import setup, find_packages


version = "0.1.0"

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    long_description=''

setup(
    name='concorde',
    version=version,
    description='Object Oriented API calls to the Pushover Service',
    long_description=long_description,
    url='https://github.com/KronosKoderS/concorde',
    download_url='https://github.com/KronosKoderS/concorde/tarball/v' + version,
    author='KronoSKoderS',
    author_email='superuser.kronos@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite="tests.get_tests",
    packages=find_packages(exclude=['tests'])
)