import re
import datetime
from typing import List, Union
import warnings
from dateutil.parser import isoparse
import numpy as np
from geodesic.account.projects import _ProjectDescr
from geodesic.bases import _APIObject
from geodesic.descriptors import _BoolDescr, _DTypeDescr, _DatetimeDescr, _DatetimeIntervalDescr, _DictDescr, \
    _FloatDescr, _IntDescr, _ListDescr, _NumberDescr, _RegexDescr, _StringDescr, _TupleDescr, _TypeConstrainedDescr, \
    _BaseDescr, _URLDescr
from geodesic.entanglement.dataset import Dataset, _DatasetDescr, _valid_resampling
from geodesic.stac import Item, Feature
from geodesic.utils import datetime_to_utc

__all__ = [
    "GlobalProperties",
    "AssetSpec",
    "Container",
    "Step",
    "StepInput",
    "StepOutput",
    "Webhook",
    "Bucket",
    "Equal",
    "User",
    "TemporalBinning",
    "StridedBinning",
    "OutputBand",
    "OutputTimeBins",
    "ReduceMethod",
    "NearestSelection",
    "RangeSelection",
    "BinSelection",
    "TimeBinSelection"
]


resample_options = _valid_resampling + [s.upper() for s in _valid_resampling]
bin_size_re = re.compile(r'^\d+(ms|us|ns|[YMWDhms]){1}')


class Equal(_APIObject):
    """Temporal binning with equal bin size (either by count or size)
    """
    bin_size = _RegexDescr(bin_size_re, doc="the bin size, in time units for each bin")
    bin_count = _IntDescr(doc="the count of bins to create")


class User(_APIObject):
    """Temporal binning by user specified bins.
    """
    omit_empty = _BoolDescr(doc="don't create a space for empty bins in resulting output")

    def __init__(self, **spec):
        self.omit_empty = False
        self._bins = None
        super().__init__(**spec)

    @property
    def bins(self):

        if self._bins is not None:
            return self._bins
        b = self.get('bins', [])
        if not isinstance(b, list):
            raise ValueError("bins must be a list of list of datetimes")
        out = []
        for d in b:
            if d is None:
                raise ValueError("bin cannot be None")
            dates = d
            try:
                out.append([d for d in map(isoparse, dates)])
            except Exception as e:
                raise e
        self._bins = out
        return out

    @bins.setter
    def bins(self, v: List[List[Union[datetime.datetime, str]]]):
        b = []
        for d in v:
            if len(d) != 2:
                raise ValueError("bins must be a list of pairs of start/end datetime bin edges")

            if isinstance(d[0], str):
                for dt in d:
                    try:
                        isoparse(dt)
                    except Exception as e:
                        raise ValueError("bin edges must be datetimes or parsable rfc3339 strings") from e
                b.append(list(d))

            elif isinstance(d[0], datetime.datetime):
                b.append([datetime_to_utc(dt).isoformat() for dt in d])
        self._set_item('bins', b)


class TemporalBinning(_APIObject):
    """Temporal binning is a class to represent the temporal binning in a series request.

    Args:
        spec(dict): The dict to initialize the class with.
    """
    equal = _TypeConstrainedDescr((Equal, dict), doc="specify Equal time binning")
    user = _TypeConstrainedDescr((User, dict), doc="specify time bins defined by User time binning")
    reference = _StringDescr(doc="reference the time bins to another asset in the Job")


class Webhook(_APIObject):
    """A webhook triggered on completion of a step in a Tesseract Job

    NotImplemented

    A future version of Tesseract will allow webhooks when a job step has completed, which will POST
    information to a url with specified headers and credentials
    """

    url = _URLDescr(doc="url")
    headers = _DictDescr(doc="dictionary with string keys to string values headers to pass along: {'key': 'value'}")
    credentials = _StringDescr(doc="name of the credential to use (geodesic.accounts.Credential)")


