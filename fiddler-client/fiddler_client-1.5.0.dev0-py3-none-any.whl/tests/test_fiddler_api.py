import pytest

from fiddler import FiddlerApi
from pytest_mock import MockFixture
from fiddler.v2.schema.server_info import Version


def test_client_v1_creation_fail():
    with pytest.raises(ValueError) as e:
        client_v1 = FiddlerApi('', '', '')


def test_client_v2_creation_fail():
    with pytest.raises(ValueError) as e:
        client_v2 = FiddlerApi('', '', '', version=2)


def test_get_server_info_without_server_version(mocker: MockFixture):
    mocker.patch('fiddler.connection.Connection.check_connection', return_value='OK')

    supported_features = {
        'features': {
            'enable_schema_creation': True,
            'authorization': True,
            'fairness': False,
            'dev_cluster': False,
        },
        'supported_client_version': '22.10.0',
        'enable_fiddler_v2': False,
    }
    mock_get_supported_features = mocker.patch('fiddler.FiddlerApi._get_supported_features')
    mock_get_supported_features.return_value = supported_features
    client = FiddlerApi('https://test.fiddler.ai', 'test', 'foo-token', version=1)

    assert client.v2.server_info.server_version is None
    assert client.v2.server_info.features == supported_features["features"]

    client = FiddlerApi('https://test.fiddler.ai', 'test', 'foo-token', version=2)

    assert client.v2.server_info.server_version is None
    assert client.v2.server_info.features == supported_features['features']


def test_get_server_info_with_server_version(mocker: MockFixture):
    mocker.patch('fiddler.connection.Connection.check_connection', return_value='OK')

    supported_features = {
        'features': {
            'enable_schema_creation': True,
            'authorization': True,
            'fairness': False,
            'dev_cluster': False,
        },
        'supported_client_version': '22.10.0',
        'enable_fiddler_v2': False,
        'server_version': "22.10.0"
    }
    mock_get_supported_features = mocker.patch('fiddler.FiddlerApi._get_supported_features')
    mock_get_supported_features.return_value = supported_features
    client = FiddlerApi('https://test.fiddler.ai', 'test', 'foo-token', version=1)

    assert client.v2.server_info.server_version == Version.parse(supported_features['server_version'])
    assert client.v2.server_info.features == supported_features["features"]

    client = FiddlerApi('https://test.fiddler.ai', 'test', 'foo-token', version=2)

    assert client.v2.server_info.server_version == Version.parse(supported_features['server_version'])
    assert client.v2.server_info.features == supported_features['features']
