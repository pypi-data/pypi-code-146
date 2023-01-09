# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hue_sunrise']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0', 'requests>=2.28.1,<3.0.0', 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['hue-sunrise = hue_sunrise.main:app']}

setup_kwargs = {
    'name': 'hue-sunrise',
    'version': '0.6.4',
    'description': '',
    'long_description': '# Hue sunrise\n\n[![pipeline status](https://gitlab.com/marvin.vanaalst/hue-sunrise/badges/main/pipeline.svg)](https://gitlab.com/marvin.vanaalst/hue-sunrise/-/commits/main)\n[![coverage report](https://gitlab.com/marvin.vanaalst/hue-sunrise/badges/main/coverage.svg)](https://gitlab.com/marvin.vanaalst/hue-sunrise/-/commits/main)\n[![PyPi](https://img.shields.io/pypi/v/hue-sunrise)](https://pypi.org/project/hue-sunrise/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![Downloads](https://pepy.tech/badge/hue-sunrise)](https://pepy.tech/project/hue-sunrise)\n\nEnjoy waking up more gently by having your [philips hue](https://www.philips-hue.com/de-de) lights simulate a sunrise.\n\n## Installation\n\n```bash\npip install hue-sunrise\n```\n\n## Usage\n\nFirst register your Hue bridge interactively\n\n```bash\nhue-sunrise register\n```\n\nThen simply call it with\n\n```bash\nhue-sunrise run\n```\n\nAnd view the config using\n\n```bash\nhue-sunrise config show\n```\n\nIf you want to change the configuration use\n\n```bash\nhue-sunrise config ip               # IP address of your Hue bridge\nhue-sunrise config lights           # lights which should participate\nhue-sunrise config scene-length     # how many minutes the sunrise should take\nhue-sunrise config afterglow        # how many minutes to stay lit after the sunrise\n```\n\nor, if you want to change where the configuration files are stored use the following environment variables\n\n```bash\nHS_CONFIG_PATH\nHS_LOG_PATH\n```\n\n\nAnd finally if anything failed an you need to manually switch of the lights use\n\n```bash\nhue-sunrise shutdown\n```\n\n## Thanks\n\nThe beautiful CLI is due to [typer](https://typer.tiangolo.com/).\n',
    'author': 'Marvin van Aalst',
    'author_email': 'marvin.vanaalst@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
