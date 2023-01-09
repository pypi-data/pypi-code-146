from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.4'
DESCRIPTION = 'A python package covering miscellaneous uses. Developed for personal uses.'

# Setting up
setup(
    name="fiiireflyyy",
    version=VERSION,
    author="fiiireflyyy (Willy Lutz)",
    author_email="<lutz0willy@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['scikit-learn', 'umap-learn', 'opencv-python', 'matplotlib', 'tensorflow==2.8.3', 'pandas',
                      'numpy', 'imaris-ims-file-reader', 'zarr', 'seaborn'],
    keywords=['python', 'machine learning', 'deep learning', 'data analysis', 'system management',],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
