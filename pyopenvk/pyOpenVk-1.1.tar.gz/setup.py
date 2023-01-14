from io import open
from setuptools import setup


"""
:authors: Ptushkea
:license: MIT License
:copyright: (c) 2023 Ptushkea
"""

version = '1.1'
'''
with open(README.md, encoding='utf-8') as f:
	long_description = f.read()
'''

long_description = '''Проста у використанні реалізація OpenVk Api'''

setup(
	name='pyOpenVk',
	version=version,

	author='Ptushkea',
	author_email='alyonalisicyna@gmail.com',

	description = (
		u'Проста у використанні реалізація OpenVk Api'
		u'pyOpenVk - python OpenVK Api'
	),
	long_description=long_description,
	long_description_content_type='text/markdown',

	url='https://github.com/ptushkea/pyOpenVk',
	download_url='https://github.com/ptushkea/pyOpenVk/releases',

	license='MIT License, see LICENSE file',

	packages=['pyOpenVk'],
	install_requires=['requests']
)