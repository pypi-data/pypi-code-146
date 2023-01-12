
from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ImageSteganography',
  version='1.0.0',
  description='With this library you can hide any message inside an image.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/jkdxbns',  
  author='Justin Mascarenhas',
  author_email='jmascarenhas1998@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Image_Steganography', 
  packages=find_packages(),
  install_requires=['opencv-python', 'numpy'] 
)
