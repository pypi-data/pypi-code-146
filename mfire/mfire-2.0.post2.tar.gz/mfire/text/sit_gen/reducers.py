"""
@package mfire.sit_gen.sitgen_reduce

Module for aggregation
"""

from typing import Tuple

import shapely

from mfire.sit_gen import Predictor, Tracker
from mfire.text.base import BaseReducer
from mfire.composite import TextComponentComposite, WeatherComposite
from mfire.settings import get_logger

LOGGER = get_logger(name="reducers.mod", bind="reducers")


class SitGenReducer(BaseReducer):
    """
    Classe Reducer pour les textes de situation générale

    Structure de self.summary:
    {
        "Dépressions et fronts froids associés": liste des (front froid,dépression),
        "Dépressions": liste des dépressions détéctées,
        "Anticyclones": liste des anticyclones détéctés,
        "Fronts froids": liste des fronts froids détéctés,
    }
    Exemple de la structure de self.summary['Dépressions']:
        [
            [ma_depr à t=0, cette même depr à t+1, cette même depr à t+2, ...],
            [de même pour une autre depression...],
            ...
        ]
    """

    def reset(self) -> None:
        """Resets the reduction process and initialize the three dictionnaries
        used for reduction
        """
        self.predictions = dict()
        self.objects = dict()
        self.summary = dict()

    def add_prediction(self, weather: WeatherComposite) -> None:
        """Runs a Predictor object on a given WeatherComposite that detects synoptic
        objects, and gathers the results into the self.predictions dictionnary.

        The self.predictions dict has the following structure after the add_prediction
        method.

        >>> my_reducer.predictions
        {
            "2022-10-01T00:00:00": {
                "features": [
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
            },
            "2022-10-01T03:00:00": {
                "features": [
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
            },
            ...
        }

        Args:
            weather (WeatherComposite): Weather object to detect synoptic objects on.
        """
        for valid_time, features_collection in Predictor(weather).run().items():
            (
                self.predictions.setdefault(valid_time, dict())
                .setdefault("features", list())
                .extend(features_collection["features"])
            )

    def filter_objects(self, bounds: Tuple[float, float, float, float]) -> dict:
        """Method used for selecting features from the self.objects dictionnary
        that are related to the given geographical bounds given.
        An object / feature is considered as related to the given bounds if it
        intersects the box created out of these given boundaries.

        The self.objects and the returned dictionnaries have the following structure :
        >>> my_reducer.filter_objects(bounds)
        {
            "depressions": [
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
            ],
            "anticyclones": [...],
            "fronts": [...],
            "joined_depressions_fronts": [
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
                    ]
                ],
                [...],
                ...
            ]
        }

        Args:
            bounds (Tuple[float, float, float, float]): Coordinates of the boundaries
                (lon_min, lat_min, lon_max, lat_max)

        Returns:
            dict: Dictionnary looking like self.objects, containing only the objects
                intersecting the box described by the given bounds.
        """
        box = shapely.geometry.box(*bounds)
        filtered_objects = {key: [] for key in self.objects}
        for key, objects in self.objects.items():
            for track in objects:
                tr = track
                if isinstance(track[0], (tuple, list)):
                    tr = track[0]
                if any(obj.shape.intersects(box) for obj in tr):
                    filtered_objects[key].append(track)
        return filtered_objects

    def compute(self, text_compo: TextComponentComposite) -> dict:
        """Method that reduces the given TextComponentComposite into a dictionnary
        that contains for all geo ids the list of synoptic objects detected and their
        evolutions.

        The returned dictionnary has the following structure
        >>> my_reducer.compute(my_compo)
        {
            "geo_id_1": {
                "depressions": [
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
                ],
                "anticyclones": [...],
                "fronts": [...],
                "joined_depressions_fronts": [
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
                        ]
                    ],
                    [...],
                    ...
                ]
            },
            "geo_id_2": {...},
            ...
        }

        Args:
            text_compo (TextComponentComposite): Computed component containing the
                data to be reduced.

        Returns:
            dict: Reduction result.
        """
        self.reset()

        # Predictions par weather
        for weather in text_compo.weathers:
            self.add_prediction(weather=weather)

        # Track all objects
        self.objects = Tracker().run(self.predictions)

        # Association d'objets geo par geo
        for geo_id in text_compo.geos:
            bounds = text_compo.weathers[0].geos.bounds(geo_id=geo_id)
            self.summary[geo_id] = self.filter_objects(bounds=bounds)

        return self.summary
