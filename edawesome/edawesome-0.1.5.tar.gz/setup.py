# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edawesome']

package_data = \
{'': ['*'], 'edawesome': ['html/edawesome/*']}

install_requires = \
['ipython>=8.5.0,<9.0.0',
 'kaggle>=1.5.12,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'patool>=1.12,<2.0',
 'pyspark>=3.3.1,<4.0.0',
 'scikit-learn>=1.2.0',
 'scipy>=1.8.0,<1.9.0',
 'seaborn>=0.12.1,<0.13.0',
 'statsmodels>=0.13.5,<0.14.0',
 'transitions>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'edawesome',
    'version': '0.1.5',
    'description': 'Quick, easy and customizable data analysis with pandas and seaborn',
    'long_description': '# EDAwesome\n\nThis is a package for quick, easy and customizable data analysis with pandas and seaborn. We automate all the routine so you can focus on the data. Clear and cuztomizable workflow is proposed.\n\n## Installation\n\nEDAwesome is generally compatible with standard Anaconda environment in therms of dependencies. So, you can just install it in you environment with pip:\n\n```bash\npip install edawesome\n```\n\nYou can also install the dependencies, using `requirements.txt`:\n\n```bash\npip install -r requirements.txt\n```\n\nIf you use Poetry, just include the depedencies in your `pyproject.toml`:\n\n```toml\n[tool.poetry.dependencies]\npython = ">=3.8,<3.11"\nseaborn = "^0.12.1"\nkaggle = "^1.5.12"\nipython = "^8.5.0"\ntransitions = "^0.9.0"\npatool = "^1.12"\npyspark = "^3.3.1"\npandas = "^1.5.2"\nstatsmodels = "^0.13.5"\nscikit-learn = ">=1.2.0"\nscipy = "~1.8.0"\n```\n\n## Usage\n\nThis package is designed to be used in Jupyter Notebook. You can use step-by-step workflow or just import the functions you need. Below is the example of the step-by-step workflow:\n\n### Quick start\n\n```python\nfrom edawesome.eda import EDA\n\neda = EDA(\n    data_dir_path=\'/home/dreamtim/Desktop/Coding/turing-ds/MachineLearning/tiryko-ML1.4/data\',\n    archives=[\'/home/dreamtim//Downloads/home-credit-default-risk.zip\'],\n    use_pyspark=True,\n    pandas_mem_limit=1024**2,\n    pyspark_mem_limit=\'4g\'   \n)\n```\n\nThis will create the `EDA` object. Now you can load the data into your EDA:\n\n```python\neda.load_data()\n```\n\nThis will display the dataframes and their shapes. You can also use `eda.dataframes` to see the dataframes. Now you can go to the next step:\n\n```python\neda.next()\neda.clean_check()\n```\n\nLet us say, that we don\'t want to do any cleaning in this case. So, we just go to the next step:\n\n```python\neda.next()\neda.categorize()\n```\n\nNow you can compare some numerical column by category just in one line:\n\n```python\neda.compare_distributions(\'application_train\', \'ext_source_3\', \'target\')\n```\n\n### Real-world example\n\nFull notebook which was used for examples above can be found in one of my real ML projects.\n\nThere is also an example `quickstart.ipynb` notebook in this repo.\n\n### Documentation\n\nYou can find the documentation [here](https://timofeiryko.github.io/edawesome).\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.',
    'author': 'Timofei Ryko',
    'author_email': 'timofei.ryko@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
