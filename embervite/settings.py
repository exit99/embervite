import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Project Apps
    'events',
    # Third Party Apps
    'pipeline',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'embervite.middleware.LoginRequiredMiddleware',
)

ROOT_URLCONF = 'embervite.urls'

WSGI_APPLICATION = 'embervite.wsgi.application'


############
# DATABASE #
############


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


#############
# TEMPLATES #
#############


TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


##########
# STATIC #
##########

# url prefix for user uploaded files, stuff that django has to serve directly
MEDIA_URL = '/media/'
# url prefix for static files like css, js, images
STATIC_URL = '/static/'
# url prefix for *static* /admin media
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
# path to django-served media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# path used for collectstatic, *where the webserver not django will expect to find files*
STATIC_ROOT = os.path.join(BASE_DIR, 'public/')
# path to directories containing static files for django project, apps, etc, css/js
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
# List of finder classes that know how to find static files in various locations.
STATICFILES_FINDERS = (
    'pipeline.finders.PipelineFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
PIPELINE_ENABLED = True
PIPELINE_DISABLE_WRAPPER = False

PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.cssmin.CSSMinCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.jsmin.JSMinCompressor'

PIPELINE_CSS = {
    'site': {
        'source_filenames': (
            'css/bootstrap.min.css',
            'css/bootstrap-theme.min.css',
            'css/main.css',
        ),
        'output_filename': 'site.min.css',
    }
}

PIPELINE_JS = {
    'top-js': {
        'source_filenames': (
            'js/vendor/modernizr-2.6.2-respond-1.1.0.min.js',
            'js/jquery-2.1.1.min.js',
            'js/angular.min.js',

            'js/events/app.js',
            'js/events/controller.js',
            'js/events/directive.js',
        ),
        'output_filename': 'base.min.js',
    },
    'bottom-js': {
        'source_filenames': (
            'js/vendor/bootstrap.min.js',
            'js/main.js',
        ),
        'output_filename': 'base.min.js',
    }
}


############
# MESSAGES #
############

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'


import warnings
import exceptions
warnings.filterwarnings("ignore", category=exceptions.RuntimeWarning, module='django.db.backends.sqlite3.base', lineno=53)


###########
# TESTING #
###########

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

#########################
# LOCAL SETTINGS LOADER #
#########################

DEBUG_APPS = None
try:
    from embervite.local_settings import *
except ImportError:
    pass
else:
    INSTALLED_APPS += DEBUG_APPS
