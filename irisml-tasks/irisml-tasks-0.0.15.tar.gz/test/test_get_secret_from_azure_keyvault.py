import unittest
import unittest.mock
from irisml.tasks.get_secret_from_azure_keyvault import Task


class TestGetSecretFromAzureKeyvault(unittest.TestCase):
    @unittest.mock.patch('irisml.tasks.get_secret_from_azure_keyvault.SecretClient')
    def test_simple(self, mock_client):
        mock_secret = unittest.mock.MagicMock(value='secret_value')
        mock_client.return_value.get_secret.return_value = mock_secret
        outputs = Task(Task.Config('example', 'secret_name')).execute(Task.Inputs())
        self.assertEqual(outputs.secret, 'secret_value')
        mock_client.assert_called_with(vault_url='https://example.vault.azure.net', credential=unittest.mock.ANY)
