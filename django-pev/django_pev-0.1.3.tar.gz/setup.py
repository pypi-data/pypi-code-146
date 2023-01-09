# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_pev']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.2', 'sqlparse']

setup_kwargs = {
    'name': 'django-pev',
    'version': '0.1.3',
    'description': 'Context manager to upload explain plans to https://explain.dalibo.com/',
    'long_description': '# Django Postgres Explain Visualizer (Django-PEV)\n\n[![PyPI version](https://badge.fury.io/py/django-pev.svg)](https://pypi.org/project/django-pev/)\n[![versions](https://img.shields.io/pypi/pyversions/django-pev.svg)](https://pypi.org/project/django-pev/)\n[![Lint](https://github.com/uptick/django-pev/actions/workflows/ci.yaml/badge.svg)](https://github.com/uptick/django-pev/actions/workflows/ci.yaml)\n\nThis tool captures sql queries and uploads the query plan to postgresql explain visualizer (PEV) by [dalibo](https://explain.dalibo.com/). This is especially helpful for debugging slow queries.\n\n# Usage\n\nWrap some code with the explain context manager. All sql queries are captured\nalongside a stacktrace (to locate where it was called). The slowest query is accessible via `.slowest`.\n\n```python\nimport django_pev\nfrom django.contrib.auth.models import User\n\nwith django_pev.explain() as e:\n    # Every SQL query is captured\n    list(User.objects.filter(email=\'test@test.com\').all())\n\n# Rerun the slowest query with `EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON)`\npev_response = e.slowest.visualize(\n    # By default the text of the query is not uploaded for security reasons\n    upload_query=True,\n    # Set to false if the query is slow and you want only an explain\n    analyze=True,\n    # Give a helpful title for the uploaded query plan\n    title="Measuring email filter",\n)\nprint(pev_response.url)\n\n# View the postgres explain visualization\ne.slowest.visualize_in_browser()\n\n# View the stack trace of the slowest query\nprint(e.slowest.stacktrace)\n\n# Delete the plan hosted on https://explain.dalibo.com\npev_response.delete()\n```\n\n**How to debug a slow endpoint in production**\n\nIf you have access to `python manage.py shell` on the production server;\nyou can run the following code snippet to get an explain plan uploaded. In general this technique is all types of profiling.\n\n```python\nimport django_pev\n\nfrom django.contrib.auth.models import User\nfrom django.test import Client as TestClient\n\nclient = TestClient()\n# Authentication\nclient.force_login(User.objects.get(id=1))\nurl = "/some_slow_url"\n\nwith django_pev.explain() as e:\n    response = client.get(url)\n\nprint(e.slowest.visualize(title=f"Fetching {url}"))\n\n```\n\n# Disclaimer\n\nCredit goes to Pierre Giraud (@pgiraud) for PEV2 and Alex Tatiyants (@AlexTatiyants) for the original pev tool.\n\nIN NO EVENT SHALL DALIBO BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF DALIBO HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n\nDALIBO SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND DALIBO HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.\n',
    'author': 'william chu',
    'author_email': 'william.chu@uptickhq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
