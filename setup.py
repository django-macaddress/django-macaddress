import os
from setuptools import setup, find_packages

version = "1.4.0"

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-macaddress",
    version = version,
    url = 'http://github.com/tubaman/django-macaddress',
    license = 'BSD',
    description = "MAC address model and form fields for Django apps.",
    long_description = read('README.rst'),
    author = 'Ryan Nowakowski',
    author_email = 'tubaman@fattuba.com',
    maintainer = 'Arun K. R.',
    maintainer_email = 'the1.arun@gmail.com',
    packages = ['macaddress', 'macaddress.tests'],
    install_requires = ['netaddr'],
    tests_require = ['django'],
    test_suite="runtests.runtests",

    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
