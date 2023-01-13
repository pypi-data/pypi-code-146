from abc import ABC
import json
import warnings
from typing import Tuple, List

import shapely
import cv2
import geojson
import geojsoncontour
import numpy as np
import xarray as xr
from centerline.geometry import Centerline
from skimage import img_as_ubyte
from skimage.segmentation import morphological_chan_vese, checkerboard_level_set
from skimage.morphology import medial_axis
from skimage.filters.edges import convolve

from mfire.settings import get_logger, TEXT_ALGO
from mfire.composite.weather import WeatherComposite

warnings.filterwarnings("ignore", category=shapely.errors.ShapelyDeprecationWarning)


class ABCSegmentation(ABC):
    """ABC class for segmentation process.

    The segmentation consists in assigning a class to each pixel of a given ndarray,
    out of a given ndarray containing the probability for each pixel to belong to
    a list of classes.
    After this process of defining which pixel belongs to which class, we use image
    processing tools such as open_cv or skimage to extract object from the ndarray.
    Eventually we store extracted objects into geojson Features.

    Attrs:
        weather (WeatherComposite): weather object containing the used for the
            previously-done-prediction.
        channels (List[str]): names of the segmentation classes.
        threshold (float): threshold value to define if a pixel belong to a class
            or not.
        logger (Logger)
    """

    def __init__(self, weather: WeatherComposite):
        """Init method

        Args:
            weather (WeatherComposite): weather object containing the data used
                for the predictions.
        """
        self.weather = weather
        _text_algo = TEXT_ALGO[self.weather.id][self.weather.algorithm]
        self.channels = _text_algo["output"]
        self.threshold = _text_algo["threshold"]
        self.logger = get_logger(name=self.__module__, weather_id=self.weather.id)
        self.reset()

    def extract_value(self, var: str, **kwargs) -> xr.DataArray:
        """Method that extracts a value for a given variable contained in the
        self.weather.compute() Dataset.

        Args:
            var (str): Variable name
            **kwargs (Mapping, optionnal): xarray.DataArray.sel method's arguments.

        Returns:
            xr.DataArray: extracted values
        """
        return self.weather.compute()[var].sel(**kwargs).max(dim="id")

    def get_properties(self, da: xr.DataArray) -> dict:
        """returns a dictionnary containing the basic properties of an object
        according to the given xarray.DataArray describing the object itself.

        Args:
            da (xr.DataArray): DataArray used for predicting an object,
                thus containing the basic properties of this object.

        Returns:
            dict: Properties of the object.
        """
        return dict(
            name=da.name,
            validity_time=str(da.valid_time.values),
            reference_time=str(self.weather.production_datetime.as_np_datetime64()),
        )

    def reset(self):
        """
        Resets the segmentation process and initialize the self.summary dictionnary.
        """
        self.summary = dict()

    def process_single(self, da: xr.DataArray) -> List[geojson.Feature]:
        """Processes the segmentation on a single class.
        It takes a DataArray containing the probability for each pixel of belonging
        to the class it represents.
        It then detects the objects of that class and export them to a geojson Features.

        This method is currently NotImplemented because it belongs to an ABC class.
        Any class inheriting from ABCSegmentation must implement this method to properly
        work.

        Args:
            da (xr.DataArray): DataArray containing the proability for each pixel of
                belonging to a class.

        Raises:
            NotImplementedError: Currently not implemented.

        Returns:
            List[geojson.Feature]: List of objects detected.
        """
        raise NotImplementedError

    def process(self, ds: xr.Dataset) -> dict:
        """Processes the segmentation on all the variables (aka object classes) of a
        given xarray.Dataset, and returns the detected objects as geojson Features.

        The input Dataset has the following structure :
        >>> ds
        <xarray.Dataset>
        Dimensions:        (valid_time: 8, latitude: 118, longitude: 95)
        Coordinates:
            * valid_time     (valid_time) datetime64[ns] 2022-10-01 ...2022-10-02T21:0..
            * latitude       (latitude) float64 -5.75 -6.0 -6.25 ... -34.5 -34.75 -35.0
            * longitude      (longitude) float64 24.75 25.0 25.25 ... 47.75 48.0 48.25
        Data variables:
            anticyclone      (valid_time, latitude, longitude) float64 nan nan ... nan
            depression       (valid_time, latitude, longitude) float64 nan nan ... nan
        >>> my_segmentation.process(ds)
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

        Args:
            ds (xr.Dataset): Dataset to process.

        Returns:
            dict: dictionnary listing all the objects found at every valid_time.
        """
        for valid_time in ds.valid_time.values:
            self.logger.info(f"Processing valid_time '{valid_time}'.")
            features = [
                ft
                for var in self.channels
                for ft in self.process_single(ds[var].sel(valid_time=valid_time))
            ]
            self.summary[str(valid_time)] = geojson.FeatureCollection(features=features)
        return self.summary


