import time
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import attr
import numpy
import pandas
import pyspark
import pytz

from tecton import snowflake_context
from tecton._internals.rewrite import rewrite_tree_for_spine
from tecton._internals.sdk_decorators import sdk_public_method
from tecton_athena import athena_session
from tecton_core import conf
from tecton_core.logger import get_logger
from tecton_core.query.node_interface import DataframeWrapper
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_interface import recurse_query_tree
from tecton_core.query.nodes import UserSpecifiedDataNode
from tecton_core.query.rewrite import rewrite_tree
from tecton_spark.query import translate

logger = get_logger("Dataframe")


def set_pandas_timezone_from_spark(pandas_df):
    """Match pandas timezone to that of Spark, s.t. the timestamps are correctly displayed."""
    from tecton.tecton_context import TectonContext

    tz = TectonContext.get_instance()._spark.conf.get("spark.sql.session.timeZone")
    for col in pandas_df.columns:
        if pandas.core.dtypes.common.is_datetime64_dtype(pandas_df[col]):
            pandas_df[col] = pandas_df[col].dt.tz_localize(pytz.timezone(tz))
            pandas_df[col] = pandas_df[col].dt.tz_convert(pytz.timezone("UTC"))
            pandas_df[col] = pandas_df[col].dt.tz_localize(None)
    return pandas_df


@attr.s(auto_attribs=True)
class FeatureVector(object):
    """
    FeatureVector Class.

    A FeatureVector is a representation of a single feature vector. Usage of a FeatureVector typically involves
    extracting the feature vector using ``to_pandas()``, ``to_dict()``, or ``to_numpy()``.

    """

    _names: List[str]
    _values: List[Union[int, str, bytes, float, list]]
    _effective_times: List[Optional[datetime]]
    slo_info: Optional[Dict[str, str]] = None

    @sdk_public_method
    def to_dict(
        self, return_effective_times: bool = False
    ) -> Dict[str, Union[int, str, bytes, float, list, dict, None]]:
        """Turns vector into a Python dict.

        :param: return_effective_times: Whether to return the effective time of the feature.

        :return: A Python dict.
        """
        if return_effective_times:
            return {
                name: {"value": self._values[i], "effective_time": self._effective_times[i]}
                for i, name in enumerate(self._names)
            }

        return dict(zip(self._names, self._values))

    @sdk_public_method
    def to_pandas(self, return_effective_times: bool = False) -> pandas.DataFrame:
        """Turns vector into a Pandas DataFrame.

        :param: return_effective_times: Whether to return the effective time of the feature as part of the DataFrame.

        :return: A Pandas DataFrame.
        """
        if return_effective_times:
            return pandas.DataFrame(
                list(zip(self._names, self._values, self._effective_times)), columns=["name", "value", "effective_time"]
            )

        return pandas.DataFrame([self._values], columns=self._names)

    @sdk_public_method
    def to_numpy(self, return_effective_times: bool = False) -> numpy.array:
        """Turns vector into a numpy array.

        :param: return_effective_times: Whether to return the effective time of the feature as part of the list.

        :return: A numpy array.
        """
        if return_effective_times:
            return numpy.array([self._values, self._effective_times])

        return numpy.array(self._values)

    def _update(self, other: "FeatureVector"):
        self._names.extend(other._names)
        self._values.extend(other._values)
        self._effective_times.extend(other._effective_times)


