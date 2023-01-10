#!/usr/bin/env python
# coding: utf-8


import sys
import subprocess
from setuptools import setup


def readme_md_to_rst():
      try:
          return subprocess.check_output(['pandoc', 'README.md', '--to=rst'], universal_newlines=True)
      except Exception:
          print("Failed to convert README.md through pandoc, proceeding anyway")
          return 'Test'


if sys.version_info < (3, 8):
      print('\n\tSF2 requires Python 3.8+\n')
      sys.exit()


setup(name='SignFinder',
      version='2.0.2',
      description='Antivirus evasion toolkit',
      long_description=readme_md_to_rst(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: Public Domain',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Topic :: Security',
        'Topic :: Software Development :: Assemblers',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Disassemblers',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
      ],      
      url='https://github.com/d3ranged/sf2',
      author='d3ranged',
      author_email='d3ranged_blog@proton.me',
      license='Unlicense',
      packages=['SignFinder'],
      install_requires=[
          'prompt-toolkit>=3.0.31', 'rich>=12.5.1', 'pyelftools>=0.29', 'pefile>=2022.5.30', 'capstone>=4.0.2'
      ],
      entry_points = {
        'console_scripts': ['sf2=SignFinder.__main__:cli_start'],
      },
      keywords='security malware hacking pentesting antivirus elf pe av evasion bypass hacking-tool crypter fud antivirus-evasion redteam undetectable',
      include_package_data=True,
      zip_safe=False)

