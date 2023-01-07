# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ap0dl',
 'ap0dl.core',
 'ap0dl.core.cli',
 'ap0dl.core.cli.commands',
 'ap0dl.core.cli.helpers',
 'ap0dl.core.cli.helpers.players',
 'ap0dl.core.codebase',
 'ap0dl.core.codebase.downloader',
 'ap0dl.core.codebase.extractors',
 'ap0dl.core.codebase.extractors.dailymotion',
 'ap0dl.core.codebase.extractors.doodstream',
 'ap0dl.core.codebase.extractors.gogoplay',
 'ap0dl.core.codebase.extractors.mp4upload',
 'ap0dl.core.codebase.extractors.mycloud',
 'ap0dl.core.codebase.extractors.okru',
 'ap0dl.core.codebase.extractors.rapidvideo',
 'ap0dl.core.codebase.extractors.streamlare',
 'ap0dl.core.codebase.extractors.streamsb',
 'ap0dl.core.codebase.extractors.streamtape',
 'ap0dl.core.codebase.extractors.videobin',
 'ap0dl.core.codebase.extractors.vidstream',
 'ap0dl.core.codebase.helpers',
 'ap0dl.core.codebase.providers',
 'ap0dl.core.codebase.providers.allanime',
 'ap0dl.core.codebase.providers.animekaizoku',
 'ap0dl.core.codebase.providers.animeonsen',
 'ap0dl.core.codebase.providers.animeout',
 'ap0dl.core.codebase.providers.animepahe',
 'ap0dl.core.codebase.providers.animepahe.inner',
 'ap0dl.core.codebase.providers.animexin',
 'ap0dl.core.codebase.providers.animixplay',
 'ap0dl.core.codebase.providers.animtime',
 'ap0dl.core.codebase.providers.crunchyroll',
 'ap0dl.core.codebase.providers.gogoanime',
 'ap0dl.core.codebase.providers.hahomoe',
 'ap0dl.core.codebase.providers.hentaistream',
 'ap0dl.core.codebase.providers.kamyroll',
 'ap0dl.core.codebase.providers.kawaiifu',
 'ap0dl.core.codebase.providers.nineanime',
 'ap0dl.core.codebase.providers.tenshimoe',
 'ap0dl.core.codebase.providers.twistmoe',
 'ap0dl.core.codebase.providers.zoro',
 'ap0dl.core.config']

package_data = \
{'': ['*']}

install_requires = \
['anchor-kr>=0.1.3,<0.2.0',
 'anitopy>=2.1.0,<2.2.0',
 'click>=8.0.4,<8.1.0',
 'comtypes>=1.1.11,<1.2.0',
 'cssselect>=1.1.0,<1.2.0',
 'httpx>=0.23.0,<0.24.0',
 'packaging>=22.0,<23.0',
 'pkginfo>=1.9.2,<2.0.0',
 'pycryptodomex>=3.14.1,<3.15.0',
 'pyyaml>=6.0,<7.0',
 'regex>=2022.10.31,<2022.11.0',
 'rich>=13.0.0,<14.0.0',
 'tqdm>=4.62.3,<4.63.0',
 'yarl>=1.8.1,<1.9.0']

entry_points = \
{'console_scripts': ['ap0dl = ap0dl.__main__:__ap0dl_cli__']}

setup_kwargs = {
    'name': 'ap0dl',
    'version': '1.5.1',
    'description': 'Efficient, fast, powerful and light-weight anime multi-purpose tool',
    'long_description': '',
    'author': 'rares9301',
    'author_email': 'rares.sarmasag@cnmbct.ro',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
