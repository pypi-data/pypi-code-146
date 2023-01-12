# -*- coding: utf-8 -*-
# Copyright (c) 2023 Miroslav Hruska
"""
The setup script for the daul package. 
"""

#%% Modules
import os
from setuptools import setup, find_packages

#%% Reading of readme
cwd = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(cwd, 'README.rst')) as h:
  long_description = h.read()

#%% Actual setup
setup(
  name="daul",
  version='0.1.0',
  description="Data analysis and other utilities for python.", 
  long_description=long_description, 
  long_description_content_type='text/x-rst',
  #   
  author="Miroslav Hruska",
  author_email="hruska.miro@gmail.com", 
  #   
  url='https://github.com/hruskamiro/daul', 
  keywords="data analysis utilities",
  classifiers=[
    "License :: OSI Approved :: MIT License",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent", 
  ],
  # 
  packages=find_packages(),
  #   
  python_requires='>=2.7,<3', 
  #   
  install_requires=['numpy>=1.16.5,<1.17', 
                    'pandas>=0.24.2,<0.25', 
                    'fplib>=0.1.1,<0.2',
                    'pathlib>=1.0.1,<1.1']
)
