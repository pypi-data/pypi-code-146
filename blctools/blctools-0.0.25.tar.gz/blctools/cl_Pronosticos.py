import json
import pandas as pd
import datetime as dt
import requests as req

from . import dirs

from .cl_UsuarioCammesa import *

__all__ = ['Pronosticos']

class Pronosticos(UsuarioCammesa):
    
    def __check_son_numeros(self,iterable):
        es_numero = lambda x: isinstance(x,(int,float))
        return all(map(es_numero,iterable))
        
    def __check_son_string(self,iterable):
        es_string = lambda x: isinstance(x,str)
        return all(map(es_string,iterable))

    def __check_id_parques(self,id_parques):
        
        if isinstance(id_parques,(list,set,tuple)):
            todos_numeros = self.__check_son_numeros(id_parques)
            if not todos_numeros:
                raise TypeError('Todos los valores de ID_Parque deben ser del tipo Int o Float') 

        elif isinstance(id_parques,dict):
            todos_numeros = self.__check_son_numeros(id_parques.values())
            todos_strings = self.__check_son_string(id_parques.keys())

            if not todos_numeros:
                raise TypeError('Todos los valores del diccionario ID_Parque deben ser del tipo Int o Float')
            
            elif not todos_strings:
                raise TypeError('Todos las llaves del diccionario ID_Parque deben ser del tipo String') 
        
        elif isinstance(id_parques,(int,float,str)):
            pass  
        
        elif isinstance(id_parques,str):
            pass
        
        else:
            raise TypeError('La lista de IDs de parques para pedir pronósticos debe ser del tipo Tuple, List, Set o Dict.\nO bien ser un único número')

    def __hora_op(self,fecha):
        return fecha.hour +1

    def __fecha_op(self,fecha):  
        if (fecha.hour +1) == 24 :
            return (fecha.date() - dt.timedelta(days=1))
        else:
            return fecha.date()

    def _consultar_pronostico_viejo(self,id_parque,nombre_parque=None):
        '''
        Función para solicitar los pronósticos de los parques.
        La estructura de la respuesta es:
            respuesta = {ID_parque : respuesta_API}
                respuesta_API = {
                    ID_solicitud
                    ID_parque
                    pronóstico
                    }
            pronóstico = {time, kW}
        '''
        if not self.check_credenciales():
            raise SystemError('Imposible descargar pronósticos. Credenciales inválidas o sin conexión')

        url = f'https://cdspronosticos.cammesa.com/pronosticos/api/pronosticos/findPronostico?central={id_parque}'

        header = {'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Bearer {self._token["access_token"]}'
                }
        
        r = req.get(url, headers=header)
        r_parsed = json.loads(r.text)
        
        #Retransmite errores de la API en caso de haber
        if 'pronosticos' not in r_parsed:
            raise SystemError(r_parsed['message'])

        #Continuar si todo está OK
        df = pd.DataFrame(data=r_parsed['pronosticos'])
        
        df['Park_ID'] = id_parque
        
        if isinstance(nombre_parque,str) or (nombre_parque is None):
            df['UC'] = nombre_parque
        else:
            raise TypeError('El parámetro "nombre_parque" debe ser del tipo String o None')
        
        return df
    
    def _consultar_pronostico_nuevo(self,id_parque,nombre_parque=None):
        if not self.check_credenciales():
            raise SystemError('Imposible descargar pronósticos. Credenciales inválidas o sin conexión')
    
        url = 'https://cdspronosticos.cammesa.com/v2/api/getPoints'
        header = {'Authorization': f'Bearer {self._token["access_token"]}',
                'Content-Type': 'application/json;charset=UTF-8'
            }
    
        #Esta nueva API tiene una TONELADA de datos que se están desaprovechando
        # ver cómo consumirlos en modo pronóstico y en RT
        
    def consultar_pronosticos(self,id_parques,pronostico='viejo'):

        self.__check_id_parques(id_parques)
        
        #Determina la función de consulta de pronóstico a utilizar
        if pronostico == 'viejo':
            funcion = self._consultar_pronostico_viejo 
        else:
            funcion = self._consultar_pronostico_nuevo
        
        #Listado de IDs, sin nombre
        if isinstance(id_parques,(list,tuple,set)):
            lista_dfs = [funcion(int(id)) for id in id_parques]
        
        #Listado de IDs, con nombre (diccionario)
        elif isinstance(id_parques,dict):
            lista_dfs = [funcion(int(id),n) for id, n in id_parques.items()]
            
        #Si pusieron un número en formato string y con cero: ejemplo 781.0
        else:
            id = int(float(id_parques))
            funcion(id)

        df = pd.concat(lista_dfs,ignore_index=True).rename(columns={'kw':'MWh'})
        
        df['time'] = pd.to_datetime(df['time'],format='%Y-%m-%dT%H:%M:%S')
        df['Fecha'] = df['time'].apply(self.__fecha_op)
        df['Hora'] = df['time'].apply(self.__hora_op)
        df['MWh'] = df['MWh'] /1000

        return df.loc[:,['Fecha','Hora','UC','MWh','Park_ID']]
    
    def descargar_pronosticos(self,id_parques,dir_descarga=None):
        if dir_descarga is None:
            dir_descarga = ''
        else:
            dir_descarga = dirs.check_dir(dir_descarga) + '\\'
        
        print(f'Se descargarán los pronósticos en:\n{dir_descarga}')
        
        fecha_salida = dt.datetime.now().strftime("%d-%m-%y %H-%M")
        nombre_archivo = f'Pronosticos_CAMMESA_{fecha_salida}.xlsx'
        ruta_salida = dir_descarga + nombre_archivo
        
        df = self.consultar_pronosticos(id_parques)
        df.to_excel(ruta_salida,index=False)