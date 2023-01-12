"""
The track recover is a plugin that aims to recover track_ids that are lost. A track is considered as lost when
a new one have been generated for an element that already had a track_id associated, loosing the old track_id.
NOTE: This plugin only work in a very limited set of cases. It is only expected to work for very static scenes,
where the elements do not move much and don't overlap one another.

Author: Eric Canas.
Github: https://github.com/Eric-Canas
Email: eric@ericcanas.com
Date: 11-09-2022
"""
import numpy as np
from warnings import warn
from time import time

from vid2info.utils.general import iou
from vid2info.state.config import DIFFERENCE_TO_CONSIDER_ELEMENT_LEFT_SCENE_IN_SECONDS, MIN_IOU_TO_CONSIDER_OVERLAP, \
    OUT_CLASS_NAME, OUT_TIMESTAMP, MAX_BBOXES_TO_CHECK_IN_PAST, MAX_FRAMES_TO_CHECK_IN_PAST, MAX_RECOVER_TRACK_ATTEMPTS

from vid2info.inference.config import BBOX_XYXY, CLASS_NAME
from vid2info.state.finite_state_machine.element_finite_state_machine import ElementFiniteStateMachine


class TrackRecoverer:
    def __init__(self, finite_state_machines_config: dict, recover_track_attempts: int = MAX_RECOVER_TRACK_ATTEMPTS,
                 verbose: bool = True):
        self.state_buffer = None # Must be initialized before recovering track_ids.
        self.finite_state_machines_config = finite_state_machines_config
        self.recover_tracks_attempts = {}
        self.recovered_tracks_correspondences = {}
        self.max_recover_track_attempts = recover_track_attempts
        self.verbose = verbose


    def recover_track_id_from_state_machine(self, last_detection, track_id: int, current_class: str | None = None, bbox_xyxy: np.ndarray | None = None,
                                  recover_default_machines: bool = False, in_scene_tracks: tuple | list = ()) -> ElementFiniteStateMachine | None:
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
        assert self.state_buffer is not None, "The state buffer must be initialized before recovering track_ids."
        finite_state_machine = last_detection.finite_state_machine if last_detection is not None else None
        if finite_state_machine is None:
            assert current_class is not None, "If the element is new, the current class must be given."
            if current_class not in self.finite_state_machines_config:
                assert 'default' in self.finite_state_machines_config, f"Element class {current_class} not found " \
                                                                       f"in finite state machine configs and no default " \
                                                                       f"config found."
                if recover_default_machines:
                    recovered_track_id = self.recover_track_id(class_name=current_class, bbox_xyxy=bbox_xyxy,
                                                               in_scene_tracks=in_scene_tracks)
                    if recovered_track_id is not None:
                        self.recovered_tracks_correspondences[track_id] = recovered_track_id
                        if self.verbose:
                            print(f"Recovered track {track_id} with track {recovered_track_id}")
                        return self.state_buffer.get_element_state_machine(track_id=recovered_track_id, current_class=current_class,
                                                               recover_default_machines=False)
                    else:
                        self.recover_tracks_attempts[track_id] = self.recover_tracks_attempts.get(track_id, 0) + 1
                        # We will set this state machine temporally as None, so we can recover it later.
                        if self.recover_tracks_attempts[track_id] < self.max_recover_track_attempts:
                            if self.verbose:
                                print(f"Could not recover track {track_id} after {self.recover_tracks_attempts[track_id]} attempts.")
                            return None
                        elif self.verbose:
                            print(f"Generating default state machine for track {track_id} after {self.recover_tracks_attempts[track_id]} attempts.")

                warn(f"Element class {current_class} not found in finite state machine configs. Using default")
                current_class = 'default'
            config = self.finite_state_machines_config[current_class]
            finite_state_machine = ElementFiniteStateMachine(config=config)
        return finite_state_machine

    def recover_track_id(self, class_name: str, bbox_xyxy: np.ndarray, mismatch_recovery : bool = False,
                         max_difference_in_seconds: float | int = DIFFERENCE_TO_CONSIDER_ELEMENT_LEFT_SCENE_IN_SECONDS,
                         in_scene_tracks : list | tuple = (), min_iou: float = MIN_IOU_TO_CONSIDER_OVERLAP) -> int | None:
        """
        Tries to recover the track_id of an element for which we suspect that the track_id could have been lost
        given its finite_state_machine. If the track_id is recovered, it will be returned. If not, None will be returned.

        NOTE: This is only reliable when the elements are very static. Do not relay in this function if your elements
        are moving and tends to be overlapping between them.

        :param class_name: str. The current class detected for that element.
        :param bbox_xyxy: np.ndarray. The current bounding box of the element.
        :param in_scene_tracks: list | tuple. The tracks of the elements that are actually in the scene.
        :param mismatch_recovery: bool. True when we are recovering from a mismatch detection. False otherwise.
        :param max_difference_in_seconds: float | int. The maximum time difference in seconds to consider than
                                                an element in the history has not checked.
        :param min_iou: float. The minimum IoU between the bounding boxes of the element and the elements in the scene.

        :return int | None. The track_id of the element if it is recovered, None otherwise.
        """
        current_time = time()
        in_scene_tracks = set(in_scene_tracks)
        in_scene_tracks.union(set(self.recovered_tracks_correspondences.values()))
        # Search in the elements_history for those elements that have the same out_class_name than our current class.
        suspicious_track_ids = [track_id for track_id, element_info in self.state_buffer.elements_history.items()
                                    if self.track_id_is_suspicious(track_id=track_id, in_scene_track_ids=in_scene_tracks,
                                                                   mismatch_recovery=mismatch_recovery,
                                                                   element_info=element_info, current_object_class_name=class_name,
                                                                   max_difference_in_seconds=max_difference_in_seconds,
                                                                   current_time=current_time)]
        if len(suspicious_track_ids) > 0:
            # Check for the closer bbox to the current bbox
            suspicious_bboxes = [self.get_biggest_bbox_of_element(track_id=suspicious_track_id)
                                 for suspicious_track_id in suspicious_track_ids]
            # Get the intersection over union (IoU) between the current bbox and each suspicious bbox
            iou_values = [iou(bbox_xyxy, suspicious_bbox) if suspicious_bbox is not None else 0.
                          for suspicious_bbox in suspicious_bboxes]
            assert len(iou_values) == len(suspicious_track_ids), "The number of IoU values must be the same as the " \
                                                                    "number of suspicious track_ids. Got " \
                                                                    f"{len(iou_values)} and {len(suspicious_track_ids)}"
            if any(iou_value > min_iou for iou_value in iou_values):
                # Get the index of the biggest IoU value
                max_iou_index = np.argmax(iou_values)
                old_track_id = suspicious_track_ids[max_iou_index]
                return old_track_id
            elif self.verbose:
                print(f"Could not recover track_id for element with class {class_name} and bbox {bbox_xyxy}.")

        return None


    def get_biggest_bbox_of_element(self, track_id: int, max_bboxes_to_past: int = MAX_BBOXES_TO_CHECK_IN_PAST,
                                    max_frames_to_past:int = MAX_FRAMES_TO_CHECK_IN_PAST) -> np.ndarray | None:
        """
        Gets the biggest bbox of the element with the given track_id in the buffer or None if the element is
         not in the buffer.

        :param track_id: int. The track_id of the element to get the biggest bbox of.
        :param max_bboxes_to_past: int. The number of bboxes to look back in the buffer.
        :param max_frames_to_past: int. The number of frames to look back in the buffer.

        :return: np.ndarray or None. The biggest bbox of the element with the given track_id in the buffer.
        """
        biggest_area, biggest_bbox, checked_bboxes = -1, None, 0
        areas, bboxes, centers = [], [], []
        for i, scene_state in enumerate(reversed(self.state_buffer.buffer)):
            if track_id in scene_state.elements:
                bbox = scene_state.elements[track_id].bbox_xyxy
                area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
                bboxes.append(bbox), areas.append(area)
                centers.append(((bbox[0] + bbox[2]) / 2, (bbox[3] + bbox[1]) / 2))
                checked_bboxes += 1
            if checked_bboxes >= max_bboxes_to_past or i >= max_frames_to_past:
                break

        if checked_bboxes == 0:
            return None
        centers = np.array(centers, dtype=np.float32)
        centers_median, centers_std = np.median(centers, axis=0), np.std(centers, axis=0)
        # Get the mask of the centers that are not outliers
        centers_mask = np.all(np.abs(centers - centers_median) < 2 * centers_std, axis=1)

        # Take the max_area bbox that is not an outlier
        if np.any(centers_mask):
            valid_bboxes = np.array(bboxes)[centers_mask]
            valid_areas = np.array(areas)[centers_mask]
            biggest_bbox = valid_bboxes[np.argmax(valid_areas)]
        else:
            warn(f"Could not get the biggest bbox of element with track_id {track_id} because all "
                 f"the centers are outliers")
            biggest_bbox = None
        return biggest_bbox

    def track_id_is_suspicious(self, track_id: int, in_scene_track_ids: list | tuple, element_info: dict,
                               current_object_class_name: str, current_time: float | None = None,
                               mismatch_recovery: bool = True,
                               max_difference_in_seconds: float | int = DIFFERENCE_TO_CONSIDER_ELEMENT_LEFT_SCENE_IN_SECONDS) -> bool:
        """
        Checks if the given track_id could be suspicious of being the lost track of the element we are actually
        checking against. It does not take into account its position, only if they match by class and time.

        :param track_id: int. The track_id to check. It is a track_id from the elements_history.
        :param in_scene_track_ids: list | tuple. The track_ids of the elements that are actually in the scene.
        :param element_info: dict. The information of the element with the given track_id. It is, its entry in the
                                elements_history
        :param current_object_class_name: str. The current class name of the element for which we are checking
                                            for suspicious track_ids.
        :param current_time: float | None. The current time of the frame. If None, it will be taken as now.
        :param mismatch_recovery: bool. True when we are checking in a mismatch detection. It can be used when
                                    overwriting this method to change the behavior.
        :param max_difference_in_seconds: float | int. The maximum time difference in seconds to consider than
                                                an element is not alive anymore.

        :return: bool. True if the track_id is suspicious, False otherwise.
        """
        if current_time is None:
            current_time = time()
        is_track_still_alive = element_info[OUT_TIMESTAMP] > current_time - max_difference_in_seconds
        # If the track_id is not in the scene and the element has not been checked for a long time
        return track_id not in in_scene_track_ids and element_info[OUT_CLASS_NAME] == current_object_class_name and \
                is_track_still_alive

    def track_id_is_being_recovered(self, track_id: int, state_machine: ElementFiniteStateMachine | None = None) -> bool:
        """
        Checks if the given track_id is being recovered or not.

        :param track_id: int. The track_id to check.
        :param state_machine: ElementFiniteStateMachine | None. The state machine of the element with the given
            track_id or None. When using the recoverer together with finite_state_machines (as always will happen),
            this function will only return True if the state_machine is None. This is because the recoverer will
            not assign any state machine while trying to recover the track_id.

        :return bool. True if the track_id is being recovered, False otherwise.
        """
        return track_id in self.recover_tracks_attempts and self.recover_tracks_attempts[track_id] < self.max_recover_track_attempts \
            and state_machine is None and track_id not in self.recovered_tracks_correspondences

    def sanity_check(self, tracker_out: dict):

        tracker_out_keys = tuple(tracker_out.keys())
        # Find those elements that will collide once recovered to their correspondences
        transformed_track_ids = [self.recovered_tracks_correspondences.get(track_id, track_id)
                                 for track_id in tracker_out_keys]
        repeated_pairs = [(tracker_out_keys[i], track_id) for i, track_id in enumerate(transformed_track_ids)
                            if transformed_track_ids.count(track_id) > 1]
        if len(repeated_pairs) > 0:
            collisions = {collision_key : [tracker_id for tracker_id, correspondence in repeated_pairs
                                            if correspondence == collision_key]
                            for _, collision_key in repeated_pairs}
            for correspondence, origins in collisions.items():
                retags = []
                for detected_track in origins:
                    element = tracker_out[detected_track]
                    current_best_correspondence = self.recover_track_id(class_name=element[CLASS_NAME], bbox_xyxy=element[BBOX_XYXY],
                                                                   in_scene_tracks=tracker_out_keys, mismatch_recovery=True)
                    retags.append(current_best_correspondence)
                if any(retag is not None for retag in retags):
                    for current_track_id, retag in zip(origins, retags):
                        if retag is not None and retag != current_track_id:
                            from_previous = self.recovered_tracks_correspondences.get(current_track_id, None)
                            self.recovered_tracks_correspondences[current_track_id] = retag
                            print(f"Retagging track_id {current_track_id} to {retag} from {from_previous}")
                else:
                    print(f"Could not retag any of the collisions {origins} to any other track_id.")