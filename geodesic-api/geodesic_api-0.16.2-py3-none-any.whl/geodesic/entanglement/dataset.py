from typing import Any, Optional, Union, List, Tuple
from functools import lru_cache
import re
import zlib
import warnings
import datetime as pydatetime

from geodesic.account.projects import Project, get_project
from geodesic.account.tokens import Token
from geodesic.bases import _APIObject
from dateutil.parser import isoparse

from geodesic.service import ServiceClient
from dateutil.parser import parse

from collections import defaultdict

from geodesic.descriptors import _BaseDescr, _DictDescr, _ListDescr, _StringDescr
from geodesic.client import get_client, raise_on_error
from geodesic.account import get_active_project
from geodesic.entanglement import Object
from geodesic.boson import BosonDescr, BosonConfig, DEFAULT_CREDENTIAL_KEY
from geodesic.stac import _AssetsDescr, FeatureCollection, Asset
import numpy as np
from geodesic.utils import DeferredImport, datetime_to_utc
from shapely.geometry import shape, box, MultiPolygon

display = DeferredImport('IPython.display')
pyproj = DeferredImport('pyproj')
ee = DeferredImport('ee')
Image = DeferredImport('PIL', 'Image')
object_widget = DeferredImport('geodesic.widgets.geodesic_widgets.object_widget')
item_assets_widget = DeferredImport('geodesic.widgets.geodesic_widgets.item_assets_widget')

arcgis = DeferredImport('arcgis')

datasets_client = ServiceClient('entanglement', 1, 'datasets')
stac_client = ServiceClient('spacetime', 1, 'stac')
boson_client = ServiceClient('boson', 1, 'proxy')
ted_client = ServiceClient('ted', 1, 'share')

stac_root_re = re.compile(r'(.*)\/collections\/')

_valid_resampling = [
    "nearest",
    "bilinear",
    "cubic",
    "cubicspline",
    "lanczos",
    "average",
    "mode",
    "max",
    "min",
    "median",
    "q1",
    "q3",
    "sum",
]


@lru_cache(maxsize=None)
def _get_dataset(name: str, project: str = None, version_datetime: Union[str, pydatetime.datetime] = None) -> 'Dataset':
    """gets a Dataset from Entanglement by name

    Args:
        ids: an optional list of dataset IDs to return
        search: a search string to use to search for datasets who's name/description match
        project: the name of the project to search datasets. Defaults to the active project
        version_datetime: the point in time to search the graph - will return older versions of
            datasets given a version_datetime.

    Returns:
        a DatasetList of matching Datasets.
    """
    dataset_list = list_datasets(ids=[name], project=project, version_datetime=version_datetime)
    if len(dataset_list) == 0:
        raise ValueError(f"dataset '{name}' not found")
    elif len(dataset_list) > 1:
        raise ValueError(f"more than one dataset matching '{name}' found, this should not happen, please report this")

    return dataset_list[0]


def get_dataset(
        name: str,
        project: str = None,
        version_datetime: Union[str, pydatetime.datetime] = None,
        refresh=False) -> 'Dataset':

    if refresh:
        _get_dataset.cache_clear()
    return _get_dataset(name, project, version_datetime)


def list_datasets(ids: Union[List, str] = [],
                  search: str = None,
                  project=None,
                  version_datetime: Union[str, pydatetime.datetime] = None) -> 'DatasetList':
    """searchs/returns a list of Datasets from Entanglement based on the user's query

    Args:
        ids: an optional list of dataset IDs to return
        search: a search string to use to search for datasets who's name/description match
        project: the name of the project to search datasets. Defaults to the active project
        version_datetime: the point in time to search the graph - will return older versions of
            datasets given a version_datetime.

    Returns:
        a DatasetList of matching Datasets.
    """

    if project is None:
        project = get_active_project()
    else:
        if isinstance(project, str):
            project = get_project(project)
        elif not isinstance(project, Project):
            raise ValueError("project must be a string or Project")

    params = {}
    if ids:
        if isinstance(ids, str):
            ids = ids.split(",")
        params['ids'] = ",".join(ids)

    if search is not None:
        params['search'] = search

    params['project'] = project.uid
    # Find object versions that were valid at a specific datetime
    if version_datetime is not None:
        # check for valid format
        if isinstance(version_datetime, str):
            params['datetime'] = datetime_to_utc(isoparse(version_datetime)).isoformat()
        elif isinstance(version_datetime, pydatetime.datetime):
            params['datetime'] = datetime_to_utc(version_datetime).isoformat()
        else:
            raise ValueError("version_datetime must either be RCF3339 formatted string, or datetime.datetime")

    resp = datasets_client.get('', **params)
    raise_on_error(resp)

    js = resp.json()
    if js['datasets'] is None:
        return DatasetList([])

    ds = [Dataset(**r) for r in js["datasets"]]
    datasets = DatasetList(ds, ids=ids)
    return datasets


