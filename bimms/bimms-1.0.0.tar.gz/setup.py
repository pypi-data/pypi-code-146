from setuptools import setup

setup(
   name='bimms',
   version='1.0.0',
   description='BIMMS python API',
   long_description = 'file: README.md',
   author='Louis Regnacq - Florian Kolbl',
   packages=['bimms'],  #same as name
   include_package_data = True,
   url = 'https://github.com/fkolbl/BIMMS',
   classifiers =[
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent'
     ],
    install_requires=['numpy','andi-py','matplotlib','scipy'], #external packages as dependencies
    python_requires = '>=3.6'
)
