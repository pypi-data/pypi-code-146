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

"""gRPC action scripts."""
from __future__ import annotations

from modalic.api.common.proto.mosaic_pb2 import Parameters, ProcessMeta
from modalic.utils import shared


def parameters_to_proto(parameters: shared.Parameters) -> Parameters:
    r"""."""
    return Parameters(
        tensor=parameters.tensor,
        data_type=parameters.data_type,
        model_version=parameters.model_version,
    )


def parameters_from_proto(msg: Parameters) -> shared.Parameters:
    r"""."""
    tensor: list[bytes] = list(msg.parameters.tensor)
    return shared.Parameters(
        tensor=tensor,
        data_type=msg.parameters.data_type,
        model_version=msg.parameters.model_version,
    )


def process_meta_to_proto(meta: shared.ProcessMeta) -> ProcessMeta:
    r"""."""
    return ProcessMeta(round_id=meta.round_id, loss=meta.loss)


def to_meta(round_id: int, loss: float) -> shared.ProcessMeta:
    r"""."""
    return shared.ProcessMeta(round_id=round_id, loss=loss)
