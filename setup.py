import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-macaddress",
    version = "1.3.0",
    url = 'http://github.com/tubaman/django-macaddress',
    license = 'BSD',
    description = "MAC address model and form fields for Django apps.",
    long_description = read('README.rst'),
    author = 'Ryan Nowakowski',
    author_email = 'tubaman@fattuba.com',
    maintainer = 'Arun K. R.',
    maintainer_email = 'the1.arun@gmail.com',
    packages = ['macaddress'],
    install_requires = ['netaddr'],
    tests_require = ['django'],

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
