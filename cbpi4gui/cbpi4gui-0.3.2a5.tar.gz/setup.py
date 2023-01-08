from setuptools import setup
import os
import re


with open(os.path.join(os.path.abspath(os.path.dirname(
        __file__)), 'cbpi4gui', 'version.py'), 'r', encoding='latin1') as fp:
    try:
        match = re.search('.*\"(.*)\"', fp.readline())
        version = match.group(1)
    except IndexError:
        raise RuntimeError('Unable to determine version.')

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

print(version)

setup(name='cbpi4gui',
      version=version,
      description='CraftBeerPi4 User Interface',
      author='Alexander Vollkopf',
      author_email='avollkopf@web.de',
      url='https://openbrewing.gitbook.io/craftbeerpi4_support/',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'cbpi4-ui-plugin': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4gui'],
      long_description=long_description,
      long_description_content_type='text/markdown'
     )
