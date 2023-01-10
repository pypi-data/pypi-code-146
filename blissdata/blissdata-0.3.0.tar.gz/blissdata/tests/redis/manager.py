import pytest
from blissdata.redis.manager import RedisAddress


@pytest.mark.parametrize(
    "address, expected, redis_env",
    [
        (None, "redis://localhost:6379", None),
        (None, "redis://mycomputer:6379", "mycomputer"),
        (None, "redis://mycomputer:2000", "mycomputer:2000"),
        ("foo:2000", "redis://foo:2000", False),
        ("localhost:/foo.sock", "unix:///foo.sock", False),
        ("localhost:2000", "redis://localhost:2000", False),
    ],
)
def test_redis_address(mocker, address, expected, redis_env):
    mock_environ = mocker.patch("os.environ.get", return_value=redis_env)
    redis_address = RedisAddress.factory(address)
    assert redis_address.url == expected
    if redis_env is False:
        mock_environ.assert_not_called()
    else:
        mock_environ.assert_called_with("REDIS_HOST")
