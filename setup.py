from os.path import dirname, join
from setuptools import setup

from macaddress.version import __version__ as version


def read(fname):
    return open(join(dirname(__file__), fname)).read()

setup(
    name="django-macaddress",
    version=version,
    url='http://github.com/tubaman/django-macaddress',
    license='BSD',
    description="MAC address model and form fields for Django apps.",
    long_description=read('README.rst'),
    author='Ryan Nowakowski',
    author_email='tubaman@fattuba.com',
    maintainer='Arun Karunagath',
    maintainer_email='the1.arun@gmail.com',
    packages=['macaddress', 'macaddress.tests'],
    tests_require=['Django'],
    test_suite="runtests.runtests",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
