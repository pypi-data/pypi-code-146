import json
import requests as req

__all__ = ['UsuarioCammesa']

class UsuarioCammesa():
    def __init__(self,usr=None,pwd=None):
        # Se puede dejar hardcodeado o solicitar usr y pwd
        self._usr = usr
        self._pwd = pwd
        self._header = {'Content-Type': 'application/x-www-form-urlencoded'}
        self._scrt = "6a5fd084-fc67-4468-829c-0ff3a68f6ca3"   #Código adicional, provisto por CAMMESA para cada API
        self._token = None

    @property
    def usr(self):
        return self._usr

    @property
    def pwd(self):
        return self._pwd
    
    @usr.setter
    def usr(self,val):
        if not isinstance(val,str):
            raise TypeError('El nombre de usuario debe ser del tipo String')

    @pwd.setter
    def pwd(self,val):
        if not isinstance(val,str):
            raise TypeError('La contraseña debe ser del tipo String')

    def log_in(self):
        url = "https://keycloak.cammesa.com/auth/realms/Cammesa/protocol/openid-connect/token"
        params = {
            'username': self.usr,
            'password': self.pwd,
            'grant_type': 'password',
            'client_id': 'pronosticos',
            'client_secret': self._scrt
        }
        
        #Solicitud de credenciales para la API
        r = req.post(url,headers = self._header,data=params)
        r_parsed = json.loads(r.text)
        
        #Chequear error de usuario y contraseña en la respuesta de la API
        if 'error' in r_parsed:
            print('No se pudo iniciar sesión: Credenciales inválidas')
            self._token = None
        elif not ('access_token' in r_parsed):
            print('No se pudo iniciar sesión: Error desconocido. ')
            self._token = None
        else:
            self._token = r_parsed

    def log_out(self):

        url = 'https://keycloak.cammesa.com/auth/realms/Cammesa/protocol/openid-connect/logout'
        params = {
            'd_refresh_token':self._token['refresh_token'],
            'client_id': 'pronosticos',
            'client_secret': self._scrt}

        req.post(url,headers = self._header,data=params)

    def __check_usr_pwd(self):
        if self.usr is None :
            raise ValueError('Debe ingresar usuario vía la funcion .usr')
        elif self.pwd is None:
            raise ValueError('Debe ingresar contraseña vía la funcion .pwd')
        else:
            return True

    def check_credenciales(self):
        if self.__check_usr_pwd():
            if self._token is None:
                print(f'Forzando inicio de sesión para el usuario {str(self.usr)}')
                self.log_in()
                if self._token is None:
                    print('No se pudo forzar inicio de sesión. Abortando proceso.')
                    return False
        return True