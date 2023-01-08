import marshmallow_mongoengine as me

from marshmallow import Schema, fields
from marshmallow.validate import Length, Regexp, Range

from ... import mongo
from ...models import User

_email_field = fields.Str(required=True, validate=Regexp(User.USER_EMAIL_REGEX))
_password_field = fields.Str(required=True, validate=Length(User.MIN_PASSWORD_LENGTH,User.MAX_PASSWORD_LENGTH))

class PostUserTokenSchema(Schema):
    email = _email_field
    password = _password_field

class PostRegisterUserSchema(Schema):
    name = fields.Str(required=True, validate=Length(User.MIN_USERNAME_LENGTH,User.MAX_USERNAME_LENGTH))
    password = _password_field
    email = _email_field

class PostResetPasswordSchema(Schema):
    email = _email_field