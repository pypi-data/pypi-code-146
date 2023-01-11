"""nifti2gif setup."""

from setuptools import setup, find_packages

VERSION = '0.0.1'

setup(name='nifti2gif',
      version=VERSION,
      description='Create GIF from NIfTI image.',
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
