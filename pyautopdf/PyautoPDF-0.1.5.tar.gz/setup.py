from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.rst")) as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.5'
DESCRIPTION = 'Business Report Automation'

# Setting up
setup(
    name="PyautoPDF",
    version=VERSION,
    author="Shailesh Suthar",
    author_email="shaileshsuthar676@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['openpyxl', 'pywin32'],
    keywords=['python', 'PDF', 'PDF automation', 'documentation', 'report automation', 'report'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
