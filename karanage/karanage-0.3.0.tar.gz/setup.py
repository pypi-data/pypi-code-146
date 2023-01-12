#!/usr/bin/python3
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2023, Edouard DUPIN, all right reserved
##
## @license MPL v2.0 (see license file)
##

from setuptools import setup
import os

def readme():
	with open('README.md') as f:
		return f.read()

def read_version_file():
	if not os.path.isfile("version.txt"):
		return ""
	file = open("version.txt", "r")
	data_file = file.read()
	file.close()
	if len(data_file) > 4 and data_file[-4:] == "-dev":
		data_file = data_file[:-4]
	return data_file

# https://pypi.python.org/pypi?%3Aaction=list_classifiers
setup(name='karanage',
      version=read_version_file(),
      description='Karanage interface is a simple interface to access to the karanage service to send and receive data',
      long_description=readme(),
      url='https://gitea.atria-soft.org/kangaroo-and-rabbit/karanage',
      author='Edouard DUPIN',
      author_email='yui.heero@gmail.com',
      license='MPL-2',
      packages=['karanage'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Libraries'
      ],
      install_requires=[
          'requests'
      ],
      long_description_content_type="text/markdown",
      keywords='kar karanage',
      include_package_data = True,
      zip_safe=False)

#To developp: sudo ./setup.py install --user
#             sudo ./setup.py develop --user
#TO register all in pip: ./setup.py register sdist upload

# https://packaging.python.org/en/latest/tutorials/packaging-projects/
# python3 -m build
# python3 -m twine upload dist/*

