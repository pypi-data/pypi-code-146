from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from soccer_sdk_utils.model.club_translation import ClubTranslation


class ClubTranslationSchema(Schema):
    id = fields.Str(required=True)
    src = fields.Str(required=True, data_key="from")
    dst = fields.Str(required=True, data_key="to")

    class Meta:
        strict = True
        ordered = True
        model = ClubTranslation
        unknown = EXCLUDE

    @post_load
    def make_translation(self, data, **kwargs):
        return ClubTranslation(**data)

    @staticmethod
    def filter(translation_dict: dict | None) -> dict | None:
        if translation_dict is None:
            return None

        schema = ClubTranslationSchema(unknown=EXCLUDE)
        instance = schema.load(translation_dict)
        translation_dict = schema.dump(instance)

        return translation_dict


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

    from soccer_sdk_utils.dao.club_translation import ClubTranslationDAO
    from soccer_sdk_utils.model.club_translation import ClubTranslation

    data = ClubTranslationDAO().get_all()

    try:
        results = ClubTranslationSchema(unknown=EXCLUDE).load(data, many=True)

        for result in results:
            logging.info(result)
    except ValidationError as err:
        logging.error(err)
        sys.exit(1)
