# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

# This call to setup() does all the work
setup(
  name="cmtt",
  version="0.8.0",
  description="A library for processing Code Mixed Text. Still in development!",
  long_description_content_type="text/markdown",
  long_description=long_description,
  url="https://cmtt.readthedocs.io/",
  author="Reuben Devanesan",
  author_email="reubendevanesan@gmail.com",
  license="MIT",
  classifiers=[
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Operating System :: OS Independent"
  ],
  dependency_links=[
    'http://download.pytorch.org/whl/cpu/torch-1.0.0-cp36-cp36m-linux_x86_64.whl'
  ],
  # packages=["cmtt", "cmtt/data", "cmtt/preprocessing"],
  packages=find_packages(),
  include_package_data=True,
  data_files=[('cmtt/data', ['cmtt/data/data.json']), ('cmtt/preprocessing/tokenizer', ['cmtt/preprocessing/tokenizer/vocab.txt', 'cmtt/preprocessing/tokenizer/vocab_2.txt'])],
  install_requires=[
    "numpy", 
    "pandas", 
    "requests", 
    "tqdm",
    'fastai==1.0.57',
    "sentencepiece",
    "torch==1.8.0",
    "dill",
    "torchtext==0.9.0",
    "googletrans"
  ]
)
