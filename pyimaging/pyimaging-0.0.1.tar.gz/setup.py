# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['imaging']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['imaging = src.imaging.main:app']}

setup_kwargs = {
    'name': 'pyimaging',
    'version': '0.0.1',
    'description': '轻量级 Python 图像处理库',
    'long_description': '# imaging\n\n> 轻量级 Python 图像处理库\n\n',
    'author': 'yiyun',
    'author_email': 'yiyungent@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/yiyungent/imaging',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
