"""
This class implements the Pipeline of the inference. It will use a raw frame of the video as input,
and will output a State object, with the current situation.

Author: Eric Canas.
Github: https://github.com/Eric-Canas
Email: eric@ericcanas.com
Date: 16-07-2022
"""
from vid2info.state.finite_state_machine.track_recoverer import TrackRecoverer
from vid2info.inference.detection.yolov7_detector import YoloV7Detector
from vid2info.inference.detection.yolov6_detector import YoloV6Detector
from vid2info.inference.tracking.tracker import Tracker
from vid2info.inference.segmentation.pidnet_segmenter import PidNetSegmenter

from vid2info.state.state_buffer import StateBuffer
from vid2info.state.scene_state import SceneState
from vid2info.state.element_state import ElementState

from vid2info.inference.detection.config import WEIGTHS_PATH, DETECTOR_MIN_CONFIDENCE_TH, IOU_NMS_TH, \
    MAX_DETECTIONS_PER_IMAGE, HALF_MODE, DATASET_YML, NORMALIZE_OUTPUT
from vid2info.inference.segmentation.config import PARAMS_YAML as SEGMENTER_PARAMS_YML,\
    MODEL_NAME as SEGMENTER_MODEL_NAME, WEIGTHS_PATH as SEGMENTER_WEIGTHS_PATH
from vid2info.inference.tracking.config import TRACKING_TH, TRACKING_MATCH_TH, TRACKING_MAX_BUFFER
from vid2info.inference.config import INFERENCE_DEVICE

from vid2info.video.config import DEFAULT_VIDEO_HW, DEFAULT_VIDEO_FRAME_RATE

import numpy as np
from collections import deque
from time import time

FRAME_RATE_BUFFER_SIZE = 32 # Frames

