import os
from vid2info.inference.config import GENERAL_MODELS_PATH
# All paths are specified from the root directory of the project
MODEL_NAME = 'pidnet_small'
MODELS_PATH = os.path.join(GENERAL_MODELS_PATH, 'segmentation')
WEIGTHS_PATH = os.path.join(MODELS_PATH, MODEL_NAME+'.pt')
PIDNET_SCALE_FACTOR = 8

PARAMS_YAML = os.path.join(MODELS_PATH, MODEL_NAME+'.yml')

