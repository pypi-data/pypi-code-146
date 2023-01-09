# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dsp_tools', 'dsp_tools.models', 'dsp_tools.schemas', 'dsp_tools.utils']

package_data = \
{'': ['*'], 'dsp_tools': ['docker/*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'jsonpath-ng>=1.5.3,<2.0.0',
 'jsonschema>=4.17.3,<5.0.0',
 'lxml>=4.9.2,<5.0.0',
 'networkx>=2.8.8,<3.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.5.2,<2.0.0',
 'pystrict>=1.3,<2.0',
 'regex>=2022.10.31,<2023.0.0',
 'requests>=2.28.1,<3.0.0',
 'xlrd>=1.0.0']

entry_points = \
{'console_scripts': ['dsp-tools = dsp_tools.dsp_tools:main']}

setup_kwargs = {
    'name': 'dsp-tools',
    'version': '2.0.0',
    'description': 'DSP-TOOLS is a Python package with a command line interface that helps you interact with a DaSCH service platform (DSP) server.',
    'long_description': '[![PyPI version](https://badge.fury.io/py/dsp-tools.svg)](https://badge.fury.io/py/dsp-tools)\n\n# DSP-TOOLS documentation\n\nDSP-TOOLS is a Python package with a command line interface that helps you interact with a DSP server. The DSP server \nyou interact with can be on a remote server, or on your local machine. The two main tasks that DSP-TOOLS serves for are:\n\n**Create a project with its data model(s), described in a JSON file, on a DSP server**  \nIn order to archive your data on the DaSCH Service Platform, you need a data model that describes your data.\nThe data model is defined in a JSON project definition file which has to be transmitted to the DSP server. If the DSP \nserver is aware of the data model for your project, conforming data can be uploaded into the DSP repository.\n\n**Upload data, described in an XML file, to a DSP server that has a project with a matching data model**  \nSometimes, data is added in large quantities. Therefore, DSP-TOOLS allows you to perform bulk imports of your\ndata. In order to do so, the data has to be described in an XML file. DSP-TOOLS is able to read the XML file and upload\nall data to the DSP server.\n\nAll of DSP-TOOLS\' functionality revolves around these two basic tasks. \n\nDSP-TOOLS provides the following functionalities:\n\n- [`dsp-tools create`](./dsp-tools-usage.md#create-a-project-on-a-dsp-server) creates the project with its data model(s) \n  on a DSP server from a JSON file.\n- [`dsp-tools get`](./dsp-tools-usage.md#get-a-project-from-a-dsp-server) reads a project with its data model(s) from \n  a DSP server and writes it into a JSON file.\n- [`dsp-tools xmlupload`](./dsp-tools-usage.md#upload-data-to-a-dsp-server) uploads data from an XML file (bulk\n  data import) and writes the mapping from internal IDs to IRIs into a local file.\n- [`dsp-tools excel2json`](./dsp-tools-usage.md#create-a-json-project-file-from-excel-files) creates an entire JSON\n  project file from a folder with Excel files in it.\n    - [`dsp-tools excel2lists`](./dsp-tools-usage.md#create-the-lists-section-of-a-json-project-file-from-excel-files)\n      creates the "lists" section of a JSON project file from one or several Excel files. The resulting section can be \n      integrated into a JSON project file and then be uploaded to a DSP server with `dsp-tools create`.\n    - [`dsp-tools excel2resources`](./dsp-tools-usage.md#create-the-resources-section-of-a-json-project-file-from-an-excel-file)\n      creates the "resources" section of a JSON project file from an Excel file. The resulting section can be integrated \n      into a JSON project file and then be uploaded to a DSP server with `dsp-tools create`.\n    - [`dsp-tools excel2properties`](./dsp-tools-usage.md#create-the-properties-section-of-a-json-project-file-from-an-excel-file)\n      creates the "properties" section of a JSON project file from an Excel file. The resulting section can be integrated \n      into a JSON project file and then be uploaded to a DSP server with `dsp-tools create`.\n- [`dsp-tools excel2xml`](./dsp-tools-usage.md#create-an-xml-file-from-excelcsv) transforms a data source to XML if it \n  is already structured according to the DSP specifications.\n- [The module `excel2xml`](./dsp-tools-usage.md#use-the-module-excel2xml-to-convert-a-data-source-to-xml) provides helper\n  methods that can be used in a Python script to convert data from a tabular format into XML.\n- [`dsp-tools id2iri`](./dsp-tools-usage.md#replace-internal-ids-with-iris-in-xml-file)\n  takes an XML file for bulk data import and replaces referenced internal IDs with IRIs. The mapping has to be provided\n  with a JSON file.\n- [`dsp-tools start-stack / stop-stack`](./dsp-tools-usage.md#start-a-dsp-stack-on-your-local-machine)\n  assist you in running a DSP stack on your local machine.\n',
    'author': 'DaSCH - Swiss National Data and Service Center for the Humanities',
    'author_email': 'info@dasch.swiss',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.dasch.swiss/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
