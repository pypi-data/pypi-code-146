from collections import namedtuple
from pathlib import Path
import pyarrow.compute as pc
from functools import partial
from itertools import repeat
from typing import Dict, Optional, Union
from dagster import Field, InputContext, MultiPartitionKey, MultiPartitionsDefinition, OutputContext, PartitionsDefinition, StaticPartitionsDefinition, StringSource, UPathIOManager, io_manager
import pandas as pd
from upath import UPath
from pyarrow import dataset as ds
import pyarrow as pa

DF_TYPES = Union[pd.DataFrame, pa.Table] # TODO other df types


def require_asset(f):
    def f_inner(self, context: Union[OutputContext, InputContext], *args, **kwargs):
        assert context.has_asset_key, 'only for assets'
        return f(self, context, *args, **kwargs)

    return f_inner


class PartitionedArrrowIOManager(UPathIOManager):

    def __init__(self, base_path: str, client_kwargs=None, catalog=True, schema_prefix=''):

        base_path = UPath(base_path, client_kwargs=client_kwargs)
        super().__init__(base_path)

        self.catalog = catalog
        self.schema_prefix = schema_prefix


    def _get_paths_for_partitions(
        self, context: Union[InputContext, OutputContext]
    ) -> Dict[str, UPath]:
        """
        Returns a dict of partition_keys into I/O paths for a given context.
        """
        if not context.has_asset_partitions:
            raise TypeError(
                f"Detected {context.dagster_type.typing_type} input type "
                f"but the asset is not partitioned"
            )

        partition_keys = context.asset_partition_keys
        asset_path = self._get_path_without_extension(context)
        return {
            partition_key: asset_path
            for partition_key in partition_keys
        }
        
    @require_asset
    def dump_to_path(self, context: OutputContext, obj: DF_TYPES, path: UPath):
        """Child classes should override this method to write the object to the filesystem."""
        # if type(obj) in  DF_TYPES:
        #     raise Exception(f"Outputs of type {type(obj)} not supported.")
        context.log.info(f'Got {len(obj.index)} records...')
        context.log.info(f'Got {obj.columns} columns...')
        context.log.info(f'Got {obj.dtypes} dtypes...')
        context.log.info(obj.head(5))

        partition_columns = self.get_partitions(context)
        
        ds.write_dataset(
            pa.Table.from_pandas(obj),
            str(path),
            partitioning=partition_columns,
            format='parquet',
            existing_data_behavior=self.get_existing_data_behaviour(context),
            filesystem=context.resources.s3_fs,
            partitioning_flavor='hive'
        )

        if self.catalog and len(obj.index)>0: #TODO add dtypes to pd dataframes at creation
            self._generate_ddl(context, obj, path, partition_columns)

    @require_asset
    def load_from_path(self, context: InputContext, path: UPath) -> DF_TYPES:
        context.log.debug(f'Writing to {str(path).split("//")[-1]}')
        # raise ValueError(path)
        df = ds.dataset(
            str(path).split('//')[-1],
            filesystem=context.resources.s3_fs,
            partitioning='hive',
            format="parquet"
        )
        if context.metadata.get('as_type', 'pandas')=='dataset':
            return df
        
        df = df.to_table(
            filter = self.get_partition_filters(context), 
            columns=self.get_columns(context),
        )
        if (as_type:=context.metadata.get('as_type', 'pandas'))=='arrow':
            return df   
        elif as_type == 'pandas':
        
            return df.to_pandas()
        else:
            raise ValueError(f"unknown type '{as_type}'")

    def get_partitions(self, context: Union[OutputContext, InputContext]):
        
        if not context.has_partition_key:
            return None

        partition_def = context.asset_partitions_def
        
        if isinstance(partition_def, StaticPartitionsDefinition):
            return [partition_def.name]
        elif isinstance(partition_def, MultiPartitionsDefinition):
            return [dim.name for dim in partition_def.partitions_defs]
        else:
            raise ValueError(f'Unkown partition type {partition_def.__class__}')


    def get_partition_filters(self, context: InputContext):

        if not context.has_asset_partitions:
            return None

        def partition_filters(partition_key, partition_def: PartitionsDefinition):# -> Boolean:

            if isinstance(partition_def, MultiPartitionsDefinition):
                partition_key: MultiPartitionKey = partition_key
                return all(map(partition_filters, partition_key.keys_by_dimension[partition_def.name], partition_def.partitions_defs))
            

            if isinstance(partition_def, StaticPartitionsDefinition):
                return pc.field(partition_def.name).isin([partition_key])
            else:
                raise ValueError(f'Unknown partition definition {partition_def.__class__}')

        return  partition_filters(
                context.partition_key, 
                context.asset_partitions_def
            )


    def get_columns(self, context):
        columns = context.metadata.get("columns")
        if columns is not None:
            context.log.debug(
                f"{self.__class__} received metadata value columns={columns}")
        return columns

    def get_existing_data_behaviour(self, context):

        return 'delete_matching'


    def _get_schema(self, context):

        path = context.asset_key.path
        if len(path) == 1:
            schema = ''
            table = path[0]
        elif len(path) == 2:
            schema, table = path
        else:
            raise ValueError()


        if prefix:= self.schema_prefix:
            schema = f"{prefix}_{schema}"
        else:
            # schema = schema or 'default'
            schema = schema or context.resources.trino_connection.schema
        
        DBInfo = namedtuple("DBInfo", ('catalog', 'schema', 'table')) 
        return DBInfo(None, schema, table)

    def _generate_ddl(self, context, df: pd.DataFrame, path, partition_columns):
        _, schema, table = self._get_schema(context)
        #TODO schema not currently used
        # if schema is not None:
        #     table = f'{schema}.{table}'
        conn = context.resources.trino_connection
        ddl_path = Path(context.metadata.get('ddl_path', None))

        if not ddl_path:
            return

        path = str(path)

        ddl = f"""
            {ddl_path.read_text().replace('CREATE TABLE', "CREATE TABLE IF NOT EXISTS")}
            WITH (
                external_location = '{path.replace('s3', 's3a')}',
                {f"partitioned_by = ARRAY{partition_columns}" if partition_columns else ""}

            )
        """

        context.log.debug("DDL")
        context.log.debug(ddl)

        cur = conn.cursor()
        cur.execute(ddl)
        context.log.debug(f"Sync results: {cur.fetchall()}")



@io_manager(
    config_schema={
        "base_path": Field(StringSource),
        "endpoint_url": Field(StringSource, is_required=False)
    },
    required_resource_keys={"s3_fs", "trino_connection"}, # TODO shouldnt be required
)
def arrow_io_manager(init_context):
    """Persistent IO manager arrow
    """
    base_path = init_context.resource_config["base_path"]
    endpoint_url = init_context.resource_config.get("endpoint_url")

    client_kwargs = {
        'endpoint_url': endpoint_url
    }

    athena_parquet_io_manager = PartitionedArrrowIOManager(base_path, client_kwargs=client_kwargs)
    return athena_parquet_io_manager
