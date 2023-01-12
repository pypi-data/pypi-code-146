#!/usr/bin/python3
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2012, Edouard DUPIN, all right reserved
##
## @license APACHE v2.0 (see license file)
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
setup(name='karanage-tools',
      version=read_version_file(),
      description='Karanage generic tools',
      long_description=readme(),
      url='https://gitea.atria-soft.org/kangaroo-and-rabbit/karanage',
      author='Edouard DUPIN',
      author_email='yui.heero@gmail.com',
      license='MPL-2',
      packages=['karanage-tools'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Libraries'
      ],
      install_requires=[
          'karanage'
      ],
      long_description_content_type="text/markdown",
      keywords='system cpu status',
      scripts=[
          'bin/karanage-system',
          'bin/karanage-tools-state-get',
          'bin/karanage-tools-state-history-get',
        ],
      include_package_data = True,
      zip_safe=False)

#To developp: sudo ./setup.py install
#             sudo ./setup.py develop
#TO register all in pip: ./setup.py register sdist upload

