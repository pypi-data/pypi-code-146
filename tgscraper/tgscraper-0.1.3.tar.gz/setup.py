# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tgscraper']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.2,<2.0.0', 'pydantic>=1.10.4,<2.0.0', 'telethon>=1.26.1,<2.0.0']

setup_kwargs = {
    'name': 'tgscraper',
    'version': '0.1.3',
    'description': 'Demo version of a package for easy telegram scraping',
    'long_description': '# tgscraper\n\nThis is a simple package to scrape data from Telegram channels (and other content in the future). It is based on the [Telethon](https://docs.telethon.dev/en/stable/).\n\nIt can be used as a CLI tool (saves scraped data to a CSV file) or as a Python package (returns pandas DataFrame).\n\n## Installation\n\n### Install to run as a CLI tool\n\nTo use it as a CLI, ptobably the best way to install tgscraper is just to clone this repository and run it from there. We use Poetry to manage dependencies and Python version. To install Poetry, follow the instructions [here](https://python-poetry.org/docs/#installation). After that, run the following commands in the root directory of the project:\n\n```bash\npoetry install\npoetry add tgscraper\n```\n\n**To run tgscraper as a script, you need Python 3.11 installed** (otherwise, Poetry will probably fail to create an environment).\n\nAlternatively, you can install dependencies into you own environment without Poetry, using `requirements.txt` file (it can be found in this repository):\n\n```bash\npip install -r requirements.txt\npip install tgscraper\n```\n\n### Install to use in your code\n\n#### For poetry\n\nIf you use Poetry, just include the dependencies in your `pyproject.toml` file:\n\n```toml\n[tool.poetry.dependencies]\npython = "^3.11"\npydantic = "^1.10.4"\ntelethon = "^1.26.1"\npandas = "^1.5.2"\n```\n\nMake sure that you don\'t have any conflicts with the versions of the dependencies.\n\nThen, add tgscraper to your project and install it:\n\n```bash\npoetry add tgscraper\npoetry install\n```\n\n#### For other environment managers\n\nIf you use other environment managers, you can install tgscraper using pip:\n\n```bash\npip install -r requirements.txt\npip install tgscraper\n```\n\n#### Python version\n\n**To use tgscraper in your code, you need Python 3.11 in the environment that you use.**\n\n## Usage\n\n### Provide API credentials\n\nTo run tgscraper you need to provide `tgs_config.toml` file with your API credentials in `tgscraper` directory. You can get them from [my.telegram.org](https://my.telegram.org/). List of channels you want to scrape is also required here. It looks like this (you can find an example in `tgs_config.toml.example` file)\n\n```toml\n[telegram]\n# api_id = ID HERE (int)\n# api_hash = HASH HERE (str)\n# phone = PHONE HERE (str)\n# username = USERNAME HERE (str)\n\n[input]\nchannels = ["https://t.me/svtvnews"]\n# You can include multiple channels here\n```\n\nAlternatively, you can use interactive mode to provide this information (it is enabled automatically if you don\'t provide `tgs_config.toml` file).\n\n### Run the scraper as a CLI tool\n\nWe use Poetry to manage dependencies and build the package. To run the scraper as a CLI tool, you need to run it in Poetry\'s virtual environment. To do that, run the following command in the root directory of the project:\n\n```bash\npoetry run python tgscraper/tgscraper.py\n```\n\nThe script will create a folder `output` in the root directory of the project if it doesn\'t exist and save the scraped data there. The name of the file will be the name of the channel.\n\nAlternatively, you can use `poetry shell` to enter the virtual environment and run the scraper just as a regular Python script.\n\n### Use in your code\n\nAfter pip installing the package, you can use it in your code like this:\n\n```python\nfrom tgscraper import tgscraper\nimport pandas as pd\n\n# Client a Telegram client\nclient = tgscraper.init()\n# Be aware that you can be prompted to enter your phone number and a code, sent to your Telegram account\n\n# Get the posts from the channel into a pandas DataFrame\nposts_df = tgscraper.get_posts(client, link, limit=100)\n\n# Do something with the data\nposts_df.to_csv("posts.csv")\n```\n\n### Logging\n\nBy default, tgscraper saves the logs into `logs` directory, filenames are constructed from date and time. To customize the logging, you can use `BasicConfig` from `logging` module. For example, to log into console, you can use the following code:\n\n```python\nimport logging\nlogging.basicConfig(level=logging.INFO)\n```\n\nYou can also get the logger and customize it:\n\n```python\nlogger = logging.getLogger("tgscraper")\n# Do something with the logger\n```\n\n## Contribution\n\nFeel free to open an issue or a pull request if you have any suggestions or found a bug. ',
    'author': 'Timofei Ryko',
    'author_email': 'timofei.ryko@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/timofeiryko/tgscraper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
