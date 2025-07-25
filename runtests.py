#!/usr/bin/env python
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


SETTINGS = {
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    'INSTALLED_APPS': (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.admin',
        'macaddress',
    ),
    'SITE_ID': 1,
    'SECRET_KEY': 'this-is-just-for-tests-so-not-that-secret',
    'TEMPLATES': [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ]
            }
        }
    ],
    'MIDDLEWARE': (
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
    ),
    'DEFAULT_AUTO_FIELD': 'django.db.models.AutoField',
}

if not settings.configured:
    settings.configure(**SETTINGS)




def runtests():
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['macaddress'])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
