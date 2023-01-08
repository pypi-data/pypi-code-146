# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cowpatch']

package_data = \
{'': ['*']}

install_requires = \
['CairoSVG>=2.5.2,<3.0.0',
 'ipython>=8.0.1,<9.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.21.4,<2.0.0',
 'plotnine>=0.10.0,<0.11.0',
 'svgutils>=0.3.4,<0.4.0']

setup_kwargs = {
    'name': 'cowpatch',
    'version': '0.1.2',
    'description': 'A package for combining python ggplot visuals',
    'long_description': '# cowpatch\n\n\n[![test and codecov](https://github.com/benjaminleroy/cowpatch/actions/workflows/ci.yml/badge.svg)](https://github.com/benjaminleroy/cowpatch/actions/workflows/ci.yml)\n[![codecov](https://codecov.io/gh/benjaminleroy/cowpatch/branch/main/graph/badge.svg?token=QM5G5WV7AE)](https://codecov.io/gh/benjaminleroy/cowpatch)\n[![CodeFactor](https://www.codefactor.io/repository/github/benjaminleroy/cowpatch/badge)](https://www.codefactor.io/repository/github/benjaminleroy/cowpatch)\n\nA package for combining/aranging multiple python ggplot visuals from [`plotnine`](https://plotnine.readthedocs.io/en/stable/)<!--, with allowances to also combined figures from [`matplotlib`](https://matplotlib.org/) and [`seaborn`](https://seaborn.pydata.org/)-->. Internally, we leverage SVG objects and descriptions to accomplish it\'s goals.\n\n<!--\n## Installation\n\nCurrently this project is under development and is not on\n[pypi](https://pypi.org/). As such, to install this package please do the\nfollowing:\n\n1. clone repository to your local computer (this assumes you have `git`\ninstalled):\n    ```bash\n    $ git clone https://github.com/benjaminleroy/cowpatch.git\n    ```\n2. install `poetry` if you don\'t have it already\n    ```bash\n    $ pip install poetry\n    ```\n3. then install the package (you need to be in the `cowpatch` root folder)\n    ```bash\n    $ poetry install\n    ```\n-->\n\n## Installation\n\nTo install the current version of this package, please run\n\n```\npip install cowpatch\n```\n\nIf you would like to experiment with the development version of this package\nplease following the guidelines in the contributing page.\n\n## Usage\n\n```python\nimport cowpatch as cow\nimport plotnine as p9\nimport plotnine.data as p9_data\nimport numpy as np\n```\n\n```python\n# creation of some some ggplot objects\ng0 = p9.ggplot(p9_data.mpg) +\\\n    p9.geom_bar(p9.aes(x="hwy")) +\\\n    p9.labs(title = \'Plot 0\')\n\ng1 = p9.ggplot(p9_data.mpg) +\\\n    p9.geom_point(p9.aes(x="hwy", y = "displ")) +\\\n    p9.labs(title = \'Plot 1\')\n\ng2 = p9.ggplot(p9_data.mpg) +\\\n    p9.geom_point(p9.aes(x="hwy", y = "displ", color="class")) +\\\n    p9.labs(title = \'Plot 2\')\n```\n\n```python\nvis_patch = cow.patch(g0,g1,g2)\nvis_patch += cow.layout(design = np.array([[0,1],\n                                           [0,2]]),\n                        rel_heights = [1,2])\nvis_patch.show(width = 11, height = 7)\n```\n<!--\n```python\nvis_patch.save(width=11, height=7, filename="images/readme.svg")\n```\n-->\n![cowpatch example](images/readme.svg)\n\nPlease see additional documentation pages like "Getting-Started" and the\nindividual pages on different plot arrangement strategies.\n\n## Future Goals\n\nThis package is currently in development (please feel welcome to contribute, with code, examples, issues, publicity, etc.). We envision a sequence of versions coming out with different added features in each. The order of the features will look something like the following\n\n- [x] MVP #1: base implimentation (reflecting `cowplot` and `gridExtra` functionality, minus labeling and titles)\n- [ ] MVP #2: figure labeling and titles and `cow.text()` objects\n- [ ] MVP #3: "Arithmetic of arrangement" (reflecting `patchwork`)\n\nIn addition, we envision the following features coming along in parallel:\n\n- [ ] inseting plots (like seen in `cowplot`)\n- [ ] wrapping of `matplotlib`, `plotnine` and `seaborn` plots to work within the `cowpatch` framework and within the `patchwork` framework\n- [ ] more complex drawing tools like the `R` package `grid` to allow for easy creation of complex features\n\nFor the interested reader, a lot of these ideas have been sketched in our `notes/` folder as "proof of concepts".\n\n## Package Logistics\n\n### Background and history\n\nThis package\'s name is a merging of the names of `R` packages\' `cowplot` and `patchwork`. It attempts to provide similar plot arrangement and combination tools as `gridExtra`, `cowplot` and `patchwork` for the `plotnine`\'s `ggplot` objects.\n\nThis package is not directly related to any of aforementioned packages (including the [Wilke Lab](https://wilkelab.org/), lead by Claus O. Wilke) but naturally stands on the shoulders of the contributions each of the packages made.\n\nThis package leverages a SVG backend to create the arangements. This may make the actual package a bit more "hacky" then some may like, but we hope it can still be of use to the community.\n\n\n### Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n### License\n\n`cowpatch` was created by [Benjamin LeRoy](https://benjaminleroy.github.io/) ([benjaminleroy](https://github.com/benjaminleroy)) and Mallory Wang ([wangmallory](https://github.com/wangmallory)). It is licensed under the terms of the MIT license.\n\n### Credits\n\nThis `python` package stands on the shoulders of many open-source tools, `cowpatch` structure was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter), the documentation leverages [`sphinx`](https://www.sphinx-doc.org/en/master/), and underlying testing leverages [`pytest`](https://docs.pytest.org/en/7.0.x/), [`hypothesis`](https://hypothesis.readthedocs.io/en/latest/) and [`pytest-regression`](https://pytest-regressions.readthedocs.io/en/latest/overview.html). See the full list of package dependencies on [Github](https://github.com/benjaminleroy/cowpatch/blob/main/pyproject.toml).\n\n',
    'author': 'Benjamin LeRoy',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://benjaminleroy.github.io/cowpatch/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
