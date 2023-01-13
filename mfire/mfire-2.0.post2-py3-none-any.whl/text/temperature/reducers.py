import string
from pint import Unit

from xarray import DataArray

from mfire.settings import get_logger, TEXT_ALGO
from mfire.text.base import BaseReducer
from mfire.utils.unit_converter import convert_dataarray
from mfire.utils.date import Datetime
from mfire.composite import WeatherComposite
from mfire.localisation.area_algebre import compute_IoU
from mfire.utils.xr_utils import mask_set_up

# Logging
LOGGER = get_logger(name="temperature_reducer.mod", bind="temperature_reducer")


class TemperatureReducer(BaseReducer):
    """Classe Reducer pour le module temperature.

    La méthode "compute" ici prend en entrée un "WeatherComposite" contenant
    exactement un "field" "temperature".

    Le résumé en sortie a la structure suivante:
    self.summary = {
        "general": {
            "start": <Datetime: date de début>,
            "stop": <Datetime: date de fin>,
            "tempe": {
                "units": <str: unités>,
                "mini": {
                    "low": <float: valeur basse des minimales>,
                    "high": <float: valeur haute des minimales>,
                },
                "maxi": {
                    "low": <float: valeur basse des maximales>,
                    "high": <float: valeur haute des maximales>,
                }
            }
        },
        "meta": {
            "production_datetime": <Datetime: date de début de production>,
        }
    }
    """

    def init_summary(self) -> None:
        self.summary = {
            "general": {
                "start": "",
                "stop": "",
                "tempe": {
                    "units": "",
                    "mini": {
                        "low": None,
                        "high": None,
                    },
                    "maxi": {
                        "low": None,
                        "high": None,
                    },
                },
            },
            "meta": {"production_datetime": ""},
        }

    @staticmethod
    def drop_axis(masks_da):
        """Removes the "Axis" masks from masks_da

        Args:
            masks_da (DataArray): All the masks for a given axis
            (including the axis itself)

        Returns:
            DataArray: All the masks, excluding the Axis
        """
        no_axis_da = masks_da

        for i, mask_id in enumerate(masks_da["id"]):
            if masks_da.isel(id=i)["areaType"].data == "Axis":
                no_axis_da = no_axis_da.drop_sel(id=mask_id.data)

        return no_axis_da

    def generate_summary(
        self, t_da: DataArray, units: Unit, masks_da: DataArray
    ) -> string:
        """_summary_

        Args:
            t_da (DataArray): _description_
            units (Unit): _description_
            masks_da (DataArray): _description_

        Returns:
            string: _description_
        """
        t_da = convert_dataarray(t_da, units).round(0)
        t_masks = mask_set_up(masks_da, t_da)

        t_masks = TemperatureReducer.drop_axis(t_masks)

        summary = TemperatureSummary(t_da, t_masks).generate_summary()

        return summary

    def compute_general_summary(self, compo: WeatherComposite) -> None:
        """Used to populate the "general" section of the summary data structure

        Generates a summary for all of the zones, for the whole period,
        following the level 2 guidelines
        (http://confluence.meteo.fr/pages/viewpage.action?pageId=333535918):
        * A maximum of 3 descriptive zones
        * a maximum of 3°C per descriptive zone

        Args:
            compo (WeatherComposite): component for which we need to generate
                a temperature summary
        """

        start = []
        stop = []

        # computing all the masks
        # if GeoComposite.mask_id is defined, its the only one computed
        # if we dont reset, we only get one mask, like...wtf?
        compo.geos.reset()
        compo.geos.mask_id = None
        masks_da = compo.geos.compute()

        for name in compo.params.keys():
            # trying to retrieve the Units from the WeatherComposite
            # i it fails, we get the default values
            units = compo.units.get(
                name,
                TEXT_ALGO[compo.id][compo.algorithm]["params"][name]["default_units"],
            )

            # computing the temperature dataset and only keeping
            # the useful variable
            # @todo : we could try to convert to int here in  order not to
            # round() further down
            param_da = self.data[name].astype("float16")

            # comuting each grid points min and max value for the period
            tn_da = param_da.min("valid_time", keep_attrs=True)
            tx_da = param_da.max("valid_time", keep_attrs=True)

            tn_summary = self.generate_summary(tn_da, units, masks_da)
            tx_summary = self.generate_summary(tx_da, units, masks_da)

            self.summary["general"]["tempe"]["mini"] = tn_summary
            self.summary["general"]["tempe"]["maxi"] = tx_summary
            self.summary["general"]["tempe"]["unit"] = units

            start.append(Datetime(param_da.valid_time.min().values))
            stop.append(Datetime(param_da.valid_time.max().values))

        self.summary["general"]["start"] = min(start)
        self.summary["general"]["stop"] = min(stop)

    def post_process_general_summary(self):
        """Does various operations on the summary dict in order to"""
        pass

    def add_metadata(self, compo: WeatherComposite) -> None:
        """Méthode qui ajoute au summary les metadata d'intérêt.
        Args:
            compo (Composite): Composant sur lequels on se base pour produire le texte
        """
        self.summary["meta"]["production_datetime"] = compo.production_datetime

    def compute(self, compo: WeatherComposite, metadata: dict = None) -> dict:
        super().compute(compo=compo)
        self.init_summary()
        self.compute_general_summary(compo)
        self.post_process_general_summary()
        self.add_metadata(compo)
        return self.summary


