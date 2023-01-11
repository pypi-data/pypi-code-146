from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Retro3D',
  version='1.01',
  description='3d engine',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Deepak Deo',
  author_email='deepakbr14@yahoo.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='3d game engine software rendering', 
  packages=find_packages(),
  install_requires=['numpy', 'pygame'],
)