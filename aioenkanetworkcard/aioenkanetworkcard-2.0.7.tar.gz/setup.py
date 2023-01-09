# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioenkanetworkcard', 'aioenkanetworkcard.src.utils']

package_data = \
{'': ['*'],
 'aioenkanetworkcard': ['src/assets/*',
                        'src/assets/InfoCharter/*',
                        'src/assets/constant/*',
                        'src/assets/elementColor/*',
                        'src/assets/font/*',
                        'src/assets/icon/*',
                        'src/assets/stars/*',
                        'src/assets/teapmleOne/artifact/*',
                        'src/assets/teapmleOne/background/*',
                        'src/assets/teapmleOne/charterInfo/*',
                        'src/assets/teapmleOne/maska/*',
                        'src/assets/teapmleOne/stats/*',
                        'src/assets/teapmleOne/talants/*',
                        'src/assets/teapmleOne/weapons/*',
                        'src/assets/teapmleTree/artifact/*',
                        'src/assets/teapmleTree/background/*',
                        'src/assets/teapmleTree/constant/closed/*',
                        'src/assets/teapmleTree/constant/open/*',
                        'src/assets/teapmleTree/maska/*',
                        'src/assets/teapmleTree/name/*',
                        'src/assets/teapmleTree/talants/*',
                        'src/assets/teapmleTree/weapon/*',
                        'src/assets/teapmleTwo/artifact/*',
                        'src/assets/teapmleTwo/background/*',
                        'src/assets/teapmleTwo/charterInfo/*',
                        'src/assets/teapmleTwo/charter_element/*',
                        'src/assets/teapmleTwo/infoUser/*',
                        'src/assets/teapmleTwo/maska/*',
                        'src/assets/teapmleTwo/stats/*',
                        'src/assets/teapmleTwo/talants/*',
                        'src/assets/teapmleTwo/weapon/*']}

install_requires = \
['Pillow>=9.3.0,<10.0.0',
 'asyncache>=0.3.1,<0.4.0',
 'cachetools>=5.2.0,<6.0.0',
 'enkanetwork.py>=1.3.3,<2.0.0']

setup_kwargs = {
    'name': 'aioenkanetworkcard',
    'version': '2.0.7',
    'description': 'Wrapper module for enkanetwork.py for creating character cards.',
    'long_description': '<p align="center">\n  <img src="https://raw.githubusercontent.com/DEViantUA/EnkaNetworkCard/main/img/banner.jpg" alt="Баннер"/>\n</p>\n\n**<p align="center"> <a href="https://github.com/DEViantUA/EnkaNetworkCard">GitHub</a> | <a href="https://github.com/DEViantUA/EnkaNetworkCard/tree/main/Example">Example</a> | <a href = "https://discord.gg/SJ3d9x4e"> Discord <a> | <a href = "https://deviantua.github.io/EnkaNetworkCard-Documentation/"> Documentation <a> </p>**\n\n# EnkaNetworkCard\nWrapper for [EnkaNetwork.py](https://github.com/mrwan200/EnkaNetwork.py) to create character cards in Python.\n\n## Installation:\n\n```\npip install aioenkanetworkcard\n```\n### Dependencies:\n  Dependencies that must be installed for the library to work:\n  * Pillow\n  * requests\n  * io\n  * math\n  * threading\n  * datetime\n  * random\n  * enkanetwork.py\n  * logging\n\n\n## Sample Results:\n\n### The result of a custom images and adaptation (template= 1).\n<img src="https://raw.githubusercontent.com/DEViantUA/EnkaNetworkCard/main/img/Example1.png" width=\'300\' alt="Example1"/> <img src="https://raw.githubusercontent.com/DEViantUA/EnkaNetworkCard/main/img/Example2.png" width=\'300\' alt="Example2"/> \n\n### Usual result (template= 1).\n<img src="https://raw.githubusercontent.com/DEViantUA/EnkaNetworkCard/main/img/Example3.png" width=\'300\' alt="Example3"/> <img src="https://raw.githubusercontent.com/DEViantUA/EnkaNetworkCard/main/img/Example4.png" width=\'300\' alt="Example4"/> \n\n### The result of a custom images and adaptation (template= 2).\n<img src="https://raw.githubusercontent.com/DEViantUA/EnkaNetworkCard/main/img/Example5.png.png" width=\'300\' alt="namecard = True"/> <img src="https://raw.githubusercontent.com/DEViantUA/EnkaNetworkCard/main/img/Example6.png.png" width=\'300\' alt="namecard = False"/> \n\n### Usual result (template= 2).\n<img src="https://raw.githubusercontent.com/DEViantUA/EnkaNetworkCard/main/img/Example8.png.png" width=\'300\' alt="namecard = True"/> <img src="https://raw.githubusercontent.com/DEViantUA/EnkaNetworkCard/main/img/Example7.png.png" width=\'300\' alt="namecard = False"/> ',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/DEViantUA/EnkaNetworkCard/wiki/Dokumentation-enkanetworkcard',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
