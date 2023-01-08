from marshmallow import EXCLUDE, Schema, fields, post_load

from soccer_sdk_utils.model.league import League


class LeagueSchema(Schema):
    name = fields.Str(allow_none=True, load_default=None)
    conference = fields.Str(allow_none=True, load_default=None)

    class Meta:
        strict = True
        ordered = True
        model = League
        unknown = EXCLUDE

    @post_load
    def make_league(self, data, **kwargs):
        return League(**data)
