"""
Django settings for scaffold project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import copy
from djangae.settings_base import * #Set up some AppEngine specific stuff
from django.core.urlresolvers import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

from .boot import get_app_config
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_app_config().secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# Application definition

INSTALLED_APPS = (
    'djangae', # Djangae needs to come before django apps in django 1.7 and above
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangosecure',
    'csp',
    'cspreports',
    'djangae.contrib.gauth.datastore',
    'djangae.contrib.security',
    'blog',
)

MIDDLEWARE_CLASSES = (
    'djangae.contrib.security.middleware.AppEngineSecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'djangae.contrib.gauth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'csp.middleware.CSPMiddleware',
    'session_csrf.CsrfMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "session_csrf.context_processor"
)

SECURE_CHECKS = [
    "djangosecure.check.sessions.check_session_cookie_secure",
    "djangosecure.check.sessions.check_session_cookie_httponly",
    "djangosecure.check.djangosecure.check_security_middleware",
    "djangosecure.check.djangosecure.check_sts",
    "djangosecure.check.djangosecure.check_frame_deny",
    "djangosecure.check.djangosecure.check_ssl_redirect",
    "scaffold.checks.check_session_csrf_enabled",
    "scaffold.checks.check_csp_is_not_report_only"
]

CSP_REPORT_URI = reverse_lazy('report_csp')
CSP_REPORTS_LOG = True
CSP_REPORTS_LOG_LEVEL = 'warning'
CSP_REPORTS_SAVE = True
CSP_REPORTS_EMAIL_ADMINS = False

ROOT_URLCONF = 'scaffold.urls'

WSGI_APPLICATION = 'scaffold.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = 'static'

# Default CSP settings, used as the basis for both development and production settings
DEFAULT_CSP_DEFAULT_SRC = ("'self'", "*.gstatic.com")
DEFAULT_CSP_STYLE_SRC = ("'self'", "fonts.googleapis.com", 
                         "*.gstatic.com", "maxcdn.bootstrapcdn.com")
DEFAULT_CSP_FONT_SRC = ("'self'", "themes.googleusercontent.com", "*.gstatic.com")
DEFAULT_CSP_FRAME_SRC = ("'self'", "www.google.com", "www.youtube.com", 
                         "accounts.google.com", "apis.google.com", "plus.google.com")
DEFAULT_CSP_SCRIPT_SRC = ("'self'", "*.googleanalytics.com", 
                          "*.google-analytics.com", "ajax.googleapis.com", "maxcdn.bootstrapcdn.com")
DEFAULT_CSP_IMG_SRC = ( "*" )   # Set open to allow users to link to images from anywhere
DEFAULT_CSP_CONNECT_SRC = ("'self'", "plus.google.com", "www.google-analytics.com")

# CSP settings for development (DEBUG=True) mode. For production CSP settings see settings_live.py
CSP_DEFAULT_SRC = copy.copy( DEFAULT_CSP_DEFAULT_SRC )
CSP_STYLE_SRC = copy.copy( DEFAULT_CSP_STYLE_SRC )
CSP_FONT_SRC = copy.copy( DEFAULT_CSP_FONT_SRC )
CSP_FRAME_SRC = copy.copy( DEFAULT_CSP_FRAME_SRC )
CSP_SCRIPT_SRC = copy.copy( DEFAULT_CSP_SCRIPT_SRC )
CSP_IMG_SRC = copy.copy( DEFAULT_CSP_IMG_SRC )
CSP_CONNECT_SRC = copy.copy( DEFAULT_CSP_CONNECT_SRC )

# In debug mode it seems that on Firefox, https sources have to be added in manually
CSP_STYLE_SRC = CSP_STYLE_SRC + ( "https://maxcdn.bootstrapcdn.com", )
CSP_SCRIPT_SRC = CSP_SCRIPT_SRC + ( "https://ajax.googleapis.com", "https://maxcdn.bootstrapcdn.com" )

from djangae.contrib.gauth.settings import *
