# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kodexa',
 'kodexa.assistant',
 'kodexa.connectors',
 'kodexa.model',
 'kodexa.pipeline',
 'kodexa.platform',
 'kodexa.selectors',
 'kodexa.steps',
 'kodexa.testing',
 'kodexa.training']

package_data = \
{'': ['*']}

install_requires = \
['addict==2.4.0',
 'appdirs>=1.4.4,<2.0.0',
 'better-exceptions>=0.3.3,<0.4.0',
 'datamodel-code-generator>=0.13.0,<0.14.0',
 'deepdiff==5.8.1',
 'jsonpickle==2.2.0',
 'msgpack==1.0.4',
 'ply>=3.11,<4.0',
 'pydantic-yaml>=0.8.0,<0.9.0',
 'pydantic>=1.10.4,<2.0.0',
 'pyfunctional>=1.4.3,<1.5.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.1,<3.0.0',
 'simpleeval==0.9.12',
 'urllib3>=1.26.14,<2.0.0']

setup_kwargs = {
    'name': 'kodexa',
    'version': '6.0.136a0',
    'description': 'Python SDK for the Kodexa Platform',
    'long_description': '# Kodexa\n\n[![Build and Package with Poetry](https://github.com/kodexa-ai/kodexa/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/kodexa-ai/kodexa/actions/workflows/main.yml)\n\n![img.png](https://docs.kodexa.com/img.png)\n\nKodexa is a platform for building intelligent document processing pipelines. It is a set of tools and services that\nallow you to build a pipeline that can take a document, extract the content, and then process it to extract the\ninformation you need.\n\nIt is built on a set of core principles:\n\n* **Document Centric** - Kodexa is built around the idea of a document. A document is a collection of content\n  nodes that are connected together. This is a powerful model that allows you to build pipelines that can\n  extract content from a wide range of sources.\n\n* **Pipeline Oriented** - Kodexa is built around the idea of a pipeline. A pipeline is a series of steps that\n  can be executed on a document. This allows you to build a pipeline that can extract content from a wide range\n  of sources.\n\n* **Extensible** - Kodexa is built around the idea of a pipeline. A pipeline is a series of steps that can be executed\n  on a document. This allows you to build a pipeline that can extract content from a wide range of sources.\n\n* **Label Driven** - Kodexa focuses on the idea of labels. Labels are a way to identify content within a document\n  and then use that content to drive the processing of the document.\n\n# Python SDK\n\nThis repository contains the Python SDK for Kodexa. The SDK is the primary way to interact with Kodexa. It allows you to\ndefine actions, models, and pipelines that can be executed on Kodexa. It also includes a complete SDK client for\nworking with a Kodexa platform instance.\n\n## Documentation & Examples\n\nDocumentation is available at the [Kodexa Documentation Portal](https://docs.kodexa.com)\n\n## Current Development\n\nThe main branch is 6.0 which is a production release.\n\n## Set-up\n\nWe use poetry to manage our dependencies, so you can install them with:\n\n    poetry install\n\nYou can then run the tests with:\n\n    poetry run pytest\n\n# Contributing\n\nWe welcome contributions to the Kodexa platform. Please see our [contributing guide](CONTRIBUTING.md) for more details.\n\n# License\n\nApache 2.0\n',
    'author': 'Austin Redenbaugh',
    'author_email': 'austin@kodexa.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
