# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['encord_active',
 'encord_active.app',
 'encord_active.app.actions_page',
 'encord_active.app.common',
 'encord_active.app.common.components',
 'encord_active.app.common.components.sticky',
 'encord_active.app.common.components.tags',
 'encord_active.app.conf',
 'encord_active.app.data_quality',
 'encord_active.app.data_quality.sub_pages',
 'encord_active.app.model_quality',
 'encord_active.app.model_quality.sub_pages',
 'encord_active.app.views',
 'encord_active.cli',
 'encord_active.cli.utils',
 'encord_active.lib',
 'encord_active.lib.charts',
 'encord_active.lib.coco',
 'encord_active.lib.common',
 'encord_active.lib.dataset',
 'encord_active.lib.db',
 'encord_active.lib.db.helpers',
 'encord_active.lib.embeddings',
 'encord_active.lib.encord',
 'encord_active.lib.metrics',
 'encord_active.lib.metrics.geometric',
 'encord_active.lib.metrics.heuristic',
 'encord_active.lib.metrics.semantic',
 'encord_active.lib.model_predictions',
 'encord_active.lib.project']

package_data = \
{'': ['*'], 'encord_active.app': ['assets/*', 'static/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'av>=9.2.0,<10.0.0',
 'encord>=0.1.43,<0.2.0',
 'faiss-cpu>=1.7.2,<2.0.0',
 'inquirer>=2.10.0,<3.0.0',
 'loguru>=0.6.0,<0.7.0',
 'matplotlib>=3.5.3,<4.0.0',
 'natsort>=8.1.0,<9.0.0',
 'numpy>=1.23.1,<2.0.0',
 'opencv-python==4.5.5.64',
 'pandas>=1.4.3,<2.0.0',
 'pandera>=0.13.4,<0.14.0',
 'plotly>=5.10.0,<6.0.0',
 'psutil>=5.9.4,<6.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'pytz>=2022.2.1,<2023.0.0',
 'rich>=12.6.0,<13.0.0',
 'scikit-learn>=1.0.1,<2.0.0',
 'scipy==1.8.1',
 'shapely>=1.7.0,<2.0.0',
 'streamlit-nested-layout>=0.1.1,<0.2.0',
 'streamlit==1.13.0',
 'termcolor>=2.0.1,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'torch>=1.12.1,<2.0.0',
 'torchvision>=0.13.1,<0.14.0',
 'typer>=0.6.1,<0.7.0',
 'types-pytz>=2022.2.1,<2023.0.0',
 'watchdog>=2.1.9,<3.0.0']

extras_require = \
{'coco': ['pycocotools>=2.0.6,<3.0.0'],
 'notebooks': ['jupyterlab>=3.5.2,<4.0.0', 'ipywidgets>=8.0.4,<9.0.0']}

entry_points = \
{'console_scripts': ['encord-active = encord_active.cli.main:cli']}

setup_kwargs = {
    'name': 'encord-active',
    'version': '0.1.19',
    'description': 'Enable users to improve machine learning models in an active learning fashion via data, label, and model quality.',
    'long_description': '<p align="center">\n<a href="https://encord-active-docs.web.app" target="_blank">Documentation</a> |\n<a href="https://colab.research.google.com/drive/11iZE1CCFIGlkWdTmhf5XACDojtGeIRGS?usp=sharing" target="_blank">Try it Now</a> |\n<a href="https://encord.com/encord_active/" target="_blank">Website</a> |\n<a href="https://encord.com/blog/" target="_blank">Blog</a> |\n<a href="https://join.slack.com/t/encordactive/shared_invite/zt-1hc2vqur9-Fzj1EEAHoqu91sZ0CX0A7Q" target="_blank">Slack Community</a>\n</p>\n\n<h1 align="center">\n  <p align="center">Encord Active</p>\n  <a href="https://encord.com"><img src="src/encord_active/app/assets/encord_2_02.png" width="150" alt="Encord logo"/></a>\n</h1>\n\n[![PRs-Welcome][contribute-image]][contribute-url]\n![Licence][license-image]\n[![PyPi project][pypi-package-image]][pypi-package]\n![PyPi version][pypi-version-image]\n[![Open In Colab][colab-image]][colab-notebook]\n\n[![docs][docs-image]][encord-active-docs]\n[!["Join us on Slack"][slack-image]][join-slack]\n[![Twitter Follow][twitter-image]][twitter-url]\n\n## ❓ What is Encord Active?\n\n[Encord Active][encord-active-landing] is an open-source active learning framework that helps you find failure modes in your models and improve your data quality and model performance.\n\nUse Encord Active to visualize your data, evaluate your models, surface model failure modes, find labeling mistakes, prioritize high-value data for re-labeling and more!\n\n![video](resources/ea-demo.gif)\n\n## 💡 When to use Encord Active?\n\nEncord Active helps you understand and improve your data, labels, and models at all stages of your computer vision journey.\nWhether you\'ve just started collecting data, labeled your first batch of samples, or have multiple models in production.\n\n![encord active diagram](resources/process-chart-ea.webp)\n\n## Installation\n\nThe simplest way to install the CLI is using `pip` in a suitable virtual environment:\n\n```shell\npip install encord-active\n```\n\nWe recommend using a virtual environment, such as `venv`:\n\n```shell\npython3.9 -m venv ea-venv\nsource ea-venv/bin/activate\npip install encord-active\n```\n\n> `encord-active` requires [python3.9][python-39].\n> If you have trouble installing `encord-active`, you find more detailed instructions on\n> installing it [here][encord-active-docs].\n\n## 👋 Quickstart\n\nGet started immediately by sourcing your environment and running the code below.\nThis downloads a small dataset and launches the Encord Active App for you to explore:\n\n```shell\nencord-active quickstart\n```\n\nAfter opening the UI, we recommend you to head to the [workflow documentation][encord-active-docs-workflow] to see some common workflows.\n\n## ⬇️\xa0 Downloading a pre-built project\n\nThe quickest way to get started is by downloading an existing dataset.\nThe download command will ask which pre-built dataset to use and will download it into a new directory in the current working directory.\n\n```shell\n$ encord-active download\n$ cd /path/of/downloaded/project\n$ encord-active visualise\n```\n\nThe app should then open in the browser.\nIf not, navigate to [`localhost:8501`](http://localhost:8501).\nOur [docs][encord-active-docs] contains more information about what you can see in the page.\n\n## <img width="24" height="24" src="resources/logo.png"/> Importing an Encord Project\n\nThis section requires [setting up an ssh key][encord-docs-ssh] with Encord, so slightly more technical.\n\n> If you haven\'t set up an ssh key with Encord, you can follow the tutorial in [this\xa0link][encord-docs-ssh].\n\nTo import an Encord project, use this command:\n\n`$ encord-active import project`\n\n> There are also options for importing projects from, e.g,. KITTI, CVAT, and COCO. Find more details in [the documentation][encord-active-docs-workflow-import-data].\n\n## ⭐ Concepts and features\n\n### 📊 Quality metric\n\nQuality metric are applied to your data, labels, and predictions to assign them quality metric scores.\nPlug in your own or rely on Encord Actives prebuilt quality metrics.\nThe quality metrics automatically decompose your data, label, and model quality to show you how to improve your model performance from a data-centric perspective.\nEncord Active ships with 25+ metrics and more are coming; [contributions][contribute-url] are also very welcome.\n\n**Other core features:**\n\n- [Model Decomposition](https://encord-active-docs.web.app/pages/model-quality/metrics)\n- [Data Exploration](https://encord-active-docs.web.app/pages/data-quality/summary)\n- [Similarity Search](https://encord-active-docs.web.app/workflows/Improve-your-data/similar-images)\n- [Annotator Benchmarks](https://encord-active-docs.web.app/pages/label-quality/explorer/)\n- [Data Tagging](https://encord-active-docs.web.app/workflows/tags/#steps)\n- [COCO Exports](https://encord-active-docs.web.app/pages/export/filter_export)\n- And much more!\n\nVisit our [documentation][encord-active-docs] to learn more.\n\n### Supported data:\n\n| Data   |     | Labels          |     | Project sizes |                |\n| ------ | --- | --------------- | --- | ------------- | -------------- |\n| `jpg`  | ✅  | Bounding Boxes  | ✅  | Images        | 100.000        |\n| `png`  | ✅  | Polygons        | ✅  | Videos        | 100.000 frames |\n| `tiff` | ✅  | Segmentation    | ✅  |               |                |\n| `mp4`  | ✅  | Classifications | 🟡  |               |                |\n|        |     | Polylines       | 🟡  |               |                |\n\n## 🧑🏽\u200d💻Development\n\n### 🛠 Build your own metrics\n\nEncord Active is built with customizability in mind. Therefore, you can easily build your own custom metrics\xa0🔧\xa0See the\xa0[Writing Your Own Metric][encord-active-docs-write-metric]\xa0page in the docs for details on this topic. If you need help or guidance feel free to ping us in the **[slack community](https://encordactive.slack.com)**!\n\n## 🔖 Documentation\n\nFind our\xa0documentation [here](https://encord-active-docs.web.app).\n\n## 👪 Community and support\n\nJoin our community on\xa0[Slack][join-slack]\xa0to connect with the team behind Encord Active.\n\nAlso, feel free to [suggest improvements or report problems][report-issue] via github issues.\n\n## 🎇 Contributions\n\nIf you\'re using Encord Active in your organization, please try to add your company name to the\xa0[ADOPTERS.md][adopters]. It really helps the project to gain momentum and credibility. It\'s a small contribution back to the project with a big impact.\n\nIf you want to share your custom metrics or improve the tool, please see our\xa0[contributing docs][contribute-url].\n\n### 🦸 Contributors\n\n<a href="https://github.com/encord-team/encord-active/graphs/contributors">\n  <img src="https://contrib.rocks/image?repo=encord-team/encord-active" />\n</a>\n\n[@Javi Leguina](https://github.com/jleguina)\n\n## Licence\n\nThis repository is published under the Apache 2.0 licence.\n\n[adopters]: https://github.com/encord-team/encord-active/blob/main/ADOPTERS.md\n[colab-notebook]: https://colab.research.google.com/drive/11iZE1CCFIGlkWdTmhf5XACDojtGeIRGS?usp=sharing\n[contribute-url]: https://encord-active-docs.web.app/contributing\n[encord-active-docs-workflow-import-data]: https://encord-active-docs.web.app/workflows/import-data\n[encord-active-docs-workflow]: https://encord-active-docs.web.app/category/workflows\n[encord-active-docs-write-metric]: https://encord-active-docs.web.app/metrics/write-your-own\n[encord-active-docs]: https://encord-active-docs.web.app/\n[encord-active-landing]: https://encord.com/encord-active/\n[encord-docs-ssh]: https://docs.encord.com/admins/settings/public-keys/#set-up-public-key-authentication\n[join-slack]: https://join.slack.com/t/encordactive/shared_invite/zt-1hc2vqur9-Fzj1EEAHoqu91sZ0CX0A7Q\n[new-issue]: https://github.com/encord-team/encord-active/issues/new\n[pypi-package]: https://www.piwheels.org/project/encord-active/\n[python-39]: https://www.python.org/downloads/release/python-3915/\n[report-issue]: https://github.com/encord-team/data-quality-pocs/issues/new\n[slack-community]: https://encord-active.slack.com\n[twitter-url]: https://twitter.com/encord_team\n[colab-image]: https://colab.research.google.com/assets/colab-badge.svg\n[contribute-image]: https://img.shields.io/badge/PRs-welcome-blue.svg\n[docs-image]: https://img.shields.io/badge/docs-online-blue\n[license-image]: https://img.shields.io/github/license/encord-team/encord-active\n[pypi-package-image]: https://img.shields.io/pypi/v/encord-active\n[pypi-version-image]: https://img.shields.io/pypi/pyversions/encord-active\n[slack-image]: https://img.shields.io/badge/Slack-4A154B?logo=slack&logoColor=white\n[twitter-image]: https://img.shields.io/twitter/follow/encord_team?label=%40encord_team&style=social\n',
    'author': 'Cord Technologies Limited',
    'author_email': 'hello@encord.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://encord.com/encord-active/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*, !=3.8.*',
}


setup(**setup_kwargs)
