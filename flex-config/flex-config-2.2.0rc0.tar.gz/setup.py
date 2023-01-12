# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flex_config', 'flex_config.file_sources']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.2,<2.0.0']

extras_require = \
{'all': ['boto3>=1.13.1,<2.0.0',
         'pyyaml>=5.3.1,<6.0.0',
         'toml>=0.10.2,<0.11.0'],
 'aws': ['boto3>=1.13.1,<2.0.0'],
 'toml': ['toml>=0.10.2,<0.11.0'],
 'yaml': ['pyyaml>=5.3.1,<6.0.0']}

setup_kwargs = {
    'name': 'flex-config',
    'version': '2.2.0rc0',
    'description': 'Easily configure Python apps via environment variables, YAML, and AWS SSM Param Store.',
    'long_description': '# Flex Config\n[![triaxtec](https://circleci.com/gh/triaxtec/flex-config.svg?style=svg)](https://app.circleci.com/pipelines/github/triaxtec/flex-config?branch=master)\n[![codecov](https://codecov.io/gh/triaxtec/flex-config/branch/master/graph/badge.svg?token=3utvPfZSLB)](https://codecov.io/gh/triaxtec/flex-config)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Generic badge](https://img.shields.io/badge/type_checked-mypy-informational.svg)](https://mypy.readthedocs.io/en/stable/introduction.html)\n[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)\n\n\nConfigure your applications as easily as possible.\n\n## Main Features\n### Load config from wherever\n- Comes with built in support for loading from dicts, environment variables, JSON/YAML/TOML files, and AWS SSM Parameter Store.\n- Super easy to set up a custom source and load from anywhere.\n\n### Type conversion, validation, and hints via [Pydantic]\n```python\n# "ConfigSchema" is pydantic\'s BaseModel renamed and re-exported for easier use \nfrom flex_config import ConfigSchema, construct_config\n\nclass Config(ConfigSchema):\n    a_string: str\n    an_int: int\n\n# Raises ValidationError\nmy_bad_config = construct_config(Config, {"a_string": ["not", "a", "string"], "an_int": "seven"})\n\nmy_good_config = construct_config(Config, {"a_string": "my_string", "an_int": "7"})\nassert isinstance(my_good_config.an_int, int)\n```\n\n### Dynamic loading of config values\n```python\nfrom pathlib import Path\nfrom typing import Dict, Any\n\n# "ConfigSchema" is pydantic\'s BaseModel renamed and re-exported for easier use \nfrom flex_config import ConfigSchema, construct_config, AWSSource, YAMLSource, EnvSource, ConfigSource\n\nclass Config(ConfigSchema):\n    env: str\n    my_thing: str\n\ndef get_ssm_params(config_so_far: Dict[str, Any]) -> ConfigSource:\n    # env is set to live or dev via environment variables in the deployment environment\n    env = config_so_far.get("env")\n    if env == "local":  # Not a live deployment, my_thing is in a local yaml file\n        return {}\n    return AWSSource(f"my_app/{config_so_far[\'env\']}")\n\n\nmy_config = construct_config(Config, [EnvSource("MY_APP_"), YAMLSource(Path("my_file.yaml")), get_ssm_params])\n```\n\n## Installation\nBasic install: `poetry install flex_config`\nWith all optional dependencies (support for AWS SSM, YAML, and TOML): `poetry install flex_config -E all`\n\nFor a full tutorial and API docs, check out the [hosted documentation]\n\n[Pydantic]: https://github.com/samuelcolvin/pydantic/\n[hosted documentation]: https://triaxtec.github.io/flex-config\n',
    'author': 'Dylan Anthony',
    'author_email': 'danthony@triaxtec.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/triaxtec/flex-config',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
