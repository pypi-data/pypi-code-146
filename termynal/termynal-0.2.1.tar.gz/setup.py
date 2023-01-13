# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['termynal']

package_data = \
{'': ['*'], 'termynal': ['assets/*']}

install_requires = \
['markdown']

extras_require = \
{'mkdocs': ['mkdocs>=1.4,<2.0']}

entry_points = \
{'markdown.extensions': ['termynal = termynal.markdown:TermynalExtension'],
 'mkdocs.plugins': ['termynal = termynal.plugin:TermynalPlugin']}

setup_kwargs = {
    'name': 'termynal',
    'version': '0.2.1',
    'description': '',
    'long_description': '# Termynal\n\nA lightweight and modern animated terminal window.\nBuilt for [mkdocs](https://www.mkdocs.org/).\n\n## Installation\n\n<!-- termynal -->\n\n```\n$ pip install termynal\n---> 100%\nInstalled\n```\n\n[Example](https://daxartio.github.io/termynal/)\n\n## Usage\n\nUse `<!-- termynal -->` before code block\n\n````\n<!-- termynal -->\n\n```\n// code\n```\n````\n\nor `console` in code block\n\n````\n```console\n// code\n```\n````\n\nprogress, prompt `---> 100%`\n\n````\n```console\n$ show progress\n---> 100%\nDone!\n```\n````\n\ncommand, start with `$`\n\n````\n```console\n$ command\n```\n````\n\ncomment, start with `#`\n\n````\n```console\n# comment\n```\n````\n\n`mkdocs` plugin\n\n```yaml\n...\nplugins:\n  - termynal\n...\n```\n\nThanks [ines](https://github.com/ines/termynal)\n',
    'author': 'Danil Akhtarov',
    'author_email': 'daxartio@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/termynal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
