from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.absolute()

CONFIG_DIR = BASE_DIR / "configs"

# For Experiment Manager
EXP_DIR = BASE_DIR / "experiments"
EXP_LOG_FILENAME = "run.log"
EXP_PIPELINE_CONFIG_FILENAME = "pipeline_config.yaml"
EXP_MODEL_ANALYSIS_SUBDIR = "model_analysis"
EXP_PIPELINE_BUNDLE_FILENAME = "pipeline_bundle.pickle"

# For Feature Manager
FEATURE_BUNDLE_FILENAME = "feature_bundle.pickle"
FM_FEATURE_SUBDIR = "features"

# For Model Analysis
MA_TRAIN_DATASET_NAME = "train"
MA_VAL_DATASET_NAME = "val"
MA_PREDICTION_FILENAME = "prediction.csv"
MA_OVERALL_NAME = "OVERALL"
MA_SAMPLE_COUNT_NAME = "sample_count"
MA_PRED_COL = "prediction"
MA_PRED_PROBA_COL = "prediction_probability"

SAVE_MODEL_NAME = "model_0"
