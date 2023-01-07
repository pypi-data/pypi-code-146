from marshmallow import EXCLUDE, Schema, fields, post_load

from soccer_sdk_utils.model.images import Images


class ImagesSchema(Schema):
    logo = fields.Str(allow_none=True, load_default=None)

    class Meta:
        strict = True
        ordered = True
        model = Images
        unknown = EXCLUDE

    @post_load
    def make_images(self, data, **kwargs):
        return Images(**data)
