from setuptools import setup, find_packages

VERSION = '0.0.7' 
DESCRIPTION = 'Pacote para conexão com a API do Mercado Livre'
LONG_DESCRIPTION = 'Pacote em Python trazendo conexões fáceis com os endpoints da API do Mercado Livre'

# Setting up
setup(
    name="meli-package", 
    version=VERSION,
    author="Gabriel Celestino",
    author_email="<gabrielceles1410@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],

    keywords=['python', 'mercadolivre', 'meli'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)