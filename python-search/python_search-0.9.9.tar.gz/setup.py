# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_search',
 'python_search.apps',
 'python_search.configuration',
 'python_search.data_ui',
 'python_search.entry_capture',
 'python_search.entry_description_generator',
 'python_search.entry_type',
 'python_search.events',
 'python_search.events.ranking_generated',
 'python_search.events.run_performed',
 'python_search.infrastructure',
 'python_search.init',
 'python_search.interpreter',
 'python_search.next_item_predictor',
 'python_search.next_item_predictor.features',
 'python_search.next_item_predictor.features.entry_embeddings',
 'python_search.next_item_predictor.inference',
 'python_search.plugins',
 'python_search.sdk',
 'python_search.search',
 'python_search.search_ui',
 'python_search.shortcut']

package_data = \
{'': ['*']}

install_requires = \
['PySimpleGUI>=4.60.1,<5.0.0',
 'PyYAML>=6.0,<7.0',
 'certifi>=2022.6.15,<2023.0.0',
 'colorama>=0.4.5,<0.5.0',
 'dill>=0.3.5.1,<0.4.0.0',
 'fire>=0.4.0,<0.5.0',
 'pydantic>=1.9.1,<2.0.0',
 'pyroscope-io>=0.8.0,<0.9.0']

extras_require = \
{':extra == "server"': ['mlflow>=1.29.0,<1.30.0'],
 'server': ['fastapi>=0.79.0,<0.80.0',
            'kafka-python>=2.0.2,<3.0.0',
            'scipy>=1.8.1',
            'xgboost>=1.6.1,<2.0.0',
            'matplotlib>=3.5.2,<4.0.0',
            'pandas>=1.4.3,<2.0.0',
            'redis>=4.3.4,<5.0.0',
            'uvicorn>=0.18.2,<0.19.0',
            'numpy>=1.23.4',
            'msgpack-numpy>=0.4.8',
            'pyspark>=3.0',
            'keras>=2.10',
            'arize>=5.2.0,<6.0.0',
            'jupyterlab>=3.5.0,<4.0.0'],
 'server:sys_platform == "linux"': ['tensorflow>=2.10.0']}

entry_points = \
{'console_scripts': ['aps_webapi = python_search.sdk.web_api_sdk:main',
                     'browser = python_search.apps.browser:main',
                     'clipboard = python_search.apps.clipboard:main',
                     'collect_input = python_search.apps.collect_input:main',
                     'feature_toggle = '
                     'python_search.feature_toggle:FeatureToggle.main',
                     'generic_data_collector = '
                     'python_search.data_collector:GenericDataCollector.initialize',
                     'next_item = '
                     'python_search.next_item_predictor.next_item_pipeline:main',
                     'next_item_pipeline = '
                     'python_search.next_item_predictor.next_item_pipeline:main',
                     'notify_send = python_search.apps.notification_ui:main',
                     'ps_container = python_search.container:start',
                     'ps_webapi = python_search.sdk.web_api_sdk:main',
                     'python_search = python_search.cli:main',
                     'python_search_infra = '
                     'python_search.infrastructure.infrastructure:main',
                     'python_search_webapi = python_search.web_api:main',
                     'reminders = python_search.plugins.reminders:main',
                     'run_entry = python_search.cli:_run_key_bin',
                     'run_key = python_search.cli:_run_key_bin']}

scripts = \
['wrap_log_command.sh']

setup_kwargs = {
    'name': 'python-search',
    'version': '0.9.9',
    'description': 'Build your knowledge database in python and retrieve it efficiently',
    'long_description': 'None',
    'author': 'Jean Carlo Machado',
    'author_email': 'machado.c.jean@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'scripts': scripts,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
