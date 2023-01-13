from typing import Optional, Dict, List
from functools import cached_property

import shapely
import geojson
import numpy as np
from scipy.signal import savgol_filter
from scipy.spatial.distance import cosine

from mfire.settings import get_logger
from mfire.utils.geo import CompassRose8, distance_on_earth

__all__ = ["ADTracker", "FrontTracker", "Tracker"]


class SynObj(geojson.Feature):
    """Class that represents a synoptic object using a geojson.Feature interface.
    It provides two properties:
    - validity_time : quick access to the self.properties["validity_time"] value.
    - shape: the representation of the object as a shapely.geometry.shape

    Inheritance:
        geojson.Feature
    """

    @property
    def validity_time(self) -> str:
        """Quick access to self.properties["validity_time"]"""
        return self.properties.get("validity_time")

    @cached_property
    def shape(self) -> shapely.geometry.base.BaseGeometry:
        """Corresponding shapely.geometry.shape described by self.geometry"""
        return shapely.geometry.shape(self.geometry)


SynObjTrack = List[SynObj]


class ADTracker:
    """Class for tracking Anticyclone - Depression objects.

    Attrs:
        name (str)
        objects (dict)
        track_list (list)
        logger (Logger)
    """

    buffer_size: int = 3

    def __init__(self, name: str) -> None:
        """Init method.

        Args:
            name (str): Name of the object to track.
        """
        self.name = name
        self.logger = get_logger(
            name=self.__module__,
            cls=self.__class__.__name__,
            obj_name=self.name,
        )
        self.reset()

    def reset(self) -> None:
        """Method for reseting the tracking process and initializing the self.object
        dictionnary and the self.track_list.
        """
        self.objects = dict()
        self.track_list = list()

    def filter_objects(
        self, objects: Dict[str, List[SynObj]]
    ) -> Dict[str, List[SynObj]]:
        """Method used for selecting elements from the given objects list that
        have the properties["name"] == self.name

        Args:
            objects (Dict[str, List[SynObj]]): Objects's list to filter.

        Returns:
            Dict[str, List[SynObj]]: Filtered objects
        """
        return {
            date: [
                SynObj(**ft)
                for ft in objs["features"]
                if ft["properties"]["name"] == self.name
            ]
            for date, objs in objects.items()
        }

    def is_tracked(self, obj: SynObj) -> bool:
        """Checks whether a given obj is already tracked in the self.track_list

        Args:
            obj (dict): Object to check

        Returns:
            bool: Whether the obj is tracked or not
        """
        return any(obj in track for track in self.track_list)

    def similarity_score(self, obj1: SynObj, obj2: SynObj) -> Optional[float]:
        """Score used for comparing two given SynObj.
        This score is based on the IoU of the two objects.

        Args:
            obj1 (SynObj): Object 1
            obj2 (SynObj): Object 2

        Returns:
            Optional[float]: IoU of the two given objects if their intersection > 0.1,
                else None.
        """
        shape1, shape2 = [o.shape.buffer(self.buffer_size) for o in (obj1, obj2)]
        intersection = shape1.intersection(shape2)
        iou = intersection.area / (shape1.area + shape2.area - intersection.area)
        if iou > 0.1:
            return iou
        return None

    def add_direction(self, track: SynObjTrack) -> SynObjTrack:
        """Adds the direction information to the properties of all the SynObj contained
        in a given SynObjTrack.

        Args:
            track (SynObjTrack): List of SynObj to add the direction information to.

        Returns:
            SynObjTrack: New list of SynObj containing the direction information.
        """
        p1, p2 = (track[i].shape.centroid.coords[0] for i in (0, -1))
        direction = CompassRose8.from_points(p1, p2).text
        for obj in track:
            obj.properties["direction"] = direction
        return track

    def track_single(self, obj: SynObj, index: int) -> SynObjTrack:
        """Tracks a given object throughout the full self.objects list.

        Basically, the self.objects dictionnary lists all the objects found in
        the previously-done segmentation at every valid_time. This method takes
        a single object and its index in the list(self.objects.values()). It then
        finds all the objects corresponding to the future states of the given
        object.

        Args:
            obj (SynObj): Given object.
            index (int): Position index of the given of in the self.object.values()
                list.

        Returns:
            SynObjTrack: List of SynObj corresponding to the all the states of the given
                object in time.
        """
        track = [obj]
        objects = list(self.objects.values())[index + 1 :]
        for idx, next_objects in enumerate(objects):
            next_object_candidates = []
            self.logger.debug(f"---> Next Obj list {idx+1}/{len(objects)}")
            for obj_idx, next_obj in enumerate(next_objects):
                self.logger = self.logger.bind(
                    next_val_time=next_obj["properties"]["validity_time"]
                )
                if self.is_tracked(obj=next_obj):
                    self.logger.debug(
                        f"---> Next_obj {obj_idx+1}/{len(next_objects)} already tracked"
                    )
                    continue
                score = self.similarity_score(track[-1], next_obj)
                if score is None:
                    self.logger.debug(
                        f"---> Next_obj {obj_idx+1}/{len(next_objects)} too distant"
                    )
                    continue
                self.logger.debug(
                    f"---> Next_obj {obj_idx+1}/{len(next_objects)} "
                    f"added to candidates with score {score}"
                )
                next_object_candidates.append((score, next_obj))
            if len(next_object_candidates) > 0:
                track.append(max(next_object_candidates)[1])
                self.logger.debug(
                    "---> Next_obj chosen "
                    f"{np.argmax(np.array(next_object_candidates)[:, 0])+1} "
                    f"among {len(next_object_candidates)} candidates."
                )
        return self.add_direction(track)

    def run(self, objects: Dict[str, List[SynObj]]) -> List[SynObjTrack]:
        """Tracks all the objects in the given objects dictionnary.

        The objects dictionnary and the self.track_list have the following structure:
        >>> objects
        {
            "2022-10-01T00:00:00": [
                {
                    "type": "Feature",
                    "geometry": {...},
                    "properties": {...}
                },
                {
                    "type": "Feature",
                    "geometry": {...},
                    "properties": {...}
                },
                ...
            ],
            "2022-10-01T03:00:00": [
                {
                    "type": "Feature",
                    "geometry": {...},
                    "properties": {...}
                },
                {
                    "type": "Feature",
                    "geometry": {...},
                    "properties": {...}
                },
                ...
            ],
            ...
        }

        >>> ADTracker("depression").run(objects)
        [
            [
                {
                    "type": "Feature",
                    "geometry": {...},
                    "properties": {
                        "validity_time": "2022-10-01T00:00:00"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {...},
                    "properties": {
                        "validity_time": "2022-10-01T03:00:00"
                    }
                },
                ...
            ],
            [...],
            ...
        ]

        Args:
            objects (Dict[str, List[SynObj]]): Dictionnary containing all the objects
                detected at all the valid_time.

        Returns:
            List[SynObjTrack]: List of SynObj Tracking lists of objects.
        """
        self.objects = self.filter_objects(objects=objects)
        for idx, (val_time, objects_list) in enumerate(self.objects.items()):
            self.logger.debug(f"Validity time : {val_time}")
            for obj_idx, obj in enumerate(objects_list):
                if self.is_tracked(obj=obj):
                    self.logger.debug(
                        f"Object {obj_idx+1}/{len(objects_list)} already tracked"
                    )
                    continue
                self.logger.debug(
                    f"Start tracking object {obj_idx+1}/{len(objects_list)}"
                )
                track = self.track_single(obj, idx)
                if len(track) > 1:
                    self.track_list.append(track)
                else:
                    self.logger.debug(f"Object {obj_idx+1}/{len(objects_list)} lonely.")
        return self.track_list


