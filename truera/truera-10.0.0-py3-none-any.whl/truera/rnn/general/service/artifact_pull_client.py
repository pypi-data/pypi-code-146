import argparse
import sys
import time

sys.path.append('..')
from container import Locator
from sync_client import SyncClient

if __name__ == '__main__':
    help_string = "Server to pull artifacts from s3 or az"
    parser = argparse.ArgumentParser(description=help_string)
    parser.add_argument('--project', type=str, help=('The project name'))
    parser.add_argument(
        '--backend',
        type=str,
        default="s3",
        help=('The backend storage system. Currently only supports s3, az')
    )
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help=(
            'The config containing the cache paths and connection parameters'
        )
    )

    args_cmd = parser.parse_args()

    if (args_cmd.config is None):
        sync_client = SyncClient(args_cmd.backend)
    else:
        sync_client = SyncClient(args_cmd.backend, config_path=args_cmd.config)

    while (True):
        for project in sync_client.sync_service.list_projects():
            for artifact in sync_client.sync_service.list_artifacts(project):

                data_collection = artifact[0]
                split = artifact[1]
                model = artifact[2]
                sync_client.sync_service.pull(
                    Locator.Artifact(project, model, data_collection, split)
                )

        time.sleep(600)
