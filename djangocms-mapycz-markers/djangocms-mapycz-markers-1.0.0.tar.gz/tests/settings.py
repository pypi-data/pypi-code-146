"""Test settings."""

SECRET_KEY = "secret"
SITE_ID = 1
STATIC_URL = '/static/'
ROOT_URLCONF = 'tests.urls'

INSTALLED_APPS = (
    # Django apps requirted set.
    "django",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.forms.fields",
    'sekizai',
    "cms",
    "menus",
    "treebeard",
    ## Dependencies for Aldryn forms.
    # "easy_thumbnails",
    # "filer",
    # "aldryn_forms",
    ## The plugin.
    'djangocms_mapycz_markers',
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "tests",
    }
}

LANGUAGES = (
    ('en-us', 'English'),
    ('cs', 'Česky'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['tests/templates'],
        'OPTIONS': {
            'context_processors': [
                # Django's defaults.
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',  # Needed by Django CMS.

                # Django CMS's core context processors.
                'cms.context_processors.cms_settings',
                'sekizai.context_processors.sekizai',  # Static file management for template blocks.

                # Other Django's modules.
                'constance.context_processors.config',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
]

CMS_TEMPLATES = (
    ('page.html', 'Page'),
)
