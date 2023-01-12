# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['computerender']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0', 'click>=8.0.1']

entry_points = \
{'console_scripts': ['computerender = computerender.__main__:main']}

setup_kwargs = {
    'name': 'computerender',
    'version': '0.1.4',
    'description': 'Computerender',
    'long_description': '# Computerender Python Client\n\n[![PyPI](https://img.shields.io/pypi/v/computerender.svg)][pypi status]\n[![Python Version](https://img.shields.io/pypi/pyversions/computerender)][pypi status]\n![License](https://img.shields.io/pypi/l/computerender)\n\n[![Tests](https://github.com/computerender/computerender-python/workflows/Tests/badge.svg)][tests]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi status]: https://pypi.org/project/computerender/\n[tests]: https://github.com/computerender/computerender-python/actions?workflow=Tests\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\nPython client for using the computerender API.\n\n## Updates\n\n- v0.1: Improved Error handling\n- v0.0: Img2img!\n\n## Installation\n\n```console\n$ pip install computerender\n```\n\n## Examples\n\n```python\n\nfrom computerender import Computerender\nimport asyncio\n\ncr = Computerender()\n\n# Generate image and save to file\nwith open("cow.jpg", "wb") as f:\n    img_bytes = asyncio.run(cr.generate("a cow wearing sunglasses"))\n    f.write(img_bytes)\n\n# Generate image with custom parameters\nimg_bytes = asyncio.run(cr.generate("testing", w=1024, h=384, iterations=20))\n\n# img2img generation reading from and writing to files\nwith open("cow.jpg", "rb") as in_f:\n    img_bytes = asyncio.run(\n        cr.generate(\n            "van gogh painting of a cow wearing sunglasses",\n            img=in_f.read()\n        )\n    )\nwith open("van_gogh_cow.jpg", "wb") as out_f:\n    out_f.write(img_bytes)\n\n# img2img one-liner reading and writing to file\nopen("fly.jpg", "wb").write(asyncio.run(cr.generate("fly", img=open("cow.jpg", "rb").read())))\n\n# Generate image and use it for img2img without saving anything to files\nimg_bytes = asyncio.run(\n    cr.generate("testing", w=1024, h=384, iterations=20)\n)\nresult_bytes = asyncio.run(\n    cr.generate("testing style transfer", img=img_bytes)\n)\n```\n\n"a cow wearing sunglasses"\n<img src="https://i.imgur.com/nhEQtQo.jpg"\nalt="a cow wearing sunglasses" width="256"/>\n\n"van gogh painting of a cow wearing sunglasses"\n<img src="https://i.imgur.com/0qV4YB2.jpg"\nalt="van gogh painting of a cow wearing sunglasses" width="256"/>\n\n## License\n\nDistributed under the terms of the [MIT license][license]\n',
    'author': 'computerender',
    'author_email': 'peter@computerender.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/computerender/computerender-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
