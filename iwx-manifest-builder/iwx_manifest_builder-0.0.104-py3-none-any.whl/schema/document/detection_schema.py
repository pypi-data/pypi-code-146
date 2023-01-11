from marshmallow import Schema, fields
from ..bbox_coord_schema import BboxCoordAttrsSchema
from ..bbox_pixels_coord_schema import BboxPixelsCoordAttrsSchema
from ..category_schema import CategoryAttrsSchema
from ..image_schema import ImageAttrsSchema
from ..inferred_schema import InferredAttrsSchema


class DetectionSchema(Schema):
    id = fields.String()
    bbox_coord = fields.Nested(BboxCoordAttrsSchema())
    bbox_pixels_coord = fields.Nested(BboxPixelsCoordAttrsSchema())
    bbox_pixels_coord_area = fields.Int()
    category = fields.Nested(CategoryAttrsSchema())
    image = fields.Nested(ImageAttrsSchema())
    inferred = fields.Nested(InferredAttrsSchema())
    score = fields.Float()