class Container(_APIObject):
    """A container that runs arbitrary code to execute a model for aggregation, machine learning, etc

    NotImplemented

    """
    repository = _StringDescr(doc="the docker repository to pull from", default="docker.io")
    image = _StringDescr(doc="the name of the image to use")
    tag = _StringDescr(doc="the tag of the image to use")
    pull_secret_credential = _StringDescr(doc="name of the credential to use to pull the container")
    args = _DictDescr(doc="additional arguments to pass to the inference function (NOT IMPLEMENTED)")


class BinSelection(_APIObject):
    """Selection of a time bin based on a datetime or index
    """
    # reference asset - which time bins it'll draw from (StepOutput only)
    reference_asset = _StringDescr(doc="which asset to reference the time bins. For step outputs")

    datetime = _DatetimeDescr(doc="datetime to use for selection")
    index = _IntDescr(doc="datetime to use for selection")


class StridedBinning(_APIObject):
    """Create output time bins based on a from, duration, stride, offset, and count
    """
    from_selection = _TypeConstrainedDescr((BinSelection, dict), coerce=True, dict_name="from", doc="from where the"
                                           " bins begin. Either an index or a datetime")
    from_end = _BoolDescr(doc="use the right end of the bin if True")
    duration = _RegexDescr(bin_size_re, doc="the bin size, in time units for each bin")
    stride = _RegexDescr(bin_size_re, doc="the stride (step forward), in time units between each bin")
    count = _IntDescr(doc="how many bins")
    offset = _RegexDescr(bin_size_re, doc="the offset from the first date to start the bins")

    def __init__(self,
                 from_selection=BinSelection(),
                 from_end=False,
                 duration=None,
                 stride=None,
                 count=None,
                 offset=None):

        self.from_selection = from_selection
        self.from_end = from_end
        self.duration = duration
        self.stride = stride
        if offset is None:
            offset = stride
        self.offset = offset
        self.count = count


class RangeSelection(_APIObject):
    """Selection of bins between a start and an end
    """
    from_index = _IntDescr(dict_name="from", doc="starting point of bin selection in a range")
    to_index = _IntDescr(dict_name="to", doc="ending point of bin selection in a range")

    def __init__(self, from_index=None, to_index=None):
        self.from_index = from_index
        self.to_index = to_index


class NearestSelection(_APIObject):
    """Selection of the nearest bin to a specified before/after point
    """
    before = _DatetimeDescr(doc="select the nearest bin BEFORE this value")
    after = _DatetimeDescr(doc="select the nearest bin AFTER this value")


class ReduceMethod(_APIObject):
    """Reduce along time bin dimension into a single bin
    """
    op = _StringDescr(one_of=['min', 'max', 'mean', 'sum', 'first', 'last'], doc="reduction operation on time bins")


class TimeBinSelection(_APIObject):
    """A description of which time bins to select from the input
    """
    # Only one of the following can be set
    all = _BoolDescr(doc="select all time bins from input")
    index = _IntDescr(doc="the index of the time bin to select")
    since = _TypeConstrainedDescr((BinSelection, dict), coerce=True, doc="select all bins since this selection")
    until = _TypeConstrainedDescr((BinSelection, dict), coerce=True, doc="select all bins before this selection")
    range = _TypeConstrainedDescr((RangeSelection, dict), coerce=True, doc="selection all bins in a range")
    nearest = _TypeConstrainedDescr((NearestSelection, dict), coerce=True, doc="select the nearest time bin")

    # Reduce along time dimension with this operation
    reduce = _TypeConstrainedDescr((ReduceMethod, dict), coerce=True, doc="reduce along time dimension before sending"
                                   " to model. This will send a single time bin (NOT IMPLEMENTED)")


class OutputBand(_APIObject):
    """An output bin, either a name or STAC eo band
    """
    band_name = _StringDescr(doc="the name of the bin")
    eo_band = _DictDescr(doc="an eo:band object of information about this band")


