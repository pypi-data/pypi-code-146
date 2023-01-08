import enum
import unittest
from datetime import date

import pandas as pd
import pandas.testing

from chalk.client import ChalkAPIClientImpl
from chalk.client.client_impl import _OfflineQueryResponse
from chalk.features import features


class Color(enum.Enum):
    blue = "blue"
    black = "black"
    white = "white"


@features
class User:
    id: int
    fav_color: Color
    birthday: date


class TestClientSerialization(unittest.TestCase):
    def test_deserialize_null_int_enum(self):
        client = ChalkAPIClientImpl(
            client_id="dummy",
            client_secret="dummy",
            environment="dummy",
            api_server="dummy",
        )

        fixture_response = _OfflineQueryResponse(
            columns=["user.id", "user.fav_color"],
            output=[
                [1, None],
                ["blue", "black"],
            ],
        )

        # this shouldn't throw
        client._decode_offline_response(offline_query_response=fixture_response)

    def test_deserialize_date(self):
        client = ChalkAPIClientImpl(
            client_id="dummy",
            client_secret="dummy",
            environment="dummy",
            api_server="dummy",
        )

        fixture_response = _OfflineQueryResponse(
            columns=["user.birthday"],
            output=[
                ["2022-09-08"],
            ],
        )

        decoded_frame = client._decode_offline_response(offline_query_response=fixture_response)
        expected_frame = pd.DataFrame(data={"user.birthday": [date.fromisoformat("2022-09-08")]})
        pandas.testing.assert_frame_equal(decoded_frame, expected_frame)
