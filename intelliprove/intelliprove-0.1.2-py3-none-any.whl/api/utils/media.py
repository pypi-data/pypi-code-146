import cv2
import tempfile
import os

from typing import Union
from pathlib import Path
from uuid import uuid4
from intelliprove.api.exceptions import MediaException


def is_valid_image_path(im_path: Union[Path, str]) -> bool:
    im_path = Path(im_path) if isinstance(im_path, str) else im_path
    return im_path.is_file() and im_path.suffix.lower() in ('.png', '.jpg', '.jpeg')


def is_valid_video_path(vid_path: Union[Path, str]) -> bool:
    im_path = Path(vid_path) if isinstance(vid_path, str) else vid_path
    return im_path.is_file() and im_path.suffix.lower() in ('.mp4', '.m4v', '.h264', '.mov', '.avi')


def get_first_video_frame(video_path: Union[Path, str]) -> Path:
    video_path = str(video_path)

    cap = cv2.VideoCapture(video_path)
    cap.open(video_path)
    success, image = cap.read()
    if not success:
        raise Exception(f'Could not read first frame from video. Video path: {video_path}')

    tempdir = tempfile.gettempdir()
    filename = f"{uuid4().hex}_video_frame.jpg"
    temppath = os.path.join(tempdir, filename)

    cv2.imwrite(temppath, image)

    return Path(temppath)


def check_file_size(path: Union[Path, str], format: str = "bytes") -> float:
    path = Path(path) if isinstance(path, str) else path
    if not path.exists() or not path.is_file():
        raise MediaException("The given path is not a valid path or is not a file.", path)

    size = float(os.path.getsize(path))
    if format.lower() == "kb":
        size /= 1000
    elif format.lower() == "mb":
        size /= 10e6
    elif format.lower() == "gb":
        size /= 10e9

    return size
