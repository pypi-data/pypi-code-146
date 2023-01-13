# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['munitests']

package_data = \
{'': ['*']}

install_requires = \
['ibm-watson>=6.1.0,<7.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'matplotlib>=3.6.3,<4.0.0',
 'notebook>=6.5.2,<7.0.0',
 'pandas>=1.5.2,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'seaborn>=0.12.2,<0.13.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'munitests',
    'version': '0.3.0',
    'description': 'A test suite for the Chatbot MUNI',
    'long_description': "# A test suite for the Chatbot MUNI\n\nMUNI is your municipal Chatbot in Denmark, and can answer questions about everything from ID cards and MitID to child care. If you have a question for your municipality, MUNI will do its best to answer you.\n\nThe MUNI project is a collaboration between 36 municipalities, with Aarhus as the contract holder. In the project, they have implemented technology based on artificial intelligence to handle inquiries from citizens. This replaces much of the physical and telephone contact involved in citizen services. MUNI provides citizens with guidance and support and ensures that staff can handle more complex tasks.\n\nIn March 2022, the Chatbot collaboration won the Innovation Award. The reason given by the panel of judges was that the project is built on an outstanding and broad municipal cooperation. It uses new technology in an innovative way in an exemplary manner. It manages to exploit economies of scale while giving space for individual solutions among the individual municipalities. Deep integrations into systems and continuous development ensure the solution's relevance in the public's meeting with citizens. Read more here: https://www.digitaliseringsprisen.dk/#vinderne-2022-forside\n\n## Getting Started\n\nYou can install the MUNI test suite by running:\n\n```\npip install munitests\n```\n\nOr in a notebook:\n\n```\n!pip install munitests\n```\n\nAdditionally, if you want to make sure you always have to latest version use:\n\n```\npip install munitests --upgrade\n```\n\nOr in a notebook:\n\n```\n!pip install munitests --upgrade\n```\n",
    'author': 'Jens Peder Meldgaard',
    'author_email': 'jenspederm@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
