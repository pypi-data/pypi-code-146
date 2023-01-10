from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='fakerMM',
  version='0.0.8',
  description='datos sinteticos personalizados',
  long_description=open('README.txt').read() + '\n\n',
  url='',  
  author='Patricia Perez Villegas',
  author_email='',
  license='MIT', 
  classifiers=classifiers,
  keywords='faker', 
  packages=find_packages(),
  install_requires=['faker'] 
)