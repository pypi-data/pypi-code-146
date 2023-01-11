import logging
from collections import namedtuple
from dataclasses import dataclass, field, fields
from time import monotonic
from typing import Iterable, Iterator, NamedTuple, Optional, Type, Union

from clickhouse_pool import ChPool

from hcube.api.backend import CubeBackend
from hcube.api.exceptions import ConfigurationError
from hcube.api.models.aggregation import (
    Aggregation,
    AggregationOp,
    ArrayAgg,
    Count,
    Sum,
)
from hcube.api.models.cube import Cube
from hcube.api.models.dimensions import (
    ArrayDimension,
    DateDimension,
    DateTimeDimension,
    Dimension,
    IntDimension,
    StringDimension,
)
from hcube.api.models.filters import (
    ComparisonFilter,
    EqualityFilter,
    Filter,
    IsNullFilter,
    ListFilter,
    NegativeListFilter,
    Or,
    OverlapFilter,
    SubstringFilter,
    SubstringMultiValueFilter,
)
from hcube.api.models.materialized_views import AggregatingMaterializedView
from hcube.api.models.metrics import FloatMetric, IntMetric, Metric
from hcube.api.models.query import CubeQuery
from hcube.api.models.transforms import (
    ExplicitMappingTransform,
    StoredMappingTransform,
    Transform,
)
from hcube.backends.clickhouse.dictionaries import DictionaryDefinition
from hcube.backends.clickhouse.indexes import IndexDefinition
from hcube.settings import GlobalSettings

logger = logging.getLogger("hcube.backends.clickhouse")


@dataclass
class TableMetaParams:
    engine: str = "CollapsingMergeTree"
    sign_col: str = "sign"
    primary_key: [str] = field(default_factory=list)
    sorting_key: [str] = field(default_factory=list)
    partition_key: [str] = field(default_factory=list)
    indexes: [IndexDefinition] = field(default_factory=list)
    dictionaries: [DictionaryDefinition] = field(default_factory=list)
    # Using a skip index with FINAL queries may lead to incorrect results in some cases
    # so Clickhouse added a `use_skip_indexes_if_final` setting which is false by default.
    # Here we switch it on to make use of skip indexes as in normal situations it is safe.
    # You can switch it off by using the following meta parameter with a False value.
    use_skip_indexes_if_final: bool = True


