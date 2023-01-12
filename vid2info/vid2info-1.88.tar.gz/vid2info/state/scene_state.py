"""
This class implements the state of a concrete frame.

Author: Eric Canas.
Github: https://github.com/Eric-Canas
Email: eric@ericcanas.com
Date: 17-07-2022
"""

from time import time
import numpy as np

from vid2info.utils.general import crop_segmentation_mask
from vid2info.inference.utils import crop_bbox_from_image
from vid2info.inference.config import BBOX_XYXY, CLASS_NAME, CLASS_ID
from vid2info.state.element_state import ElementState

from warnings import warn

crop_img_if_given = lambda img, bbox, copy = True: crop_bbox_from_image(image=img, bbox_xyxy=bbox, is_normalized=True, copy=copy) \
                                        if img is not None else None

class SceneState:
    def __init__(self, tracker_out : dict, buffer, get_first_element_time_stamp: callable = lambda track_id : None,
                 frame: np.ndarray | None = None, segmentation_mask : dict | None = None,
                 save_full_segmentation_mask : bool = False, element_state_class : callable = ElementState,
                 element_state_machine_configs : dict | None = None):
        """
        Initialize the SceneState. It is used for defining the current scene, and will contain the
        state of each individual element in the scene.

        :param tracker_out: dictionary. The output of the tracker. It is the dictionary outputted by
                get_track_ids when return_as_dict is True. It's keys are the track_ids and the values are
                dictionaries with, at least, the following keys: ('bbox_xyxy', 'confidence', 'class_id', 'track_length')
        :param buffer: StateBuffer. The StateBuffer containing the N previous SceneStates.
        :param get_first_element_time_stamp: callable. A function that returns the first_timestamp of the first
                detection of the element with the given track_id in the buffer or the current timestamp if the
                element is not in the buffer.
        :param frame: np.ndarray or None. The frame of the scene. If given, it will save a cropped subimage for
                each detected element.
        :param segmentation_mask: dict or None. The segmentation mask of the scene, embedded within a dictionary
                with the following keys: ('segmentation_mask', 'background_class_idx', 'class_names_list'). If given,
                it will save a cropped subimage for each detected element.

        :param save_full_segmentation_mask: bool. If True, it will save the full segmentation mask of the scene.
        """

        self.elements = {}
        recover_tracks = buffer.track_recoverer is not None
        if recover_tracks:
            buffer.track_recoverer.sanity_check(tracker_out=tracker_out)
        mutated_track_ids = {}
        track_id_has_collision = False
        for original_track_id, element in tracker_out.items():
            if recover_tracks:
                track_id = buffer.track_recoverer.recovered_tracks_correspondences.get(original_track_id, original_track_id)
                track_id_has_collision = track_id in buffer.track_recoverer.recovered_tracks_correspondences
            else:
                track_id = original_track_id
            element_class_name = element[CLASS_NAME] if CLASS_NAME in element else element[CLASS_ID]
            finite_state_machine, element_segmentation_mask = None, None
            if element_state_machine_configs is not None:
                finite_state_machine = buffer.get_element_state_machine(track_id=track_id, current_class=element_class_name,
                                        bbox_xyxy=element[BBOX_XYXY], recover_default_machines=recover_tracks,
                                                                    in_scene_tracks=tuple(tracker_out.keys()))
                if recover_tracks and not track_id_has_collision:
                    track_id = buffer.track_recoverer.recovered_tracks_correspondences.get(track_id, track_id)
            if segmentation_mask is not None:
                element_segmentation_mask = crop_segmentation_mask(segmentation_mask=segmentation_mask,
                                                                   bbox=element[BBOX_XYXY], copy=not save_full_segmentation_mask)

            element_state = element_state_class(element_tracker_info=element,
                                             first_detection_timestamp=get_first_element_time_stamp(track_id=track_id),
                                             element_buffer=buffer.get_element_buffer(track_id=track_id),
                                             element_img=crop_img_if_given(img=frame, bbox=element[BBOX_XYXY], copy=True),
                                             element_segmentation_mask=element_segmentation_mask,
                                             finite_state_machine=finite_state_machine)
            self.elements[track_id] = element_state

            if original_track_id != track_id:
                mutated_track_ids[original_track_id] = track_id

        for original_track_id, new_track_id in mutated_track_ids.items():
            tracker_out[new_track_id] = tracker_out.pop(original_track_id)

        self.timestamp = time()
        self.segmentation_mask = segmentation_mask if save_full_segmentation_mask else None

    def __len__(self):
        return len(self.elements)

    def get_elements_age_in_seconds(self) -> dict:
        """
        Returns the age of each element in the scene in seconds.

        :return dict. The age of each element in the scene. The keys are the track_ids and
                        the values are the age in seconds.
        """
        return {track_id : self.elements[track_id].age_in_seconds for track_id in self.elements}

    def get_element_counts(self) -> dict:
        """
        Returns the number of elements in the scene for each class.

            Returns:
                dict. The number of elements in the scene for each class. The keys are the class names and
                the values are the number of elements in the scene for that class.
            """
        classes_list = [element.class_name for element in self.elements.values()]
        return {class_name: classes_list.count(class_name) for class_name in set(classes_list)}
