import unittest
from uvs_training_sdk import TrainingClient, ResourceType


class TestClients(unittest.TestCase):
    def test_create_multi_service_client_fails_when_endpoint_missing(self):
        with self.assertRaises(AssertionError):
            TrainingClient(ResourceType.MultiServiceResource, None, None, 'test_key')

    def test_create_multi_service_client_works(self):
        TrainingClient(ResourceType.MultiServiceResource, None, 'https://endpoints.com', 'test_key')

    def test_create_single_service_client_fails_when_resource_name_missing(self):
        with self.assertRaises(AssertionError):
            TrainingClient(ResourceType.MultiServiceResource, None, None, 'test_key')
