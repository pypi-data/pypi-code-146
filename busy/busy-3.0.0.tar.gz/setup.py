import os
from setuptools import setup
from setuptools import find_packages
from pathlib import Path

with open(os.path.join(os.path.dirname(__file__), 'version')) as versionfile:
    version = versionfile.read().strip()

long_description = (Path(__file__).parent / 'README.md').read_text()

setup(name='busy',
      version=version,
      description='Command-line task and plan management tool',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://gitlab.com/fpotter/tools/busy',
      author='Francis Potter',
      author_email='busy@fpotter.com',
      license='MIT',
      packages=find_packages(),
      entry_points={'console_scripts':['busy=busy.__main__:main']},
      zip_safe=False)
