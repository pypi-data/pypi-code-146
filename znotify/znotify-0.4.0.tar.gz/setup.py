# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['znotify']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'znotify',
    'version': '0.4.0',
    'description': 'sdk for notify',
    'long_description': '# notify-py-sdk\n\nSend notifications to [Notify](https://github.com/znotify/Notify)\n\n## Installation\n\n```bash\npip install znotify\n```\n\n## Usage\n\n```python\nfrom znotify import Client\n\nclient = Client.create("user_id")\nclient.send("Hello World")\n```\n\n## Development\n\n### Run tests\n\n```bash\npython -m unittest discover\n```\n\n',
    'author': 'Zxilly',
    'author_email': 'zhouxinyu1001@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ZNotify/py-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
