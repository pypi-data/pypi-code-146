## configuracion de la instalacion del distribuible
from setuptools import setup, find_packages

setup(
    name='Mensajes-RoollAvendano',
    version='6.0',
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
## luego python -m build para generar 
# la nueva version y distrnuibles
## ahora para comprobar si todo los paquetes estan coprrectamenmte creadios}
## y se pueden publicar
## python -m twine check dist/* ( antes eliminamos los tar anteriores)

##luego otra vez python -m build, para volver a construir el tgz., rar, y ahora volver
## a chequear con python -m twine check dist/* y ahora debe pasar.
# ahora ya se han geenrado lños distrubuible publicos, y ahora podemos publicarlos
## ahora lo que voya  subir es los tar dentro de dist
## con python -m twine upload -r testpypi dist/* ( para todos los paquetes dentro de dist)
##te pide usuario y contraseña en la web de prueba testpypi

##instala en int3net, y me slae un linck, al que puedo acceder
##ahora incluso de puede decarhgar e instalar con ese link en un ambiente python
## y lo verifico con pip list
## luegoi piuedo desintslar todo las librerias, mensajkes-avendnao, y el numpy
#ahpra una vez comprpnado, lo subo a la pagina oficial con el comando
#python -m twine upload dist/*
## luego instalamos el paquete, y debe instalarse yamboen el numpy desde la nuve
## lo puedo instalar desde el comando dos en cualquier sitio
## o desde el visual code
## y luego puedo correr, pero eso si, desde el msdos, tengo que tipeaqr antes python
## para el interprete, igual tengo que hacer en el visual code
## importo y corro
## no olivdar para cualquier actualizacion ejm, en un metodo, preferile boirrar la carpeta
##dist y su contenido, y volver a genrar el dsitrbuible con python -m build
## luego chequear con python -m twine check dist/*
##luego subo al repositorio oficial con python -m twine upload dist/*
## luego ya puedo descarlao desde el msdos o visual code con:
##pip install Mensaje-RoollAvendano --upgrade (con upgrade se desintalaza la version anterior
# # y se reemplaza con la nueva)) ( no es necesario el interporete de python, esto se hace para correr en si el paquete con 
# # from import y esas cosas)
##Mensaje -RoollAendano es el nombre del paquete tal como esta en el setup y tal como se subio

