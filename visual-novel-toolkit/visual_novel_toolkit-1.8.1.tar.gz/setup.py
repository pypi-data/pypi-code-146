# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['visual_novel_toolkit', 'visual_novel_toolkit.words']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4', 'httpx', 'typer']

entry_points = \
{'console_scripts': ['vntk = visual_novel_toolkit:cli']}

setup_kwargs = {
    'name': 'visual-novel-toolkit',
    'version': '1.8.1',
    'description': 'A set of useful tools to improve DX of visual novel games.',
    'long_description': '# Visual novel toolkit [![build](https://img.shields.io/github/workflow/status/proofit404/visual-novel-toolkit/release?style=flat-square)](https://github.com/proofit404/visual-novel-toolkit/actions/workflows/release.yml?query=branch%3Arelease) [![pypi](https://img.shields.io/pypi/v/visual-novel-toolkit?style=flat-square)](https://pypi.org/project/visual-novel-toolkit)\n\nA set of useful tools to improve DX of visual novel games.\n\n**[Documentation](https://proofit404.github.io/visual-novel-toolkit) |\n[Source Code](https://github.com/proofit404/visual-novel-toolkit) |\n[Task Tracker](https://github.com/proofit404/visual-novel-toolkit/issues)**\n\n![](index.jpg)\n\n## Questions\n\nIf you have any questions, feel free to create an issue in our\n[Task Tracker](https://github.com/proofit404/visual-novel-toolkit/issues). We\nhave the\n[question label](https://github.com/proofit404/visual-novel-toolkit/issues?q=is%3Aopen+is%3Aissue+label%3Aquestion)\nexactly for this purpose.\n\n## Enterprise support\n\nIf you have an issue with any version of the library, you can apply for a paid\nenterprise support contract. This will guarantee you that no breaking changes\nwill happen to you. No matter how old version you\'re using at the moment. All\nnecessary features and bug fixes will be backported in a way that serves your\nneeds.\n\nPlease contact [proofit404@gmail.com](mailto:proofit404@gmail.com) if you\'re\ninterested in it.\n\n## License\n\n`visual-novel-toolkit` library is offered under the two clause BSD license.\n\n<p align="center">&mdash; ⭐ &mdash;</p>\n',
    'author': 'Josiah Kaviani',
    'author_email': 'proofit404@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/visual-novel-toolkit',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '==3.11.1',
}


setup(**setup_kwargs)
