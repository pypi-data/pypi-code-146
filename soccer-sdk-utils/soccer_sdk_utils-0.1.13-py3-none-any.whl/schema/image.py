from marshmallow import EXCLUDE, Schema, fields, post_load

from soccer_sdk_utils.model.image import Image


class ImageSchema(Schema):
    id = fields.Str(required=True, allow_none=True, load_default=None)
    filename = fields.Str(required=True, allow_none=True, load_default=None)
    path = fields.Str(required=True, allow_none=True, load_default=None)
    title = fields.Str(required=True, allow_none=True, load_default=None)
    alt_text = fields.Str(required=True, allow_none=True, load_default=None)
    url = fields.Str(required=True, allow_none=True, load_default=None)

    class Meta:
        strict = True
        ordered = True
        model = Image
        unknown = EXCLUDE

    @post_load
    def make_image(self, data, **kwargs):
        return Image(**data)
