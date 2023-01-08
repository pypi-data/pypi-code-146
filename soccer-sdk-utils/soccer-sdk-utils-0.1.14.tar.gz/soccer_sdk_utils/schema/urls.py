from marshmallow import EXCLUDE, Schema, fields, post_load

from soccer_sdk_utils.model.values import Values


class UrlsSchema(Schema):
    sw = fields.URL(allow_none=True, load_default=None)
    tds = fields.URL(allow_none=True, load_default=None)

    class Meta:
        strict = True
        ordered = True
        model = Values
        unknown = EXCLUDE

    @post_load
    def make_urls(self, data, **kwargs):
        return Values(**data)
