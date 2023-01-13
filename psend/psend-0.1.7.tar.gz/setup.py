# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['psend']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0']

extras_require = \
{':python_version >= "2.7" and python_version < "3.0"': ['requests>=2.27.1,<3.0.0'],
 ':python_version >= "3.8" and python_version < "4.0"': ['requests>=2.28.1,<3.0.0']}

entry_points = \
{'console_scripts': ['psend = psend.functions:send_push_notification']}

setup_kwargs = {
    'name': 'psend',
    'version': '0.1.7',
    'description': 'Utility to send push notification.',
    'long_description': '# psend\nSimple python utility for send push notifications.\n\n## Description\nA python client to send push notifications to phones and other device.\n\nThe notifications will recived by the "[Simple Push Notification API](https://play.google.com/store/apps/details?id=net.xdroid.pn)" App.\n\n## How to install\n\nYou can install it using **pip**\n\n```bash\npip install psend\n```\n## How to use\n\nAfter installing this, it can be used by calling the script:\n\n```bash\npsend\n```\n\nor using python:\n\n```bash\npython -m psend\n```\n## Options\nThe options for this utility can shown using `-h` flag:\n\n```\nusage: psend [-h] -k KEY [KEY ...] -t TITLE -c CONTENT [-u URL]\n\nUtility to send push notification\n\noptions:\n  -h, --help            show this help message and exit\n  -k KEY [KEY ...], --key KEY [KEY ...]\n  -t TITLE, --title TITLE\n  -c CONTENT, --content CONTENT\n  -u URL, --url URL\n\nSend push notification to Simple Push Notification API\n(https://play.google.com/store/apps/details?id=net.xdroid.pn)\n```\n\n## References\n\n* Git repository: https://github.com/sandrospadaro/psend\n* Pypi repository: https://pypi.org/project/psend/',
    'author': 'Sandro Spadaro',
    'author_email': 'sandro.spadaro@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sandrospadaro/psend',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=2.7,<4.0',
}


setup(**setup_kwargs)
