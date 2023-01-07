from marshmallow import EXCLUDE, Schema, fields, post_load

from soccer_sdk_utils.model.suggestion import Suggestion


class SuggestionSchema(Schema):
    id = fields.Str()
    description = fields.Str()
    author = fields.Str()
    state = fields.Str()
    opened_on = fields.DateTime()
    closed_on = fields.DateTime()

    class Meta:
        strict = True
        ordered = True
        model = Suggestion
        unknown = EXCLUDE

    @post_load
    def make_suggestion(self, data, **kwargs):
        return Suggestion(**data)


if __name__ == "__main__":
    pass
