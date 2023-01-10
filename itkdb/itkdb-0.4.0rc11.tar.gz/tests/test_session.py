from __future__ import annotations

import betamax

import itkdb


def test_urljoin(auth_session):
    assert (
        auth_session._normalize_url("/resource/")
        == "https://itkpd-test.unicorncollege.cz/resource/"
    )
    assert (
        auth_session._normalize_url("resource/")
        == "https://itkpd-test.unicorncollege.cz/resource/"
    )
    assert (
        auth_session._normalize_url("/resource")
        == "https://itkpd-test.unicorncollege.cz/resource"
    )
    assert (
        auth_session._normalize_url("resource")
        == "https://itkpd-test.unicorncollege.cz/resource"
    )
    assert (
        auth_session._normalize_url("https://itkpd-test.unicorncollege.cz/resource")
        == "https://itkpd-test.unicorncollege.cz/resource"
    )
    assert (
        auth_session._normalize_url("https://google.com/resource")
        == "https://google.com/resource"
    )


def test_expires_after(auth_user):
    assert itkdb.core.Session(expires_after=dict(days=1))


def test_no_bearer(auth_session, mocker):
    spy = mocker.spy(auth_session.user, "authenticate")
    with betamax.Betamax(auth_session).use_cassette("test_session.test_no_bearer"):
        response = auth_session.get("https://google.com/")

    assert spy.call_count == 0
    assert "Authorization" not in response.request.headers
