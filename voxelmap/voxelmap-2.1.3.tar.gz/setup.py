# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['voxelmap']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'opencv-python>=4.7.0.68,<5.0.0.0',
 'pandas>=1.5.2,<2.0.0',
 'pygame>=2.1.2,<3.0.0',
 'pyopengl>=3.1.6,<4.0.0',
 'pytest>=7.2.0,<8.0.0',
 'scipy>=1.10.0,<2.0.0']

setup_kwargs = {
    'name': 'voxelmap',
    'version': '2.1.3',
    'description': 'A Python library for making voxel and 3D models from NumPy arrays.',
    'long_description': '# voxelmap\n\nA Python library for making voxel and three-dimensional models from NumPy arrays.\n\n<!-- <center><a href="https://andrewatcloud.com/voxelmap/"><img src="https://github.com/andrewrgarcia/voxelmap/blob/main/extra/voxeldog.png?raw=true" width="450"></a></center> -->\n\n<center><a href="https://andrewatcloud.com/voxelmap/"><img src="https://github.com/andrewrgarcia/voxelmap/blob/main/extra/land_ImageMesh.png?raw=true" width="800"></a></center>\n\n## Installation\n\n```ruby\npip install voxelmap\npip install --upgrade voxelmap\n```\n\n## Just starting? Check out the Colab notebook (click on below icon)\n\n<a href="https://colab.research.google.com/drive/1RMEMgZHlk_tKAzfS4QfXLJV9joDgdh8N?usp=sharing">\n<img src="https://github.com/andrewrgarcia/powerxrd/blob/main/img/colab.png?raw=true" width="300" ></a>\n\n\n## Contributing / Hacktoberfest\n\nMeaningful contributions to the project are always welcome. This project is also active as a part of Hacktoberfest 2022. Before making a PR, please make sure to read the [CONTRIBUTING](./CONTRIBUTING.md) document.\n\nYou may use the Issues section of this repository if you\'d like to propose some new ideas/enhancements or report a bug.\n\n\n## Disclaimer: Use At Your Own Risk\n\nThis program is free software. It comes without any warranty, to the extent permitted by applicable law. You can redistribute it and/or modify it under the terms of the MIT LICENSE, as published by Andrew Garcia. See LICENSE below for more details.\n\n[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)\n\n**[MIT license](./LICENSE)** Copyright 2022 © <a href="https://github.com/andrewrgarcia" target="_blank">Andrew Garcia</a>.\n',
    'author': 'andrewrgarcia',
    'author_email': 'garcia.gtr@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
