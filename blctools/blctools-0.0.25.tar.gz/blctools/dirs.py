import zipfile as __zipfile
from pathlib import Path as __Path

from .cl_CarpetaServicios import __CarpetaServicios

Servicios = __CarpetaServicios()

def indicar_ruta(nueva_ruta):
    
        Servicios.ruta = nueva_ruta
        Servicios.ruta_encontrada=True

raiz = str(__Path.cwd())

def get_servicios():
    '''Ubica la ruta a la carpeta "SERVICIOS" de la nube de BLC pero ejecutada desde una computadora personal.'''

    if Servicios.ruta_encontrada:
        return Servicios.ruta
    else:
        raise ValueError('No se ha especificado una ruta para la carpeta de Servicios.')

def get_dc_cfg():
    return get_servicios() + '\\03 ASSET-CROM\\06 Datos Crudos\\04 blctools'

def get_dc_cammesa():
    '''Devuelve la ruta a la carpeta "06 Datos Crudos" en la nube de BLC, asociado a la pc personal'''
    return get_servicios() + '\\03 ASSET-CROM\\06 Datos Crudos\\03 CAMMESA'

def get_dc_ppod():
    '''Devuelve la ruta a la carpeta de PPOs diarios en la carpeta de datos crudos de AM'''
    return get_dc_cammesa() + '\\01 PPO D UNIF'

def get_dc_ppodi():
    '''Devuelve la ruta a la carpeta de PPOs diarios en la carpeta de datos crudos de AM'''
    return get_dc_cammesa() + '\\01 PPO D I'

def get_dc_ppodf():
    '''Devuelve la ruta a la carpeta de PPOs diarios en la carpeta de datos crudos de AM'''
    return get_dc_cammesa() + '\\01 PPO D F'

def get_dc_dtei():
    '''Devuelve la ruta a la carpeta de DTES Iniciales en la carpeta de datos crudos de AM'''
    return get_dc_cammesa() + '\\02 DTE I'

def get_dc_dtef():
    '''Devuelve la ruta a la carpeta de DTES Iniciales en la carpeta de datos crudos de AM'''
    return get_dc_cammesa() + '\\02 DTE F'

def get_dc_dte():
    '''Devuelve la ruta a la carpeta de DTES Iniciales en la carpeta de datos crudos de AM'''
    return get_dc_cammesa() + '\\02 DTE UNIF'

def get_dc_pronosticos():
    '''Devuelve la ruta a la carpeta de DTES Iniciales en la carpeta de datos crudos de AM'''
    return get_dc_cammesa() + '\\03 PRONOSTICOS'

def get_dc_10s():
    '''Ubica la ruta de los archivos 10 segundales, según la pc en la que se ejecute este script'''
    return get_servicios() + '\\03 ASSET-CROM\\06 Datos Crudos\\01 10 segundales'

def get_dc_10s_fecha(fecha):
        return get_dc_10s() + '\\' + fecha.strftime('%Y-%m-%d')
                    
def encontrar_archivos_procesables(archivos_necesarios,archivos_disponibles):
    '''Toma una lista de objetos PATH con archivos existentes y una lista de nombres de archivos necesarios a procesar.
    Devuelve una lista de objetos path de aquellos archivos disponibles y necesarios '''
    
    return [archivo for archivo in archivos_disponibles if archivo.stem.upper() in archivos_necesarios]

def encontrar_archivos_faltantes(archivos_necesarios,archivos_disponibles):
    
    archivos_disponibles = [x.stem.upper() for x in archivos_disponibles]
    
    return [archivo for archivo in archivos_necesarios if archivo not in archivos_disponibles]

def _concat_paths(path1,path2):
    return __Path(str(path1)+str(path2))

def check_dir(dir):
    '''Recibe una ruta, bien como objeto pathlib.Path o string
    Si no es una ruta absoluta, asume que es relativa a la dirección desde donde esté corriendo el script.'''
    if isinstance(dir,str):
        dir = __Path(dir)
    elif isinstance(dir,__Path):
        pass
    else:
        raise TypeError('Se esperaba un objeto pathlib.Path o String como variable de entrada')
    
    if not dir.is_absolute():
        dir = _concat_paths(raiz,dir)
    
    try:
        dir.mkdir(parents=True, exist_ok=True)
        return str(dir)
    except:
        raise ValueError(f'No se pudo crear el directorio:\\n{dir}') 

def check_dirs(dir_list):
    """Itera sobre una lista de directiores y les aplica la función check_dir.
    
    dir_list = Lista de directorios a checkear y eventualmente crear
    """
    for dir in dir_list:
        check_dir(dir)

def filtra_archivos(iterable,extension):
    '''busca en un iterable todos los archivos que terminen con la extensión determinada.
    Devuelve una lista de python de archivos con ruta completa como resultado.'''
    
    filtrar_extension = lambda x : str(x).upper().endswith(f'{extension.upper()}')

    return list(filter(filtrar_extension,iterable))

def extraer(dir_zips, dir_extraccion,extension=None):
    '''Busca archivos zip en el directiorio dir_zips. 
    Luego extrae en el directorio dir_extraccion todos los archivos dentro del zip que terminen con la extensión provista '''

    zips_encontrados = filtra_archivos(__Path(dir_zips).iterdir(),'zip')

    for archivo in zips_encontrados:
        
        ruta_archivo = str(archivo)
        
        if __zipfile.is_zipfile(ruta_archivo):
            f = __zipfile.ZipFile(ruta_archivo, mode='r')
        
            archivos_ext = filtra_archivos(f.namelist(),extension)
            
            if archivos_ext:
                for archivo_ext in archivos_ext:
                    f.extract(archivo_ext, path = dir_extraccion)
                    f.close()
                    print(f'Archivo {archivo_ext} extraído.')