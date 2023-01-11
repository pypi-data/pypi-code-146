# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ipyezannotation',
 'ipyezannotation.annotators',
 'ipyezannotation.studio',
 'ipyezannotation.studio.coders',
 'ipyezannotation.studio.storage',
 'ipyezannotation.studio.storage.sqlite',
 'ipyezannotation.studio.widgets',
 'ipyezannotation.utils',
 'ipyezannotation.widgets']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=8.7.0,<9.0.0', 'ipywidgets>=8.0.3,<9.0.0', 'sqlmodel>=0.0.8,<0.0.9']

setup_kwargs = {
    'name': 'ipyezannotation',
    'version': '0.1.4',
    'description': 'Easy, simple to customize, pythonic data annotation framework.',
    'long_description': '# Easy Annotation\n\n**ipyezannotation** - Easy, simple to customize, pythonic data annotation framework.\n\n# Disclaimer\n\nThis project is in early development stage, so don\'t blame me if it opens-up a black hole in your HDD 😄, \nother than that **IT WORKS!** 🥳\n\nDocs & examples coming soon.\n\n# Dependencies\n\nThis project currently supports `Python>=3.8`.\n\n# Installation\n\nThere are two options to install this project:\n\n- Download and install from PyPI by simply running: `pip install ipyezannotation` & you\'re done!\n- Alternatively, install from source using Poetry. This project uses `poetry>=1.3` to manage dependencies.\n\n# Examples\n\n## Images selection annotation\n\nAnnotation using `ImageSelectAnnotator`.\n\nDefine data to annotate with `ImageSelectAnnotator`:\n\n```python\nsource_groups = [\n    ["./surprized-pikachu.png"] * 16,\n    ["./surprized-pikachu.png"] * 7,\n    ["./surprized-pikachu.png"] * 8,\n    ["./surprized-pikachu.png"] * 4,\n]\n```\n\nConvert input data to `Sample`\'s:\n\n```python\nfrom ipyezannotation.studio.sample import Sample, SampleStatus\n\nsamples = [\n    Sample(\n        status=SampleStatus.PENDING,\n        data=group,\n        annotation=None\n    )\n    for group in source_groups\n]\n```\n\nInitialize database of your liking and synchronize it with your new input samples:\n\n```python\nfrom ipyezannotation.studio.storage.sqlite import SQLiteDatabase\n\ndb = SQLiteDatabase("sqlite:///:memory:")\nsynced_samples = db.sync(samples)\n```\n\nConfigure & create annotation `Studio` to label your samples:\n\n```python\nfrom ipyezannotation.studio import Studio\nfrom ipyezannotation.annotators import ImageSelectAnnotator\n\nStudio(\n    annotator=ImageSelectAnnotator(n_columns=8),\n    database=db\n)\n```\n\n![](./examples/image-select-annotation/output.png)\n\n# Inspiration\n\nLove letter to the following projects coming soon ❤️\n\n- `ipyannotations`\n- `superintendent`\n- `label-studio`\n',
    'author': 'Matas Gumbinas',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gMatas/ipyezannotation',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
