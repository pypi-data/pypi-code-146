# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['formkit_ninja',
 'formkit_ninja.management.commands',
 'formkit_ninja.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.1.5,<5.0.0',
 'django-ninja>=0.20.0,<0.21.0',
 'django-ordered-model>=3.6,<4.0',
 'pydantic<2']

setup_kwargs = {
    'name': 'formkit-ninja',
    'version': '0.1.4',
    'description': 'A Django-Ninja backend to specify FormKit schemas',
    'long_description': '# Formkit-Ninja\n\nA Django-Ninja framework for FormKit schemas and form submissions\n\n## Why\n\nFormKit out of the box has awesome schema support - this lets us integrate FormKit instances as Django models\n\n- Upload / edit / download basic FormKit schemas\n- Translated "option" values from the Django admin\n- Reorder "options" and schema nodes\n- List and Fetch schemas for different form types\n\n## Use\n\nTo use, `pip install formkit-ninja` and add the following to settings `INSTALLED_APPS`:\n\n```py\nINSTALLED_APPS = [\n    ...\n    "formkit_ninja",\n    "ordered_model",\n    "ninja",\n    ...\n]\n```\n\n## Test\n\nPull the repo:\n\n`gh repo clone catalpainternational/formkit-ninja`\n`cd formkit-ninja`\n`poetry install`\n`poetry run pytest`\n\n## Lint\n\n`poetry run black --check .`\n`poetry run isort --check .`\n`poetry run flake8 .`\n',
    'author': 'Josh Brooks',
    'author_email': 'josh@catalpa.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/catalpainternational/formkit-ninja',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
