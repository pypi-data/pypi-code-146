from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from soccer_sdk_utils.model.conference import Conference
from soccer_sdk_utils.schema.values import ValuesSchema


class ConferenceSchema(Schema):
    id = fields.UUID()
    name = fields.Str(allow_none=True, load_default=None)
    gender = fields.Str(allow_none=True, load_default=None)
    division = fields.Str(allow_none=True, load_default=None)
    ids = fields.Nested(ValuesSchema)
    urls = fields.Nested(ValuesSchema)

    class Meta:
        strict = True
        ordered = True
        model = Conference
        unknown = EXCLUDE

    @post_load
    def make_conference(self, data, **kwargs):
        return Conference(**data)


if __name__ == "__main__":
    import logging
    import os
    import sys

    from dotenv import load_dotenv

    dirname = os.path.dirname(__file__)
    basedir = os.path.abspath("../..")
    load_dotenv(os.path.join(basedir, ".env"))

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )
    logger = logging.getLogger(__name__)

    from soccer_sdk_utils.dao import ConferenceDAO

    conference_data = ConferenceDAO().get_all()

    try:
        result = ConferenceSchema(unknown=EXCLUDE).load(conference_data, many=True)

        for conference in result:
            logger.info(conference)
    except ValidationError as err:
        logger.error(err.messages)
        sys.exit(1)
