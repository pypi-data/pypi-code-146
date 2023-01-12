# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['simple_export', 'simple_export.utils']

package_data = \
{'': ['*'],
 'simple_export': ['.idea/*', '.idea/inspectionProfiles/*', 'template/*']}

install_requires = \
['openpyxl>=3.0.10,<4.0.0']

setup_kwargs = {
    'name': 'simple-export',
    'version': '0.1.5',
    'description': '简单的模板导出工具',
    'long_description': '# simple_export\n\nsimple_export是一款导出工具包，目标是根据模板快速导出\n[simple_export](https://github.com/mtl940610/simple_export/)\n\n',
    'author': 'mtl',
    'author_email': '576694002@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
