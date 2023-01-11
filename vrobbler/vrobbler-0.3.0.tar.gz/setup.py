# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vrobbler',
 'vrobbler.apps.music',
 'vrobbler.apps.music.migrations',
 'vrobbler.apps.scrobbles',
 'vrobbler.apps.scrobbles.migrations',
 'vrobbler.apps.videos',
 'vrobbler.apps.videos.migrations']

package_data = \
{'': ['*'],
 'vrobbler': ['templates/*', 'templates/scrobbles/*', 'templates/videos/*']}

install_requires = \
['Django>=4.0.3,<5.0.0',
 'Markdown>=3.3.6,<4.0.0',
 'Pillow>=9.0.1,<10.0.0',
 'colorlog>=6.6.0,<7.0.0',
 'dj-database-url>=0.5.0,<0.6.0',
 'django-allauth>=0.50.0,<0.51.0',
 'django-celery-results>=2.3.0,<3.0.0',
 'django-extensions>=3.1.5,<4.0.0',
 'django-filter>=21.1,<22.0',
 'django-markdownify>=0.9.1,<0.10.0',
 'django-mathfilters>=1.0.0,<2.0.0',
 'django-simple-history>=3.1.1,<4.0.0',
 'django-taggit>=2.1.0,<3.0.0',
 'djangorestframework>=3.13.1,<4.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'psycopg2[production]>=2.9.3,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'python-json-logger>=2.0.2,<3.0.0',
 'redis>=4.2.2,<5.0.0',
 'whitenoise>=6.3.0,<7.0.0']

entry_points = \
{'console_scripts': ['vrobbler = vrobbler.cli:main']}

setup_kwargs = {
    'name': 'vrobbler',
    'version': '0.3.0',
    'description': '',
    'long_description': 'None',
    'author': 'Colin Powell',
    'author_email': 'colin@unbl.ink',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
