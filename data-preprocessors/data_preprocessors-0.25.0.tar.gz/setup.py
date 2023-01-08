# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_preprocessors']

package_data = \
{'': ['*']}

install_requires = \
['bnlp-toolkit>=3.1.2,<4.0.0', 'nltk>=3.7,<4.0', 'pandas==1.3.0']

setup_kwargs = {
    'name': 'data-preprocessors',
    'version': '0.25.0',
    'description': 'An easy to use tool for Data Preprocessing specially for Text Preprocessing',
    'long_description': '<div align="center">\n    \n<img src="https://github.com/MusfiqDehan/data-preprocessors/raw/master/branding/logo.png">\n\n<p>Data Preprocessors</p>\n\n<sub>An easy to use tool for Data Preprocessing specially for Text Preprocessing</sub>\n\n<!-- Badges -->\n\n<!-- [<img src="https://deepnote.com/buttons/launch-in-deepnote-small.svg">](PROJECT_URL) -->\n[![](https://img.shields.io/pypi/v/data-preprocessors.svg)](https://pypi.org/project/data-preprocessors/)\n[![Downloads](https://img.shields.io/pypi/dm/data-preprocessors)](https://pepy.tech/project/data-preprocessors)\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1mJuRfIz__uS3xoFaBsFn5mkLE418RU19?usp=sharing)\n[![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/keras-team/keras-io/blob/master/examples/vision/ipynb/mnist_convnet.ipynb)\n\n</div>\n\n## **Table of Contents**\n\n- [Installation](#installation)\n- [Quick Start](#quick-start)\n- [Features](#features)\n    - [Split Textfile](#split-textfile)\n    - [Build Parallel Corpus](#build-parallel-corpus)\n    - [Separate Parallel Corpus](#)\n    - [Remove Punctuation](#remove-punctuation)\n    - [Space Punctuation](#space-punctuation)\n    - [Text File to List](#text-file-to-list)\n    - [List to Text File](#list-to-text-file)\n    - [Count Characters of a Sentence](#)\n    - [Count Words of Sentence](#)\n    - [Count No of Lines in a Text File](#)\n    - **[Apply Any Function in a Full Text File](#)**\n\n    \n\n## **Installation**\nInstall the latest stable release<br>\n**For windows**<br>\n```\npip install -U data-preprocessors\n```\n\n**For Linux/WSL2**<br>\n```\npip3 install -U data-preprocessors\n```\n\n## **Quick Start**\n\n```python\nfrom data_preprocessors import text_preprocessor as tp\nsentence = "bla! bla- ?bla ?bla."\nsentence = tp.remove_punc(sentence)\nprint(sentence)\n\n>> bla bla bla bla\n```\n\n## **Features**\n\n### Split Textfile\n\nThis function will split your textfile into train, test and validate. Three separate text files. By changing `shuffle` and `seed` value, you can randomly shuffle the lines of your text files.\n\n```python\nfrom data_preprocessors import text_preprocessor as tp\ntp.split_textfile(\n    main_file_path="example.txt",\n    train_file_path="splitted/train.txt",\n    val_file_path="splitted/val.txt",\n    test_file_path="splitted/test.txt",\n    train_size=0.6,\n    val_size=0.2,\n    test_size=0.2,\n    shuffle=True,\n    seed=42\n)\n\n# Total lines:  500\n# Train set size:  300\n# Validation set size:  100\n# Test set size:  100\n```\n\n### Separate Parallel Corpus\n\nBy using this function, you will be able to easily separate `src_tgt_file` into separated `src_file` and `tgt_file`.\n\n```python\nfrom data_preprocessors import text_preprocessor as tp\ntp.separate_parallel_corpus(src_tgt_file="", separator="|||", src_file="", tgt_file="")\n```\n\n### Remove Punctuation\n\nBy using this function, you will be able to remove the punction of a single line of a text file.\n\n```python\nfrom data_preprocessors import text_preprocessor as tp\nsentence = "bla! bla- ?bla ?bla."\nsentence = tp.remove_punc(sentence)\nprint(sentence)\n\n# bla bla bla bla\n```\n\n### Space Punctuation\n\nBy using this function, you will be able to add one space to the both side of the punction so that it will easier to tokenize the sentence. This will apply on a single line of a text file. But if we want, we can use it in a full twxt file.\n\n```python\nfrom data_preprocessors import text_preprocessor as tp\nsentence = "bla! bla- ?bla ?bla."\nsentence = tp.space_punc(sentence)\nprint(sentence)\n\n# bla bla bla bla\n```\n\n### Text File to List\n\nConvert any text file into list.\n\n```python\n mylist= tp.text2list(myfile_path="myfile.txt")\n```\n\n### List to Text File\n\nConvert any list into a text file (filename.txt)\n\n```python\ntp.list2text(mylist=mylist, myfile_path="myfile.txt")\n```\n\n### Apply a function in whole text file\n\nIn the place of `function_name` you can use any function and that function will be applied in the full/whole text file.\n\n```python\nfrom data_preprocessors import text_preprocessor as tp\ntp.apply_whole(\n    function_name, \n    myfile_path="myfile.txt", \n    modified_file_path="modified_file.txt"\n)\n```\n\n',
    'author': 'Md. Musfiqur Rahaman',
    'author_email': 'musfiqur.rahaman@northsouth.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MusfiqDehan/data-preprocessors',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
