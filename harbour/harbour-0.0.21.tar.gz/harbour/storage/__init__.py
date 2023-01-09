import gzip
import io
import os
import uuid

import boto3


class Bucket:

    def __init__(self, bucket):

        self.name = os.getenv(bucket) or bucket
        self.client = boto3.client('s3', region_name='us-east-1')

    def scan(self, prefix='', *args, **kwargs):
        """Returns all the keys in a given prefix"""

        keys = []
        token = None

        while True:

            if token:

                response = self.client.list_objects_v2(
                    Bucket=self.name,
                    Prefix=prefix,
                    ContinuationToken=token,
                    MaxKeys=1000
                )

            else:

                response = self.client.list_objects_v2(
                    Bucket=self.name,
                    Prefix=prefix,
                    MaxKeys=1000
                )

            keys.extend(
                [c['Key'] for c in response.get('Contents', [])]
            )

            # Gets the next token iteration or breaks the loop
            token = response.get('NextContinuationToken', None)

            if token is None:
                break

        return keys

    def upload(self, filename, key, compress=False, delete=False, *args, **kwargs):
        """Uploads a file to the storage"""

        if not os.path.exists(filename):

            msg = 'The file {} could not be found'.format(filename)

            raise FileNotFoundError(msg)

        client = boto3.client('s3')

        if compress:

            # Defines a unique ID for the upload
            tmp_path = '/tmp/{}.gz'.format(uuid.uuid4().hex)

            # Writes the file as gzip
            with gzip.open(tmp_path, 'wt+') as gz:

                with open(filename, 'r') as file:

                    gz.write(file.read())

            # Sanitizes the key
            key += '.gz' if not key.endswith('.gz') else ''

            # Uploads the file
            response = client.upload_file(
                Filename=tmp_path,
                Bucket=self.name,
                Key=key
            )

            # Removes the temp file from disk
            os.remove(tmp_path)

        else:

            # Uploads the file
            response = client.upload_file(
                Filename=filename,
                Bucket=self.name,
                Key=key
            )

        # Removes the source file from disk
        if delete:

            os.remove(filename)

        return 's3://{}/{}'.format(self.name, key)

    def download(self, key, filename, overwrite=False, *args, **kwargs):
        """Downloads a key from the bucket and save as filename"""

        # Deletes the file before downloading
        if overwrite:
            try:
                os.remove(filename)
            except FileNotFoundError:
                pass

        response = self.client.download_file(
            Bucket=self.name,
            Key=key,
            Filename=filename
        )

        return filename

    def delete(self, keys, *args, **kwargs):
        """Deletes all the keys specified"""

        batch = []
        for key in keys:

            batch.append(key)

            # Hard limit of 1000 keys per call. Do not change it.
            if len(batch) == 1000:

                response = self.client.delete_objects(
                    Bucket=self.name,
                    Delete={
                        'Objects': [
                            {
                                'Key': k,
                            } for k in batch
                        ],
                    }
                )

                batch = []

        # Deletes the residual records
        else:
            response = self.client.delete_objects(
                Bucket=self.name,
                Delete={
                    'Objects': [
                        {
                            'Key': k,
                        } for k in batch
                    ],
                }
            )
