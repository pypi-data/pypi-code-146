from .. import BASE_PATH

def create_module(app, api):
    
    from .resources import IngredientsList, IngredientInstance
    
    api.add_resource(
        IngredientsList,
        BASE_PATH + '/ingredients'
    )
    api.add_resource(
        IngredientInstance,
        BASE_PATH + '/ingredients/<string:ingredient_id>'
    )