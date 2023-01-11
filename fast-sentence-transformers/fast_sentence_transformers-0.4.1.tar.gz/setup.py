# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_sentence_transformers',
 'fast_sentence_transformers.examples',
 'fast_sentence_transformers.txtai',
 'fast_sentence_transformers.txtai.models',
 'fast_sentence_transformers.txtai.pipeline',
 'fast_sentence_transformers.txtai.pipeline.train',
 'fast_sentence_transformers.txtai.text']

package_data = \
{'': ['*']}

install_requires = \
['onnx>=1.12.0,<2.0.0',
 'onnxruntime>=1.10,<2.0',
 'psutil>=5.9.2,<6.0.0',
 'sentence-transformers>=2.1.0']

setup_kwargs = {
    'name': 'fast-sentence-transformers',
    'version': '0.4.1',
    'description': 'This repository contains code to run faster sentence-transformers using tools like quantization, ONNX and pruning.',
    'long_description': '# Fast Sentence Transformers\nThis repository contains code to run faster `sentence-transformers` using tools like quantization and `ONNX`. Just run your model much faster, while a lot of memory. There is not much to it!\n\n[![Python package](https://github.com/Pandora-Intelligence/fast-sentence-transformers/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/Pandora-Intelligence/fast-sentence-transformers/actions/workflows/python-package.yml)\n[![Current Release Version](https://img.shields.io/github/release/pandora-intelligence/fast-sentence-transformers.svg?style=flat-square&logo=github)](https://github.com/pandora-intelligence/fast-sentence-transformers/releases)\n[![pypi Version](https://img.shields.io/pypi/v/fast-sentence-transformers.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/fast-sentence-transformers/)\n[![PyPi downloads](https://static.pepy.tech/personalized-badge/fast-sentence-transformers?period=total&units=international_system&left_color=grey&right_color=orange&left_text=pip%20downloads)](https://pypi.org/project/fast-sentence-transformers/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)\n\n# Install\n```bash\npip install fast-sentence-transformers\n```\nOr for GPU support.\n```bash\npip install fast-sentence-transformers[gpu]\n```\n\n# Quickstart\n\n```python\n\nfrom fast_sentence_transformers import FastSentenceTransformer as SentenceTransformer\n\n# use any sentence-transformer\nencoder = SentenceTransformer("all-MiniLM-L6-v2", device="cpu", quantize=True)\n\nencoder.encode("Hello hello, hey, hello hello")\nencoder.encode(["Life is too short to eat bad food!"] * 2)\n```\n\n# Benchmark\nIndicative benchmark for CPU usage with smallest and largest model on `sentence-transformers`. Note, ONNX doesn\'t have GPU support for quantization yet.\n\n| model                                 | Type   | default | ONNX | ONNX+quantized | ONNX+GPU |\n| ------------------------------------- | ------ | ------- | ---- | -------------- | -------- |\n| paraphrase-albert-small-v2            | memory | 1x      | 1x   | 1x             | 1x       |\n|                                       | speed  | 1x      | 2x   | 5x             | 20x      |\n| paraphrase-multilingual-mpnet-base-v2 | memory | 1x      | 1x   | 4x             | 4x       |\n|                                       | speed  | 1x      | 2x   | 5x             | 20x      |\n\n# Shout-Out\n\nThis package heavily leans on `sentence-transformers` and `txtai`.\n',
    'author': 'David Berenstein',
    'author_email': 'david.m.berenstein@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pandora-intelligence/fast-sentence-transformers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