class Dataset(Object):
    """Allows interaction with SeerAI datasets.

    Dataset provides a way to interact with datasets in the SeerAI.

    Args:
        \\*\\*obj (dict): Dictionary with all properties in the dataset.

    Attributes:
        alias(str): Alternative name for the dataset. This name has fewer restrictions on characters and should be human readable.
    """
    item = _DictDescr(doc="the contents of the dataset definition")
    alias = _StringDescr(nested="item", doc="the alias of this object, anything you wish it to be")
    data_api = _StringDescr(nested="item", doc="the api to access the data")
    item_type = _StringDescr(nested="item", doc="the api to access the data")
    item_assets = _AssetsDescr(nested="item", doc="information about assets contained in this dataset")
    services = _ListDescr(nested="item", item_type=str, doc="list of services that expose the data for this dataset")
    providers = _ListDescr(nested="item", doc="list of providers for this dataset")
    stac_extensions = _ListDescr(nested="item", doc="list of STAC extensions this dataset uses")
    links = _ListDescr(nested="item", doc="list of links")
    metadata = _DictDescr(nested="item", doc="arbitrary metadata for this dataset")
    boson_config = BosonDescr(nested="item", doc="boson configuration for this dataset", default=BosonConfig())
    version = _StringDescr(nested="item", doc="the version string for this dataset", default='')

    def __init__(self, **obj):
        o = {'class': "dataset"}
        # If this came from the dataset API, this needs to be built as an object
        if 'item' not in obj:
            o['item'] = obj
            uid = obj.get('uid')
            if uid is not None:
                o['uid'] = uid
            o['name'] = obj.get('name', None)
            o['class'] = "dataset"
            o['domain'] = obj.get('domain', "*")
            o['category'] = obj.get('category', "*")
            o['type'] = obj.get('type', "*")
            o['description'] = obj.get('description', '')
            o['keywords'] = obj.get('keywords', [])
            o['metadata'] = obj.get('metadata', {})

            # geom from extent
            extent = obj.get('extent', {})
            spatial_extent = extent.get('spatial', None)
            if spatial_extent is not None:
                boxes = []
                for bbox in spatial_extent.get('bbox', []):
                    g = box(*bbox, ccw=False)
                    boxes.append(g)

                if len(boxes) == 1:
                    g = boxes[0]
                else:
                    g = MultiPolygon(boxes)

                self.geometry = g

        # Otherwise, parse as object
        else:
            obj['item']['uid'] = obj['uid']
            o = obj

        project = o.get('item', {}).get('project', None)

        super().__init__(**o)
        if project is not None:
            self.project = project

    def validate(self):
        res = self._client.post(
            "datasets/validate",
            dataset=self.item,
            project=self.project.uid
        )

        try:
            raise_on_error(res)
        except Exception:
            try:
                js = res.json()['error']
                print("Failed Validation:")
                print(js['detail'])
            except Exception:
                print(res.text)
            return False

        return True

    @property
    def object_class(self):
        return "Dataset"

    @object_class.setter
    def object_class(self, v):
        if v.lower() != "dataset":
            raise ValueError("shouldn't happen")
        self._set_item('class', 'dataset')

    @property
    def bands(self):
        return self.item_assets

    def _ipython_display_(self, **kwargs):
        # Make this look like dataset list but with a single entry so one template can be used for both
        datasetList = {self.name: self}
        return object_widget.ObjectWidget(datasetList)._ipython_display_(**kwargs)

    def create(self):
        """
        Creates a new Dataset in Entanglement

        Raises:
            requests.HTTPError: If this failed to create or if the dataset already exists
        """
        # Make sure the uid is either None or valid
        _ = self.uid

        body = {
            "overwrite": False,
            "dataset": self.item
        }

        res = raise_on_error(self._client.post("datasets", project=self.project.uid, **body))

        try:
            uids = res.json()['uids']
        except KeyError:
            raise KeyError("no uids returned, something went wrong")

        if len(uids) > 1:
            raise ValueError("more datasets affected than requested, something unexpected happened")

        self._set_item('uid', uids[0])

    def save(self):
        """
        Updates an existing Dataset in Entanglement.

        Raises:
            requests.HTTPError: If this failed to save.
        """
        # Make sure the uid is either None or valid
        try:
            self.uid
        except ValueError as e:
            raise e

        body = {
            "overwrite": True,
            "dataset": self.item
        }

        res = raise_on_error(self._client.post("datasets", project=self.project.uid, **body))
        try:
            uids = res.json().get('uids', [])
        except KeyError:
            raise KeyError("no uids returned, something went wrong")

        if len(uids) > 1:
            raise ValueError("more datasets affected than requested, something unexpected happened")
        elif len(uids) == 1:
            self._set_item('uid', uids[0])

    def query(
        self,
        bbox: Optional[List] = None,
        datetime: Union[List, Tuple] = None,
        limit: Optional[Union[bool, int]] = 10,
        intersects: Optional[object] = None,
        **kwargs
    ):
        """ Query the dataset for items.

        Query this service's OGC Features or STAC API.

        Args:
            bbox: The spatial extent for the query as a bounding box. Example: [-180, -90, 180, 90]
            datetime: The temporal extent for the query formatted as a list: [start, end].
            limit: The maximum number of items to return in the query.

        Returns:
            A :class:`geodesic.stac.FeatureCollection` with all items in the dataset matching the query.

        Examples:
            A query on the `sentinel-2-l2a` dataset with a given bouding box and time range. Additionally it
            you can apply filters on the parameters in the items.

            >>> bbox = geom.bounds
            >>> date_range = (datetime.datetime(2020, 12,1), datetime.datetime.now())
            >>> ds.query(
            ...          bbox=bbox,
            ...          datetime=date_range,
            ...          query={'properties.eo:cloud_cover': {'lte': 10}}
            ... )
        """
        # STAC client is for Spacetime requests
        client = stac_client

        # No prefix needed for Spacetime queries
        url_prefix = ''
        project = self.project.uid

        # STAC Collection <=> Dataset name
        collection = self.get('collection', self.name)

        # If this Dataset is a boson, the url needs to be crafted slightly differently.
        # Specifically, it needs the servicer and dataset config fragment prefixed to the
        # STAC/OGC Features url fragment
        if self.boson_config and self.boson_config.provider_name != '':
            if 'collection' in self.boson_config.properties:
                collection = self.boson_config.properties['collection']
            client = boson_client
            url_prefix = f'stac/{self.name}.{project}/'

        api = kwargs.get("api", self.data_api)
        # clients = self.clients

        if api is None:
            api = "stac"

        query_all = False
        if not limit:
            limit = kwargs.pop('page_size', 500)
            query_all = True

        # Request query/body
        params = {"limit": limit, 'project': project}

        if api == "features":
            url = url_prefix + f"collections/{collection}/items"
        elif api == "stac":
            params["collections"] = kwargs.get("collections", [collection])
            url = url_prefix + "search"
        else:
            raise ValueError(f"specified api must be either 'features' or 'stac', got '{api}'")

        # Parse geospatial aspect of this query (bbox and intersects)
        params = self._query_parse_geometry(params, api, bbox, intersects)

        # Parse STAC search specific query/filtering
        if api == "stac":
            params = self._query_parse_stac_query(params, api, kwargs)

        if datetime is not None:
            params["datetime"] = "/".join([datetime_to_utc(parsedate(d)).isoformat() for d in datetime])

        if api == "features":
            res = raise_on_error(client.get(url, **params))
        elif api == "stac":
            res = raise_on_error(client.post(url, **params))

        # Wrap the results in a FeatureCollection
        collection = FeatureCollection(dataset=self, query=params, **res.json())

        # If query_all, this cycles through all pages and reads into the feature collection.
        if query_all:
            collection.get_all()

        # Set a flag on the collection denoting that STAC capabilities are available.
        if api == "stac":
            collection._is_stac = True

        return collection

    def _query_parse_geometry(self, params: dict, api: str, bbox: Optional[list], intersects: object) -> dict:
        """
        For a STAC/OGC Features query, parse the bbox/geometry depending on the API type

        Arguments:
            params: the dictionary of parameters we are updated for the query. Modified inplace, but also returned.
            api: the type of api for the call we are building
            bbox: the four corners of a geospatial bounding box
            intersects: a geometry object or something that satisfies the geointerface spec

        Returns:
            params

        """
        # If the bounding box only provided.
        if bbox is not None and intersects is None:
            if api == "stac":
                params["bbox"] = bbox
            else:
                params["bbox"] = ",".join(map(str, bbox))
        # If a intersection geometry was provided
        if intersects is not None:
            # Geojson
            if isinstance(intersects, dict):
                try:
                    g = shape(intersects)
                except ValueError:
                    try:
                        g = shape(intersects['geometry'])
                    except Exception as e:
                        raise ValueError('could not determine type of intersection geometry') from e

            elif hasattr(intersects, "__geo_interface__"):
                g = intersects

            else:
                raise ValueError("intersection geometry must be either geojson or object with __geo_interface__")

            # If STAC, use the geojson
            if api == "stac":
                params["intersects"] = g.__geo_interface__
            # Bounding box is all that's supported for OAFeat
            else:
                try:
                    # Shapely
                    params["bbox"] = ','.join([str(x) for x in g.bounds])
                except AttributeError:
                    # ArcGIS
                    params["bbox"] = ','.join([str(x) for x in g.extent])
        return params

    def _query_parse_stac_query(self, params: dict, api: str, kwargs: dict) -> dict:
        """
        For a STAC/OGC Features query, parse the bbox/geometry depending on the API type

        Arguments:
        """
        # Individual item ids to get
        ids = kwargs.get("ids", None)
        if ids is not None:
            params["ids"] = ids

        # Parse the original STAC Query object, this will go away soon now that
        # The core STAC spec adopted CQL.
        query = kwargs.get("query", None)
        if query is not None:
            for k, v in query.items():
                gt = v.get("gt")
                if gt is not None and isinstance(gt, pydatetime.datetime):
                    v["gt"] = gt.isoformat()
                lt = v.get("lt")
                if lt is not None and isinstance(lt, pydatetime.datetime):
                    v["lt"] = lt.isoformat()
                gte = v.get("gte")
                if gte is not None and isinstance(gte, pydatetime.datetime):
                    v["gte"] = gte.isoformat()
                lte = v.get("lte")
                if lte is not None and isinstance(lte, pydatetime.datetime):
                    v["lte"] = lte.isoformat()
                eq = v.get("eq")
                if eq is not None and isinstance(eq, pydatetime.datetime):
                    v["eq"] = eq.isoformat()
                neq = v.get("neq")
                if neq is not None and isinstance(neq, pydatetime.datetime):
                    v["neq"] = neq.isoformat()
                query[k] = v

            params["query"] = query

        # Sortby object, see STAC sort spec
        sortby = kwargs.pop("sortby", None)
        if sortby is not None:
            params["sortby"] = sortby

        # Fields to include/exclude.
        fields = kwargs.pop("fields", None)
        if fields is not None:
            fieldsObj = defaultdict(list)
            # fields with +/-
            if isinstance(fields, list):
                for field in fields:
                    if field.startswith("+"):
                        fieldsObj["include"].append(field[1:])
                    elif field.startswith("-"):
                        fieldsObj["exclude"].append(field[1:])
                    else:
                        fieldsObj["include"].append(field)
            else:
                fieldsObj = fields
            params["fields"] = fieldsObj
        return params

    def warp(self, *,
             bbox: list,
             datetime: Union[List, Tuple] = None,
             pixel_size: Optional[list] = None,
             shape: Optional[list] = None,
             pixel_dtype: Union[np.dtype, str] = np.float32,
             bbox_srs: str = "EPSG:4326",
             output_srs: str = "EPSG:3857",
             resampling: str = 'nearest',
             input_nodata: Any = None,
             output_nodata: Any = None,
             compress: bool = True,
             content_type: str = 'raw',
             asset_bands: list = [],
             asset_names: list = [],
             band_ids: list = [],
             query: dict = {},
             filter: dict = {},
             ):
        """get pixel data or an image from this `Dataset`

        `warp` gets requested pixels from a dataset by calling Boson. This method returns either a
        numpy array or the bytes of a image file (jpg, png, gif, or tiff). If the `content_type` is
        "raw", this will return a numpy array, otherwise it will return the requested image format as
        bytes that can be written to a file. Where possible, a COG will be returned for Tiff format,
        but is not guaranteed.

        Args:
            bbox: a bounding box to export as imagery (xmin, ymin, xmax, ymax)
            datetime: a start and end datetime to query against. Imagery will be filtered to between this range and
                mosaiced.
            pixel_size: the x/y pixel size of the output imagery. This should be specified in the output spatial
                reference.
            shape: the shape of the output image (rows, cols). Either this or the `pixel_size` must be specified,
                but not both.
            pixel_dtype: a numpy datatype or string descriptor in numpy format (e.g. <f4) of the output. Most, but
                not all basic dtypes are supported.
            bbox_srs: the spatial reference of the bounding bbox, as a string. May be EPSG:<code>, WKT, Proj4, ProjJSON,
                etc.
            output_srs: the spatial reference of the output pixels.
            resampling: a string to select the resampling method.
            input_nodata: in the source imagery, what value should be treated as no data?
            output_nodata: what value should be set as the nodata value in the resulting dataset. Only meaningful for
                tiff outputs.
            compress: compress bytes when transfering. This will usually, but not always improve performance
            content_type: the image format. Default is "raw" which sends raw image bytes that will be converted into a
                numpy. If "jpg", "gif", or "tiff", returns the bytes of an image file instead, which can directly be
                written to disk.
            asset_bands: a list containing dictionaries with the keys "asset" and "bands". Asset should point to an
                asset in the dataset, and "bands" should list band indices (0-indexed) or band names.
            asset_names: DEPRECATED, use asset_bands instead
            band_ids: DEPRECATED, use asset_bands instead
            query: DEPREACTED, use filter
            filter: a CQL2 JSON filter to filter images that will be used for the resulting output.

        Returns:
            a numpy array or bytes of an image file.
        """

        if pixel_size is None and shape is None:
            raise ValueError('must specify at least pixel_size or shape')
        elif pixel_size is not None and shape is not None:
            raise ValueError('must specify pixel_size or shape, but not both')

        if content_type not in ('raw', 'jpeg', 'jpg', 'gif', 'tiff', 'png'):
            raise ValueError('content_type must be one of raw, jpeg, jpg, gif, tiff, png')

        if resampling not in _valid_resampling:
            raise ValueError(f'resampling must be one of {", ".join(_valid_resampling)}')

        if pixel_dtype in ['byte', 'uint8']:
            ptype = pixel_dtype
        else:
            ptype = np.dtype(pixel_dtype).name

        req = {
            'output_extent': bbox,
            'output_extent_spatial_reference': bbox_srs,
            'output_spatial_reference': output_srs,
            'pixel_type': ptype,
            'resampling_method': resampling,
            'content_type': content_type,
            'compress_response': compress
        }

        if datetime is not None:
            req["time_range"] = [datetime_to_utc(parsedate(d)).isoformat() for d in datetime]

        if asset_bands:
            req['asset_bands'] = asset_bands

        if asset_names:
            warnings.warn('"asset_names" is deprecated, use "asset_bands" instead', DeprecationWarning)
            req['asset_names'] = asset_names

        if band_ids:
            warnings.warn('"band_ids" is deprecated, use "asset_bands" instead', DeprecationWarning)
            req['band_ids'] = band_ids

        if query:
            req['query'] = query

        if filter:
            req['filter'] = filter

        if pixel_size is not None:
            if isinstance(pixel_size, (list, tuple)):
                req['output_pixel_size'] = pixel_size
            elif isinstance(pixel_size, (int, float)):
                req['output_pixel_size'] = (pixel_size, pixel_size)

        if shape is not None:
            req['output_shape'] = shape

        if input_nodata is not None:
            req['input_no_data'] = input_nodata
        if output_nodata is not None:
            req['output_no_data'] = output_nodata,

        res = raise_on_error(boson_client.post(f'raster/{self.name}.{self.project.uid}/warp', **req))

        raw_bytes = res.content
        if compress:
            raw_bytes = zlib.decompress(raw_bytes)

        if content_type == 'raw':
            h = res.headers
            bands = int(h['X-Image-Bands'])
            rows = int(h['X-Image-Rows'])
            cols = int(h['X-Image-Columns'])

            x = np.frombuffer(raw_bytes, dtype=pixel_dtype)
            return x.reshape((bands, rows, cols))
        return raw_bytes

    def share(self, servicer: str, ttl=None) -> Token:
        """
        Shares a dataset, producing a token that will allow unauthenticated users to run a proxied boson request

        Args:
            servicer: The name of the servicer to use in the boson request.
            ttl: The time in seconds until the dataset's token should expire.
                 Defaults to -1 (no expiration) if not provided.

        Raises:
            requests.HTTPError: If the user is not permitted to access the dataset or if an error occurred

        Returns:
            a share token created by Ted and its corresponding data
        """
        name = self.name
        project = self.project.uid

        if ttl is None:
            ttl = -1
        else:
            if isinstance(ttl, int):
                ttl = ttl
            else:
                raise ValueError("ttl must be an integer")

        params = {}
        params['dataset'] = name
        params['servicer'] = servicer
        params['project'] = project
        params['ttl'] = ttl

        res = raise_on_error(ted_client.post('', **params))
        return Token(**res.json())

    @staticmethod
    def from_arcgis_item(
            name: str,
            item_id: str,
            arcgis_instance: str = "https://www.arcgis.com/",
            credential=None,
            layer_id: int = None,
            gis=None) -> 'Dataset':
        """creates a new Dataset from an ArcGIS Online/Enterprise item

        Args:
            name: name of the Dataset to create
            item_id: the item ID of the ArcGIS Item Referenced
            arcgis_instance: the base url of the ArcGIS Online or Enterprise root. Defaults to AGOL, MUST be specified
                             for ArcGIS Enterprise instances
            credential: the name or uid of a credential required to access this. Currently, this must be the
                        client credentials of an ArcGIS OAuth2 Application. Public layers do not require credentials.
            layer_id: an integer layer ID to subset a service's set of layers.
            gis: the logged in `arcgis.gis.GIS` to use to access the metadata for this item. To access secure content,
                 if this is not specified, the active GIS is used.

        Returns:
            a new `Dataset`.

        Examples:
            >>> ds = Dataset.from_arcgis_item(
            ...          name="my-dataset",
            ...          item_id="abc123efghj34234kxlk234joi",
            ...          credential="my-arcgis-creds"
            ... )
            >>> ds.save()
        """

        if arcgis_instance.endswith('/'):
            arcgis_instance = arcgis_instance[:-1]
        url = f'{arcgis_instance}/sharing/rest/content/items/{item_id}?f=pjson'

        if gis is None:
            gis = arcgis.env.active_gis

        js = _get_arcgis_url(url, gis=gis)

        # Get the server metadata for additional info that can be used to construct a initial dataset
        server_metadata = _get_arcgis_url(js['url'], gis=gis)
        try:
            server_metadata = server_metadata.json()
        except Exception:
            server_metadata = {}

        item_assets = {}
        if js['type'] == 'Image Service':
            data_api = 'stac'
            item_type = 'raster'

            _get_esri_band_info(server_metadata, item_assets)
            _get_raster_function_assets(server_metadata, item_assets)

        elif js['type'] == 'Feature Service':
            data_api = 'features'
            item_type = 'other'
        elif js['type'] == 'Map Service':
            data_api = 'features'
            item_type = 'other'
        else:
            raise ValueError(f"unsupported ArcGIS Service Type '{js['type']}'")

        if 'termsofuse' in js.get('licenseInfo'):
            license = "https://goto.arcgis.com/termsofuse/viewtermsofuse"
        else:
            license = '(unknown)'

        spatial_extent = {'bbox': [[-180, -90, 180, 90]]}
        if 'extent' in js:
            (x0, y0), (x1, y1) = js['extent']

            spatial_extent = {'bbox': [[x0, y0, x1, y1]]}

        extent = {
            'spatial': spatial_extent,
            'temporal': {
                'interval': [[None, None]]
            }
        }

        providers = []
        if 'owner' in js:
            providers.append({
                "name": js['owner'],
                "roles": ["processor"],
                "url": arcgis_instance
            })

        c = server_metadata.get('capabilities', [])
        supportsQuery = False
        supportsImage = False
        if 'Catalog' in c or 'Query' in c:
            supportsQuery = True
        if 'Image' in c:
            supportsImage = True

        url = js['url']
        if layer_id is not None:
            url += f'/{layer_id}'

        boson_cfg = BosonConfig(
            provider_name="geoservices",
            url=url,
            thread_safe=True,
            pass_headers=['X-Esri-Authorization'],
            properties={
                "supportsQuery": supportsQuery,
                "supportsImage": supportsImage,
            }
        )

        alias = js.get('title', name)
        keywords = js.get('tags', [])

        description = js.get('description')
        if description is None:
            description = js.get('snippet', '')

        credentials = {}
        if credential is not None:
            credentials = {
                DEFAULT_CREDENTIAL_KEY: credential
            }

        dataset = boson_dataset(
            name=name,
            alias=alias,
            description=description,
            keywords=keywords,
            license=license,
            data_api=data_api,
            item_type=item_type,
            extent=extent,
            boson_cfg=boson_cfg,
            providers=providers,
            item_assets=item_assets,
            credentials=credentials
        )

        return dataset

    @staticmethod
    def from_arcgis_layer(
            name: str,
            url: str,
            arcgis_instance: str = 'https://www.arcgis.com',
            credential=None,
            gis=None) -> 'Dataset':
        """creates a new Dataset from an ArcGIS Online/Enterprise Service URL

        Args:
            name: name of the Dataset to create
            url: the URL of the Feature, Image, or Map Server. This is the layer url, not the Service url.
                 Only the specified layer will be available to the dataset
            arcgis_instance: the base url of the ArcGIS Online or Enterprise root. Defaults to AGOL, MUST be specified
                             for ArcGIS Enterprise instances
            credential: the name or uid of a credential required to access this. Currently, this must be the
                        client credentials of an ArcGIS OAuth2 Application. Public layers do not require credentials.
            gis: the logged in `arcgis.gis.GIS` to use to access the metadata for this item. To access secure content,
                 if this is not specified, the active GIS is used.

        Returns:
            a new `Dataset`.

        Examples:
            >>> ds = Dataset.from_arcgis_layer(
            ...          name="my-dataset",
            ...          url="https://services9.arcgis.com/ABC/arcgis/rest/services/SomeLayer/FeatureServer/0",
            ...          credential="my-arcgis-creds"
            ... )
            >>> ds.save()
        """

        if url.endswith('/'):
            url = url[:-1]

        layer_id = url.split('/')[-1]
        try:
            layer_id = int(layer_id)
        except ValueError:
            raise ValueError("invalid url, must be of the form https://<host>/.../LayerName/FeatureServer/<layer_id>"
                             f"got {url}")

        url = '/'.join(url.split('/')[:-1])
        return Dataset.from_arcgis_service(
            name=name,
            url=url,
            arcgis_instance=arcgis_instance,
            credential=credential,
            layer_id=layer_id,
            gis=gis
        )

    @staticmethod
    def from_arcgis_service(
            name: str,
            url: str,
            arcgis_instance: str = 'https://www.arcgis.com',
            credential=None,
            layer_id: int = None,
            gis=None) -> 'Dataset':
        """creates a new Dataset from an ArcGIS Online/Enterprise Service URL

        Args:
            name: name of the Dataset to create
            url: the URL of the Feature, Image, or Map Server. This is not the layer url, but the Service url.
                 Layers will be enumerated and all accessible from this dataset.
            arcgis_instance: the base url of the ArcGIS Online or Enterprise root. Defaults to AGOL, MUST be specified
                             for ArcGIS Enterprise instances
            credential: the name or uid of a credential required to access this. Currently, this must be the
                        client credentials of an ArcGIS OAuth2 Application. Public layers do not require credentials.
            layer_id: an integer layer ID to subset a service's set of layers.
            gis: the logged in `arcgis.gis.GIS` to use to access the metadata for this item. To access secure content,
                 if this is not specified, the active GIS is used.

        Returns:
            a new `Dataset`.

        Examples:
            >>> ds = Dataset.from_arcgis_service(
            ...          name="my-dataset",
            ...          url="https://services9.arcgis.com/ABC/arcgis/rest/services/SomeLayer/FeatureServer",
            ...          credential="my-arcgis-creds"
            ... )
            >>> ds.save()
        """

        if url.endswith('/'):
            url = url[:-1]
        if not url.endswith("Server"):
            raise ValueError("url must end with ImageServer, FeatureServer, or MapServer")
        server_metadata = _get_arcgis_url(url, gis=gis)

        # Get the name, if the name doesn't exist, get the serviceItemId and build using from_arcgis_item
        dataset_alias = server_metadata.get('name')
        if dataset_alias is None:
            item_id = server_metadata.get('serviceItemId')
            # No way to find out the alias/human readable name, so set to the provided dataset name
            if item_id is None:
                dataset_alias = name
            else:
                return Dataset.from_arcgis_item(
                    name=name,
                    item_id=item_id,
                    arcgis_instance=arcgis_instance,
                    credential=credential,
                    layer_id=layer_id,
                    gis=gis)

        item_assets = {}

        if layer_id is not None:
            layer_id += f'/{layer_id}'

        if 'ImageServer' in url:
            data_api = 'stac'
            item_type = 'raster'

            _get_esri_band_info(server_metadata, item_assets)
            _get_raster_function_assets(server_metadata, item_assets)

        elif 'FeatureServer' in url:
            data_api = 'features'
            item_type = 'other'
        elif 'MapServer' in url:
            data_api = 'features'
            item_type = 'other'
        else:
            raise ValueError("unsupported service type")

        license = '(unknown)'

        spatial_extent = {'bbox': [[-180, -90, 180, 90]]}

        e = {}
        if 'extent' in server_metadata:
            e = server_metadata['extent']
        elif 'fullExtent' in server_metadata:
            e = server_metadata['fullExtent']

        x0 = e.get('xmin', -180.0)
        y0 = e.get('ymin', -90.0)
        x1 = e.get('xmax', 180.0)
        y1 = e.get('ymax', 90.0)

        sr = e.get('spatialReference', {})
        wkid = sr.get('latestWkid', sr.get('wkid', 4326))

        if wkid != 4326:
            p0 = pyproj.Proj(f'epsg:{wkid}', preserve_units=True)
            p1 = pyproj.Proj('epsg:4326', preserve_units=True)
            t = pyproj.Transformer.from_proj(p0, p1, always_xy=True)
            lo0, la0 = t.transform(x0, y0)
            lo1, la1 = t.transform(x1, y1)

        else:
            lo0, la0, lo1, la1 = x0, y0, x1, y1

        spatial_extent = {'bbox': [[lo0, la0, lo1, la1]]}

        extent = {
            'spatial': spatial_extent,
            'temporal': {
                'interval': [[None, None]]
            }
        }

        c = server_metadata['capabilities']
        supportsQuery = False
        supportsImage = False
        if 'Catalog' in c or 'Query' in c:
            supportsQuery = True
        if 'Image' in c:
            supportsImage = True

        boson_cfg = BosonConfig(
            provider_name="geoservices",
            url=url,
            thread_safe=True,
            pass_headers=['X-Esri-Authorization'],
            properties={
                "supportsQuery": supportsQuery,
                "supportsImage": supportsImage,
            }
        )

        credentials = {}
        if credential is not None:
            credentials = {
                DEFAULT_CREDENTIAL_KEY: credential
            }

        dataset = boson_dataset(
            name=name,
            alias=server_metadata.get('name', name),
            description=server_metadata.get('description', ''),
            keywords=[],
            license=license,
            data_api=data_api,
            item_type=item_type,
            extent=extent,
            boson_cfg=boson_cfg,
            item_assets=item_assets,
            credentials=credentials
        )

        return dataset

    @staticmethod
    def from_stac_collection(
            name: str,
            url: str,
            credential=None,
            item_type: str = 'raster',
            provider_name='geodesic') -> 'Dataset':
        """Create a new Dataset from a STAC Collection

        Args:
            name: name of the Dataset to create
            url: the url to the collection (either STAC API or OGC API: Features)
            credential: name or uid of the credential to access the API
            item_type: what type of items does this contain? "raster" for raster data, "features" for features, other
                       types, such as point_cloud may be specified, but doesn't alter current internal functionality.
            provider_name: the name of the Boson provider. Default is "geodesic", which exposes some basic raster
                           functionality. Current other option is "stac"

        Returns:
            a new `Dataset`.

        Examples:
            >>> ds = Dataset.from_stac_collection(
            ...          name="landsat-c2l2alb-sr-usgs",
            ...          url="https://landsatlook.usgs.gov/stac-server/collections/landsat-c2l2alb-sr"
            ...)
            >>> ds.save()
        """

        if provider_name not in ['stac', 'geodesic']:
            raise ValueError("provider_name must be either 'stac' or 'geodesic'")

        if url.endswith('/'):
            url = url[:-1]

        if 'collections' not in url:
            raise ValueError("url must be of the form {STAC_ROOT}/collections/:collectionId")

        rs = stac_root_re.match(url)

        try:
            root = rs.group(1)
        except Exception:
            raise ValueError("invalid URL")

        res = get_client().get(url)

        try:
            stac_collection = res.json()
        except Exception:
            raise ValueError("unable to get service metadata. (did you enter the correct url?)")

        stac_extent = stac_collection.get('extent', {})
        spatial_extent = stac_extent.get('spatial', {})
        bbox = spatial_extent.get('bbox', [[-180.0, -90.0, 180.0, 90.0]])
        temporal_extent = stac_extent.get('temporal', {})
        interval = temporal_extent.get('interval', [
            [
                None,
                None
            ]
        ])

        extent = {
            'spatial': {'bbox': bbox},
            'temporal': {'interval': interval},
        }

        if interval[0][1] is None:
            interval[0][1] = pydatetime.datetime(2040, 1, 1).strftime("%Y-%m-%dT%H:%M:%SZ")

        item_assets = stac_collection.get('item_assets', {})

        links = stac_collection.get('links', [])
        extensions = stac_collection.get('stac_extensions', [])
        providers = stac_collection.get('providers', [])

        keywords = stac_collection.get('keywords', [])
        keywords += ['boson']

        boson_cfg = BosonConfig(
            provider_name=provider_name,
            url=root,
            thread_safe=True,
            pass_headers=[],
            properties={
                "collection": stac_collection['id']
            }
        )

        data_api = 'stac'

        credentials = {}
        if credential is not None:
            credentials = {
                DEFAULT_CREDENTIAL_KEY: credential
            }

        dataset = boson_dataset(
            name=name,
            alias=stac_collection.get('title', name),
            description=stac_collection.get('description', ''),
            keywords=keywords,
            license=stac_collection.get('license', ''),
            data_api=data_api,
            item_type=item_type,
            extent=extent,
            boson_cfg=boson_cfg,
            providers=providers,
            links=links,
            item_assets=item_assets,
            stac_extensions=extensions,
            credentials=credentials
        )

        return dataset

    @staticmethod
    def from_bucket(
            name: str,
            url: str,
            pattern: str = None,
            region: str = None,
            datetime_field: str = None,
            start_datetime_field: str = None,
            end_datetime_field: str = None,
            oriented: bool = False,
            credential: str = None,
            **kwargs) -> 'Dataset':
        """Creates a new Dataset from a Cloud Storage Bucket (S3/GCP/Azure)

        Args:
            name: name of the Dataset to create
            url: the url to the bucket, including the prefix (ex. s3://my-bucket/myprefix, gs://my-bucket/myprefix, ...)
            pattern: a regex to filter for files to index
            region: for S3 buckets, the region where the bucket is
            datetime_field: the name of the metadata key on the file to find a timestamp
            start_datetime_field: the name of the metadata key on the file to find a start timestamp
            end_datetime_field: the name of the metadata key on the file to find an end timestamp
            oriented: Is this oriented imagery? If so, EXIF data will be parsed for geolocation. Anything missing
                      location info will be dropped.
            credential: the name or uid of the credential to access the bucket.
            kwargs: other metadata that will be set on the Dataset, such as description, alias, etc

        Returns:
            a new `Dataset`.

        Examples:
            >>> ds = Dataset.from_bucket(
            ...          name="bucket-dataset",
            ...          url="s3://my-bucket/myprefix",
            ...          pattern=r".*\\.tif",
            ...          region="us-west-2",
            ...          datetime_field="TIFFTAG_DATETIME",
            ...          oriented=False,
            ...          credential="my-iam-user",
            ...          description="my dataset is the bomb"
            ...)
            >>> ds.save()

        """

        info = {
            'name': name,
            'alias': kwargs.get('alias', name),
            'description': kwargs.get('description', '(no description)'),
            'keywords': kwargs.get('keywords', []),
            'license': kwargs.get('license', 'unknown'),
            'data_api': kwargs.get('data_api', 'stac'),
            'item_type': kwargs.get('item_type', 'raster'),
            'extent': kwargs.get('extent', {
                "spatial": {
                    "bbox": [[-180.0, -90.0, 180.0, 90.0]]
                },
                "temporal": {
                    "interval": [[None, None]]
                }
            }),
            'providers': kwargs.get('providers', []),
            'item_assets': kwargs.get('item_assets', {}),
            'links': kwargs.get('links', []),
            'stac_extensions': kwargs.get('stac_extensions', ['item_assets']),
            'credentials': {
                DEFAULT_CREDENTIAL_KEY: credential
            }
        }

        if pattern is not None:
            try:
                re.compile(pattern)
            except Exception:
                raise ValueError(f"invalid pattern '{pattern}'")

        properties = {
            'alias': info['alias'],
            'description': info['description']
        }
        if pattern is not None:
            properties['pattern'] = pattern
        if datetime_field is not None:
            properties['datetime_field'] = datetime_field
        if start_datetime_field is not None:
            properties['start_datetime_field'] = start_datetime_field
        if end_datetime_field is not None:
            properties['end_datetime_field'] = end_datetime_field
        if region is not None:
            properties['region'] = region

        boson_cfg = BosonConfig(
            provider_name="bucket",
            url=url,
            properties=properties,
            thread_safe=True,
            max_page_size=500
        )

        return boson_dataset(boson_cfg=boson_cfg, **info)

    @staticmethod
    def from_google_earth_engine(
            name: str,
            asset: str,
            credential: str,
            folder: str = 'projects/earthengine-public/assets',
            url: str = 'https://earthengine-highvolume.googleapis.com',
            **kwargs) -> 'Dataset':
        """Creates a new Dataset from a Google Earth Engine Asset

        Args:
            name: name of the Dataset to create
            asset: the asset in GEE to use (ex. 'LANDSAT/LC09/C02/T1_L2')
            credential: the credential to access this, a Google Earth Engine GCP Service Account. Future will allow
                        the use of a oauth2 refresh token or other.
            folder: by default this is the earth engine public, but you can specify another folder if needed to point
                    to legacy data or personal projects.
            url: the GEE url to use, defaults to the recommended high volume endpoint.
            kwargs: other metadata that will be set on the Dataset, such as description, alias, etc

        Returns:
            a new `Dataset`.

        Examples:
            >>> ds = Dataset.from_google_earth_engine(
            ...          name="landsat-9-c2-gee",
            ...          asset="s3://my-bucket/myprefixLANDSAT/LC09/C02/T1_L2",
            ...          credential="google-earth-engine-svc-account",
            ...          description="my dataset is the bomb"
            ...)
            >>> ds.save()

        """

        item_assets = {
            "image": Asset(
                title="image",
                description="image data for this dataset"
            )
        }

        info = {
            'name': name,
            'alias': kwargs.get('alias', name),
            'description': kwargs.get('description', '(no description)'),
            'keywords': kwargs.get('keywords', []),
            'license': 'https://earthengine.google.com/terms/',
            'data_api': kwargs.get('data_api', 'stac'),
            'item_type': kwargs.get('item_type', 'raster'),
            'extent': kwargs.get('extent', {
                "spatial": {
                    "bbox": [[-180.0, -90.0, 180.0, 90.0]]
                },
                "temporal": {
                    "interval": [[None, None]]
                }
            }),
            'providers': kwargs.get('providers', [{
                'name': 'Google',
                'description': "Google provides Earth Engine for Google Earth Engine combines a multi-petabyte "
                               "catalog of satellite imagery and geospatial datasets with planetary-scale analysis "
                               "capabilities. Scientists, researchers, and developers use Earth Engine to detect "
                               "changes, map trends, and quantify differences on the Earth's surface. Earth Engine "
                               "is now available for commercial use, and remains free for acadecmic and research use.",
                'url': 'https://earthengine.google.com/',
                'roles': [
                    "host",
                    "processor",
                    "producer",
                    "licensor"
                ]
            }]),
            'item_assets': kwargs.get('item_assets', item_assets),
            'links': kwargs.get('links', []),
            'stac_extensions': kwargs.get('stac_extensions', ['item_assets']),
            'credentials': {
                DEFAULT_CREDENTIAL_KEY: credential
            }
        }

        try:
            if not ee.data._credentials:
                ee.Initialize()
            _parse_earth_engine_data(asset, info, **kwargs)
        except ImportError:
            pass

        boson_cfg = BosonConfig(
            provider_name="google-earth-engine",
            url=url,
            thread_safe=True,
            max_page_size=500,
            properties={
                'asset': asset,
                'folder': folder
            }
        )

        return boson_dataset(boson_cfg=boson_cfg, **info)


