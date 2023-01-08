from setuptools import setup, find_packages
import sys
sys.path.append('src')
from quiltz.domain.version import version

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
  name='quiltz-domain',  
  version=version,
  author="Rob Westgeest",
  author_email="rob@qwan.eu",
  description="A domain utility module for python",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/qwaneu/quiltz-domain",
  packages=find_packages(where='src'),
  package_dir={'':'src'},
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
)
