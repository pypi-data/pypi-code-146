# -*- coding: utf-8 -*-
""" Read from an S3 Bucket """


from boto3.resources.factory import ServiceResource

from baseblock import FileIO
from baseblock import BaseObject


class S3BucketReader(BaseObject):
    """ Read from an S3 Bucket """

    def __init__(self,
                 s3: ServiceResource):
        """ Change Log

        Created:
            25-Jul-2022
            craigtrim@gmail.com
            *   in pursuit of
                https://bast-ai.atlassian.net/browse/COR-11
        """
        BaseObject.__init__(self, __name__)
        self._s3 = s3

    def process(self,
                bucket_name: str,
                file_name: str,
                load_files: bool) -> dict or None:
        """ Open and Read S3 Files

        Args:
            bucket_name (str): the name of the S3 bucket
            file_name (str): the file name (or prefix) to search for
            load_files (bool): load the contents of the input files
                if None, the keyed value will be None

        Returns:
            dict: a dictionary of file contents keyed by file name
        """

        s3_bucket = self._s3.Bucket(bucket_name)

        files = [x for x in s3_bucket.objects.filter(Prefix=file_name)]

        d_files = {}
        for file in files:

            if not load_files:  # consumer just wants file paths, not contents
                d_files[file.key] = None
                continue

            data = file.get()['Body'].read().decode(encoding='utf-8',
                                                    errors='ignore')

            if file.key.endswith('.yaml') or file.key.endswith('.yml'):
                data = FileIO.parse_yaml(data)
            elif file.key.endswith('json'):
                data = FileIO.parse_json(data)

            d_files[file.key] = data

        return d_files
