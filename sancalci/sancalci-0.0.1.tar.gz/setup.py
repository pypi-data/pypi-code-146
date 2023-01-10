from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='sancalci',
  version='0.0.1',
  description='A simple calculator',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='SANTHIYA S',
  author_email='sandhiyas0109@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='basic calculator', 
  packages=find_packages(),
  install_requires=[''] 
)