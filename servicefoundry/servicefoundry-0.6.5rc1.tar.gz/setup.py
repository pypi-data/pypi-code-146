# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['servicefoundry',
 'servicefoundry.auto_gen',
 'servicefoundry.builder',
 'servicefoundry.builder.builders',
 'servicefoundry.builder.builders.tfy_python_buildpack',
 'servicefoundry.cli',
 'servicefoundry.cli.commands',
 'servicefoundry.cli.io',
 'servicefoundry.core',
 'servicefoundry.core.notebook',
 'servicefoundry.core.notebook.io',
 'servicefoundry.function_service',
 'servicefoundry.function_service.deployment_examples.class_deployment',
 'servicefoundry.function_service.deployment_examples.function_deployment',
 'servicefoundry.function_service.deployment_examples.model_composition',
 'servicefoundry.function_service.deployment_examples.one_service_calling_another',
 'servicefoundry.function_service.remote',
 'servicefoundry.internal',
 'servicefoundry.io',
 'servicefoundry.lib',
 'servicefoundry.lib.auth',
 'servicefoundry.lib.clients',
 'servicefoundry.lib.config',
 'servicefoundry.lib.dao',
 'servicefoundry.lib.infra',
 'servicefoundry.lib.model',
 'servicefoundry.requirements',
 'servicefoundry.requirements.interceptor',
 'servicefoundry.v2',
 'servicefoundry.v2.examples.job_deployment',
 'servicefoundry.v2.examples.model_deployment.hf',
 'servicefoundry.v2.examples.model_deployment.mlfoundry',
 'servicefoundry.v2.examples.service_deployment',
 'servicefoundry.v2.lib']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'Mako>=1.1.6,<2.0.0',
 'PyJWT>=2.3.0,<3.0.0',
 'PyYAML>=6.0,<7.0',
 'chevron>=0.14.0,<0.15.0',
 'click>=8.0.4,<9.0.0',
 'cookiecutter>=2.1.1,<3.0.0',
 'docker>=6.0.1,<7.0.0',
 'fastapi>=0.78.0,<0.79.0',
 'filelock>=3.8.0,<4.0.0',
 'gitignorefile>=1.1.2,<2.0.0',
 'importlib-metadata>=4.2,<5.0',
 'importlib-resources>=5.2.0,<6.0.0',
 'packaging>=21.3,<22.0',
 'pydantic>=1.9.1,<2.0.0',
 'pygments>=2.12.0,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'python-socketio[client]>=5.5.2,<6.0.0',
 'questionary>=1.10.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich-click>=1.2.1,<2.0.0',
 'rich>=12.0.0,<13.0.0',
 'typing-extensions>=4.3.0,<5.0.0',
 'uvicorn>=0.18.2,<0.19.0']

extras_require = \
{'notebook': ['ipywidgets>=7.6.0,<8.0.0', 'ipython>=7.10.0,<8.0.0']}

entry_points = \
{'console_scripts': ['servicefoundry = servicefoundry.cli.__main__:main',
                     'sfy = servicefoundry.cli.__main__:main']}

setup_kwargs = {
    'name': 'servicefoundry',
    'version': '0.6.5rc1',
    'description': 'Generate deployed services from code',
    'long_description': "# ServiceFoundry\n\nServiceFoundry is a client library that allows you to containerize and deploy your Machine Learning model (or other\nservices) to a managed Kubernetes Cluster. This also generates a Grafana cluster with complete visibility of your\nService Health, System Logs, and Kubernetes Workspace.\n\nIt is available both as a command-line-interface and via APIs that allow you to deploy directly from your Jupyter\nNotebook.\n\nYou can access the health of your service, monitoring links and deployed endpoints by logging on to TrueFoundry's\ndashboard.\n\n# Installation\n\n```\npip install -U servicefoundry\n```\n\n# Documentation\n\nhttps://docs.truefoundry.com/servicefoundry/\n",
    'author': 'Abhishek Choudhary',
    'author_email': 'abhichoudhary06@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/innoavator/servicefoundry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
