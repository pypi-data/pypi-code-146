import pytest

from sktmls.models.contrib import VasXcloudRuleModel


class TestVasXcloudRuleModels:
    @pytest.fixture(scope="class")
    def param(self):
        return {
            "model": VasXcloudRuleModel(
                "test_model",
                "test_version",
                [
                    "age",
                    "real_arpu_bf_m1",
                    "app_use_traffic_game",
                    "app_use_days_video_median_yn",
                    "data_use_night_ratio_median_yn",
                ],
            )
        }

    def test_000_vax_xcloud_return(self, param):
        assert param.get("model").predict([5, 55000, 10000, "Y", "Y"]) == {"items": []}

    def test_001_vax_xcloud_return(self, param):
        assert param.get("model").predict([20, 10000, 10000, "Y", "Y"]) == {"items": []}

    def test_002_vax_xcloud_return(self, param):
        assert param.get("model").predict([20, 55000, 0, "N", "N"]) == {"items": []}

    def test_003_vax_xcloud_return(self, param):
        assert param.get("model").predict([20, 55000, 10000, "Y", "Y"]) == {
            "items": [
                {
                    "id": "NA00007114",
                    "name": "게임패스 얼티밋",
                    "type": "vas_xcloud",
                    "props": {"context_id": "context_default"},
                }
            ]
        }

    def test_004_vax_xcloud_return(self, param):
        assert param.get("model").predict([20, 55000, 0, "Y", "Y"]) == {
            "items": [
                {
                    "id": "NA00007114",
                    "name": "게임패스 얼티밋",
                    "type": "vas_xcloud",
                    "props": {"context_id": "context_default"},
                }
            ]
        }

    def test_005_vax_xcloud_return(self, param):
        assert param.get("model").predict([20, 55000, 10000, "N", "Y"]) == {
            "items": [
                {
                    "id": "NA00007114",
                    "name": "게임패스 얼티밋",
                    "type": "vas_xcloud",
                    "props": {"context_id": "context_default"},
                }
            ]
        }

    def test_006_vax_xcloud_return(self, param):
        assert param.get("model").predict([20, 55000, 10000, "Y", "N"]) == {
            "items": [
                {
                    "id": "NA00007114",
                    "name": "게임패스 얼티밋",
                    "type": "vas_xcloud",
                    "props": {"context_id": "context_default"},
                }
            ]
        }
