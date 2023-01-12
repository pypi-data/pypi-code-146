# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['insilicho']

package_data = \
{'': ['*']}

install_requires = \
['Pint>=0.19.2,<0.20.0',
 'PyYAML>=6.0,<7.0',
 'mypy>=0.991,<0.992',
 'numpy==1.23.5',
 'pandas>=1.5.0,<2.0.0',
 'scipy>1.7.0']

setup_kwargs = {
    'name': 'insilicho',
    'version': '1.1.1',
    'description': 'An insilico model for CHO cells',
    'long_description': '![tests](https://github.com/culturerobotics/insilicho/actions/workflows/python_tests.yml/badge.svg)\n![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)\n\n# InSiliCHO\nA model to capture CHO dynamics in-silico.  An accompanying streamlit app to try the model out is [available](https://culturebio-insilicho.streamlit.app/). \n\nModel is based on the following primary sources:\n- Pörtner, Ralf, ed. Animal Cell Biotechnology: Methods and Protocols. Vol. 2095. Methods in Molecular Biology. New York, NY: Springer US, 2020. https://doi.org/10.1007/978-1-0716-0191-4. \n- Möller, Johannes, Tanja Hernández Rodríguez, Jan Müller, Lukas Arndt, Kim B. Kuchemüller, Björn Frahm, Regine Eibl, Dieter Eibl, and Ralf Pörtner. “Model Uncertainty-Based Evaluation of Process Strategies during Scale-up of Biopharmaceutical Processes.” Computers & Chemical Engineering 134 (March 2020): 106693. https://doi.org/10.1016/j.compchemeng.2019.106693.\n\nAdditional sources include:\n- Parolini, Dott Nicola, and Susanna Carcano. “A model for cell growth in batch bioreactors,” 2009, Thesis.\n- Frahm, Björn. “Seed Train Optimization for Cell Culture.” In Animal Cell Biotechnology, edited by Ralf Pörtner, 1104:355–67. Methods in Molecular Biology. Totowa, NJ: Humana Press, 2014. https://doi.org/10.1007/978-1-62703-733-4_22.\n\n- Möller, Johannes, Kim B. Kuchemüller, Tobias Steinmetz, Kirsten S. Koopmann, and Ralf Pörtner. “Model-Assisted Design of Experiments as a Concept for Knowledge-Based Bioprocess Development.” Bioprocess and Biosystems Engineering 42, no. 5 (May 2019): 867–82. https://doi.org/10.1007/s00449-019-02089-7.\n\n\n\n\n# Usage\nThis repo serves as a standalone package, available to install using (or added as a dependency) using:\n\n`pip install -e git+https://github.com/culturerobotics/insilicho#egg=insilicho`\n\n# Example\n\n```python\n\n  from insilicho import run\n\n  def T(time):\n      """returns temperature in degC"""\n      return 36.4\n\n  def F(time):\n      """returns flow rate in L/hr"""\n      return 0.003\n\n  model = run.GrowCHO(\n      {"parameters": {"K_lys": "0.05 1/h"}},\n      feed_fn=F,\n      temp_fn=T,\n  )\n\n  model.execute(plot=True, initial_conditions={"V": "50 mL"})\n  \n  final_vol = model.full_result.state[-1, 8]\n  print(final_V) # 0.914L\n\n```\n',
    'author': 'Culture Biosciences',
    'author_email': 'matt@culturebiosciences.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
