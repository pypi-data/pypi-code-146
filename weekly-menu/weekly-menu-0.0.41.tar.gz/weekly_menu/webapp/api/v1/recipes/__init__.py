from .. import BASE_PATH

def create_module(app, api):
    
    from .resources import RecipeList, RecipeInstance, RecipeIngredientsList, RecipeIngredientInstance
    
    api.add_resource(
        RecipeList,
        BASE_PATH + '/recipes'
    )
    api.add_resource(
        RecipeInstance,
        BASE_PATH + '/recipes/<string:recipe_id>'
    )

    # TODO remove if not used
    api.add_resource(
        RecipeIngredientsList,
        BASE_PATH + '/recipes/<string:recipe_id>/ingredients'
    )
    api.add_resource(
        RecipeIngredientInstance,
        BASE_PATH + '/recipes/<string:recipe_id>/ingredients/<string:ingredient_id>'
    )