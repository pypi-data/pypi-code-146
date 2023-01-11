from . import dirs

from pathlib import Path
from cryptography.fernet import Fernet
from sqlalchemy import create_engine as ce

__all__ = ['SQLConnector',]

class SQLConnector():
    
    def __init__(
        self,
        host= None,
        port= None,
        usr = None,
        pwd = None,
        db = None,
        db_type = None,
        db_dialect = None,
        conectar=False
        ):
        
        self._host = None
        self._port = None
        self._usr = None
        self._pwd = None
        self._db = None
        self._db_type = None
        self._db_dialect = None
        self._conexion = None
        self._motor = None
        self._conectado = None

        has_some_init_params = host or port or usr or pwd or db or db_type
        if not has_some_init_params:
            try:
                self.__configurar_login()
            except:
                print('No se logró leer automáticamente la configuración privada del conector SQLL')
            
        has_all_init_params = host and port and usr and pwd and db and db_type
        if has_all_init_params:
            self.host = host 
            self.port = port 
            self.usr = usr 
            self.pwd = pwd 
            self.db = db 
            self.db_type = db_type
            self.db_type = db_dialect #Opcional
            
        if has_some_init_params and not has_all_init_params:
            print('Configuración del conector SQL incompleta, por favor ingresar los parámetros:')
            print('host')
            print('port')
            print('user')
            print('password')
            print('db')
            print('db_type')
            print('db_dialect')
        
        all_params_configured = self.host and self.port and self.usr and self.pwd and self.db and self.db_type
        if all_params_configured:
            self.motor = self.crear_motor()
        
        self.conectado = False
        if conectar:
            self.conectar()
        
    @property
    def host(self):
        return self._host
    
    @host.setter
    def host(self,val):
        self._host = val

    @property
    def port(self):
        return self._port
    
    @port.setter
    def port(self,val):
        self._port = val

    @property
    def usr(self):
        return self._usr
    
    @usr.setter
    def usr(self,val):
        self._usr = val
    
    @property
    def pwd(self):
        return self._pwd
    
    @pwd.setter
    def pwd(self,val):
        self._pwd = val
    
    @property
    def db(self):
        return self._db
    
    @db.setter
    def db(self,val):
        self._db = val

    @property
    def db_type(self):
        return self._db_type

    @db_type.setter
    def db_type(self,val):
        self._db_type = val
    
    @property
    def db_dialect(self):
        return self._db_dialect
    
    @db_dialect.setter
    def db_dialect(self,val):
        self._db_dialect = val
    
    @property
    def motor(self):
        return self._motor
    
    @motor.setter
    def motor(self,val):
        self._motor = val
    
    @property
    def conexion(self):
        return self._conexion
    
    @conexion.setter
    def conexion(self,val):
        self._conexion = val
        if not val is None:
            self.conectado = 'actualizar_status'
    
    @property
    def conectado(self):
        return self._conectado
    
    @conectado.setter
    def conectado(self,val):
        '''Note that "val" is not used'''
        try:
            self._conectado = not self.conexion.closed
        except:
            self._conectado = val
    
    def __leer_parametros_encriptados(self):
        '''Lee los parámetros encriptados para conectarse a la BD.'''

        ruta = dirs.get_dc_cfg() 
        file_cfg = Path(ruta + '\\' + 'cfg.db')
        
        txt_enc = file_cfg.read_text()
        
        key = 'chcoJbbFgDtz1dZIDg9g2JIfcCcTlG33q8I3SIJEixE='
        f = Fernet(key)

        txt = f.decrypt(txt_enc)
        txt = txt.decode()
        
        return txt

    def __obtener_parametros(self,):
        '''Convierte el texto de parámetros a un diccionario'''
        
        params = self.__leer_parametros_encriptados()
        
        d = locals()
        exec(f"dct = {params}",globals(), d)
        return d['dct']

    def __configurar_login(self):

        p = self.__obtener_parametros()

        self.host = p['host']
        self.port = p['port']
        self.usr = p['usr']
        self.pwd = p['pwd']
        self.db = p['db']
        self.db_type = p['db_type']
        self.db_dialect = p['db_dialect']

    def crear_motor(
        self,
        host = None, 
        port = None,
        usr = None, 
        pwd = None,
        db = None,
        db_type = None,
        db_dialect = None,
        echo=False,
        future=False
    ):
        '''Crea un objeto "Engine" para interactuar con la base de datos.'''
        if host is None:
            host = self.host
            
        if port is None:
            port = self.port
              
        if usr is None:
            usr = self.usr
            
        if pwd is None:
            pwd = self.pwd
            
        if db is None:
            db = self.db
            
        if db_type is None:
            db_type = self.db_type
            
        if db_dialect is None:
            db_dialect = self.db_dialect
            
        if db_dialect:
            url = f"{db_type}+{db_dialect}://{usr}:{pwd}@{host}:{port}/{db}"
        else:
            url = f"{db_type}://{usr}:{pwd}@{host}:{port}/{db}"

        return ce(url,echo=echo,future=future)

    def conectar(self,mensajes=False):
        '''Intenta conectarse a la base de datos'''
        self.conexion = self.motor.connect()
        
        if mensajes:
            if self.conectado:
                print('Conexión exitosa')
            else:
                print("Imposible conectarse a la Base de Datos del CROM")

    def desconectar(self,mensajes=False):
        
        if self.conectado:
            self._conexion.close()
            self.conexion = self._conexion
        
        if mensajes:
            if not self.conectado :
                print('Desconexión exitosa')
            else:
                print("Error al desconectar.")

    def checkear_conexion(self,mensajes=False):
        if not self.conectado:
            try:
                self.conectar(mensajes=mensajes)
            except:
                pass

        return self.conectado