# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kpops',
 'kpops.cli',
 'kpops.component_handlers',
 'kpops.component_handlers.helm_wrapper',
 'kpops.component_handlers.kafka_connect',
 'kpops.component_handlers.schema_handler',
 'kpops.component_handlers.topic',
 'kpops.component_handlers.utils',
 'kpops.components',
 'kpops.components.base_components',
 'kpops.components.base_components.models',
 'kpops.components.streams_bootstrap',
 'kpops.components.streams_bootstrap.producer',
 'kpops.components.streams_bootstrap.streams',
 'kpops.pipeline_generator',
 'kpops.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'cachetools>=5.2.0,<6.0.0',
 'dictdiffer>=0.9.0,<0.10.0',
 'pydantic[dotenv]>=1.9.1,<2.0.0',
 'pyhumps>=3.7.3,<4.0.0',
 'python-schema-registry-client>=2.4.1,<3.0.0',
 'requests>=2.28.0,<3.0.0',
 'rich>=12.4.4,<13.0.0',
 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['kpops = kpops.cli.main:app']}

setup_kwargs = {
    'name': 'kpops',
    'version': '0.6.1',
    'description': 'KPOps is a tool to deploy Kafka pipelines to Kubernetes',
    'long_description': '# KPOps\n\n[![Latest release](https://img.shields.io/github/v/release/bakdata/kpops)](https://github.com/bakdata/kpops/releases/latest)\n[![Build status](https://github.com/bakdata/kpops/actions/workflows/ci.yaml/badge.svg)](https://github.com/bakdata/kpops/actions/workflows/ci.yaml)\n\nFor detailed usage and installation instructions, check out\nthe [documentation](https://bakdata.github.io/kpops/latest).\n\n## Features\n\n- **Deploy Kafka apps to Kubernetes**: KPOps allows to deploy consecutive Kafka Streams applications, producers, and Kafka connectors using an easy-to-read and write pipeline definition. \n- **Configure multiple pipelines and steps**: KPOps comes with various abstractions that simplify configuring multiple pipelines and steps within pipelines by sharing configuration between different applications, like producers or streaming applications.\n- **Customize your components**: KPOps comes with multiple base components (Kafka connect, producer, etc.) and allows you to introduce custom components.\n- **Handle your topics and schemas**: KPOps not only creates and deletes your topics but also registers and deletes your schemas.\n- **Manage the lifecycle of your components**: KPOps can deploy, destroy, reset, and clean your defined components from the Kubernetes cluster.\n\n## Install KPOps\n\nKPOps comes as a [PyPI package](https://pypi.org/project/kpops/). \nYou can install it with [pip](https://github.com/pypa/pip):\n\n```shell\npip install kpops\n```\n\n## Documentation\n\n- [What is KPOps?](https://bakdata.github.io/kpops/latest/user)\n- [Getting started with KPOps](https://bakdata.github.io/kpops/latest/user/getting-started/)\n- [Examples](https://bakdata.github.io/kpops/latest/user/examples)\n\n## Contributing\n\nWe are happy if you want to contribute to this project.\nIf you find any bugs or have suggestions for improvements, please open an issue.\nWe are also happy to accept your PRs.\nJust open an issue beforehand and let us know what you want to do and why.\n\n## License\n\nKPOps is licensed under the [MIT License](https://github.com/bakdata/kpops/blob/main/LICENSE).\n',
    'author': 'bakdata',
    'author_email': 'opensource@bakdata.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bakdata/kpops',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
