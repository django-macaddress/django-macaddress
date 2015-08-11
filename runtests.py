#!/usr/bin/env python
import sys

import django
from django.conf import settings


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.admin',
            'macaddress.tests',
            'macaddress',
        ),
        SITE_ID=1,
        SECRET_KEY='this-is-just-for-tests-so-not-that-secret',
        MIDDLEWARE_CLASSES=(),
    )


from django.test.utils import get_runner


def runtests():
    if hasattr(django, 'setup'):
        django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    apps = ['macaddress', ]
    failures = test_runner.run_tests(apps)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
