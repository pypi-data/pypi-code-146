import pyodbc
import pandas as pd
from pathlib import Path

from . import dirs
from . import fechas

from .cl_ApiCammesa import *

__all__ = ['ReporteBase',]

class ReporteBase(ApiCammesa):
    
    def __init__(
        self,
        fecha_i = None,
        fecha_f = None,
        periodo = None,
        nemo_rpt = None,
        nombre = None,
        formato_nombre_archivo = None,
        parques = [],
        extension = None,
        tabla_datos = None,
        tabla_fecha = None,
        col_filtro = None,
        dir_salida = None,
        dir_descarga = None,
        dir_extraccion = None,
        funcion_archivos_necesarios = None,
        
        valores_custom_filtro = {},
        ):
        
        super().__init__()

        self._fecha_i = fechas.hoy() if fecha_i is None else fecha_i
        self._fecha_f = fechas.hoy() if fecha_f is None else fecha_f
        self._periodo = None
        self._nemo_rpt = nemo_rpt
        self._nombre = nombre
        self._formato_nombre_archivo = formato_nombre_archivo
        self._parques = parques
        self._extension = extension
        self._tabla_datos = tabla_datos
        self._tabla_fecha = tabla_fecha
        self._col_filtro = col_filtro
        
        dir_zip = dirs.raiz + '\\00 ZIP'
        dir_ext = dirs.raiz + '\\01 MDB'
        
        self._dir_salida = dirs.raiz if dir_salida == None else dir_salida 
        self._dir_descarga = dir_zip + '\\00 ZIP' if dir_descarga == None else dir_descarga 
        self._dir_extraccion = dir_ext if dir_extraccion == None else dir_extraccion 
        
        self.fan = funcion_archivos_necesarios
        
        self._archivos_necesarios = None
        self._archivos_encontrados = None
        self._archivos_faltantes = None
        self._archivos_disponibles = None
        self._datos = None
        
        #Chequear directorios configurados
        dirs_a_checkear = [
            self._dir_descarga,
            self._dir_descarga ,
            self._dir_extraccion,
        ]
        
        dirs.check_dirs(dirs_a_checkear)
        
        #Actualiza fechas y disponibilidad de archivos
        # Al usar los setters fecha_i y fecha_f se actualizan archivos necesarios/disponibles, etc. automáticamente
        if periodo is None: 
            self.fecha_i = self._fecha_i
            self.fecha_f = self._fecha_f
        else:
            try:
                self.periodo = periodo
            except:
                print("No se pudo procesar el parámetro periodo correctamente.")
                
                self.fecha_i = self._fecha_i
                self.fecha_f = self._fecha_f
                
                print(f"Fecha de inicio {self.fecha_i}")
                print(f"Fecha de fin {self.fecha_f}")
                
        #Actualiza filtros custom
        self.filtro_custom_dict = valores_custom_filtro
        
    @property
    def fecha_i(self):
        return self._fecha_i
    
    @property
    def fecha_f(self):
        return self._fecha_f
    
    @property
    def periodo(self):
        return self._periodo

    @property
    def nemo_rpt(self):
        return self._nemo_rpt
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def formato_nombre_archivo(self):
        return self._formato_nombre_archivo
    
    @property
    def parques(self):
        return self._parques
    
    @property
    def extension(self):
        return self._extension
    
    @property
    def tabla_datos(self):
        return self._tabla_datos
    
    @property
    def tabla_fecha(self):
        return self._tabla_fecha
    
    @property
    def dir_salida(self):
        return self._dir_salida
    
    @property
    def dir_descarga(self):
        return self._dir_descarga
    
    @property
    def dir_extraccion(self):
        return self._dir_extraccion
    
    @property
    def archivos_necesarios(self):
        '''Lista de objetos pathlib.Path representando nombres de archivos con extensión
        No incluyen la ruta absoluta hacia su ubicación teórica'''
        return self._archivos_necesarios

    @property
    def archivos_encontrados(self):
        '''Lista de objetos pathlib.Path con los archivos reales encontrados'''
        return self._archivos_encontrados

    @property
    def archivos_faltantes(self):
        '''Archivos necesarios pero no encontrados
        Lista de pathlib.Path representando nombres de archivos con extensión
        No incluyen la ruta absoluta hacia su ubicación teórica'''
        return self._archivos_faltantes

    @property
    def archivos_disponibles(self):
        '''Combinación de archivos necesarios y encontrados
        Lista de pathlib.Path representando nombres de archivos con extensión
        No incluyen la ruta absoluta hacia su ubicación teórica'''
        return self._archivos_disponibles
    
    @property
    def datos(self):
        return self._datos
    
    @property
    def col_filtro(self):
        return self._col_filtro
    
    @datos.setter
    def datos(self,val):
        self._datos = val
        
    @property
    def fan(self):
        '''Función de Archivos Necesarios: F.A.N. '''
        return self._fan
    
    @archivos_necesarios.setter
    def archivos_necesarios(self,val):
        self._archivos_necesarios = val
    
    @archivos_encontrados.setter
    def archivos_encontrados(self,val):
        self._archivos_encontrados = val
    
    @archivos_faltantes.setter
    def archivos_faltantes(self,val):
        self._archivos_faltantes = val
    
    @archivos_disponibles.setter
    def archivos_disponibles(self,val):
        self._archivos_disponibles = val

    @extension.setter
    def extension(self,val):
        self._extension = val
    
    @fecha_i.setter
    def fecha_i(self,val):
        '''Ingresar una fecha para usar como fecha inicial del rango a analizar/pricesar
        Puede ser un objeto datetime.datetime o texto (string)'''
        fi, ff = fechas.validar_fechas(val,self._fecha_f)
        self._fecha_i = fi
        self._fecha_f = ff
        self._actualizar_archivos()
        
    @fecha_f.setter
    def fecha_f(self,val):
        '''Ingresar una fecha para usar como fecha final del rango a analizar/pricesar
        Puede ser un objeto datetime.datetime o texto (string)'''
        fi, ff = fechas.validar_fechas(self._fecha_i,val)
        self._fecha_i = fi
        self._fecha_f = ff
        self._actualizar_archivos()

    @nemo_rpt.setter
    def nemo_rpt(self,val):
        self._nemo_rpt = val
 
    @nombre.setter
    def nombre(self,val):
        self._nombre = str(val)
    
    @formato_nombre_archivo.setter
    def formato_nombre_archivo(self,val):
        if val is None:
            raise Exception('No se ha ingresado una expresión para codificar los nombres de los archivos.')
        self._formato_nombre_archivo = val
    
    @parques.setter
    def parques(self,val):
        if isinstance(val,(list,set,tuple)):
            str_filter =lambda x: isinstance(x,str)
            results = map(str_filter,val)
            if all(results):
                self._parques = val
            else:
                raise TypeError('Todos los valores dentro de la lista "parques" deben ser del tipo string.')
        else:
            raise TypeError('Se esperaba una lista, set o tuple para la variable "parques".')
            
    @tabla_datos.setter
    def tabla_datos(self,val):
        self._tabla_datos = str(val)
    
    @tabla_fecha.setter
    def tabla_fecha(self,val):
        self._tabla_fecha = str(val)
        
    @col_filtro.setter
    def col_filtro(self,val):
        self._col_filtro = str(val)  
        
    @dir_salida.setter
    def dir_salida(self,val):
        '''Toma una ruta a una carpeta en formato string o como objeto pathlib.Path'''
        self._dir_salida = dirs.check_dir(val)

    @dir_descarga.setter
    def dir_descarga(self,val):
        '''Toma una ruta a una carpeta en formato string o como objeto pathlib.Path'''
        self._dir_descarga = dirs.check_dir(val)
        
    @dir_extraccion.setter
    def dir_extraccion(self,val):
        '''Toma una ruta a una carpeta en formato string o como objeto pathlib.Path'''
        self._dir_extraccion = dirs.check_dir(val)
        
    @fan.setter
    def fan(self,val):
        '''Función de Archivos Necesarios: F.A.N. '''
        if val is None:
            raise Exception('No se ha ingresado una función para calcular los archivos necesarios.')
        self._fan = val
    
    @periodo.setter
    def periodo(self,val):
        if not (val is None):
            fi,ff = fechas.obtener_periodo(val)
            self.fecha_f = ff
            self.fecha_i = fi
            self.fecha_f = ff
            self._periodo = val
            
    def _actualizar_archivos(self):
        
        self.archivos_encontrados = self._obtener_archivos_encontrados()
        self.archivos_necesarios = self._obtener_archivos_necesarios()
        
        existe = lambda x: x.exists()
        no_existe = lambda x: not x.exists()

        self.archivos_faltantes = list(filter(no_existe,self.archivos_necesarios))
        self.archivos_disponibles = list(filter(existe,self.archivos_necesarios))

    def _obtener_archivos_encontrados(self):
        iterable = Path(self.dir_extraccion).iterdir()
        lista_archivos = dirs.filtra_archivos(iterable,self.extension)
        return lista_archivos

    def _obtener_archivos_necesarios(self):
        iterable = self.fan(self.fecha_i,self.fecha_f)  
        lista_nombres = [self._nombre_archivo(fechas[0]) for fechas in iterable]
        lista_nombres = sorted(lista_nombres)
        
        obj_path = lambda x: Path(self.dir_extraccion + '\\' + x)
        
        lista_objetos = [obj_path(archivo) for archivo in lista_nombres]
        
        return lista_objetos

    def _nombre_archivo(self,fecha):
        if self.formato_nombre_archivo is None:
            raise Exception('No se ha ingresado una expresión para codificar los nombres de los archivos.')
        elif self.extension is None:
            raise Exception('No se ha ingresado una extensión de archivo a procesar.')
        
        nombre_puro = fecha.strftime(self.formato_nombre_archivo)
        nombre_completo = nombre_puro + '.' + self.extension
        return nombre_completo.upper()
    
    def extraer(self):
        dirs.extraer(self._dir_descarga, self._dir_extraccion,extension=self.extension)
        self._actualizar_archivos()

    def __get_lista_sql(self):
        '''Tome un iterable de python y lo convierte a un string tipo lista SQL'''
        lista_sql = [f"\'{elemento}\'" for elemento in self.parques]
        lista_sql = ', '.join(lista_sql)
        lista_sql = f"({lista_sql})"
        
        return lista_sql

    def _procesar_archivo(self,archivo):
        
        print(f'Cargando .mdb en la memoria: {archivo}')
   
        #Preparar consultas SQL
        if self.parques:
            lista_sql = self.__get_lista_sql()

            SQL_datos = f'SELECT * FROM {self.tabla_datos} WHERE {self.col_filtro} IN {lista_sql};'
        else:
            SQL_datos = f'SELECT * FROM {self.tabla_datos};'
            
        SQL_fecha = f'SELECT * FROM {self.tabla_fecha};'

        #Preparando conexión con el archivo .mdb
        driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'
        str_conexion = f"Driver={driver};DBQ={str(archivo)};"

        conexion = pyodbc.connect(str_conexion)
        cursor = conexion.cursor()

        #Recuperar datos desde el archivo
        data_archivo = cursor.execute(SQL_datos).fetchall()
        encabezado = ['Fecha',] + [x[0] for x in cursor.description]

        fecha_archivo = cursor.execute(SQL_fecha).fetchall()

        #Colocarle fecha a los registros
        for index,_ in enumerate(data_archivo):
            data_archivo[index] = (fecha_archivo[0][0],) + tuple(data_archivo[index])

        #Cerrar conexión con el archivo
        cursor.close()
        conexion.close()
        df = pd.DataFrame(data_archivo,columns=encabezado)
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
        
        return df

    def _procesar_archivos(self):
        '''Abre y filtra todos los archivos disponibles MDB para los parques seleccionados.
        Devuelve un df de pandas unificado.
        '''
        
        cant_archivos = len(self.archivos_disponibles)
        
        if cant_archivos > 0:
            print(f"Iniciando procesamiento de {cant_archivos} archivos")
            print(f'Ruta de carga: {self.archivos_disponibles[0].parent}')
            # Lista de Dataframes
            dataframes = [self._procesar_archivo(archivo) for archivo in self.archivos_disponibles]
            df = pd.concat(dataframes)
            
            if df.empty:
                print(f"No se encontraron datos para el/los parques: {self.parques}")
            
            return df
        else:
            print(f"No hay archivos para procesar")
            return pd.DataFrame()

    def consultar(self,exportar_consulta=False,dir_consulta=None,filtro=None):
        return super().consultar(
            self.fecha_i,
            self.fecha_f,
            self.nemo_rpt,
            exportar_consulta = exportar_consulta,
            dir_consulta = dir_consulta,
            filtro = filtro
        )
        
    def descargar(self,exportar_consulta=False,dir_consulta=None,filtro=False):
        '''Primero consulta los reportes posibles para descargar, usando la función "consultar" de más arriba.
        Luego descarga la consulta desde una función privada de la clase ApiCammesa.
        
        No pude hacer funcionar un llamado directo a la función "descargar" de la clase ApiCammesa. 
        Me tira conflicto de nombres'''
        super().consultar(
            self.fecha_i,
            self.fecha_f,
            self.nemo_rpt,
            exportar_consulta = exportar_consulta,
            dir_consulta = dir_consulta,
            filtro = filtro
        )
        
        super().descargar_consulta(dir_descarga=self.dir_descarga)
        
        self.extraer()

    def cargar(self,descargar=False,filtro=False,exportar_consulta=False):
        '''Función que realiza la consulta en CAMMESA por en un rango de fechas, descarga los archivos .zip,
        extrae los archivos .mdb dentro de los archivos .zip, 
        filtra la tabla del archivo MDB seleccionada según el listado de parques provisto
        la columna provista y devuelve el resultado como un dataframe de pandas
        '''
        
        if descargar == True:
            self.descargar(
                exportar_consulta=exportar_consulta,
                dir_consulta=None, 
                filtro=filtro
            )

        #Hay que encontrar los archivos acá
        if self.archivos_disponibles:
            self._datos = self._procesar_archivos()
        else:
            raise Exception(f'No hay archivos disponibles para cargar entre las fechas {self.fecha_i} y {self.fecha_f}')
        
        if self._datos.empty:
            print("No se logró cargar datos para la configuración actual.")
        
        return self._datos
    
    def a_excel(self,descargar=False,filtro=False,exportar_consulta=False):
        '''Exporta a excel un dataframe de pandas con una tabla carga del PPO de CAMMESA.
        Previamente filtra por un listado de MNEMOTÉCNICOS de CAMMESA (parques).

        df_ppo = Dataframe de Pandas con los partes PPO procesados por la función "procesar"
        parques = Listado de MNEMOTÉCNICOS de CAMMESA para filtrar la tabla df_ppo
        dir_out = String con la ruta completa a la carpeta en la cual se exportará el archivo Excel.
        tabla = Tabla PPO a procesar. Se utiliza sólo para nombrar el archivo de salida.
        '''
        
        print("Se exportarán los archivos a formato Excel")
        
        if self._datos is None:
            self.cargar(descargar=descargar,filtro=filtro,exportar_consulta=exportar_consulta)
            
        df = self._datos
        
        if not df.empty:
            fecha_desde_real = df.loc[:,"Fecha"].min().strftime('%y-%m-%d')
            fecha_hasta_real = df.loc[:,"Fecha"].max().strftime('%y-%m-%d')

            # Al convertir la fecha a dt.date, no se puede ejecutar el script dos veces
            df.loc[:,"Fecha"] = df.loc[:,"Fecha"].dt.date

            prefijo = f'{self.nombre} {self.tabla_datos}'
            rango_fechas = f'{fecha_desde_real} a {fecha_hasta_real}'

            if len(self.parques) == 1: 
                nombre_archivo = f"{prefijo} {self.parques[0]} {rango_fechas}.xlsx"
            else:
                nombre_archivo = f"{prefijo} {rango_fechas}.xlsx"
                
            if self.dir_salida is None:
                ruta_salida = nombre_archivo
            else:
                ruta_salida = self.dir_salida + '\\' + nombre_archivo

            df.to_excel(ruta_salida, index=False,engine='openpyxl')
            
            # Con esta línea, los datos se vuelven a convertir en formato dt.datetime y el script se puede correr varias veces.
            df.loc[:,"Fecha"] = pd.to_datetime(df.loc[:,"Fecha"],format='%Y-%m-%d')