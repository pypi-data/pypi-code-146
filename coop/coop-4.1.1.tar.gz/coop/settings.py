import posixpath

# Misc rubbish
SITE_ID = 1
DEFAULT_PER_PAGE = 20

# Sites built on coop all share a common URL structure and WSGI application
ROOT_URLCONF = 'coop.urls'
WSGI_APPLICATION = 'coop.wsgi.application'


# URLs for assets
ASSETS_URL = '/assets/'
MEDIA_URL = posixpath.join(ASSETS_URL, 'media/')
STATIC_URL = posixpath.join(ASSETS_URL, 'static/')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'


# What is installed by default
INSTALLED_APPS = [
    'coop',

    # Third party apps
    'taggit',
    'modelcluster',
    'wagtailmetadata',
    'wagtailcache',
    'wagtailfontawesome',
    'webpack_loader',
    'honeypot',

    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.sitemaps.views',

    # Wagtail apps
    'wagtail',
    'wagtail.admin',
    'wagtail.documents',
    'wagtail.snippets',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.images',
    'wagtail.embeds',
    'wagtail.search',
    'wagtail.contrib.redirects',
    'wagtail.contrib.settings',
    'wagtail.contrib.table_block',
]

try:
    import diskcache  # noqa
    INSTALLED_APPS.append('diskcache')

    DISK_CACHE = {
        'BACKEND': 'diskcache.DjangoCache',
        'LOCATION': '/srv/cache',
        'TIMEOUT': 300,
        # ^-- Django setting for default timeout of each key.
        'SHARDS': 8,
        'DATABASE_TIMEOUT': 0.010,  # 10 milliseconds
        # ^-- Timeout for each DjangoCache database transaction.
        'OPTIONS': {
            'size_limit': 2 ** 30   # 1 gigabyte
        },
    }
    CACHES = {
        'default': DISK_CACHE,
        'renditions': DISK_CACHE
    }
except ImportError:
    pass


# Localisation - most sites are Australian
TIME_ZONE = 'Australia/Hobart'
LANGUAGE_CODE = 'en-au'

USE_I18N = True
USE_L10N = False
USE_TZ = True


# Standard middleware required by Wagtail
MIDDLEWARE = [
    'bugsnag.django.middleware.BugsnagMiddleware',
    'wagtailcache.cache.UpdateCacheMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'wagtailcache.cache.FetchFromCacheMiddleware',
]


# Wagtail uses Django templates, but we use Jinja templates.
# Some common Jinja extensions are used that cover most use-cases we need.
TEMPLATES_DJANGO = {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
            'django.template.context_processors.request',
            'wagtail.contrib.settings.context_processors.settings',
        ]
    }
}
TEMPLATES_JINJA = {
    'BACKEND': 'django.template.backends.jinja2.Jinja2',
    'APP_DIRS': True,
    'OPTIONS': {
        'extensions': [
            'wagtail.jinja2tags.core',
            'wagtail.admin.jinja2tags.userbar',
            'wagtail.images.jinja2tags.images',
            'wagtail.contrib.settings.jinja2tags.settings',
            'coop.jinja2tags.core.Extension',
            'wagtailmetadata.jinja2tags.WagtailMetadataExtension',
        ],
    },
}

TEMPLATES = [TEMPLATES_DJANGO, TEMPLATES_JINJA]
WAGTAIL_CACHE = True


# Who to email when things break
ADMINS = [
    ('Django debug', 'django@neonjungle.studio'),
]
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'bugsnag_filter': {
            '()': 'coop.logging.RequireNoBugsnagSetting'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false', 'bugsnag_filter'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

# Stop us from getting moderation emails by default
WAGTAILADMIN_NOTIFICATION_INCLUDE_SUPERUSERS = False

# Max image upload size
WAGTAILIMAGES_MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100mb

# Add the 'responsive-object' class to embeds by default
WAGTAILEMBEDS_RESPONSIVE_HTML = True

# Override if you actually need a zip_code
HONEYPOT_FIELD_NAME = 'zip_code'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
