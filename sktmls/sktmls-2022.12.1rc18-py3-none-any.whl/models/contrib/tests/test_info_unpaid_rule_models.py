import pytest

from sktmls.models.contrib import InfoUnpaidRuleModel


class TestInfoUnpaidRuleModels:
    @pytest.fixture(scope="class")
    def param(self):
        return {"model": InfoUnpaidRuleModel("test_model", "test_version", ["filter_col"])}

    def test_000_info_unpaid_no_return(self, param):
        assert param.get("model").predict(["N"]) == {"items": []}

    def test_001_info_unpaid_return(self, param):
        assert param.get("model").predict(["Y"]) == {
            "items": [{"id": "INF0000001", "name": "미납 요금 및 납부 안내", "type": "info_unpaid", "props": {}}]
        }
