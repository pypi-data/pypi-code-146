from unittest.mock import patch

import pytest

from sym.flow.cli.commands.users.list import get_user_data
from sym.flow.cli.helpers.utils import human_friendly, utc_to_local
from sym.flow.cli.tests.factories.users import UserFactory


class TestUsersList:
    @pytest.fixture
    def users(self):
        yield [
            UserFactory.create(identities__0__matcher__email="z@z.com"),
            UserFactory.create(identities__0__matcher__email="b@z.com", is_admin=True),
            UserFactory.create(identities__0__matcher__email="b@b.com"),
        ]

    @pytest.fixture(autouse=True)
    def patchypatch(self, users):
        with patch("sym.flow.cli.helpers.api.SymAPI.get_users", return_value=users):
            yield

    def test_get_user_data(self, users, global_options):
        table_data = get_user_data(global_options.sym_api)

        assert table_data[0] == ["Name", "Email", "Role", "Created At"]
        assert table_data[1] == [
            users[2].sym_name,
            users[2].sym_identifier,
            users[2].role,
            human_friendly(utc_to_local(users[2].created_at)),
        ]
        assert table_data[2] == [
            users[1].sym_name,
            users[1].sym_identifier,
            users[1].role,
            human_friendly(utc_to_local(users[1].created_at)),
        ]
        assert table_data[3] == [
            users[0].sym_name,
            users[0].sym_identifier,
            users[0].role,
            human_friendly(utc_to_local(users[0].created_at)),
        ]
