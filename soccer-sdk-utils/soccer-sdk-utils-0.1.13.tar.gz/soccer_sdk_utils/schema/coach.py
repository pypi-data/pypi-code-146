from marshmallow import EXCLUDE, Schema, fields, post_load

from soccer_sdk_utils.model.coach import CoachingChange


class CoachingChangeSchema(Schema):
    program = fields.Str(required=True)
    program_url = fields.Str(required=True)
    old_coach = fields.Str(required=False)
    old_coach_url = fields.Str(required=False)
    new_coach = fields.Str(required=False)
    new_coach_url = fields.Str(required=False)
    clgid = fields.Str(required=True)

    class Meta:
        strict = True
        ordered = True
        model = CoachingChange
        unknown = EXCLUDE

    @post_load
    def make_coaching_change(self, data, **kwargs):
        return CoachingChange(**data)