class OutputTimeBins(_APIObject):
    """How to define what the output time bins are for a step output
    """
    nontemporal = _BoolDescr(doc="nontemporal; there will only be one single bin created")
    user = _TypeConstrainedDescr((User, dict), coerce=True, doc="user defined bin edges")
    strided = _TypeConstrainedDescr((StridedBinning, dict), coerce=True, doc="build bins by defining a from, duration,"
                                    " stride, offset, and count")
    equal = _TypeConstrainedDescr((Equal, dict), coerce=True, doc="equal sized bins between the start and end datetime")


class AssetBands(_APIObject):
    """Specify and asset from a dataset as well as a list of bands
    """
    asset = _StringDescr(doc="asset name to reference from the dataset")
    bands = _ListDescr(item_type=(str, int), doc="a list of band indices (0-indexed) or band names to reference")


class FeatureAggregation(_APIObject):
    """FeatureAggregation specifies how features should be handled while rasterizing
    """
    value = _TypeConstrainedDescr((str, float, int, complex))
    aggregation_rules = _ListDescr(item_type=str)
    groups = _ListDescr(item_type=dict)


class WarpOptions(_APIObject):
    shape = _TupleDescr(doc="the shape of the output for this asset (rows, columns)", min_len=2, max_len=2)
    pixel_size = _TupleDescr(doc="the size of each pixel in the output SRS (x, y)", min_len=2, max_len=2)
    resample = _StringDescr(
        one_of=resample_options,
        doc=f"resampling method to use, one of {', '.join(resample_options)}")
    defer_search = _BoolDescr(doc="if set to True, Tesseract won't check if the data exists at this tile and instead"
                              " use Boson directly to obtain the pixel data. (default: False")
    order_by = _StringDescr(doc="order by a field in the inputs because mosaicing/reducing the outputs")
    reduce = _TypeConstrainedDescr((ReduceMethod, dict), doc="if multiple images are used for input, `reduce` specifies"
                                                             " how to aggregate. If this is empty, all are mosaiced in"
                                                             " order.")


class RasterizeOptions(_APIObject):
    shape = _TupleDescr(doc="the shape of the output for this asset (rows, columns)", min_len=2, max_len=2)
    pixel_size = _TupleDescr(doc="the size of each pixel in the output SRS (x, y)", min_len=2, max_len=2)
    value = _TypeConstrainedDescr((str, float, int, complex))
    aggregation_rules = _ListDescr(item_type=str)
    groups = _ListDescr(item_type=dict)
    defer_search = _BoolDescr(doc="if set to True, Tesseract won't check if the data exists at this tile and instead"
                              " use Boson directly to obtain the feature data to rasterize. (default: False")


class StepInput(_APIObject):
    """An input for a processing step
    """
    asset_name = _StringDescr(doc="name of the asset from a previous `StepOutput` to use as input for this `Step`")
    spatial_chunk_shape = _TupleDescr(doc="the shape of each chunk of input for this step in row/column space")
    type = _RegexDescr(r"((?:tensor)|(?:features)|(?:records))", doc="the type of input")
    overlap = _IntDescr(doc="number of pixels of overlap to apply when tiling the inputs")
    bands = _ListDescr(item_type=(int, float), coerce_items=True, doc="band index/ID of the bands to select from input")
    time_bin_selection = _TypeConstrainedDescr((TimeBinSelection, dict), coerce=True, doc="which time bins should be"
                                               " selected from the input")
    asset_bands = _ListDescr(item_type=(AssetBands, dict), coerce_items=True, doc="a list of `AssetBand` objects")
    dataset_project = _ProjectDescr(doc="the project that the step's input belongs to. This will be set automatically"
                                    " when setting the dataset")
    dataset = _DatasetDescr(project=dataset_project, doc="the Dataset that will be used in this step. This may only be"
                            " only used if `asset_name` is empty.")
    no_data = _ListDescr(
        item_type=(int, float, complex, str),
        doc="set the value to be ignored and treated as no data in the output")
    ids = _ListDescr(item_type=(int, str), doc="list of item IDs to be used to query from the specified dataset")
    datetime = _DatetimeIntervalDescr(doc="the datetime interval to be used to query for matching data")
    filter = _DictDescr(doc="a dictionary representing a JSON CQL2 filter as defined by the OGC spec: "
                        "https://github.com/opengeospatial/ogcapi-features/tree/master/cql2")
    stac_items = _ListDescr(item_type=(dict, Feature, Item), doc="a list of OGC/STAC features/items to use in lieu"
                            " of a query", dict_name='items')


