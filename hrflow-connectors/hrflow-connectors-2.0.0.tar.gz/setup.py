# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hrflow_connectors',
 'hrflow_connectors.connectors.adzuna',
 'hrflow_connectors.connectors.breezyhr',
 'hrflow_connectors.connectors.breezyhr.utils',
 'hrflow_connectors.connectors.bullhorn',
 'hrflow_connectors.connectors.bullhorn.utils',
 'hrflow_connectors.connectors.ceridian',
 'hrflow_connectors.connectors.greenhouse',
 'hrflow_connectors.connectors.hrflow',
 'hrflow_connectors.connectors.hrflow.warehouse',
 'hrflow_connectors.connectors.hubspot',
 'hrflow_connectors.connectors.poleemploi',
 'hrflow_connectors.connectors.recruitee',
 'hrflow_connectors.connectors.sapsuccessfactors',
 'hrflow_connectors.connectors.sapsuccessfactors.utils',
 'hrflow_connectors.connectors.smartrecruiters',
 'hrflow_connectors.connectors.talentsoft',
 'hrflow_connectors.connectors.teamtailor',
 'hrflow_connectors.connectors.waalaxy',
 'hrflow_connectors.connectors.workable',
 'hrflow_connectors.core',
 'hrflow_connectors.core.backend']

