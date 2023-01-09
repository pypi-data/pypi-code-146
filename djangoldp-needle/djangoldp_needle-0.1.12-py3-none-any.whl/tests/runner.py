import sys

import django
from django.conf import settings as django_settings
from djangoldp.conf.ldpsettings import LDPSettings

# create a test configuration
config = {
    # add the packages to the reference list
    'ldppackages': [
        'djangoldp_account',
        'djangoldp_needle',
        'djangoldp_needle.tests'
    ],

    # required values for server
    'server': {
        'AUTH_USER_MODEL': 'djangoldp_account.LDPUser',
        'REST_FRAMEWORK': {
            'DEFAULT_PAGINATION_CLASS': 'djangoldp.pagination.LDPPagination',
            'PAGE_SIZE': 5
        },
        # map the config of the core settings (avoid asserts to fail)
        'SITE_URL': 'http://happy-dev.fr',
        'BASE_URL': 'http://happy-dev.fr',
    }
}

ldpsettings = LDPSettings(config)
django_settings.configure(ldpsettings)

django.setup()
from django.test.runner import DiscoverRunner

test_runner = DiscoverRunner(verbosity=1)

failures = test_runner.run_tests([
    'djangoldp_needle.tests.test_first_annotation_on_user_creation',
    'djangoldp_needle.tests.test_annotation_target_add',
    'djangoldp_needle.tests.test_annotation_add',
    'djangoldp_needle.tests.test_annotation_activity'
])
if failures:
    sys.exit(failures)

