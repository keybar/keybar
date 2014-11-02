import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, '..', '..')

SECRET_KEY = 'na2p&yexkp-g83$2m^&b!r+a%nv2ci1!d9vh^a_7h!hv*7&h79'

DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

SITE_ID = 1

INSTALLED_APPS = (
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Asyncronous worker support
    'celery',
    'kombu.transport.django',

    # i18n/l10n
    'django_babel',
    'statici18n',

    # For our REST Api
    'rest_framework',

    # Form helpers
    'floppyforms',

    # user (social-) account management
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',

    # Keybar apps
    'keybar',
    'keybar.core',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'keybar.urls'

WSGI_APPLICATION = 'keybar.wsgi.application'

AUTH_USER_MODEL = 'keybar.User'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'db.sqlite3'),
    }
}

TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'bower_components'),
    os.path.join(PROJECT_DIR, 'src', 'keybar', 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'src', 'keybar', 'templates'),
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('de', _('German')),
    ('en', _('English')),
)

LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'src/keybar/locale'),
    os.path.join(PROJECT_DIR, 'src/keybar/templates/locale'),
)

# Do not make the session and csrf cookie secure (https:// only)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'web', 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'web', 'media')

# Celery / Queue configuration
from kombu import Queue

BROKER_URL = "django://"

# Per default process all celery tasks in-process.
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

# Only accept JSON. This will be the default in Celery 3.2
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

# Explicitly set default queue and exchange types. This is only useuseful for
# RabbitMQ but still good to have as a general rule.
CELERY_DEFAULT_QUEUE = "default"
CELERY_DEFAULT_EXCHANGE = "default"
CELERY_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_DEFAULT_ROUTING_KEY = "default"
CELERY_CREATE_MISSING_QUEUES = True

# Track started tasks. This adds a new STARTED state once a task
# is started by the celery worker.
CELERY_TRACK_STARTED = True

CELERY_QUEUES = (
    Queue('default', routing_key='default'),
    Queue('celery', routing_key='celery'),
)

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERYBEAT_MAX_LOOP_INTERVAL = 3600
CELERY_DISABLE_RATE_LIMITS = True

# Make our `LOGGING` configuration the only truth and don't let celery
# overwrite it.
CELERYD_HIJACK_ROOT_LOGGER = False

# Don't log celery log-redirection as warning (default).
# We manage our logging through `django.conf.settings.LOGGING` and
# want that to be our first-citizen config.
CELERY_REDIRECT_STDOUTS_LEVEL = 'INFO'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'formatters': {
        'verbose': {
            'format':
                '[%(asctime)s] %(levelname)s:%(name)s %(funcName)s\n %(message)s',  # noqa
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'loggers': {
        # This is the root logger that catches everything, if there's no other
        # match on the logger name. If we want custom logging handing for our
        # code vs. third-party code, define loggers for each module/app
        # that's using standard python logging.
        'root': {
            'level': 'INFO',
            'handlers': ['console'],
        },
        'celery': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'keybar': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'django': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Django security related settings.
SECURE_SSL_REDIRECT = True

# Commit to HTTPS only for 12 months (HSTS)
SECURE_HSTS_SECONDS = 31536000

# prevent framing
SECURE_FRAME_DENY = True

# Don't let the browser guess content-types
SECURE_CONTENT_TYPE_NOSNIFF = True

# Enable browser XSS Filter
SECURE_BROWSER_XSS_FILTER = True

# Force cookies to be https only (or at least tell the browsers to do so...)
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

LOGIN_URL = reverse_lazy('account_login')
LOGIN_REDIRECT_URL = reverse_lazy('keybar-index')


# Django REST Framework related settings.

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
       'keybar.core.auth.KeybarApiSignatureAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

# (social-) auth related settings

ACCOUNT_AUTHENTICATION_METHOD = 'email'

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_EMAIL_VERIFICATION = 'optional'

ACCOUNT_EMAIL_SUBJECT_PREFIX = 'Keybar - '

ACCOUNT_SIGNUP_FORM_CLASS = 'keybar.web.forms.RegisterForm'

ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False

ACCOUNT_UNIQUE_EMAIL = True

ACCOUNT_USER_DISPLAY = 'keybar.utils.get_user_name'

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'

ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = False

ACCOUNT_SESSION_REMEMBER = False

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED

SOCIALACCOUNT_AUTO_SIGNUP = True

# Keybar related settings

GPG_BIN = '/usr/bin/gpg'
GPG_HOME = ''

KEYBAR_SERVER_CERTIFICATE = None
KEYBAR_SERVER_KEY = None

KEYBAR_CLIENT_CERTIFICATE = None
KEYBAR_CLIENT_KEY = None


try:
    import certifi
except ImportError:
    certifi = None


def _default_ca_certs():
    if certifi is None:
        raise Exception('The \'certifi\' package is required to use https')
    return certifi.where()


KEYBAR_CA_BUNDLE = _default_ca_certs()

# NOTE: CHANGING THOSE VALUES REQUIRES RE-ENCRYPTION OF EVERYTHING
# AND HAS SOME DEEP IMPACT. JUST DONT!
KEYBAR_KDF_SALT_LENGTH = 16
KEYBAR_KDF_LENGTH = 32

# In 2013 100,000 was the recommended value, so we settle with one million
# for now.
KEYBAR_KDF_ITERATIONS = 1000000

KEYBAR_DOMAIN = None
KEYBAR_HOST = None

# Django 1.7: Required to silence the check if `ModelAdmin.search_fields` is
# a list. We generate this list dynamically, thus it's working but the check
# framework does not evaluate the expressions and fails.
SILENCED_SYSTEM_CHECKS = ['admin.E126']
