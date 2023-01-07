import os
import cv2
from argparse import ArgumentParser
from .tools import compare


def get_args():
    parser = ArgumentParser()
    parser.add_argument("path", type=str)
    args = parser.parse_args()
    return args


def compare_images_in_directory(path: str):
    files = os.listdir(path)
    images = [cv2.imread(os.path.join(path, f)) for f in files]
    compare(images)


args = get_args()
compare_images_in_directory(**vars(args))
