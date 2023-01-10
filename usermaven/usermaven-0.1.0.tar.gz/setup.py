# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['usermaven', 'usermaven.test']

package_data = \
{'': ['*'], 'usermaven': ['assets/images/logos/*']}

install_requires = \
['backoff>=1.10.0,<2.0.0',
 'monotonic>=1.5',
 'python-dateutil>2.1',
 'requests>=2.7,<3.0',
 'six>=1.5']

setup_kwargs = {
    'name': 'usermaven',
    'version': '0.1.0',
    'description': '',
    'long_description': '<p align="center">\n  <a href="https://usermaven.com/">\n    <img src="usermaven/assets/images/logos/usermaven-logo.png" height="60">\n  </a>\n  <p align="center">PRIVACY-FRIENDLY ANALYTICS TOOL</p>\n</p>\n\n\n# Usermaven-python \n\nThis module is compatible with Python 3.6 and above.\n\n## Installing\n\n```bash\npip3 install usermaven-python\n```\n\n## Usage\n\n```python\nfrom usermaven import Client\nclient = Client(api_key=\'api_key\', server_token="server_token")\nclient.identify({\'email\': \'john@gmail.com\',\'id\': \'123\', \'created_at\': \'2022\'})\nclient.track(\'user_id\', \'signed_up\')\n```\n\n### Instantiating usermaven-python\'s client object\n\nCreate an instance of the client with your Usermaven workspace credentials.\n\n```python\nfrom usermaven import Client\nclient = Client(api_key="api_key", server_token="server_token")\n```\n\n### Create a Usermaven user profile\n\n```python\nclient.identify({\'email\': \'john@gmail.com\',\'id\': \'123\', \'created_at\': \'2022\'})\n```\n\n#### Required arguments\n`user`: The user object is the only required argument for `identify` call. `email`, `id` and `created_at` are required\nfields for the user object. Recommended fields for the user object are `first_name` and `last_name`. Additionally you \ncan pass any custom properties in the form of dictionary to your user object.\n\n#### Optional arguments\nYou can also pass optional arguments to the `identify` method.\n\n`company`: A company object for which the user belongs to. It is optional but if it is passed, it must contain `name`,\n`id` and `created_at` fields. You can also submit custom properties in the form of dictionary for the company object. \nExample:\n```python\nclient.identify({\'email\': \'john@gmail.com\',\'id\': \'123\', \'created_at\': \'2022\'}, \n                company={\'name\': \'usermaven\', \'id\': \'5\', \'created_at\': \'2022\',\n                         \'custom\': {\'plan\': \'enterprise\', \'industry\': \'Technology\'}})\n```\n\n### Track a custom event\n\n```python\nclient.track(\'user_id\', \'plan_purchased\')\n```\n\n#### Required arguments\n`user_id`: For the `track` call, you must pass the `user_id` of the user you want to track the event for.\n\n`event_type`: For track call, `event_type` is a required argument and you must pass a value to the event_type.\nWe recommend using [verb] [noun], like `goal created` or `payment succeeded` to easily identify what your events mean\nlater on.\n\n#### Optional arguments\nYou can also pass optional arguments to the `track` method.\n\n`company`: A company object for which the user belongs to. It is optional but if it is passed, it must contain `name`,\n`id` and `created_at` fields. You can also submit custom properties in the form of dictionary for the company object. \nExample:\n```python\nclient.track(\'user_id\', \'signed_up\', company={\'name\': \'usermaven\', \'id\': \'5\', \'created_at\': \'2022\',\n                                              \'custom\': {\'plan\': \'enterprise\', \'industry\': \'Technology\'}})\n```\n\n`event_attributes`: This can contain information related to the event that is being tracked. Example:\n```python\nclient.track(\'user_id\', \'video_watched\', event_attributes={\'video_title\': \'demo\', \'watched_at\': \'2022\'})\n```\n\n## Local Setup for Development\nFor local development, you can clone the repository and install the dependencies using the following commands:\n\n```bash\ngit clone "https://github.com/usermaven/usermaven-python.git"\npoetry install\n```\n\n## Running tests\n\nChanges to the library can be tested by running `python -m unittest -v` from the parent directory.\n',
    'author': 'usermaven',
    'author_email': 'azhar@usermaven.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
