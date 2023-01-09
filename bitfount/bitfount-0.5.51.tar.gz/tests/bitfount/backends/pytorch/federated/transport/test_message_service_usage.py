"""Tests for MessageService federated transport layer with PyTorch models."""
from collections.abc import Sequence
from typing import Callable
from unittest.mock import Mock

from pytest import fixture

from tests.utils.concurrency_utils import run_local_modeller_and_workers
from tests.utils.helper import (
    AUC_THRESHOLD,
    backend_test,
    create_local_modeller_and_workers,
    integration_test,
)


@backend_test
@integration_test
class TestMessageServiceUsage:
    """Tests for the message service classes using PyTorch models."""

    @fixture
    def mock_get_pod_public_keys(
        self, apply_mock_get_pod_public_keys: Callable[[str], Mock]
    ) -> Mock:
        """Mocks out get_pod_public_keys function in modeller.py."""
        return apply_mock_get_pod_public_keys(
            "bitfount.federated.modeller._get_pod_public_keys"
        )

    async def test_classification_results_only(
        self,
        mock_get_pod_public_keys: Mock,
        mock_message_aes_decryption: Mock,
        mock_message_aes_encryption: Mock,
        mock_rsa_encryption: Mock,
        mock_rsa_sign_message: Mock,
    ) -> None:
        """Tests PyTorchTabularClassifier with ResultsOnly protocol."""
        modeller, workers = create_local_modeller_and_workers(
            model_name="PyTorchTabularClassifier",
            protocol_name="ResultsOnly",
            algorithm_name="ModelTrainingAndEvaluation",
        )

        modeller_results = await run_local_modeller_and_workers(modeller, workers)

        assert isinstance(modeller_results, dict)
        for result in modeller_results.values():
            assert result is not None
            assert isinstance(result, dict)
            auc = result["AUC"]
            assert auc > AUC_THRESHOLD

    async def test_classification_federated_averaging_and_early_stopping_autoeval_true(
        self,
        mock_get_pod_public_keys: Mock,
        mock_message_aes_decryption: Mock,
        mock_message_aes_encryption: Mock,
        mock_rsa_encryption: Mock,
        mock_rsa_sign_message: Mock,
    ) -> None:
        """Tests PyTorchTabularClassifier with FederatedAveraging and EarlyStopping."""
        modeller, workers = create_local_modeller_and_workers(
            model_name="PyTorchTabularClassifier",
            protocol_name="FederatedAveraging",
            algorithm_name="FederatedModelTraining",
            early_stopping=True,
        )

        modeller_results = await run_local_modeller_and_workers(modeller, workers)

        assert modeller_results is not None
        assert isinstance(modeller_results, Sequence)
        auc = float(modeller_results[0]["AUC"])
        assert auc > AUC_THRESHOLD

    async def test_classification_federated_averaging_and_early_stopping_autoeval_false(
        self,
        mock_get_pod_public_keys: Mock,
        mock_message_aes_decryption: Mock,
        mock_message_aes_encryption: Mock,
        mock_rsa_encryption: Mock,
        mock_rsa_sign_message: Mock,
    ) -> None:
        """Tests PyTorchTabularClassifier with FederatedAveraging and EarlyStopping."""
        modeller, workers = create_local_modeller_and_workers(
            model_name="PyTorchTabularClassifier",
            protocol_name="FederatedAveraging",
            algorithm_name="FederatedModelTraining",
            early_stopping=True,
            auto_eval=False,
        )

        modeller_results = await run_local_modeller_and_workers(modeller, workers)

        assert modeller_results == []

    async def test_classification_secure_aggregation(
        self,
        mock_get_pod_public_keys: Mock,
        mock_message_aes_decryption: Mock,
        mock_message_aes_encryption: Mock,
        mock_rsa_decryption: Mock,
        mock_rsa_encryption: Mock,
        mock_rsa_sign_message: Mock,
    ) -> None:
        """Tests PyTorchTabularClassifier Federated Averaging and Secure Aggregation."""
        modeller, workers = create_local_modeller_and_workers(
            model_name="PyTorchTabularClassifier",
            protocol_name="FederatedAveraging",
            algorithm_name="FederatedModelTraining",
            secure_aggregation=True,
        )

        modeller_results = await run_local_modeller_and_workers(modeller, workers)

        assert modeller_results is not None
        assert isinstance(modeller_results, Sequence)
        auc = float(modeller_results[0]["AUC"])
        assert auc > AUC_THRESHOLD
