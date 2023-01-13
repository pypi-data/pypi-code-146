# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dapla', 'dapla.spark']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.6.0,<3.0.0',
 'gcsfs>=2022.7.1',
 'google-cloud-storage>=2.7.0,<3.0.0',
 'ipython>=8.6.0,<9.0.0',
 'jupyterhub>=3.0.0,<4.0.0',
 'lxml>=4.9.1,<5.0.0',
 'pandas>=1.4.2',
 'pyarrow>=8.0.0',
 'pydantic>=1.9.1',
 'requests>=2.27.1']

setup_kwargs = {
    'name': 'dapla-toolbelt',
    'version': '1.3.9',
    'description': "Python module for use within Jupyterlab notebooks, specifically aimed for Statistics Norway's data platform called Dapla",
    'long_description': '# dapla-toolbelt\n\nPython module for use within Jupyterlab notebooks, specifically aimed for Statistics Norway\'s data platform called \n`Dapla`. It contains support for authenticated access to Google Services such as Google Cloud Storage (GCS) and custom\nDapla services such as [Maskinporten Guardian](https://github.com/statisticsnorway/maskinporten-guardian). The \nauthentication process is based on the [TokenExchangeAuthenticator](https://github.com/statisticsnorway/jupyterhub-extensions/tree/main/TokenExchangeAuthenticator)\nfor Jupyterhub.\n\n[![PyPI version](https://img.shields.io/pypi/v/dapla-toolbelt.svg)](https://pypi.python.org/pypi/dapla-toolbelt/)\n![Unit tests](https://github.com/statisticsnorway/dapla-toolbelt/actions/workflows/unit-tests.yml/badge.svg) \n![Code coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/bjornandre/73205f2f30335801fa2819c31b3ecf79/raw/pytest-coverage-badge-dapla-toolbelt.json) \n![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)\n[![License](https://img.shields.io/pypi/l/dapla-toolbelt.svg)](https://pypi.python.org/pypi/dapla-toolbelt/)\n\nThese operations are supported:\n* List contents of a bucket\n* Open a file in GCS\n* Copy a file from GCS into local\n* Load a file (CSV, JSON or XML) from GCS into a pandas dataframe\n* Save contents of a data frame into a file (CSV, JSON, XML) in GCS\n\nWhen the user gives the path to a resource, they do not need to give the GCS uri, only the path. \nThis just means users don\'t have to prefix a path with "gs://". \nIt is implicitly understood that all resources accessed with this tool are located in GCS, \nwith the first level of the path being a GCS bucket name.\n\n## Installation\n\n`pip install dapla-toolbelt`\n\n## Usage Examples\n\n``` python\nfrom dapla import FileClient\nfrom dapla import GuardianClient\nimport pandas as pd\n\n# Load data using the Maskinporten Guardian client\nresponse = GuardianClient.call_api("https://data.udir.no/api/kag", "88ace991-7871-4ccc-aaec-8fb6d78ed04e", "udir:datatilssb")\ndata_json = response.json()\n\nraw_data_df = pd.DataFrame(data_json)  # create pandas data frame from json\nraw_data_df.head()  # show first rows of data frame\n\nFileClient.ls("bucket-name/folder")  # list contents of given folder\n\n# Save data into different formats\npath_base = "bucket-name/folder/raw_data"\nFileClient.save_pandas_to_json(raw_data_df, f"{path_base}.json")  # generate json from data frame, and save to given path\nFileClient.save_pandas_to_csv(raw_data_df, f"{path_base}.csv")  # generate csv from data frame, and save to given path\nFileClient.save_pandas_to_xml(raw_data_df, f"{path_base}.xml")  # generate xml from data frame, and save to given path\n\nFileClient.cat(f"{path_base}.json")  # print contents of file\n\n# Load data from different formats\n# All these data frames should contain the same data:\ndf = FileClient.load_json_to_pandas(f"{path_base}.json")  # read json from path and load into pandas data frame\ndf.head()  # show first rows of data frame\ndf = FileClient.load_csv_to_pandas(f"{path_base}.csv")  # read csv from path and load into pandas data frame\ndf.head()  # show first rows of data frame\ndf = FileClient.load_xml_to_pandas(f"{path_base}.xml")  # read xml from path and load into pandas data frame\ndf.head()  # show first rows of data frame\n\n```\n\n## Development\n\n### Prerequisites\n\n- Python >3.8 (3.10 is preferred)\n- Poetry, install via `curl -sSL https://install.python-poetry.org | python3 -`\n\nYou can also execute `make` in the project folder to see available `make` commands.\n\n### Dependency Management\n\nPoetry is used for dependency management. [Poe the Poet](https://github.com/nat-n/poethepoet) is used for running poe tasks within poetry\'s virtualenv. \nUpon cloning this project first install necessary dependencies, then run the tests to verify everything is working.\n\n#### Install all dependencies\n\n```shell\npoetry install\n```\n\n### Add dependencies\n\n#### Main\n\n```shell\npoetry add <python package name>\n```\n\n#### Dev\n\n```shell\npoetry add --group dev <python package name>\n```\n\n### Run tests\n\n```shell\npoetry run poe test\n```\n\n### Run project locally in Jupyter\n\nTo run the project locally in Jupyter run:\n\n```shell\npoetry run poe jupyter\n```\n\nA Jupyter instance should open in your browser. Open and run the cells in the `demo.ipynb` file.\n\n### Bumping version\n\nUse `make` to bump the *patch*, *minor* version or *major* version before creating a pull request to the `main` GIT branch.\nOr run a poe task like this:\n\n```shell\npoetry run poe bump-patch-version\n```\n\nYou can use either `bump-version-patch`, `bump-version-minor`, or `bump-version-major`.\nBumping must be done with a clean git working space, and automatically commits with the new version number.\n\nThen just run `git push origin --tags` to push the changes and trigger the release process.\n\n### Building and releasing\n\nBefore merging your changes into the `main` branch, make sure you have bumped the version like outlined above.\n\nAn automatic release process will build *dapla-toolbelt* upon pull request-creation, merges, and direct commits to the\n`main` GIT branch. It will also release a new version of the package to **pypi.org** automatically when a commit is \ntagged, for example by a GitHub release.\n\n### Building and releasing manually\n\nRun `make build` to build a wheel and a source distribution.\n\nRun `make release-validate` to do all that AND validate it for release.\n\nRun this (replacing <SEMVER> with your current version number) to check the contents of your wheel:\n`tar tzf dist/dapla-toolbelt-<SEMVER>.tar.gz`\n\n#### Test release\n\nYou have to bump the version of the package (see documentation on "Bumping version" above) before releasing, \nbecause even test.pypi.org does not allow re-releases of a previously released version.\n\nRun the following command in order to build, validate, and test package publication by uploading to TestPyPI:\n`make release-test`\n\nYou will have to manually enter a username and password for a user registered to [test.pypi.org](https://test.pypi.org) \nin order for this to work.\n\n#### Production release\n\n**NB: A manual production release should only be done as a last resort**, if the regular CI/CD pipeline \ndoes not work, and it\'s necessary to release regardless.\n\nYou have to bump the version of the package (see documentation on "Bumping version" above) to something \ndifferent from the last release before releasing.\n\nIn order to publish a new version of the package to PyPI for real, run `make release`. \nAuthenticate by manually entering your [pypi.org](https://pypi.org) username and password. \n',
    'author': 'Statistics Norway',
    'author_email': 'stat-dev@ssb.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/statisticsnorway/dapla-toolbelt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