def _parse_earth_engine_data(asset: str, info: dict, **kwargs):
    gee_info = {}
    try:
        item = ee.ImageCollection(asset).limit(1)
        gee_info = item.getInfo()
    except Exception:
        item = ee.FeatureCollection(asset).limit(1)
        gee_info = item.getInfo()

    gee_type = gee_info.get('type')

    if gee_type is None:
        return

    properties = gee_info.get('properties', {})
    if properties.get('description') is not None and kwargs.get('description') is None:
        info['description'] = properties.get('description')

    features = gee_info.get('features', [])
    if len(features) == 0:
        return

    feature = features[0]
    item_assets = {}
    if gee_type == 'ImageCollection':
        bands = feature['bands']
        for band in bands:
            asset_name = band['id']
            item_assets[asset_name] = Asset(
                title=asset_name,
                type="image/tiff; application=geotiff"
            )

        item_assets["image"] = Asset(
            title="image",
            description="image data for this dataset",
            type="image/tiff; application=geotiff"
        )
        info['item_assets'] = item_assets


def boson_dataset(*,
                  name: str,
                  alias: str,
                  description: str,
                  keywords: List[str],
                  license: str,
                  data_api: str,
                  item_type: str,
                  extent: dict,
                  boson_cfg: 'BosonConfig',
                  providers: list = [],
                  item_assets: dict = {},
                  links: list = [],
                  stac_extensions: list = [],
                  credentials={}) -> Dataset:

    boson_cfg.credentials = credentials

    dataset = Dataset(
        name=name,
        alias=alias,
        description=description,
        keywords=keywords,
        license=license,
        data_api=data_api,
        item_type=item_type,
        extent=extent,
        boson_config=boson_cfg,
        providers=providers,
        item_assets=item_assets,
        links=links,
        stac_extensions=stac_extensions,
        version="v0.0.1",
        created=pydatetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        updated=pydatetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        services=["boson"],
        object_class="dataset",
        domain="*",
        category="*",
        type="*",
        project=get_active_project().uid
    )

    return dataset


