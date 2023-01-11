from __future__ import annotations

import logging
import string
from typing import List, Mapping, Optional, Sequence, Union

import numpy as np
import pandas as pd

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.bad_data_http_communicator import \
    HttpBadDataCommunicator
from truera.protobuf.dataquality import bad_data_service_pb2 as bd_pb
from truera.protobuf.public.common.data_kind_pb2 import \
    DataKindDescribed  # pylint: disable=no-name-in-module


class BadDataClient():

    def __init__(
        self,
        connection_string: Optional[str] = None,
        auth_details: Optional[AuthDetails] = None,
        logger=None,
        use_http: bool = False,
        *,
        verify_cert: Union[bool, str] = True
    ):
        if (not use_http):
            from truera.client.private.communicator.bad_data_grpc_communicator import \
                GrpcBadDataCommunicator
        self.logger = logger or logging.getLogger(__name__)
        self.auth_details = auth_details
        self.communicator = HttpBadDataCommunicator(
            connection_string, auth_details, logger, verify_cert=verify_cert
        ) if use_http else GrpcBadDataCommunicator(
            connection_string, auth_details, logger
        )

    def get_schema_mismatch_rows(
        self,
        project_id: str,
        data_kind: DataKindDescribed,
        *,
        data_split_id: Optional[str] = None,
        feature_name: Optional[str] = None
    ) -> pd.DataFrame:
        request = bd_pb.GetSchemaMismatchRowsRequest(
            project_id=project_id,
            data_kind=data_kind,
            split_id=data_split_id,
        )

        response = self.communicator.get_schema_mismatch_rows(request)
        return self._create_df_from_schema_mismatch_rows(
            response, feature_name=feature_name
        )

    def _create_df_from_schema_mismatch_rows(
        self,
        schema_mismatch_rows_response: bd_pb.GetSchemaMismatchRowsResponse,
        feature_name: Optional[str] = None
    ) -> pd.DataFrame:

        filtered_rows = []
        if not feature_name:
            filtered_rows = schema_mismatch_rows_response.schema_mismatch_row
        else:
            feature_names = []
            feature_names.extend(schema_mismatch_rows_response.feature_names)
            feature_name_index = feature_names.index(feature_name)

            for row in schema_mismatch_rows_response.schema_mismatch_row:
                if feature_name_index in row.schema_mismatch_feature_index:
                    filtered_rows.append(row)

        df = pd.DataFrame(
            [list(i.row_string) for i in filtered_rows],
            columns=list(schema_mismatch_rows_response.feature_names)
        ).astype("string")
        return df
