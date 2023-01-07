import logging

from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from soccer_sdk_utils.model.user import User


class UserSchema(Schema):
    id = fields.UUID(required=False)
    first_name = fields.Str(required=False, allow_none=True, load_default=None)
    last_name = fields.Str(required=False, allow_none=True, load_default=None)
    username = fields.Str(required=False, allow_none=True, load_default=None)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    registered_on = fields.DateTime(required=False, allow_none=True, load_default=None)
    phone = fields.Str(required=False, allow_none=True, load_default=None)

    class Meta:
        strict = True
        ordered = True
        model = User
        unknown = EXCLUDE

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

    @staticmethod
    def filter(user_dict: dict | None) -> dict | None:
        if user_dict is None:
            return None

        schema = UserSchema(unknown=EXCLUDE)

        user_instance = schema.load(user_dict)
        user_dict = schema.dump(user_instance)

        return user_dict


if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    dirname = os.path.dirname(__file__)
    basedir = os.path.abspath("../..")
    load_dotenv(os.path.join(basedir, ".env"))

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )
    logger = logging.getLogger(__name__)

    # Creating Schemas from Dictionaries
    # https://marshmallow.readthedocs.io/en/stable/quickstart.html#creating-schemas-from-dictionaries

    # Serializing Objects ("Dumping")
    logger.info("Serializing Objects ('Dumping')")
    user = User(password="something", email="john.doe@python.org")
    schema = UserSchema(unknown=EXCLUDE)
    result = schema.dump(user)
    logger.info(result)

    # Filtering Output
    logger.info("Filtering Output")
    summary_schema = UserSchema(unknown=EXCLUDE, only=("id", "email"))
    result = summary_schema.dump(user)
    logger.info(result)

    # Deserializing Objects ("Loading")
    logger.info("Deserializing Objects ('Loading')")
    # https://marshmallow.readthedocs.io/en/stable/quickstart.html#deserializing-objects-loading
    user_data = {
        "id": "d15dc781-4780-4994-b9ec-5771376c2a2e",
        "email": "janedoe@yahoo.com",
        "password": "something",
    }

    schema = UserSchema(unknown=EXCLUDE)
    result = schema.load(user_data)
    logger.info(result)

    # Handling Collections of Objects
    logger.info("Handling Collections of Objects")
    user1 = User(email="mick@stones.com")
    user2 = User(email="keith@stones.com")
    users = [user1, user2]
    schema = UserSchema(unknown=EXCLUDE, many=True)
    result = schema.dump(users)  # Or UserSchema().dump(users, many=True)
    logger.info(result)

    user_data = [
        {
            "id": "d15dc781-4780-4994-b9ec-5771376c2a2e",
            "email": "janedoe@yahoo.com",
            "password": "something else",
        },
        {
            "id": "d15dc781-4780-4994-b9ec-5771376c2a2f",
            "email": "jonedoe@gmail.com",
            "password": "something",
        },
    ]

    result = UserSchema(unknown=EXCLUDE).load(user_data, many=True)
    logger.info(result)

    from common.dao import UserDAO

    logging.info("Loading data from the database ...")
    user_data = UserDAO().get_all()

    try:
        users = UserSchema(unknown=EXCLUDE).load(user_data, many=True)

        for user in users:
            logger.info(user)
    except ValidationError as err:
        logger.error(err.messages)
        logger.error(err.valid_data)
