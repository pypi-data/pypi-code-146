# -*- coding:utf-8 -*-
import os
from importlib.machinery import SourceFileLoader
from setuptools import setup, find_packages

version = (
    SourceFileLoader("waveletai._version", os.path.join("waveletai", "_version.py")).load_module().get_versions()
)

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setup(name='waveletai',
      version=version,
      packages=find_packages(exclude=['tests', 'tests.*']),  # 查找包的路径
      include_package_data=False,
      package_data={'waveletai': [""]},
      description='WaveletAI A Machine Learning Lifecycle Platform',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Janus',
      url='https://ai.xiaobodata.com/',
      keywords='ml ai waveletai',
      classifiers=[
          'Intended Audience :: Developers',
          'Development Status :: 4 - Beta',
          'Programming Language :: Python :: 3.7',
          'Natural Language :: Chinese (Simplified)',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
      ],
      python_requires='>=3.6',
      project_urls={
          'wavelet-plus': 'https://plus.xiaobodata.com/',
          'wavelet-ai': 'https://ai.xiaobodata.com/'
      },
      install_requires=[
          'pymysql',
          'boto3',
          'Minio',
          'mlflow>=1.27, <=1.29',
          'jsonschema==3.2.0',
          'bravado',
          'pika',
          'tqdm',
          'simplejson',
          'future>=0.17.1',
          'requests-oauthlib>=1.0.0',
          'oauthlib>=2.1.0',
          'protobuf<=3.20.1'
      ],
      entry_points={
          # Define a Tracking Store plugin for tracking URIs with scheme 'file-plugin'
          'mlflow.tracking_store': 'waveletai-store=waveletai.mlflow_plugs.tracking_store:WaveletAIStore',
          'mlflow.project_backend': 'waveletai-backend=waveletai.mlflow_plugs.project_backend:WaveletAIBackend',
          'mlflow.artifact_repository': 'waveletai-artifact-repository=waveletai.mlflow_plugs.artifact_repository:WaveletAIArtifactRepository',
      }
      )
