# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['animdl',
 'animdl.core',
 'animdl.core.cli',
 'animdl.core.cli.commands',
 'animdl.core.cli.helpers',
 'animdl.core.cli.helpers.players',
 'animdl.core.codebase',
 'animdl.core.codebase.downloader',
 'animdl.core.codebase.extractors',
 'animdl.core.codebase.extractors.dailymotion',
 'animdl.core.codebase.extractors.doodstream',
 'animdl.core.codebase.extractors.gogoplay',
 'animdl.core.codebase.extractors.mp4upload',
 'animdl.core.codebase.extractors.mycloud',
 'animdl.core.codebase.extractors.okru',
 'animdl.core.codebase.extractors.rapidvideo',
 'animdl.core.codebase.extractors.streamlare',
 'animdl.core.codebase.extractors.streamsb',
 'animdl.core.codebase.extractors.streamtape',
 'animdl.core.codebase.extractors.videobin',
 'animdl.core.codebase.extractors.vidstream',
 'animdl.core.codebase.helpers',
 'animdl.core.codebase.providers',
 'animdl.core.codebase.providers.allanime',
 'animdl.core.codebase.providers.animekaizoku',
 'animdl.core.codebase.providers.animeonsen',
 'animdl.core.codebase.providers.animeout',
 'animdl.core.codebase.providers.animepahe',
 'animdl.core.codebase.providers.animepahe.inner',
 'animdl.core.codebase.providers.animexin',
 'animdl.core.codebase.providers.animixplay',
 'animdl.core.codebase.providers.animtime',
 'animdl.core.codebase.providers.crunchyroll',
 'animdl.core.codebase.providers.gogoanime',
 'animdl.core.codebase.providers.hahomoe',
 'animdl.core.codebase.providers.hentaistream',
 'animdl.core.codebase.providers.kamyroll',
 'animdl.core.codebase.providers.kawaiifu',
 'animdl.core.codebase.providers.nineanime',
 'animdl.core.codebase.providers.tenshimoe',
 'animdl.core.codebase.providers.twistmoe',
 'animdl.core.codebase.providers.yugen',
 'animdl.core.codebase.providers.zoro',
 'animdl.core.config']

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
{'console_scripts': ['animdl = animdl.__main__:__animdl_cli__']}

setup_kwargs = {
    'name': 'animdl',
    'version': '1.6.55',
    'description': 'A highly efficient, fast, powerful and light-weight anime downloader and streamer for your favorite anime.',
    'long_description': '',
    'author': 'justfoolingaround',
    'author_email': 'kr.justfoolingaround@gmail.com',
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
