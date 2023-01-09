from datetime import timedelta
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional

import attr

from tecton_proto.args import feature_view_pb2

AVAILABILITY_SPOT = "spot"
AVAILABILITY_ON_DEMAND = "on_demand"
AVAILABILITY_SPOT_FALLBACK = "spot_with_fallback"
DATABRICKS_SUPPORTED_AVAILABILITY = {AVAILABILITY_SPOT, AVAILABILITY_ON_DEMAND, AVAILABILITY_SPOT_FALLBACK}
EMR_SUPPORTED_AVAILABILITY = {AVAILABILITY_SPOT, AVAILABILITY_ON_DEMAND, AVAILABILITY_SPOT_FALLBACK}


class SparkVersions(str, Enum):
    Emr6_5 = "emr-6.5.0"
    Emr6_7 = "emr-6.7.0"
    Dbr10_4 = "10.4.x-scala2.12"
    Dbr9_1 = "9.1.x-scala2.12"


DEFAULT_SPARK_VERSIONS = {"databricks_spark_version": SparkVersions.Dbr10_4, "emr_spark_version": SparkVersions.Emr6_7}
EMR_SUPPORTED_SPARK = {SparkVersions.Emr6_5, SparkVersions.Emr6_7}
DATABRICKS_SUPPORTED_SPARK = {SparkVersions.Dbr10_4, SparkVersions.Dbr9_1}


@attr.s(auto_attribs=True)
class ExistingClusterConfig:
    """Use an existing Databricks cluster.

    :param existing_cluster_id: ID of the existing cluster.
    """

    existing_cluster_id: str

    def _to_proto(self) -> feature_view_pb2.ExistingClusterConfig:
        proto = feature_view_pb2.ExistingClusterConfig()
        proto.existing_cluster_id = self.existing_cluster_id

        return proto

    def _to_cluster_proto(self) -> feature_view_pb2.ClusterConfig:
        return feature_view_pb2.ClusterConfig(existing_cluster=self._to_proto())


@attr.s(auto_attribs=True)
class EMRClusterConfig:
    f"""Configuration used to specify materialization cluster options.

    This class describes the attributes of the new clusters which are created in EMR during
    materialization jobs. You can configure options of these clusters, like cluster size and extra pip dependencies.

    :param instance_type: Instance type for the cluster. Must be a valid type as listed in https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-supported-instance-types.html.
        Additionally, Graviton instances such as the m6g family are not supported. If not specified, a value determined by the Tecton backend is used.
    :param instance_availability: Instance availability for the cluster : "spot", "on_demand", or "spot_with_fallback".
        If not specified, default is spot.
    :param number_of_workers: Number of instances for the materialization job. If not specified, a value determined by the Tecton backend is used
    :param first_on_demand: The first `first_on_demand` nodes of the cluster will use on_demand instances. The rest will use the type specified by instance_availability.
        If first_on_demand >= 1, the master node will use on_demand instance type. `first_on_demand` is recommended to be set >= 1 for cluster configs for critical streaming features.
    :param root_volume_size_in_gb: Size of the root volume in GB per instance for the materialization job.
        If not specified, a value determined by the Tecton backend is used.
    :param extra_pip_dependencies: Extra pip dependencies to be installed on the materialization cluster. Must be PyPI packages, or wheels/eggs in S3 or DBFS.
    :param spark_config: Map of Spark configuration options and their respective values that will be passed to the
        FeatureView materialization Spark cluster.
    :param emr_version: EMR version of the cluster. Supported versions include "emr-6.7.0" and "emr-6.5.0". (Default: emr-6.5.0)

    Note on ``extra_pip_dependencies``: This is a list of packages that will be installed during materialization.
    To use PyPI packages, specify the package name and optionally the version, e.g. ``"tensorflow"`` or ``"tensorflow==2.2.0"``.
    To use custom code, package it as a Python wheel or egg file in S3 or DBFS, then specify the path to the file,
    e.g. ``"s3://my-bucket/path/custom.whl"``, or ``"dbfs:/path/to/custom.whl"``.

    These libraries will only be available to use inside Spark UDFs. For example, if you set
    ``extra_pip_dependencies=["tensorflow"]``, you can use it in your transformation as shown below.

    An example of EMRClusterConfig.

    .. code-block:: python

        from tecton import batch_feature_view, Input, EMRClusterConfig

        @batch_feature_view(
            sources=[FilteredSource(credit_scores_batch)],
            # Can be an argument instance to a batch feature view decorator
            batch_compute = EMRClusterConfig(
                instance_type = 'm5.2xlarge',
                number_of_workers=4,
                extra_pip_dependencies=["tensorflow==2.2.0"],
            ),
            # Other named arguments to batch feature view
            ...
        )

        # Use the tensorflow package in the UDF since tensorflow will be installed
        # on the EMR Spark cluster. The import has to be within the UDF body. Putting it at the
        # top of the file or inside transformation function won't work.

        @transformation(mode='pyspark')
        def test_transformation(transformation_input):
            from pyspark.sql import functions as F
            from pyspark.sql.types import IntegerType

            def my_tensorflow(x):
                import tensorflow as tf
                return int(tf.math.log1p(float(x)).numpy())

            my_tensorflow_udf = F.udf(my_tensorflow, IntegerType())

            return transformation_input.select(
                'entity_id',
                'timestamp',
                my_tensorflow_udf('clicks').alias('log1p_clicks')
            )
    """

    instance_type: Optional[str] = None
    instance_availability: Optional[str] = None
    number_of_workers: Optional[int] = None
    first_on_demand: Optional[int] = None
    root_volume_size_in_gb: Optional[int] = None
    extra_pip_dependencies: Optional[List[str]] = None
    spark_config: Optional[Dict[str, str]] = None
    emr_version: str = DEFAULT_SPARK_VERSIONS["emr_spark_version"]

    def _to_proto(self) -> feature_view_pb2.NewClusterConfig:
        proto = feature_view_pb2.NewClusterConfig()
        if self.instance_type:
            proto.instance_type = self.instance_type
        if self.instance_availability:
            if self.instance_availability not in EMR_SUPPORTED_AVAILABILITY:
                raise ValueError(
                    f"Instance availability {self.instance_availability} is not supported. Choose one of {EMR_SUPPORTED_AVAILABILITY}"
                )
            proto.instance_availability = self.instance_availability
        if self.emr_version not in EMR_SUPPORTED_SPARK:
            raise ValueError(
                f"EMR version {self.emr_version} is not supported. Supported versions: {EMR_SUPPORTED_SPARK}"
            )
        if self.number_of_workers:
            proto.number_of_workers = self.number_of_workers
        if self.first_on_demand:
            proto.first_on_demand = self.first_on_demand
        if self.root_volume_size_in_gb:
            proto.root_volume_size_in_gb = self.root_volume_size_in_gb
        if self.extra_pip_dependencies:
            proto.extra_pip_dependencies.extend(self.extra_pip_dependencies)
        if self.spark_config:
            spark_config = SparkConfigWrapper(self.spark_config)._to_proto()
            proto.spark_config.CopyFrom(spark_config)
        proto.pinned_spark_version = self.emr_version

        return proto

    def _to_cluster_proto(self) -> feature_view_pb2.ClusterConfig:
        return feature_view_pb2.ClusterConfig(new_emr=self._to_proto())


