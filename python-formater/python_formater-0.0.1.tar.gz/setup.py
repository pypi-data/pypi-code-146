from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='python_formater',
  version='0.0.1',
  description='format the python code',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Rakesh M',
  author_email='rakesh.manjunath21@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='code formater', 
  packages=find_packages(),
  install_requires=[''] 
)