"""
This class implements the Pipeline of the inference. It will use a raw frame of the video as input,
and will output a State object, with the current situation.

Author: Eric Canas.
Github: https://github.com/Eric-Canas
Email: eric@ericcanas.com
Date: 16-07-2022
"""
from threading import Thread

from vid2info.state.finite_state_machine.track_recoverer import TrackRecoverer
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
from time import time, sleep
from vid2info.inference.pipeline import Pipeline
FRAME_RATE_BUFFER_SIZE = 32 # Frames

class PipelineBackground(Pipeline):
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
        Wrapper class for the inference pipeline that allows to run the pipeline in a separated thread. In this class,
        process_frame will not return the current scene state, but the last processed one.

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
        super().__init__(detector_model_path=detector_model_path, video_frame_rate=video_frame_rate,
                         original_img_hw=original_img_hw,
                         detector_dataset_yml=detector_dataset_yml, max_detections_per_img=max_detections_per_img,
                         detector_confidence_th=detector_confidence_th, nms_th=nms_th, agnostic_nms=agnostic_nms,
                         use_only_high_confidence_detection=use_only_high_confidence_detection,
                         track_th=track_th, match_thresh=match_thresh, track_buffer=track_buffer,
                         segmenter_model_path=segmenter_model_path, segmenter_params_path=segmenter_params_path,
                         segmenter_model_name=segmenter_model_name,
                         element_state_class=element_state_class, scene_state_class=scene_state_class,
                         finite_state_machine_config=finite_state_machine_config,
                         merge_batch_detections=merge_batch_detections,
                         save_images_in_scene_state=save_images_in_scene_state,
                         tracker_recoverer=tracker_recoverer,
                         inference_device=inference_device, half_mode=half_mode)

        self._last_frame = None
        self._last_scene_state = self.state_buffer.state_from_tracker_out(tracker_out={}, add_to_buffer=False)
        self._started = False

        self.stopped = False

    def process_frame(self, frame: np.ndarray, is_bgr : bool = False) -> SceneState:
        """
        Wrapper for the process_frame method of the InferencePipeline. It will not return the current scene state,
        but the last processed one. Return will occur inmediately, and the scene state will be updated in a separated
        thread.

        :param frame: np.ndarray. Raw frame to process. In the format (H, W, C). With three channels
                (BGR or RGB).
        :param is_bgr: bool. If True, the frame is in BGR format. If False, it is in RGB format.

        :return: The SceneState of the given frame. It will contain each one of the element detections
                 together with its track.
        """
        self._last_frame = frame
        if not self._started:
            self._started = True
            self._start()

        return self._last_scene_state

    def process_last_frame(self):
        """
        Process the last frame that was passed to the process_frame method. It will update the scene state
        with the new information.
        """
        assert self._last_frame is not None, "No frame has been passed to the process_frame method."
        self._last_scene_state = super().process_frame(self._last_frame)

    def _start(self):
        """
        Start the thread that will update the scene state.
        """
        self.stopped = False
        self._thread = Thread(target=self._update_scene_state)
        self._thread.start()

    def _update_scene_state(self):
        """
        Thread that will update the scene state.
        """
        while not self.stopped:
            self.process_last_frame()
            sleep(0.001)

    def stop(self):
        """
        Stop the thread that updates the scene state.
        """
        self.stopped = True
        self._thread.join()

    def __del__(self):
        self.stop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