@attr.s(auto_attribs=True)
class DatabricksClusterConfig:
    """Configuration used to specify materialization cluster options.

    This class describes the attributes of the new clusters which are created in Databricks during
    materialization jobs. You can configure options of these clusters, like cluster size and extra pip dependencies.

    :param instance_type: Instance type for the cluster. Must be a valid type as listed in https://databricks.com/product/aws-pricing/instance-types.
        Additionally, Graviton instances such as the m6g family are not supported. If not specified, a value determined by the Tecton backend is used.
    :param instance_availability: Instance availability for the cluster : "spot", "on_demand", or "spot_with_fallback".
        If not specified, default is spot.
    :param first_on_demand: The first `first_on_demand` nodes of the cluster will use on_demand instances. The rest will use the type specified by instance_availability.
        If first_on_demand >= 1, the driver node use on_demand instance type.
    :param number_of_workers: Number of instances for the materialization job. If not specified, a value determined by the Tecton backend is used.
        If set to 0 then jobs will be run in single-node clusters.
    :param root_volume_size_in_gb: Size of the root volume in GB per instance for the materialization job.
        If not specified, a value determined by the Tecton backend is used.
    :param extra_pip_dependencies: Extra pip dependencies to be installed on the materialization cluster. Must be PyPI packages, or wheels/eggs in S3 or DBFS.
    :param spark_config: Map of Spark configuration options and their respective values that will be passed to the
        FeatureView materialization Spark cluster.
    :param dbr_version: DBR version of the cluster. Supported versions include 9.1.x-scala2.12 and 10.4.x-scala2.12. (Default: 10.4.x-scala2.12)

    Note on ``extra_pip_dependencies``: This is a list of packages that will be installed during materialization.
    To use PyPI packages, specify the package name and optionally the version, e.g. ``"tensorflow"`` or ``"tensorflow==2.2.0"``.
    To use custom code, package it as a Python wheel or egg file in S3 or DBFS, then specify the path to the file,
    e.g. ``"s3://my-bucket/path/custom.whl"``, or ``"dbfs:/path/to/custom.whl"``.

    These libraries will only be available to use inside Spark UDFs. For example, if you set
    ``extra_pip_dependencies=["tensorflow"]``, you can use it in your transformation as shown below.

    An example of DatabricksClusterConfig.

    .. code-block:: python

        from tecton import batch_feature_view, Input, DatabricksClusterConfig

        @batch_feature_view(
            sources=[FilteredSource(credit_scores_batch)],
            # Can be an argument instance to a batch feature view decorator
            batch_compute = DatabricksClusterConfig(
                instance_type = 'm5.2xlarge',
                spark_config = {"spark.executor.memory" : "12g"}
                extra_pip_dependencies=["tensorflow"],
            ),
            # Other named arguments to batch feature view
            ...
        )

        # Use the tensorflow package in the UDF since tensorflow will be installed
        # on the Databricks Spark cluster. The import has to be within the UDF body. Putting it at the
        # top of the file or inside transformation function won't work.

        @transformation(mode='pyspark')
        def test_transformation(transformation_input):
            from pyspark.sql import functions as F
            from pyspark.sql.types import IntegerType

            def my_tensorflow(x):
                import tensorflow as tf
                return int(tf.math.log1p(float(x)).numpy())

            my_tensorflow_udf = F.udf(my_tensorflow, IntegerType())

            return transformation_input.select(
                'entity_id',
                'timestamp',
                my_tensorflow_udf('clicks').alias('log1p_clicks')
            )

    """

    instance_type: Optional[str] = None
    instance_availability: Optional[str] = None
    number_of_workers: Optional[int] = None
    first_on_demand: Optional[int] = None
    root_volume_size_in_gb: Optional[int] = None
    extra_pip_dependencies: Optional[List[str]] = None
    spark_config: Optional[Dict[str, str]] = None
    dbr_version: str = DEFAULT_SPARK_VERSIONS["databricks_spark_version"]

    def _to_proto(self) -> feature_view_pb2.NewClusterConfig:
        proto = feature_view_pb2.NewClusterConfig()
        if self.instance_type:
            proto.instance_type = self.instance_type
        if self.instance_availability:
            if self.instance_availability not in DATABRICKS_SUPPORTED_AVAILABILITY:
                raise ValueError(
                    f"Instance availability {self.instance_availability} is not supported. Choose {AVAILABILITY_SPOT}, {AVAILABILITY_ON_DEMAND} or {AVAILABILITY_SPOT_FALLBACK}"
                )
            proto.instance_availability = self.instance_availability
        if self.dbr_version not in DATABRICKS_SUPPORTED_SPARK:
            raise ValueError(
                f"Databricks version {self.dbr_version} is not supported. Supported versions: {DATABRICKS_SUPPORTED_SPARK}"
            )

        if self.number_of_workers is not None:
            proto.number_of_workers = self.number_of_workers
        if self.root_volume_size_in_gb:
            proto.root_volume_size_in_gb = self.root_volume_size_in_gb
        if self.first_on_demand:
            proto.first_on_demand = self.first_on_demand
        if self.extra_pip_dependencies:
            # Pretty easy to do e.g. extra_pip_dependencies="tensorflow" by mistake and end up with
            # [t, e, n, s, o, r, f, l, o, w] as a list of dependencies passed to the Spark job.
            #
            # Since this is annoying to debug, we check for that here.
            if isinstance(self.extra_pip_dependencies, str):
                raise ValueError("extra_pip_dependencies must be a list")
            proto.extra_pip_dependencies.extend(self.extra_pip_dependencies)
        if self.spark_config:
            spark_config = SparkConfigWrapper(self.spark_config)._to_proto()
            proto.spark_config.CopyFrom(spark_config)
        proto.pinned_spark_version = self.dbr_version

        return proto

    def _to_cluster_proto(self) -> feature_view_pb2.ClusterConfig:
        return feature_view_pb2.ClusterConfig(new_databricks=self._to_proto())


