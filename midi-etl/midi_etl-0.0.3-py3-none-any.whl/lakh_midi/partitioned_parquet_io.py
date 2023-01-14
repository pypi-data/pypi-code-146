from collections import namedtuple
from functools import partial
from itertools import chain
from pathlib import Path
from typing import Callable, List, Union
from dagster import Field, IOManager, InputContext, MultiPartitionsDefinition, OutputContext, PartitionKeyRange, StaticPartitionsDefinition, StringSource, TimeWindowPartitionsDefinition, io_manager
import pandas
import pendulum
from dagster import _check as check
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd

#TODO test schema prefix outcomes
# 
class PartitionedParquetIOManager(IOManager):
    """
    This IOManager will take in a pandas dataframe and store it in parquet at the
    specified path.
    It stores outputs for different partitions in different filepaths.
    Downstream ops can either load this dataframe into a pandas df or simply retrieve a path
    to where the data is stored.
    """

    def __init__(self, base_path, read_kwargs=None):
        self._base_path = base_path
        self._read_kwargs = read_kwargs or {}
        self._schema_prefix = None

    def get_partition_column(self, context: Union[InputContext, OutputContext]):
        """
        fetch one or more partition columns
        """

        if isinstance(context.asset_partitions_def, StaticPartitionsDefinition):
            partition_column = [context.asset_partitions_def.name]
        elif isinstance(context.asset_partitions_def, MultiPartitionsDefinition):
            # if multi partition just infer partitions from the 
            # MultiPartitionsDefintion
            partition_column = list(context.asset_partition_key.keys_by_dimension.keys())
        
        if context.has_partition_key:
            assert partition_column is not None, 'partition_column must be specified via meta data for partitioned assets'
        
        partition_column = list(partition_column)
        return partition_column
    
    def handle_output(self, context: OutputContext,
                      df: Union[pandas.DataFrame, pandas.Series]):
        path = self._get_path(context)

        partition_column = self.get_partition_column(context)
        assert set(partition_column).intersection(df.columns) == set(partition_column), \
            'not all partition columns found in the DataFrame '\
            f'got {df.columns}, expected {partition_column}'
    
        if isinstance(df, pandas.Series):
            df = df.to_frame()
        if isinstance(df, pandas.DataFrame):
            row_count = len(df)
            context.log.info(f"Row count: {row_count}")
            context.log.info(df.head())
            
            if row_count > 0:
                table =  pa.Table.from_pandas(df)
                pq.write_to_dataset(
                    table,
                    path,
                    partition_column,
                    filesystem=context.resources.s3_fs,
                    existing_data_behavior='delete_matching',
                )
                self._generate_ddl(context, df, path, partition_column)
            else:
                context.log.warning('No data handed to IOManager for this partition')

        else:
            raise Exception(f"Outputs of type {type(df)} not supported.")

        # context.add_output_metadata({"row_count": row_count, "path": path})

    def load_input(
        self, context: InputContext
    ) -> Union[pandas.DataFrame, List[pandas.DataFrame]]:

        input_type = context.dagster_type.typing_type
        path = self._get_path(context)
        context.log.info(path)
        
        columns = context.metadata.get("columns")
        if columns is not None:
            context.log.debug(
                f"{self.__class__} received metadata value columns={columns}")

        allow_missing_partitions = context.metadata.get(
            "allow_missing_partitions", False
        )

        if input_type == List[pandas.DataFrame] and (not context.has_asset_partitions):
                raise TypeError(f"Detected {input_type} input type but the asset is not partitioned")


        if input_type in [pandas.DataFrame, List[pandas.DataFrame]]:
            context.log.debug(f"Loading Dataframe from {path}")
            partition_filter = self.get_partition_filter(context)
            # raise ValueError(path)
            # table = pq.read_table(
            #     path,
            #     columns=columns,
            #     filesystem=context.resources.s3_fs,
            #     use_pandas_metadata=True,
                
            #     filters=list(chain.from_iterable(partition_filter)) if partition_filter else None
            # )
            df = pq.ParquetDataset(
                    path, 
                    filesystem=context.resources.s3_fs,
                    filters=list(chain.from_iterable(partition_filter)) if partition_filter else None
                ).read_pandas(
                    columns=columns,
                ).to_pandas()

            return df

        else:
            return check.failed(
                f"Inputs of type {context.dagster_type} not supported. Please specify a valid type "
                "for this input either in the op signature or on the corresponding In."
            )
    
    def _generate_ddl(self, context, df: pd.DataFrame, path, partition_columns):
        _, schema, table = self._get_schema(context)
        conn = context.resources.trino_connection
        ddl = f"""
            {pd.io.sql.get_schema(df, table, con=conn).replace('CREATE TABLE', "CREATE TABLE IF NOT EXISTS")}
            WITH (
                external_location = '{path.replace('s3', 's3a')}',
                {f"partitioned_by = ARRAY{partition_columns}" if partition_columns else ""}

            )

        """.replace("TEXT", "VARCHAR")

        sync = f"CALL system.sync_partition_metadata('{schema}', '{table}', 'FULL')"
        
        cur = conn.cursor()
        cur.execute(ddl)
        context.log.debug(f"Executing ddl: {cur.fetchall()}")
        context.log.debug(ddl)
        cur.execute(sync)
        context.log.debug(f"Executing sync: {cur.fetchall()}")
            
    
    def _get_path(self, context: Union[InputContext, OutputContext]):
        key = '/'.join(context.asset_key.path)  # type: ignore
        base_path = self._base_path
        s3 = False
        if base_path.startswith('s3://'):
            s3 = True
            base_path = base_path[len('s3://'):]

        bucket_path = Path(base_path)
        path = (bucket_path / f'{key}').as_posix()

        return f"s3://{path}" if s3 else path

    def _get_schema(self, context):
        # if not self._catalogue_dataset:
        #     return {}
        
        table = context.asset_key.path

        # using schema = foo and table = bar as examples when neccesary
        # nothing supplied uses default schema with asset table name
        # schema = default, table = bar
        # just the schema prefix used if no primary asset key
        # schema = foo table = bar
        # schema prefixed if supplied 
        # schema = prefix_foo table = bar
        schema = ''
        if len(table) == 1:
            table, *_ = table
        elif len(table)==2:
            schema, table = table
        else:
            raise NotImplementedError(
                'asset path must be maximum depth of 2 '
                f'got {table}'
            )

        if prefix:= self._schema_prefix:
            if schema:
                schema = f"{prefix}_{schema}"
            else:
                schema = prefix
        else:
            # schema = schema or 'default'
            schema = schema or 'midi'
        
        DBInfo = namedtuple("DBInfo", ('catalog', 'schema', 'table')) #not YAGNI
        return DBInfo(None, schema, table)


    def get_partition_filter(
            self, context: Union[InputContext,
                                 OutputContext]) -> Callable[[dict], bool]:
        
        if not context.has_asset_partitions:
            context.log.debug(f"Found no partition definition...")
            return None
        
        assert hasattr(context.asset_partitions_def, 'name'), 'please set name on the parition definition, eg `def.name = "something"`'
        
        return self._get_partition_filter(context, context.asset_partitions_def)
    
    def _get_partition_filter(self,
        context: Union[InputContext, OutputContext],
        asset_partitions_def
    ):
        context.log.info(asset_partitions_def)
        if isinstance(asset_partitions_def,  TimeWindowPartitionsDefinition):

            context.log.debug(f"Found time partition definition...")
            return self._handle_time_partition(context, asset_partitions_def)

        elif isinstance(asset_partitions_def, StaticPartitionsDefinition):

            context.log.debug(f"Found static partition definition...")
            return self._handle_static_partition(context, asset_partitions_def)

        elif isinstance(asset_partitions_def, MultiPartitionsDefinition):
            context.log.debug(f"Found multi partition definition...")
            return self._handle_multi_partition(context, asset_partitions_def)

        else:
            raise ValueError('Unknown Partition definition type')
        
        
        
    def _handle_time_partition(self, context, asset_partitions_def: TimeWindowPartitionsDefinition):
        
        raise NotImplementedError()
        def generic_partition_filter(partitions: dict,
                                     start: pendulum.datetime,
                                     end: pendulum.datetime):# -> Boolean:

            partition_date = pendulum.from_format(partitions[asset_partitions_def.name],
                                                  "YYYY-MM-DD")
            if start <= partition_date < end:
                return True
            return False

        start, end = (pendulum.instance(t) for t in context.asset_partitions_time_window)

        partition_filter = partial(generic_partition_filter,
                                   start=start,
                                   end=end)
        return partition_filter
    
    def _handle_static_partition(self, context: Union[InputContext,
                                 OutputContext], asset_partitions_def: StaticPartitionsDefinition):
        def generic_partition_filter(partitions: dict):# -> Boolean:
        
            return (asset_partitions_def.name, 'in', range_set),
        
        partition_range = PartitionKeyRange(
                asset_partitions_def.get_first_partition_key(),
                asset_partitions_def.get_last_partition_key(),
        )
        range_set = asset_partitions_def.get_partition_keys_in_range(partition_range)
        
        return generic_partition_filter
    
        
    def _handle_multi_partition(self, context: Union[InputContext,
                                 OutputContext], asset_partitions_def):
        """
        Assumes that the partition columns are named according
        to the MultiPartitionDefintion
        """
        
        def generic_partition_filter(partitions):
            # raise ValueError(partitions )
            return all(p_f(partitions) for p_name, p_f in partition_filters.items())

        partition_def: MultiPartitionsDefinition = asset_partitions_def
        partition_filters = {
                part_def.name: self._get_partition_filter(context, part_def.partitions_def)
                for part_def in partition_def.partitions_defs}
        
        return generic_partition_filter
    
@io_manager(
    config_schema={
        "base_path": Field(StringSource),
        "schema_prefix": Field(StringSource, is_required=False, default_value=""),
        "read_kwargs": Field(dict, is_required=False),
    },
    required_resource_keys={"s3_fs", "trino_connection"},
)
def partitioned_athena_parquet_io_manager(init_context):
    """Persistent IO manager using for parquet
    """
    # optional
    base_path = init_context.resource_config.get("base_path")
    read_kwargs = init_context.resource_config.get("read_kwargs") or {}

    athena_parquet_io_manager = PartitionedParquetIOManager(base_path, read_kwargs=read_kwargs)
    return athena_parquet_io_manager
