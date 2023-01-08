
from uuid import uuid4
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended.config import config
from marshmallow_mongoengine import schema

from . import authenticate, encode_password, get_user_by_email
from .schemas import PostRegisterUserSchema, PostUserTokenSchema, PostResetPasswordSchema
from .. import BASE_PATH
from ... import validate_payload
from ...models import User, ShoppingList, UserPreferences
from ...exceptions import InvalidCredentials, NotFound

auth_blueprint = Blueprint(
    'auth',
    __name__,
    url_prefix = BASE_PATH + '/auth'
)

@auth_blueprint.route('/token', methods=['POST'])
@validate_payload(PostUserTokenSchema(), 'user')
def get_token(user: PostUserTokenSchema):
    user = authenticate(user['email'], user['password'])
    
    if not user:
        raise InvalidCredentials("Provided credentials doesn't match for specific user")

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=user.email)
    return jsonify(user_id=user.id,access_token=access_token, expires_in=config.access_expires.seconds), 200


@auth_blueprint.route('/register', methods=['POST'])
@validate_payload(PostRegisterUserSchema(), 'user_meta')
def register_user(user_meta: PostRegisterUserSchema):
    user = User()
    user.name = user_meta['name']
    user.password = encode_password(user_meta['password'])
    user.email = user_meta['email']
    user.save()

    # Create a new shopping list for the newly created user
    shop_list = ShoppingList()
    shop_list.owner = user.id
    shop_list.name = 'Shopping List' #TODO name of the list may vary based on the location of the user
    shop_list.save()

    # Create a new preferences object for the newly created user
    shop_list = UserPreferences()
    shop_list.owner = user.id
    shop_list.save()
    
    return jsonify(user.to_mongo()), 200

@auth_blueprint.route('/reset_password', methods=['POST'])
@validate_payload(PostResetPasswordSchema(), 'user_meta')
def reset_password(user_meta: PostResetPasswordSchema):
    user = get_user_by_email(user_meta['email'])

    if user is None:
        raise NotFound('User not found')

    # TODO: send mail

    return '', 204

@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    # TODO: token validation and blacklisting
    return '', 204
    
