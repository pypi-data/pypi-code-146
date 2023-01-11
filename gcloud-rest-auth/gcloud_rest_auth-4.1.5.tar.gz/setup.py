# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gcloud', 'gcloud.rest', 'gcloud.rest.auth']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=1.0.0,<3.0.0',
 'cryptography>=2.0.0,<39.0.0',
 'future>=0.17.0,<0.19.0',
 'pyjwt>=1.5.3,<3.0.0',
 'requests>=2.2.1,<3.0.0',
 'six>=1.11.0,<2.0.0']

extras_require = \
{':python_version < "3.0"': ['chardet>=2.0,<4.0'],
 ':python_version >= "3.7"': ['chardet>=2.0,<4.1']}

setup_kwargs = {
    'name': 'gcloud-rest-auth',
    'version': '4.1.5',
    'description': 'Python Client for Google Cloud Auth',
    'long_description': '(Asyncio OR Threadsafe) Python Client for Google Cloud Auth\n===========================================================\n\n    This is a shared codebase for ``gcloud-rest-auth`` and ``gcloud-rest-auth``\n\nThis library implements an ``IamClient`` class, which can be used to interact\nwith GCP public keys and URL sign blobs.\n\nIt additionally implements a ``Token`` class, which is used for authorizing\nagainst Google Cloud. The other ``gcloud-rest-*`` package components accept a\n``Token`` instance as an argument; you can define a single token for all of\nthese components or define one for each. Each component corresponds to a given\nGoogle Cloud service and each service requires various "`scopes`_".\n\n|pypi| |pythons-aio| |pythons-rest|\n\nInstallation\n------------\n\n.. code-block:: console\n\n    $ pip install --upgrade gcloud-{aio,rest}-auth\n\nUsage\n-----\n\nSee `our docs`_.\n\nCLI\n~~~\n\nThis project can also be used to help you manually authenticate to test GCP\nroutes, eg. we can list our project\'s uptime checks with a tool such as\n``curl``:\n\n.. code-block:: console\n\n    # using default application credentials\n    curl \\\n      -H "Authorization: Bearer $(python3 -c \'from gcloud.rest.auth import Token; print(Token().get())\')" \\\n      "https://monitoring.googleapis.com/v3/projects/PROJECT_ID/uptimeCheckConfigs"\n\n    # using a service account (make sure to provide a scope!)\n    export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service.json\n    curl \\\n      -H "Authorization: Bearer $(python3 -c \'from gcloud.rest.auth import Token; print(Token(scopes=["\'"https://www.googleapis.com/auth/cloud-platform"\'"]).get())\')" \\\n      "https://monitoring.googleapis.com/v3/projects/PROJECT_ID/uptimeCheckConfigs"\n\n    # using legacy account credentials\n    export GOOGLE_APPLICATION_CREDENTIALS=~/.config/gcloud/legacy_credentials/EMAIL@DOMAIN.TLD/adc.json\n    curl \\\n      -H "Authorization: Bearer $(python3 -c \'from gcloud.rest.auth import Token; print(Token().get())\')" \\\n      "https://monitoring.googleapis.com/v3/projects/PROJECT_ID/uptimeCheckConfigs"\n\nContributing\n------------\n\nPlease see our `contributing guide`_.\n\n.. _contributing guide: https://github.com/talkiq/gcloud-rest/blob/master/.github/CONTRIBUTING.rst\n.. _our docs: https://talkiq.github.io/gcloud-rest\n.. _scopes: https://developers.google.com/identity/protocols/googlescopes\n\n.. |pypi| image:: https://img.shields.io/pypi/v/gcloud-rest-auth.svg?style=flat-square\n    :alt: Latest PyPI Version (gcloud-rest-auth)\n    :target: https://pypi.org/project/gcloud-rest-auth/\n\n.. |pythons-aio| image:: https://img.shields.io/pypi/pyversions/gcloud-rest-auth.svg?style=flat-square&label=python (aio)\n    :alt: Python Version Support (gcloud-rest-auth)\n    :target: https://pypi.org/project/gcloud-rest-auth/\n\n.. |pythons-rest| image:: https://img.shields.io/pypi/pyversions/gcloud-rest-auth.svg?style=flat-square&label=python (rest)\n    :alt: Python Version Support (gcloud-rest-auth)\n    :target: https://pypi.org/project/gcloud-rest-auth/\n',
    'author': 'Vi Engineering',
    'author_email': 'voiceai-eng@dialpad.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/talkiq/gcloud-aio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
