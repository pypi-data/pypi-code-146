# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pretty_jwt']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pjwt = pretty_jwt:entrypoint']}

setup_kwargs = {
    'name': 'pretty-jwt',
    'version': '0.1.0',
    'description': 'Simple utility for viewing JWT tokens in console',
    'long_description': '# Pretty JWT\n\nSimple utility for viewing JWT tokens in console.\n\n## Install\n\n```shell\npip install pretty_jwt\n```\n\n## Use\n\n```shell\npjwt eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiSm9obiBEb2UifQ.DjwRE2jZhren2Wt37t5hlVru6Myq4AhpGLiiefF69u8\n\nHeader:\n{\n    "alg": "HS256",\n    "typ": "JWT"\n}\nPayload:\n{\n    "name": "John Doe"\n}\nSignature:\nDjwRE2jZhren2Wt37t5hlVru6Myq4AhpGLiiefF69u8\n```',
    'author': 'Elisei',
    'author_email': 'elisey.rav@gmail.comp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/elisey/pretty_jwt',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
