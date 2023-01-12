"""
This class implements a buffer containing a set of states. It will serve as interface with the
individual states.

Author: Eric Canas.
Github: https://github.com/Eric-Canas
Email: eric@ericcanas.com
Date: 16-07-2022
"""

from collections import deque

import numpy as np
from loguru import logger
from vid2info.state.finite_state_machine.track_recoverer import TrackRecoverer
from vid2info.utils.config import TIME_FORMAT, ELEMENT_AGE_TIME_FORMAT
from vid2info.utils.general import time_as_str
from vid2info.state.config import ELEMENT_BUFFER_SIZE, INITIAL_TIMESTAMP, OUT_TIMESTAMP, INITIAL_CLASS_NAME, \
    OUT_CLASS_NAME, FINITE_STATE_MACHINE, TRACK_LENGTH, INITIAL_BBOX_XYXY, OUT_BBOX_XYXY
from vid2info.state.finite_state_machine.config_keys import TIMESTAMP, PREVIOUS_STATE, NEW_STATE
from vid2info.state.finite_state_machine.element_finite_state_machine import ElementFiniteStateMachine
from vid2info.state.config import BUFFER_SIZE
from vid2info.state.scene_state import SceneState
from vid2info.state.element_state import ElementState
from time import time


class StateBuffer:
    def __init__(self, buffer_size : int = BUFFER_SIZE, running_online : bool = False,
                 scene_state_class : callable = SceneState, element_state_class : callable = ElementState,
                 finite_state_machines_config: dict | None = None, keep_elements_history: bool = False,
                 track_recoverer: TrackRecoverer | None = None):
        """
        Initialize the StateBuffer. It is used for tracking the history of the last scene and
         element states.

        :param buffer_size: int. The size of the history buffer to keep.
        :param running_online: bool. If True, it will assume that the video is comming from an online stream
                like a webcam. So the timestamps of the states will update with the current time in every call.
                If False, it will assume that the video is coming from a pre-recorded file. So the timestamps
                will have to be served from the video.
        :param scene_state_class: type. The class of the scene state. It should be a subclass of SceneState.
        :param element_state_class: Class. The class of the element states. It should be a subclass of ElementState.
        :param finite_state_machines_config: dict. The configuration of the finite state machines for the elements.
                It is a dictionary with the track_id as key and the configuration as value.
        :param keep_elements_history: bool. If True, the element states will be kept in the buffer. If False, the
                element states will be removed from the buffer when they are not in the scene anymore.
        :param recover_tracks_for_static_elements: bool. Only used when finite_state_machines_config is passed.
                If True, it will try to recover the tracks for the elements with a class that fallbacks in a default
                state machine. NOTE: It should ONLY be used when we are expecting very STATIC elements that do not tend
                to overlap with each other. Otherwise, it could produce unexpected results. The expected scenario for
                this flag is when we do expect static elements, that can be partially lost by occlusions, and that have
                an attached state machine that makes transitions based in the object class but that only accept a few
                 entry classes but the classes. For example: A lot of robotic faces that always starts with the class
                 "neutral expression" and for which we are registering the expression transitions.
        :param recover_track_attempts: int. Only used when finite_state_machines_config is passed and
                recover_tracks_for_static_elements is True. The number of attempts to recover the track of the elements
                that fallback in a default state machine.
        """
        self.buffer_size = max(buffer_size, 1)
        self.buffer = deque(maxlen=self.buffer_size)
        self.running_online = running_online
        self.scene_state_class = scene_state_class
        self.element_state_class = element_state_class
        self.finite_state_machines_config = finite_state_machines_config
        self.keep_elements_history = keep_elements_history
        self.elements_history = {}

        self.track_recoverer = track_recoverer
        if self.track_recoverer is not None:
            self.track_recoverer.state_buffer = self

        self.recovered_tracks_correspondences = {}

    def state_from_tracker_out(self, tracker_out : dict, add_to_buffer : bool = True,
                               frame: np.ndarray | None = None,
                               segmentation_mask : dict | None = None) -> SceneState:
        """
        Create a new state from the tracker output.

        :param tracker_out: dictionary. The output of the tracker. It is the dictionary outputted by
                get_track_ids when return_as_dict is True. It's keys are the track_ids and the values are
                dictionaries with, at least, the following keys: ('bbox_xyxy', 'confidence', 'class_id', 'track_length')
        :param add_to_buffer: bool. If True, the state will be added to the buffer.
        :param frame: np.ndarray or None. The frame of the scene. If given, it will save a cropped subimage for
                each detected element.
        :param segmentation_mask: np.ndarray or None. The segmentation mask of the scene. If given, it will save a
                cropped segmentation mask for each detected element.
        :return: SceneState. The new state. If add_to_buffer was True it can be also found in the last element of the
                current self.buffer.
        """
        scene_state = self.scene_state_class(tracker_out=tracker_out, buffer=self,
                                             get_first_element_time_stamp=self.get_first_element_time_stamp,
                                             frame=frame, segmentation_mask=segmentation_mask,
                                             element_state_class=self.element_state_class,
                                             element_state_machine_configs=self.finite_state_machines_config)
        if add_to_buffer:
            self.buffer.append(scene_state)
            if self.keep_elements_history:
                self.update_history(scene_state)
        return scene_state


    def get_first_element_time_stamp(self, track_id : int) -> float | None:
        """
        Get the first_timestamp of the first detection of the element with the given track_id in the buffer
        or current_time if the element is not in the buffer, and it is running online (webcam).
        If the element is not in the buffer and is not running online, it will return None.

        :param track_id: int. The track_id of the element to get the first_timestamp of.

        :return: float or None. The first_timestamp of the first detection of the element with the given track_id
                in the buffer or current_time if the element is not in the buffer, and it is running online (webcam).
                If the element is not in the buffer and is not running online, it will return None.
        """
        for scene_state in self.buffer:
            if track_id in scene_state.elements:
                track_id = self.recovered_tracks_correspondences.get(track_id, track_id)
                return scene_state.elements[track_id].first_detection_timestamp
        if self.running_online:
            return time()
        else:
            raise NotImplementedError("Not implemented yet for the case where the video is not coming from an online stream.")


    def get_last_detection_of_element(self, track_id: int) -> ElementState | None:
        """
        Get the last detection of the element with the given track_id in the buffer or None if
        the element is not in the buffer.

        :param track_id: int. The track_id of the element to get the last detection of.

        :return: ElementState or None. The last detection of the element with the given track_id in the buffer or None if
                the element is not in the buffer.
        """
        for scene_state in reversed(self.buffer):
            if track_id in scene_state.elements:
                return scene_state.elements[track_id]
        return None

    def get_element_buffer(self, track_id: int, buffer_size: int = ELEMENT_BUFFER_SIZE) -> deque:
        """
        Returns a buffer with the last buffer_size elements with the given track_id in the scene_buffer. If the track_id
        disappears in the scene_buffer for some in between frames, these frames will be ignored. So the buffer will be
        not representative of the distance between frames.

        :param track_id: int. The track_id of the element we want to get the buffer for.
        :param buffer_size: int. The maximum size of the expected buffer.

        :return deque. A buffer containing the last buffer_size elements with the given track_id in the scene_buffer.
        """
        element_buffer = deque(maxlen=buffer_size)
        # Read the scene_buffer backwards
        for scene_state in reversed(self.buffer):
            if track_id in scene_state.elements:
                element_buffer.append(scene_state.elements[track_id])
            if len(element_buffer) == buffer_size:
                break
        element_buffer = deque(reversed(element_buffer))
        return element_buffer

    def get_element_state_machine(self, track_id: int, current_class: str | None = None, bbox_xyxy: np.ndarray | None = None,
                                  recover_default_machines: bool = False, in_scene_tracks: tuple | list = ()) -> ElementFiniteStateMachine:
        """
        Returns the state machine of the element with the given track_id. If this element is new,
        it will create a new state machine using the configs given in element_state_machine_configs.

        :param track_id: int. The track_id of the element.
        :param current_class : str | None. The current class of the element, only used if the element is new.
        :param bbox_xyxy: np.ndarray | None. The bounding box of the element, only used if the element is new.
        :param recover_default_machines: bool. If True, the default state machines will be recovered if the element is new.
        :param in_scene_tracks: tuple | list. The tracks of the elements that are actually in the scene. Only used if
                recover_default_machines is True.

        :return ElementFiniteStateMachine. The current state machine of the element.
        """
        # Check for the last aparition of the element in the buffer.
        finite_state_machine = None
        last_detection = self.get_last_detection_of_element(track_id=track_id)
        if last_detection is not None:
            finite_state_machine = last_detection.finite_state_machine
        if finite_state_machine is None:
            if self.track_recoverer is not None:
                # It will try to find the old track_id for the element. Filling its correspondences buffer (lately used
                # by the SceneState) if it is able to find one. Otherwise, it will return None or create a new one.
                finite_state_machine = self.track_recoverer.recover_track_id_from_state_machine(
                    last_detection=last_detection, track_id=track_id, current_class=current_class, bbox_xyxy=bbox_xyxy,
                    recover_default_machines=True)
            else:
                if current_class not in self.finite_state_machines_config:
                    assert 'default' in self.finite_state_machines_config, f"Element class {current_class} not found " \
                                                                           f"in finite state machine configs and no default " \
                                                                           f"config found."
                    current_class = 'default'
                config = self.finite_state_machines_config[current_class]
                finite_state_machine = ElementFiniteStateMachine(config=config)
        return finite_state_machine


    def update_history(self, state : SceneState):
        """
        Update the elements_history dictionary. It will keep the track of all the elements that have been
        seen during the analysis.
        """
        for track_id, element in state.elements.items():
            if self.track_recoverer is not None and \
                    self.track_recoverer.track_id_is_being_recovered(track_id=track_id, state_machine=element.finite_state_machine):
                # This way, the track_id won't be added to the history if it is being recovered.
                continue
            if track_id not in self.elements_history:
                initial_hist_state = {
                    INITIAL_TIMESTAMP: element.first_detection_timestamp,
                    INITIAL_CLASS_NAME: element.class_name,
                    FINITE_STATE_MACHINE: element.finite_state_machine,
                    INITIAL_BBOX_XYXY: element.bbox_xyxy,
                }
                self.elements_history[track_id] = initial_hist_state

            element_hist_update = {
                OUT_TIMESTAMP: element.timestamp,
                OUT_CLASS_NAME: element.class_name,
                OUT_BBOX_XYXY: element.bbox_xyxy,
                TRACK_LENGTH: element.track_length
            }
            self.elements_history[track_id].update(element_hist_update)

    def print_elements_history(self, min_track_length: int = 0):
        """
        Print the elements_history dictionary.

        :param min_track_length: int. The minimum track length to print it.
        """
        assert self.keep_elements_history, "The elements_history dictionary is not kept. Impossible to print it."

        for track_id, element in self.elements_history.items():
            track_len = element[TRACK_LENGTH]
            if track_len > min_track_length:
                start, end = element[INITIAL_TIMESTAMP], element[OUT_TIMESTAMP]
                print("Track id: ", track_id)
                print(f"\t From: {time_as_str(start, time_format=TIME_FORMAT)} - To: {time_as_str(end, time_format=TIME_FORMAT)} "
                      f"(Age: {time_as_str(end - start, time_format=ELEMENT_AGE_TIME_FORMAT)})")
                print(f"\t Entered as: {element[INITIAL_CLASS_NAME]} - Left as: {element[OUT_CLASS_NAME]}")
                print(f"\t Track length: {track_len}")
                print("\t Last known bbox: ", tuple(round(coord, ndigits=2) for coord in element[OUT_BBOX_XYXY]))
                print(f"\t Finite state machine: \n{element[FINITE_STATE_MACHINE]}")

    def get_elements_time_per_state(self, class_to_state_dict: dict = {})-> dict[int, dict[str, float]]:
        """
        Returns a dictionary with the time spent in each state for each element.

        :return dict[int, dict[str, float]]. A dictionary with the time spent in each state for each element.
        """
        assert self.keep_elements_history, "The elements_history dictionary is not kept. Impossible to print it."
        elements_time_per_state = {}
        for track_id, element in self.elements_history.items():
            element_info = {}
            initial_timestamp, history = element[INITIAL_TIMESTAMP], element[FINITE_STATE_MACHINE].history
            initial_class = class_to_state_dict.get(element[INITIAL_CLASS_NAME], element[INITIAL_CLASS_NAME])
            if len(history) == 0:
                out_class_name = class_to_state_dict.get(element[OUT_CLASS_NAME], element[OUT_CLASS_NAME])
                if out_class_name != initial_class:
                    logger.warning(f"Element {track_id} has no history. That's a missing track.")
                initial_time = element[OUT_TIMESTAMP] - initial_timestamp
                element_info[element[INITIAL_CLASS_NAME]] = initial_time
            else:
                previous_timestamp = initial_timestamp
                assert history[0][PREVIOUS_STATE] == initial_class, "The first state of the element is not the initial class."
                for entry in history:
                    change_timestamp, lapse_state = entry[TIMESTAMP], entry[PREVIOUS_STATE]
                    element_info[lapse_state] = change_timestamp - previous_timestamp
                    previous_timestamp = change_timestamp
                lapse_state = class_to_state_dict.get(element[OUT_CLASS_NAME], element[OUT_CLASS_NAME])
                if history[-1][NEW_STATE] != lapse_state:
                    logger.warning(f"The last state of the element is not the final class. Probably the track_id {track_id} has been lost")
                    continue
                element_info[lapse_state] = element[OUT_TIMESTAMP] - previous_timestamp
            elements_time_per_state[track_id] = element_info

        return elements_time_per_state
