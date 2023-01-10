# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['robotoff',
 'robotoff.app',
 'robotoff.cli',
 'robotoff.elasticsearch',
 'robotoff.elasticsearch.product',
 'robotoff.insights',
 'robotoff.prediction',
 'robotoff.prediction.category',
 'robotoff.prediction.category.neural',
 'robotoff.prediction.object_detection',
 'robotoff.prediction.object_detection.utils',
 'robotoff.prediction.ocr',
 'robotoff.scheduler',
 'robotoff.spellcheck',
 'robotoff.spellcheck.elasticsearch',
 'robotoff.spellcheck.patterns',
 'robotoff.spellcheck.percentages',
 'robotoff.spellcheck.vocabulary',
 'robotoff.utils',
 'robotoff.workers',
 'robotoff.workers.tasks']

package_data = \
{'': ['*']}

install_requires = \
['APScheduler>=3.8.1,<3.9.0',
 'Pillow>=9.3.0,<9.4.0',
 'Pint==0.9',
 'cachetools>=5.2.0,<6.0.0',
 'dacite>=1.6.0,<1.7.0',
 'elasticsearch>=8.5.3,<8.6.0',
 'falcon-cors>=1.1.7,<1.2.0',
 'falcon-multipart>=0.2.0,<0.3.0',
 'falcon>=2.0.0,<2.1.0',
 'flashtext>=2.7,<2.8',
 'gunicorn>=20.1.0,<20.2.0',
 'influxdb-client>=1.34.0,<1.35.0',
 'jsonschema>=4.4.0,<4.5.0',
 'langid>=1.1.6,<1.2.0',
 'matplotlib>=3.5.0,<3.6.0',
 'more-itertools>=8.9.0,<8.10.0',
 'numpy>=1.23.5,<1.24.0',
 'orjson>=3.8.2,<3.9.0',
 'peewee>=3.14.4,<3.15.0',
 'protobuf>=3.17.3,<3.18.0',
 'psycopg2-binary>=2.9.1,<2.10.0',
 'py-healthcheck>=1.10.1,<2.0.0',
 'pymongo>=3.12.0,<3.13.0',
 'python-redis-lock>=4.0.0,<4.1.0',
 'requests>=2.28.1,<2.29.0',
 'rq>=1.11.1,<1.12.0',
 'sentry-sdk[falcon]>=1.11.0,<1.12.0',
 'spacy-lookups-data>=1.0.3,<2.0.0',
 'spacy>=3.4.1,<3.5.0',
 'transformers>=4.25.1,<4.26.0',
 'tritonclient[grpc]>=2.26.0,<3.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['robotoff-cli = robotoff.cli.main:main']}

setup_kwargs = {
    'name': 'robotoff',
    'version': '1.18.2',
    'description': 'Real-time and batch prediction service for Open Food Facts.',
    'long_description': None,
    'author': 'Open Food Facts Team',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
