from __future__ import annotations
from typing import Dict

import geojson
import xarray as xr
from tensorflow.keras.models import load_model

from mfire.settings import get_logger, TEXT_ALGO
from mfire.composite import WeatherComposite
from mfire.sit_gen.preprocessing import open_preprocessing
from mfire.sit_gen.segmentation import get_segmentation
from mfire.sit_gen.generator import DataGenerator

__all__ = ["Predictor"]


class Predictor:
    """Class predicting the synoptic objects in the given WeatherComposite.

    The Prediction process consists in three main steps:
    * pre-processing : the data comming from the given Weather is reshaped and
        normalized
    * predicting: a data generator feeds the Deep Learning model, which return
        for each pixel the probability of belonging to a specific synoptic object
        class.
    * post_processing: Given the previous matrix of probability, a segmentation is
    to be carried out in order to define where the synoptic objects are.

    A synoptic object is identified by a geojson.Feature.

    Attrs:
        weather (WeatherComposite): object containing data
        algo_settings (dict): settings of the algorithm chosen for the prediction
            process
        logger (Logger)
        preprocessor (Normalizer): tool for normalizing data
        postprocessor (Segmentation): tool for segmentating the probability matrix
    """

    def __init__(self, weather: WeatherComposite) -> None:
        """Init method

        Args:
            weather (WeatherComposite): object containing data
        """
        self.weather = weather
        self.algo_settings = TEXT_ALGO[self.weather.id][self.weather.algorithm]
        self.logger = get_logger(name=self.__module__, weather_id=self.weather.id)
        self.reset()

        self.preprocessor = open_preprocessing(self.algo_settings["normalizer"])
        self.postprocessor = get_segmentation(self.weather)

    def reset(self):
        """Method for reseting the prediction process and initializing private
        intermediary DataArrays, Datasets and dictionnaries
        """
        self._preproc_da = None
        self._preds_ds = None
        self._postproc_dict = None

    def pre_process(self) -> xr.DataArray:
        """Method for preprocessing the data comming from the self.weather.
        The preprocessing consists in:
        1. Normalizing the Dataset produced by the weather.compute() using the
        self.preprocessor Normalizer.
        2. reshaping the normalized Dataset into a single DataArray

        The weather.compute() Dataset and the returned DataArray have the following
        structures:
        >>> my_predictor.weather.compute()
        <xarray.Dataset>
        Dimensions:        (latitude: 118, longitude: 95, valid_time: 8, id: 1)
        Coordinates:
            * latitude       (latitude) float64 -5.75 -6.0 -6.25 ... -34.5 -34.75 -35.0
            * longitude      (longitude) float64 24.75 25.0 25.25 ... 47.75 48.0 48.25
            * valid_time     (valid_time) datetime64[ns] 2022-07-23...2022-07-23T21:0...
            * id             (id) object 'meteor'
            areaName       (id) object 'Meteor'
            areaType       (id) object ''
        Data variables:
            msl            (valid_time, latitude, longitude, id) float64 nan nan ... nan
            u850           (valid_time, latitude, longitude, id) float64 nan nan ... nan
            v850           (valid_time, latitude, longitude, id) float64 nan nan ... nan

        >>> my_predictor.pre_process()
        <xarray.DataArray 'super_set' (valid_time: 8, latitude: 118, longitude: 95,
                               variable: 3)>
        array([[[[[...]]]]])
        Coordinates:
            * valid_time     (valid_time) datetime64[ns] 2022-07-23...2022-07-23T21:0...
            * latitude       (latitude) float64 -5.75 -6.0 -6.25 ... -34.5 -34.75 -35.0
            * longitude      (longitude) float64 24.75 25.0 25.25 ... 47.75 48.0 48.25
            * variable       (variable) <U2 'msl' 'u_850' 'v_850'

        Returns:
            xr.DataArray: Preprocessed dataarray
        """
        if self._preproc_da is not None:
            self.logger.warning("Pre-process already done.")
            return self._preproc_da

        self.logger.info("Pre-process starting.")
        ds = self.weather.compute().max(dim="id")
        preproc_ds = self.preprocessor.transform(ds).assign_coords(
            longitude=(((ds.longitude + 180) % 360) - 180).round(5)
        )

        # transposer ("latitude", "longitude", "variable", "step")
        # et ordonner les variables selon l'ordre donné par les params
        self._preproc_da = (
            xr.merge(
                [
                    (
                        preproc_ds[var]
                        .expand_dims("variable")
                        .assign_coords({"variable": [var]})
                        .rename("super_set")
                    )
                    for var in preproc_ds
                ]
            )
            .super_set.transpose("valid_time", "latitude", "longitude", "variable")
            .sel(variable=list(self.algo_settings["params"]))
        )
        self.logger.info("Pre-process done.")
        return self._preproc_da

    def predict(self) -> xr.Dataset:
        """Method for predicting the probability of each pixel belonging to synoptic
        object's classes. It uses the previously preprocessed DataArray
        self._preproc_da, gives it to a DataGenerator that feeds a previously
        Deep Learned model.

        The output Dataset has the following structure:
        >>> my_predictor.predict()
        <xarray.Dataset>
        Dimensions:        (valid_time: 8, latitude: 118, longitude: 95)
        Coordinates:
            * valid_time     (valid_time) datetime64[ns] 2022-07-23...2022-07-23T21:0...
            * latitude       (latitude) float64 -5.75 -6.0 -6.25 ... -34.5 -34.75 -35.0
            * longitude      (longitude) float64 24.75 25.0 25.25 ... 47.75 48.0 48.25
        Data variables:
            anticyclone      (valid_time, latitude, longitude) float64 nan nan ... nan
            depression       (valid_time, latitude, longitude) float64 nan nan ... nan

        Returns:
            xr.Dataset: Predictior Dataset
        """
        if self._preds_ds is not None:
            self.logger.warning("Predict already done.")
            return self._preds_ds

        self.logger.info("Predict start")
        generator = DataGenerator(self._preproc_da, **self.algo_settings["generator"])

        model = load_model(filepath=self.algo_settings["model"])

        predictions = generator.gather(model.predict(generator[:]))

        coords = {
            "valid_time": generator.data.valid_time,
            "latitude": generator.data.latitude,
            "longitude": generator.data.longitude,
        }

        self._preds_ds = xr.Dataset(
            {
                channel: (tuple(coords), predictions[:, :, :, i])
                for i, channel in enumerate(self.algo_settings["output"])
            },
            coords=coords,
        )
        return self._preds_ds

    def post_process(self) -> Dict[str, geojson.FeatureCollection]:
        """Method that post-processes the prediction Dataset self._preds_ds, by
        segmentating it and finding the true class of all pixels. The resulting
        dictionnary lists all the synoptic objects found for every valid_time.

        The resulting dictionnary has the following structure:
        >>> my_predictor.post_process()
        {
            "2022-10-01T00:00:00": {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {...},
                        "properties": {...}
                    },
                    ...
                ]
            },
            "2022-10-01T03:00:00": {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {...},
                        "properties": {...}
                    },
                    ...
                ]
            },
            ...
        }

        Returns:
            Dict[str, geojson.FeatureCollection]: Resulting dictionnary
        """
        if self._postproc_dict is not None:
            self.logger.warning("Post-process already done.")
            return self._postproc_dict

        self.logger.info("Post-process starting.")
        self._postproc_dict = self.postprocessor.process(self._preds_ds)
        self.logger.info("Post-process done.")
        return self._postproc_dict

    def run(self) -> Dict[str, geojson.FeatureCollection]:
        """Method that runs the full prediction process.
        It consists in three main steps:
        * pre-process: the data comming from the given Weather is reshaped and
            normalized
        * predict: a data generator feeds the Deep Learning model, which return
            for each pixel the probability of belonging to a specific synoptic object
            class.
        * post_process: Given the previous matrix of probability, a segmentation is
        to be carried out in order to define where the synoptic objects are.

        The resulting dictionnary has the following structure:
        >>> my_predictor.run()
        {
            "2022-10-01T00:00:00": {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {...},
                        "properties": {...}
                    },
                    ...
                ]
            },
            "2022-10-01T03:00:00": {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {...},
                        "properties": {...}
                    },
                    ...
                ]
            },
            ...
        }

        Returns:
             Dict[str, geojson.FeatureCollection]: Resulting prediction dictionnary
        """
        self.pre_process()
        self.predict()
        return self.post_process()
