import imp
from .. import BASE_PATH

RELATIVE_PATH = BASE_PATH + '/users/me'

def create_module(app, api):
    
    from .resources import UserProfileInstance
    from .preferences import create_module as create_user_preferences_module
    
    api.add_resource(
        UserProfileInstance,
        RELATIVE_PATH
    )

    create_user_preferences_module(app, api)