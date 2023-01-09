# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['femwell', 'femwell.examples', 'femwell.mesh', 'femwell.tests']

package_data = \
{'': ['*']}

install_requires = \
['gmsh', 'matplotlib', 'pygmsh', 'scikit-fem>=8.0.0', 'shapely>=2.0.0']

setup_kwargs = {
    'name': 'femwell',
    'version': '0.0.4',
    'description': 'Mode solver for photonic and electric waveguides based on FEM',
    'long_description': "# Femwell\n\n[![Docs](https://github.com/helgegehring/femwell/actions/workflows/docs.yml/badge.svg)](https://HelgeGehring.github.io/femwell/)\n[![Build](https://github.com/helgegehring/femwell/actions/workflows/build.yml/badge.svg)](https://github.com/HelgeGehring/femwell/actions/workflows/build.yml)\n[![PiPy](https://img.shields.io/pypi/v/femwell)](https://pypi.org/project/femwell/)\n[![Downloads](https://static.pepy.tech/badge/femwell/month)](https://pepy.tech/project/femwell)\n\nWorking on a finite element based simulation tool for integrated circuits, electric and photonic!\nThe documentation is lagging behind the state of code, so there's several features for which there are only examples in the code.\n\n**You can try out the examples in the browser! Hover the rocket at the top on the example pages and click live code!**\n(Might take some time to load)\n\n# Working Features\n- Photonic eigenmode solver\n- Electric eigenmode solver\n- Thermal mode solver (static and transient)\n- Coulomb solver\n\n# Possible Simulations\n- Eigenmodes of waveguides and determining their effective refractive index\n- Eigenmodes of electric transmission lines and determining their propagation constant (in work)\n- Static thermal profiles\n- Transient thermal behavior\n- Static electric fields\n- Overlap integrals between waveguide modes\n- Overlap integral between a waveguide mode and a fiber mode\n- Coupled mode theory - coupling between adjacent waveguides\n- Heat based photonic phase shifters\n- Pockels based photonic phase shifters\n\n# Contributors\n- Helge Gehring (Google): Maintainer\n- Simon Bilodeau (Google): Meshes everything\n- Joaquin Matres (Google): Code simplifications\n\nHappy about every form of contribution - pull requests, feature requests, issues, questions, ... :)\n",
    'author': 'Helge Gehring',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/HelgeGehring/femwell',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
