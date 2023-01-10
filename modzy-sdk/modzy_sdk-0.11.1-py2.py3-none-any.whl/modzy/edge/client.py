import logging

import grpc

from .inferences import EdgeInferenceClient
from .jobs import EdgeJobsClient


class EdgeClient:
    """The Edge API client object.

    This class is used to interact with the Modzy Edge API.

    Attributes:
        host (str): The host for the Modzy Edge API.
        port (int): The port on which Modzy Edge is listening.
    """

    def __init__(self, host, port):
        """Creates an `ApiClient` instance.

        Args:
            host (str): The host for the API.
            port (int): Port for the API.
        """
        self.logger = logging.getLogger(__name__)
        self.host = host
        self.port = port
        self.origin = '{}:{}'.format(self.host, self.port)
        self._channel = None
        self.jobs: EdgeJobsClient | None = None
        self.inferences: EdgeInferenceClient | None = None

    def connect(self):
        if self._channel is None:
            self._channel = grpc.insecure_channel(self.origin)
            self.jobs = EdgeJobsClient(self._channel, origin=self.origin)
            self.inferences = EdgeInferenceClient(self._channel, origin=self.origin)
        return self

    def close(self):
        self._channel.close()

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.close()

    def submit_embedded(self, identifier, version, sources, explain=False):
        """Submits a job containing embedded data.

        Args:
            identifier (str): The model identifier.
            version (str): The model version string.
            sources (dict): A mapping of source names to text sources. Each source should be a
                mapping of model input filename to filepath or file-like object.
            explain (bool): indicates if you desire an explainable result for your model.`

        Returns:
            str: Job identifier returned by Modzy Edge.

        Raises:
            ApiError: An ApiError will be raised if the API returns an error status,
                or the client is unable to connect.

            Example:
                .. code-block::

                    job = client.submit_embedded('model-identifier', '1.2.3',
                    {
                        'source-name-1': {
                            'model-input-name-1': b'some bytes',
                            'model-input-name-2': bytearray([1,2,3,4]),
                        },
                        'source-name-2': {
                            'model-input-name-1': b'some bytes',
                            'model-input-name-2': bytearray([1,2,3,4]),
                        }
                    })

        """
        self.logger.warning("Deprecated. Use EdgeClient.jobs.submit_embedded().")
        self.connect()
        return self.jobs.submit_embedded(identifier, version, sources, explain)

    def submit_text(self, identifier, version, sources, explain=False):
        """Submits text data for a multiple source `Job`.

        Args:
            identifier (str): The model identifier.
            version (str): The model version string.
            sources (dict): A mapping of source names to text sources. Each source should be a
                mapping of model input filename to filepath or file-like object.
            explain (bool): indicates if you desire an explainable result for your model.`

        Returns:
            str: Job identifier returned by Modzy Edge.

        Raises:
            ApiError: An ApiError will be raised if the API returns an error status,
                or the client is unable to connect.

            Example:
                .. code-block::

                    job = client.submit_text('model-identifier', '1.2.3',
                    {
                        'source-name-1': {
                            'model-input-name-1': 'some text',
                            'model-input-name-2': 'some more text',
                        },
                        'source-name-2': {
                            'model-input-name-1': 'some text 2',
                            'model-input-name-2': 'some more text 2',
                        }
                    })

        """
        self.logger.warning("Deprecated. Use EdgeClient.jobs.submit_text().")
        self.connect()
        return self.jobs.submit_text(identifier, version, sources, explain)

    def submit_aws_s3(self, identifier, version, sources, access_key_id, secret_access_key, region, explain=False):
        """Submits AwS S3 hosted data for a multiple source `Job`.

        Args:
            identifier (str): The model identifier or a `Model` instance.
            version (str): The model version string.
            sources (dict): A mapping of source names to text sources. Each source should be a
                mapping of model input filename to S3 bucket and key.
            access_key_id (str): The AWS Access Key ID.
            secret_access_key (str): The AWS Secret Access Key.
            region (str): The AWS Region.
            explain (bool): indicates if you desire an explainable result for your model.`

        Returns:
            str: Job identifier returned by Modzy Edge.

        Raises:
            ApiError: An ApiError will be raised if the API returns an error status,
                or the client is unable to connect.

            Example:
                .. code-block::

                    job = client.submit_aws_s3('model-identifier', '1.2.3',
                    {
                        'source-name-1': {
                            'model-input-name-1': {
                                'bucket': 'my-bucket',
                                'key': '/my/data/file-1.dat'
                            },
                            'model-input-name-2': {
                                'bucket': 'my-bucket',
                                'key': '/my/data/file-2.dat'
                            }
                        },
                        'source-name-2': {
                            'model-input-name-1': {
                                'bucket': 'my-bucket',
                                'key': '/my/data/file-3.dat'
                            },
                            'model-input-name-2': {
                                'bucket': 'my-bucket',
                                'key': '/my/data/file-4.dat'
                            }
                        }
                    },
                        access_key_id='AWS_ACCESS_KEY_ID',
                        secret_access_key='AWS_SECRET_ACCESS_KEY',
                        region='us-east-1',
                    )
        """
        self.logger.warning("Deprecated. Use EdgeClient.jobs.submit_aws_s3().")
        self.connect()
        return self.jobs.submit_aws_s3(identifier, version, sources, access_key_id, secret_access_key, region, explain)

    def get_job_details(self, job_identifier):
        """Get job details.

        Args:
            job_identifier (str): The job identifier.

        Returns:
            dict: Details for requested job.

        Raises:
            ApiError: An ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        self.logger.warning("Deprecated. Use EdgeClient.jobs.get_job_details().")
        self.connect()
        return self.jobs.get_job_details(job_identifier)

    def get_all_job_details(self, timeout=None):
        """Get job details for all jobs.

        Args:
            timeout (int): Optional timeout value in seconds.

        Returns:
            dict: Details for all jobs that have been run.

        Raises:
            ApiError: An ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        self.logger.warning("Deprecated. Use EdgeClient.jobs.get_all_job_details().")
        self.connect()
        return self.jobs.get_all_job_details(timeout)

    def block_until_complete(self, job_identifier, poll_interval=0.01, timeout=30):
        """Block until job complete.

        Args:
            job_identifier (str): The job identifier.

        Returns:
            dict: Final job details.

        Raises:
            ApiError: An ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        self.logger.warning("Deprecated. Use EdgeClient.jobs.block_until_complete().")
        self.connect()
        self.jobs.block_until_complete(job_identifier, poll_interval, timeout)

    def get_results(self, job_identifier):
        """Block until job complete.

        Args:
            job_identifier (str): The job identifier.

        Returns:
            dict: Results for the requested job.

        Raises:
            ApiError: An ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        self.logger.warning("Deprecated. Use EdgeClient.jobs.get_results().")
        self.connect()
        return self.jobs.get_results(job_identifier)
