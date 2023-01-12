import os

INFERENCE_DEVICE = 'cpu'
GENERAL_MODELS_PATH = os.path.join('.', 'vid2info', 'inference', 'models')
XMIN, YMIN, XMAX, YMAX, CONFIDENCE, CLASS_ID = 'xmin', 'ymin', 'xmax', 'ymax', 'confidence', 'class_id'
CLASS_NAME, CLASS_NAMES_LIST, BBOX_XYXY = 'class_name', 'class_names_list', 'bbox_xyxy'

SEGMENTATION_MASK, BACKGROUND_CLASS_IDX = 'segmentation_mask', 'background_class_idx'

SEGMENTATION_MAKS_DICT_KEYS = (CLASS_NAMES_LIST, SEGMENTATION_MASK, BACKGROUND_CLASS_IDX)
UINT8_TO_FLOAT = 1/255
