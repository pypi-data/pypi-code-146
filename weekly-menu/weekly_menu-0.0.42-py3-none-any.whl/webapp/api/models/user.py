from .. import mongo

class User(mongo.Document):
    MIN_USERNAME_LENGTH = 4
    MAX_USERNAME_LENGTH = 64
    MIN_PASSWORD_LENGTH = 4
    MAX_PASSWORD_LENGTH = 64
    USER_EMAIL_REGEX = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    
    name = mongo.StringField(min_length=MIN_USERNAME_LENGTH, max_length=MAX_USERNAME_LENGTH)
    password = mongo.BinaryField(required=True)
    email = mongo.StringField(unique=True, regex=USER_EMAIL_REGEX)

    meta = {
        'collection' : 'users',
        'strict': False
    }

    def __repr__(self):
           return "<User '{}'>".format(self.username)