import pprint

from flask import jsonify
from flask_restful import Resource, abort, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import NotUniqueError
from mongoengine.fields import ObjectIdField
from mongoengine.queryset.visitor import Q

from .schemas import IngredientSchema, PatchIngredientSchema, PutIngredientSchema
from ...models import Ingredient, User, Recipe, ShoppingList
from ... import validate_payload, get_payload, paginated, parse_query_args, mongo, load_user_info, put_document, patch_document, search_on_model
from ...exceptions import DuplicateEntry, BadRequest, Forbidden


class IngredientsList(Resource):
    @jwt_required
    @parse_query_args
    @paginated
    @load_user_info
    def get(self, query_args, page_args, user_info: User):
        return search_on_model(Ingredient, Q(owner=str(user_info.id)), query_args, page_args)

    @jwt_required
    @validate_payload(IngredientSchema(), 'ingredient')
    @load_user_info
    def post(self, ingredient: Ingredient, user_info: User):
        # Associate user id
        ingredient.owner = user_info.id

        try:
            ingredient.save(force_insert=True)
        except NotUniqueError as nue:
            raise DuplicateEntry(
                description="duplicate entry found for an ingredient", details=nue.args or [])

        return ingredient, 201


class IngredientInstance(Resource):
    @jwt_required
    @load_user_info
    def get(self, user_info: User, ingredient_id=''):
        if ingredient_id != None:
            return Ingredient.objects(Q(_id=ingredient_id) & Q(owner=str(user_info.id))).get_or_404()

    @jwt_required
    @load_user_info
    def delete(self, user_info: User, ingredient_id=''):
        if ingredient_id != None:
            ingredient = Ingredient.objects(
                Q(_id=ingredient_id) & Q(owner=str(user_info.id))).get_or_404()

            # Removing references in embedded documents is not automatic (see: https://github.com/MongoEngine/mongoengine/issues/1592)
            Recipe.objects(owner=user_info.id).update(
                pull__ingredients__ingredient=ingredient.id)
            ShoppingList.objects(owner=user_info.id).update(
                pull__items__item=ingredient.id)

            ingredient.delete()

            return "", 204

    @jwt_required
    @validate_payload(PutIngredientSchema(), 'new_ingredient')
    @load_user_info
    def put(self, new_ingredient: Ingredient, user_info: User, ingredient_id=''):
        old_ingredient = Ingredient.objects(
            Q(_id=ingredient_id) & Q(owner=str(user_info.id))).get_or_404()

        result = put_document(Ingredient, new_ingredient, old_ingredient)

        if(result.modified_count != 1):
            raise BadRequest(
                description='no matching ingredient with id: {}'.format(ingredient_id))

        old_ingredient.reload()
        return old_ingredient, 200

    @jwt_required
    @validate_payload(PatchIngredientSchema(), 'new_ingredient')
    @load_user_info
    def patch(self, new_ingredient, user_info: User, ingredient_id=''):
        old_ingredient = Ingredient.objects(
            Q(_id=ingredient_id) & Q(owner=str(user_info.id))).get_or_404()

        result = patch_document(Ingredient, new_ingredient, old_ingredient)

        if(result.modified_count != 1):
            raise BadRequest(
                description='no matching ingredient with id: {}'.format(ingredient_id))

        old_ingredient.reload()
        return old_ingredient, 200