def parsedate(dt):
    try:
        return parse(dt)
    except TypeError:
        return dt


class DatasetList(_APIObject):
    def __init__(self, datasets, ids=[]):

        self.ids = ids
        if len(ids) != len(datasets):
            self.ids = [dataset.name for dataset in datasets]
        for dataset in datasets:
            self._set_item(dataset.name, dataset)

    def __getitem__(self, k) -> Dataset:
        if isinstance(k, str):
            return super().__getitem__(k)
        elif isinstance(k, int):
            did = self.ids[k]
            return super().__getitem__(did)
        else:
            raise KeyError("invalid key")

    def _ipython_display_(self, **kwargs):
        return object_widget.ObjectWidget(self)._ipython_display_(**kwargs)


class ItemAssets(dict):
    def __init__(self, item_assets=None, ds_name=None):
        self.update(item_assets)
        self._ds_name = ds_name

    def _ipython_display_(self, **kwargs):
        return item_assets_widget.ItemAssetsWidget(self)._ipython_display_(**kwargs)


class _DatasetDescr(_BaseDescr):
    """A geodesic Dataset descriptor

    Returns a Dataset object, sets the Dataset name on the base object. Dataset
    MUST exist in Entanglement, in a user accessible project/graph.

    """

    def __init__(self, project=None, **kwargs):
        super().__init__(**kwargs)
        self.project = project

    def _get(self, obj: object, objtype=None) -> dict:
        # Try to get the private attribute by name (e.g. '_dataset')
        return getattr(obj, self.private_name, None)

    def _set(self, obj: object, value: object) -> None:
        dataset = self.get_dataset(value)

        # Reset the private attribute (e.g. "_dataset") to None
        setattr(obj, self.private_name, dataset)

        if self.project is not None:
            self.project.__set__(obj, dataset.project)

        self._set_object(obj, dataset.name)

    def get_dataset(self, value, refresh=False):
        # If the Dataset was set, we need to validate that it exists and the user has access
        dataset_name = None
        if isinstance(value, str):
            dataset_name = value
            project = get_active_project().uid
        else:
            dataset = Dataset(**value)
            dataset_name = dataset.name
            project = dataset.project.uid

        try:
            return get_dataset(dataset_name, project=project, refresh=refresh)
        except Exception:
            # Try to get from 'global'
            try:
                return get_dataset(dataset_name, project='global', refresh=refresh)
            except Exception as e:
                projects = set([project, 'global'])
                raise ValueError(f"dataset '{dataset_name}' does not exist in ({', '.join(projects)}) or"
                                 " user doesn't have access") from e

    def _validate(self, obj: object, value: object) -> None:
        if not isinstance(value, (Dataset, str, dict)):
            raise ValueError(f"'{self.public_name}' must be a Dataset or a string (name)")

        # If the Dataset was set, we need to validate that it exists and the user has access
        self.get_dataset(value, refresh=True)