class FrontTracker(ADTracker):
    """Class for tracking Fronts objects.
    It adds specific features for the tracking of front objects that are not
    necessary for the tracking of anticyclones or depressions, such as :
    - a method to smoothen object's coordinates
    - a new similarity score

    Inheritance:
        - ADTracker

    """

    buffer_size: int = 2

    @classmethod
    def smoothen_obj(cls, obj: SynObj) -> SynObj:
        """Class method to smoothen object's coordinates using a
        Savitzky-Golay filter. It basically reduces the number of points
        used for describing a front.

        Args:
            obj (SynObj): Object to smoothen.

        Returns:
            SynObj: New smoothen object.
        """
        # listing points and removing duplicates
        points_list = []
        for line in obj.geometry.coordinates:
            for point in line:
                if point not in points_list:
                    points_list.append(point)
        # separating
        xy = np.array(sorted(points_list)).T

        # smoothing using a Savitzky-Golay and sub-sampling
        ww = savgol_filter(xy, 3, 1)
        ww = np.concatenate((ww[:, ::3], ww[:, -1:]), axis=-1)

        return SynObj(
            geometry=geojson.LineString(coordinates=ww.T.tolist()),
            properties=obj.properties,
        )

    def similarity_score(self, obj1: SynObj, obj2: SynObj) -> Optional[float]:
        """Score used for comparing two given SynObj.
        This score is based on intersection of the objects and their cosine distance.

        Args:
            obj1 (SynObj): Object 1
            obj2 (SynObj): Object 2

        Returns:
            Optional[float]: score value.
        """
        shape1, shape2 = self.smoothen_obj(obj1).shape, self.smoothen_obj(obj2).shape
        if shape1.buffer(self.buffer_size).intersects(shape2.buffer(self.buffer_size)):
            score_cos = np.mean(
                (
                    cosine(shape1.coords[0], shape2.coords[0]),
                    cosine(shape1.coords[-1], shape2.coords[-1]),
                )
            )
            len_min, len_max = sorted((shape1.length, shape2.length))
            if score_cos < 0.2 and len_max < 3 * len_min:
                return len_min - len_max
        return None


