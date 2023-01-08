from setuptools import setup, find_packages
import sys
sys.path.append('src')
from quiltz.messaging.version import version

with open("README.md", "r") as fh:
  long_description = fh.read()

with open("requirements/prod.txt", "r") as fh:
  requires = fh.readlines()

setup(
  name='quiltz-messaging',  
  version=version,
  author="Rob Westgeest",
  author_email="rob@qwan.eu",
  description="A messaging utility module for python",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/qwaneu/quiltz-messaging",
  package_dir={'':'src'},
  packages=find_packages(where='src'),
  install_requires=requires,
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
)
