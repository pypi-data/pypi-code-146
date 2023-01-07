from marshmallow import EXCLUDE, Schema, fields, post_load

from soccer_sdk_utils.model.team import Team


class TeamSchema(Schema):
    id = fields.Str(allow_none=True, load_default=None)
    title = fields.Str(allow_none=True, load_default=None)
    abbreviation = fields.Str(allow_none=True, load_default=None)

    class Meta:
        strict = True
        ordered = True
        model = Team
        unknown = EXCLUDE

    @post_load
    def make_team(self, data, **kwargs):
        return Team(**data)
