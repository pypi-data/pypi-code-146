from .. import API_PREFIX

API_VERSION = 'v1'
BASE_PATH = API_PREFIX + '/' + API_VERSION


def create_module(app, api):
    from .auth import create_module as create_auth_module
    from .scrapers import create_module as create_scrapers_module
    from .ingredients import create_module as create_ingredients_module
    from .menu import create_module as create_menu_module
    from .recipes import create_module as create_recipes_module
    from .users import create_module as create_users_module
    from .shopping_list import create_module as create_shopping_list_module
    from .config import create_module as create_config_module

    create_auth_module(app)

    create_scrapers_module(app)

    create_ingredients_module(app, api)
    create_menu_module(app, api)
    create_recipes_module(app, api)
    create_users_module(app, api)
    create_shopping_list_module(app, api)
    create_config_module(app, api)
