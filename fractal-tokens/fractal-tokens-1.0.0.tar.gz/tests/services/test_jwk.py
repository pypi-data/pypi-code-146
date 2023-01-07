def test_local(local_jwk_service):
    assert len(local_jwk_service.get_jwks()) == 1


def test_empty_local(empty_local_jwk_service):
    assert len(empty_local_jwk_service.get_jwks()) == 0


def test_remote(mocker, mocked_urlopen, remote_jwk_service):
    mocker.patch("urllib.request.urlopen", return_value=mocked_urlopen)
    assert len(remote_jwk_service.get_jwks("http://localhost")) == 0


def test_automatic_local(automatic_jwk_service):
    assert len(automatic_jwk_service.get_jwks()) == 1


def test_automatic_remote(mocker, mocked_urlopen, automatic_jwk_service):
    mocker.patch("urllib.request.urlopen", return_value=mocked_urlopen)
    assert len(automatic_jwk_service.get_jwks("http://localhost")) == 0
