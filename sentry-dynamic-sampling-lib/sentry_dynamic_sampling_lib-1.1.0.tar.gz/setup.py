# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sentry_dynamic_sampling_lib']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.9.4,<6.0.0',
 'requests-cache>=0.9.7,<0.10.0',
 'schedule>=1.1.0,<2.0.0',
 'wrapt>=1.14.1,<2.0.0']

setup_kwargs = {
    'name': 'sentry-dynamic-sampling-lib',
    'version': '1.1.0',
    'description': '',
    'long_description': '# Sentry Dynamic Sampling Controller\n\nThis project aims to provide dynamic sampling without relying on Sentry Dynamic Sampling.\n\n\nIt work by installing the library [sentry-dynamic-sampling-lib](https://github.com/SpikeeLabs/sentry-dynamic-sampling-lib) on each project that use sentry. This lib hooks into the sentry callback to change the sampling rate. to get the rate the lib calls this service.\n\n\n\n\n## Install\n```bash\n# install deps\npoetry install\n\n# pre-commit\npoetry run pre-commit install --install-hook\npoetry run pre-commit install --install-hooks --hook-type commit-msg\n```\n\n\n## Run\n```bash\npoetry shell\n\n# add user\npython manage.py createsuperuser\n\n# run server\n# admin @ http://localhost:8000/admin/\npython manage.py runserver\n\n```\n',
    'author': 'jeanloup.monnier',
    'author_email': 'jean-loup.monnier@spikeelabs.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
