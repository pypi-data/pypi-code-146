import pprint
import re

from datetime import datetime
from flask import jsonify
from flask_restful import Resource, abort, request, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import NotUniqueError
from mongoengine.fields import ObjectIdField, ObjectId
from mongoengine.queryset.visitor import Q

from .schemas import MenuSchema, PatchMenuSchema, PutMenuSchema, MenuRecipeSchema
from ...models import Ingredient, User, menu, ShoppingList, Menu, Recipe
from ... import validate_payload, paginated, mongo, load_user_info, put_document, patch_document, parse_query_args, search_on_model
from ...exceptions import DuplicateEntry, BadRequest

def _dereference_recipes(menu: Menu):
    if menu.recipes != None:
        menu_recipes = [recipe.to_mongo()
                            for recipe in menu.recipes]
        menu = menu.to_mongo()
        for i in range(len(menu_recipes)):
            menu['recipes'][i] = menu_recipes[i]
    return menu

class MenuList(Resource):

    menu_query_reqparse = reqparse.RequestParser()
    menu_query_reqparse.add_argument(
        'day',
        type=str,
        location=['args'],
        help='day must be in the form yyyy-MM-dd',
        trim=True,
        required=False
    )

    @jwt_required
    @parse_query_args
    @paginated
    @load_user_info
    def get(self, query_args, page_args, user_info: User):
        return search_on_model(Menu, Q(owner=str(user_info.id)), query_args, page_args)
    
    @jwt_required
    @validate_payload(MenuSchema(), 'menu')
    @load_user_info
    def post(self, menu: Menu, user_info: User):
        #Associate user id
        menu.owner = user_info.id
        
        try:
            menu.save(force_insert=True)
        except NotUniqueError as nue:
            raise DuplicateEntry(description="duplicate entry found for a menu", details=nue.args or [])
        
        return menu, 201

class MenuInstance(Resource):
    @jwt_required
    @load_user_info
    def get(self, user_info: User, menu_id=''):
        menu = Menu.objects(Q(owner=str(user_info.id)) & Q(_id=menu_id)).get_or_404()

        #return _dereference_recipes(menu)
        return menu
    
    @jwt_required
    @load_user_info
    def delete(self, user_info: User, menu_id=''):
        Menu.objects(Q(owner=str(user_info.id)) & Q(_id=menu_id)).get_or_404().delete()
        return "", 204
    
    @jwt_required
    @validate_payload(PutMenuSchema(), 'new_menu')
    @load_user_info
    def put(self, new_menu: Ingredient, user_info: User, menu_id=''):
        old_menu = Menu.objects(Q(_id=menu_id) & Q(owner=str(user_info.id))).get_or_404()

        result = put_document(Menu, new_menu, old_menu)

        if(result.modified_count != 1):
            raise BadRequest(description='no matching menu with id: {}'.format(menu_id))
        
        old_menu.reload()
        return old_menu, 200
        

    @jwt_required
    @validate_payload(PatchMenuSchema(), 'new_menu')
    @load_user_info
    def patch(self, new_menu: Menu, user_info: User, menu_id=''):
        old_menu = Menu.objects(Q(_id=menu_id) & Q(owner=str(user_info.id))).get_or_404()

        result = patch_document(Menu, new_menu, old_menu)

        if(result.modified_count != 1):
            raise BadRequest(description='no matching menu with id: {}'.format(menu_id))
        
        old_menu.reload()
        return old_menu, 200

def _retrieve_base_menu(menu_id: str, user_id: str) -> Menu:
    return Menu.objects(Q(owner=user_id) & Q(_id=menu_id)).get_or_404()


class MenuRecipesList(Resource):
    @jwt_required
    @load_user_info
    def get(self, user_info: User, menu_id=''):
        menu = _retrieve_base_menu(menu_id, str(user_info.id))
        return [menu_menu.to_mongo() for menu_menu in menu.recipes] if menu.recipes != None else []

    @jwt_required
    @validate_payload(MenuRecipeSchema(), 'menu_recipe')
    @load_user_info
    def post(self, menu_id, menu_recipe, user_info: User):
        menu = _retrieve_base_menu(menu_id, str(user_info.id))
        recipe = Recipe.objects(Q(owner=str(user_info.id)) & Q(_id=menu_recipe['recipe_id'])).get_or_404()
        
        if menu.recipes:
            menu.recipes.append(recipe.id)
        else:
            menu.recipes = [recipe.id]
        
        menu.save()
        return menu.recipes, 200


class MenuRecipesInstance(Resource):
    @jwt_required
    @load_user_info
    def delete(self, user_info: User, menu_id='', ingredient_id=''):
        menu = _retrieve_base_menu(menu_id, str(user_info.id))
        
        if menu.recipes != None and len(menu.recipes) == 1:
            raise BadRequest('no recipes to delete for this menu')

        ingredient_id = ObjectId(ingredient_id)

        menu.recipes = [menu_menu for menu_menu in menu.recipes if menu_menu.ingredient.id != ingredient_id]

        menu.save()

        return "", 204
