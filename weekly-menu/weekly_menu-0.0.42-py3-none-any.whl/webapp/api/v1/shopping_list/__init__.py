from .. import BASE_PATH

def create_module(app, api):
    
    from .resources import UserShoppingLists, UserShoppingList, UserShoppingListItems, UserShoppingListItem
    
    api.add_resource(
        UserShoppingLists,
        BASE_PATH + '/shopping-lists'
    )

    api.add_resource(
        UserShoppingList,
        BASE_PATH + '/shopping-lists/<string:shopping_list_id>'
    )

    # TODO remove if not used
    api.add_resource(
        UserShoppingListItems,
        BASE_PATH + '/shopping-lists/<string:shopping_list_id>/items'
    )

    api.add_resource(
        UserShoppingListItem,
        BASE_PATH + '/shopping-lists/<string:shopping_list_id>/items/<string:shopping_list_item_id>'
    )