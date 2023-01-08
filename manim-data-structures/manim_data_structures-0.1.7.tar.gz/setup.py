# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['manim_data_structures']

package_data = \
{'': ['*']}

install_requires = \
['manim>=0.16.0']

entry_points = \
{'manim.plugins': ['manim_data_structures = manim_data_structures']}

setup_kwargs = {
    'name': 'manim-data-structures',
    'version': '0.1.7',
    'description': 'A Manim implementation for data structures',
    'long_description': '<picture>\n    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/drageelr/manim-data-structures/main/docs/source/_static/logo-white-no-bg.svg">\n    <img alt="Light Mode Logo" src="https://raw.githubusercontent.com/drageelr/manim-data-structures/main/docs/source/_static/logo-color-no-bg.svg">\n</picture>\n<br />\n<br />\n<p align="center">\n    <a href="https://pypi.org/project/manim-data-structures/"><img src="https://img.shields.io/pypi/v/manim-data-structures.svg?style=plastic&logo=pypi" alt="PyPI Latest Release"></a>\n    <a href="http://choosealicense.com/licenses/mit/"><img src="https://img.shields.io/badge/license-MIT-red.svg?style=plastic" alt="MIT License"></a>\n    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=plastic" alt="Code style: black">\n    <a href="https://manim-data-structures.readthedocs.io/en/latest/"><img src="https://readthedocs.org/projects/manim-data-structures/badge/?version=latest&style=plastic" alt="Documentation Status"></a>\n    <a href="https://pepy.tech/project/manim-data-structures"><img src="https://pepy.tech/badge/manim-data-structures/month?style=plastic" alt="Downloads"> </a>\n    <a href=""><img src="https://github.com/drageelr/manim-data-structures/actions/workflows/publish-package.yml/badge.svg?style=plastic&branch=main"></a>\n    <br />\n    <br />\n    <i>A plugin that contains common data structures to create Manimations.</i>\n</p>\n\n## Installation\nTo install, simply run the following command:\n```\npip install manim-data-structures\n```\n\n## Importing\nSimply use the following line of code to import the package:\n```python\nfrom manim_data_structures import *\n```\n\n## Usage\n### Code\n```python\nclass MainScene(Scene):\n    def construct(self):\n        # Create an array\n        arr = MArray([8, 7, 6, 5, 4])\n        self.play(Create(arr))\n\n        # Animate array\n        self.play(arr.animate.shift(UP * 2.5 + LEFT * 5))\n\n        # Animate array element\n        self.play(arr.animate_elem(3).shift(DOWN * 0.5))\n\n        # Animate array element mobjects\n        self.play(arr.animate_elem_square(0).set_fill(BLACK), arr.animate_elem_value(0).rotate(PI / 2).set_fill(RED), arr.animate_elem_index(0).rotate(PI / 2))\n\n        # Display array with hex values\n        arr2 = MArray([0, 2, 4, 6, 8], index_hex_display=True, index_offset=4)\n        self.play(Create(arr2))\n        self.play(arr2.animate.shift(DOWN * 2.5 + LEFT * 5))\n\n        # Create customized array\n        arr3 = MArray([1, 1, 2], mob_square_args={\'color\': GRAY_A, \'fill_color\': RED_E, \'side_length\': 0.5}, mob_value_args={\'color\': GOLD_A, \'font_size\': 28}, mob_index_args={\'color\': RED_E, \'font_size\': 22})\n        self.play(Create(arr3))\n\n        # Append element\n        self.play(Write(arr2.append_elem(10)))\n\n        # Append customized element\n        self.play(Write(arr2.append_elem(12, mob_square_args={\'fill_color\': BLACK})))\n\n        # Update value of element\n        self.play(Write(arr2.update_elem_value(3, 0, mob_value_args={\'color\': RED})), arr2.animate_elem_square(3).set_fill(WHITE))\n\n        self.wait()\n```\n\n### Output\n\n\nhttps://user-images.githubusercontent.com/56049229/203757924-6f3aed6d-e870-468f-a269-a572350355b1.mp4\n\n\n## Other Links\n\n- [Official Documentation](https://manim-data-structures.readthedocs.io/en/latest/)\n- [Changelog](https://github.com/drageelr/manim-data-structures/blob/main/CHANGELOG.md)\n',
    'author': 'Hammad Nasir',
    'author_email': 'hammadn99@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/drageelr/manim-data-structures',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
