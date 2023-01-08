# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['full_yaml_metadata']
install_requires = \
['markdown>=3.4.1,<4.0.0', 'pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'markdown-full-yaml-metadata',
    'version': '2.2.1',
    'description': 'YAML metadata extension for Python-Markdown',
    'long_description': '# YAML metadata extension for [Python-Markdown](https://github.com/waylan/Python-Markdown)\n\n[![test](https://github.com/sivakov512/python-markdown-full-yaml-metadata/actions/workflows/test.yml/badge.svg)](https://github.com/sivakov512/python-markdown-full-yaml-metadata/actions/workflows/test.yml)\n[![Coverage Status](https://coveralls.io/repos/github/sivakov512/python-markdown-full-yaml-metadata/badge.svg)](https://coveralls.io/github/sivakov512/python-markdown-full-yaml-metadata)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Python versions](https://img.shields.io/pypi/pyversions/markdown-full-yaml-metadata.svg)](https://pypi.python.org/pypi/markdown-full-yaml-metadata)\n[![PyPi](https://img.shields.io/pypi/v/markdown-full-yaml-metadata.svg)](https://pypi.python.org/pypi/markdown-full-yaml-metadata)\n\nThis extension adds YAML meta data handling to markdown with all YAML features.\n\nAs in the original, metadata is parsed but not used in processing.\n\nMetadata parsed as is by PyYaml and without additional transformations, so this plugin is not compatible with original [Meta-Data extension](https://pythonhosted.org/Markdown/extensions/meta_data.html).\n\n\n## Basic Usage\n\n``` python\nimport markdown\n\n\ntext = """---\ntitle: What is Lorem Ipsum?\ncategories:\n  - Lorem Ipsum\n  - Stupid content\n...\n\nLorem Ipsum is simply dummy text.\n"""\n\nmd = markdown.Markdown(extensions=[\'full_yaml_metadata\']})\nmd.convert(text) == \'<p>Lorem Ipsum is simply dummy text.</p>\'\nmd.Meta == {\'title\': \'What is Lorem Ipsum?\', \'categories\': [\'Lorem Ipsum\', \'Stupid content\']}\n```\n\n### Specify a custom YAML loader\n\nBy default the full YAML loader is used for parsing, which is insecure when\nused with untrusted user data. In such cases, you may want to specify a\ndifferent loader such as [`yaml.SafeLoader`](https://msg.pyyaml.org/load) using\nthe `extension_configs` keyword argument:\n\n```python\nimport markdown\nimport yaml\n\nmd = markdown.Markdown(extensions=[\'full_yaml_metadata\']}, extension_configs={\n        "full_yaml_metadata": {\n            "yaml_loader": yaml.SafeLoader,\n        },\n    },\n)\n```\n\n\n## Development and contribution\n\nFirst of all you should install [Poetry](https://python-poetry.org).\n\n* install project dependencies\n```bash\nmake install\n```\n\n* run linters\n```bash\nmake lint\n```\n\n* run tests\n```bash\nmake test\n```\n\n* feel free to contribute!\n',
    'author': 'Nikita Sivakov',
    'author_email': 'sivakov512@icloud.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sivakov512/python-markdown-full-yaml-metadata',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
