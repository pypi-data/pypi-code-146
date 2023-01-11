# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kalyke', 'kalyke.clients', 'kalyke.internal', 'kalyke.models']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.6.0,<3.0.0',
 'cryptography>=39.0.0,<40.0.0',
 'httpx[http2]>=0.23.1,<0.24.0']

setup_kwargs = {
    'name': 'kalyke-apns',
    'version': '0.2.1',
    'description': 'A library for interacting with APNs and VoIP using HTTP/2.',
    'long_description': '# kalyke\n\n![Test](https://github.com/nnsnodnb/kalyke/workflows/Test/badge.svg)\n[![Maintainability](https://api.codeclimate.com/v1/badges/fb85bcf746e1f4025afa/maintainability)](https://codeclimate.com/github/nnsnodnb/kalyke/maintainability)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Coverage Status](https://coveralls.io/repos/github/nnsnodnb/kalyke/badge.svg?branch=main)](https://coveralls.io/github/nnsnodnb/kalyke?branch=main)\n\n[![PyPI Package version](https://badge.fury.io/py/kalyke-apns.svg)](https://pypi.org/project/kalyke-apns)\n[![Python Supported versions](https://img.shields.io/pypi/pyversions/kalyke-apns.svg)](https://pypi.org/project/kalyke-apns)\n[![wheel](https://img.shields.io/pypi/wheel/kalyke-apns.svg)](https://pypi.org/project/kalyke-apns)\n[![format](https://img.shields.io/pypi/format/kalyke-apns.svg)](https://pypi.org/project/kalyke-apns)\n[![implementation](https://img.shields.io/pypi/implementation/kalyke-apns.svg)](https://pypi.org/project/kalyke-apns)\n[![LICENSE](https://img.shields.io/pypi/l/kalyke-apns.svg)](https://pypi.org/project/kalyke-apns)\n\nA library for interacting with APNs and VoIP using HTTP/2.\n\n## Installation\n\nkalyke requires python 3.7 or later.\n\n```bash\n$ pip install kalyke-apns\n```\n\n## Usage\n\n### APNs\n\n```python\nimport asyncio\n\nfrom kalyke import ApnsClient, ApnsConfig, Payload, PayloadAlert\n\nclient = ApnsClient(\n    use_sandbox=True,\n    team_id="YOUR_TEAM_ID",\n    auth_key_id="AUTH_KEY_ID",\n    auth_key_filepath="/path/to/AuthKey_AUTH_KEY_ID.p8",\n)\n\nregistration_id = "a8a799ba6c21e0795b07b577b562b8537418570c0fb8f7a64dca5a86a5a3b500"\n\npayload_alert = PayloadAlert(title="YOUR TITLE", body="YOUR BODY")\npayload = Payload(alert=payload_alert, badge=1, sound="default")\nconfig = ApnsConfig(topic="com.example.App")\n\nasyncio.run(client.send_message(device_token=registration_id, payload=payload, apns_config=config))\n```\n\n### VoIP\n\n```python\nimport asyncio\nfrom pathlib import Path\n\nfrom kalyke import ApnsConfig, ApnsPushType, VoIPClient\n\nclient = VoIPClient(\n    use_sandbox=True,\n    auth_key_filepath=Path("/") / "path" / "to" / "YOUR_VOIP_CERTIFICATE.pem",\n)\n\nregistration_id = "a8a799ba6c21e0795b07b577b562b8537418570c0fb8f7a64dca5a86a5a3b500"\n\npayload = {"key": "value"}\nconfig = ApnsConfig(topic="com.example.App.voip", push_type=ApnsPushType.VOIP)\n\nasyncio.run(client.send_message(device_token=registration_id, payload=payload, apns_config=config))\n```\n\n## License\n\nThis software is licensed under the MIT License (See [LICENSE](LICENSE)).\n',
    'author': 'Yuya Oka',
    'author_email': 'nnsnodnb@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nnsnodnb/kalyke',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
