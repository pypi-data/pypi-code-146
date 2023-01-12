# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['url_filter',
 'url_filter.backends',
 'url_filter.filtersets',
 'url_filter.integrations']

package_data = \
{'': ['*']}

install_requires = \
['cached-property>=1.5.2,<2.0.0', 'django>=3.2.4']

setup_kwargs = {
    'name': 'dj-url-filter',
    'version': '0.4.4',
    'description': 'Django URL Filter provides a safe way to filter data via human-friendly URLs.',
    'long_description': '=================\nDjango URL Filter\n=================\n\n.. image:: https://badge.fury.io/py/dj-url-filter.svg\n   :target: http://badge.fury.io/py/dj-url-filter\n.. image:: https://readthedocs.org/projects/django-url-filter/badge/?version=latest\n   :target: http://django-url-filter.readthedocs.io/en/latest/?badge=latest\n.. image:: https://codecov.io/gh/enjoy2000/django-url-filter/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/enjoy2000/django-url-filter\n\nDjango URL Filter provides a safe way to filter data via human-friendly URLs.\n\n* Free software: MIT license\n* GitHub: https://github.com/enjoy2000/django-url-filter\n* Documentation: http://django-url-filter.readthedocs.io/\n\nNotes\n-----\nThis is a forked version of https://github.com//miki725/django-url-filter to add Django 4 support and my other projects.\n\nOverview\n--------\n\nThe main goal of Django URL Filter is to provide an easy URL interface\nfor filtering data. It allows the user to safely filter by model\nattributes and also allows to specify the lookup type for each filter\n(very much like Django\'s filtering system in ORM).\n\nFor example the following will retrieve all items where the id is\n``5`` and title contains ``"foo"``::\n\n    example.com/listview/?id=5&title__contains=foo\n\nIn addition to basic lookup types, Django URL Filter allows to\nuse more sophisticated lookups such as ``in`` or ``year``.\nFor example::\n\n    example.com/listview/?id__in=1,2,3&created__year=2013\n\nRequirements\n------------\n\n* Python 3.9+\n* Django 3.4+\n* Django REST Framework 2 or 3 (only if you want to use DRF integration)\n\nInstalling\n----------\n\nEasiest way to install this library is by using ``pip``::\n\n    $ pip install dj-url-filter\n\nUsage Example\n-------------\n\nTo make example short, it demonstrates Django URL Filter integration\nwith Django REST Framework but it can be used without DRF (see below).\n\n::\n\n  from url_filter.integrations.drf import DjangoFilterBackend\n\n\n  class UserViewSet(ModelViewSet):\n      queryset = User.objects.all()\n      serializer_class = UserSerializer\n      filter_backends = [DjangoFilterBackend]\n      filter_fields = [\'username\', \'email\']\n\nAlternatively filterset can be manually created and used directly\nto filter querysets::\n\n  from django.http import QueryDict\n  from url_filter.filtersets import ModelFilterSet\n\n\n  class UserFilterSet(ModelFilterSet):\n      class Meta(object):\n          model = User\n\n  query = QueryDict(\'email__contains=gmail&joined__gt=2015-01-01\')\n  fs = UserFilterSet(data=query, queryset=User.objects.all())\n  filtered_users = fs.filter()\n\nAbove will automatically allow the use of all of the Django URL Filter features.\nSome possibilities::\n\n    # get user with id 5\n    example.com/users/?id=5\n\n    # get user with id either 5, 10 or 15\n    example.com/users/?id__in=5,10,15\n\n    # get user with id between 5 and 10\n    example.com/users/?id__range=5,10\n\n    # get user with username "foo"\n    example.com/users/?username=foo\n\n    # get user with username containing case insensitive "foo"\n    example.com/users/?username__icontains=foo\n\n    # get user where username does NOT contain "foo"\n    example.com/users/?username__icontains!=foo\n\n    # get user who joined in 2015 as per user profile\n    example.com/users/?profile__joined__year=2015\n\n    # get user who joined in between 2010 and 2015 as per user profile\n    example.com/users/?profile__joined__range=2010-01-01,2015-12-31\n\n    # get user who joined in after 2010 as per user profile\n    example.com/users/?profile__joined__gt=2010-01-01\n\nFeatures\n--------\n\n* **Human-friendly URLs**\n\n  Filter querystring format looks\n  very similar to syntax for filtering in Django ORM.\n  Even negated filters are supported! Some examples::\n\n    example.com/users/?email__contains=gmail&joined__gt=2015-01-01\n    example.com/users/?email__contains!=gmail  # note !\n\n* **Related models**\n\n  Support related fields so that filtering can be applied to related\n  models. For example::\n\n    example.com/users/?profile__nickname=foo\n\n* **Decoupled filtering**\n\n  How URLs are parsed and how data is filtered is decoupled.\n  This allows the actual filtering logic to be decoupled from Django\n  hence filtering is possible not only with Django ORM QuerySet but\n  any set of data can be filtered (e.g. SQLAlchemy query objects)\n  assuming corresponding filtering backend is implemented.\n\n* **Usage-agnostic**\n\n  This library decouples filtering from any particular usage-pattern.\n  It implements all the basic building blocks for creating\n  filtersets but it does not assume how they will be used.\n  To make the library easy to use, it ships with some integrations\n  with common usage patterns like integration with Django REST Framework.\n  This means that its easy to use in custom applications with custom\n  requirements (which is probably most of the time!)\n',
    'author': 'Hat Dao',
    'author_email': 'enjoy3013@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
