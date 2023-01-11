# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jinjax']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=3.0', 'markupsafe>=2.0', 'whitenoise>=5.3']

setup_kwargs = {
    'name': 'jinjax',
    'version': '0.18',
    'description': 'Replace your HTML templates with Python server-Side components',
    'long_description': '<h1>\n  <img src="https://github.com/jpsca/jinjax/raw/main/logo.png"width="48" height="48" align="top">\n  JinjaX\n</h1>\n\nFrom chaos to clarity: The power of components in your server-side-rendered Python web app.\n\n**Documentation:** https://jinjax.scaletti.dev/\n\nWrite server-side components as single Jinja template files.\nUse them as HTML tags without doing any importing.\n\n## About\n\n- This project is developed by *Juan-Pablo Scaletti*.<br>\n- I love building products and sharing knowledge.\n\n',
    'author': 'Juan-Pablo Scaletti',
    'author_email': 'juanpablo@jpscaletti.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://jinjax.scaletti.dev/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
