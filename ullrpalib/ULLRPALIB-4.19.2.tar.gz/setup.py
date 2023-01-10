import pathlib
from setuptools import find_packages, setup

# https://antonio-fernandez-troyano.medium.com/crear-una-libreria-python-4e841fbd154f

# cd Z:\RPA\RPALIB\0998_LIB_Python\Scripts\
# python setup.py sdist bdist_wheel
# twine upload --repository testpypi dist/ULLRPALIB-0.0.3.tar.gz dist/ULLRPALIB-0.0.3-py3-none-any.whl
# twine upload dist/ULLRPALIB-0.0.5.tar.gz dist/ULLRPALIB-0.0.5-py3-none-any.whl
# python -m pip install -e z:\RPA\RPALIB\0998_LIB_Python\Scripts
# python -m pip install ULLRPALIB
# pip freeze

'''
python -m pip install wheel
python -m pip install twine
z:
cd Z:\RPA\RPALIB\0998_LIB_Python\Scripts
python setup.py sdist bdist_wheel
twine upload dist/ULLRPALIB-3.12.1.tar.gz dist/ULLRPALIB-3.12.1-py3-none-any.whl

python -m pip install ULLRPALIB --upgrade
'''



HERE = pathlib.Path(__file__).parent

VERSION = '4.19.2' # Muy importante, ir cambiando para reflejar el histórico
# El primer numero de la versión es para el número de fuentes de librerías, en este caso 3 da para DatosUXXIEC, Excel, General
# El segundo numero es para el numero total de funciones de la librería sumando todas las fuentes 
# El tercer numumero es para registrar modificaciones y mejoras dentro de la librería

PACKAGE_NAME = 'ULLRPALIB' #Debe coincidir con el nombre de la carpeta 
AUTHOR = 'ULL-RPA' 
AUTHOR_EMAIL = 'gerencia.sce.ticger@ull.edu.es' 
URL = 'https://github.com/RPA-ULL/0998_LIB_Python_Scripts'

LICENSE = 'MIT' #Tipo de licencia
DESCRIPTION = 'Librería para utilidades generales de RPA para Python' #Descripción corta
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') #Referencia al documento README con una descripción más elaborada
LONG_DESC_TYPE = "text/markdown"


#Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
INSTALL_REQUIRES = [
      'openpyxl','pandas','xlrd'
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)