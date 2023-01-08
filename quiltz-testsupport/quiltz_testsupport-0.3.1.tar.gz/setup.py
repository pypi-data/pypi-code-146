from setuptools import setup, find_packages
import sys
sys.path.append('src')
from quiltz.testsupport.version import version

with open("README.md", "r") as fh:
  long_description = fh.read()

with open("requirements/prod.txt", "r") as fh:
  requires = fh.readlines()

setup(
  name='quiltz_testsupport',  
  version=version,
  author="Rob Westgeest",
  author_email="rob@qwan.eu",
  description="A testsupport utility module for python",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/qwaneu/quiltz-testsupport",
  packages=find_packages(where='src'),
  package_dir={'':'src'},
  package_data={'': ['**/pems/*.pem']},
  include_package_data=True,
  install_requires=requires,
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
)
