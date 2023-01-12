"""
The WebcamReader class is a wrapper for the cv2.VideoCapture class. It is used to read frames from a webcam.

Author: Eric Canas
Github: https://github.com/Eric-Canas
Email: eric@ericcanas.com
Date: 09-07-2022
"""

import cv2
import numpy as np
from warnings import warn
import time

from vid2info.video.config import DEFAULT_VIDEO_FRAME_RATE

from vid2info.video.utils import calculate_frame_size_keeping_aspect_ratio
from vid2info.video._webcam_reader_multithread import _WebcamReaderMultithread


class WebcamReader:
    def __init__(self, as_rgb: bool = False, h: int | None = None, w: int|None = None,
                 batch_size : int | None = None, run_in_background : bool = True,
                 max_frame_rate: int | None = DEFAULT_VIDEO_FRAME_RATE):
        """
        Initialize the WebcamReaader.

        It must be between 0 and the video real frame rate.
        :param as_rgb: If True, the frames will be returned as RGB instead of BGR.
        :param h: int or None. Height to resize the frames to. If None, the original height will be used, except if
                w is provided, in which case it will resize to keep the original aspect ratio.
        :param w: int or None. Width to resize the frames to. If None, the original width will be used, except if
                h is provided, in which case it will resize to keep the original aspect ratio.
        :param batch_size: int or None. If not None, the iterator will yield batches of frames (B, H, W, C), if
                None, the iterator will yield the frames as they are (H, W, C).
        :param run_in_background: If True, the frames will be read in a background thread (speeding up the reading).
        :param max_frame_rate: int or None. The maximum frame rate to read the frames at.
                                            If None, the maximum frame rate will be used.
        """
        self.run_in_background = run_in_background
        self.cap = _WebcamReaderMultithread(src=0).start() if run_in_background else cv2.VideoCapture(0)
        self.frame_size_hw = (int(self.cap.get(propId=cv2.CAP_PROP_FRAME_HEIGHT)), int(self.cap.get(propId=cv2.CAP_PROP_FRAME_WIDTH)))

        self.as_rgb = as_rgb

        if h is not None or w is not None:
            # If one is None, calculate the other
            if sum(1 for x in (h, w) if x is None) == 1:
                h, w = self.calculate_frame_size_keeping_aspect_ratio(h=h, w=w)
            elif np.isclose(h/w, self.frame_size_hw[0]/self.frame_size_hw[1]):
                warn(f'Video_Reader have been set to resize videos to {h}x{w}, the original video aspect ratio '
                     f'will be lost {self.frame_size_hw[0]}x{self.frame_size_hw[1]}.', UserWarning)
            self.output_hw = (h, w)
        else:
            self.output_hw = self.frame_size_hw
        self.batch_size = batch_size

        self.start_timestamp = time.time()
        self.max_frame_rate = max_frame_rate
        self.last_frame_timestamp = self.start_timestamp

    @property
    def current_timestamp_seconds(self):
        return time.time() - self.start_timestamp

    def __iter__(self):
        return self

    def __next__(self):
        return self.read_next_frame()

    def __del__(self):
        # Close the video
        if self.run_in_background:
            self.cap.stop()
        self.cap.release()
        self.cap = None

    def read_next_frame(self) -> np.ndarray:
        """
        Read the next frame from the video. (Skipping the frames_offset if it is greater than one.)
        """
        batch_size = 1 if self.batch_size is None else self.batch_size
        frames = []
        for i in range(batch_size):
            ret, frame = self.cap.read()
            if not ret:
                raise StopIteration("The webcam have closed?.")
            if self.as_rgb:
                cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2RGB, dst=frame)
            if self.output_hw != self.frame_size_hw:
                frame = cv2.resize(src=frame, dsize=self.output_hw[::-1])
            frames.append(frame)

        if self.max_frame_rate is not None:
            # Sleep to simulate the frame rate (0.8 is a magic number, just to compensate the execution resuming time)
            time.sleep(max(0, (1/self.max_frame_rate)*0.8 - (time.time() - self.last_frame_timestamp)))
            self.last_frame_timestamp = time.time()

        return frames[0] if self.batch_size is None else np.stack(frames, axis=0)

    def read_video_iterator(self, from_start: bool = False) -> np.ndarray:
        """
        Yields the frames of the video. If simulate_frame_rate is not None,
         the frames are yielded at the given simulated frame rate. That is, skipping real_frame_rate / simulate_frame_rate
         at each iteration.

        :param from_start: If True, the iterator will start from the beginning of the video.

        :return: The next frame in the video.
        """
        # While webcam is open
        while self.cap.isOpened():
            yield self.read_next_frame()
        raise StopIteration


    # --------------- AUXILIARY METHODS ---------------
    def calculate_frame_size_keeping_aspect_ratio(self, h:int | None, w:int|None) -> tuple[int, int]:
        """
        When only one of the frame size dimensions is given, the other one is calculated keeping the
        aspect ratio with the original video.

        :param h: int or None. Height of the frame. If None, w must be provided.
        :param w: int or None. Width of the frame. If None, h must be provided.
        :return: The height and width of the frame.
        """
        frame_h, frame_w = self.frame_size_hw
        return calculate_frame_size_keeping_aspect_ratio(original_h=frame_h, original_w=frame_w, new_h=h, new_w=w)