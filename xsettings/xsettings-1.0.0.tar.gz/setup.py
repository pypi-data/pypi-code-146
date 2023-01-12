# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xsettings']

package_data = \
{'': ['*']}

install_requires = \
['ciso8601>=2.3.0,<3.0.0',
 'xbool>=1.0.0,<2.0.0',
 'xinject>=1.2.0,<2.0.0',
 'xloop>=1.0.1,<2.0.0',
 'xsentinels>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'xsettings',
    'version': '1.0.0',
    'description': 'Ways to document, centeralize, retreive and validate settings.',
    'long_description': "![PythonSupport](https://img.shields.io/static/v1?label=python&message=%203.8|%203.9|%203.10|%203.11&color=blue?style=flat-square&logo=python)\n![PyPI version](https://badge.fury.io/py/xsettings.svg?)\n\n- [Introduction](#introduction)\n- [Documentation](#documentation)\n- [Install](#install)\n- [Quick Start](#quick-start)\n- [Licensing](#licensing)\n\n# Introduction\n\nHelps document and centralizing settings in a python project/library.\n\nFacilitates looking up Settings from `retrievers`, such as an environmental variable retriever.\n\nConverts and standardizes any retrieved values to the type-hint on the setting attribute (such as bool, int, datetime, etc).\n\nInterface to provide own custom retrievers, to grab settings/configuration from wherever you want.\n\nRetrievers can be stacked, so multiple ones can be consulted when retrieving a setting.\n\nSee **[xsettings docs](https://xyngular.github.io/py-xsettings/latest/)**.\n\n# Documentation\n\n**[📄 Detailed Documentation](https://xyngular.github.io/py-xsettings/latest/)** | **[🐍 PyPi](https://pypi.org/project/xsettings/)**\n\n# Install\n\n```bash\n# via pip\npip install xsettings\n\n# via poetry\npoetry add xsettings\n```\n\n# Quick Start\n\n```python\nfrom xsettings import EnvVarSettings, SettingsField\nfrom xsettings.errors import SettingsValueError\nfrom typing import Optional\nimport dataclasses\nimport os\n\n# Used to showcase looking up env-vars automatically:\nos.environ['app_version'] = '1.2.3'\n\n# Used to showcase complex setting types:\n@dataclasses.dataclass\nclass DBConfig:\n    @classmethod\n    def from_dict(cls, values: dict):\n        return DBConfig(**values)\n\n    user: str\n    host: str\n    password: str\n\n\n# Some defined settings:\nclass MySettings(EnvVarSettings):\n    app_env: str = 'dev'\n    app_version: str\n    api_endpoint_url: str\n    \n    some_number: int\n\n    # For Full Customization, allocate SettingsField,\n    # In this case an alternate setting lookup-name\n    # if you want the attribute name to differ from lookup name:\n    token: Optional[str] = SettingsField(name='API_TOKEN')\n\n    # Or if you wanted a custom-converter for a more complex obj:\n    db_config: DBConfig = SettingsField(\n        converter=DBConfig.from_dict\n    )\n\n# Settings subclasses are singleton-like dependencies that are\n# also injectables and lazily-created on first-use.\n# YOu can use a special `Settings.grab()` class-method to\n# get the current settings object.\n#\n# So you can grab the current MySettings object lazily via\n# its `grab` class method:\nMySettings.grab().some_number = 3\n\nassert MySettings.grab().some_number == 3\n\n# You can also use a proxy-object, it will lookup and use\n# the current settings object each time its used:\nmy_settings = MySettings.proxy()\n\n# Here I showcase setting a dict here and using the converter\n# I defined on the SettingsField to convert it for me:\nmy_settings.db_config = {\n    'user': 'my-user',\n    'password': 'my-password',\n    'host': 'my-host'\n}\n\n\nexpected = DBConfig(\n    user='my-user',\n    password='my-password',\n    host='my-host'\n)\n\n# The dict gets converted automatically to the DBConfig obj:\nassert MySettings.grab().db_config == expected\n\n# If you set a setting with the same/exact type as\n# it's type-hint, then it won't call the converter:\nmy_settings.db_config = expected\n\n# It's the same exact object-instance still (ie: not changed/converted):\nassert my_settings.db_config is expected\n\n\n# Will use the default value of `dev` (default value on class)\n# since it was not set to anything else and there is no env-var for it:\nassert my_settings.app_env == 'dev'\n\n# EnvVarSettings (superclass) is configured to use the EnvVar retriever,\n# and so it will find this in the environmental vars since it was not\n# explicitly set to anything on settings object:\nassert my_settings.app_version == '1.2.3'\n\n# Any Settings subclass can use dependency-injection:\nassert my_settings.token is None\n\nwith MySettings(token='my-token'):\n    assert my_settings.token == 'my-token'\n\n    # Parent is still consulted for any settings unset on child but set on parent:\n    assert my_settings.db_config == expected\n\n    # Can set settings like you expect,\n    # this will go into the child created in above `with` statement:\n    my_settings.app_env = 'prod'\n\n    assert my_settings.app_env == 'prod'\n\n# After `with` child is not the current settings object anymore,\n# reverts back to what it was before:\nassert my_settings.token is None\n\ntry:\n    # If a setting is undefined and required (ie: not-optional),\n    # and it was not set to anything nor is there a default or an env-var for it;\n    # Settings will raise an exception when getting it:\n    print(my_settings.api_endpoint_url)\nexcept SettingsValueError as e:\n    assert True\nelse:\n    assert False\n\ntry:\n    # `SettingsValueError` inherits from both AttributeError and ValueError,\n    # as the error could be due to either aspect; so you can also do an except\n    # for either standard error:\n    print(my_settings.api_endpoint_url)\nexcept ValueError as e:\n    assert True\nelse:\n    assert False\n```\n\n\n\n# Licensing\n\nThis library is licensed under the MIT-0 License. See the LICENSE file.\n",
    'author': 'Josh Orr',
    'author_email': 'josh@orr.blue',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/xyngular/py-xsettings',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