class Pipeline:
    def __init__(self, detector_model_path: str = WEIGTHS_PATH, video_frame_rate: int | None = DEFAULT_VIDEO_FRAME_RATE,
                 original_img_hw : tuple | list | np.ndarray = DEFAULT_VIDEO_HW,
                 use_only_high_confidence_detection : bool = False,

                 detector_dataset_yml : str | None = DATASET_YML, max_detections_per_img : int = MAX_DETECTIONS_PER_IMAGE,
                 detector_confidence_th : float = DETECTOR_MIN_CONFIDENCE_TH, nms_th : float = IOU_NMS_TH,
                 agnostic_nms: bool = False,

                 track_th : float = TRACKING_TH, match_thresh : float = TRACKING_MATCH_TH,
                 track_buffer : int = TRACKING_MAX_BUFFER,

                 segmenter_model_path: str | None = SEGMENTER_WEIGTHS_PATH,
                 segmenter_params_path: str = SEGMENTER_PARAMS_YML, segmenter_model_name : str = SEGMENTER_MODEL_NAME,

                 element_state_class: type = ElementState, scene_state_class : type = SceneState,
                 finite_state_machine_config: dict | None = None, merge_batch_detections: bool = False,
                 save_images_in_scene_state: bool = True,
                 tracker_recoverer: TrackRecoverer | None = None,

                 inference_device : str = INFERENCE_DEVICE, half_mode=HALF_MODE):
        """
        Initialize the Pipeline. It will use a raw frame of the video as input, and will output a State object,
        with the current situation.

        :param detector_model_path: string. Path to the weights of the detector.
        :param video_frame_rate: int. Frame rate of the video that outputs each frame. It is relevant
                for the tracker. If video is coming from a webcam working on the fly, it should be None.
                In this case the pipeline will track the empirical frame rate at which we are calling it,
                and will keepit synchronized.
        :param original_img_hw: tuple. The original size of the image that is going to be processed. It is,
                the size of the original_video that we are processing.

        :param detector_dataset_yml: string. Path to the dataset yml file of the detector. It will be used to
                load the labels of the classes.
        :param max_detections_per_img: int. Maximum number of detections per image.
        :param detector_confidence_th: float. Minimum confidence threshold for the detector.
        :param nms_th: float. IOU threshold for the non-max suppression of the detector.
        :param agnostic_nms: bool. If True, the detector will not use the class id when performing the nms.
        :param use_only_high_confidence_detection: bool. If True, only high confidence detections will be used as
        input to the tracker. Otherwise, all the tracker will receive all the detections above the detector
        confidence threshold, together with all the detections below the tracker confidence threshold.

        :param track_th: Float. The threshold to consider a track as valid.
        :param match_thresh: Float. The threshold to consider a match between two tracks.
        :param track_buffer: Int. The number of frames to keep the track in the buffer.

        :param segmenter_model_path: string or None. Path to the weights of the segmenter. If None,
                the segmenter will not be used.
        :param segmenter_params_path: string. Path to the yml file with the segmenter params. If segmenter_model_path
                is None, this parameter will be ignored.
        :param segmenter_model_name: string. Name of the segmenter model (must end with 'small', 'medium' or 'large').
                If segmenter_model_path is None, this parameter will be ignored.

        :param element_state_class: type. The class to use for the element state. It should inherit from
                                vid2info.state.element_state.ElementState. This class will be used for implementing all
                                the Bronze Specific State management logic.
        :param scene_state_class: type. The class to use for the scene state. It should inherit from
                                vid2info.state.scene_state.SceneState. This class will be used for implementing all
                                the Bronze Specific State management logic (with the information of all the Elements
                                in the scene).
        :param save_images_in_scene_state: bool. If True, a cropped image of the detected element will be saved
                                                in the scene state.
        :param finite_state_machine_config: dict. Configuration of the finite state machine.
        :param merge_batch_detections: Boolean. Whether to merge batches or not. If it is True, and the input is a batch
                                of images, predictions will be merged as if they came from a single image. It is only
                                recommended for very static scenes.

        :param recover_tracks_for_static_elements: bool. Only used when finite_state_machines_config is passed.
                If True, it will try to recover the tracks for the elements with a class that fallbacks in a default
                state machine. NOTE: It should ONLY be used when we are expecting very STATIC elements that do not tend
                to overlap with each other. Otherwise, it could produce unexpected results. The expected scenario for
                this flag is when we do expect static elements, that can be partially lost by occlusions, and that have
                an attached state machine that makes transitions based in the object class but that only accept a few
                 entry classes but the classes. For example: A lot of robotic faces that always starts with the class
                 "neutral expression" and for which we are registering the expression transitions.

        :param inference_device: string. Device to use for the inference. It can be 'cpu' or 'cuda'.
        :param half_mode: bool. If True, the models will be loaded in half precision. Only valid when inference_device
                is 'cuda'.
        """

        if 'yolov6' in detector_model_path:
            detector_class = YoloV6Detector
        elif 'yolov7' in detector_model_path:
            detector_class = YoloV7Detector
        else:
            raise ValueError(f"Unknown detector model: {detector_model_path}. FileName must contain 'yolov6' or 'yolov7'")

        self.detector = detector_class(weights=detector_model_path, dataset_yml=detector_dataset_yml,
                                       confidence_th=detector_confidence_th, nms_th=nms_th,
                                       max_dets=max_detections_per_img,
                                       inference_device=inference_device, half_mode=half_mode,
                                       merge_batches=merge_batch_detections, agnostic_nms=agnostic_nms)

        self.use_only_high_confidence_detection = use_only_high_confidence_detection

        self.segmenter = PidNetSegmenter(weights=segmenter_model_path, params_yml=segmenter_params_path,
                                         model_name=segmenter_model_name, inference_device=inference_device)\
                                            if segmenter_model_path is not None else None
        # Set all the structures for keeping the frame_rate updated in case it is being read online
        running_online = video_frame_rate is None
        self.update_video_frame_rate = running_online
        self.video_frame_rate = video_frame_rate if self.update_video_frame_rate else DEFAULT_VIDEO_FRAME_RATE
        self.video_frame_rate_track = deque(maxlen=FRAME_RATE_BUFFER_SIZE) if self.update_video_frame_rate else None

        self.track_th = track_th
        self.tracker = Tracker(original_img_hw=original_img_hw, frame_rate=self.video_frame_rate,
                               track_th=track_th, match_thresh=match_thresh, track_buffer=track_buffer,
                               class_names=self.detector.class_names)

        self.save_images_in_scene_state = save_images_in_scene_state
        self.state_buffer = StateBuffer(buffer_size=self.tracker.track_buffer_length, running_online=running_online,
                                        element_state_class=element_state_class, scene_state_class=scene_state_class,
                                        finite_state_machines_config=finite_state_machine_config,
                                        track_recoverer=tracker_recoverer,
                                        keep_elements_history=finite_state_machine_config is not None)
        

    def process_frame(self, frame: np.ndarray, is_bgr : bool = False) -> SceneState:
        """
        Process a frame and return its SceneState.

        NOTE: Take into account that it will automatically state buffer. So, to keep it consistent,
            you should always call this function with consecutive frames.

        :param frame: np.ndarray. Raw frame to process. In the format (H, W, C). With three channels
                (BGR or RGB).
        :param is_bgr: bool. If True, the frame is in BGR format. If False, it is in RGB format.

        :return: The SceneState of the given frame. It will contain each one of the element detections
                 together with its track.
        """
        # Update the frame rate if it is being read online
        if self.update_video_frame_rate:
            self.video_frame_rate_track.append(time())
            frame_time_diffs = np.diff(self.video_frame_rate_track)
            if len(frame_time_diffs) > 1:
                self.video_frame_rate = 1 / np.mean(frame_time_diffs)
                self.tracker.set_frame_rate(new_frame_rate = self.video_frame_rate)

        detector_below_th = self.track_th if not self.use_only_high_confidence_detection else 0.
        # Detect the objects in the frame
        detections = self.detector.detect(image=frame, input_is_bgr=is_bgr, return_all_below_th=detector_below_th,)
        if frame.ndim == 4:
            frame = frame[frame.shape[0]//2]
        # Segment the objects in the frame
        segmentations = self.segmenter.segment(image=frame, is_bgr=is_bgr, return_as_dict=True)\
                                        if self.segmenter is not None else None
        # Get the track of the objects
        tracks = self.tracker.get_track_ids(detections=detections, return_as_dict=True)
        # Update the state buffer
        scene_state = self.state_buffer.state_from_tracker_out(tracker_out=tracks, add_to_buffer=True,
                                                               frame=frame if self.save_images_in_scene_state else None,
                                                               segmentation_mask=segmentations)

        return scene_state


