# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sc_vortex_2d',
 'sc_vortex_2d.data_vortex',
 'sc_vortex_2d.data_vortex.temperature_03',
 'sc_vortex_2d.data_vortex.temperature_05',
 'sc_vortex_2d.data_vortex.temperature_08']

package_data = \
{'': ['*']}

install_requires = \
['scipy>=1.9.3,<2.0.0']

setup_kwargs = {
    'name': 'sc-vortex-2d',
    'version': '1.0.1',
    'description': 'Numerical result of CdGM mode.',
    'long_description': '# sc-vortex-2d\nThis library provide numerical results of s-wave Caroli-de Gennes-Matricon mode (CdGM mode) at \n$T/T_c=0.3, 0.5, 0.8$.\nYou can get the eigenenergy, eigenfunction and pair potential at each temperature.\n\n## Description\nIt is known that there are low-energy excitation levels inside the s-wave vortex core in the superconductor.\nThese states are got by solving following Bogoliubov-de Gennes equation(BdG eq) self-consistently.\n\n$$\n\\left[-\\frac{1}{2k_{F}\\xi_{0}}\\nabla^{2}-\\mu\\right]\\mathcal{U}_{q}(\\boldsymbol{r})+\\Delta(\\boldsymbol{r})\\mathcal{V}_{q}(\\boldsymbol{r}) = E_{q}\\mathcal{U}_{q}(\\boldsymbol{r}) \n$$\n\n$$\n\\left[\\frac{1}{2k_{F}\\xi_{0}}\\nabla^{2}+\\mu\\right]\\mathcal{V}_{q}(\\boldsymbol{r})+\\Delta^{*}(\\boldsymbol{r})\\mathcal{U}_{q}(\\boldsymbol{r}) = E_{q}\\mathcal{V}_{q}(\\boldsymbol{r})  \n$$\n\n$$\n\\Delta(\\boldsymbol{r})=g\\sum_{E_{q}\\leq E_{\\mathrm{c}}} \\mathcal{U}_{q}(r)\\mathcal{V}_{q}^{*}(r)[1-2f(E_{q})] \n$$\n\nHere, BdG eq is rewritten in dimensionless form using Pippard length $\\xi_{0} = \\hbar v_{F}/\\Delta_{0}$ and zero-temperature bulk gap $\\Delta_{0}$.\n$f(E_{q})$ is Fermi distribution function. Solutions in an isolated vortex, especially CdGM mode is given by following form.\n\n$$\n\\begin{bmatrix}\n\\mathcal{U}_{n}(r, \\theta) \\\\\n\\mathcal{V}_{n}(r, \\theta)\n\\end{bmatrix}\n=\\frac{1}{\\sqrt{2\\pi}}\n\\begin{bmatrix}\nu_{n}(r)e^{in\\theta} \\\\\nv_{n}(r)e^{i(n + 1)\\theta}\n\\end{bmatrix}\n$$\n\n\nHere, $n$ corresponds to angular momentum quantum number, i.e. CdGM mode is characterized by this number. In this library, the range of $n$ is integers of in $[-70, 69]$. Note that the part of $u_{n}(r), v_{n}(r)$ in the right side of above formula is one of the target of this library, not the left side of it.\n\n## Install\nYou can install via [PyPI](https://pypi.org/). For example,\n\n```\n $ pip install  sc-vortex-2d \n```\n\n## Usage\n```python\n"""Sample python code"""\n\nfrom sc_vortex_2d.vortex import VortexInstanceT03\nfrom scipy import interpolate\n\ninstance: VortexInstanceT03 = VortexInstanceT03()\n\ndelta: interpolate.CubicSpline = instance.get_pair_potential() \n\ne0: float = instance.get_ith_eigen_energy(0) # lowest energy level in the region of e > 0.\n\nu0, v0 = instance.get_ith_eigen_func(0) # get wave functions\n\nparams = instance.Parameters # Parameters of the system. Enum.\n\n```\n## Links\nhttps://webpark1378.sakura.ne.jp/\n',
    'author': 'Shun Makino',
    'author_email': 'shunmakino6211@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ShuN6211/sc-vortex-2d',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
