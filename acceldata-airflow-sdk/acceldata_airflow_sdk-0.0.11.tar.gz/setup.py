from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: Apache Software License',
  'Programming Language :: Python :: 3'
]

setup(
  name='acceldata_airflow_sdk',
  version='0.0.11',
  description='Acceldata Airflow SDK.' + '\n\n' + open('README.txt').read(),
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type="text/markdown",
  url='',
  author='acceldata',
  author_email='apisupport@acceldata.io',
  license='MIT License',
  classifiers=classifiers,
  keywords='acceldata-airflow',
  packages=find_packages(),
  install_requires=['requests', 'dataclasses', 'typing']
)