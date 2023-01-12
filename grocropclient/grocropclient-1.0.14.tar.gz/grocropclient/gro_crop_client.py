import os
from datetime import datetime
from enum import Enum
from typing import List

import pandas as pd
from fuzzywuzzy import fuzz
from groclient import GroClient

from grocropclient import crop_budgets
from grocropclient.constants import FrequencyList, OtherItemsList, SourceList, MetricList, CropList, GRO_YIELD_MODELS, AreaWeightingSeriesList, ItemNameCategoryList, CROP_BUDGET_REGIONS, NATIONAL_AND_STATE_CROP_BUDGET_REGIONS, US_States


API_HOST = "api.gro-intelligence.com"

AVAILABLE_SOURCES = [s.value for s in SourceList]
AVAILABLE_METRICS = [s.value for s in MetricList]
AVAILABLE_ITEMS   = [s.value for s in CropList] + [s.value for s in OtherItemsList]

AVAILABLE_METRICS_NAMES = [(s.value, s.name.replace('_', ' ')) for s in MetricList]
AVAILABLE_ITEMS_NAMES   = [(s.value, s.name.replace('_', ' ')) for s in CropList] + [(s.value, s.name.replace('_', ' ')) for s in OtherItemsList]



def is_valid_selection(dataseries: dict) -> bool:
    """Returns True if the source/item/metric selection is within the US Crop tier."""
    return dataseries['source_id'] in AVAILABLE_SOURCES and \
    dataseries['metric_id'] in AVAILABLE_METRICS and \
    dataseries['item_id'] in AVAILABLE_ITEMS


def days_ago(gro_date: str):
    """Return the number of days between today's data and a Gro date."""
    # Wer remove the TZ ([0:10]) before we parse.
    return (datetime.today() - datetime.strptime(gro_date[0:10], "%Y-%m-%d")).days


# Translate ENUM into their value when inside a dictionary.
# This is useful when using methods that take ids as input, e.g. get_data_series.
def handle_enums(obj):
  fix_enum = lambda x: x.value if isinstance(x, Enum) else x
  
  if isinstance(obj, dict):
    for k,v in obj.items():
        obj[k] = list(map(fix_enum, v)) if isinstance(v, list) else fix_enum(v)
  elif isinstance(obj, list):
        obj = [fix_enum(v) for v in obj]
  else:
        obj = fix_enum(obj)
  
  return obj

def get_region_id(region_name: str, source_name: str) -> int:
    """Map crop budget region_name to numeric region_id"""
    region_name = region_name.lower()
    source_name = source_name.lower()
    return CROP_BUDGET_REGIONS[source_name][region_name]


def is_corn_or_soybeans(item_name: str) -> str:
    """
    This method is required because a different series exists for either corn or soybeans for Yield and Price 
    in the Area Weighting service.
    
    Returns
    -------
    either 'corn' or 'soybeans'
    """
    for word in item_name.split(' '):
        if ItemNameCategoryList.CORN.value in word.lower():
            return ItemNameCategoryList.CORN.value
        elif ItemNameCategoryList.SOYBEANS.value in word.lower():
            return ItemNameCategoryList.SOYBEANS.value


