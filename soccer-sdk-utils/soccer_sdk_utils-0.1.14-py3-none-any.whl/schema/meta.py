from marshmallow import EXCLUDE, Schema, fields, post_load

from soccer_sdk_utils.model.meta import MetaProperty


class MetaPropertySchema(Schema):
    """MetaProperty schema."""

    class Meta:
        strict = True
        ordered = True
        model = MetaProperty
        unknown = EXCLUDE

    # pylint: disable=invalid-name
    name = fields.Str(required=True)
    value = fields.Str(required=True)

    @post_load
    def make_meta_property(self, data, **kwargs):
        """Make meta property."""
        return MetaProperty(**data)
