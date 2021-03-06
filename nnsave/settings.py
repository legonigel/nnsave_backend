"""
Django settings for nnsave_backend project.

Copyright (C) 2016 Nigel Armstrong legonigel@gmail.com
All rights reserved.

This software may be modified and distributed under the terms
of the MIT license. See LICENSE file for details

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kek#gm$i89u66mbb=ld6loi4v)i5x%gazv*8+*8&ra-xe(ke5$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'import_export',
    'nnsave_app'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'nnsave.urls'

WSGI_APPLICATION = 'nnsave.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
	'ENGINE': 'django.contrib.gis.db.backends.postgis',
	'NAME': 'nnsave',
	'USER': 'nnsave_user',
	'PASSWORD': 'nnsave_password',
	'HOST': 'localhost',
	'PORT': ''
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'


#Suppress 110 warnings
import logging, copy
from django.utils.log import DEFAULT_LOGGING

LOGGING = copy.deepcopy(DEFAULT_LOGGING)
LOGGING['filters']['suppress_deprecated'] = {
    '()': 'nnsave.settings.SuppressDeprecated'
}
class SuppressDeprecated(logging.Filter):
    def filter_deprecation_warnings(self, record):
	warnings_to_filter = [
	    'RemovedInDjango110Warning'
	]
	return not any([warn in record.getMessage() for warn in warnings_to_filter])
