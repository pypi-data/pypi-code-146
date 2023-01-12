import os

DEFAULT_DATASET_DIR = 'dataset'
DEFAULT_TRAIN_FOLDER = 'train'
DEFAULT_RAW_VIDEOS_FOLDER = 'raw_videos'

DEFAULT_TRAIN_DIR = os.path.join('.', DEFAULT_DATASET_DIR, DEFAULT_TRAIN_FOLDER)
DEFAULT_RAW_VIDEOS_DIR = os.path.join('.', DEFAULT_DATASET_DIR, DEFAULT_RAW_VIDEOS_FOLDER)


DO_YOU_WANT_TO_REMOVE_FOLDER_CONTENT = "{} is not empty. Do you want to remove its content?"