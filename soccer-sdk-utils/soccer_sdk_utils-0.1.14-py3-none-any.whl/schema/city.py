from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from soccer_sdk_utils.model.city import City


class CitySchema(Schema):
    id = fields.UUID(required=True)
    name = fields.Str(required=True)
    spid = fields.Str(required=True)

    class Meta:
        strict = True
        ordered = True
        model = City
        unknown = EXCLUDE

    @post_load
    def make_city(self, data, **kwargs):
        return City(**data)


if __name__ == "__main__":
    import logging
    import os
    import sys

    from dotenv import load_dotenv

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )

    dirname = os.path.dirname(__file__)
    basedir = os.path.abspath("../..")
    load_dotenv(os.path.join(basedir, ".env"))

    from common.dao import CityDAO

    city_data = CityDAO().get_all()

    try:
        result = CitySchema(unknown=EXCLUDE).load(city_data, many=True)

        for city in result:
            logging.info(city)
    except ValidationError as err:
        logging.error(err.messages)
        sys.exit(1)
