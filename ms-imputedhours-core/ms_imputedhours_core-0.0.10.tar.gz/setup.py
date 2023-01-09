from setuptools import setup, find_packages
from ms_imputedhours_core import __version__
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

setup(
      name='ms_imputedhours_core',
      version=__version__,
      packages=find_packages(),
      author='Jonathan Rodriguez Alejos',
      author_email='jrodriguez.5716@gmail.com',
      install_requires=open('requirements.txt').read().splitlines(),
      long_description=long_description,
      long_description_content_type='text/markdown'
)