package_data = \
{'': ['*'],
 'hrflow_connectors.connectors.adzuna': ['docs/*'],
 'hrflow_connectors.connectors.breezyhr': ['docs/*'],
 'hrflow_connectors.connectors.bullhorn': ['docs/*'],
 'hrflow_connectors.connectors.ceridian': ['docs/*'],
 'hrflow_connectors.connectors.greenhouse': ['docs/*'],
 'hrflow_connectors.connectors.hubspot': ['docs/*'],
 'hrflow_connectors.connectors.poleemploi': ['docs/*'],
 'hrflow_connectors.connectors.recruitee': ['docs/*'],
 'hrflow_connectors.connectors.sapsuccessfactors': ['docs/*'],
 'hrflow_connectors.connectors.smartrecruiters': ['docs/*'],
 'hrflow_connectors.connectors.talentsoft': ['docs/*'],
 'hrflow_connectors.connectors.teamtailor': ['docs/*'],
 'hrflow_connectors.connectors.waalaxy': ['docs/*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'hrflow>=1.9.0,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0']

extras_require = \
{'s3': ['boto3>=1.24.66,<2.0.0']}

setup_kwargs = {
    'name': 'hrflow-connectors',
    'version': '2.0.0',
    'description': 'hrflow-connectors is an open source project created by HrFlow.ai to allow developers to connect easily HR ecosystem component.',
    'long_description': '<p align="center">\n  <a href="https://hrflow.ai">\n    <img alt="hrflow" src="https://img.riminder.net/logo-hrflow.svg" width="120" />\n  </a>\n</p>\n<h1 align="center">\n  HrFlow.ai connectors\n</h1>\n\n![GitHub Repo stars](https://img.shields.io/github/stars/Riminder/hrflow-connectors?style=social) ![](https://img.shields.io/github/v/release/Riminder/hrflow-connectors) ![](https://img.shields.io/github/license/Riminder/hrflow-connectors)\n\n\n<p align="center">\n  <a href="https://hrflow.ai">\n    <img alt="hrflow" src="https://hrflow-ai.imgix.net/corporate.svg"/>\n  </a>\n</p>\n\n<br/>\n\n## About HrFlow.ai\n\n**[HrFlow.ai](https://hrflow.ai/) is on a mission to make AI and data integration pipelines a commodity in the HR Industry:**\n  1. **Unify**: Link your Talent Data channels with a few clicks, so they can share data.\n  2. **Understand**: Leverage our AI solutions to process your Talent Data.\n  3. **Automate**: Sync data between your tools and build workflows that meet your business logic.\n\n**HrFlow-Connectors** is an open-source project created by HrFlow.ai to democratize Talent Data integration within the HR Tech landscape.\n\nWe invite developers to join us in our mission to bring AI and data integration to the HR industr, as a developper you can: \n\n- Create new connectors quickly and easily with our low-code connector approach and abstracted concepts\n- Contribute to the Connectors\' framework with your own code\n- Leverage our AI solutions to process your Talent Data\n- Sync data between your tools and build workflows that meet your business logic\n- Link your Talent Data channels with a few clicks, so they can share data\n\n📃 **More instructions are available in the Documentation section below** \n\n## :electric_plug: List of Connectors\n\n| Name 🔌 | Type 🔧  | Available 📦 | Release date 📅 | Last update 🔁 \n| - | - | - | - | - |\n| **ADP** | HCM Cloud | :hourglass: |   |  |\n| **ADENCLASSIFIEDS** | Job Board | :hourglass: |  |  |\n| **Adzuna** | Job Board | :heavy_check_mark: | *08/09/2022* | *12/01/2023* |\n| **Agefiph** | Job Board | :hourglass: |  |  |\n| **APEC** | Job Board | :hourglass: |  |  |\n| **Bullhorn** | ATS | :heavy_check_mark: | *26/01/2022* | *12/01/2023* |\n| **Breezy.hr** | ATS | :heavy_check_mark: | *19/01/2022* | *12/01/2023* |\n| **Cadreemploi** | Job Board | :hourglass: |  |  |\n| **Cegid (Meta4)** |  | :hourglass: |  |  |\n| **Ceridian** | HCM | :heavy_check_mark: | *19/01/2022* | *12/01/2023* |\n| **Cornerjob** | Job Board | :hourglass: |  |  |\n| **Cornerstone OnDemand** |  | :hourglass: |  |  |\n| **Crosstalent** | ATS | :wrench: | *19/01/2022* | |\n| **Digitalrecruiters** | ATS | :hourglass: |  |  |\n| **Distrijob** | Job Board | :hourglass: |  |  |\n| **Engagement Jeunes** | Job Board | :hourglass: |  |  |\n| **FashionJobs** | Job Board | :hourglass: |  |  |\n| **Fieldglass SAP** | Recruiting Software | :hourglass: |  |  |\n| **Flatchr** | ATS  | :wrench: | *21/04/2022* | |\n| **Glassdoor** | Job Board | :hourglass: |  |  |\n| **GoldenBees** | Job Board | :hourglass: |  |  |\n| **Greenhouse** | ATS  | :heavy_check_mark: | *19/01/2022* | *12/01/2023* |\n| **Handicap-Job** | Job Board | :hourglass: |  |  |\n| **HelloWork** | Job Board | :hourglass: |  |  |\n| **Hubspot** | CRM | :heavy_check_mark: | *27/10/2022* | *12/01/2023* |\n| **ICIMS** | ATS | :hourglass: |  |  |\n| **Indeed** | Job Board | :hourglass: |  |  |\n| **Inzojob** | Job Board | :hourglass: |  |  |\n| **Jobijoba** | Job Board | :hourglass: |  |  |\n| **Jobrapido** | Job Board | :hourglass: |  |  |\n| **JobTeaser** | Job Board | :hourglass: |  |  |\n| **Jobtransport** | Job Board | :hourglass: |  |  |\n| **Jobvitae** | Job Board | :hourglass: |  |  |\n| **Jobvite** |  | :hourglass: |  |  |\n| **Jooble** | Job Board | :hourglass: |  |  |\n| **Keljob** | Job Board | :hourglass: |  |  |\n| **Kronos (UKG)** | HCM Cloud | :hourglass: |  |  |\n| **Laponi** | Job Board | :hourglass: |  |  |\n|**Leboncoin** |     | :wrench: | *13/07/2022* | |\n| **LesJeudis** | Job Board | :hourglass: |  |  |\n| **Lever** | CRM-ATS | :hourglass:  |  |  |\n| **LinkedIn** | Job Board | :hourglass: |  |  |\n| **Mailchimp** | Marketing Tools | :hourglass: |  |  |\n| **Meteojob** | Job Board | :hourglass: |  |  |\n| **Microsoft Dynamics** | HCM Cloud | :hourglass: |  |  |\n| **Monster** | Job Board | :wrench: | *23/11/2022* | |\n| **Nuevoo** | Job Board | :hourglass: |  |  |\n| **Optioncarriere** | Job Board | :hourglass: |  |  |\n| **Oracle** | Cloud Apps | :hourglass: |  |  |\n| **Pole Emploi** | Job Board | :heavy_check_mark: |*15/07/2022* | *12/01/2023* |\n| **Recruitee** | ATS | :heavy_check_mark: | *30/10/2022* | *12/01/2023* |\n| **RecruitBox** |  | :hourglass: |  |  |\n| **RegionsJob** | Job Board | :hourglass: |  |  |\n| **SAPSuccessfactors** | Cloud Apps for HR | :heavy_check_mark: | *19/01/2022* | *12/01/2023* |\n| **Salesforce** | CRM-ATS | :hourglass: |  |  |\n| [**Smartrecruiters**](src/hrflow_connectors/connectors/smartrecruiters/) | ATS | :heavy_check_mark: | *21/03/2022* | *30/06/2022* |\n| **Staffme** | Job Board | :hourglass: |  |  |\n| **Staffsante** | Job Board | :hourglass: |  |  |\n| **Taleez** | ATS | :wrench: |*19/01/2022* | |\n| **Talentsoft** | HCM | :heavy_check_mark: | *19/04/2022* | *09/05/2022* |\n| **Talentlink** |  | :hourglass: |  |  |\n| **Teamtailor** | ATS | :heavy_check_mark: | *06/10/2022* | *12/01/2023* |\n| **Tekkit** | Job Board | :hourglass: |  |  |\n| **Turnover-IT** | Job Board | :hourglass: |  |  |\n| **Twilio** | Marketing Tools | :hourglass: |  |  |\n| **Ultimate Software (UKG)** |  | :hourglass: |  |  |\n| **Waalaxy** |  | :heavy_check_mark: |*18/11/2022* | *12/01/2023* |\n| **Workable** | HCM | :heavy_check_mark: | *27/09/2022* | *12/01/2023* |\n| **Welcome To The Jungle** | Job Board | :hourglass: |  |  |\n| **Wizbii** | Job Board | :hourglass: |  |  |\n| **Workday** | HCM Cloud | :heavy_check_mark: |  |  |\n| **XML** | Job Board | :wrench: |  |  |\n\n\n## \U0001fa84 Quickstart\n### What I can do?\nWith Hrflow Connector, you can **synchronize** and **process** multiple **HR data streams** in just a few lines of code.\n\nYou can do any kind of data transfer between HrFlow.ai and external destinations :\n* Pull jobs : `External Job flow` :arrow_right: ***`Hrflow.ai Board`***\n* Pull profiles : `External Profile flow` :arrow_right: ***`Hrflow.ai Source`***\n* Push job : ***`Hrflow.ai Board`*** :arrow_right: `External destination`\n* Push profile : ***`Hrflow.ai Source`*** :arrow_right: `External destination`\n\nThe features offered by this package:\n* **Synchronize an entire data** stream with a ready-to-use solution\n*  **Synchronize only certain data** in a stream meeting a condition defined by you : [`logics`](DOCUMENTATION.md#logics)\n* **Format the data as you wish** or use the default formatting that we propose adapted to each connector : [`format`](DOCUMENTATION.md#format)\n* **Leverage the provider *Hrflow.ai\'s ** Job and Profile Warehouse * with a many available options like [`hydrate_with_parsing`](src/hrflow_connectors/connectors/hrflow/warehouse.py#L42) or [`update_content`](src/hrflow_connectors/connectors/hrflow/warehouse.py#L39)\n\n### How to use a connector ?\n**Prerequisites**\n* [✨ Create a Workspace](https://hrflow.ai/signup/)\n* [🔑 Get your API Key](https://developers.hrflow.ai/docs/api-authentification)\n\n1. **`pip install hrflow-connectors`**\n2. Pick the connector you would like to use. Let\'s say it\'s **SmartRecruiters**\n3. Navigate to the connector\'s _README_. That would be [here](src/hrflow_connectors/connectors/smartrecruiters/README.md) for **SmartRecruiters**\n4. Choose from the available actions the one you would like to use\n5. Navigate to the action\'s documentation to find ready for copy/paste integration code\n\n:checkered_flag: **TADA! You have just used your first connector.**\n\n\n## 📖 Documentation\nTo find out **more about the HrFlow.ai Connectors framework** take a look at the [📖 documentation](DOCUMENTATION.md).\n\n## :bulb: Contributions\n\nPlease feel free to contribute to the quality of this content by\nsubmitting PRs for improvements to code, architecture, etc.\n\nAny contributions you make to this effort are of course greatly\nappreciated.\n\n👉 **To find out more about how to proceed, the rules and conventions to follow, read carefully [`CONTRIBUTING.md`](CONTRIBUTING.md).**\n\n## 🔗 Resources\n* Our Developers documentation : https://developers.hrflow.ai/\n* Our API list (Parsing, Revealing, Embedding, Searching, Scoring, Reasoning) : https://www.hrflow.ai/api\n* Our cool demos labs : https://labs.hrflow.ai\n\n## :page_with_curl: License\n\nSee the [`LICENSE`](LICENSE) file for licensing information.\n',
    'author': 'HrFlow.ai',
    'author_email': 'support+hrflow_connectors@hrflow.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Riminder/hrflow-connectors',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '==3.10.5',
}


setup(**setup_kwargs)
