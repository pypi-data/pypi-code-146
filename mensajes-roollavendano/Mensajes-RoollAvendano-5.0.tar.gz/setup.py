## configuracion de la instalacion del distribuible
from setuptools import setup, find_packages

setup(
    name='Mensajes-RoollAvendano',
    version='5.0',
    description='Un paquete para saludar y despedir',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rooll Avendaño',
    author_email='hola@hecto.de',
    url='http://hecto.de',
    license_files=['LICENSE'],
    ## aqui viene lo importante:
    packages=find_packages(),
    scripts=[],
    # ahora cambia para el test
    test_suite='tests',  ## aqui hay que ponerlo como un init.py , para que lo reconozca como un paquete para que lo pueda leer
    ## aqui se pone cuando hay dependencia con un paquete externo, con su version
    ##   install_requires=['numpy>=1.23.0']
    ## o con la compresnion de listas, para una lista de dependencias de paquetes, de un text validado con manifest
    install_requires=[paquete.strip() for paquete in open("requirements.txt").readlines()],

    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python :: 2.3',
    ]
)
## ahora en el terminal, python setup.py sdist paraq distrbuiir, en la carpeta donde esta el setup
## se forma un tar.gz listo para instalarse
## luego desde el terminal accdemos a la carpeta dist
##tipeamos  pip install (nombre completo del tar)
## pip list , debe estar mensajes 1.0
## luefgo probamos, entrando a cmd, tipeamos python
## y ahora poedemos poner from mensajes import *, y sguimos la seguencia, llamando a 
## las funciones y clases y debe funcionaER
## con exit() sales.
## cuando hago nuevas  versiones, hago todo el proceso, pero en pip install pongo --upgrade
## con la nueva modificacion puedo importar por el terminal from mensajes.hola.saludo import generar_array#y luego llamar a la funcion generar_array

## se puede incluir una prueba
## puedo tipear python setup.py test  y funciona

## para prueba se crea una carpte tests, y ahi se lleva el test.py y mas cosas
## y es un test paraq cada subpaquete en  teoria. con el import unittest

## ahora para ejecutar los test ponemos: python setup.py test , este test es palabra clave
## una vez hecho el test, ya puedo crear el nuevo paquete

##para construinr el paquete build, paquete publkico y la publicacion(twine)
## pip install build twine --upgrade
## luego python -m build para generar la nueva version y distrnuibles
## ahora para comprobar si todo los paquetes estan coprrectamenmte creadios}
## y se pueden publicar
## python -m twine check dist/* ( antes eliminamos los tar anteriores)

##luego otra vez python -m build

