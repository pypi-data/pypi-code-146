import pytest

from sktmls.models.contrib import InfoDefectRuleModel


class TestInfoDefectRuleModel:
    @pytest.fixture(scope="class")
    def param(self):
        return {"model": InfoDefectRuleModel("test_model", "test_version", ["svc_scrb_period", "eqp_chg_period"])}

    def test_000_info_defect_return(self, param):
        assert param.get("model").predict([10, 0]) == {
            "items": [{"id": "INF0000004", "name": "초기 불량 대처 방법 안내", "props": {}, "type": "info_defect"}]
        }

    def test_001_info_defect_return(self, param):
        assert param.get("model").predict([50, 15]) == {
            "items": [{"id": "INF0000004", "name": "초기 불량 대처 방법 안내", "props": {}, "type": "info_defect"}]
        }

    def test_002_info_defect_return(self, param):
        assert param.get("model").predict([10, 15]) == {
            "items": [{"id": "INF0000004", "name": "초기 불량 대처 방법 안내", "props": {}, "type": "info_defect"}]
        }

    def test_003_info_defect_return(self, param):
        assert param.get("model").predict([50, 0]) == {"items": []}