class ClickhouseCubeBackend(CubeBackend):

    """
    Backend to Clickhouse using the low-level Clickhouse API from `clickhouse-driver`.
    """

    dimension_type_map = (
        (IntDimension, "Int"),
        (StringDimension, "String"),
        (DateDimension, "Date"),
        (DateTimeDimension, "DateTime64"),
        (FloatMetric, "Float"),
        (IntMetric, "Int"),
    )
    default_settings = {}

    def __init__(
        self,
        database=None,
        query_settings=None,
        **client_attrs,
    ):
        super().__init__()
        self.database = database
        assert self.database, "database must be present"
        self.query_settings = query_settings or {}
        self.client_attrs = client_attrs
        self.pool = ChPool(database=database, **client_attrs)
        self._table_exists = {}

    def initialize_storage(self, cube: Type[Cube]) -> None:
        self._create_table(cube)

    def _create_table(self, cube: Type[Cube]):
        table_name = self.cube_to_table_name(cube)
        if not self._table_exists.get(table_name, False):
            self._init_table(cube)
            self._create_materialized_views(cube)
            self._table_exists[table_name] = True
        self._create_dictionaries(cube)

    def drop_storage(self, cube: Type[Cube]) -> None:
        self._drop_dictionaries(cube)
        self._drop_table(cube)
        self._table_exists.pop(self.cube_to_table_name(cube), None)

    def store_records(self, cube: Type[Cube], records: Iterable[NamedTuple]):
        with self.pool.get_client() as client:
            client.execute(f"USE {self.database}")
            meta = self.get_table_meta(cube)
            clean_records = cube.cleanup_records(records)
            client.execute(
                f"INSERT INTO {self.database}.{self.cube_to_table_name(cube)} VALUES ",
                ({**rec._asdict(), meta.sign_col: 1} for rec in clean_records),
            )

    def get_records(
        self,
        query: CubeQuery,
        info: Optional[dict] = None,
        auto_use_materialized_views: bool = True,
    ) -> Iterator[NamedTuple]:
        """
        If a `dict` is passed to `info`, it will be populated with some debugging info about the
        query
        """
        text, params, fields, matview = self._prepare_db_query(
            query, auto_use_materialized_views=auto_use_materialized_views
        )
        logger.debug('Query: "%s", params: "%s"', text, params)
        result = namedtuple("Result", fields)
        if type(info) is dict:
            info["query_text"] = text
            info["query_params"] = params
            info["used_materialized_view"] = matview
        # we could use execute_iter here, but is breaks the communication if some stuff is left
        # unconsumed "in the wire", so this seems safer
        start = monotonic()
        with self.pool.get_client() as client:
            output = client.execute(text, params)
            logger.debug(f"Query time: {monotonic() - start: .3f} s")
            for rec in output:
                yield result(*rec)

    def get_count(self, query: CubeQuery) -> int:
        text, params, *_ = self._prepare_db_query(query)
        text = f"SELECT COUNT() FROM ({text}) AS _count"
        logger.debug('Query: "%s", params: "%s"', text, params)
        start = monotonic()
        with self.pool.get_client() as client:
            output = client.execute(text, params)
            logger.debug(f"Query time: {monotonic() - start: .3f} s")
            return output[0][0]

    def delete_records(self, query: CubeQuery) -> None:
        """
        In clickhouse we do not delete the records, but rather insert the same records with
        an opposite sign. Clickhouse takes care of the rest.

        The query must not contain any aggregations or group_bys - just filter and limit + ordering
        """
        # check that the query can be used
        if query.aggregations or query.groups or query.transforms:
            raise ConfigurationError(
                "Delete query can only have a filter, no aggregations, group_bys or transforms"
            )

        meta = self.get_table_meta(query.cube)
        table = f"{self.database}.{self.cube_to_table_name(query.cube)}"
        where_parts = []
        params = {}
        for fltr in query.filters:
            filter_text, filter_params = self._ch_filter(fltr)
            where_parts.append(filter_text)
            params.update(filter_params)
        where = " AND ".join(where_parts)

        dims = [dim.name for dim in query.cube._dimensions.values()]
        metrics = [metric.name for metric in query.cube._metrics.values()]
        dim_names = ",".join(dims)
        metric_names = ",".join(metrics)
        metric_names += "," if metric_names else ""
        metric_sums = ",".join(f"sum({metric}*{meta.sign_col}) as {metric}" for metric in metrics)
        metric_sums += "," if metric_sums else ""

        # In a previous version, we simply inserted the records returned by a select with FINAL
        # keyword with the opposite sign. But it turns out that the FINAL keyword has some problems
        # - in newer versions of clickhouse a special setting has to be given to use skip indexes
        # with FINAL and it still has strange performance issues - it seems that skip indexes are
        # not used for FINAL queries by default, this code path is not well tested.
        #
        # This is why we use a different approach which gets around the FINAL keyword by using
        # an aggregation query to get the sums of the metrics and then insert these values with
        # the opposite sign.
        #
        # Please note that we could not just insert plain records with opposite sign without using
        # final, because if there already were records with the -1 sign, we could just duplicate
        # both the positive and negative records. By using the aggregation query, we are sure that
        # only the positive records are negated by inserting records with the opposite sign.

        whole_text = (
            f"INSERT INTO {table} ({dim_names}, {metric_names} {meta.sign_col}) "
            f"SELECT {dim_names}, {metric_sums} -1 "
            f"FROM {table} "
            f"{'WHERE ' + where + ' ' if where else ''}"
            f"GROUP BY {dim_names} "
            f"HAVING SUM({meta.sign_col}) > 0"
        )
        logger.debug("Delete query: %s, params: %s", whole_text, params)
        start = monotonic()
        with self.pool.get_client() as client:
            client.execute(whole_text, params)
            logger.debug(f"Query time: {monotonic() - start: .3f} s")

    def delete_records_hard(self, query: CubeQuery) -> None:
        """
        Clickhouse has a DELETE command, but it is not very efficient. We support it by this extra
        method, but it is not recommended to use it.
        """
        logger.warning("Hard delete is not recommended for Clickhouse, it performs poorly")
        # check that the query can be used
        if query.aggregations or query.groups or query.transforms:
            raise ConfigurationError(
                "Delete query can only have a filter, no aggregations, group_bys or transforms"
            )

        table = f"{self.database}.{self.cube_to_table_name(query.cube)}"
        where_parts = []
        params = {}
        for fltr in query.filters:
            filter_text, filter_params = self._ch_filter(fltr)
            where_parts.append(filter_text)
            params.update(filter_params)
        where = " AND ".join(where_parts)

        # put it together
        text = f"ALTER TABLE {table} DELETE "
        if where:
            text += f"WHERE {where} "

        logger.debug("Delete query: %s, params: %s", text, params)
        start = monotonic()
        with self.pool.get_client() as client:
            client.execute(text, params)
            logger.debug(f"Query time: {monotonic() - start: .3f} s")

    @classmethod
    def get_table_meta(cls, cube: Type[Cube]) -> TableMetaParams:
        meta = TableMetaParams()
        if hasattr(cube, "Clickhouse"):
            for _field in fields(TableMetaParams):
                if hasattr(cube.Clickhouse, _field.name):
                    setattr(meta, _field.name, getattr(cube.Clickhouse, _field.name))
        return meta

    def _prepare_db_query(
        self, query: CubeQuery, auto_use_materialized_views: bool = True, append_to_select=""
    ) -> (str, dict, list, Optional[Type[AggregatingMaterializedView]]):
        """
        returns the query text, parameters to be added during execution and a list of parameter
        names that are expected in the result
        """
        meta = self.get_table_meta(query.cube)
        params = {}
        fields = []
        select_parts = []
        # materialized views - we must deal with it first because it influences the usage of the
        # sign column
        matview = None
        if auto_use_materialized_views:
            matviews = query.possible_materialized_views()
            if matviews:
                matview = matviews[0]
                logger.debug(f"Switching to materialized view: {matview.__name__}")

        # transforms
        for transform in query.transforms:
            _field, _select = self._translate_transform(transform)
            fields.append(_field)
            select_parts.append(_select)

        if query.groups or query.aggregations:
            for grp in query.groups:
                if grp.name not in fields:
                    fields.append(grp.name)
                    select_parts.append(grp.name)
            for agg in query.aggregations:
                select_part, agg_params = self._translate_aggregation(
                    agg, None if matview else meta.sign_col
                )
                params.update(agg_params)
                if agg.name not in fields:
                    # if the aggregation is over a transformed field, it is already in the select
                    # and in the fields set
                    select_parts.append(select_part)
                    fields.append(agg.name)
            final = False
        else:
            for dim in query.cube._dimensions.values():
                fields.append(dim.name)
                select_parts.append(dim.name)
            for metric in query.cube._metrics.values():
                fields.append(metric.name)
                select_parts.append(metric.name)
            final = True  # there are no aggregations, we need to use FINAL

        select = ", ".join(select_parts) + append_to_select
        group_by = ", ".join(grp.name for grp in query.groups)
        table = f"{self.database}.{self.cube_to_table_name(matview if matview else query.cube)}"
        # ordering
        order_by = ", ".join(f"{ob.dimension.name} {ob.direction.name}" for ob in query.orderings)
        where_parts = []
        for fltr in query.filters:
            filter_text, filter_params = self._ch_filter(fltr)
            where_parts.append(filter_text)
            params.update(filter_params)
        where = " AND ".join(where_parts)
        final_part = "FINAL" if final else ""

        # put it together
        text = f"SELECT {select} FROM {table} {final_part} "
        if where:
            text += f"WHERE {where} "
        if group_by:
            text += f"GROUP BY {group_by} "
            if not matview:
                # if materialized view is not used, we also add the following filter to
                # remove results where all the records were already removed
                text += f"HAVING SUM({meta.sign_col}) > 0 "
        if order_by:
            text += f"ORDER BY {order_by} "
        if query.limit:
            text += f"LIMIT {query.limit} "
        # get suitable settings for the query
        applied_settings = self._get_query_settings()
        if final and meta.use_skip_indexes_if_final:
            applied_settings["use_skip_indexes_if_final"] = 1
        settings_part = ", ".join(f"{k} = {v}" for k, v in applied_settings.items())
        if settings_part:
            text += f" SETTINGS {settings_part}"
        return text, params, fields, matview

    def _get_query_settings(self) -> dict:
        return {**self.default_settings, **self.query_settings}

    def _translate_aggregation(self, agg: Aggregation, sign_column: Optional[str]) -> (str, dict):
        """
        Return an SQL fragment as string and a dictionary of parameters to be added during execution
        """
        params = {}
        agg_name = self._agg_name(agg)
        inside = ""
        if agg.metric:
            if isinstance(agg, Sum):
                inside = f"{agg.metric.name} * {sign_column}" if sign_column else agg.metric.name
            else:
                inside = agg.metric.name
        elif isinstance(agg, Count):
            if agg.distinct:
                inside = f"DISTINCT {agg.distinct.name}"
            else:
                # plain count without any metric - to properly count, we must take sign
                # into account
                agg_name = "SUM" if sign_column else agg_name
                inside = sign_column if sign_column else ""
        elif isinstance(agg, ArrayAgg):
            inside = agg.distinct.name if agg.distinct else agg.metric.name
        else:
            raise NotImplementedError(f"Aggregation {agg} is not implemented")
        if agg.filters:
            agg_name += "If"
            where_parts = []
            for fltr in agg.filters:
                filter_text, filter_params = self._ch_filter(fltr)
                where_parts.append(filter_text)
                params.update(filter_params)
            inside += ", " + " AND ".join(where_parts)
        return f"{agg_name}({inside}) AS {agg.name}", params

    def _ch_filter(self, fltr: Filter) -> (str, dict):
        """
        returns a tuple with the string that should be put into the where part of the query and
        a dictionary with the parameters that should be passed to the query during execution
        for proper escaping.
        """
        # combinators first
        if isinstance(fltr, Or):
            queries = []
            params = {}
            for subfilter in fltr.filters:
                query, subparams = self._ch_filter(subfilter)
                queries.append(query)
                params.update(subparams)
            return f'({" OR ".join(queries)})', params
        # then plain filters
        key = f"_where_{id(fltr)}_{fltr.dimension.name}"
        if isinstance(fltr, ListFilter):
            return f"{fltr.dimension.name} IN (%({key})s)", {key: fltr.values}
        if isinstance(fltr, NegativeListFilter):
            return f"{fltr.dimension.name} NOT IN (%({key})s)", {key: fltr.values}
        if isinstance(fltr, IsNullFilter):
            modifier = "" if fltr.is_null else " NOT"
            return f"{fltr.dimension.name} IS{modifier} NULL", {}
        if isinstance(fltr, ComparisonFilter):
            return f"{fltr.dimension.name} {fltr.comparison.value} %({key})s", {key: fltr.value}
        if isinstance(fltr, EqualityFilter):
            return f"{fltr.dimension.name} = %({key})s", {key: fltr.value}
        if isinstance(fltr, SubstringFilter):
            fn = "positionUTF8" if fltr.case_sensitive else "positionCaseInsensitiveUTF8"
            return f"{fn}({fltr.dimension.name}, %({key})s) > 0", {key: fltr.value}
        if isinstance(fltr, SubstringMultiValueFilter):
            fn = (
                "multiSearchAnyUTF8" if fltr.case_sensitive else "multiSearchAnyCaseInsensitiveUTF8"
            )
            return f"{fn}({fltr.dimension.name}, %({key})s)", {key: fltr.values}
        if isinstance(fltr, OverlapFilter):
            return f"hasAny({fltr.dimension.name}, %({key})s)", {key: fltr.values}
        raise ValueError(f"unsupported filter {fltr.__class__}")

    @classmethod
    def _agg_name(cls, agg: Aggregation) -> str:
        if agg.op in (AggregationOp.SUM, AggregationOp.COUNT, AggregationOp.MAX, AggregationOp.MIN):
            # CH aggregations return 0 by default, but we want None to be compatible with other
            # backends, most notably standard SQL
            if not GlobalSettings.aggregates_zero_for_empty_data and agg.op != AggregationOp.COUNT:
                return f"{agg.op.name}OrNull"
            return agg.op.name
        if agg.op == AggregationOp.ARRAY:
            if agg.distinct:
                return "groupUniqArray"
            return "groupArray"
        raise ValueError(f"Unsupported aggregation {agg}")

    @classmethod
    def cube_to_table_name(cls, cube: Union[Type[Cube], Type[AggregatingMaterializedView]]):
        return cube.__name__

    def _init_table(self, cube: Type[Cube]):
        """
        Creates the corresponding db table if the table is not yet present.
        """
        name = self.cube_to_table_name(cube)
        meta = self.get_table_meta(cube)
        fields = [
            f"{dim.name} {self._ch_type(dim)}"
            for dim in list(cube._dimensions.values()) + list(cube._metrics.values())
        ]
        field_part = ", ".join(fields)
        # indexes
        idx_part = ", ".join([idx.definition() for idx in meta.indexes])
        if idx_part:
            field_part += ", " + idx_part
        # sorting key
        cube_dim_names = set(cube._dimensions.keys())
        if meta.sorting_key:
            key_dim_names = set(meta.sorting_key)
            if key_dim_names - cube_dim_names:
                raise ConfigurationError(
                    f"Only cube dimensions may be part of the sorting key. These are extra: "
                    f"'{list(key_dim_names-cube_dim_names)}'"
                )
            if cube_dim_names - key_dim_names:
                logger.warning(
                    f"Dimensions '{list(cube_dim_names-key_dim_names)}' is missing from "
                    f"sorting_key, it will be collapsed in merge."
                )
            sorting_key = ", ".join(dim for dim in meta.sorting_key)
        else:
            sorting_key = ", ".join(dim for dim in cube._dimensions)
        # primary key
        primary_key = sorting_key
        if meta.primary_key:
            key_dim_names = set(meta.primary_key)
            if key_dim_names - cube_dim_names:
                raise ConfigurationError(
                    f"Only cube dimensions may be part of the primary key. These are extra: "
                    f"'{list(key_dim_names-cube_dim_names)}'"
                )
            primary_key = ", ".join(dim for dim in meta.primary_key)
        engine = meta.engine
        if engine == "CollapsingMergeTree":
            engine = f"{engine}({meta.sign_col})"
            field_part += f", {meta.sign_col} Int8 default 1"
        partition_part = ""
        if meta.partition_key:
            partition_part = f"PARTITION BY ({','.join(meta.partition_key)})"
        allow_nullable_key = any(dim.null for dim in cube._dimensions.values())
        settings_part = "SETTINGS allow_nullable_key = 1" if allow_nullable_key else ""
        command = (
            f"CREATE TABLE IF NOT EXISTS {self.database}.{name} ({field_part}) "
            f"ENGINE = {engine} "
            f"PRIMARY KEY ({primary_key}) "
            f"ORDER BY ({sorting_key}) "
            f"{partition_part} "
            f"{settings_part};"
        )
        logger.debug(command)
        with self.pool.get_client() as client:
            client.execute(command)

    def _ch_type(self, dimension: Union[Dimension, Metric]) -> str:
        if isinstance(dimension, ArrayDimension):
            subtype = self._ch_type(dimension.dimension)
            return f"Array({subtype})"
        for dim_cls, ch_type in self.dimension_type_map:
            if isinstance(dimension, (IntDimension, IntMetric)):
                sign = "U" if not dimension.signed else ""
                ch_type = f"{sign}{ch_type}{dimension.bits}"
            if isinstance(dimension, dim_cls):
                if hasattr(dimension, "null") and dimension.null:
                    return f"Nullable({ch_type})"
                return ch_type
        raise ValueError("unsupported dimension: %s", dimension.__class__)

    def _create_materialized_views(self, cube: Type[Cube]):
        for mv in cube._materialized_views:
            if mv.projection:
                self._create_projection(cube, mv)
            else:
                self._create_materialized_view(cube, mv)

    def _create_materialized_view(
        self, cube: Type[Cube], matview: Type[AggregatingMaterializedView], populate=True
    ):
        preserved = ", ".join(dim.name for dim in matview._dimensions.values())
        allow_nullable_key = any(dim.null for dim in matview._dimensions.values())
        settings_part = "SETTINGS allow_nullable_key = 1" if allow_nullable_key else ""
        aggregs = [
            f"{self._agg_name(agg)}({agg.metric.name}) AS {agg.metric.name}"
            for agg in matview._aggregations
        ]
        agg_part = ", ".join(aggregs)
        table_name = self.cube_to_table_name(cube)
        view_name = self.cube_to_table_name(matview)
        pop = "POPULATE" if populate else ""
        command = (
            f"CREATE MATERIALIZED VIEW IF NOT EXISTS {self.database}.{view_name} "
            f"ENGINE = AggregatingMergeTree() ORDER BY ({preserved}) {settings_part} "
            f"{pop} AS SELECT {preserved}, {agg_part} FROM {self.database}.{table_name} "
            f"GROUP BY {preserved};"
        )
        logger.debug(command)
        with self.pool.get_client() as client:
            client.execute(command)

    def _create_projection(
        self, cube: Type[Cube], matview: Type[AggregatingMaterializedView], populate=True
    ):
        meta = self.get_table_meta(cube)
        preserved = ", ".join(dim.name for dim in matview._dimensions.values())
        aggregs = [
            self._translate_aggregation(agg, meta.sign_col)[0] for agg in matview._aggregations
        ]
        if matview.preserve_sign:
            aggregs.append(f"SUM({meta.sign_col}) AS _{meta.sign_col}")
        agg_part = ", ".join(aggregs)
        table_name = self.cube_to_table_name(cube)
        view_name = self.cube_to_table_name(matview)
        command = (
            f"ALTER TABLE {self.database}.{table_name} ADD PROJECTION IF NOT EXISTS {view_name} "
            f"(SELECT {preserved}, {agg_part} GROUP BY {preserved});"
        )
        logger.debug(command)
        with self.pool.get_client() as client:
            client.execute(command)
            if populate:
                client.execute(
                    f"ALTER TABLE {self.database}.{table_name} MATERIALIZE PROJECTION {view_name}"
                )

    def _create_dictionaries(self, cube: Type[Cube]):
        meta = self.get_table_meta(cube)
        with self.pool.get_client() as client:
            for dict_def in meta.dictionaries:
                # we want to check potential changes in dictionary definition
                out = client.execute(
                    f"SELECT comment FROM system.dictionaries "
                    f"WHERE database = '{self.database}' AND name = '{dict_def.name}'"
                )
                if out:
                    if out[0][0] != f"blake2:{dict_def.checksum}":
                        logger.info(
                            'Dictionary "%s" definition has changed, recreating', dict_def.name
                        )
                        client.execute(dict_def.drop_sql(database=self.database))
                    else:
                        continue
                client.execute(dict_def.definition_sql(database=self.database))

    def _drop_dictionaries(self, cube: Type[Cube]):
        meta = self.get_table_meta(cube)
        with self.pool.get_client() as client:
            for dict_def in meta.dictionaries:
                client.execute(dict_def.drop_sql(database=self.database))

    def _translate_transform(self, transform: Transform) -> (str, str):
        """
        returns the name of the field in the resulting records and the string which should be part
        of the select
        """
        if isinstance(transform, ExplicitMappingTransform):
            key_array = list(transform.mapping.keys())
            value_array = list(transform.mapping.values())
            select = (
                f"transform({transform.dimension.name}, {key_array}, {value_array}) "
                f"AS {transform.name}"
            )
            return transform.name, select
        if isinstance(transform, StoredMappingTransform):
            select = (
                f"dictGet('{self.database}.{transform.mapping_name}', "
                f"'{transform.mapping_field}', "
                f"toUInt64({transform.dimension.name})) AS {transform.name}"
            )
            return transform.name, select
        raise ValueError(f"Unsupported transform {transform.__class__} in the clickhouse backend")

    def _drop_table(self, cube: Type[Cube]):
        with self.pool.get_client() as client:
            client.execute(
                f"DROP TABLE IF EXISTS {self.database}.{self.cube_to_table_name(cube)} SYNC"
            )