def _get_esri_band_info(server_metadata: dict, item_assets: dict):

    eo_bands = []
    for band_name in server_metadata.get('bandNames', []):
        eo_bands.append({
            "name": band_name,
            "description": "an image service band",
        })

    asset = Asset(**{
        "title": "image",
        "type": "application/octet-stream",
        "description": "image data for this image service",
        "roles": ["dataset"]
    })
    if len(eo_bands) > 0:
        asset["eo:bands"] = eo_bands

    item_assets["image"] = asset


def _get_raster_function_assets(server_metadata: dict, item_assets: dict):
    for rasterFunctionInfo in server_metadata.get('rasterFunctionInfos', []):
        name = rasterFunctionInfo.get('name', 'None')
        if name != 'None':
            description = rasterFunctionInfo.get('description', '')
            item_assets[name] = Asset(**{
                "title": name,
                "type": "application/octet-stream",
                "description": description,
                "roles": ["dataset"]
            })


def _get_arcgis_url(url: str, gis: 'arcgis.GIS' = None) -> dict:

    js = {}

    if gis is None:
        try:
            gis = arcgis.env.active_gis
        except Exception:
            pass
        else:
            gis = arcgis.GIS()

    # no GIS provided, use the geodesic client
    if gis is None:
        res = get_client().get(url, f='pjson')
        try:
            js = raise_on_error(res).json()
        except Exception:
            raise ValueError("unable to get item info. (did you enter the correct arcgis_instance?)")
    else:
        try:
            js = gis._con.get(url)
        except Exception as e:
            raise ValueError("unable to get item info, ensure you are logged into ArcGIS through"
                             " the ArcGIS API for Python") from e

    return js
