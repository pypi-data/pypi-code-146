# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zodipy']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=5.0.1',
 'healpy>=1.15.0,<2.0.0',
 'jplephem>=2.17,<3.0',
 'numpy>=1.22.3,<2.0.0']

setup_kwargs = {
    'name': 'zodipy',
    'version': '0.8.3',
    'description': 'Software for simulating zodiacal emission',
    'long_description': '\n<img src="docs/img/zodipy_logo.png" width="350">\n\n[![PyPI version](https://badge.fury.io/py/zodipy.svg)](https://badge.fury.io/py/zodipy)\n[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)\n![Tests](https://github.com/MetinSa/zodipy/actions/workflows/tests.yml/badge.svg)\n[![codecov](https://codecov.io/gh/Cosmoglobe/zodipy/branch/main/graph/badge.svg?token=VZP9L79EUJ)](https://codecov.io/gh/Cosmoglobe/zodipy)\n[![arXiv Paper](https://img.shields.io/badge/arXiv-2205.12962-green)](https://arxiv.org/abs/2205.12962)\n---\n\n\nZodiPy is a Python tool for simulating the zodiacal emission in intensity that an arbitrary Solar System observer sees, either in the form of timestreams or full-sky HEALPix maps.\n\n![plot](docs/img/zodipy_map.png)\n\n# Help\nSee the [documentation](https://cosmoglobe.github.io/zodipy/) for more information and examples on how to use ZodiPy for different applications.\n\n# Installation\nZodiPy is installed using `pip install zodipy`.\n\n# A simple example\n```python\nimport astropy.units as u\nfrom astropy.time import Time\n\nfrom zodipy import Zodipy\n\n\nmodel = Zodipy("dirbe")\n\nemission = model.get_emission_ang(\n    25 * u.micron,\n    theta=[10, 10.1, 10.2] * u.deg,\n    phi=[90, 89, 88] * u.deg,\n    obs_time=Time("2022-01-01 12:00:00"),\n    obs="earth",\n)\n\nprint(emission)\n#> [15.35392831 15.35495051 15.35616009] MJy / sr\n```\n\n# Scientific paper and citation\nFor an overview of the ZodiPy model approach and other information regarding zodiacal emission and interplanetary dust modeling we refer to the scientific paper on ZodiPy:\n- [Cosmoglobe: Simulating zodiacal emission with ZodiPy (San et al. 2022)](https://arxiv.org/abs/2205.12962). \n\nSee [CITATION](https://github.com/Cosmoglobe/zodipy/blob/dev/CITATION.bib) if you have used ZodiPy in your work and want to cite the software.\n\n# Funding\nThis work has received funding from the European Union\'s Horizon 2020 research and innovation programme under grant agreements No 776282 (COMPET-4; BeyondPlanck), 772253 (ERC; bits2cosmology) and 819478 (ERC; Cosmoglobe).\n\n\n<div style="display: flex; flex-direction: row; justify-content: space-evenly">\n    <img style="width: 49%; height: auto; max-width: 500px; align-self: center" src="https://user-images.githubusercontent.com/28634670/170697040-d5ec2935-29d0-4847-8999-9bc4eaa59e56.jpeg"> \n    &nbsp; \n    <img style="width: 49%; height: auto; max-width: 500px; align-self: center" src="https://user-images.githubusercontent.com/28634670/170697140-b010aa69-9f9a-44c0-b702-8a05ec0b6d3e.jpeg">\n</div>',
    'author': 'Metin San',
    'author_email': 'metinisan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Cosmoglobe/zodipy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