@attr.s(auto_attribs=True)
class SparkConfigWrapper:
    spark_config_map: Dict[str, str]

    HARDCODED_OPTS = {
        "spark.driver.memory": "spark_driver_memory",
        "spark.executor.memory": "spark_executor_memory",
        "spark.driver.memoryOverhead": "spark_driver_memory_overhead",
        "spark.executor.memoryOverhead": "spark_executor_memory_overhead",
    }

    def _to_proto(self):
        proto = feature_view_pb2.SparkConfig()
        for opt, val in self.spark_config_map.items():
            if opt in self.HARDCODED_OPTS:
                setattr(proto, self.HARDCODED_OPTS[opt], val)
            else:
                proto.spark_conf[opt] = val

        return proto


@attr.s(auto_attribs=True)
class ParquetConfig:
    """(Config Class) ParquetConfig Class.

    This class describes the attributes of Parquet-based offline feature store storage for the feature definition.

    :param subdirectory_override: This is for the location of the feature data in the offline store. By default, all feature views will be under the subdirectory <workspace_name> if this param is not specified.
    """

    subdirectory_override: Optional[str] = None

    def _to_proto(self):
        store_config = feature_view_pb2.OfflineFeatureStoreConfig()
        store_config.parquet.SetInParent()
        if self.subdirectory_override:
            store_config.subdirectory_override = self.subdirectory_override
        return store_config


