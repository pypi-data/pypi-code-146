# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['linkml_renderer',
 'linkml_renderer.paths',
 'linkml_renderer.renderers',
 'linkml_renderer.style']

package_data = \
{'': ['*']}

install_requires = \
['airium>=0.2.5,<0.3.0',
 'click>=8.1.3,<9.0.0',
 'linkml-runtime>=1.4.1,<2.0.0',
 'linkml>=1.4.1,<2.0.0']

extras_require = \
{':extra == "docs"': ['myst-parser[docs]>=0.18.1,<0.19.0',
                      'sphinx[docs]>=5.3.0,<6.0.0',
                      'sphinx-autodoc-typehints[docs]>=1.19.4,<2.0.0',
                      'sphinx-click[docs]>=4.3.0,<5.0.0',
                      'sphinx-rtd-theme[docs]>=1.0.0,<2.0.0']}

entry_points = \
{'console_scripts': ['linkml-render = linkml_renderer.cli:main']}

setup_kwargs = {
    'name': 'linkml-renderer',
    'version': '0.1.1',
    'description': 'linkml-renderer',
    'long_description': '# linkml-renderer\n\nGenerating HTML, Markdown, Mermaid, and other rendering artefacts from LinkML data.\n\nThis applies a configurable *generic* mapping between instance data and the target output file.\nThis is an example of a "no code" approach to generating visual representations of data.\n\nIn general, writing custom code (e.g. in Jinja) that is specific to your schema may produce\nmore user-friendly results. LinkML-renderer should only be used in cases where it is harder to\ncommit developer resources to writing custom code.\n\nStatus: experimental\n\n## Command Line Usage\n\nMinimally, you must pass in a schema (LinkML YAML) and a file of instance data conforming to the schema:\n\n`linkml-render -s my-schema.yaml my-data.yaml`\n\nor with a specific output file:\n\n`linkml-render -s my-schema.yaml my-data.yaml -o output.html`\n\nThe default output type is HTML.\n\nTo produce other formats:\n\n`linkml-render -s my-schema.yaml -f markdown my-data.yaml -o output.md`\n\nYou can pass in a configuration file using `--config` (`-c).\n\n`linkml-render -s my-schema.yaml  my-data.yaml -c my-config.yaml`\n\nThe YAML file should conform to the style datamodel Configuration object.\n(note: autodocumentation for this model will be produced later, for now\nconsult the LinkML file).\n\n## Python Usage\n\nWhen this library matures, the python documentation will be linked from the main LinkML docs.\n\nFor now, see the docstrings directly in the source, and the test folder for examples.\n\nSee minimal sphinx docs: https://linkml.github.io/linkml-renderer\n\n## Output types\n\n- HTML\n- Markdown\n- Mermaid\n\nNote that the mermaid can be optionally embedded inside the HTML or Markdown.\n\n## How it works\n\nThe input object is treated as a tree, and nodes in the tree are recursively visited, producing\noutput in the desired format.\n\nFor HTML and markdown generation, the following default rules are applied:\n\n- singular outer objects are translated to Description Lists\n- lists of objects are translated to tables \n\nThese rules are contextual:\n\n- Tables are not nested inside tables\n\nThe rules are also configurable. See the style schema and test cases for details.\n\nFor example, in the person infoschema, a Container contains a list of persons and a list of organizations.\nThe default rendering will create two tables, with each row representing an individual or organization.\n\nThis can lead to wide tables if there are a large number of slots.\n\nIf the `persons` or `organizations` slot is mapped to `RenderType.description_list`, then instead, each item\ngets its own description list, resulting in a longer narrower page.\n\n## Limitations and Future plans\n\nCurrently there are limits to customizability, both in terms of stylesheets and in terms of how schema\nelements map to output elements.\n\nThe HTML generation is currently hardwired to use Bootstrap.\n\nIt is likely that the functionality here may be subsumed into a future linkml.js library. At this time\nthe framework may be extended to include interactive form-based data entry.\n\nThe library has not yet been tested on a wide range of data.\n\n',
    'author': 'Harshad Hegde',
    'author_email': 'hhegde@lbl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
