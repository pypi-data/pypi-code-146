import unittest
import waveletai
import os
import uuid
from waveletai.dataset import Dataset


class DataTestCase(unittest.TestCase):
    global app_id
    global dataset_id

    def setUp(self):
        globals()["app_id"] = "b0a81f012780401391bc2ed0e6046c13"
        super(DataTestCase, self).setUp()
        waveletai.init(
            api_token="eyJhcGlfdXJsIjogImh0dHA6Ly9mYXQuYWkueGlhb2JvZGF0YS5jb20vYXBpIiwgInVzZXJfaWQiOiAiODhmNmJmODY2NTU2NGI0ZDgxODc1NmMzNTc4YzI0MjIiLCAiYXBpX3Rva2VuIjogIjM5MWVlMTU0OTNiNmE0ZmU5MjA5NWZlNjUyZjFhZWY2YzAyNjIzMDE2MTdjNjlhMjM1ZmQyYjU1OTRhZTAxMzMifQ==")

    def test_1_create_dataset(self):
        waveletai.set_app(app_id)
        dataset: Dataset = waveletai.create_dataset(name="test_data", path="dataset_init/")
        globals()["dataset_id"] = dataset.id
        self.assertEqual("test_data", dataset.name)
        print(dataset.id)

    def test_2_get_dataset(self):
        waveletai.set_app(app_id)
        dataset: Dataset = waveletai.get_dataset(dataset_id)
        self.assertEqual("test_data", dataset.name)

    def test_3_upload_dataset_artifacts(self):
        waveletai.set_app(app_id)
        waveletai.upload_dataset_artifacts(dataset_id, "dataset_update/")

    def test_4_download_dataset_artifact(self):
        # globals()["dataset_id"] = "53220cd73f574115bf90108d75a2310e"
        globals()["dataset_id"] = dataset_id
        dataset: Dataset = waveletai.get_dataset(dataset_id)
        dataset.download_artifact("2/test_AI_model_data_164.xls", "dataset_download/single/")
        for curDir, dirs, files in os.walk("dataset_download/single/"):
            self.assertEqual("test_AI_model_data_164.xls", files[0])

    def test_5_download_dataset_artifacts(self):
        # globals()["dataset_id"] = "53220cd73f574115bf90108d75a2310e"
        globals()["dataset_id"] = dataset_id
        dataset: Dataset = waveletai.get_dataset(dataset_id)
        dataset.download_artifacts("./dataset_download/")
        for curDir, dirs, files in os.walk("dataset_download/"):
            if "json" in curDir:
                self.assertIn("a.yaml", files)
            if "2" in curDir:
                self.assertIn("test_AI_model_data_164.xls", files)

    def test_6_update_dataset(self):
        waveletai.set_app(app_id)
        name = "sdk-u-"+str(uuid.uuid4()).split("-")[0]
        dataset: Dataset = waveletai.get_dataset(dataset_id)
        dataset.update(name=name, desc="sdk-update-data-desc-1")
        dataset: Dataset = waveletai.get_dataset(dataset_id)
        self.assertEqual(name, dataset.name)

    def test_7_del_dataset(self):
        waveletai.set_app(app_id)
        waveletai.delete_dataset(dataset_id)

    # def test_8_get_netease(self):
    #     waveletai.set_app('d857f8b29eef4a96b1a53cb593d061a7')
    #     data = waveletai.download_data('c5724a6230b540d3bd97fe8b68238f0d', 'raw_data.csv', 'dataset_download/single/')
    #     print(data)

    def test_get_ip(self):
        # 可以封装成函数，方便 Python 的程序调用
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        print(ip)
        return ip


if __name__ == '__main__':
    unittest.main()
