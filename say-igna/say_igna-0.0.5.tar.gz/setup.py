from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.5'
DESCRIPTION = 'Descripción paquete pip'
LONG_DESCRIPTION = 'Creando larga paquete pip'

# Setting up
setup(
    name="say_igna",
    version=VERSION,
    author="Ignacio Mendiola Rodriguez",
    author_email="<ignamendi21@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[]
)