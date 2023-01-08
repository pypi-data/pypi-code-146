import pprint

from flask import jsonify
from flask_restful import Resource, abort, request
from flask_jwt_extended import jwt_required
from mongoengine.errors import NotUniqueError
from mongoengine.fields import ObjectIdField, ObjectId
from mongoengine.queryset.visitor import Q

from weekly_menu.webapp.api.models import user

from .schemas import UserPreferencesSchema, PatchUserPreferencesSchema, PutUserPreferencesSchema
from ....models import UserPreferences, User
from .... import load_user_info, validate_payload, put_document, patch_document, search_on_model, paginated, parse_query_args
from ....exceptions import DuplicateEntry, BadRequest, Conflict, NotFound

class UserPreferenceList(Resource):
    @jwt_required
    @parse_query_args
    @paginated
    @load_user_info
    def get(self, query_args, page_args, user_info: User): 
        return search_on_model(UserPreferences, Q(owner=str(user_info.id)), query_args, page_args)

    @jwt_required
    @validate_payload(UserPreferencesSchema(), 'preferences')
    @load_user_info
    def post(self, preferences: UserPreferences, user_info: User):
        #Associate user id
        preferences.owner = user_info.id
        
        try:
            preferences.save(force_insert=True)
        except NotUniqueError as nue:
            raise DuplicateEntry(description="duplicate entry found for a menu", details=nue.args or [])
        
        return preferences, 201

class UserPreferencesInstance(Resource):

    @jwt_required
    @load_user_info
    def get(self, user_info: User, user_prefs_id: str): 
        prefs = UserPreferences.objects(Q(_id=user_prefs_id) & Q(owner=str(user_info.id))).get_or_404()

        #return _dereference_item(shopping_list)
        return prefs

    @jwt_required
    @load_user_info
    def delete(self, user_info: User, user_prefs_id=''):
        UserPreferences.objects(Q(_id=user_prefs_id) & Q(owner=str(user_info.id))).get_or_404().delete()
        return "", 204
    
    @jwt_required
    @validate_payload(PutUserPreferencesSchema(), 'new_preferences')
    @load_user_info
    def put(self, new_preferences: UserPreferences, user_info: User, user_prefs_id=''):
        old_preferences = UserPreferences.objects(Q(_id=user_prefs_id) & Q(owner=str(user_info.id))).get_or_404()

        result = put_document(UserPreferences, new_preferences, old_preferences)

        if(result.modified_count != 1):
            raise BadRequest(description='no matching preferences with id: {}'.format(user_prefs_id))
        
        old_preferences.reload()
        return old_preferences, 200
        

    @jwt_required
    @validate_payload(PatchUserPreferencesSchema(), 'new_preferences')
    @load_user_info
    def patch(self, new_preferences: UserPreferences, user_info: User, user_prefs_id=''):
        old_preferences = UserPreferences.objects(Q(_id=user_prefs_id) & Q(owner=str(user_info.id))).get_or_404()

        result = patch_document(UserPreferences, new_preferences, old_preferences)

        if(result.modified_count != 1):
            raise BadRequest(description='no matching preferences with id: {}'.format(user_prefs_id))
        
        old_preferences.reload()
        return old_preferences, 200

