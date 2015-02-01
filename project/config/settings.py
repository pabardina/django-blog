# -*- coding:utf8 -*-
from __future__ import unicode_literals


#==============================================================================
# Calculation of directories relative to the project module location
#==============================================================================

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
BASEPATH = os.path.abspath(os.path.dirname(__file__))


#==============================================================================
# Generic Django project settings
#==============================================================================

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TIME_ZONE = 'Europe/Paris'
USE_TZ = True
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('fr', 'Français'),
)

INSTALLED_APPS = (
    # django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # project app
    'blog',

    # lib / dependences
    'django_extensions',
    'pagedown', # App for adding markdown preview to the django admin
)

#==============================================================================
# SECRET KEY
#==============================================================================

SECRET_FILE = os.path.join(BASEPATH, 'secret.txt')

try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        from random import choice
        import string
        symbols = ''.join((string.ascii_lowercase,
                           string.digits,
                           string.punctuation))
        SECRET_KEY = ''.join([choice(symbols) for i in range(50)])
        secret = open(SECRET_FILE, 'w')
        secret.write(SECRET_KEY)
        secret.close()
    except IOError:
        raise Exception('Please create a %s file with random characters '
                        'to generate your secret key!' % SECRET_FILE)


#==============================================================================
# Templates
#==============================================================================

TEMPLATE_DIRS = (
    os.path.join(BASEPATH, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
    'django.core.context_processors.static',
    'django.core.context_processors.media',
]

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


#==============================================================================
# Middleware
#==============================================================================

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'


#==============================================================================
# Project URLS and media settings
#==============================================================================

STATIC_URL = '/static/'


#==============================================================================
# Import local settings
#==============================================================================

from .local_settings import *
