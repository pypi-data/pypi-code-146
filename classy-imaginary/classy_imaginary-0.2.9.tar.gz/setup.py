# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['classy_imaginary',
 'classy_imaginary.enhancers',
 'classy_imaginary.enhancers.phraselists',
 'classy_imaginary.modules',
 'classy_imaginary.modules.diffusion',
 'classy_imaginary.modules.midas',
 'classy_imaginary.modules.midas.midas',
 'classy_imaginary.samplers',
 'classy_imaginary.vendored',
 'classy_imaginary.vendored.blip',
 'classy_imaginary.vendored.clip',
 'classy_imaginary.vendored.clipseg',
 'classy_imaginary.vendored.codeformer',
 'classy_imaginary.vendored.k_diffusion',
 'classy_imaginary.vendored.k_diffusion.models']

package_data = \
{'': ['*'],
 'classy_imaginary': ['configs/*'],
 'classy_imaginary.vendored': ['noodle_soup_prompts/*'],
 'classy_imaginary.vendored.blip': ['configs/*']}

install_requires = \
['Pillow>=8.0.0',
 'click-shell>=2.1',
 'click>=8.0.4',
 'diffusers',
 'einops==0.3.0',
 'fairscale>=0.4.4',
 'ftfy',
 'gfpgan>=1.3.7',
 'imageio==2.9.0',
 'kornia==0.6',
 'llvmlite>=0.39.1,<0.40.0',
 'numpy',
 'omegaconf==2.1.1',
 'open-clip-torch',
 'protobuf!=3.20.2,!=3.19.5',
 'psutil',
 'pytorch-lightning==1.4.2',
 'realesrgan>=0.3.0,<0.4.0',
 'requests',
 'timm>=0.4.12',
 'torch>=1.2.0',
 'torchdiffeq',
 'torchmetrics==0.6.0',
 'torchvision>=0.13.1',
 'tqdm',
 'transformers==4.19.2']

setup_kwargs = {
    'name': 'classy-imaginary',
    'version': '0.2.9',
    'description': 'This is not a useful package. It is a wrapper around imaginary to provide a Class interface.',
    'long_description': 'This is not a useful package. It is a wrapper around imaginary to provide a Class interface.\n',
    'author': 'Hanoush',
    'author_email': 'hanoush87@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
