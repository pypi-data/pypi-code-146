# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['devoud', 'devoud.lib']

package_data = \
{'': ['*'],
 'devoud': ['data/*', 'ui/fonts/*', 'ui/png/*', 'ui/svg/*', 'ui/themes/*']}

install_requires = \
['PySide6>=6.4.1,<7.0.0', 'adblockparser>=0.7,<0.8', 'requests>=2.9.2,<3.0.0']

entry_points = \
{'console_scripts': ['devoud = devoud.Devoud:main']}

setup_kwargs = {
    'name': 'devoud',
    'version': '1.0b12',
    'description': 'A simple web browser written in Python using PySide6',
    'long_description': '<h1 align="center">Devoud</h1>\n\n<h3 align="center">Простой веб-браузер написанный на Python с использованием PySide6</h3>\n\n![icon](./screenshot.png)\n![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)\n![Qt](https://img.shields.io/badge/Qt-%23217346.svg?style=for-the-badge&logo=Qt&logoColor=white)\n![Arch](https://img.shields.io/badge/Arch%20Linux-1793D1?logo=arch-linux&logoColor=fff&style=for-the-badge)\n![Debian](https://img.shields.io/badge/Debian-D70A53?style=for-the-badge&logo=debian&logoColor=white)\n![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)\n## Установка\n* Проверить установленный Python3 и pip3\n* Скачать архив с программой\n* Запустить Devoud.py\n* Подтвердить скачивание модулей\n## Вопросы\n* О всех найденных ошибках и предложениях по улучшению программы сообщайте во вкладке [Задачи](https://codeberg.org/OneEyedDancer/Devoud/issues)\n## Лицензия\n[![GPLv3](https://www.gnu.org/graphics/gplv3-with-text-136x68.png)](https://www.gnu.org/licenses/gpl-3.0)',
    'author': 'OneEyedDancer',
    'author_email': 'ooeyd@ya.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://codeberg.org/OneEyedDancer/Devoud',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
