import pprint

from flask import jsonify
from flask_restful import Resource, abort, request
from flask_jwt_extended import jwt_required
from mongoengine.errors import NotUniqueError
from mongoengine.fields import ObjectIdField, ObjectId
from mongoengine.queryset.visitor import Q

from .schemas import RecipeSchema, PatchRecipeSchema, PutRecipeSchema, RecipeIngredientSchema, RecipeIngredientWithoutRequiredIngredientSchema
from ...models import Recipe, User, RecipeIngredient
from ... import validate_payload, paginated, mongo, put_document, patch_document, load_user_info, patch_embedded_document, parse_query_args, search_on_model
from ...exceptions import DuplicateEntry, BadRequest, Conflict, NotFound


def _dereference_ingredients(recipe: Recipe):
    if recipe.ingredients != None:
        recipe_ingredients = [ing.ingredient.to_mongo()
                            for ing in recipe.ingredients]
        recipe = recipe.to_mongo()
        for i in range(len(recipe_ingredients)):
            recipe['ingredients'][i]['ingredient'] = recipe_ingredients[i]
    return recipe


class RecipeList(Resource):
    @jwt_required
    @parse_query_args
    @paginated
    @load_user_info
    def get(self, query_args, page_args, user_info: User):
        return search_on_model(Recipe, Q(owner=str(user_info.id)), query_args, page_args)

    @jwt_required
    @validate_payload(RecipeSchema(), 'recipe')
    @load_user_info
    def post(self, recipe: Recipe, user_info: User):
        # Associate user id
        recipe.owner = user_info.id

        try:
            recipe.save(force_insert=True)
        except NotUniqueError as nue:
            raise DuplicateEntry(
                description="duplicate entry found for a recipe", details=nue.args or [])

        return recipe, 201


class RecipeInstance(Resource):
    @jwt_required
    @load_user_info
    def get(self, user_info: User, recipe_id=''):
        recipe = Recipe.objects(Q(_id=recipe_id) & Q(
            owner=str(user_info.id))).get_or_404()

        #return _dereference_ingredients(recipe)
        return recipe

    @jwt_required
    @load_user_info
    def delete(self, user_info: User, recipe_id=''):
        Recipe.objects(Q(_id=recipe_id) & Q(
            owner=str(user_info.id))).get_or_404().delete()
        return "", 204

    @jwt_required
    @validate_payload(PutRecipeSchema(), 'new_recipe')
    @load_user_info
    def put(self, new_recipe: Recipe, user_info: User, recipe_id=''):
        old_recipe = Recipe.objects(Q(_id=recipe_id) & Q(owner=str(user_info.id))).get_or_404()

        result = put_document(Recipe, new_recipe, old_recipe)

        if(result.modified_count != 1):
            raise BadRequest(description='no matching recipe with id: {}'.format(recipe_id))
        
        old_recipe.reload()
        return old_recipe, 200

    @jwt_required
    @validate_payload(PatchRecipeSchema(), 'new_recipe')
    @load_user_info
    def patch(self, new_recipe: Recipe, user_info: User, recipe_id=''):
        old_recipe = Recipe.objects(Q(_id=recipe_id) & Q(owner=str(user_info.id))).get_or_404()

        result = patch_document(Recipe, new_recipe, old_recipe)

        if(result.modified_count != 1):
            raise BadRequest(description='no matching recipe with id: {}'.format(recipe_id))
        
        old_recipe.reload()
        return old_recipe, 200

def _retrieve_base_recipe(recipe_id: str, user_id: str) -> Recipe:
    return Recipe.objects(Q(owner=user_id) & Q(_id=recipe_id)).get_or_404()


class RecipeIngredientsList(Resource):
    @jwt_required
    @load_user_info
    def get(self, user_info: User, recipe_id=''):
        recipe = _retrieve_base_recipe(recipe_id, str(user_info.id))
        return [recipe_ingredient.to_mongo() for recipe_ingredient in recipe.ingredients] if recipe.ingredients != None else []

    @jwt_required
    @validate_payload(RecipeIngredientSchema(), 'recipe_ingredient')
    @load_user_info
    def post(self, recipe_id, recipe_ingredient: RecipeIngredient, user_info: User):
        recipe = _retrieve_base_recipe(recipe_id, str(user_info.id))

        # Check if an ingredient is already present in a recipe
        current_ingredients_in_recipe = [str(ing.ingredient.id) for ing in recipe.ingredients]
        if str(recipe_ingredient.ingredient.id) in current_ingredients_in_recipe:
            raise Conflict('ingredient already present inside shopping list')

        recipe.ingredients.append(recipe_ingredient)
        recipe.save()
        return recipe_ingredient, 201


class RecipeIngredientInstance(Resource):

    @jwt_required
    @load_user_info
    def get(self, user_info: User, recipe_id: str, ingredient_id: str):

        recipe = Recipe.objects(Q(_id=recipe_id) & Q(owner=str(user_info.id)) & Q(ingredients__ingredient=ingredient_id)).get_or_404()

        for ing_doc in recipe.ingredients:
            if str(ing_doc.ingredient.id) == ingredient_id:
                return ing_doc, 200


        raise NotFound(description='can\'t find ingredient with id {} in recipe {}'.format(ingredient_id, recipe_id))

    @jwt_required
    @load_user_info
    def delete(self, user_info: User, recipe_id='', ingredient_id=''):
        recipe = _retrieve_base_recipe(recipe_id, str(user_info.id))
        
        if recipe.ingredients != None and len(recipe.ingredients) == 1:
            raise BadRequest('no ingredients to delete for this recipe')

        ingredient_id = ObjectId(ingredient_id)

        recipe.ingredients = [recipe_ingredient for recipe_ingredient in recipe.ingredients if recipe_ingredient.ingredient.id != ingredient_id]

        recipe.save()

        return "", 204

    @jwt_required
    @load_user_info
    @validate_payload(RecipeIngredientWithoutRequiredIngredientSchema(), 'recipe_ingredient')
    def patch(self, user_info: User, recipe_id: str, ingredient_id: str, recipe_ingredient: RecipeIngredient):
        recipe = _retrieve_base_recipe(recipe_id, str(user_info.id))
        
        for ing_doc in recipe.ingredients:
            if str(ing_doc.ingredient.id) == ingredient_id:
                recipe_ingredient = ing_doc = patch_embedded_document(recipe_ingredient, ing_doc)
                break

        recipe.save()

        return recipe_ingredient, 200

    @jwt_required
    @load_user_info
    @validate_payload(RecipeIngredientSchema(), 'recipe_ingredient')
    def put(self, user_info: User, recipe_id: str, ingredient_id: str, recipe_ingredient: RecipeIngredient):

        # NOTE An item could be changed
        #if shopping_list_item.item != None and shopping_list_item_id != str(shopping_list_item.item.id):
        #    raise Conflict("can't update item {} with different item {}".format(str(shopping_list_item.item.id), shopping_list_item_id))

        Recipe.objects(Q(_id=recipe_id) & Q(owner=str(user_info.id)) & Q(ingredients__ingredient=ingredient_id)).update(set__ingredients__S=recipe_ingredient)

        return recipe_ingredient, 200