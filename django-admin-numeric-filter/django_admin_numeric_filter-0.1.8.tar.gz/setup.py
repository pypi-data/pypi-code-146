# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['admin_numeric_filter']

package_data = \
{'': ['*'],
 'admin_numeric_filter': ['static/css/*', 'static/js/*', 'templates/admin/*']}

install_requires = \
['django>=3.2']

setup_kwargs = {
    'name': 'django-admin-numeric-filter',
    'version': '0.1.8',
    'description': 'Numeric filters for Django admin',
    'long_description': "![Screenshot](https://github.com/lukasvinclav/django-admin-numeric-filter/raw/master/screenshot.png)\n\n# django-admin-numeric-filter\n\n![](https://img.shields.io/badge/Version-0.1.8-orange.svg?style=flat-square)\n![](https://img.shields.io/badge/Django-2.0+-green.svg?style=flat-square)\n![](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)\n\ndjango-admin-numeric-filter provides you several filter classes for Django admin which you can use to filter results in change list. It works in **list_filter** when a field name is defined as list where the first value is field name and second one is custom filter class (you can find classes below).\n\nDon't forget to inherit your model admin from **admin_actions.admin.NumericFilterModelAdmin** to load custom CSS styles and JavaScript files declared in inner Media class.\n\n## Getting started\n\n1. Installation\n\n```bash\npip install django-admin-numeric-filter\n```\n\n2. Add **admin_numeric_filter** into **INSTALLED_APPS** in your settings file before **django.contrib.admin**.\n\n## Sample admin configuration\n\n```python\nfrom admin_numeric_filter.admin import NumericFilterModelAdmin, SingleNumericFilter, RangeNumericFilter, \\\n    SliderNumericFilter\n\nfrom .models import YourModel\n\n\nclass CustomSliderNumericFilter(SliderNumericFilter):\n    MAX_DECIMALS = 2\n    STEP = 10\n\n\n@admin.register(YourModel)\nclass YourModelAdmin(NumericFilterModelAdmin):\n    list_filter = (\n        ('field_A', SingleNumericFilter), # Single field search, __gte lookup\n        ('field_B', RangeNumericFilter), # Range search, __gte and __lte lookup\n        ('field_C', SliderNumericFilter), # Same as range above but with slider\n        ('field_D', CustomSliderNumericFilter), # Filter with custom attributes\n    )\n```\n\n## Filter classes\n\n| Class name                               | Description                            |\n|------------------------------------------|----------------------------------------|\n| admin_actions.admin.SingleNumericFilter  | Single field search, __gte lookup      |\n| admin_actions.admin.RangeNumericFilter   | Range search, __gte and __lte lookup   |\n| admin_actions.admin.SliderNumericFilter  | Same as range above but with slider    |\n\n\n## Slider default options for certain field types\n\n| Django model field                       | Step                     | Decimal places             |\n|------------------------------------------|--------------------------|----------------------------|\n| django.db.models.fields.DecimalField()   | Based on decimal places  | max precision from DB      |\n| django.db.models.fields.FloatField()     | Based on decimal places  | field decimal_places attr  |\n| django.db.models.fields.IntegerField()   | 1                        | 0                          |",
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lukasvinclav/django-admin-numeric-filter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
