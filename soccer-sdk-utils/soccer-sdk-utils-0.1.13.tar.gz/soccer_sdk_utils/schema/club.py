from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from soccer_sdk_utils.model.club import Club, ClubCommitmentStats
from soccer_sdk_utils.schema.meta import MetaPropertySchema


class ClubSchema(Schema):
    id = fields.UUID(required=True)
    name = fields.Str(required=True)
    city = fields.Str(allow_none=True, load_default=None)
    state = fields.Str(required=True)
    meta = fields.List(fields.Nested(MetaPropertySchema))

    class Meta:
        strict = True
        ordered = True
        model = Club
        unknown = EXCLUDE

    @post_load
    def make_club(self, data, **kwargs):
        return Club(**data)

    @staticmethod
    def filter(club_dict: dict | None) -> dict | None:
        if club_dict is None:
            return None

        schema = ClubSchema(unknown=EXCLUDE)

        club_instance = schema.load(club_dict)
        club_dict = schema.dump(club_instance)

        return club_dict


class ClubCommitmentStatsSchema(Schema):
    club = fields.Str(required=True)
    di = fields.Int(required=True)
    dii = fields.Int(required=True)
    diii = fields.Int(required=True)
    naia = fields.Int(required=True)
    total = fields.Int(required=True)

    class Meta:
        strict = True
        ordered = True
        model = ClubCommitmentStats
        unknown = EXCLUDE

    @post_load
    def make_club_commitment_stats(self, data, **kwargs):
        return ClubCommitmentStats(**data)


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

    from soccer_sdk_utils.dao.club import ClubDAO

    club_data = ClubDAO().get_all()

    try:
        result = ClubSchema(unknown=EXCLUDE).load(club_data, many=True)

        for club in result:
            logger.info(club)
    except ValidationError as err:
        logger.error(err.messages)
        sys.exit(1)
