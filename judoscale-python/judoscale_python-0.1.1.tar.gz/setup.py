# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['judoscale', 'judoscale.core', 'judoscale.django', 'judoscale.flask']

package_data = \
{'': ['*']}

install_requires = \
['requests<3.0.0']

setup_kwargs = {
    'name': 'judoscale-python',
    'version': '0.1.1',
    'description': 'Official Python adapter for Judoscale — the advanced autoscaler for Heroku',
    'long_description': '# judoscale-python\n\nThis is the official Python adapter for [Judoscale](https://elements.heroku.com/addons/judoscale). You can use Judoscale without it, but this gives you request queue time metrics and job queue time (for supported job processors).\n\n## Installation\n\nAdd judoscale-python to your <code>requirements.txt</code> file or the equivalent:\n\n```\njudoscale-python >= 1.0.0rc1\n```\n\nThen run this from a terminal to install the package:\n\n```sh\npip install -r requirements.txt\n```\n\n## Supported web frameworks\n\n- [x] Django\n- [x] Flask\n- [ ] FastAPI\n\n## Supported job processors\n\n- [ ] Celery\n- [ ] RQ\n\n## Using Judoscale with Django\n\nAdd Judoscale app to `settings.py`:\n\n```python\nINSTALLED_APPS = [\n    "judoscale.django",\n    # ... other apps\n]\n```\n\nThis sets up the Judoscale middleware to capture request queue times.\n\nOptionally, you can customize Judoscale in `settings.py`:\n\n```python\nJUDOSCALE = {\n    # LOG_LEVEL defaults to ENV["LOG_LEVEL"] or "INFO".\n    "LOG_LEVEL": "DEBUG",\n\n    # API_BASE_URL defaults to ENV["JUDOSCALE_URL"], which is set for you when you install Judoscale.\n    # This is only exposed for testing purposes.\n    "API_BASE_URL": "https://example.com",\n\n    # REPORT_INTERVAL_SECONDS defaults to 10 seconds.\n    "REPORT_INTERVAL_SECONDS": 5,\n}\n```\n\nOnce deployed, you will see your request queue time metrics available in the Judoscale UI.\n\n# Using Judoscale with Flask\n\nThe Flask support for Judoscale is packaged into a Flask extension. Import the extension class and use like you normally would in a Flask application:\n\n\n```py\n# app.py\n\nfrom judoscale.flask import Judoscale\n\n# If your app is a top-level global\n\napp = Flask("MyFlaskApp")\napp.config.from_object(\'...\')  # or however you configure your app\njudoscale = Judoscale(app)\n\n\n# If your app uses the application factory pattern\n\njudoscale = Judoscale()\n\ndef create_app():\n    app = Flask("MyFlaskApp")\n    app.config.from_object(\'...\')  # or however you configure your app\n    judoscale.init_app(app)\n    return app\n```\n\nThis sets up the Judoscale extension to capture request queue times.\n\nOptionally, you can override Judoscale\'s own configuration via your application\'s [configuration dictionary](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Flask.config). The Judoscale Flask extension looks for a top-level `"JUDOSCALE"` key in `app.config`, which should be a dictionary, and which the extension uses to configure itself as soon as `judoscale.init_app()` is called.\n\n```python\nJUDOSCALE = {\n    # LOG_LEVEL defaults to ENV["LOG_LEVEL"] or "INFO".\n    "LOG_LEVEL": "DEBUG",\n\n    # API_BASE_URL defaults to ENV["JUDOSCALE_URL"], which is set for you when you install Judoscale.\n    # This is only exposed for testing purposes.\n    "API_BASE_URL": "https://example.com",\n\n    # REPORT_INTERVAL_SECONDS defaults to 10 seconds.\n    "REPORT_INTERVAL_SECONDS": 5,\n}\n```\n\nNote the [official recommendations for configuring Flask](https://flask.palletsprojects.com/en/2.2.x/config/#configuration-best-practices).\n\n## Development\n\nThis repo includes a `sample-apps` directory containing apps you can run locally. These apps use the judoscale-python adapter, but they override `API_BASE_URL` so they\'re not connected to the real Judoscale API. Instead, they post API requests to https://requestcatcher.com so you can observe the API behavior.\n\nSee the `README` in a sample app for details on how to set it up and run locally.\n\n### Contributing\n\n`judoscale-python` uses [Poetry](https://python-poetry.org/) for managing dependencies and packaging the project. Head over to the [installations instructions](https://python-poetry.org/docs/#installing-with-the-official-installer) and install Poetry, if needed.\n\nClone the repo with\n\n```sh\n$ git clone git@github.com:judoscale/judoscale-python.git\n$ cd judoscale-python\n```\n\nVerify that you are on a recent version of Poetry:\n\n```sh\n$ poetry --version\nPoetry (version 1.3.1)\n```\n\nInstall dependencies with Poetry and activate the virtualenv\n\n```sh\n$ poetry install\n$ poetry shell\n```\n\nRun tests with\n\n```sh\n$ python -m unittest discover -s tests\n```\n',
    'author': 'Adam McCrea',
    'author_email': 'adam@adamlogic.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/judoscale/judoscale-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
