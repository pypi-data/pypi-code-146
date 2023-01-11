#from distutils.core import setup
import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("LICENSE",'r') as f:
    license = f.read()

setup(
name="tcranno",
version="1.0.2",
description="TCR repertoire specificity annotation toolkit",
long_description = long_description,
long_description_content_type="text/markdown",
author="LUO Jiaqi",
include_package_data=True,
zip_safe=True,
url="https://github.com/deepomicslab/TCRanno",
#packages=setuptools.find_packages(),
classifiers=["Programming Language :: Python :: 3","License :: OSI Approved :: MIT License","Operating System :: OS Independent",],
py_modules=['tcranno.core_analysis', 'tcranno.repertoire_analysis','tcranno.model_predict'],
packages=['tcranno'],
package_dir={'tcranno': 'tcranno'},
package_data={'tcranno': ['data/*.pkl', 'pretrained/pretrained_encoder.h5', 'example/example.sh', 'example/example.py','example/example_input_repertoire.tsv']},
#license=license,
)