@attr.s(auto_attribs=True)
class DeltaConfig:
    """(Config Class) DeltaConfig Class.

    This class describes the attributes of DeltaLake-based offline feature store storage for the feature definition.

    :param time_partition_size: The size of a time partition in the DeltaLake table, specified as a datetime.timedelta. Defaults to 24 hours.
    :param subdirectory_override: This is for the location of the feature data in the offline store. By default, all feature views will be under the subdirectory <workspace_name> if this param is not specified.
    """

    time_partition_size: Optional[timedelta] = timedelta(hours=24)
    subdirectory_override: Optional[str] = None

    def _to_proto(self):
        store_config = feature_view_pb2.OfflineFeatureStoreConfig()
        store_config.delta.time_partition_size.FromTimedelta(self.time_partition_size)
        if self.subdirectory_override:
            store_config.subdirectory_override = self.subdirectory_override
        return store_config


@attr.s(auto_attribs=True)
class DynamoConfig:
    """(Config Class) DynamoConfig Class.

    This class describes the attributes of DynamoDB based online feature store for the feature definition.
    Currently there are no attributes for this class.
    Users can specify online_store = DynamoConfig()
    """

    def _to_proto(self):
        store_config = feature_view_pb2.OnlineStoreConfig()
        store_config.dynamo.enabled = True
        store_config.dynamo.SetInParent()
        return store_config


@attr.s(auto_attribs=True)
class RedisConfig:
    """(Config Class) RedisConfig Class.

    This class describes the attributes of Redis based online feature store for the feature definition.
    Currently there are no attributes for this class.
    Users can specify online_store = RedisConfig()
    Note : Your Tecton deployment needs to be connected to Redis before you can use this configuration option.
    Please contact Tecton support for details.
    """

    def _to_proto(self):
        store_config = feature_view_pb2.OnlineStoreConfig()
        store_config.redis.enabled = True
        store_config.redis.SetInParent()
        return store_config


@attr.s(auto_attribs=True)
class MonitoringConfig:
    """Configuration used to specify monitoring options.

    This class describes the FeatureView materialization freshness and alerting configurations. Requires
    materialization to be enabled. Freshness monitoring requires online materialization to be enabled.
    See `Monitoring Materialization`_ for more details.

    :param monitor_freshness: Defines the enabled/disabled state of monitoring when feature data is materialized to the online feature store.
    :type monitor_freshness: bool
    :param expected_freshness: Threshold used to determine if recently materialized feature data is stale.
        Data is stale if ``now - anchor_time(most_recent_feature_value) > expected_freshness``.
        Value must be at least 2 times the feature tile length.
        If not specified, a value determined by the Tecton backend is used
    :type expected_freshness: timedelta, optional
    :param alert_email: Email that alerts for this FeatureView will be sent to.
    :type alert_email: str, optional

    An example declaration of a MonitorConfig

        .. code-block:: python

            from datetime import timedelta
            from tecton import batch_feature_view, Input, MonitoringConfig
            # For all named arguments to the batch feature view, see docs for details and types.
            @batch_feature_view(
                sources=[FilteredSource(credit_scores_batch)],
                # Can be an argument instance to a batch feature view decorator
                monitoring = MonitoringConfig(
                    monitor_freshness=True,
                    expected_freshness=timedelta(weeks=1),
                    alert_email="brian@tecton.ai"
                ),
                # Other named arguments
                ...
            )

            # Your batch feature view function
            def credit_batch_feature_view(credit_scores):
              ...

    .. _Monitoring Materialization: https://docs.tecton.ai/v2/overviews/monitoring_materialization.html
    """

    monitor_freshness: bool
    expected_freshness: Optional[timedelta] = None
    alert_email: Optional[str] = None

    def _to_proto(self) -> feature_view_pb2.MonitoringConfig:
        proto = feature_view_pb2.MonitoringConfig()

        if self.expected_freshness:
            proto.expected_freshness.FromTimedelta(self.expected_freshness)

        proto.alert_email = self.alert_email or ""
        proto.monitor_freshness = self.monitor_freshness
        return proto
