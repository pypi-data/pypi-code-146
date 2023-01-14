# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mockcache']
setup_kwargs = {
    'name': 'mockcache3',
    'version': '2.0',
    'description': 'The Python dictionary-based mock memcached client library.',
    'long_description': 'The Python dictionary-based mock memcached client library. It does not\nconnect to any memcached server, but keeps a dictionary and stores every cache\ninto there internally. It is a just emulated API of memcached client only for\ntests. It implements expiration also. NOT THREAD-SAFE.\nThis module and other memcached client libraries have the same behavior.\n\nIt is a fork from [mockcache](https://github.com/lunant/mockcache) to support\nnew Python versions and fix a few bugs.\n',
    'author': 'Hong Minhee',
    'author_email': 'None',
    'maintainer': 'Iuri de Silvio',
    'maintainer_email': 'iurisilvio@gmail.com',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
