from marshmallow import EXCLUDE, Schema, fields, post_load

from soccer_sdk_utils.model.bltoken import BlacklistToken


class BlacklistTokenSchema(Schema):
    id = fields.UUID(required=False)
    token = fields.Str(required=True)
    blacklisted_on = fields.DateTime(required=False, allow_none=True, load_default=None)

    class Meta:
        strict = True
        ordered = True
        model = BlacklistToken
        unknown = EXCLUDE

    @post_load
    def make_blacklist_token(self, data, **kwargs):
        return BlacklistToken(**data)

    @staticmethod
    def filter(blacklist_token_dict: dict | None) -> dict | None:
        if blacklist_token_dict is None:
            return None

        schema = BlacklistTokenSchema(unknown=EXCLUDE)

        blacklist_token_instance = schema.load(blacklist_token_dict)
        blacklist_token_dict = schema.dump(blacklist_token_instance)

        return blacklist_token_dict
