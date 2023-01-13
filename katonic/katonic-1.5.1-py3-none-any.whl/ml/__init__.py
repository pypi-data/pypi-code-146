#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
import base64
import os


def __decode_py(message):
    base64_bytes = message.encode("ascii")
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode("ascii")


# set environment variable
os.environ["MLFLOW_S3_ENDPOINT_URL"] = __decode_py(
    "aHR0cDovL21pbmlvLXNlcnZlci5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsOjkwMDAv"
)

os.environ["AWS_ACCESS_KEY_ID"] = __decode_py("bWxmbG93X2tleQ==")

os.environ["AWS_SECRET_ACCESS_KEY"] = __decode_py("WWFoZGVlVGhhaXJhaEg3ZQ==")

os.environ["MLFLOW_BASE_URL"] = __decode_py(
    "aHR0cDovL21sZmxvdy1zZXJ2aWNlLm1sZmxvdy5zdmMuY2x1c3Rlci5sb2NhbDo1MDAw"
)