class StepOutput(_APIObject):
    """An output for a processing step
    """
    asset_name = _StringDescr(doc="name of an asset this step emits")
    type = _RegexDescr(r"((?:tensor)|(?:features)|(?:records))", doc="the type of output")
    chunk_shape = _TupleDescr(
        doc="the shape of the output from this asset from the container. Even if the container performs a reduction, "
            "please specify the full dimensions in the order (time, band/feature, rows, columns). (1, 1, 1, 1) for "
            " scaler output",
        min_len=4,
        max_len=4)
    pixel_dtype = _DTypeDescr(doc="the dtype of this ouptut asset")
    fill_value = _TypeConstrainedDescr((int, float, str, complex), doc="the fill value for this output asset")
    trim = _IntDescr(doc="the number of border pixels to remove from output of the model. This typically"
                     " should match the overlap in the step input, but for cases like models that upsample"
                     " (e.g. superresolution), this should trim off a different value.")
    output_time_bins = _TypeConstrainedDescr((OutputTimeBins, dict), coerce=True,
                                             doc="how to generate output time bins")
    output_bands = _ListDescr(item_type=(OutputBand, dict), coerce_items=True, doc="band names or STAC eo:band objects")
    compression = _StringDescr(one_of=['zlib', 'blosc', 'none'], doc="the compression algorithm for output data")
    chip_size = _IntDescr(default=512, doc="size of the chips to break work into (default=512, max=2048)")
    warp_options = _TypeConstrainedDescr((WarpOptions, dict), coerce=True, doc="options that will be used to"
                                         " warp/reproject/resample a raster dataset into a specific grid/spatial"
                                         " reference before processing. If you are working with raster data from an"
                                         " input `Dataset`, this must be specified")
    rasterize_options = _TypeConstrainedDescr((RasterizeOptions, dict), coerce=True, doc="options that will be used to"
                                              " rasterize a vector dataset into a specific grid/spatial"
                                              " reference before processing. If you are working with feature data from"
                                              " an input `Dataset`, this must be specified")


class Step(_APIObject):
    """A step in a Tesseract Job

    NotImplemented

    """
    name = _StringDescr(doc="the name of this step")
    type = _StringDescr(doc="the type of this step (model, rechunk)")
    inputs = _ListDescr(item_type=(StepInput, dict), doc="a list of inputs for this step", coerce_items=True)
    outputs = _ListDescr(item_type=(StepOutput, dict), doc="a list of outputs for this step", coerce_items=True)
    container = _TypeConstrainedDescr((Container, dict))
    gpu = _BoolDescr(doc="make the step run on a machine with GPU resources", default=False)
    workers = _IntDescr(doc="number of workers to run for this step")


class Bucket(_APIObject):
    url = _StringDescr(doc="a storage URL, (e.g. s3://bucket/prefix or gs://bucket/prefix). If this is specified,"
                       " you do not need to specify prefix, platform, bucket, region, account or domain")
    prefix = _StringDescr(doc="all output will be written to this prefix")
    platform = _StringDescr(doc="the platform for this bucket (aws, gcp, azure)")
    bucket = _StringDescr(doc="name of the bucket or container")
    region = _StringDescr(doc="storage region (AWS)")
    credentials = _StringDescr(doc="credentials to access this bucket")
    account = _StringDescr(doc="the azure storage account name (e.g. storageaccount)")
    domain = _StringDescr(doc="the azure storage domain (e.g. us.core.windows.net)")
    requester_pays = _BoolDescr(doc="requester pays to access bucket", default=False)


