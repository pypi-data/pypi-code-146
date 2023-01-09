"""Test MessageService federated transport layer with LightGBM models."""
from collections.abc import Iterable
from typing import Callable
from unittest.mock import Mock

import pytest
from pytest import fixture

from tests.utils.concurrency_utils import run_local_modeller_and_workers
from tests.utils.helper import (
    AUC_THRESHOLD,
    backend_test,
    create_local_modeller_and_workers,
    integration_test,
)


@integration_test
class TestMessageServiceUsage:
    """Tests for Message Service federated transport layer for training jobs."""

    @fixture
    def mock_get_pod_public_keys(
        self, apply_mock_get_pod_public_keys: Callable[[str], Mock]
    ) -> Mock:
        """Mocks out get_pod_public_keys function in modeller.py."""
        return apply_mock_get_pod_public_keys(
            "bitfount.federated.modeller._get_pod_public_keys"
        )

    @pytest.mark.skip(
        "[BIT-1914] LGBMRandomForestClassifier incompatible with ResultsOnly"
    )
    @backend_test
    async def test_classifier_runs(
        self,
        mock_get_pod_public_keys: Mock,
        mock_message_aes_decryption: Mock,
        mock_message_aes_encryption: Mock,
        mock_rsa_encryption: Mock,
        mock_rsa_sign_message: Mock,
    ) -> None:
        """Tests that a Logistic Regression classifier runs."""
        modeller, workers = create_local_modeller_and_workers(
            model_name="LGBMRandomForestClassifier",
            protocol_name="ResultsOnly",
            algorithm_name="ModelTrainingAndEvaluation",
        )

        modeller_results = await run_local_modeller_and_workers(modeller, workers)

        assert isinstance(modeller_results, Iterable)
        for result in modeller_results:
            assert result is not None
            assert isinstance(result, dict)
            auc = result["AUC"]
            assert auc > AUC_THRESHOLD
