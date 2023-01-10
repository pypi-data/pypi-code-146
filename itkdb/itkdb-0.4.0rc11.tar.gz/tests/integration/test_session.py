from __future__ import annotations

import betamax
import pytest

import itkdb


@pytest.mark.xfail
def test_fake_route(auth_session):
    with betamax.Betamax(auth_session).use_cassette("test_session.test_fake_route"):
        with pytest.raises(itkdb.exceptions.NotFound):
            auth_session.get("aFakeRoute")


def test_invalid_project(auth_session):
    with betamax.Betamax(auth_session).use_cassette(
        "test_session.test_invalid_project"
    ):
        with pytest.raises(itkdb.exceptions.BadRequest):
            auth_session.get(
                "listComponents", json={"project": "Fake", "pageInfo": {"pageSize": 1}}
            )


def test_missing_required(auth_session):
    with betamax.Betamax(auth_session).use_cassette(
        "test_session.test_missing_required"
    ):
        with pytest.raises(itkdb.exceptions.BadRequest):
            auth_session.get("getComponent", json={"pageInfo": {"pageSize": 1}})


@pytest.mark.xfail
def test_unauthorized():
    session = itkdb.core.Session(user=itkdb.core.User(accessCode1="", accessCode2=""))
    with betamax.Betamax(session).use_cassette("test_session.test_unauthorized"):
        with pytest.raises(itkdb.exceptions.Forbidden):
            session.get(
                "listComponents", json={"project": "S", "pageInfo": {"pageSize": 1}}
            )
