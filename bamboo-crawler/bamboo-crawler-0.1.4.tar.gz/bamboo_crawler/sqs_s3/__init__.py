import functools
import hashlib
import json
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple, Union

import boto3

from ..interfaces.context import Context
from ..interfaces.inputter import Inputter
from ..interfaces.outputter import Outputter

SQSQueue = Any
S3Bucket = Any
SQSMessage = Any


@dataclass
class SQSS3Inputter(Inputter[bytes]):
    bucket_name: str
    queue_name: str
    s3_config: Dict[str, Any] = field(default_factory=dict)
    sqs_config: Dict[str, Any] = field(default_factory=dict)
    message: Optional[SQSMessage] = None

    @functools.cached_property
    def queue(self) -> SQSQueue:
        sqs = boto3.resource("sqs", **self.sqs_config)
        queue = sqs.get_queue_by_name(QueueName=self.queue_name)
        return queue

    @functools.cached_property
    def bucket(self) -> S3Bucket:
        s3 = boto3.resource("s3", **self.s3_config)
        return s3.Bucket(self.bucket_name)

    def read(self) -> Context[bytes]:
        message = self.__read_sqs()
        body, meta = self.__read_s3(message)
        return Context(body, **meta)

    def __read_sqs(self) -> SQSMessage:
        if self.message is not None:
            return self.message

        messages = list(self.queue.receive_messages())
        while not messages:
            time.sleep(5)
            messages = list(self.queue.receive_messages())

        message = messages[0]
        self.message = message
        return message

    def __read_s3(self, message: SQSMessage) -> Tuple[bytes, Dict[str, Any]]:
        j = json.loads(message.body)
        obj = self.bucket.Object(j["s3_body"])
        metadata = j["metadata"]
        response = obj.get()
        return response["Body"].read(), metadata

    def done(self) -> None:
        super().done()
        if self.message is not None:
            self.message.delete()
            self.message = None


class SQSS3Outputter(Outputter[Union[str, bytes]]):
    def __init__(
        self,
        bucket_name: str,
        queue_name: str,
        *,
        s3_config: Dict[str, Any] = {},
        sqs_config: Dict[str, Any] = {},
    ) -> None:
        super().__init__()
        s3 = boto3.resource("s3", **s3_config)
        sqs = boto3.resource("sqs", **sqs_config)
        bucket = s3.Bucket(bucket_name)
        queue = sqs.get_queue_by_name(QueueName=queue_name)
        self.bucket = bucket
        self.queue = queue

    def write(
        self,
        value: Union[str, bytes],
        *,
        context: Optional[Context[Union[str, bytes]]] = None,
    ) -> None:
        bucket = self.bucket
        queue = self.queue
        encoding = sys.getdefaultencoding()
        if context is not None:
            metadata = context.metadata
        else:
            metadata = {}
        if isinstance(value, str):
            value = value.encode(encoding)

        name = hashlib.sha256(value).hexdigest()
        obj = bucket.Object(name)
        obj.put(
            Body=value,
            ContentEncoding=encoding,
            ContentType="text/plain",
        )
        j = json.dumps({"s3_body": obj.key, "metadata": metadata})
        queue.send_message(MessageBody=j)
