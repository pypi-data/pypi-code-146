from datetime import datetime
from datetime import timezone
import fnmatch
import logging
from multiprocessing import Process
import os
from pathlib import Path
import time
from time import sleep

from azure.storage.blob import __version__
from azure.storage.blob import BlobServiceClient
import humanize
from sumtypes import match

from truera.rnn.general.service.container import Locator
from truera.rnn.general.service.sync_service import SyncService
from truera.rnn.general.utils import log
from truera.rnn.general.utils.paths import md5

log.configure(logging.INFO)


def watch_status(fp, remote_size):
    '''
    This is a progress tracker for file downloads. It must be on the file top level as it will be pickled
    in multiprocessing.Process and the pickle expects this method to be top level.
    https://stackoverflow.com/questions/8804830/python-multiprocessing-picklingerror-cant-pickle-type-function 
    '''
    sleep(1)
    while True:
        local_size = fp.stat().st_size
        share = 100 * local_size / remote_size

        print(
            fp,
            humanize.naturalsize(local_size),
            "/",
            humanize.naturalsize(remote_size),
            f"({share:0.2f}%)",
            end='\r'
        )
        sleep(1)


class AZSyncService(SyncService):
    '''
    Interface to communicate with an azure container.
    '''

    def __init__(self, config, **kwargs):
        super(AZSyncService, self).__init__(config)
        if 'container' in kwargs:
            self.az_container_name = kwargs['container']
        else:
            self.az_container_name = config['az']['container']

        if 'az_prefix' in kwargs:
            self.az_repo_prefix = kwargs['az_prefix']
        else:
            self.az_repo_prefix = config['az']['repo_prefix']

        if 'connection_string' in kwargs:
            self.az_connection_string = kwargs['connection_string']
        else:
            self.az_connection_string = config['az']['connection_string']
        if 'ARTIFACT_PROXY_AZURE_SECRET' in self.az_connection_string:
            self.az_connection_string = os.path.expandvars(
                self.az_connection_string
            )
        self.az_client = BlobServiceClient.from_connection_string(
            self.az_connection_string
        )
        self.az_container = self.az_client.get_container_client(
            self.az_container_name
        )

    def push(self, locator: Locator):
        '''
        Pushes the items specified by the locator from the local cache to the backing storage. Use a
        timestamp file to denote when auto pulls should occur. contents will be python's epoch
        time.time()

        '''
        local_cache = super(AZSyncService, self).get_cache_path(locator)
        az_prefix = self.get_repo_path(locator, self.az_repo_prefix)
        files_pushed = 0
        # Single File Push
        if (type(locator) == Locator.Export):
            file_path = os.path.join(local_cache, locator.filename)
            az_dest = os.path.join(az_prefix, locator.filename)
            self.push_file(file_path, az_dest)
            return

        # Folder File Push
        for root, dirs, files in os.walk(local_cache):
            for filename in files:
                file_prefix = os.path.join(root[len(local_cache):], filename)
                file_path = os.path.join(local_cache, file_prefix)
                az_dest = os.path.join(az_prefix, file_prefix)
                if (filename != 'timestamp' and not filename.endswith('.pyc')):
                    self.push_file(file_path, az_dest)
                    files_pushed += 1

        if (files_pushed > 0):
            timestamp_fp = os.path.join(local_cache, 'timestamp')
            with open(timestamp_fp, 'w') as timestamp_file:
                timestamp_file.write(str(time.time()))
            self.push_file(timestamp_fp, os.path.join(az_prefix, 'timestamp'))

    def push_file(self, file_path, az_dest):
        log.info(
            'Starting upload: {} to az://{}'.format(
                file_path, os.path.join(self.az_container_name, az_dest)
            )
        )
        with open(file_path, "rb") as data:
            self.az_container.upload_blob(
                name=az_dest, data=data, overwrite=True
            )
        log.info('Completed upload.')

    def sync(self, locator: Locator, preserve=True, check_time=True):
        '''Sync the items specified by the locator to/from the backing storage to the local cache.
        Presently just syncs from instead of to. Skips remote files that are no newer than local
        cache files.

        Supported locators: artifacts, split, data collections, models.

        '''
        local_cache = Path(super(AZSyncService, self).get_cache_path(locator))
        log.info("Syncing to local cache at {}".format(local_cache))
        az_prefix = self.get_repo_path(locator, self.az_repo_prefix)
        log.info("Azure prefix : {}".format(az_prefix))

        for az_obj in self.az_container.list_blobs(name_starts_with=az_prefix):
            key = az_obj['name']
            fname = az_obj['name'][len(az_prefix):]

            local_fp = local_cache / fname

            size = az_obj['size']
            mod = az_obj['last_modified']
            mod_timestamp = mod.timestamp()

            log.info(
                f"{fname}\t{humanize.naturalsize(size)}\t{humanize.naturaldate(mod)}"
            )

            if not self._need_local_update(az_obj, local_fp, check_time):
                log.info("skipped")
                continue

            self._download(az_obj, local_fp)

    def _download(self, az_obj, fp, preserve=True):
        key = az_obj['name']

        downloader = self.az_container.download_blob(key)

        log.info('Starting Download: {}'.format(fp))

        os.makedirs(os.path.dirname(fp), exist_ok=True)

        remote_size = az_obj['size']

        with open(fp, 'wb') as fh:
            t = Process(target=watch_status, args=[fp, remote_size])
            t.start()
            downloader.download_to_stream(fh)
            t.terminate()

        log.info('Completed Download: {}'.format(fp))

        mod = az_obj['last_modified']
        mod_timestamp = mod.timestamp()

        if preserve:
            os.utime(fp, (mod_timestamp, mod_timestamp))

    @classmethod
    def _need_local_update(cls, az_obj, fp, check_time):
        remote_mod = az_obj['last_modified']
        remote_size = az_obj['size']

        if not fp.exists():
            log.info("Local file does not exist")
            return True

        local_stat = fp.stat()

        if check_time:
            local_mod = datetime.fromtimestamp(
                local_stat.st_mtime, tz=timezone.utc
            )

            if remote_mod > local_mod:
                log.info(
                    f"Remote file is newer ({humanize.naturaldate(remote_mod)} vs {humanize.naturaldate(local_mod)})"
                )
                return True

        else:
            return True

        local_size = local_stat.st_size
        if remote_size != local_size:
            log.info(
                f"Remote and local files differ in size ({humanize.naturalsize(remote_size)} vs {humanize.naturalsize(local_size)})"
            )
            return True

        remote_checksum = az_obj['content_settings']['content_md5']

        if remote_checksum is not None:
            local_checksum = md5(fp)
            if remote_checksum != local_checksum:
                log.info(
                    f"Remote and local files differ in md5 checksum ({remote_checksum} vs {local_checksum})"
                )
                return True
        else:
            log.warning("Remote object does not have a checksum")

        return False

    def pull(self, locator: Locator):
        '''
        Pulls the items specified by the locator from the backing storage to the local cache.
        Supported locators: artifacts, split, data collections, models.
        '''
        super(AZSyncService, self).pull(locator)
        local_cache = Path(super(AZSyncService, self).get_cache_path(locator))

        log.info("Pulling to local cache at {}".format(local_cache))
        az_prefix = self.get_repo_path(locator, self.az_repo_prefix)
        files_pulled = 0
        log.info("Azure prefix : {}".format(az_prefix))
        local_timestamp_fp = os.path.join(local_cache, 'timestamp')
        azure_timestamp_fp = os.path.join(az_prefix, 'timestamp')
        if not os.path.exists(local_timestamp_fp):
            local_timestamp = 0
        else:
            with open(local_timestamp_fp, 'r') as timestamp_file:
                local_timestamp = float(timestamp_file.read())
        try:
            timestamp_downloader = self.az_container.download_blob(
                azure_timestamp_fp
            )
            az_timestamp = float(timestamp_downloader.content_as_text)
        except:
            az_timestamp = 0
        if az_timestamp < local_timestamp:
            log.info('Local cache is already up-to-date.')
            return

        for az_obj in self.az_container.list_blobs(name_starts_with=az_prefix):
            fname = az_obj['name'][len(az_prefix):]
            local_fp = local_cache / fname

            self._download(az_obj, local_fp)
            files_pulled += 1

        if files_pulled == 0:
            log.info('Local cache is already up-to-date.')

    def list_projects(self):
        return self._top_level_list_az(prefix=self.az_repo_prefix, dirs=True)

    def list_artifacts(self, project):
        return [
            name.split('--') for name in self._top_level_list_az(
                os.path.join(self.az_repo_prefix, project, 'artifacts/'),
                dirs=True
            )
        ]

    def list_data_collections(self, project):
        return self._top_level_list_az(
            os.path.join(self.az_repo_prefix, project, 'data_collections/'),
            dirs=True
        )

    def list_datasplits(self, project, data_collection):
        return self._top_level_list_az(
            os.path.join(
                self.az_repo_prefix, project, 'data_collections',
                data_collection + '/'
            ),
            dirs=True
        )

    def list_models(self, project):
        return self._top_level_list_az(
            os.path.join(self.az_repo_prefix, project, 'models/'), dirs=True
        )

    def list_az(self, loc: Locator, dirs=False, match='*', prefix=''):
        files = self._list_az(
            prefix=self.get_repo_path(loc, self.az_repo_prefix) + prefix,
            dirs=dirs
        )

        files = dict(
            filter(lambda kv: fnmatch.fnmatch(kv[0], match), files.items())
        )

        return files

    def _list_az(self, prefix, dirs=False):
        # TODO: figure out what the dir handling was supposed to do as in the S3 version

        az_objects_resp = self.az_container.list_blobs(name_starts_with=prefix)

        all_objects = az_objects_resp

        az_list = dict()

        for az_obj in all_objects:
            key = az_obj['name']
            prefix_stripped = key.replace(prefix, '')

            if '/' in prefix_stripped:
                if dirs:
                    az_list[prefix_stripped] = az_obj
                else:
                    az_list[prefix_stripped[:prefix_stripped.index('/')] +
                            "/"] = az_obj
                    # TODO: az_obj does not describe a directory, it describes the last file inside
                    # it
            else:
                az_list[prefix_stripped] = az_obj

        return az_list

    def _top_level_list_az(self, prefix, dirs=False):
        all_objs = self._list_az(prefix, dirs=dirs)
        az_paths = list(all_objs.keys())
        return set(
            [dirs.split('/')[0] for dirs in az_paths if dirs.split('/')[0]]
        )

    def locs_of_loc_pattern(self, pattern):
        """Return a list of locators matching the given pattern."""
        raise Exception("not implemented")

    def list_files(self, prefix, dirs=False):
        az_objects_resp = self.az_container.list_blobs(name_starts_with=prefix)
        all_objects = az_objects_resp
        az_list = set([])

        for az_obj in all_objects:
            key = az_obj['name']
            prefix_stripped = key.replace(prefix, '')

            if dirs and '/' in prefix_stripped:
                az_list.add(prefix_stripped[:prefix_stripped.index('/')])

            elif not dirs and '/' not in prefix_stripped:
                az_list.add(prefix_stripped)

        return az_list