class TemperatureSummary:

    REQUIRED_DENSITY = 0.05  # minimum proportion of points for a valid zone
    MAX_RANGE = 3  # maximum difference of temperature in a descriptive zone
    MAX_ZONES = 3  # maximum number of descriptive zones

    def __init__(self, t_da: DataArray, masks: DataArray) -> None:
        self.t_da = t_da
        self.masks = masks

    def get_best_zone(self, da: DataArray) -> string:
        """Finds the zone most corresponding to the DataArray da

        Args:
            da (DataArray): temperatures for which we find to find a best matching zone

        Returns:
            string: the name of the zone (the 'areaName' of its corresponding
            mask)
        """

        # we filter out the masks not in our bbox (this makes the IoU faster)
        # plus, the IoU demands that the data and the masks share the same coords
        filtered_mask_da = self.masks.sel(latitude=da.latitude, longitude=da.longitude)

        # compute_IoU computes its score by making the sum of all the values >0
        # This obviously does not bode very well with negative temperatures :P
        # we figured that the easiest fix was to set all temperatures to 1
        # so that the IoU would not be influenced by higher values
        bool_da = da.where(da.isnull(), 1)

        # then we find the best mask
        iou_da = compute_IoU(bool_da.squeeze() > 0, filtered_mask_da)
        best_mask = self.masks.id.isel(id=iou_da.argmax("id"))

        LOGGER.info(
            f"BEST ZONE : {str(best_mask['areaName'].data)}"
            + f" {str(best_mask['areaType'].data)}"
        )

        return str(best_mask["areaName"].data), best_mask["areaType"].data

    def is_zone_valid(self, test_da: DataArray) -> bool:
        """
            returns whether the number of points in zone_da is high enough
            compared to the number of points in ref_da
        Args:
            test_da (DataArray): the zone we want to test
        Returns:
            bool: True if the number of points is high enough. False otherwise
        """
        return self.zone_coverage(test_da) >= self.REQUIRED_DENSITY

    def get_max_range(self, da: DataArray = None) -> int:
        """Returns the difference between the max and min values of a DataArray

        Args:
            da (DataArray): the DataArray for which we want the range

        Returns:
            int: the range of values for da
        """
        if da is None:
            da = self.t_da

        LOGGER.info(
            f"Max range : {int(da.min())}° - {int(da.max())}° : "
            + f"{int(da.max() - da.min()) + 1}°"
        )

        return int(da.max() - da.min())

    def get_t_within_values(
        self, t_da: DataArray, min_val: int, max_val: int
    ) -> DataArray:
        """
        Returns a subset of t_da with the data in the bracket [min_val; max_val[
        Args :
            t_da : a xr.DataArray containing all the values
            min_val : lower bound for the accepted value (included)
            max_val : higher bound for the accepted values (exluded)
        Retruns :
            DataArray : the subset of t_da
        """

        tmp_da = t_da.where(t_da >= min_val).where(t_da < max_val)

        return tmp_da

    def get_best_range(
        self, mini: int, maxi: int, t_range: int = MAX_RANGE
    ) -> DataArray:
        """Returns the best range of t_range values between t_min and t_max

        Args:
            da (DataArray): _description_
            min (int): max value
            max (int): min value
            t_range (int, optional): range of values to find

        Returns:
            DataArray: The most representating da.
            returns None if no not enough values are available
        """

        # computing all the possible intermediate classes
        best_zone = None
        best_score = 0

        while mini <= maxi and mini + t_range <= maxi:

            if maxi - mini <= t_range:
                t_range = maxi - mini  # we can't go past maxi !

            tmp_da = self.t_da.where(self.t_da >= mini).where(
                self.t_da < mini + t_range
            )
            LOGGER.info(f"    Using {int(mini)} <= data < {int(mini + t_range)}")
            score = self.score_zone(tmp_da)

            if score > best_score and self.is_zone_valid(tmp_da):
                best_score = score
                best_zone = tmp_da

            mini += 1

        return best_zone

    def score_zone(self, zone_da: DataArray) -> float:
        """computes the proportion of point of zone_da in the original zone

        Args:
            zone_da (DataArray): the zone we want to score

        Returns:
            float: the score of the zone
        """
        return float(zone_da.count() / self.t_da.count())

    def zone_coverage(self, zone_da: DataArray) -> float:
        """Computes the proportion of ref_da points present in zone_da

        Args:
            zone_da (DataArray): zone to score
            ref_da (DataArray): reference used to compute the score

        Returns:
            float: _description_
        """
        return float(zone_da.count() / self.t_da.count())

    def get_higher_range(self) -> DataArray:
        """Finds the DataArray containing hte highest range of °c that is representative
        enough

        Args:
            t_range (int, optional): range of the values to return.
            Defaults to MAX_RANGE.

        Returns:
            DataArray: _description_
        """

        t_max = int(self.t_da.max())
        t_min = int(self.t_da.min())

        max_da = self.t_da.where(self.t_da >= t_max - self.MAX_RANGE)

        # making sure the da does not consist manly of extreme, isolated values
        while not self.is_zone_valid(max_da) and t_max > t_min:
            t_max -= 1
            max_da = self.t_da.where(self.t_da >= t_max - self.MAX_RANGE)

        return max_da

    def get_lower_range(self, t_min=None, t_max=None, t_range=MAX_RANGE) -> DataArray:
        """Finds the DataArray containing the lowest range of °c that is representative
        engouh

        Args: t_range (int, optional): the range of the values to return.
        Defaults to MAX_RANGE.

        Returns:
            DataArray: _description_
        """

        if t_max is None:
            t_max = int(self.t_da.max())
        if t_min is None:
            t_min = int(self.t_da.min())

        # we ignore da consisting mainly of extreme isolated values
        is_zone_valid = False

        while (not is_zone_valid) and t_max > t_min:
            # we dont want range to accidentaly overlap
            if t_max - t_min < t_range:
                t_range = t_max - t_min

            min_da = self.t_da.where(self.t_da >= t_min)
            min_da = min_da.where(min_da <= t_min + t_range)

            is_zone_valid = self.is_zone_valid(min_da)
            t_min += 1

        return min_da

    def find_best_brackets(self) -> dict:
        """finds the DataArray(s) that best divide the temperature in a
        maximum of 3 brackets of MAX_RANGE values each

        Returns:
            dict: dict containing the das representing the brackets, in the
            following order : higher values, lower values, mid values
        """

        brackets = []

        t_range = self.get_max_range()
        t_min = self.t_da.min()

        # No matter how many zones we'll describe, there will always be
        # at least one. We abritrarily decide to start with the highest values
        max_t_da = self.get_higher_range()
        brackets.append(max_t_da)

        # we dont want to have overlaping values in the following descriptions
        t_max = max_t_da.min() - 1

        if t_max - t_min < self.MAX_RANGE:
            t_range = t_max - t_min
        else:
            t_range = self.MAX_RANGE

        # Making sure there are enough values left for another bracket
        if t_range > 0:

            min_t_da = self.get_lower_range(t_max=t_max)

            if min_t_da.count() == 0:
                LOGGER.info("Did not find values in the lowest range.")
                return brackets

            brackets.append(min_t_da)

            # we update t_min in order to not have overlapping ranges of °C
            # in the descriptions
            t_min = min_t_da.max() + 1

        if t_max - t_min < t_range:
            t_range = t_max - t_min

        # Naive implementation, we assume that MAX_ZONES will always = 3
        if t_range > 0:

            mid_t_da = self.get_best_range(int(t_min), int(t_max), t_range)

            # If the mid rang is not representative enough, it returns None
            if mid_t_da is not None:

                brackets.append(mid_t_da)

        return brackets

    def generate_summary(self) -> dict:
        """
        Generates a dict containing the data used to best summarize
        the temperature field t_da with these constraints
        * there can only be a maximum 3 zones used in the description
        * there can only be a maximum of MAX_RANGE temperature difference
          in a descriptive zone
        Returns : dict
        """
        summary = {}

        brackets_name = ["high", "low", "mid"]

        brackets = self.find_best_brackets()

        for i, bracket in enumerate(brackets):
            zone_name, zone_type = self.get_best_zone(bracket)
            summary[brackets_name[i]] = {
                "location": zone_name,
                "location_type": zone_type,
                "min": int(bracket.min().data),
                "max": int(bracket.max().data),
            }

        return summary