class GroCropClient(object):

    def __init__(self, api_host=API_HOST, access_token=None, proxy_host=None, proxy_port=None,
                 proxy_username=None, proxy_pass=None):
        """Construct a GroCropClient instance.
        Parameters
        ----------
        api_host : string, optional
            api_host : string
            The API host's url, excluding 'https://', to be consistent with groclient/lib.py
            ex. 'api.gro-intelligence.com'
        access_token : string, optional
            Your Gro API authentication token. If not specified, the
            :code:`$GROAPI_TOKEN` environment variable is used. See
            :doc:`authentication`.
        proxy_host : string, optional
            If you're instantiating the GroCropClient behind a proxy, you'll need to 
            provide the proxy_host to properly send requests using the groclient 
            library.
        proxy_port : int, optional
            If you're instantiating the GroCropClient behind a proxy, you'll need to 
            provide the proxy_port to properly send requests using the groclient 
            library.
        proxy_username : string, optional 
            If you're instantiating the GroCropClient behind a proxy, and your proxy 
            requires a username and password, you'll need to provide the proxy_username.
        proxy_pass : string optional
            Password for your proxy username.
        
        Raises
        ------
            RuntimeError
                Raised when neither the :code:`access_token` parameter nor
                :code:`$GROAPI_TOKEN` environment variable are set.
        Examples
        --------
            >>> client = GroClient()  # token stored in $GROAPI_TOKEN
            >>> client = GroClient(access_token="your_token_here")
        """

        if access_token is None:
            access_token = os.environ.get("GROAPI_TOKEN")
            if access_token is None:
                raise RuntimeError("GROAPI_TOKEN environment variable must be set when "
                                   "Your Gro Client is constructed without the access_token argument")
        self._api_host = api_host
        self._access_token = access_token
        self._proxy_host = proxy_host
        self._proxy_port = proxy_port
        self._proxy_username = proxy_username
        self._proxy_pass = proxy_pass

        self._client = GroClient(api_host = self._api_host, 
                                 access_token = self._access_token, 
                                 proxy_host = self._proxy_host,
                                 proxy_port = self._proxy_port,
                                 proxy_username = self._proxy_username,
                                 proxy_pass = self._proxy_pass)

    def get_sources(self):
        """Returns a list of all US Crop sources, as JSON.
            The schema for our US crop sources is:
            ['description',
            'fileFormat',
            'historicalStartDate',
            'id',
            'language',
            'longName',
            'name',
            'regionalCoverage',
            'resolution',
            'sourceLag']
        """
        dict = self._client.lookup('sources', [s.value for s in SourceList])
        return list(dict.values())

    def get_metrics(self, with_details=False):
        """Returns a list of metrics supported by the US Crop API.
           The list of id's comes from MetricList.
           For each item, we fetch the data from the Gro API via `lookup` if with_details is True. 
        """
        if with_details:
            return [self._client.lookup("metrics", m.value) for m in MetricList]
        else:
            return [{"short_name": m.name, "id": m.value} for m in MetricList]

    def get_crops(self, with_details=False):
        """Returns a list of metrics supported by the US Crop API.
           The list of id's comes from CropList.
           For each item, we fetch the data from the Gro API via `lookup` if with_details is True
        """
        if with_details:
            return [self._client.lookup("items", c.value) for c in CropList]
        else:
            return [{"short_name": c.name, "id": c.value} for c in CropList]

    # CROP BUDGET functions

    def get_crop_budgets(self, crop='', state=''):
        """Returns all crop budgets.
           The list can be filtered by crop (use name, not id) and by state (use name not id).
        """
        return crop_budgets.get_all_crop_budgets(self._api_host, self._access_token, crop=crop, state=state)

    def get_crop_budget_as_df(self, source_name, item_name, region_name, productivity):
        """Returns a given crop budget, as a pandas data frame.
           Use the source_name, item_name, region_name and productivity from the result of get_crop_budgets(…).
        """
        return crop_budgets.get_crop_budget_as_df(self._api_host, self._access_token, source_name=source_name, item_name=item_name, region_name=region_name, productivity=productivity)

    def get_crop_budget_yield_model(self, item_name: str, region_name: str, source_name: str, latest_date_only=False) -> pd.DataFrame:
        """
        Get the Gro Yield Model values (bu/acre) for the given item and region combination. If `latest_date_only` is True, only get the latest Yield value.
        The Yield value returned for each date is a weighted average of the district region values within the requested region,
        where the area of Corn or Soybeans harvested in those districts represents the weight.

        Parameters
        ----------
        item_name: str
        The `item_name` is from the result of from the result of get_crop_budgets(…)
        region_name: str 
        The `region_name` is from the result of from the result of get_crop_budgets(…)
        latest_date_only: bool
        If `latest_date_only` is True, only get the latest Yield value.

        Returns 
        -------
                    Yield 
        2000-02-25  0.217
        2000-03-04  0.217
        2000-03-12  0.221
        """
        region_id = get_region_id(region_name, source_name)
        crop = is_corn_or_soybeans(item_name)
        region_name = region_name.lower()
        if crop == ItemNameCategoryList.CORN.value:
            if region_name in NATIONAL_AND_STATE_CROP_BUDGET_REGIONS: 
                return self.get_yield_model_df(region_name, CropList.CORN.value, 284, latest_date_only)
            else:
                yield_dict = self._client.get_area_weighted_series(AreaWeightingSeriesList.CORN_YIELD.value, ['NASS Corn (US only)'], region_id, latest_date_only=latest_date_only)
        elif crop == ItemNameCategoryList.SOYBEANS.value:
            if region_name in NATIONAL_AND_STATE_CROP_BUDGET_REGIONS:
                return self.get_yield_model_df(region_name, CropList.SOYBEANS.value, 287, latest_date_only)
            else:
                yield_dict = self._client.get_area_weighted_series(AreaWeightingSeriesList.SOYBEANS_YIELD.value, ['NASS Soybeans (US only)'], region_id, latest_date_only=latest_date_only)
 
        return pd.DataFrame({'Yield': yield_dict.values()}, yield_dict.keys())
    

    def get_crop_budget_price(self, item_name: str, region_name: str, source_name: str, latest_date_only=False) -> pd.DataFrame:
        """
        Get the DTN Price ($/bu) values for the given item and region combination. If `latest_date_only` is True, only get the latest Price value.
        The price value returned for each date is an average of the district region values within the requested region.

        Parameters
        ----------
        item_name: str
        The `item_name` is from the result of from the result of get_crop_budgets(…)
        region_name: str 
        The `region_name` is from the result of from the result of get_crop_budgets(…)
        latest_date_only: bool
        If `latest_date_only` is True, only get the latest Price value.

        Returns 
        -------
                    Price
        2000-02-25  0.217
        2000-03-04  0.217
        2000-03-12  0.221
        """
        region_id = get_region_id(region_name, source_name)
        crop = is_corn_or_soybeans(item_name)
        if crop == ItemNameCategoryList.CORN.value:
            price_dict = self._client.get_area_weighted_series(AreaWeightingSeriesList.CORN_PRICE.value, ['AVERAGE'], region_id,latest_date_only=latest_date_only)
        elif crop == ItemNameCategoryList.SOYBEANS.value:
            price_dict = self._client.get_area_weighted_series(AreaWeightingSeriesList.SOYBEANS_PRICE.value, ['AVERAGE'], region_id, latest_date_only=latest_date_only)

        return pd.DataFrame({'Price': price_dict.values()}, price_dict.keys())
    # END OF CROP BUDGET functions

    def lookup(self, entity_type, entity_ids):
        """Retrieve details about a given id or list of ids of type entity_type.
        https://developers.gro-intelligence.com/gro-ontology.html
        Parameters
        ----------
        entity_type : { 'metrics', 'items', 'regions', 'frequencies', 'sources', 'units' }
        entity_ids : int or list of ints
        Returns
        -------
        dict or dict of dicts
            A dict with entity details is returned if an integer is given for entity_ids.
            A dict of dicts with entity details, keyed by id, is returned if a list of integers is
            given for entity_ids.
            Example::
                { 'id': 274,
                  'contains': [779, 780, ...]
                  'name': 'Corn',
                  'definition': 'The seeds of the widely cultivated corn plant <i>Zea mays</i>,'
                                ' which is one of the world\'s most popular grains.' }
            Example::
                {   '274': {
                        'id': 274,
                        'contains': [779, 780, ...],
                        'belongsTo': [4138, 8830, ...],
                        'name': 'Corn',
                        'definition': 'The seeds of the widely cultivated corn plant'
                                      ' <i>Zea mays</i>, which is one of the world\'s most popular'
                                      ' grains.'
                    },
                    '270': {
                        'id': 270,
                        'contains': [1737, 7401, ...],
                        'belongsTo': [8830, 9053, ...],
                        'name': 'Soybeans',
                        'definition': 'The seeds and harvested crops of plants belonging to the'
                                      ' species <i>Glycine max</i> that are used in the production'
                                      ' of oil and both human and livestock consumption.'
                    }
                }
        """        
        entity_ids = handle_enums(entity_ids)
        return self._client.lookup(entity_type, entity_ids)

    def lookup_unit_abbreviation(self, unit_id):

        return self.lookup("units", unit_id)["abbreviation"]

    def find_data_series(self, **kwargs):
        """Find data series from the US Crop tier matching a combination of entities specified by
        name and yield them ranked by coverage.
        Parameters
        ----------
        metric : string, optional
        item : string, optional
        region : string, optional
        partner_region : string, optional
        start_date : string, optional
            YYYY-MM-DD
        end_date : string, optional
            YYYY-MM-DD
        e.g. dataseries_gen = client.find_data_series(item="corn", metric="planted area", region="Illinois")
            for i in range(5):
            print(next(dataseries_gen))
        """
        dataseries_gen = self._client.find_data_series(**kwargs)
        while True:
            result = next(dataseries_gen)
            if is_valid_selection(result):
                yield result


    def get_data_series(self, **kwargs):
        """Get available data series for the given selections from the US Crop tier.
        https://developers.gro-intelligence.com/data-series-definition.html
        Parameters
        ----------
        metric_id : integer, optional
        item_id : integer, optional
        region_id : integer, optional
        partner_region_id : integer, optional
        source_id : integer, optional
        frequency_id : integer, optional
        Returns
        -------
        list of dicts
            Example::
                [{ 'metric_id': 2020032, 'metric_name': 'Seed Use',
                    'item_id': 274, 'item_name': 'Corn',
                    'region_id': 1215, 'region_name': 'United States',
                    'source_id': 24, 'source_name': 'USDA FEEDGRAINS',
                    'frequency_id': 7,
                    'start_date': '1975-03-01T00:00:00.000Z',
                    'end_date': '2018-05-31T00:00:00.000Z'
                }, { ... }, ... ]
        """

        # We translate ENUMs if needed.
        kwargs = handle_enums(kwargs)

        dataseries = self._client.get_data_series(**kwargs)
        filtered_dataseries=[series for series in dataseries if is_valid_selection(series)]
        return filtered_dataseries

    def get_data_points(self, **selections):
        """Gets all the data points for a given selection within the "US crops" tier.
        Parameters
        ----------
        metric_id : integer or list of integers
            How something is measured. e.g. "Export Value" or "Area Harvested"
        item_id : integer or list of integers
            What is being measured. e.g. "Corn" or "Rainfall"
        region_id : integer or list of integers
            Where something is being measured e.g. "United States Corn Belt" or "China"
        partner_region_id : integer or list of integers, optional
            partner_region refers to an interaction between two regions, like trade or
            transportation. For example, for an Export metric, the "region" would be the exporter
            and the "partner_region" would be the importer. For most series, this can be excluded
            or set to 0 ("World") by default.
        source_id : integer
        frequency_id : integer
        unit_id : integer, optional
        start_date : string, optional
            All points with end dates equal to or after this date
        end_date : string, optional
            All points with start dates equal to or before this date
        reporting_history : boolean, optional
            False by default. If true, will return all reporting history from the source.
        complete_history : boolean, optional
            False by default. If true, will return complete history of data points for the selection. This will include
            the reporting history from the source and revisions Gro has captured that may not have been released with an official reporting_date.
        insert_null : boolean, optional
            False by default. If True, will include a data point with a None value for each period
            that does not have data.
        at_time : string, optional
            Estimate what data would have been available via Gro at a given time in the past. See
            :sample:`at-time-query-examples.ipynb` for more details.
        include_historical : boolean, optional
            True by default, will include historical regions that are part of your selections
        available_since : string, optional
            Fetch points since last data retrieval where available date is equal to or after this date
        """

        # We translate ENUMS if any.
        selections = handle_enums(selections)

        # Check that source is within tier.
        if 'source_id' not in selections:
            raise Exception('a valid source_id MUST be selected')
        if selections['source_id'] not in AVAILABLE_SOURCES:
            raise Exception('Source %d is not part of the US Crops tier' % selections['source_id'])


        # For items and metrics, we may receive a list as an input.
        # In such cases, we interset the list with the list of valid metrics (resp. items),
        # If the intersection is non-empty, we proceed.

        # Check that item is within tier.
        if 'item_id' not in selections:
            raise Exception('a valid item_id MUST be selected')
        item_id = selections["item_id"]
        if ((type(item_id) == list) and len(set(item_id) & set(AVAILABLE_ITEMS)) == 0) or \
            item_id not in AVAILABLE_ITEMS:
            raise Exception('Selected item(s) %s not part of the US Crops tier' % str(selections['item_id']))

        # Check that metric is within tier.
        if 'metric_id' not in selections:
            raise Exception('a valid metric_id MUST be selected')
        metric_id = selections["metric_id"]
        if ((type(metric_id) == list) and len(set(metric_id) & set(AVAILABLE_METRICS)) == 0) or \
            metric_id not in AVAILABLE_METRICS:
            raise Exception('Selected metrics(s) %s not part of the US Crops tier' % str(selections['metric_id']))

        return self._client.get_data_points(**selections)

    def get_ancestor_regions(
      self,
      entity_id,
      distance=None,
      include_details=True,
      ancestor_level=None,
      include_historical=True,
      ):
        """Given a region, returns all its ancestors i.e.
        regions that "contain" in the given region.
        Parameters
        ----------
        entity_id : integer
        distance: integer, optional
            Return all entities that contain the entity_id at maximum distance. If provided along
            with `ancestor_level`, this will take precedence over `ancestor_level`.
            If not provided, get all ancestors.
        include_details : boolean, optional
            True by default. Will perform a lookup() on each ancestor to find name,
            definition, etc. If this option is set to False, only ids of ancestor
            entities will be returned, which makes execution significantly faster.
        ancestor_level : integer, optional
            The region level of interest. See REGION_LEVELS constant. This should only be specified
            if the `entity_type` is 'regions'. If provided along with `distance`, `distance` will
            take precedence. If not provided, and `distance` not provided, get all ancestors.
        include_historical : boolean, optional
            True by default. If False is specified, regions that only exist in historical data
            (e.g. the Soviet Union) will be excluded.
        """
        entity_id = handle_enums(entity_id)
        return self._client.get_ancestor(
            'regions', entity_id,
            distance=distance, include_details=include_details,
            ancestor_level=ancestor_level, include_historical=include_historical)

    def get_descendant_regions(
        self,
        entity_id,
        distance=None,
        include_details=True,
        descendant_level=None,
        include_historical=True,
    ):
        """Given a region, returns all its descendants i.e. entities that are "contained" in the given region.
        The `distance` parameter controls how many levels of child entities you want to be returned.
        Additionally, if you are getting the descendants of a given region, you can specify the
        `descendant_level`, which will return only the descendants of the given `descendant_level`.
        However, if both parameters are specified, `distance` takes precedence over
        `descendant_level`.
        Parameters
        ----------
        entity_id : integer
        distance: integer, optional
            Return all entities that contain the entity_id at maximum distance. If provided along
            with `descendant_level`, this will take precedence over `descendant_level`.
            If not provided, get all ancestors.
        include_details : boolean, optional
            True by default. Will perform a lookup() on each descendant  to find name,
            definition, etc. If this option is set to False, only ids of descendant
            entities will be returned, which makes execution significantly faster.
        descendant_level : integer, optional
            The region level of interest. See REGION_LEVELS constant. This should only be specified
            if the `entity_type` is 'regions'. If provided along with `distance`, `distance` will
            take precedence. If not provided, and `distance` not provided, get all ancestors.
        include_historical : boolean, optional
            True by default. If False is specified, regions that only exist in historical data
            (e.g. the Soviet Union) will be excluded.
        """
        
        entity_id = handle_enums(entity_id)
        return self._client.get_descendant(
            'regions', entity_id,
            distance=distance, include_details=include_details,
            descendant_level=descendant_level, include_historical=include_historical)

    def get_geo_centre(self, region_id):
        """Given a region_id (int), returns the geographic centre in degrees lat/lon.
        """
        region_id = handle_enums(region_id)
        return self._client.get_geo_centre(region_id)

    def get_geojson(self, region_id, zoom_level=7):
        """Given a region ID, return shape information in geojson.
        """
        region_id = handle_enums(region_id)
        return self._client.get_geojson(region_id, zoom_level=zoom_level)

    def search(self, entity_type, search_terms, num_results=10):
        """Searches for the given search term. Better matches appear first.
        Search for the given search terms and look up their details.
        For each result, yield a dict of the entity and its properties.
        """
        if entity_type == 'regions':
            for result in self._client.search_and_lookup('regions', search_terms, num_results=num_results):
                yield result

        if entity_type == 'metrics':
            ranked_results = sorted( [ (k[0], k[1], fuzz.token_set_ratio(search_terms, k[1])) for k in AVAILABLE_METRICS_NAMES], key=lambda x:x[2], reverse=True)
            for result in ranked_results:
                yield { 'metric_id': result[0], 'metric_shortname': result[1], 'score': result[2] }
        
        if entity_type == 'items':
            ranked_results = sorted([(k[0], k[1], fuzz.token_set_ratio(search_terms, k[1])) for k in AVAILABLE_ITEMS_NAMES], key=lambda x:x[2], reverse=True)
            for result in ranked_results:
                yield { 'item_id': result[0], 'item_shortname': result[1], 'score': result[2] }

        return "N/A"

    def get_top_region_match(self, query: str) -> dict:
        """
        Simple wrapper for self.search(...), returns the top region match for a string query
        """
        searchResults=list(self.search('regions', query, num_results=1))

        if len(searchResults)==0:
            raise Exception("No region match for query "+query)
        return searchResults[0]

    def add_single_data_series(self, data_series: dict) -> None:
        """Save a data series object to the GroClient's data_series_list.
        For use with :meth:`~.get_df`.
        Parameters
        ----------
        data_series : dict
            A single data_series object, as returned by :meth:`~.get_data_series` or
            :meth:`~.find_data_series`.
            See https://developers.gro-intelligence.com/data-series-definition.html
        Returns
        -------
        None
        """
        if is_valid_selection(data_series) is False:
            raise Exception("Can't add the following data series, not in the US Crops tier: "+str(data_series))
        self._client.add_single_data_series(data_series)

    def clear_data_series_list(self) -> None:
        """
        Clear the list of saved data series which have been added with add_single_data_series(...)
        """
        self._client._data_series_list = set()
        self._client._data_series_queue = []
        self._client._data_frame = pd.DataFrame()

    def get_df(self, **kwargs):
        """Call :meth:`~.get_data_points` for each saved data series and return as a combined
        dataframe.
        Note you must have first called either :meth:`~.add_data_series` or
        :meth:`~.add_single_data_series` to save data series into the GroClient's data_series_list.
        You can inspect the client's saved list using :meth:`~.get_data_series_list`.
        See https://developers.gro-intelligence.com/api.html#groclient.GroClient.get_df for full documentation
        """

        return self._client.get_df(**kwargs)

