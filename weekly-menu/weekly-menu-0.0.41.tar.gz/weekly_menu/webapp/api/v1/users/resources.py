import pprint

from flask import jsonify
from flask_restful import Resource, abort, request
from flask_jwt_extended import jwt_required
from mongoengine.errors import NotUniqueError
from mongoengine.fields import ObjectIdField, ObjectId
from mongoengine.queryset.visitor import Q

from .schemas import UserSchema
from ...models import User
from ... import validate_payload, paginated, mongo, put_document, patch_document, load_user_info, patch_embedded_document, parse_query_args, search_on_model
from ...exceptions import DuplicateEntry, BadRequest, Conflict, NotFound

class UserProfileInstance(Resource):
    @jwt_required
    @load_user_info
    def get(self, user_info: User):
        return user_info