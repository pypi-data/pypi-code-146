import os
from vid2info.inference.config import GENERAL_MODELS_PATH

# All paths are specified from the root directory of the project
MODEL_NAME = 'yolov7-tiny'
MODELS_PATH = os.path.join(GENERAL_MODELS_PATH, 'detection')
WEIGTHS_PATH = os.path.join(MODELS_PATH, MODEL_NAME + '.pt')

DETECTOR_MIN_CONFIDENCE_TH = 0.5
IOU_NMS_TH = 0.5
MAX_DETECTIONS_PER_IMAGE = 75
DETECTOR_IMAGE_SIZE = 640
HALF_MODE = False
NORMALIZE_OUTPUT = True

DATASET_YML = os.path.join(MODELS_PATH, MODEL_NAME + '.yml')

CLASS_ID_POSITION_IN_BBOX = 5
DEFAULT_MAX_CLASSES = 80
