# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['make_release']

package_data = \
{'': ['*']}

install_requires = \
['runcommands>=1.0a71,<2.0']

entry_points = \
{'console_scripts': ['make-release = make_release:make_release.console_script']}

setup_kwargs = {
    'name': 'com-wyattbaldwin-make-release',
    'version': '1.0a4',
    'description': 'Make a release',
    'long_description': '# Make a Release\n\nMake a release of a Python package. This automates the tedious steps you\nneed to go through to make a release--bumping the version number,\ntagging, etc.\n\nIt does _not_ (currently) create distributions or upload them to PyPI.\n\n## Usage\n\n    make-release --version 1.0 --next-version 2.0\n\n## Steps\n\nBy default, all the following steps are run:\n\n- Run the project\'s test suite (`python -m unittest discover` by\n  default)\n- Prepare the release by bumping the version number in various files and\n  setting the release date in the change log file\n- Merge the development branch into the target branch (e.g., `dev` to\n  `main`)\n- Create an annotated tag pointing at the merge commit (or at the prep\n  commit when merging is disabled); if no tag name is specified, the\n  release version is used as the tag name\n- Resume development by bumping the version to the next anticipated\n  version\n\nAny of the steps can be skipped by passing the corresponding\n`--no-<step>` flag.\n\n### Tag Name\n\nThe tag name can be specified as a simple format string template. The\nproject `name` and release `version` will be injected (see below in the\nConfiguration section for an example).\n\n## Configuration\n\nConfiguration can be done in `pyproject.toml` or `setup.cfg`. This is\nmost useful if you want to permanently change one of the default\noptions.\n\nUse the long names of the command line options without the leading\ndashes. For command line flags, set the value to `true` or `false`\n(`1` and `0` also work).\n\nFor example, if your project only uses a single branch, you could\ndisable the merge step like so in `pyproject.toml`.\n\n    # pyproject.toml\n    [tool.make-release.args]\n    merge = false\n    tag-name = "{name}-{version}"\n    test-command = "my-test-runner"\n\nor like so in `setup.cfg`:\n\n    # setup.cfg\n    [make-release.args]\n    merge = false\n    tag-name = {name}-{version}\n    test-command = my-test-runner\n\nThis also shows how to specify a tag name template that\'s derived from\nthe package `name` and the release `version`.\n\n## Creating and Uploading Distribution\n\nOnce you\'ve created a release with this tool, check out the tag for the\nrelease and then run the following commands:\n\n    poetry build           # if using poetry\n    python setup.py sdist  # if using pip/setuptools\n    twine upload dist/*    # in either case\n\nNOTE: You\'ll need an account on pypi.org in order to upload\ndistributions with `twine`.\n\n## Limitations\n\n- Only git repositories are supported\n- The package name detection assumes the root directory (i.e., the git\n  repo name) is the same as the package name\n- For the change log, only markdown files are supported; the change log\n  is expected to use second-level (##) headings for each version\'s\n  section (see this project\'s `CHANGELOG.md` for an example)\n- Doesn\'t build or upload distributions\n',
    'author': 'Wyatt Baldwin',
    'author_email': 'self@wyattbaldwin.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wylee/com.wyattbaldwin/tree/dev/make-release',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
