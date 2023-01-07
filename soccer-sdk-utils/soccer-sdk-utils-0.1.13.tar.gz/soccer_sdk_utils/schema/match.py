from marshmallow import EXCLUDE, Schema, fields, post_load

from soccer_sdk_utils.model.match import Match


class MatchSchema(Schema):
    id = fields.UUID(required=True)
    gender = fields.Str(required=True)
    date = fields.Date(required=True)
    division = fields.Str(required=True)
    team1 = fields.Str(required=True)
    team2 = fields.Str(required=True)
    score1 = fields.Int(required=True)
    score2 = fields.Int(required=True)

    class Meta:
        strict = True
        ordered = True
        model = Match
        unknown = EXCLUDE

    @post_load
    def make_match(self, data, **kwargs):
        return Match(**data)
