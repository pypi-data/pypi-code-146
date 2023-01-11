"""nifti2gif setup."""

import os

from setuptools import setup, find_packages

VERSION = '0.0.4'

setup(name='nifti2gif',
      version=VERSION,
      description='Create GIF from NIfTI image.',
      long_description_content_type='text/markdown',
      long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
      author='Mikolaj Buchwald',
      author_email='mikolaj.buchwald@gmail.com',
      url='https://github.com/mikbuch/nifti2gif',
      license='BSD 3-Clause License',
      packages=find_packages(),
      install_requires=['numpy', 'nibabel', 'imageio', 'matplotlib'],
      keywords=['nifti', 'gif'],
      entry_points={'console_scripts': [
          'nifti2gif = nifti2gif.__main__:main']},
      zip_safe=False,
      include_package_data=True,
      )
