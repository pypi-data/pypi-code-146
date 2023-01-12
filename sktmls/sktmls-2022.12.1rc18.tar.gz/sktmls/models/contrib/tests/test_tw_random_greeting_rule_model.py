from sktmls.models.contrib import TwRandomGreetingRuleModel


class TestTwRanndomGreetingRuleModels:
    def test_000_random_greeting_return(self):
        rgr = TwRandomGreetingRuleModel(
            "test_model", "test_version", ["A", "B"], ["A", "B", "C"], ["C1", "C2", "C3", "C4", "C5"]
        )
        result = rgr.predict(None)
        greeting_image = result.get("items")[0]
        greeting_image_bucket = greeting_image.pop("props")
        greeting_text = result.get("items")[1]
        greeting_text_bucket = greeting_text.pop("props")
        greeting_ranking = result.get("items")[2]
        greeting_ranking_bucket = greeting_ranking.pop("props")

        assert greeting_image == {
            "id": "tw_greeting_image",
            "name": "티월드그리팅이미지타입",
            "type": "tw_greeting",
        }
        assert greeting_image_bucket.get("bucket") in ["A", "B"]

        assert greeting_text == {
            "id": "tw_greeting_text",
            "name": "티월드그리팅텍스트타입",
            "type": "tw_greeting",
        }
        assert greeting_text_bucket.get("bucket") in ["A", "B", "C"]

        assert greeting_ranking == {
            "id": "tw_greeting_ranking",
            "name": "티월드그리팅랭킹",
            "type": "tw_greeting",
        }
        assert set(greeting_ranking_bucket.get("ranking")) == set(["C1", "C2", "C3", "C4", "C5"])
