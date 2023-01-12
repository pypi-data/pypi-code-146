# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['imap_mailbox']
setup_kwargs = {
    'name': 'imap-mailbox',
    'version': '0.1.0',
    'description': 'mailbox over IMAP',
    'long_description': 'None',
    'author': 'Pedro Rodrigues',
    'author_email': 'medecau@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
