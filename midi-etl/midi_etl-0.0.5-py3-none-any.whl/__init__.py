from importlib.resources import files
from pathlib import Path
from dagster import repository, with_resources
from dagster_dbt import dbt_cli_resource as dbt
import yaml
from midi_etl.arrow_upath_iomanager import arrow_io_manager
from . import constants
from midi_etl.resources.s3_fs import s3_fs
from midi_etl.resources.trino import trino_connection
from dagstermill import local_output_notebook_io_manager
from .jobs import jobs
from .assets.dbt import assets as dbt_assets
from .assets import assets
from .resources.duckdb import duckdb
# @repository
# def lakh_midi():



#     return [*with_resources(
#             assets,
#             resource_defs={
#                 's3_fs': s3_fs,
#                 'partitioned_parquet_manager': partitioned_athena_parquet_io_manager,
#                 'trino_connection': trino_connection
#             }
#         ),
#         *jobs
#         ]

@repository
def midi_etl():

    root = files('midi_etl') / '..'
    conf = yaml.safe_load(Path('basic_config.yaml').read_text())

    return [*with_resources(
            (*assets, *dbt_assets),
            resource_defs={
                'partitioned_parquet_manager': arrow_io_manager.configured(
                    conf['resources']['partitioned_parquet_manager']['config']
                ),
                'trino_connection': trino_connection,
                's3_fs': s3_fs,
                'dbt': dbt.configured({
                    'profiles_dir': root.as_posix(),
                    'project_dir': (root/'midi_etl_dbt').as_posix(),

                }),
                'duckdb_midi_conn': duckdb.configured({
                    'schema': 'midi',
                    'read_only': False
                }),
                "output_notebook_io_manager": local_output_notebook_io_manager,
            }
        ),
        *jobs
        ]
