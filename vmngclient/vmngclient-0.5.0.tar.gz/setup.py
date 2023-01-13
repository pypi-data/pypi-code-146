# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vmngclient', 'vmngclient.api', 'vmngclient.tests', 'vmngclient.utils']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'attrs>=21.4.0,<22.0.0',
 'ciscoconfparse>=1.6.40,<2.0.0',
 'clint>=0.5.1,<0.6.0',
 'flake8-quotes>=3.3.1,<4.0.0',
 'parameterized>=0.8.1,<0.9.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests-toolbelt>=0.10.1,<0.11.0',
 'requests>=2.27.1,<3.0.0',
 'tenacity>=8.1.0,<9.0.0']

setup_kwargs = {
    'name': 'vmngclient',
    'version': '0.5.0',
    'description': 'Universal vManage API',
    'long_description': '# vManage-client\n[![Python3.8](https://img.shields.io/static/v1?label=Python&logo=Python&color=3776AB&message=3.8)](https://www.python.org/)\n\nvManage client is a package for creating simple and parallel automatic requests via official vManageAPI. It is intended to serve as a multiple session handler (provider, provider as a tenant, tenant). The library is not dependent on environment which is being run, you just need a connection to any vManage.\n\n## Installation\n```console\npip install vmngclient\n```\n\n## Hello world example\n\n<details>\n    <summary>Python (click to expand)</summary>\n\n```Python\nfrom vmngclient.session import create_vManageSession\n\n\nbase_url = "sandbox-sdwan-2.cisco.com/"\nusername = "devnetuser"\npassword = "RG!_Yw919_83"\nsession = create_vManageSession(url=base_url, username=username, password=password)\n\n\n>>> "Logged as devnetuser. The session type is SessionType.TENANT"\n>>> {\'title\': \'Cisco vManage\', \'version\': \'20.4.2.1\', \'applicationVersion\': \'20.4R-vbamboo-16-Dec-2021 19:07:17 PST\', \'applicationServer\': \'vmanage\', \'copyright\': \'Copyright (c) 2022, Cisco. All rights reserved.\', \'time\': \'2022-12-01 13:45:44\', \'timeZone\': \'UTC\', \'logo\': \'/dataservice/client/logo.png\'}\n```\n</details>\n\n### Note:\nTo remove `InsecureRequestWarning`, you can include in your scripts:\n```Python\nimport urllib3\nurllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)\n```\n\n## User creation example\n\n<details>\n    <summary>Python (click to expand)</summary>\n\n```Python\nfrom vmngclient.api.administration import UserAlreadyExistsError, UserApi\nfrom vmngclient.dataclasses import User\nfrom vmngclient.session import create_vManageSession\n\nsession = create_vManageSession(url=..., username=..., password=...)\nuser_api = UserApi(session)\n\ntest_user = User(\n    group=["basic"],\n    description="Demo User",\n    username="demouser",\n    password="password",\n    locale="en_US",\n    resource_group="global"\n)\n\ntry:\n    user_api.create_user(test_user)\nexcept UserAlreadyExistsError as error:\n    print(f"User {username} already exists.")\n```\n</details>\n\n## API usage examples\n\n### AdminTechAPI\n\n<details>\n    <summary>Python (click to expand)</summary>\n\n```Python\nfrom vmngclient.session import create_vManageSession\nfrom vmngclient.api.admin_tech_api import AdminTechAPI\n\nsession = create_vManageSession(url=..., username=..., password=...)\nadmintech = AdminTechAPI(session)\nfilename = admintech.generate("172.16.255.11")\nadmintech.download(filename)\nadmintech.delete(filename)\n```\n\n</details>\n\n\n## Contributing, reporting issues, seeking support\nPlease contact authors direcly or via Issues Github page.\n\n## **Enviroment setup**\n1. Download Python3.8 or higher.\n2. Download repository\n    ```\n    git clone https://github.com/CiscoDevNet/vManage-client.git\n    ```\n3. Install poetry v1.3.1\n    ```\n    pip install poetry==1.3.1\n    ```\n4. Configure poetry to use virtual environments in project folder (can ease IDE integration)\n    ```\n    poetry config virtualenvs.in-project true\n    ```\n5. Install dependecies \n    ```\n    poetry install\n    ```\n6. Activate `pre-commit`\n    ```\n    pre-commit install\n    ```\n\n## **Add new feature**\nTo add new feature create new branch and implement it. Before making a pull request make sure that `pre-commit` passes.\n- **Building package for tests**\\\n    To make a `.whl` file run\n    ```\n    poetry build\n    ```\n    Then in `/vManage-client/dist/` directory there is a `.whl` file named `vmngclient-<version>-py3-none-any.whl`, which can be installed by running\n    ```\n    pip install vmngclient-<version>-py3-none-any.whl\n    ```',
    'author': 'kagorski',
    'author_email': 'kagorski@cisco.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/CiscoDevNet/vManage-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
