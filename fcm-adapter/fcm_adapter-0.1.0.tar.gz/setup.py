# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fcm_adapter']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0', 'python-jose>=3.3.0,<4.0.0']

setup_kwargs = {
    'name': 'fcm-adapter',
    'version': '0.1.0',
    'description': 'Firebase Cloud Messaging Adapter',
    'long_description': '# FCM Adapter\n\nThis is a simple adapter for the [FCM](https://firebase.google.com/docs/cloud-messaging/) (Firebase Cloud Messaging) service.\n\n## Installation\n```bash\npip install fcm_adapter\n```\n\n```bash\npoetry add fcm_adapter\n```\n\n## Usage\n```python\nfrom fcm_adapter import FCMAdapter\nimport json\n\n\nasync def main(token: str):\n    with open(\'key.json\') as f:\n        key = json.load(f)\n\n    fcm_adapter = FCMAdapter(key)\n\n    await fcm_adapter.send_message(\n        {\n            "token": token,\n            "notification": {"title": "Hello World"},\n        }\n    )\n\n```\n\n\n## FCMAdapter initialization\n### Parameters\n- `key: dict` - Google key. You can get it from the [Firebase Console](https://console.firebase.google.com/). Documentation [here](https://firebase.google.com/docs/admin/setup#initialize-sdk).\n- `client: Union[httpx.AsyncClient, None] = None` - httpx.AsyncClient instance. If not provided, a new instance will be created.\n- `send_message_url: Union[str, None] = None` - FCM send message url. If not provided, the default value will be used.\n- `validate_only: bool = False` - Flag for testing the request without actually delivering the message. Works only with the `send_message` method.\n\n\n## `send`\nSend a message to a device.\nSee [FCM documentation](https://firebase.google.com/docs/reference/fcm/rest/v1/projects.messages/send) for more details.\n\n### Parameters\n- `data: dict` - Data to send to FCM service.\n\n### Returns\n- Response from FCM service. See [FCM documentation](https://firebase.google.com/docs/reference/fcm/rest/v1/projects.messages#Message) for more details.\n\n### Example\n```python\nfrom fcm_adapter import FCMAdapter\n\n\nasync def main(fcm_adapter: FCMAdapter, token: str):\n    response = await fcm_adapter.send_message(\n        {\n            "validate_only": False,\n            "message": {\n                "token": token,\n                "notification": {"title": "Hello World"},\n            },\n        }\n    )\n```\n\n## `send_message`\nSend a message to a device. The function is a wrapper around the `send` method, \nbut it expects to receive only inner message data.\n\nIf `fcm_adapter.validate_only` is set to `True`, \nthe request to FCM will be sent with `"validate_only": true`.\n\n### Parameters\n- `message: dict` - Message data to send to FCM service.\n\n### Returns\n- Response from FCM service. See [FCM documentation](https://firebase.google.com/docs/reference/fcm/rest/v1/projects.messages#Message) for more details.\n\n### Example\n```python\nfrom fcm_adapter import FCMAdapter\n\n\nasync def main(fcm_adapter: FCMAdapter, token: str):\n    response = await fcm_adapter.send_message(\n        {\n            "token": token,\n            "notification": {"title": "Hello World"},\n        }\n    )\n```\n\n# Development\nFirst, install [poetry](https://python-poetry.org/docs/#installation).\n\nThen, install dependencies:\n```bash\npoetry install\n```\n\n## Formatting\n```bash\npoetry run black .\n```\n\n## Testing\n```bash\npoetry run pytest\n```\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
