from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'My first Python package'

setup(
       # the name must match the folder name 'verysimplemodule'
        name="sample_taxcal_11", 
        version=VERSION,
        author="MounicaAnju",
        author_email="mounicapothureddy555@gmail.com",
        description=DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)