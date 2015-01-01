SECRET_KEY = 'Here'

DEBUG = True

TEMPLATE_DEBUG = True

DEBUG_APPS = (
    'django_extensions',
    'django_nose',
)

PIPELINE_VERSION = False

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = ''
SERVER_EMAIL = ''