class GlobalProperties(_APIObject):
    """GlobalProperties that will be applied to all assets if they have empty values

    Only contains a subset of the parameters for an asset.

    Args:
        **spec(dict): A dictionary that can be used to initialize the object. Optional.
    """

    shape = _TupleDescr(doc="the shape of the output for this asset (rows, columns)", min_len=2, max_len=2)
    pixel_size = _TupleDescr(doc="the size of each pixel in the output SRS (x, y)", min_len=2, max_len=2)
    pixel_dtype = _DTypeDescr(doc="output pixel dtype")
    chip_size = _IntDescr(doc="size of the chips to break work into (default=512, max=2048)")
    project = _ProjectDescr(doc="the project the source dataset belongs to. You must have read access to this project")
    output_no_data = _ListDescr(
        item_type=(int, float, complex),
        doc="set the value to be ignored and treated as nodata in the output")
    compression = _RegexDescr(regex=r'((?:zlib)|(?:blosc)|(?:none))', doc="the compression algorithm for output data")
    datetime = _DatetimeIntervalDescr(doc="the datetime interval to be used to query for matching data")
    temporal_binning = _TypeConstrainedDescr((TemporalBinning, dict), doc="the temporal binning strategy")

    def __init__(self, **spec):
        warnings.warn(
            "GlobalProperties is deprecated and will be removed in 1.0.0. Please explicitly specify parameters in "
            "StepInput/Outputs",
            DeprecationWarning)

        self._compression = None
        self._project = None
        self._datetime = None
        self._output_no_data = None
        self._temporal_binning = None

        for k, v in spec.items():
            setattr(self, k, v)


class AssetSpec(_APIObject):
    """AssetSpec is a class to represent the requested output assets in a tesseract job.

    Args:
        **spec(dict): A dictionary that can be used to initialize the object. Optional.

    """
    name = _StringDescr(doc="name of this asset")
    dataset = _DatasetDescr(doc="the dataset to derive this asset from")
    assets = _ListDescr(item_type=str, doc="the assets within the dataset to use. "
                        "Each will be separate band(s)/feature(s)")
    asset_band_counts = _ListDescr(item_type=(int,), doc="list of band counts for each asset. If empty, Tesseract will"
                                   " infer from the dataset spec or assume it's 1 and return"
                                   " a warning")
    resample = _StringDescr(
        one_of=resample_options,
        doc=f"resampling method to use, one of {', '.join(resample_options)}")
    project = _ProjectDescr(doc="the project the source dataset belongs to. You must have read access to this project")
    shape = _TupleDescr(doc="the shape of the output for this asset (rows, columns)", min_len=2, max_len=2)
    pixel_size = _TupleDescr(doc="the size of each pixel in the output SRS (x, y)", min_len=2, max_len=2)
    pixel_dtype = _DTypeDescr(doc="output pixel dtype")
    chip_size = _IntDescr(doc="size of the chips to break work into (default=512, max=2000)")
    compression = _StringDescr(one_of=['zlib', 'blosc', 'none'], doc="the compression algorithm for output data")
    input_no_data = _ListDescr(
        item_type=(int, float, complex, str),
        doc="set the value to be ignored and treated as nodata in the input")
    output_no_data = _ListDescr(
        item_type=(int, float, complex, str),
        doc="set the value to be ignored and treated as nodata in the output")
    ids = _ListDescr(item_type=(int, str), doc="list of item IDs to be used to query from the specified dataset")
    datetime = _DatetimeIntervalDescr(doc="the datetime interval to be used to query for matching data")
    query = _DictDescr(doc="a dictionary formatted like"
                       "https://github.com/radiantearth/stac-api-spec/"
                       "blob/master/item-search/README.md#query-extension"
                       "to be used to filter input data")
    filter = _DictDescr(doc="a dictionary representing a JSON CQL2 filter as defined by the OGC spec: "
                        "https://github.com/opengeospatial/ogcapi-features/tree/master/cql2")
    feature_aggregation = _TypeConstrainedDescr(
        (FeatureAggregation, dict), doc="how features should be aggregated into a resulting raster see REST API docs"
                                        " for further info: https://docs.seerai.space/tesseract/v1/index.html")
    stac_items = _ListDescr(item_type=(dict, Feature, Item), doc="a list of OGC/STAC features/items to use in lieu"
                            " of a query", dict_name='items')
    as_feature = _BoolDescr(doc="treat items as features (e.g. for Rasterize) instead of STAC items (usually Warp)")
    fill_value = _NumberDescr(doc="anywhere there is no calculated data, will be replaced with this")
    temporal_binning = _TypeConstrainedDescr((TemporalBinning, dict), doc="the temporal binning strategy")
    hooks = _ListDescr(item_type=(Webhook, dict), doc="webhooks to be called when asset is completed")

    def __init__(self, **spec):
        warnings.warn(
            "AssetSpec is deprecated and will be removed in 1.0.0. Please explicitly specify parameters in "
            "StepInput/Outputs",
            DeprecationWarning)

        # Set defaults
        self.resample = 'nearest'
        self.fill_value = 0
        self.pixel_dtype = np.float32
        self.compression = 'blosc'
        self.project = 'global'

        for k, v in spec.items():
            if k == 'items':
                k = 'stac_items'
            setattr(self, k, v)