# NOTE: use repr=False to avoid printing out the underlying dataframes when used in REPL/notebook.
@attr.define(repr=False)
class TectonDataFrame(DataframeWrapper):
    """
    A thin wrapper around Pandas, Spark, and Snowflake dataframes.
    """

    _spark_df: Optional[pyspark.sql.DataFrame] = None
    _pandas_df: Optional[pandas.DataFrame] = None
    # TODO: Change the type to snowflake.snowpark.DataFrame, currently it will
    # fail type checking for our auto generated doc.
    _snowflake_df: Optional[Any] = None
    # should already by optimized
    _querytree: Optional[NodeRef] = attr.field(default=None, repr=lambda x: "TectonQueryTree")

    @sdk_public_method
    def explain(
        self,
        node_id: bool = True,
        name: bool = True,
        description: bool = True,
        columns: bool = False,
    ):
        """Prints the query tree. Should only be used when this TectonDataFrame is backed by a query tree.

        Args:
            node_id: If True, the unique id associated with each node will be rendered.
            name: If True, the class names of the nodes will be rendered.
            description: If True, the actions of the nodes will be rendered.
            columns: If True, the columns of each node will be rendered as an appendix after tree itself.
        """
        if self._querytree:
            if not name and not description:
                raise RuntimeError("At least one of 'name' or 'description' must be True.")
            if columns and not node_id:
                raise RuntimeError("Can only show columns if 'node_id' is True.")
            print(self._querytree.pretty_str(node_id=node_id, name=name, description=description, columns=columns))
        else:
            print("Explain is only available for TectonDataFrames backed by a query tree.")

    @sdk_public_method
    def to_spark(self) -> pyspark.sql.DataFrame:
        """Returns data as a Spark DataFrame.

        :return: A Spark DataFrame.
        """
        if self._spark_df is not None:
            return self._spark_df
        else:
            from tecton.tecton_context import TectonContext

            tc = TectonContext.get_instance()
            if self._querytree is not None:
                return translate.spark_convert(self._querytree).to_dataframe(tc._spark)
            elif self._pandas_df is not None:
                return tc._spark.createDataFrame(self._pandas_df)
            else:
                raise NotImplementedError

    @sdk_public_method
    def to_pandas(self) -> pandas.DataFrame:
        """Returns data as a Pandas DataFrame.

        :return: A Pandas DataFrame.
        """
        if self._pandas_df is not None:
            return self._pandas_df

        assert self._spark_df is not None or self._snowflake_df is not None or self._querytree is not None

        if self._spark_df is not None:
            return set_pandas_timezone_from_spark(self._spark_df.toPandas())

        if self._snowflake_df is not None:
            return self._snowflake_df.to_pandas(statement_params={"SF_PARTNER": "tecton-ai"})

        if self._querytree is not None:
            return set_pandas_timezone_from_spark(self.to_spark().toPandas())

    def _to_sql(self, create_temp_views: bool = False):
        if self._querytree is not None:
            if create_temp_views:
                recurse_query_tree(
                    self._querytree,
                    lambda node: node.data._register_temp_view() if isinstance(node, UserSpecifiedDataNode) else None,
                )
            return self._querytree.to_sql()
        else:
            raise NotImplementedError

    # TODO(TEC-11097): Deprecate this method after version 0.7.0
    @sdk_public_method
    def to_snowflake(self):
        """
        Deprecated. Please use to_snowpark() instead.
        Returns data as a Snowflake DataFrame.

        :return: A Snowflake DataFrame.
        :meta private:
        """
        logger.warning("to_snowflake() is deprecated - please use to_snowpark() instead.")

        if self._snowflake_df is not None:
            return self._snowflake_df

        assert self._pandas_df is not None

        from tecton.snowflake_context import SnowflakeContext

        if conf.get_bool("ALPHA_SNOWFLAKE_SNOWPARK_ENABLED"):
            return SnowflakeContext.get_instance().get_session().createDataFrame(self._pandas_df)
        else:
            raise Exception("to_snowflake() is only available with Snowpark enabled")

    @sdk_public_method
    def to_snowpark(self):
        """
        Returns data as a Snowpark DataFrame.

        :return: A Snowpark DataFrame.
        """
        if self._snowflake_df is not None:
            return self._snowflake_df

        assert self._pandas_df is not None

        from tecton.snowflake_context import SnowflakeContext

        if conf.get_bool("ALPHA_SNOWFLAKE_SNOWPARK_ENABLED"):
            return SnowflakeContext.get_instance().get_session().createDataFrame(self._pandas_df)
        else:
            raise Exception("to_snowpark() is only available with Snowpark enabled")

    @classmethod
    def _create(cls, df: Union[pyspark.sql.DataFrame, pandas.DataFrame, NodeRef]):
        """Creates a Tecton DataFrame from a Spark or Pandas DataFrame."""
        if isinstance(df, pandas.DataFrame):
            return cls(spark_df=None, pandas_df=df, snowflake_df=None)
        elif isinstance(df, pyspark.sql.DataFrame):
            return cls(spark_df=df, pandas_df=None, snowflake_df=None)
        elif isinstance(df, NodeRef):
            rewrite_tree(df)

            from tecton.tecton_context import TectonContext

            spark = TectonContext.get_instance()._spark
            rewrite_tree_for_spine(df, spark)
            return cls(spark_df=None, pandas_df=None, snowflake_df=None, querytree=df)

        raise TypeError(f"DataFrame must be of type pandas.DataFrame or pyspark.sql.Dataframe, not {type(df)}")

    @classmethod
    # This should be merged into _create once snowpark is installed with pip
    def _create_with_snowflake(cls, df: "snowflake.snowpark.DataFrame"):
        """Creates a Tecton DataFrame from a Snowflake DataFrame."""
        from snowflake.snowpark import DataFrame as SnowflakeDataFrame

        if isinstance(df, SnowflakeDataFrame):
            return cls(spark_df=None, pandas_df=None, snowflake_df=df)

        raise TypeError(f"DataFrame must be of type snowflake.snowpark.Dataframe, not {type(df)}")

    def subtree(self, node_id: int) -> "TectonDataFrame":
        """Creates a TectonDataFrame from a subtree of prior querytree labeled by a node id in .explain()."""
        if not self._querytree:
            raise RuntimeError("Cannot construct a TectonDataFrame from a node id.")

        tree = self._querytree.create_tree()
        return self._create(NodeRef(tree.get_node(node_id).data))

    def _timed_to_pandas(self):
        """Convenience method for measuring performance."""
        start = time.time()
        ret = self.to_spark().toPandas()
        end = time.time()
        print(f"took {end-start} seconds")
        return ret

    # The methods below implement the DataframeWrapper interface
    def _register_temp_view(self):
        # TODO(TEC-11647): this will be merged with ALPHA_ATHENA_COMPUTE_ENABLED
        if conf.get_or_none("SQL_DIALECT") == "athena":
            session = athena_session.get_session()
            session.write_pandas(self.to_pandas(), self._temp_view_name)
        elif conf.get_or_none("SQL_DIALECT") == "snowflake":
            session = snowflake_context.SnowflakeContext.get_instance().get_session()
            spine_df = self.to_pandas()
            session.write_pandas(
                self.to_pandas(),
                table_name=self._temp_view_name,
                auto_create_table=True,
                table_type="temporary",
                quote_identifiers=True,
                overwrite=True,
            )
        else:
            self.to_spark().createOrReplaceTempView(self._temp_view_name)

    def _drop_temp_view(self):
        # TODO(TEC-11647): this will be merged with ALPHA_ATHENA_COMPUTE_ENABLED
        # TODO: implement cleanup using this prior to enabling athena-sql mode in tests
        if conf.get_or_none("SQL_DIALECT") == "athena":
            session = athena_session.get_session()
            session._delete_table_if_exists(session.config.database, self._temp_view_name)
        else:
            from tecton.tecton_context import TectonContext

            spark = TectonContext.get_instance()._spark
            spark.catalog.dropTempView(self._temp_view_name)

    def _select_distinct(self, columns: List[str]) -> DataframeWrapper:
        if self._pandas_df is not None:
            return TectonDataFrame._create(self._pandas_df[columns].drop_duplicates())
        elif self._spark_df is not None:
            return TectonDataFrame._create(self._spark_df.select(columns).distinct())
        else:
            raise NotImplementedError

    @property
    def _dataframe(self) -> Union[pyspark.sql.DataFrame, pandas.DataFrame]:
        if self._spark_df is not None:
            return self._spark_df
        elif self._pandas_df is not None:
            return self._pandas_df
        else:
            raise NotImplementedError

    @property
    def columns(self) -> List[str]:
        if self._spark_df is not None:
            return self._spark_df.columns
        elif self._pandas_df is not None:
            return list(self._pandas_df.columns)
        else:
            raise NotImplementedError


# for legacy compat
DataFrame = TectonDataFrame
