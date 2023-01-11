# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fractal', 'fractal.cmd', 'fractal.common', 'fractal.common.schemas']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.4.0,<3.0.0',
 'httpx>=0.23.0,<0.24.0',
 'pydantic>=1.10.1,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'rich>=12.5.1,<13.0.0',
 'sqlmodel>=0.0.8,<0.0.9']

entry_points = \
{'console_scripts': ['fractal = fractal.__main__:run',
                     'fractal_new = fractal.new:run',
                     'fractal_old = fractal.old:run']}

setup_kwargs = {
    'name': 'fractal-client',
    'version': '1.0.0rc1',
    'description': 'Client component of the Fractal analytics platform',
    'long_description': '# Fractal Client\n\n[![PyPI version](https://img.shields.io/pypi/v/fractal-client?color=gree)](https://pypi.org/project/fractal-client/)\n[![CI Status](https://github.com/fractal-analytics-platform/fractal/actions/workflows/ci.yml/badge.svg)](https://github.com/fractal-analytics-platform/fractal/actions/workflows/ci.yml)\n[![Documentation Status](https://github.com/fractal-analytics-platform/fractal/actions/workflows/documentation.yaml/badge.svg)](https://fractal-analytics-platform.github.io/fractal)\n[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)\n\nFractal is a framework to process high-content imaging data at scale and prepare it for interactive visualization.\n\n![Fractal_Overview](https://fractal-analytics-platform.github.io/assets/fractal_overview.jpg)\n\nFractal provides distributed workflows that convert TBs of image data into OME-Zarr files. The platform then processes the 3D image data by applying tasks like illumination correction, maximum intensity projection, 3D segmentation using [cellpose](https://cellpose.readthedocs.io/en/latest/) and measurements using [napari workflows](https://github.com/haesleinhuepf/napari-workflows). The pyramidal OME-Zarr files enable interactive visualization in the napari viewer.\n\nThis is the repository that contains the **Fractal client**. Find more information about Fractal in general and the other repositories at the [Fractal home page](https://fractal-analytics-platform.github.io).\n\n## Documentation\n\nSee https://fractal-analytics-platform.github.io/fractal.\n\n# Contributors and license\n\nUnless otherwise stated in each individual module, all Fractal components are released according to a BSD 3-Clause License, and Copyright is with Friedrich Miescher Institute for Biomedical Research and University of Zurich.\n\nFractal was conceived in the Liberali Lab at the Friedrich Miescher Institute for Biomedical Research and in the Pelkmans Lab at the University of Zurich (both in Switzerland). The project lead is with [@gusqgm](https://github.com/gusqgm) & [@jluethi](https://github.com/jluethi). The core development is done under contract by [@mfranzon](https://github.com/mfranzon), [@tcompa](https://github.com/tcompa) & [@jacopo-exact](https://github.com/jacopo-exact) from [eXact lab S.r.l.](exact-lab.it).\n',
    'author': 'Tommaso Comparin',
    'author_email': 'tommaso.comparin@exact-lab.it',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fractal-analytics-platform/fractal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
