import logging
import os
from typing import Optional

import numpy as np
import pandas as pd

from truera.client.model_preprocessing import verify_python_model_folder
from truera.protobuf.public.metadata_message_types_pb2 import \
    FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION  # pylint: disable=no-name-in-module
from truera.protobuf.public.metadata_message_types_pb2 import \
    FEATURE_TRANSFORM_TYPE_NO_TRANSFORM  # pylint: disable=no-name-in-module
from truera.protobuf.public.metadata_message_types_pb2 import \
    FEATURE_TRANSFORM_TYPE_PRE_POST_DATA  # pylint: disable=no-name-in-module
from truera.protobuf.public.metadata_message_types_pb2 import \
    FeatureTransformationType  # pylint: disable=no-name-in-module
from truera.public.pyfunc_model import load_model

MODEL_PACKAGE_SUCCESS_MSG = "✔️ Verified packaged model format."
MODEL_PACKAGE_FAILURE_MSG = "❌ Model is not packaged properly. See error below: "
MODEL_LOAD_SUCCESS_MSG = "✔️ Loaded model in current environment."
MODEL_LOAD_FAILURE_MSG = "❌ Model failed to load. See error below: "
MODEL_PRED_SUCCESS_MSG = "✔️ Called predict on model."
MODEL_PRED_FAILURE_MSG = "❌ Model predict call failed on test data. See error below: "
SKIP_MODEL_PREDS_MSG = "❔ Skipping test model check, as no data splits exist in this data collection."
MALFORMED_MODEL_PREDS_MSG = "❌ Model predict call returned malformed object. See error below: "
VERIFICATION_SUCCESS_MSG = "✔️ Verified model output."


def validate_packaged_python_model(
    logger: logging.Logger,
    packaged_model_dir: str,
    test_data: Optional[pd.DataFrame] = None,
    is_regression_model: bool = False,
    feature_transform_type:
    FeatureTransformationType = FEATURE_TRANSFORM_TYPE_NO_TRANSFORM
):
    logger.info("Verifying model...")

    # step 0: make sure model package is formatted correctly
    try:
        verify_python_model_folder(
            packaged_model_dir, logger=logger, silent=True
        )
    except Exception as e:
        logger.info(MODEL_PACKAGE_FAILURE_MSG)
        raise e
    logger.info(MODEL_PACKAGE_SUCCESS_MSG)

    # step 1: load model
    try:
        loaded_model = load_model(packaged_model_dir)
    except Exception as e:
        logger.info(MODEL_LOAD_FAILURE_MSG)
        raise e
    logger.info(MODEL_LOAD_SUCCESS_MSG)

    # step 2: verify feature transform
    if feature_transform_type == FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION and not hasattr(
        loaded_model, "transform"
    ):
        raise AssertionError(
            "Model object is expected to have the transform method to use this data collection."
        )
    elif feature_transform_type in [
        FEATURE_TRANSFORM_TYPE_NO_TRANSFORM,
        FEATURE_TRANSFORM_TYPE_PRE_POST_DATA
    ] and hasattr(loaded_model, "transform"):
        raise AssertionError(
            "Model object is not expected to have the transform method to use this data collection."
        )

    # step 2: pull some data from system and test model
    if test_data is None:
        logger.info(SKIP_MODEL_PREDS_MSG)
        return
    try:
        has_transform = hasattr(loaded_model, "transform")
        if has_transform:
            test_data = loaded_model.transform(test_data)
            if not isinstance(test_data, pd.DataFrame):
                logger.info(MODEL_PRED_FAILURE_MSG)
                raise AssertionError(
                    f"Transform call on model outputted object of type {type(test_data)}, expected pd.DataFrame!"
                )
        ys_pred = loaded_model.predict(test_data)
    except Exception as e:
        logger.info(MODEL_PRED_FAILURE_MSG)
        raise e
    logger.info(MODEL_PRED_SUCCESS_MSG)

    # step 3: verify output of model
    if is_regression_model:
        if not isinstance(ys_pred, (np.ndarray, pd.Series)):
            logger.info(MALFORMED_MODEL_PREDS_MSG)
            raise AssertionError(
                f"Predict call on model outputted object of type {type(ys_pred)}, expected np.ndarray or pd.Series for regression model!"
            )

        if ys_pred.shape != (1,):
            logger.info(MALFORMED_MODEL_PREDS_MSG)
            raise AssertionError(
                f"Predict call on model outputted array of shape {ys_pred.shape}, expected shape (1,) for regression model!"
            )

    else:
        if not isinstance(ys_pred, pd.DataFrame):
            logger.info(MALFORMED_MODEL_PREDS_MSG)
            raise AssertionError(
                f"Predict call on model outputted object of type {ys_pred}, expected pd.DataFrame for classification model!"
            )

        if ys_pred.shape != (1, 2):  # assumes binary classification
            logger.info(MALFORMED_MODEL_PREDS_MSG)
            raise AssertionError(
                f"Predict call on model outputted pd.DataFrame of shape {ys_pred.shape}, expected shape (1, 2) for classification model!"
            )

    logger.info(VERIFICATION_SUCCESS_MSG)
    logger.info("Verification succeeded!")
