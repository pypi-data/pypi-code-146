"""
This class implements the ByteTracker. It is used to track the elements detected by
the Yolo Detector.

Author: Eric Canas.
Github: https://github.com/Eric-Canas
Email: eric@ericcanas.com
Date: 13-07-2022
"""

from yolox.tracker.byte_tracker import BYTETracker
import numpy as np

from vid2info.inference.utils import bbox_to_dict
from vid2info.inference.detection.config import NORMALIZE_OUTPUT, DETECTOR_IMAGE_SIZE
from vid2info.inference.tracking.config import TRACKING_TH, TRACKING_MATCH_TH, TRACKING_MAX_BUFFER, \
    TRACK_SCORE, TRACK_LENGTH, BBOXES_RANGE_HW
from vid2info.video.config import DEFAULT_VIDEO_HW, DEFAULT_VIDEO_FRAME_RATE



DEFAULT_DETECTOR_OUTPUT_SIZE = (1., 1.) if NORMALIZE_OUTPUT else \
    (DETECTOR_IMAGE_SIZE if type(DETECTOR_IMAGE_SIZE) in (tuple, list) else (DETECTOR_IMAGE_SIZE, DETECTOR_IMAGE_SIZE))

class Tracker():
    def __init__(self, original_img_hw : tuple | list | np.ndarray = DEFAULT_VIDEO_HW,
                 detector_image_hw = DEFAULT_DETECTOR_OUTPUT_SIZE, track_th : float = TRACKING_TH,
                 match_thresh : float = TRACKING_MATCH_TH, track_buffer : int = TRACKING_MAX_BUFFER,
                 frame_rate : float | int = DEFAULT_VIDEO_FRAME_RATE,
                 class_names : list[str, ...] | tuple[str, ...] | None = None):
        """
        Initialize the Tracker.

        :param original_img_hw: Tuple or list of length 2. The image size of the original video.
        :param detector_image_hw: Tuple or list of length 2. The range of the bounding boxes (Usually,
                it will be the image_size of the detectector input, or (1., 1.) if it is normalized).
        :param track_th: Float. The threshold to consider a track as valid.
        :param match_thresh: Float. The threshold to consider a match between two tracks.
        :param track_buffer: Int. The number of frames to keep the track in the buffer.
        :param frame_rate: Float or Int. The frame rate of the video.
        :param class_names: List of strings. The class names of the objects.
        """
        # Build the cmd args
        inference_args = self.InferenceArgs(track_th=track_th, track_buffer=track_buffer,
                                            match_thresh=match_thresh)
        self.tracker = BYTETracker(inference_args, frame_rate=frame_rate if frame_rate is not None else
                                                    DEFAULT_VIDEO_FRAME_RATE)
        self.original_img_hw = original_img_hw
        self.detector_image_hw = detector_image_hw
        self.track_buffer_length = track_buffer
        self.class_names = class_names

    def get_track_ids(self, detections: np.ndarray,
                      class_ids_to_detect: list[int, ...] | np.ndarray | tuple[int, ...] | None = None,
                      return_as_dict: bool = True) -> dict:
        """
        Get the track ids from the detections. These detections are expected to be in the range bbox_image_hw.

        Args:
            detections: np.ndarray of shape (N, 5|6) where N is the number of detections. The first 4 columns are the
                bounding box coordinates. The 5th column is the confidence of the detection. The 6th column, if given,
                is the class of the detection.
            class_ids_to_detect: List or np.ndarray of integers, with length N or None. The classes to track. If provided,
                all the detections with a class not in this list will be discarded.
            return_as_dict: bool. If True, return the track ids dictionary with the input detections as values.
                If False, return these values formatted as a dictionary.

        Returns:
            A dictionary where keys are the track ids and values are the corresponding detections. If return_as_dict is
            False, the detections are outputted as given. If return_as_dict is True, the detections are formatted as
            a dictionary. The dictionary keys are:
                - xmin: Integer. The x coordinate of the top left corner.
                - ymin: Integer. The y coordinate of the top left corner.
                - xmax: Integer. The x coordinate of the bottom right corner.
                - ymax: Integer. The y coordinate of the bottom right corner.
                - bbox_xyxy: Tuple. The bounding box in the format (x1, y1, x2, y2).
                - confidence: Float. The confidence of the bounding box.
                - class_id: Integer. The class id.
                - class_name: String. The class name.
                - track_id: Integer. The track id.
                - track_score: Float. The track score.
                - track_length: Integer. The track length.
        """
        # Copy the detections because the tracker will modify them in place
        tracker_detections = detections.copy()
        if class_ids_to_detect:
            assert type(class_ids_to_detect) in (list, np.ndarray,
                                                 tuple), f'classes_to_detect must be a list, np.ndarray, tuple, or None. Got {type(class_ids_to_detect)}.'
            assert tracker_detections.shape[
                       1] == 6, f'Expected detections to have 6 columns [x1, y1, x2, y2, conf, class], got {detections.shape[1]}.'
            tracker_detections[..., 5] = np.isin(tracker_detections[..., 5], class_ids_to_detect)
        else:
            if tracker_detections.shape[1] == 6:
                tracker_detections = tracker_detections[..., :5]
            elif tracker_detections.shape[1] != 5:
                raise ValueError(
                    f'Expected detections to have 5 or columns [x1, y1, x2, y2, conf [, class]], got {detections.shape[1]}.')

        targets = self.tracker.update(tracker_detections, img_info=self.original_img_hw, img_size=self.detector_image_hw)
        # For each target, find the corresponding original detection
        track_ids = {}
        for target in targets:
            track_id = target.track_id
            # Get the closest detection to the target (L1 Distance)
            det_arg = np.argmin(np.sum(np.abs(tracker_detections[..., :4] - target.tlbr), axis=1))
            bbox = detections[det_arg]
            if return_as_dict:
                tracker_args = {BBOXES_RANGE_HW: self.detector_image_hw, TRACK_SCORE: float(target.score),
                                TRACK_LENGTH: target.tracklet_len}
                bbox = bbox_to_dict(bbox=bbox, class_names=self.class_names, **tracker_args)
            track_ids[track_id] = bbox
        return track_ids

    def set_frame_rate(self, new_frame_rate: float | int):
        """
        Set the frame rate of the video.

        :param new_frame_rate: Float or Int. The new frame rate.
        """
        self.tracker.get_buffer_size_from_frame_rate(frame_rate=new_frame_rate)

    class InferenceArgs():
        def __init__(self, track_th=0.3, track_buffer=30, match_thresh=0.5):
            """
            Arguments for the inference.

            :param track_th: Float. The threshold for the tracker.
            """
            self.track_thresh = track_th
            self.track_buffer = track_buffer
            self.match_thresh = match_thresh
            self.mot20 = False
