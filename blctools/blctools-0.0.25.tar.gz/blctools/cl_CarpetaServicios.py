from pathlib import Path


__all__ = ['__CarpetaServicios']


mensaje = """No se ha encontrado la carpeta hacia la nube de BLC.\n
Tendrá que indicar la ruta hacia la carpeta de Servicios manualmente.
Para ello por favor ejecutar el comando: blctools.indicar_ruta('ruta completa')
Mientras tanto se trabajará en la ruta del script actual"""


class __CarpetaServicios():
       
    def __init__(self):
        self._ruta = str(Path.cwd())
        self.ruta_encontrada = False
        
        self.__buscar_dir_segun_carpeta_usuario()
        
        if not self.ruta_encontrada:
            self.__buscar_dir_segun_archivo_py()
            
        if not self.ruta_encontrada:
            self.print_warning
        
    def __buscar_dir_segun_archivo_py(self):
        
        dir_raiz_split = self.ruta.split('\\')
        dir_rel_1 = r'OneDrive - BLCGES\Documentos Produccion\Servicios'
        dir_rel_2 = r'OneDrive - BLCGES\Servicios'
        
        for dir_rel in [dir_rel_1, dir_rel_2]:
            if dir_rel in self.ruta:
                index_dir_servicios = dir_raiz_split.index('Servicios')
                seleccion = dir_raiz_split[0:index_dir_servicios+1]
                
                dir_servicios = '\\'.join(seleccion)
                
                self.ruta = dir_servicios
                self.ruta_encontrada = True
                break
        
    def __buscar_dir_segun_carpeta_usuario(self):
        dir_usr = str(Path.home())
        dir_rel_1 = r'OneDrive - BLCGES\Documentos Produccion\Servicios'
        dir_rel_2 = r'OneDrive - BLCGES\Servicios'
        dir_rel_3 = r'OneDrive - BLCGES'
        
        for dir_rel in [dir_rel_1,dir_rel_2]:
            path_full = Path(dir_usr + '\\' + dir_rel)
            
            if path_full.is_dir() and path_full.exists():
                self.ruta = str(path_full)
                self.ruta_encontrada = True
                break
        
        path_full = Path(dir_usr + '\\' + dir_rel_3)
        if path_full.is_dir() and path_full.exists():
            path_full2 = path_full.joinpath('03 ASSET-CROM')
            if path_full2.is_dir() and path_full2.exists():
                self.ruta = str(path_full)
                self.ruta_encontrada = True

    def print_warning(self):
        if __name__ != '__main__':
            print(mensaje)
            
    @property
    def ruta(self):
        return self._ruta
    
    @ruta.setter
    def ruta(self,val):
        
        if isinstance(val,Path):
            val = str(Path(val))
            
        elif not isinstance(val,str):
            raise TypeError('La ruta ingresada debe ser del tipo String o pathlib.Path')
        
        else:
            obj_path = Path(val)
            
            if not obj_path.is_dir():
                raise ValueError('La ruta especificada aparenta no ser un directorio')
            elif not obj_path.exists():
                raise ValueError('La ruta especificada no existe')
            elif not obj_path.is_absolute():
                raise ValueError('La ruta especificada es relativa, se requiere una ruta completa')
        
            self._ruta = val