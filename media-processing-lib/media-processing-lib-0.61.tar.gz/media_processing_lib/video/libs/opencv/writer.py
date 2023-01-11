"""OpenCV video writer"""
import cv2
from ....logger import drange

def video_write(video: "MPLVideo", path: str, **kwargs):
    """OpenCV video writer"""
    width, height = video.shape[2], video.shape[1]
    fourcc = kwargs["fourcc"] if "fourcc" in kwargs else "mp4v"
    writer = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*fourcc), video.fps, (width, height))

    N = len(video)
    for i in drange(N, desc="[OpenCV::video_write]"):
        frame = video[i]
        frame = frame[..., ::-1]
        writer.write(frame)
