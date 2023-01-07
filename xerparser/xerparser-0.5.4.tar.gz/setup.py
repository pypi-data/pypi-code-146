# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xerparser', 'xerparser.schemas', 'xerparser.scripts', 'xerparser.src']

package_data = \
{'': ['*']}

install_requires = \
['html-sanitizer>=1.9.3,<2.0.0']

entry_points = \
{'console_scripts': ['test = scripts:test']}

setup_kwargs = {
    'name': 'xerparser',
    'version': '0.5.4',
    'description': 'Parse a P6 .xer file to a Python object.',
    'long_description': '# xerparser\n\nA simple Python package that reads the contents of a P6 .xer file and converts it into a Python object.  \n<br>\n*Disclaimers:  \nIt\'s helpfull if you are already familiar with the mapping and schemas used by P6 during the export process. \nRefer to the [Oracle Documentation]( https://docs.oracle.com/cd/F25600_01/English/Mapping_and_Schema/xer_import_export_data_map_project/index.htm) for more information regarding how data is mapped to the XER format.  \nTested on .xer files exported as versions 15.2 through 19.12.*  \n<br>\n## Install\n**Windows**:\n```bash\npip install xerparser\n```\n**Linux/Mac**: \n```bash\npip3 install xerparser\n```\n<br>  \n\n## Usage  \nImport the `Xer` class from `xerparser`  and pass the contents of a .xer file as an argument. Use the `Xer` class variable `CODEC` to set the proper encoding to decode the file.\n```python\nfrom xerparser import Xer\n\nfile = r"/path/to/file.xer"\nwith open(file, encoding=Xer.CODEC, errors="ignore") as f:\n    file_contents = f.read()\nxer = Xer(file_contents)\n```\n*Note: do not pass the the .xer file directly as an argument. The file must be decoded and read into a string, which can then be passed as an argument.*  \n<br>\n## Attributes \nThe tables stored in the .xer file are accessable as either Global , Project specific, Task specific, or Resource specific:\n###  Global\n  ```python\n  xer.export_info           # export data\n  xer.errors                # list of potential errors in export process\n  xer.activity_code_types   # dict of ACTVTYPE objects\n  xer.activity_code_values  # dict of ACTVCODE objects\n  xer.calendars             # dict of all CALENDAR objects\n  xer.financial_periods     # dict of FINDATES objects\n  xer.notebook_topics       # dict of MEMOTYPE objects\n  xer.projects              # dict of PROJECT objects\n  xer.tasks                 # dict of all TASK objects\n  xer.relationships         # dict of all TASKPRED objects\n  xer.resources             # dict of RSRC objects\n  xer.wbs_nodes             # dict of all PROJWBS objects\n  ```  \n### Project Specific\n```python\n# Get first project\nproject = xer.projects.values()[0]\n\nproject.activity_codes  # list of project specific ACTVTYPE objects\nproject.calendars       # list of project specific CALENDAR objects\nproject.tasks           # list of project specific TASK objects\nproject.relationships   # list of project specific TASKPRED objects\nproject.wbs_nodes       # list of project specific PROJWBS objects\n```\n### Task Specific\n```python\n# Get first task\ntask = project.tasks[0]\n\ntask.activity_codes   # dict of ACTVTYPE: ACTVCODE objects\ntask.memos            # list of TASKMEMO objects\ntask.resources        # dict of TASKRSRC objects\ntask.periods          # list of TASKFIN objects\n```\n### Resource Specific\n```python\n# Get first task resource\nresource = task.resources.values()[0]\n\nresource.periods  # list of TRSRCFIN objects\n```\n\n<br>\n\n## Error Checking\nSometimes the xer file is corrupted during the export process. A list of potential errors is generated based on common issues encountered when analyzing .xer files:  \n- Minimum required tables - an error is recorded if one of the following tables is missing:\n  - CALENDAR\n  - PROJECT\n  - PROJWBS\n  - TASK\n  - TASKPRED  \n- Required table pairs - an error is recorded if Table 1 is included but not Table 2:  \n  \n  | Table 1       | Table 2       | Notes    |\n  | :----------- |:-------------|----------|\n  | TASKFIN | FINDATES | *Financial Period Data for Task* |\n  | TRSRCFIN | FINDATES | *Financial Period Data for Task Resource* |\n  | TASKRSRC | RSRC | *Resource Data* |\n  | TASKMEMO | MEMOTYPE | *Notebook Data* |\n  | ACTVCODE | ACTVTYPE | *Activity Code Data* |\n  | TASKACTV | ACTVCODE | *Activity Code Data* |\n\n- Non-existent calendars assigned to activities.\n',
    'author': 'Jesse',
    'author_email': 'code@seqmanagement.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jjCode01/xerparser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
