# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sonusai',
 'sonusai.data_generator',
 'sonusai.metrics',
 'sonusai.mixture',
 'sonusai.queries',
 'sonusai.utils']

package_data = \
{'': ['*'], 'sonusai': ['data/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'dataclasses-json>=0.5.7,<0.6.0',
 'docopt>=0.6.2,<0.7.0',
 'keras-tuner>=1.1.3,<2.0.0',
 'matplotlib>=3.6.1,<4.0.0',
 'onnxruntime-gpu>=1.12.1,<2.0.0',
 'paho-mqtt>=1.6.1,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'pesq>=0.0.4,<0.0.5',
 'pyaaware>=1.4.7,<2.0.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'setuptools>=65.6.0,<66.0.0',
 'sh>=1.14.3,<2.0.0',
 'sox>=1.4.1,<2.0.0',
 'tensorflow-addons>=0.18.0,<0.19.0',
 'tensorflow>=2.9.0,<2.10.0',
 'tf2onnx>=1.12.1,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['aawscd_probwrite = sonusai.aawscd_probwrite:main',
                     'sonusai = sonusai.main:main']}

setup_kwargs = {
    'name': 'sonusai',
    'version': '0.10.15',
    'description': 'Framework for building deep neural network models for sound, speech, and voice AI',
    'long_description': "Sonus AI: Framework for simplified creation of deep NN models for sound, speech, and voice AI\n\nSonus AI includes functions for pre-processing training and validation data and\ncreating performance metrics reports for key types of Keras models:\n- recurrent, convolutional, or a combination (i.e. RCNNs)\n- binary, multiclass single-label, multiclass multi-label, and regresssion\n- training with data augmentations:  noise mixing, pitch and time stretch, etc.\n\nSonus AI python functions are used by:\n - Aaware Inc. sonusai executable:  Easily create train/validation data, run prediction, evaluate model performance\n - Keras model scripts:             User python scripts for keras model creation, training, and prediction. These can use sonusai-specific data but also some general useful utilities for trainining rnn-based models like CRNN's, DSCRNN's, etc. in Keras\n",
    'author': 'Chris Eddington',
    'author_email': 'chris@aaware.com',
    'maintainer': 'Chris Eddington',
    'maintainer_email': 'chris@aaware.com',
    'url': 'https://aaware.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
