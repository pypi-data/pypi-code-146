################################################################################
# IBM Confidential
# OCO Source Materials
# 5737-H76, 5725-W78, 5900-A1R
# (c) Copyright IBM Corp. 2022. All Rights Reserved.
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
################################################################################

""" Constants needed to support validation and selection of pipelines """

from fractions import Fraction
from enum import Enum, unique

ANOMALY = -1
NON_ANOMALY = 1
UNKNOWN_ANOMALY = 0

ESTIMATOR_TYPES = ["Window", "Forecasting", "Relationship"]
PIPELINES = [
    "PointwiseBoundedHoltWintersAdditive",
    "PointwiseBoundedBATS",
    "PointwiseBoundedBATSForceUpdate",
    "WindowNN",
    "WindowPCA",
    "WindowLOF",
]

# NOTE: adding/updating values in PIPELINE_INFO must
# update those defined in get_pipeline_name() within each pipeline class
PIPELINE_INFO = [
    # Window: 8
    {"name": "WindowIsolationForest", "estimator_type": "Window"},
    {"name": "WindowTSIsolationForest", "estimator_type": "Window"},
    {"name": "WindowNN", "estimator_type": "Window"},
    {"name": "WindowLOF", "estimator_type": "Window"},
    {"name": "WindowKNN", "estimator_type": "Window"},
    {"name": "ExtendedWindowIsolationForest", "estimator_type": "Window"},
    {"name": "DataStationExtendedWindowIsolationForest", "estimator_type": "Window"},
    {"name": "ExtendedWindowOneClassSVM", "estimator_type": "Window"},
    # Forecasting: 9
    {"name": "WindowResidualBATS", "estimator_type": "Forecasting"},
    {"name": "PointwiseBoundedHoltWintersAdditive", "estimator_type": "Forecasting"},
    {
        "name": "PointwiseBoundedHoltWintersMultiplicative",
        "estimator_type": "Forecasting",
    },
    {"name": "PointwiseBoundedBATS", "estimator_type": "Forecasting"},
    {"name": "PointwiseBoundedBATSForceUpdate", "estimator_type": "Forecasting"},
    {"name": "XGB", "estimator_type": "Forecasting"},
    {"name": "RandomForest", "estimator_type": "Forecasting"},
    {"name": "Bagging", "estimator_type": "Forecasting"},
    {"name": "T2RForecaster", "estimator_type": "Forecasting"},
    # Relationship: 2
    {"name": "GraphLasso", "estimator_type": "Relationship"},
    {"name": "WindowPCA", "estimator_type": "Relationship"},
]

RUNMODE_TEST = "test"
RUNMODE_INTEGRATION = "integration"
# Needed by run_time_series_ad
VALID_PIPELINES = [rec["name"] for rec in PIPELINE_INFO]
VERBOSE = False  # Set True to print out more information during training process

"""
Specify upper cap of validation set in which synt.anomalies are injected.
Upper cap as the stage of injecting anomalies + detecting them is very time consuming
TODO: apply heuristic ways to choose this upper cap based on time series characteristics
eg, seasonality, lookback windows, etc.
"""
MAX_VALIDATION_SIZE = 500  # as suggested by SROM team, instead of 10000

# maximum number of `feature_columns` to be testable in the RUNNING_TEST mode:
MAX_TARGET_SERIES_NUMBER = 100

# Below "name" MUST be consistent with those defined in prep_cv.py:
SYNTHESIZED_ANOMALY = [
    {"name": "LocalizedExtreme", "pattern": "Point", "type": "LocalizedExtreme"},
    {"name": "LevelShift", "pattern": "Segment", "type": "LevelShift"},
    {"name": "Variance", "pattern": "Segment", "type": "Variance"},
    {"name": "Trend", "pattern": "Segment", "type": "Trend"},
]

VALID_METRICS = [
    "f1",
    # "f1_macro",
    # "f1_micro",
    # "f1_weighted",
    "precision",
    "recall",
    "accuracy",
    "balanced_accuracy",
    "roc_auc",
    "average_precision",
    "pr_auc",
    "f1_pa",
]

GLOBAL_DEFAULT_SEED = 33

LEARNING_TYPE_TIMESERIES_FORECASTING = "forecasting"
# To support semi-supervised use case in MVP
LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION = "timeseries_anomaly_prediction"
# Reserved for supporting suppervised use case in future
LEARNING_TYPE_TIMESERIES_ANOMALY_DETECTION = "timeseries_anomaly_detection"

@unique
class DataType(Enum):
    INPUT = "input"
    TRAINING = "training"
    HOLDOUT = "holdout"


# Column Role
COLUMN_ROLE_TARGET = "target"
COLUMN_ROLE_SUPPORTING_FEATURE = "supporting feature"
COLUMN_ROLE_FEATURE = "feature"
COLUMN_ROLE_TIMESTAMP = "timestamp"
COLUMN_ROLE_ANOMALY_LABEL = "label"

# TShirt Size
# Small means 2vCPUs and 8GB of RAM
TSHIRT_SIZE_SMALL = "S"
# Medium means 4vCPUs and 16GB of RAM
TSHIRT_SIZE_MEDIUM = "M"
# Large means 8vCPUs and 32GB of RAM
TSHIRT_SIZE_LARGE = "L"
# Extral Large means 16CPUs and 64GB of RAM
TSHIRT_SIZE_EXTRA_LARGE = "XL"

# Pre-defined some keys used in INPUT_DATA_LIMITATION below
COLUMN = "COLUMN"
ROW = "ROW"
MAX = "MAX"
MIN = "MIN"
THRESHOLD = "THRESHOLD"
HOLDOUT_MAX_RATIO = "HOLDOUT_MAX_RATIO"
HOLDOUT_MIN = "HOLDOUT_MIN"
HOLDOUT_MAX = "HOLDOUT_MAX"

# Constant value of input data limitations for pre-assessment of customer cluster setup
INPUT_DATA_LIMITATION = {
    LEARNING_TYPE_TIMESERIES_FORECASTING: {
        ROW: {MIN: 8, THRESHOLD: 36, HOLDOUT_MAX_RATIO: Fraction(1, 3)},
        TSHIRT_SIZE_SMALL: {COLUMN: {MAX: 5}, ROW: {MAX: 20000}},
        TSHIRT_SIZE_MEDIUM: {COLUMN: {MAX: 10}, ROW: {MAX: 80000}},
        TSHIRT_SIZE_LARGE: {COLUMN: {MAX: 15}, ROW: {MAX: 300000}},
        TSHIRT_SIZE_EXTRA_LARGE: {COLUMN: {MAX: 20}, ROW: {MAX: 1000000}},
    },
    LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION: {
        ROW: {
            MIN: 30,
            HOLDOUT_MAX_RATIO: Fraction(1, 3),
            HOLDOUT_MIN: 10,
            HOLDOUT_MAX: 500,
        },
        # TODO: The below column/record limitation would be finalized after performance profiling.
        # For now, relex all MAX value for unblocking the testing.
        TSHIRT_SIZE_SMALL: {COLUMN: {MAX: 100000}, ROW: {MAX: 100000000}},
        TSHIRT_SIZE_MEDIUM: {COLUMN: {MAX: 100000}, ROW: {MAX: 100000000}},
        TSHIRT_SIZE_LARGE: {COLUMN: {MAX: 100000}, ROW: {MAX: 100000000}},
        TSHIRT_SIZE_EXTRA_LARGE: {COLUMN: {MAX: 100000}, ROW: {MAX: 100000000}},
    },
}


