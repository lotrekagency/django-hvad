#!/usr/bin/env python
import django
from django.conf import settings
from django.core import checks
from django.test.utils import get_runner
from django.utils.encoding import force_str
from urllib.parse import urlparse
import argparse
import os.path
import sys

ROOT = os.path.abspath(os.path.dirname(__file__))

#=============================================================================

MIDDLEWARE_KEY = 'MIDDLEWARE' if django.VERSION >= (1, 10) else 'MIDDLEWARE_CLASSES'

CONFIGURATION = {
    'DEBUG': True,
    'USE_I18N': True,
    'LANGUAGE_CODE': 'en',
    'LANGUAGES': (
        ('en', 'English'),
        ('ja', '日本語'),
    ),
    #'FALLBACK_LANGUAGES': ('en', 'ja'),
    'SECRET_KEY': 'dummy',
    'ROOT_URLCONF': 'hvad.test_utils.project.urls',
    'TEMPLATES': [{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'django.template.context_processors.request',
        ]}
    }],
    MIDDLEWARE_KEY: (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.admindocs.middleware.XViewMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
    ),
    'INSTALLED_APPS': (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'django.contrib.staticfiles',
        'hvad',
        'hvad.test_utils.project.app',
        'django.contrib.messages'
    ),
    'STATIC_URL': '/static/',
    'DEFAULT_AUTO_FIELD': 'django.db.models.AutoField',
}

ENGINES = {
    'postgres': 'django.db.backends.postgresql_psycopg2',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'postgis': 'django.contrib.gis.db.backends.postgis',
    'mysql': 'django.db.backends.mysql',
    'sqlite': 'django.db.backends.sqlite3',
}

EXTRA = {
    'django.db.backends.postgresql_psycopg2': {
        'TEST': {'CHARSET': 'utf8'},
    },
    'django.db.backends.mysql': {
        'TEST': {'CHARSET': 'utf8', 'COLLATION': 'utf8_general_ci'},
    },
}

#=============================================================================

def parse_database(url):
    url = urlparse(url)
    engine = ENGINES[url.scheme]
    result = {
        'ENGINE': engine,
        'NAME': url.path.strip('/'),
        'HOST': url.hostname,
        'PORT': url.port,
        'USER': url.username,
        'PASSWORD': url.password,
    }
    result.update(EXTRA.get(engine, {}))
    return result

#=============================================================================

def main(database=None, failfast=False, verbosity=1, test_labels=None):
    test_labels = ['hvad.%s' % label for label in test_labels] if test_labels else ['hvad']
    if database is None:
        database = os.environ.get('DATABASE_URL', 'sqlite://localhost/hvad.db')
    config = CONFIGURATION.copy()
    config['DATABASES'] = {'default': parse_database(database)}
    settings.configure(**config)
    django.setup()
    from django.contrib import admin
    admin.autodiscover()

    errors = checks.run_checks()
    if errors:
        print('\n'.join(force_str(error) for error in errors))
        return 1

    TestRunner = get_runner(settings)
    test_runner = TestRunner(
        pattern='*.py',
        verbosity=verbosity,
        interactive=False,
        failfast=failfast
    )
    failures = test_runner.run_tests(test_labels)
    return 0 if failures == 0 else 2

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--database')
    parser.add_argument('--failfast', action='store_true')
    parser.add_argument('--verbosity', default=1)
    parser.add_argument('test_labels', nargs='*')
    args = parser.parse_args()

    sys.exit(main(**vars(args)))
