#  Copyright 2022 Collate
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""
Great Expectations plugin to send validation results to
Azure blob storage with custom filename and filepath.

This subpackage needs to be used in Great Expectations
checkpoints actions.
"""

import functools
import os
import json
import logging
from typing import Optional, Union

from great_expectations.checkpoint.actions import ValidationAction
from great_expectations.core.batch import Batch
from great_expectations.core.expectation_validation_result import (
    ExpectationSuiteValidationResult,
)
from great_expectations.data_asset.data_asset import DataAsset
from great_expectations.data_context.data_context import DataContext
from great_expectations.data_context.types.resource_identifiers import (
    ExpectationSuiteIdentifier,
    GXCloudIdentifier,
    ValidationResultIdentifier,
)
from great_expectations.exceptions import StoreBackendError
from great_expectations.validator.validator import Validator

from azure.storage.blob import BlobServiceClient
from azure.storage.blob import ContentSettings

logger = logging.getLogger(__name__)

class KadaStoreValidationResultsAction(ValidationAction):
    """Kada Store validation action. It inherits from
    great expection validation action class and implements the
    `_run` method.

    Attributes:
        data_context: great expectation data context
        container: Azure Storage Account container
        connection_string: To connect to the Storage Account. You can find this connection string in
        the Storage Account resource in your Azure account portal.
        prefix: The folder path in your container where the .json blob will be stored.
        account_url: Url for the Azure Storage Account
    """
    # pylint: disable=arguments-differ,unused-argument
    def __init__(
        self,
        data_context: DataContext,
        container,
        connection_string=None,
        prefix=None,
        account_url=None,
        access_key=None
    ):
        super().__init__(data_context)
        self.connection_string = connection_string or os.environ.get(
            "AZURE_STORAGE_CONNECTION_STRING"
        )
        self.prefix = prefix or ""
        self.container = container
        self.account_url = account_url or os.environ.get("SAS_URL")
        self.access_key = access_key or os.environ.get("SAS_TOKEN")

    # pylint: disable=arguments-differ,unused-argument
    def _run(
        self,
        validation_result_suite: ExpectationSuiteValidationResult,
        validation_result_suite_identifier: Union[
            ValidationResultIdentifier, GXCloudIdentifier
        ],
        data_asset: Union[Validator, DataAsset, Batch],
        expectation_suite_identifier: Optional[ExpectationSuiteIdentifier] = None,
        checkpoint_identifier=None,
        payload=None,
    ):
        """main function to implement great expectation hook

        Args:
            validation_result_suite: result suite returned when checkpoint is ran
            validation_result_suite_identifier: type of result suite
            data_asset:
            payload:
            expectation_suite_identifier: type of expectation suite
            checkpoint_identifier: identifier for the checkpoint
        """
        logger.debug("KadaStoreValidationAction.run")

        if validation_result_suite is None:
            logger.warning(
                'No validation_result_suite was passed to %s action. Skipping action.', type(self).__name__
            )
            return

        if not isinstance(
            validation_result_suite_identifier,
            (ValidationResultIdentifier, GXCloudIdentifier),
        ):
            raise TypeError(
               "validation_result_id must be of type ValidationResultIdentifier or GeCloudIdentifier, not {}".format(
                    type(validation_result_suite_identifier)
                )
            )

        batch_id = validation_result_suite_identifier.batch_identifier
        run_name = validation_result_suite_identifier.run_id.run_name

        json_dict = validation_result_suite.to_json_dict()

        file_name = ''.join([batch_id,'_expectation_result_',run_name,'.json'])

        # UNCOMMENT TO TEST THIS PLUGIN IN YOUR LOCAL FILESYSTEM
        # os.makedirs("great_expectations/uncommitted/lz/ge_landing/landing", exist_ok=True)
        # file_key = os.path.join("great_expectations/uncommitted/lz/ge_landing/landing", file_name)
        # print(validation_result_suite)

        json_object = json.dumps(json_dict, indent=2)
        # UNCOMMENT TO TEST THIS PLUGIN IN YOUR LOCAL FILESYSTEM
        # with open(file_key, "w") as outfile:
        #     outfile.write(json_object)
        self.set(file_name, json_object)

    @property
    @functools.lru_cache()
    def _container_client(self):

        if self.connection_string:
            blob_service_client = BlobServiceClient.from_connection_string(
                self.connection_string
            )
        elif self.account_url:
            blob_service_client = BlobServiceClient(
                account_url=self.account_url, credential=self.access_key
            )
        else:
            raise StoreBackendError(
                "Unable to initialize ServiceClient, credentials should be set"
            )

        return blob_service_client.get_container_client(self.container)

    def set(self, key, value, content_encoding="utf-8", **kwargs):
        """Set function to upload validation results to Azure Blob Storage

        Args:
            key: Filename for the validation results JSON
            value: Validation Results object to write in the JSON
        """

        az_blob_key = os.path.join(self.prefix, key)

        if isinstance(value, str):
            if az_blob_key.endswith(".html"):
                my_content_settings = ContentSettings(content_type="text/html")
                self._container_client.upload_blob(
                    name=az_blob_key,
                    data=value,
                    encoding=content_encoding,
                    overwrite=True,
                    content_settings=my_content_settings,
                )
            else:
                self._container_client.upload_blob(
                    name=az_blob_key,
                    data=value,
                    encoding=content_encoding,
                    overwrite=True,
                )
        else:
            self._container_client.upload_blob(
                name=az_blob_key, data=value, overwrite=True
            )
        return az_blob_key
