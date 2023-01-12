import pytest

from aiotaipit import TaipitApi
from aiotaipit.const import (
    SECTION_CONTROLLERS,
    SECTION_METER_TYPES,
    SECTION_REGIONS, SECTION_METER_TYPES_FULL
)

CONF_CONTROLLER_ID = 'controllerId'

CONF_ENERGY_T3_A = 'energy_t3_a'

CONF_ENERGY_T2_A = 'energy_t2_a'

CONF_ENERGY_T1_A = 'energy_t1_a'

CONF_ENERGY_A = 'energy_a'

CONF_LAST_READING = 'lastReading'

CONF_ECOMETER_DATA = 'ecometerdata'

CONF_METER_NAME = 'metername'

CONF_SUCCESS = 'success'

CONF_DATA = 'data'

CONF_USERNAME = 'username'
CONF_ID = 'id'


@pytest.mark.asyncio
class TestTaipitApi:
    @pytest.fixture(scope='class')
    def user(self) -> dict:
        return {}

    @pytest.fixture(scope='class')
    def meter_ids(self) -> list:
        return []

    async def test_all_readings(self, api: TaipitApi, meter_ids: list):
        _all_readings = await api.async_get_all_readings()
        assert _all_readings is not None
        assert isinstance(_all_readings, list)
        assert len(_all_readings) > 0
        for readings in _all_readings:
            assert CONF_ID in readings
            assert CONF_METER_NAME in readings
            assert CONF_ECOMETER_DATA in readings
            assert CONF_LAST_READING in readings[CONF_ECOMETER_DATA]
            assert CONF_ENERGY_A in readings[CONF_ECOMETER_DATA][CONF_LAST_READING]
            assert CONF_ENERGY_T1_A in readings[CONF_ECOMETER_DATA][CONF_LAST_READING]
            assert CONF_ENERGY_T2_A in readings[CONF_ECOMETER_DATA][CONF_LAST_READING]
            assert CONF_ENERGY_T3_A in readings[CONF_ECOMETER_DATA][CONF_LAST_READING]
            meter_ids.append(readings[CONF_ID])

    async def test_get_meter_readings(self, api: TaipitApi, meter_ids: list):
        for meter_id in meter_ids:
            _readings = await api.async_get_meter_readings(meter_id)

    async def test_get_meters(self, api: TaipitApi, meter_ids: list):
        _meters = await api.async_get_meters()
        assert _meters is not None
        assert isinstance(_meters, list)
        for meter in _meters:
            if meter[CONF_ID] not in meter_ids:
                meter_ids.append(meter[CONF_ID])

    async def test_get_meter_info(self, api: TaipitApi, meter_ids: list):
        for meter_id in meter_ids:
            _info = await api.async_get_meter_info(meter_id)
            assert _info
            assert CONF_ID in _info
            assert meter_id == _info[CONF_ID]

    async def test_get_current_user(self, api: TaipitApi, user: dict):
        _current_user = await api.async_get_current_user()
        assert _current_user
        assert CONF_USERNAME in _current_user
        assert CONF_ID in _current_user
        user.update(_current_user)

    async def test_get_user_info(self, api: TaipitApi, user):
        _user_info = await api.async_get_user_info(user[CONF_ID])

    async def test_get_warnings(self, api: TaipitApi):
        _warnings = await api.async_get_warnings()
        assert _warnings is not None
        assert CONF_DATA in _warnings
        assert isinstance(_warnings[CONF_DATA], list)
        assert CONF_SUCCESS in _warnings
        assert CONF_SUCCESS in _warnings
        assert _warnings[CONF_SUCCESS]

    async def test_get_settings(self, api: TaipitApi):
        _settings = await api.async_get_settings()
        assert _settings is not None
        assert SECTION_CONTROLLERS in _settings
        assert isinstance(_settings[SECTION_CONTROLLERS], list)
        assert SECTION_METER_TYPES in _settings
        assert isinstance(_settings[SECTION_METER_TYPES], list)
        assert SECTION_METER_TYPES_FULL in _settings
        assert isinstance(_settings[SECTION_METER_TYPES_FULL], list)
        assert SECTION_REGIONS in _settings
        assert isinstance(_settings[SECTION_REGIONS], list)
