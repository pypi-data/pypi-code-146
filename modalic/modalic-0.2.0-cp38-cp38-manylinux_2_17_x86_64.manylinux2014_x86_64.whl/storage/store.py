#  Copyright (c) modalic 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.

from typing import Any, Dict, Optional

from minio import Minio

from modalic.config import Conf

# from minio.error import S3Error


class Storage:
    r"""Instantiate Storage Object that enables access to S3 layer.

    :param conf: Custom modalic configuration object containing the settings for
        using the external stroring service.
    """

    def __init__(self, conf: Conf = Conf()):
        self.conf = conf
        self.client = Minio(
            endpoint=conf.s3_endpoint,
            access_key=conf.s3_access_key,
            secret_key=conf.s3_secret_access_key,
            secure=False,
        )

    def upload(
        self,
        object: Any,
        object_name: str,
        length: int = -1,
        metadata: Optional[Dict[Any, Any]] = None,
    ) -> None:
        r"""Uploads data object to s3 storage bucket."""
        self.client.put_object(
            self.conf.bucket, object_name, object, length=length, metadata=metadata
        )

    # def create_bucket(self):
    #     r"""Instantiates and creates new bucket where all the object will be stored."""
    #     pass