class AssetSpecListDescr(_BaseDescr):
    """a list of validated AssetSpecs

    AssetSpecListDescr is a list of AssetSpec items, this sets/returns a list no matter what,
    it doesn't raise an attribute error.

    __get__ returns the list, creating it on the base object if necessary
    __set__ sets the list after validating that it is a list
    """

    def _get(self, obj: object, objtype=None) -> list:
        # Try to get the private attribute by name (e.g. '_assets')
        assets = getattr(obj, self.private_name, None)
        if assets is not None:
            # Return it if it exists
            return assets

        try:
            assets = self._get_object(obj)

            isAssetSpec = True
            for asset in assets:
                if not isinstance(asset, AssetSpec):
                    isAssetSpec = False
                    break
            if not isAssetSpec:
                self._set(obj, assets)
                return self._get(obj)

        except KeyError:
            assets = []
            self._set_object(obj, assets)
        setattr(obj, self.private_name, assets)
        return assets

    def _set(self, obj: object, value: object) -> None:
        assets = [
            AssetSpec(**asset) for asset in value
        ]
        setattr(obj, self.private_name, assets)
        self._set_object(obj, assets)

    def _validate(self, obj: object, value: object) -> None:
        if not isinstance(value, (list, tuple)):
            raise ValueError(f"'{self.public_name}' must be a tuple or list")
        if len(value) > 0:
            for asset in value:
                if not isinstance(asset, (dict, AssetSpec)):
                    raise ValueError(f"each value must be a dict/AssetSpec, not '{type(asset)}'")


class Warning(_APIObject):
    title = _StringDescr(doc="short description of the warning")
    detail = _StringDescr(doc="detailed description of the warning")
    severity = _StringDescr(doc="severity of the warning", default='LOW')

    def warn(self):
        warnings.warn(f"{self.title} (severity={self.severity}): {self.detail}")


class JobResponse(_APIObject):
    job_id = _StringDescr(doc="id of the submitted Tesseract Job")
    dataset = _TypeConstrainedDescr((Dataset, dict), doc="the generated dataset from this job", coerce=True)
    item = _TypeConstrainedDescr((Item, Feature, dict), doc="STAC Item for this job's output", coerce=True)
    n_quarks = _IntDescr(doc="nubmer of quarks produced")
    n_steps = _IntDescr(doc="nubmer of steps in this job")
    n_edges = _IntDescr(doc="number of edges in the graph")
    avg_quark_size_bytes = _FloatDescr(doc="average size of a quark, in bytes")
    warnings = _ListDescr(item_type=(Warning, dict),
                          doc="any warnings returned while planning the job", coerce_items=True)

    def warn(self):
        """Shows all warnings that came from this job
        """
        for warning in self.warnings:
            warning.warn()
