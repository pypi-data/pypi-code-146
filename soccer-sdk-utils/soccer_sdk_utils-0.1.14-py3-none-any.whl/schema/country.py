from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from soccer_sdk_utils.model.country import Country


class CountrySchema(Schema):
    id = fields.UUID(required=True)
    name = fields.Str(required=True)
    code = fields.Str(required=True)

    class Meta:
        strict = True
        ordered = True
        model = Country
        unknown = EXCLUDE

    @post_load
    def make_country(self, data, **kwargs):
        return Country(**data)

    @staticmethod
    def filter(country_dict: dict | None) -> dict | None:
        if country_dict is None:
            return None

        schema = CountrySchema(unknown=EXCLUDE)

        country_instance = schema.load(country_dict)
        country_dict = schema.dump(country_instance)

        return country_dict


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

    from soccer_sdk_utils.dao import CountryDAO

    country_data = CountryDAO().get_all()

    try:
        result = CountrySchema(unknown=EXCLUDE).load(country_data, many=True)

        for country in result:
            logger.info(country)
    except ValidationError as err:
        logger.error(err.messages)
        sys.exit(1)
