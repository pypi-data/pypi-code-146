import json

from assertpy import assert_that


class BoundingBoxes():
    def __init__(self, key: str, box_data: dict, class_labels: dict):
        self.key = key
        self.box_data = box_data
        self.class_labels = class_labels

        # validtaion
        self.validate()

    def validate(self):
        try:
            for data in self.box_data:
                assert_that(data).contains("position", "class_id", "scores", "caption")  # key값 검증
                assert_that(data['position']).is_instance_of(dict)
                assert_that(data['position']).contains("minX", "maxX", "minY", "maxY")
                assert_that(data['position']["minX"]).is_instance_of((float, int))
                assert_that(data['position']["maxX"]).is_instance_of((float, int))
                assert_that(data['position']["minY"]).is_instance_of((float, int))
                assert_that(data['position']["maxY"]).is_instance_of((float, int))
                assert_that(data['class_id']).is_instance_of(int)
                assert_that(data['scores']).contains("acc", "loss")
                assert_that(data['scores']["acc"]).is_instance_of((float, int))
                assert_that(data['scores']["loss"]).is_instance_of((float, int))
                if "unit" in data:
                    assert_that(data['unit']).is_instance_of(str)
                assert_that(data['caption']).is_instance_of(str)
        except AssertionError as e:
            raise Exception(f"BoundingBoxes Valition Error : {e.message}")

    def to_json(self):
        return json.dumps({
            "box_data": self.box_data,
            "class_labels": self.class_labels,
        })

    def to_dict(self):
        return {
            "box_data": self.box_data,
            "class_labels": self.class_labels,
        }