import unittest
import waveletai
import os
from waveletai.app import App
from waveletai.model import Model
from waveletai.feature import Feature
from waveletai.constants import FeatureType


class AppTestCase(unittest.TestCase):
    global app_id
    global dataset_id

    def setUp(self):
        globals()["app_id"] = "b0a81f012780401391bc2ed0e6046c13"
        super(AppTestCase, self).setUp()
        waveletai.init(
            api_token="eyJhcGlfdXJsIjogImh0dHA6Ly9mYXQuYWkueGlhb2JvZGF0YS5jb20vYXBpIiwgInVzZXJfaWQiOiAiODhmNmJmODY2NTU2NGI0ZDgxODc1NmMzNTc4YzI0MjIiLCAiYXBpX3Rva2VuIjogIjM5MWVlMTU0OTNiNmE0ZmU5MjA5NWZlNjUyZjFhZWY2YzAyNjIzMDE2MTdjNjlhMjM1ZmQyYjU1OTRhZTAxMzMifQ==")

    def test_1_download_feature_zip(self):
        waveletai.set_app(app_id)
        res = waveletai.download_dataset_artifacts('820651493c5b4ae68db79fa12aa1aac0', './feature_zip/coco', unzip=True,
                                                   feature_type=FeatureType.COCO.value)
        res = waveletai.download_dataset_artifacts('820651493c5b4ae68db79fa12aa1aac0', './feature_zip/voc', unzip=True,
                                                   feature_type=FeatureType.VOC.value)
        res = waveletai.download_dataset_artifacts('820651493c5b4ae68db79fa12aa1aac0', './feature_zip/yolov5',
                                                   unzip=True, feature_type=FeatureType.YOLOV5.value)
        res = waveletai.download_dataset_artifacts('820651493c5b4ae68db79fa12aa1aac0', './feature_zip/yolov3',
                                                   unzip=True, feature_type=FeatureType.YOLOV3DARKNET.value)


if __name__ == '__main__':
    unittest.main()
