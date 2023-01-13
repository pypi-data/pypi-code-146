import unittest
import waveletai
import os
import uuid
from waveletai.app import App
from waveletai.model import Model
from waveletai.constants import Visibility


class AppTestCase(unittest.TestCase):
    global app_id
    global dataset_id

    def setUp(self):
        super(AppTestCase, self).setUp()
        waveletai.init(
            api_token="eyJhcGlfdXJsIjogImh0dHA6Ly9mYXQuYWkueGlhb2JvZGF0YS5jb20vYXBpIiwgInVzZXJfaWQiOiAiODhmNmJmODY2NTU2NGI0ZDgxODc1NmMzNTc4YzI0MjIiLCAiYXBpX3Rva2VuIjogIjM5MWVlMTU0OTNiNmE0ZmU5MjA5NWZlNjUyZjFhZWY2YzAyNjIzMDE2MTdjNjlhMjM1ZmQyYjU1OTRhZTAxMzMifQ==")

    def test_1_create_app(self):
        app: App = waveletai.create_app(name="test_sdk_1", tags=[], visibility=Visibility.PRIVATE.value)
        globals()["app_id"] = app.id
        self.assertEqual("test_sdk_1", app.name)

    def test_2_update_app(self):
        waveletai.set_app(app_id)
        name = "sdk-u-" + str(uuid.uuid4()).split("-")[0]
        app: App = waveletai.update_app(name=name, desc='sdk_update', tags=[])
        self.assertEqual(name, app.name)

    def test_3_create_model(self):
        waveletai.set_app(app_id)
        model: Model = waveletai.create_model(name='sdk_test')
        self.assertEqual('sdk_test', model.name)

    def test_4_list_model(self):
        waveletai.set_app(app_id)
        res = waveletai.list_models()
        self.assertTrue(len(res) > 0)

    def test_5_delete_app(self):
        waveletai.set_app(app_id)
        res = waveletai.delete_app()


if __name__ == '__main__':
    unittest.main()
