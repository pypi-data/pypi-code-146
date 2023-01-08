from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='QuantPanda',
  version='0.0.27',
  description='Backtesting Engine',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ashish Ongari',
  author_email='ashishongari@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['backtesting', 'quant', 'algotrading', 'systematictrading', 'trading'], 
  packages=find_packages(),
  install_requires=['pandas_ta', 'pandas', 'numpy','boto3'] 
)