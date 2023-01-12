import unittest
import waveletai
import uuid
from waveletai.model import Model, ModelVersion
from waveletai.experiment import Experiment
from waveletai.constants import Visibility, ModelSourceType
import os

class ModelTestCase(unittest.TestCase):
    global app_id
    global model_id
    global experiment_id
    global repo_id

    def setUp(self):
        globals()["app_id"] = "b0a81f012780401391bc2ed0e6046c13"
        super(ModelTestCase, self).setUp()
        waveletai.init(
            api_token="eyJhcGlfdXJsIjogImh0dHA6Ly9mYXQuYWkueGlhb2JvZGF0YS5jb20vYXBpIiwgInVzZXJfaWQiOiAiODhmNmJmODY2NTU2NGI0ZDgxODc1NmMzNTc4YzI0MjIiLCAiYXBpX3Rva2VuIjogIjM5MWVlMTU0OTNiNmE0ZmU5MjA5NWZlNjUyZjFhZWY2YzAyNjIzMDE2MTdjNjlhMjM1ZmQyYjU1OTRhZTAxMzMifQ==")
        waveletai.set_app(app_id)

    def test_01_create_model(self):
        model: Model = waveletai.create_model(name='sdk_test_case', visibility=Visibility.PRIVATE.value, source=ModelSourceType.FLOW.value)
        globals()["model_id"] = model.id
        # globals()["model_id"] = '16a48da654ce4475ab6084ba2bbdf1be'
        self.assertEqual("sdk_test_case", model.name)
        print(model.id)

    def test_02_get_model(self):
        waveletai.set_app(app_id)
        waveletai.set_model(model_id)
        model: Model = waveletai.get_model()
        self.assertEqual("sdk_test_case", model.name)

    def test_03_update_model(self):
        waveletai.set_app(app_id)
        waveletai.set_model(model_id)
        name = "sdk-u-" + str(uuid.uuid4()).split("-")[0]
        model: Model = waveletai.update_model(name=name, visibility='private', desc='123')
        self.assertEqual(name, model.name)

    def test_04_register_model_version(self):
        waveletai.set_app(app_id)
        waveletai.set_model(model_id)
        modelrepo: ModelVersion = waveletai.register_model_version(desc='123',
                                                                   artifacts='modelrepo_files/',
                                                                   json_data={"test":1})
        globals()['repo_id'] = modelrepo.id
        self.assertEqual(model_id, modelrepo.model_id)

    def test_05_download_asset(self):
        waveletai.set_app(app_id)
        waveletai.set_model(model_id)
        waveletai.download_model_version_asset(repo_id, 'model', './download_model_version_asset/')

        for curDir, dirs, files in os.walk("download_model_version_asset/model"):
            if "model" in curDir:
                self.assertIn("conda.yaml", files)

    def test_06_get_model_version(self):
        waveletai.set_app(app_id)
        waveletai.set_model(model_id)
        modelrepo: ModelVersion = waveletai.get_model_version_by_model('V1')
        self.assertEqual('V1', modelrepo.version)

    def test_07_list_model_versions(self):
        waveletai.set_app(app_id)
        waveletai.set_model(model_id)
        page = -1
        pagesize = 10
        modelrepos = waveletai.list_model_versions(page, pagesize)

    def test_08_update_model_version(self):
        waveletai.set_app(app_id)
        waveletai.set_model(model_id)
        modelrepo: ModelVersion = waveletai.update_model_version('V1', '123')
        self.assertEqual('V1', modelrepo.version)

    def test_09_abandon_model_version(self):
        waveletai.set_app(app_id)
        waveletai.set_model(model_id)
        res = waveletai.abandon_model_version('V1')

    def test_10_list_experiments(self):
        waveletai.set_app(app_id)
        waveletai.set_model(model_id)
        experiments = waveletai.list_experiments()

    def test_11_list_release(self):
        waveletai.set_app(app_id)
        waveletai.set_model(model_id)
        model_releases = waveletai.list_model_releases('V1')

    def test_12_create_experiment(self):
        waveletai.set_app(app_id)
        waveletai.set_model(model_id)
        experiment: Experiment = waveletai.create_experiment(name='123')
        globals()["experiment_id"] = experiment.id
        self.assertEqual('123', experiment.name)

    def test_13_get_experiment(self):
        waveletai.set_app(app_id)
        waveletai.set_model(model_id)
        experiment: Experiment = waveletai.get_experiment(experiment_id=experiment_id)
        self.assertEqual(experiment_id, experiment.id)

    def test_14_list_releases_by_repo(self):
        waveletai.set_app(app_id)
        waveletai.set_model(model_id)
        releases = waveletai.list_model_releases_by_repo(repo_id)

    def test_15_delete_model(self):
        waveletai.set_app(app_id)
        waveletai.set_model(model_id)
        res = waveletai.delete_model()


if __name__ == '__main__':
    unittest.main()
