from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from soccer_sdk_utils.model.state_province import StateProvince


class StateProvinceSchema(Schema):
    id = fields.UUID()
    name = fields.Str()
    code = fields.Str()
    country = fields.Str()

    class Meta:
        strict = True
        ordered = True
        model = StateProvince
        unknown = EXCLUDE

    @post_load
    def make_state_province(self, data, **kwargs):
        return StateProvince(**data)


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

    from common.dao import StateProvinceDAO

    state_province_data = StateProvinceDAO().get_all()

    try:
        result = StateProvinceSchema(unknown=EXCLUDE).load(
            state_province_data, many=True
        )

        for state_province in result:
            logger.info(state_province)
    except ValidationError as err:
        logger.error(err.messages)
        sys.exit(1)
