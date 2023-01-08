from setuptools import setup, find_packages, Extension
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='alextoolkit',
  version='0.0.1',
  description='Toolkit for handling day to day tasks around tabular data',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Alex Mendoza',
  author_email='alexander.mendoza.am@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='toolkit', 
  packages=find_packages(),
  install_requires=['os', 'sys'] 
)