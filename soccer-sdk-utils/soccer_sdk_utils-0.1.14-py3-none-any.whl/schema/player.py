from marshmallow import EXCLUDE, Schema, fields, post_load, validate

from soccer_sdk_utils.model.player import Player
from soccer_sdk_utils.schema.meta import MetaPropertySchema


class PlayerSchema(Schema):
    id = fields.UUID(required=True, allow_none=True)
    gender = fields.Str(required=True, validate=validate.OneOf(["Male", "Female"]))
    first_name = fields.Str(required=True, allow_none=True)
    last_name = fields.Str(required=True, allow_none=True)
    club = fields.Str(required=True, allow_none=True)
    state = fields.Str(required=True, allow_none=True)
    position = fields.Str(required=True, allow_none=True)

    meta = fields.List(fields.Nested(MetaPropertySchema))

    class Meta:
        strict = True
        ordered = True
        model = Player
        unknown = EXCLUDE

    @post_load
    def make_player(self, data, **kwargs):
        return Player(**data)


if __name__ == "__main__":
    import logging
    import os
    from pprint import pprint

    from dotenv import load_dotenv

    dirname = os.path.dirname(__file__)
    basedir = os.path.abspath("../..")
    load_dotenv(os.path.join(basedir, ".env"))

    from common.dao.player import PlayerDAO

    player_dao = PlayerDAO()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )

    player = Player()

    player.first_name = "Fred"
    player.gender = "Male"
    player.last_name = "Flintstone"
    player.position = "Forward"
    player.city = "Bedrock"
    player.state = "NA"
    player.country = "Narnia"
    player.league = "ECNL"
    player.team = "U19 Bedrock FC"

    player.add_property("grad_year", "2023")

    player_data = PlayerSchema().dump(player)

    pprint(player_data)

    # first_name = "Alena"
    # last_name = "Watts"
    # player_data = player_dao.get_by_fname_lname(first_name, last_name)

    # if player_data is None:
    #     logging.error(f"Player '{first_name} {last_name}' not found!")
    #     sys.exit(1)
    #
    # try:
    #     result = PlayerSchema(unknown=EXCLUDE).load(player_data)
    #     logging.info(result)
    # except ValidationError as err:
    #     logging.error(err)

    # player_data = PlayerDAO().search("Female", "2024", "GA")
    #
    # if player_data is None:
    #     logging.error(f"Failed to search for players!")
    #     sys.exit(2)
    #
    # try:
    #     result = PlayerSchema(unknown=EXCLUDE).load(player_data, many=True)
    #
    #     for player in result:
    #         logging.info(player)
    # except ValidationError as err:
    #     logger.error(err)
    #     sys.exit(3)
