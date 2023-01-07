import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

os.environ['DJANGO_SETTINGS_MODULE'] = 'Infrastructure.settings'
test_dir = os.path.join(os.path.dirname(__file__), 'base_system')
sys.path.insert(0, test_dir)



def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    if hasattr(django, 'setup'):
        django.setup()
    failures = test_runner.run_tests(['base_system'])
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests()