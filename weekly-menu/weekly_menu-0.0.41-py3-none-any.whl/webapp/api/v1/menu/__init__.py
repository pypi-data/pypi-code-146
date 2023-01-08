from .. import BASE_PATH

def create_module(app, api):
    
    from .resources import MenuList, MenuInstance, MenuRecipesList, MenuRecipesInstance
    
    api.add_resource(
        MenuList,
        BASE_PATH + '/menus'
    )
    api.add_resource(
        MenuInstance,
        BASE_PATH + '/menus/<string:menu_id>'
    )

    api.add_resource(
        MenuRecipesList,
        BASE_PATH + '/menus/<string:menu_id>/recipes'
    )
    api.add_resource(
        MenuRecipesInstance,
        BASE_PATH + '/menus/<string:menu_id>/recipes/<string:recipe_id>'
    )