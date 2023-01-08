from .. import RELATIVE_PATH

def create_module(app, api):
    
    from .resources import UserPreferenceList, UserPreferencesInstance
    
    api.add_resource(
        UserPreferenceList,
        RELATIVE_PATH + '/preferences'
    )

    api.add_resource(
        UserPreferencesInstance,
        RELATIVE_PATH + '/preferences/<string:user_prefs_id>'
    )