# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dadfes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-admin-data-from-external-service',
    'version': '0.1.2',
    'description': 'Helpers to extend Django Admin with data from external service with minimal hacks',
    'long_description': '\n<div align="center">\n <p><h1>django-admin-data-from-external-service</h1> </p>\n  <p><strong>Helpers to extend Django Admin with data from external service with minimal hacks</strong></p>\n  <p></p>\n</div>\n\n[Live demo](https://dadfes.herokuapp.com/) with [sources](https://github.com/estin/django-admin-data-from-external-service/tree/master/demo) on [Heroku](https://heroku.com) free quota (please be patient, it will take some time for the app to wake up)\n - [view](http://dadfes.herokuapp.com/github/repository/) Github repository of Django org ([sources](https://github.com/estin/django-admin-data-from-external-service/tree/master/demo/github/models.py)), may appear api rate limit error\n - [view](http://dadfes.herokuapp.com/clickhouse/recipe/) recipes from ClickHouse [playground](https://clickhouse.com/docs/en/getting-started/example-datasets/recipes/) ([sources](https://github.com/estin/django-admin-data-from-external-service/tree/master/demo/clickhouse/models.py))\n\nMain features:\n - reuse Django Admin layout to simplify customization of viewing and managing external data (list/view/filter+search/ordering)\n - datasource agnostic\n - django2.x/django3.x/django4.x support\n\n## How it works\n\nUsed custom ChangeList to determine method to pull external data and mock paginator behaviour.\n\n## Example\n\n```python\nfrom django.db import models\nfrom django.contrib import admin\n\nfrom dadfes.admin import DfesAdminModelMixin\n\n\n# Declare model for external data (managed: false)\nclass ExternalUser(models.Model):\n    id = models.IntegerField("Id", primary_key=True)\n    username = models.TextField("Username")\n\n    class Meta:\n        managed = False\n        verbose_name = "External User Model"\n\n\n# 1. mixin DfesAdminModelMixin\nclass ExternalUserAdmin(DfesAdminModelMixin, admin.ModelAdmin):\n    list_display = (\n        "id",\n        "username",\n    )\n\n    # 2. and implement get_list method with returning\n    # `{"total": <total number or items>, "items": <list of ExternalUser instances>}`\n    def get_list(self, request, page_num, list_per_page):\n\n        # 2.1 pull data from some service, where\n        #   search = request.GET.get(\'q\')\n        #   order_by = request.GET.get(\'o\')\n        #   some_list_filter = request.GET.get(\'some_list_filter\')\n        data =  {\n            \'total\': 1,\n            \'users\': [\n                {\'id\': 1, \'username\': \'User1\'},\n            ]\n        }\n\n        # 2.2 map data to model instances\n        items = [ExternalUser(**i) for i in data.get("users") or []]\n\n        return {\n            "total": data.get("total") or 0,\n            "items": items,\n        }\n\n    # 3. other standart django admin customization\n    def get_object(self, request, object_id, *args, **kwargs):\n        # 3.1 fetch object from external service\n        user = {\'id\': 1, \'username\': \'User1\'},\n        # 3.2 map data to model instance\n        return ExternalUser(**user)\n\nadmin.site.register(ExternalUser, ExternalUserAdmin)\n```\n\n## License\n\nThis project is licensed under\n\n* MIT license ([LICENSE](LICENSE) or [http://opensource.org/licenses/MIT](http://opensource.org/licenses/MIT))\n',
    'author': 'Evgeniy Tatarkin',
    'author_email': 'tatarkin.evg@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/estin/django-admin-data-from-external-service',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
