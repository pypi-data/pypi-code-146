"""ImageIO video writer"""
import imageio
from ....logger import drange

def video_write(video: "MPLVideo", path: str, **kwargs):
    """ImageIO video writer"""
    writer = imageio.get_writer(path, fps=video.fps, **kwargs)
    N = len(video)

    for i in drange(N, desc="[ImageIO::video_write]"):
        frame = video[i]
        writer.append_data(frame)
    writer.close()