class Tracker:
    """Class for tracking the evolution of all synoptic objects.
    Through its method `run`, it tracks anticyclones and depressions using
    a an ADTracker, and tracks fronts using a FrontTracker. Then it associates
    depressions and fronts that are close enough (through the
    `join_depressions_fronts` method).
    """

    def reset(self) -> None:
        """Method for reset the tracking process and initializing the tracking
        lists.
        """
        self.depressions, self.fronts = [], []
        self.tracks = dict()

    def join_depressions_fronts(self) -> Dict[str, list]:
        """Method used for joining depressions and fronts that are associated
        (i.e. close enough to each other).
        This method must be used once the self.depressions and self.fronts tracking
        list are already full. It then removes the associated objects and put them
        into a joined_depressions_fronts list.

        It also returns tracking lists of fronts alone and depressions alone.

        Returns:
            Dict[str, list]: Dictionnary returning the list of joined depressions and
            fronts, a list of fronts alone, and a list of depressions alone.
        """
        depressions_fronts, only_fronts = [], []
        for front_track in self.fronts:
            front = FrontTracker.smoothen_obj(front_track[0]).shape
            val_time = front_track[0].properties["validity_time"]
            depression_candidates = []
            for depression_track in self.depressions:
                depression_point = next(
                    (
                        o.geometry.coordinates
                        for o in depression_track
                        if o.properties["validity_time"] == val_time
                    ),
                    None,
                )
                if depression_point is None:
                    continue
                score = min(
                    distance_on_earth(front.centroid.coords[0], depression_point),
                    distance_on_earth(front.coords[0], depression_point),
                    distance_on_earth(front.coords[-1], depression_point),
                )
                if score < 500:  # distance between front and depression under 500 km
                    depression_candidates.append((score, depression_track))
            if len(depression_candidates) > 0:
                depressions_fronts.append((min(depression_candidates)[1], front_track))
            else:
                only_fronts.append(front_track)

        only_depressions = [
            depression_tracking
            for depression_tracking in self.depressions
            if depression_tracking not in [d for d, _ in depressions_fronts]
        ]

        return dict(
            joined_depressions_fronts=depressions_fronts,
            depressions=only_depressions,
            fronts=only_fronts,
        )

    def run(self, objects: Dict[str, List[SynObj]]) -> Dict[str, list]:
        """Main method of the Tracker. It takes a dictionnary listing all objects at
        every valid_time, gathers these objects by tracking list (anticyclones, fronts,
        depressions, and joined depressions and fronts).

        The input and output dictionnaries have the following structures:
        >>> objects
        {
            "2022-10-01T00:00:00": [
                {
                    "type": "Feature",
                    "geometry": {...},
                    "properties": {
                        "name": "front froid",
                        "validity_time": "2022-10-01T00:00:00"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {...},
                    "properties": {
                        "name": "depression",
                        "validity_time": "2022-10-01T00:00:00"
                    }
                },
                ...
            ],
            "2022-10-01T03:00:00": [
                {
                    "type": "Feature",
                    "geometry": {...},
                    "properties": {
                        "name": "front froid",
                        "validity_time": "2022-10-01T03:00:00"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {...},
                    "properties": {
                        "name": "depression",
                        "validity_time": "2022-10-01T03:00:00"
                    }
                },
                ...
            ],
            ...
        }
        >>> Tracker().run(objects)
        {
            "joined_depressions_fronts": [
                [
                    [
                        {
                            "type": "Feature",
                            "geometry": {...},
                            "properties": {
                                "name": "depression",
                                "validity_time": "2022-10-01T00:00:00"
                            }
                        },
                        {
                            "type": "Feature",
                            "geometry": {...},
                            "properties": {
                                "name": "depression",
                                "validity_time": "2022-10-01T03:00:00"
                            }
                        },
                        ...
                    ],
                    [
                        {
                            "type": "Feature",
                            "geometry": {...},
                            "properties": {
                                "name": "front froid",
                                "validity_time": "2022-10-01T00:00:00"
                            }
                        },
                        {
                            "type": "Feature",
                            "geometry": {...},
                            "properties": {
                                "name": "front froid",
                                "validity_time": "2022-10-01T03:00:00"
                            }
                        },
                        ...
                    ]
                ],
                ...
            ],
            "anticyclones": [
                [
                    {...},
                    {...},
                    ...
                ],
                [...],
                ...
            ],,
            "fronts": [
                [
                    {...},
                    {...},
                    ...
                ],
                [...],
                ...
            ],,
            "depressions": [
                [
                    {...},
                    {...},
                    ...
                ],
                [...],
                ...
            ],
        }

        Args:
            objects (Dict[str, List[SynObj]]): _description_

        Returns:
            Dict[str, list]: _description_
        """
        self.reset()
        self.fronts = FrontTracker("front froid").run(objects=objects)
        self.depressions = ADTracker("depression").run(objects=objects)
        self.tracks["anticyclones"] = ADTracker("anticyclone").run(objects=objects)
        self.tracks.update(self.join_depressions_fronts())
        return self.tracks