######################################
########## HELPER FUNCTIONS ##########
######################################

    ###########
    ## Yield ##
    ###########

    def get_all_yield_models(self):
        """Returns all yield models as an array of {"id": …, "name": …}. """
        return [{"id": k, "name": "%s / %s" % (v["region_name"], v["item_name"])} for k,v, in GRO_YIELD_MODELS.items()]

    def get_yield_model_data(self, yield_model_id, start_date=None):
        """Returns a given yield model, starting from a given data.
           The yield_model_id can be obtained from the result of calling get_all_yield_models().
        """
        if yield_model_id not in GRO_YIELD_MODELS:
            raise Exception("Not a valid yield model")
        else:
            ym = GRO_YIELD_MODELS[yield_model_id]
            # We need to ask for revisions to get all daily predictions.
            # We need to ask for metadata to get the confidence interval value.
            params = { "show_revisions": True, "show_metadata": True,
                       "source_id": SourceList.GRO_YIELD_MODEL.value, "frequency_id": 9,
                       "item_id":  ym["item_id"], "region_id": ym["region_id"], "metric_id": ym["metric_id"]}
        if start_date:
            params["start_date"] = start_date
        return self.get_data_points(**params)

    def get_yield_model_summary_last_N_days(self, yield_model_data, N:int = 5):
        """Returns a summary { "date": …, "value": … } for a given model, over the last N days.
        """
        if len(yield_model_data) == 0:
            print("no data")
            return None
        for point in yield_model_data:
            unit_id = point['unit_id']
            if unit_id != None:
                break
        unit_abbrev = self.lookup_unit_abbreviation(unit_id)
        summary = [] 
        for k in yield_model_data:
            if days_ago(k["available_date"]) < N:
                k_summary = {"date": k["available_date"][0:10]}
                if ('metadata' in k) & ("conf_interval" in k['metadata']):
                    k_summary["value"] =  "%f ± %f (%s)" % (k["value"],
                       k["metadata"]["conf_interval"], unit_abbrev)
                else:
                    k_summary["value"] =  "%f (%s)" % (k["value"], unit_abbrev)
                summary.append(k_summary)
        summary = summary[::-1]
        return summary
    
    
    def get_yield_model_df(self, region_name: str, item_id: int, unit_id: int, latest_date_only: bool) -> pd.DataFrame:
        """
        Helper function that converts result of get_data_points() into a DataFrame for the Yield Model source
        
        returns:
                        Yield
        2018-05-18  49.454534
        2018-05-19  49.423135
        2018-06-29  54.235872
        """
        region_id = NATIONAL_AND_STATE_CROP_BUDGET_REGIONS[region_name].value
        params = {
            'source_id': SourceList.GRO_YIELD_MODEL.value,
            'frequency_id': FrequencyList.ANNUAL.value,
            'item_id':  item_id,
            'region_id': region_id,
            'metric_id': MetricList.YIELD.value,
            'unit_id': unit_id,
            'start_date': '2001-01-01',
            'show_revisions': True
        }
        data_points = self.get_data_points(**params)
        values = [data_point['value'] for data_point in data_points]
        dates = [data_point['reporting_date'].split('T')[0] for data_point in data_points]
        yield_df = pd.DataFrame(data={'Yield': values}, index=dates)
        if latest_date_only:
            return yield_df.tail(1)
        else:
            return yield_df

    ############
    ## Prices ##
    ############

    def get_cash_prices_spot_county_level(self, crop_id: int, county_id: int, start_date: str = None, end_date: str = None):
        """Returns cash prices for a crop and a county."""
        params = { "source_id": SourceList.DTN_DISTRICT_AGGREGATED,
                   "frequency_id": 1,
                   "item_id":  crop_id,
                   "region_id": county_id,
                   "metric_id": MetricList.CASH_PRICES_SPOT_DELIVERY_CLOSE,
                   "start_date": start_date,
                   "end_date": end_date
        }
        return self.get_data_points(**params)

    def get_cash_prices_new_crop_county_level(self, crop_id: int, county_id: int, start_date: str = None, end_date: str = None):
        """Returns cash prices for a crop and a county."""
        params = { "source_id": SourceList.DTN_DISTRICT_AGGREGATED,
                   "frequency_id": 1,
                   "item_id":  crop_id,
                   "region_id": county_id,
                   "metric_id": MetricList.CASH_PRICES_NEW_CROP_DELIVERY_CLOSE,
                   "start_date": start_date,
                   "end_date": end_date}
        return self.get_data_points(**params)


    def get_basis_prices_spot_county_level(self, crop_id: int, county_id: int, start_date: str = None, end_date: str = None):
        """Returns basis prices for a crop and a county."""
        params = { "source_id": SourceList.DTN_DISTRICT_AGGREGATED,
            "frequency_id": 1,
            "item_id":  crop_id,
            "region_id": county_id,
            "metric_id": MetricList.BASIS_PRICES_SPOT_DELIVERY_CLOSE,
            "start_date": start_date,
            "end_date": end_date
           }
        return self.get_data_points(**params)

    def get_basis_prices_new_crop_county_level(self, crop_id: int, county_id: int, start_date: str = None, end_date: str = None):
        """Returns basis prices for a crop and a county."""
        params = { "source_id": SourceList.DTN_DISTRICT_AGGREGATED,
            "frequency_id": 1,
            "item_id":  crop_id,
            "region_id": county_id,
            "metric_id": MetricList.BASIS_PRICES_NEW_CROP_DELIVERY_CLOSE,
            "start_date": start_date,
            "end_date": end_date
            }
        return self.get_data_points(**params)
    
    def get_cash_prices_spot_facility_level(self, crop_id: int, region_id: int, start_date: str = None, end_date: str = None):
        """Returns facility-level cash prices for a crop and a region."""
        params = { "source_id": SourceList.DTN,
                   "frequency_id": 1,
                   "item_id":  crop_id,
                   "region_id": region_id,
                   "metric_id": MetricList.CASH_PRICES_SPOT_DELIVERY_CLOSE,
                   "start_date": start_date,
                   "end_date": end_date
        }
        return self.get_data_points(**params)

    def get_cash_prices_new_crop_facility_level(self, crop_id: int, region_id: int, start_date: str = None, end_date: str = None):
        """Returns facility-level cash prices for a crop and a region."""
        params = { "source_id": SourceList.DTN,
                   "frequency_id": 1,
                   "item_id":  crop_id,
                   "region_id": region_id,
                   "metric_id": MetricList.CASH_PRICES_NEW_CROP_DELIVERY_CLOSE,
                   "start_date": start_date,
                   "end_date": end_date}
        return self.get_data_points(**params)


    def get_basis_prices_spot_facility_level(self, crop_id: int, region_id: int, start_date: str = None, end_date: str = None):
        """Returns facility-level basis prices for a crop and a region."""
        params = { "source_id": SourceList.DTN,
            "frequency_id": 1,
            "item_id":  crop_id,
            "region_id": region_id,
            "metric_id": MetricList.BASIS_PRICES_SPOT_DELIVERY_CLOSE,
            "start_date": start_date,
            "end_date": end_date
           }
        return self.get_data_points(**params)

    def get_basis_prices_new_crop_facility_level(self, crop_id: int, region_id: int, start_date: str = None, end_date: str = None):
        """Returns facility-level basis prices for a crop and a region."""
        params = { "source_id": SourceList.DTN,
            "frequency_id": 1,
            "item_id":  crop_id,
            "region_id": region_id,
            "metric_id": MetricList.BASIS_PRICES_NEW_CROP_DELIVERY_CLOSE,
            "start_date": start_date,
            "end_date": end_date
            }
        return self.get_data_points(**params)

    def get_dtn_fertilizer_prices(self, fertilizer_id: int, region_id: int, start_date: str = None, end_date: str = None):
        """Returns facility-level basis prices for a fertilizer and a region at state (L4) and national (L3) levels."""
        params = {
            "source_id": SourceList.DTN,
            "frequency_id": 2,
            "item_id":  fertilizer_id,
            "region_id": region_id,
            "metric_id": MetricList.RETAIL_PRICES_CLOSE_INDEX,
            "start_date": start_date,
            "end_date": end_date
            }
        return self.get_data_points(**params)

    def get_dtn_facilities(self, region_id: int, crop: int, include_lat_longs: bool = False):
        """Returns DTN facility IDs for a specific region, optionally adding the lat/longs for each facility"""
        params = {
            'source_id': SourceList.DTN,
            'item_id': crop,
            'region_id': region_id,
            'metric_id': MetricList.BASIS_PRICES_SPOT_DELIVERY_CLOSE
        }
        
        available_series = self.get_data_series(**params)
        output_dicts = []
        region_ids = set()
        for series in available_series:
            region_ids.add(series['region_id'])
        region_ids = sorted(list(region_ids))

        for region_id in region_ids:
            output_dicts.append({'region_id': region_id})

        if include_lat_longs:
            region_details = self.lookup('regions', region_ids)
            for output_dict in output_dicts:
                region_id_str = str(output_dict['region_id'])
                if region_id_str in region_details:
                    output_dict['latitude'] = region_details[region_id_str].get('latitude')
                    output_dict['longitude'] = region_details[region_id_str].get('longitude')
                else:
                    output_dict['latitude'] = output_dict['longitude'] = None
        
        return output_dicts

    def get_futures_prices_rolling_front_month_settle_national(self, crop_id, start_date = None, end_date = None):
        """Returns future prices for a crop."""
        params = { "source_id": SourceList.GRO_DERIVED,
            "frequency_id": 1,
            "item_id":  crop_id,
            "region_id": 1215,
            "metric_id": MetricList.FUTURES_PRICES_ROLLING_FRONT_MONTH_SETTLE,
            "start_date": start_date,
            "end_date": end_date
            }
        return self.get_data_points(**params)      

    def get_futures_prices_settle_national(self, crop_id, start_date = None, end_date = None):
        """Returns future prices for a crop."""
        params = { "source_id": SourceList.CME,
            "frequency_id": 15,
            "item_id":  crop_id,
            "region_id": 1215,
            "metric_id": MetricList.FUTURES_PRICES_SETTLE,
            "start_date": start_date,
            "end_date": end_date
            }
        return self.get_data_points(**params)
      

    ##########
    ## Area ##
    ##########

    def get_area_harvested_USDA(self, crop: CropList, region, start_date = None, end_date = None):
        """Returns area harvested for a crop and a region."""
        params = { "metric_id": MetricList.AREA_HARVESTED,
             "item_id": crop,
             "region_id": region,
             "source_id": SourceList.USDA_NASS_CROPS,
             "frequency_id": 9,
             'start_date': start_date,
             'end_date': end_date,
             'unit_id': 41
             }
        return self.get_data_points(**params)

    def get_area_planted_USDA(self, crop: CropList, region, start_date = None, end_date = None):
        """Returns area planted for a crop and a region."""
        params = { "metric_id": MetricList.AREA_PLANTED,
             "item_id": crop,
             "region_id": region,
             "source_id": SourceList.USDA_NASS_CROPS if crop in [CropList.CORN, CropList.SOYBEANS] else SourceList.USDA_FSA,
             "frequency_id": 9,
             'start_date': start_date,
             'end_date': end_date,
             'unit_id': 41
             }
        return self.get_data_points(**params)

    def get_area_planted_GroForecasts(self, crop: CropList, region, start_date = None, end_date = None ):
        """Returns area planted for a crop and a region."""
        params = { "metric_id": MetricList.AREA_PLANTED,
             "item_id": crop,
             "region_id": region,
             "source_id": SourceList.GRO_ENTERPRISE_MODELS,
             "frequency_id": 9,
             'start_date': start_date,
             'end_date': end_date,
             'unit_id': 41
             }
        return self.get_data_points(**params)

    def get_area_prevented_USDA(self, crop: CropList, region, non_irrigated=False, start_date = None, end_date = None ):
        """Returns area prevented for a crop and a region."""
        params = { "metric_id": MetricList.AREA_PREVENTED_NON_IRRIGATED if non_irrigated else MetricList.AREA_PREVENTED,
             "item_id": crop,
             "region_id": region,
             "source_id": SourceList.USDA_FSA,
             "frequency_id": 9,
             'start_date': start_date,
             'end_date': end_date,
             'unit_id': 41
             }
        return self.get_data_points(**params)

    def get_area_prevented_GroForecasts(self, crop: CropList, region, non_irrigated=False, start_date = None, end_date = None ):
        """Returns area prevented for a crop and a region."""
        params = { "metric_id": MetricList.AREA_PREVENTED_NON_IRRIGATED if non_irrigated else MetricList.AREA_PREVENTED,
             "item_id": crop.value,
             "region_id": region,
             "source_id": SourceList.GRO_ENTERPRISE_MODELS,
             "frequency_id": 9,
             'start_date': start_date,
             'end_date': end_date,
             'unit_id': 41
             }
        return self.get_data_points(**params)

    def get_planting_progress(self, crop: CropList, region, start_date = None, end_date = None):
        """Returns planting progress for a crop and a region."""
        params = {'metric_id': MetricList.PLANTING_PROGRESS, 
	          'item_id': crop, 
            	  'region_id': region, 
	          'partner_region_id': 0, 
	          'source_id': SourceList.USDA_NASS_CROPS, 
	          'frequency_id': 2,
                  'start_date': start_date,
                  'end_date': end_date
                }
        return self.get_data_points(**params)

    ###########
    ## Trade ##
    ###########
    def get_sales_qty_outstanding_NMY(self, crop: CropList, partner_region=1231, start_date = None, end_date = None):
        """Returns sales quantity outstanding between US and partner_region, for a given crop."""
        params = { 'metric_id': MetricList.SALES_QUANTITY_OUTSTANDING_NMY,
                   'item_id': crop, 
                   'region_id': 1215, 
                   'partner_region_id': partner_region, 
                   'source_id': SourceList.USDA_ESR, 
                   'frequency_id': 2, 
                   'unit_id': 14,
                   'start_date': start_date,
                   'end_date': end_date
                }
        return self.get_data_points(**params)

    def get_sales_qty_total_commitments(self, crop, partner_region=1231, start_date = None, end_date = None):
        """Returns sales quantity commitment between US and partner_region, for a given crop."""
        params = { 'metric_id': MetricList.SALES_QUANTITY_TOTAL_COMMITMENTS_MASS,
                   'item_id': crop, 
                   'region_id': 1215, 
                   'partner_region_id': partner_region, 
                   'source_id': SourceList.USDA_ESR, 
                   'frequency_id': 2, 
                   'unit_id': 14
               }
        return self.get_data_points(**params)

    #############
    ## Climate ##
    #############
    
    def get_Gro_Drought_Index(self, region_id, frequency = FrequencyList.DAILY.value, start_date=None):
        """Returns Drought Index for a region and a frequency {daily, weekly, monthly} (use FrequencyList enum)."""
        if isinstance(frequency, Enum):
            frequency = frequency.value
        if frequency not in [FrequencyList.DAILY.value, FrequencyList.WEEKLY.value, FrequencyList.MONTHLY.value]:
            raise Exception("Invalid frequency. Must be one of {daily, weekly, monthly}.")
        params = { "metric_id": 15852252, "item_id": 17388, "frequency_id": frequency, "source_id": 145,
                   "region_id": region_id }
        if start_date:
            params["start_date"] = start_date
        return self.get_data_points(**params)

    def get_Gro_Observed_Flood(self, region_id, start_date=None):
        """Returns Gro Observed Flood for a given rgion."""
        params = { "metric_id": MetricList.OBSERVED_FLOOD, "item_id": OtherItemsList.WATER_AREAS,
                   "frequency_id": FrequencyList.DAILY, "source_id": SourceList.GRO_DERIVED_GEOSPATIAL,
                   "region_id": region_id }
        if start_date:
            params["start_date"] = start_date
        return self.get_data_points(**params)

    def get_MODIS_NDVI(self, region_id, start_date=None):
        params = { "metric_id": MetricList.VEGETATION, "item_id": OtherItemsList.VEGETATION_NDVI,
                   "frequency_id": FrequencyList.EIGHT_DAY, "source_id": SourceList.GIMMS_MODIS,
                   "region_id": region_id }
        if start_date:
            params["start_date"] = start_date
        return self.get_data_points(**params)

    def get_MODIS_LST(self, region_id, start_date=None):
        params = { "metric_id": MetricList.TEMPERATURE, "item_id": OtherItemsList.LAND_TEMPERATURE,
                   "frequency_id": FrequencyList.DAILY, "source_id": SourceList.MODIS_TERRA,
                   "region_id": region_id }
        if start_date:
            params["start_date"] = start_date
        return self.get_data_points(**params)

    def get_ESA_SMOS(self, region_id, start_date=None):
        params = { "metric_id": MetricList.AVAILABILITY_IN_SOIL, "item_id": OtherItemsList.SOIL_MOISTURE,
                   "frequency_id": FrequencyList.DAILY, "source_id": SourceList.ESA_SMOS,
                   "region_id": region_id }
        if start_date:
            params["start_date"] = start_date
        return self.get_data_points(**params)

    def get_GFS_Tmax(self, region_id, start_date=None):
        params = { "metric_id": MetricList.TEMPERATURE, "item_id": OtherItemsList.TEMPERATURE_MAX,
                   "frequency_id": FrequencyList.DAILY, "source_id": SourceList.GFS_00Z,
                   "region_id": region_id, "show_revisions": True}
        if start_date:
            params["start_date"] = start_date
        return self.get_data_points(**params)

    def get_GFS_Tmin(self, region_id, start_date=None):
        params = { "metric_id": MetricList.TEMPERATURE, "item_id": OtherItemsList.TEMPERATURE_MIN,
                   "frequency_id": FrequencyList.DAILY, "source_id": SourceList.GFS_00Z,
                   "region_id": region_id, "show_revisions": True}
        if start_date:
            params["start_date"] = start_date
        return self.get_data_points(**params)

    def get_GFS_Precip(self, region_id, start_date=None):
        params = { "metric_id": MetricList.PRECIPITATION_QUANTITY, "item_id": OtherItemsList.RAINFALL,
                   "frequency_id": FrequencyList.DAILY, "source_id": SourceList.GFS_00Z,
                   "region_id": region_id, "show_revisions": True}
        if start_date:
            params["start_date"] = start_date
        return self.get_data_points(**params)
