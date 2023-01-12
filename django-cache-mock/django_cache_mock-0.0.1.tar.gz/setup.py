# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_cache_mock', 'django_cache_mock.backends']

package_data = \
{'': ['*']}

install_requires = \
['django>=3,<5']

setup_kwargs = {
    'name': 'django-cache-mock',
    'version': '0.0.1',
    'description': '',
    'long_description': '# django-cache-mock\n\nUse in-process mocks to avoid setting up external caches for Django during\ndevelopment.\n\nDjango has a limited built-in `django.core.cache.backends.locmem.LocMemCache`,\nto help development, but Django do some magic to always give you a working\nconnection.\n\nI have some reasons to abuse Django cache this way:\n\n* Thread safety: Django spin one connection per thread to avoid issues with\nthread unsafe drivers.\n* Good defaults: Django run connections with good defaults.\n* Connection reuse: Django already have a pool running and in most cases it is\nbetter to use it.\n\n## Install\n\n```shell\n$ pip install django-cache-mock\n```\n\nAlso, it is possible to install with the backends you want.\n\nFor `mockcache`, it installs a fork of the original package because it doesn´t\nwork for new versions of Python.\n\n```shell\n$ pip install django-cache-mock[mockcache]\n$ pip install django-cache-mock[fakeredis]\n$ pip install django-cache-mock[redislite]\n```\n\n## How to use\n\nIn your Django settings you already have `CACHES` defined.\n\nFor `memcached`, it\'s something like that:\n\n```python\nCACHES = {\n    "default": {\n        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",\n        "LOCATION": os.getenv("MEMCACHED_HOSTS"),\n        "OPTIONS": {\n            "no_delay": True,\n            "ignore_exc": True,\n            "max_pool_size": 4,\n            "use_pooling": True,\n        },\n    },\n}\n```\n\nJust make a call to `django_cache_mock.patch` to replace with a mock backend.\n\n**The lib will patch only when cache LOCATION is not defined.**\n\n```python\nimport django_cache_mock\n\nif DEBUG:  # Apply it only in debug mode to be extra careful.\n    django_cache_mock.patch(CACHES, "default", "mockcache")\n```\n\nThis patch replace cache with a mocked one. For mockcache,\n\n## Custom cache options\n\nThe `patch` function accepts custom params. It can be used to override mock\nbehaviours, like the db file `redislite` will use, defined by `LOCATION`:\n\n```python\ndjango_cache_mock.patch(CACHES, "default", "redislite", {"LOCATION": "data/redis.db"})\n```\n\n## How to access connections\n\nTo get Django memcached and redis clients from cache:\n\n```python\nfrom django.core.cache import caches\n\ndef give_me_memcached():\n    return caches["memcached"]._cache\n\n# for django.core.cache.backends.redis\ndef give_me_primary_redis():\n    return caches["redis"]._cache.get_client()\n\ndef give_me_secondary_redis():\n    return caches["redis"]._cache.get_client(write=False)\n\n# for django-redis\ndef give_me_primary_redis():\n    return caches["redis"].client.get_client()\n\ndef give_me_secondary_redis():\n    return caches["redis"].client.get_client(write=False)\n```\n',
    'author': 'Iuri de Silvio',
    'author_email': 'iurisilvio@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
