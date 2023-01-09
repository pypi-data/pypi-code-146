# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['miqro_rutos_sms']

package_data = \
{'': ['*']}

install_requires = \
['miqro>=1.2.0,<2.0.0', 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['miqro_rutos_sms = miqro_rutos_sms:service.run']}

setup_kwargs = {
    'name': 'miqro-rutos-sms',
    'version': '0.1.1',
    'description': '',
    'long_description': '# MIQRO MQTT SMS Service for Teltonika RUT Devices\n\nMQTT service based on the miqro library.\n\nTested on a Teltonika RUTX11.\n\nThis service uses the Teltonika RUT SMS API to send SMS messages.\n\n## Prerequisites\n\nYou need to enable the SMS API on the Teltonika RUT device and configure a username and password, as seen in the following screenshot:\n\n![Teltonika RUT SMS API](docs/screenshot.png)\n\n## Installing\n\nTo install the software, follow these steps **as root**:\n\n * If `pip3` is not installed, run `apt install python3-pip` first.\n * Then run `pip3 install miqro_rutos_sms` \n * Create the configuration file `/etc/miqro.yml`\n   * See [examples/miqro.example.yml](examples/miqro.example.yml) for an example\n   * See below for a list of configuration options\n   * See [the MIQRO documentation](https://github.com/danielfett/miqro#configuration-file) for other options you can use in the configuration file\n * Install the system service: \n   * `miqro_rutos_sms  --install`\n   * `systemctl enable miqro_rutos_sms`\n   * `systemctl start miqro_rutos_sms`\n\n## Configuration Options\n\nIn `/etc/miqro.yml`, you can use these settings to configure the service:\n\n * `host`: The IP address or host name of the Teltonika RUT device (default `192.168.1.1`).\n * `port`: The port number of the Teltonika RUT device (default `80`).\n * `username`: The username to use for authentication.\n * `password`: The password to use for authentication.\n * `delete_after`: If present, delete message after this time. Time is given like a Python timedelta, e.g., "days: 1" or "seconds: 300". If not present, messages are not deleted.\n\n## MQTT Topics\n\nThe service subscribes to the following topics:\n\n * `service/rutos_sms/send/single/<number>`: Send a single SMS message to the given number. The number must be provided with leading zeros, e.g., `00491700000000`. The message is given as the payload of the MQTT message. The result is published to the topic `service/rutos_sms/sent/single/<number>`.\n * `service/rutos_sms/send/group/<groupname>`: Send a single SMS message to the given group. The message is given as the payload of the MQTT message. The group must be configured in the Teltonika RUT device. The result is published to the topic `service/rutos_sms/sent/group/<groupname>`.\n * `service/rutos_sms/delete`: Delete a single SMS message. The message index is given as the payload of the MQTT message.\n\nThe service queries the router every 20 seconds for new messages. The messages are published to the topic `service/rutos_sms/received` in MQTT format like this:\n\n    {"index": "0", "date": "Mon Jan  9 20:01:28 2023", "sender": "+491700000000", "text": "This is an example.", "status": "read"}\n\nUnless the messages are deleted using the `delete_after` configuration, they will be published again on the next restart of the service.\n',
    'author': 'Daniel Fett',
    'author_email': 'fett@danielfett.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