class ContourSegmentation(ABCSegmentation):
    """Segmentation class for detecting "contours".
    It has specially been created for detecting "fronts" objects.
    """

    def process_single(self, da: xr.DataArray) -> List[geojson.Feature]:
        """Processes the segmentation on a single class.
        It takes a DataArray containing the probability for each pixel of belonging
        to the class it represents.
        It then detects the objects of that class and export them to a geojson Features.

        Args:
            da (xr.DataArray): DataArray containing the proability for each pixel of
                belonging to a class.

        Returns:
            List[geojson.Feature]: List of objects detected.
        """
        self.logger.info(f"Processing variable '{da.name}'.")
        image = da.where(da > self.threshold, 0).values

        # Morphological Chan Vese method
        init_level_set = checkerboard_level_set(image.shape, 10)
        level_set = morphological_chan_vese(
            image, 100, init_level_set=init_level_set, smoothing=2
        )
        percent = level_set.sum() / level_set.size
        if percent > 0.5:
            level_set = 1 - level_set
            percent = level_set.sum() / level_set.size

        # Filtering
        my_filter = np.ones((3, 3))
        skel = medial_axis(level_set)
        skel = convolve(skel, my_filter)
        dout = xr.DataArray(
            skel, coords=da.coords, dims=da.dims, name=da.name
        ).transpose("latitude", "longitude")

        # Creating a figure and turning it into a geojson
        fig = dout.plot.contourf(levels=[0.5, 1.5])
        fig.collections.remove(fig.collections[0])
        geojson_fig = geojsoncontour.contourf_to_geojson(fig)
        geometry = json.loads(geojson_fig)["features"][0]["geometry"]

        # creating lines out of the geojson
        shape = shapely.geometry.shape(geometry)
        lines = []
        for poly in shape.geoms:
            if poly.area > 3:
                res = geojson.Feature(
                    geometry=Centerline(
                        poly, interpolation_distance=0.5
                    ).__geo_interface__
                )
                res["properties"] = self.get_properties(da=da)
                lines.append(res)
        return lines


class BlobSegmentation(ABCSegmentation):
    """Segmentation class for detecting "blobs".
    It has specially been designed for detecting "anticyclones" and "depressions"
    objects
    """

    def new_feature(
        self, da: xr.DataArray, keypoint: Tuple[float, float]
    ) -> geojson.Feature:
        """Creates a geojson features out of a given probability field and a given
        keypoint representing the center of action a an object (anticyclone or
        depression).
        It also extracts specific pressure value for that keypoint.

        Args:
            da (xr.DataArray): Probability field.
            keypoint (Tuple[float, float]): (lon, lat) coordinates of the center of
                action of an object.

        Returns:
            geojson.Feature: feature describing the corresponding object.
        """
        lon = round(4 * da.longitude.values[int(keypoint[0])]) / 4
        lat = round(4 * da.latitude.values[int(keypoint[1])]) / 4
        value_pmer = int(
            self.extract_value(
                "msl", valid_time=da.valid_time.values, longitude=lon, latitude=lat
            )
            / 100
        )
        return geojson.Feature(
            geometry=dict(coordinates=(lon, lat), type="Point"),
            properties={"value_pmer": value_pmer, **self.get_properties(da=da)},
        )

    def process_single(self, da: xr.DataArray) -> List[geojson.Feature]:
        """Processes the segmentation on a single class.
        It takes a DataArray containing the probability for each pixel of belonging
        to the class it represents.
        It then detects the objects of that class and export them to a geojson Features.

        Args:
            da (xr.DataArray): DataArray containing the proability for each pixel of
                belonging to a class.

        Returns:
            List[geojson.Feature]: List of objects detected.
        """
        self.logger.info(f"Processing variable : '{da.name}'.")
        p = [100, 0.5, 0.8, 0.2]
        kernel_size = (11, 11)

        if da.name == "depression":
            p = [60, 0.45, 0.7, 0.1]
            kernel_size = (21, 21)

        # Get image
        img = da.where(da >= self.threshold, 0).values
        img8 = img_as_ubyte(img)

        # Smoothing
        blurred = cv2.GaussianBlur(img8, kernel_size, 0)
        img = cv2.threshold(blurred, 127.5, 255, cv2.THRESH_BINARY_INV)[1]

        # Setup SimpleBlobDetector parameters.
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = p[0]
        params.filterByCircularity = True
        params.minCircularity = p[1]
        params.filterByConvexity = True
        params.minConvexity = p[2]
        params.filterByInertia = True
        params.minInertiaRatio = p[3]

        # Create a detector with the parameters
        detector = cv2.SimpleBlobDetector_create(params)

        # Detect blobs.
        keypoints = detector.detect(img)

        return [self.new_feature(da, kpt) for kpt in cv2.KeyPoint_convert(keypoints)]


def get_segmentation(
    weather: WeatherComposite,
) -> BlobSegmentation | ContourSegmentation:
    """Factory function that initialize the correct segmentation object
    given a specific weather.

    Args:
        weather (WeatherComposite): Weather object.

    Returns:
        Union[BlobSegmentation, ContourSegmentation]: Segmentation object.
    """
    seg_name = TEXT_ALGO[weather.id][weather.algorithm]["segmentation"]
    return next(
        cls(weather)
        for cls in (BlobSegmentation, ContourSegmentation)
        if cls.__name__ == seg_name
    )


__all__ = ["get_segmentation", "BlobSegmentation", "ContourSegmentation"]
