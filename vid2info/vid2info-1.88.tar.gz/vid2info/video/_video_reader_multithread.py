import os

from imutils.video import FileVideoStream
from queue import Empty
from threading import Thread
from time import sleep

import cv2

class _VideoReaderMultiThread(FileVideoStream):
    def __init__(self, video_path: str, queue_size: int = 8, release_on_finished: bool = True):
        """
        Initialize the VideoReader to work in the background.
        :param video_path: str. Path to the video file.
        :param queue_size: int. Size of the queue used to store the frames.
        """
        super().__init__(path=video_path, queue_size=queue_size)
        # This sleep is needed for not messing up the thread
        sleep(0.1)
        assert os.path.isfile(video_path), f'Video file {video_path} not found.'
        self.video_path = video_path
        self.queue_size = queue_size
        self.release_on_finished = release_on_finished
        self.start()
        # This sleep is also needed for not messing up the thread
        sleep(0.1)
        self.stopped = False

    def read(self, timeout_seconds=1):
        buffer_size = self.Q.qsize()
        if buffer_size == 0 and not self.stopped:
            try:
                frame = self.Q.get(timeout=timeout_seconds)
                return True, frame
            except Empty:
                print("Read timeout. Buffer size: {}".format(buffer_size))
                return False, None
        else:
            grabbed = buffer_size > 0 and not self.stopped
            frame = self.Q.get(timeout=timeout_seconds) if grabbed else None
        return grabbed, frame

    def grab(self, timeout_seconds=1):
        grabbed, _ = self.read(timeout_seconds=timeout_seconds)
        return grabbed

    def stop(self):
        super().stop()
        self.stopped = True

    def get(self, propId):
        return self.stream.get(propId=propId)

    def set(self, propId, value):
        buffer_size = self.Q.qsize()
        self.stream.set(propId=propId, value=value)
        if propId == cv2.CAP_PROP_POS_FRAMES:
            # Empty the queue
            for _ in range(buffer_size):
                self.Q.get_nowait()
            if self.stopped:
                self.stop()
                self.thread = Thread(target=self.update, args=())
                self.stopped = False
                self.start()
            sleep(0.1)

    def update(self):
        """
        Don't release when read is finished
        :return:
        """
        # keep looping infinitely
        while True:
            # if the thread indicator variable is set, stop the
            # thread
            if self.stopped:
                break

            # otherwise, ensure the queue has room in it
            if not self.Q.full():
                # read the next frame from the file
                (grabbed, frame) = self.stream.read()

                if not grabbed:
                    self.stopped = True

                if self.transform:
                    frame = self.transform(frame)

                # add the frame to the queue
                self.Q.put(frame)
            else:
                sleep(0.01)  # Rest for 10ms, we have a full queue
        if self.release_on_finished:
            self.release()

    def release(self):
        self.stream.release()

    def isOpened(self):
        return self.stream.isOpened()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.release()

    def __del__(self):
        self.stop()
        self.release()

    def __iter__(self):
        return self

    def __next__(self):
        return self.read()
