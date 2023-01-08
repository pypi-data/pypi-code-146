from .. import BASE_PATH

def create_module(app, api):
    
    from .resources import ConfigInstance
     
    api.add_resource(
        ConfigInstance,
        BASE_PATH + '/config/<int:version_code>'
    )