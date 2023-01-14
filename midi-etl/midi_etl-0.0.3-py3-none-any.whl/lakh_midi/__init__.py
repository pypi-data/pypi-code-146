from importlib.resources import files
from dagster import repository, with_resources
from dagster_dbt import dbt_cli_resource as dbt
from lakh_midi.partitioned_parquet_io import partitioned_athena_parquet_io_manager

from lakh_midi.resources.s3_fs import s3_fs
from lakh_midi.resources.trino import trino_connection
from .assets import assets
from .jobs import jobs
from .assets.dbt import assets as dbt_assets

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
def lakh_midi_dbt():


    root = files('lakh_midi') / '..'

    return [*with_resources(
            (*assets, *dbt_assets),
            resource_defs={
                'partitioned_parquet_manager': partitioned_athena_parquet_io_manager,
                'trino_connection': trino_connection,
                's3_fs': s3_fs,
                'dbt': dbt.configured({
                    'profiles_dir': root.as_posix(),
                    'project_dir': (root/'lakh_midi_dbt').as_posix(),

                })
            }
        ),
        *jobs
        ]
