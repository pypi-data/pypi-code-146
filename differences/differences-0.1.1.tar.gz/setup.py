# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['differences',
 'differences.attgt',
 'differences.datasets',
 'differences.did',
 'differences.tests',
 'differences.tools',
 'differences.tools.feols',
 'differences.twfe']

package_data = \
{'': ['*']}

install_requires = \
['formulaic>=0.3.4,<0.4.0',
 'joblib>=1.2.0,<2.0.0',
 'linearmodels>=4.25',
 'numpy>=1.16',
 'pandas>=1.2',
 'plotto>=0.1.3,<0.2.0',
 'pyhdfe>=0.1.2,<0.2.0',
 'scikit-learn>=1.0.2',
 'scipy>=1.7.3',
 'statsmodels>=0.13,<1.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'differences',
    'version': '0.1.1',
    'description': 'difference-in-differences estimation and inference in Python',
    'long_description': '<img src="./doc/source/images/logo/bw/logo_name_bw.png" alt="drawing" width="200" \nstyle="display: block;margin-left: auto;margin-right: auto;width: 80%;"/>\n\ndifference-in-differences estimation and inference for Python\n\n**For the following use cases**\n\n- Balanced panels, unbalanced panels & repeated cross-section\n- Two + Multiple time periods\n- Fixed + Staggered treatment timing\n- Binary + Multi-Valued treatment\n- Heterogeneous treatment effects & triple difference\n- One + Multiple treatments per entity\n\nsee the [Documentation](https://differences.readthedocs.io/en/latest/) for more details.\n\n## Installing\n\nThe latest release can be installed using pip\n\n```bash\npip install differences\n```\n\nrequires Python 3.8+\n\n## Quick Start\n\n### ATTgt \n\nthe ATTgt class implements the estimation procedures suggested by [Callaway and Sant\'Anna (2021)\n](https://www.sciencedirect.com/science/article/abs/pii/S0304407620303948), [Sant\'Anna and Zhao \n(2020)](https://www.sciencedirect.com/science/article/abs/pii/S0304407620301901) and the \nmulti-valued treatement case discussed in [Callaway, Goodman-Bacon & Sant\'Anna (2021)](https://arxiv.org/abs/2107.02637)\n\n```python\nfrom differences import ATTgt, simulate_data\n\ndf = simulate_data()\n\natt_gt = ATTgt(data=df, cohort_name=\'cohort\')\n\natt_gt.fit(formula=\'y\')\n\natt_gt.aggregate(\'event\')\n```\n\n*differences* ATTgt benefitted substantially from the original authors\' R packages: Callaway & Sant\'Anna\'s [did](https://github.com/bcallaway11/did) and Sant\'Anna and \nZhao\'s [DRDID](https://github.com/pedrohcgs/DRDID)\n\n### TWFE\n\n```python\nfrom differences import TWFE, simulate_data\n\ndf = simulate_data()\n\natt_gt = TWFE(data=df, cohort_name=\'cohort\')\n\natt_gt.fit(formula=\'y\')\n```\n',
    'author': 'Bernardo Dionisi',
    'author_email': 'bernardo.dionisi@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bernardodionisi/differences',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0.0',
}


setup(**setup_kwargs)
