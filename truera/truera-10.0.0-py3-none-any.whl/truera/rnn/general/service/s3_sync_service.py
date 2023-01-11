import os
import time

import boto3
import progressbar
from sumtypes import match

from truera.rnn.general.service.container import Locator
from truera.rnn.general.service.sync_service import SyncService
from truera.rnn.general.utils import log


class S3SyncService(SyncService):
    '''
    Interface to communicate with the repo. Current supported backends are local and s3
    '''

    def __init__(self, config, **kwargs):
        super(S3SyncService, self).__init__(config)
        if ('bucket' in kwargs):
            self.s3_bucket = kwargs['bucket']
        else:
            self.s3_bucket = config['s3']['bucket']

        if ('s3_prefix' in kwargs):
            self.s3_repo_prefix = kwargs['s3_prefix']
        else:
            self.s3_repo_prefix = config['s3']['repo_prefix']

        self.boto_client = boto3.client('s3')

    def push(self, locator: Locator):
        '''
        Pushes the items specified by the locator from the local cache to the backing storage.
        Use a timestamp file to denote when auto pulls should occur. contents will be python's epoch time.time()
        '''
        local_cache = super(S3SyncService, self).get_cache_path(locator)
        s3_prefix = self.get_repo_path(locator, self.s3_repo_prefix)

        files_pushed = 0

        # Single File Push
        if (type(locator) == Locator.Export):
            file_path = os.path.join(local_cache, locator.filename)
            s3_dest = os.path.join(self.s3_repo_prefix, locator.filename)
            self.push_file(file_path, s3_dest)
            return

        # Folder File Push
        for root, dirs, files in os.walk(local_cache):
            for filename in files:
                file_prefix = os.path.join(root[len(local_cache):], filename)
                file_path = os.path.join(local_cache, file_prefix)
                s3_dest = os.path.join(s3_prefix, file_prefix)
                if (filename != 'timestamp' and not filename.endswith('.pyc')):
                    self.push_file(file_path, s3_dest)
                    files_pushed += 1

        if (files_pushed > 0):
            with open(
                os.path.join(local_cache, 'timestamp'), 'w+'
            ) as timestamp_file:
                timestamp_file.write(str(time.time()))
            self.boto_client.upload_file(
                os.path.join(local_cache, 'timestamp'), self.s3_bucket,
                os.path.join(s3_prefix, 'timestamp')
            )

    def push_file(self, file_path, s3_dest):
        log.info(
            'Starting upload: ' + file_path + ' to s3://' +
            os.path.join(self.s3_bucket, s3_dest)
        )
        progress = progressbar.ProgressBar(maxval=os.stat(file_path).st_size)

        progress.start()

        def progress_chunk(chunk):
            progress.update(progress.currval + chunk)

        self.boto_client.upload_file(
            file_path, self.s3_bucket, s3_dest, Callback=progress_chunk
        )

        progress.finish()
        log.info('Completed upload: ' + file_path)

    def pull(self, locator: Locator):
        '''
        Pulls the items specified by the locator from the backing storage to the local cache
        Use a timestamp file to denote when auto pulls should occur. contents will be python's epoch time.time()
        current supported locators: artifacts, split
        '''
        super(S3SyncService, self).pull(locator)
        local_cache = super(S3SyncService, self).get_cache_path(locator)
        s3_prefix = self.get_repo_path(locator, self.s3_repo_prefix)
        try:
            s3_timestamp = float(
                boto3.resource('s3').Object(
                    self.s3_bucket, os.path.join(s3_prefix, 'timestamp')
                ).get()['Body'].read().decode('utf-8')
            )
        except self.boto_client.exceptions.NoSuchKey:
            log.info("Could not find the timestamp indicator in " + s3_prefix)
            return
        try:
            with open(
                os.path.join(local_cache, 'timestamp'), 'r'
            ) as timestamp_file:
                local_timestamp = float(timestamp_file.read())
        except FileNotFoundError:
            local_timestamp = 0
        if (local_timestamp < s3_timestamp):
            os.makedirs(local_cache, exist_ok=True)
            files_pulled = 0
            for s3_obj in self.boto_client.list_objects(
                Bucket=self.s3_bucket, Prefix=s3_prefix
            )['Contents']:
                key = s3_obj['Key']
                filename = key[(key.rfind('/') + 1):]
                if (filename != 'timestamp'):
                    log.info('Starting Download: ' + key)
                    progress = progressbar.ProgressBar(maxval=s3_obj['Size'])

                    progress.start()

                    def progress_chunk(chunk):
                        progress.update(progress.currval + chunk)

                    self.boto_client.download_file(
                        self.s3_bucket,
                        key,
                        os.path.join(local_cache, filename),
                        Callback=progress_chunk
                    )

                    progress.finish()
                    log.info('Completed Download: ' + key)
                    files_pulled += 1
            if (files_pulled > 0):
                with open(local_cache + 'timestamp', 'w') as timestamp_file:
                    timestamp_file.write(str(s3_timestamp))
        else:
            log.info(
                "Current local cache '" + local_cache +
                "' is detected to be up to date"
            )

    def list_projects(self):
        return self._list_s3(self.s3_repo_prefix, dirs=True)

    def list_artifacts(self, project):
        return [
            name.split('--') for name in self._list_s3(
                os.path.join(self.s3_repo_prefix, project, 'artifacts/'),
                dirs=True
            )
        ]

    def list_data_collections(self, project):
        return self._list_s3(
            os.path.join(self.s3_repo_prefix, project, 'data_collections/'),
            dirs=True
        )

    def list_datasplits(self, project, data_collection):
        return self._list_s3(
            os.path.join(
                self.s3_repo_prefix, project, 'data_collections',
                data_collection + '/'
            ),
            dirs=True
        )

    def list_models(self, project):
        return self._list_s3(
            os.path.join(self.s3_repo_prefix, project, 'models/'), dirs=True
        )

    def _list_s3(self, prefix, dirs=False):
        s3_objects_resp = self.boto_client.list_objects(
            Bucket=self.s3_bucket, Prefix=prefix
        )
        if ('Contents' not in s3_objects_resp):
            return []
        all_objects = s3_objects_resp['Contents']
        s3_list = set([])
        for s3_obj in all_objects:
            key = s3_obj['Key']
            prefix_stripped = key.replace(prefix, '')
            if (dirs and '/' in prefix_stripped):
                s3_list.add(prefix_stripped[:prefix_stripped.index('/')])
            elif (not dirs and '/' not in prefix_stripped):
                s3_list.add(prefix_stripped)
        return s3_list
