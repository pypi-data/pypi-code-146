#
# Copyright 2022 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.

from typing import Any, Dict, List, NoReturn

import trafaret as t

from datarobot._compat import String
from datarobot.enums import CV_METHOD, DEFAULT_MAX_WAIT
from datarobot.errors import InvalidUsageError
from datarobot.helpers.partitioning_methods import (
    DatetimePartitioning as datarobot_datetime_partitioning,
)
from datarobot.helpers.partitioning_methods import (
    DatetimePartitioningSpecification,
    PartitioningMethod,
)


class DatetimePartitioning(
    datarobot_datetime_partitioning
):  # pylint: disable=missing-class-docstring
    @classmethod
    def datetime_partitioning_log_retrieve(
        cls, project_id: str, datetime_partitioning_id: str
    ) -> Any:
        """Retrieve the datetime partitioning log content for an optimized datetime partitioning.

        The Datetime Partitioning Log provides details about the partitioning process for an OTV
        or Time Series project.

        Parameters
        ----------
        project_id : str
            project id of the project associated with the datetime partitioning.
        datetime_partitioning_id : str
            id of the optimized datetime partitioning
        """
        url = (
            f"projects/{project_id}/optimizedDatetimePartitionings/{datetime_partitioning_id}/"
            "datetimePartitioningLog/file/"
        )
        response = cls._client.get(url)
        return response.text

    @classmethod
    def get_input_data(
        cls, project_id: str, datetime_partitioning_id: str
    ) -> DatetimePartitioningSpecification:
        """Retrieve the input used to create an Optimized DatetimePartitioning from a project for
        the specified datetime_partitioning_id. A datetime_partitioning_id is created by using the
        :meth:`generate_optimized<datarobot.DatetimePartitioning.generate_optimized>` function.

        Parameters
        ----------
        project_id : str
            the id of the project to retrieve partitioning for
        datetime_partitioning_id : ObjectId
            the ObjectId associated with the project to retrieve from mongo

        Returns
        -------
        DatetimePartitioningInput : the input to optimized datetime partitioning
        """
        url = "projects/{}/optimizedDatetimePartitionings/{}/datetimePartitioningInput/".format(
            project_id, datetime_partitioning_id
        )
        response = cls._client.get(url)
        return DatetimePartitioningSpecification.from_server_data(  # type: ignore[no-untyped-call, no-any-return]
            response.json()
        )


class DatetimePartitioningId(PartitioningMethod):
    """Defines a DatetimePartitioningId used for datetime partitioning.

    This class only includes the datetime_partitioning_id that identifies a previously
    optimized datetime partitioning and the project_id for the associated project.

    This is the specification that should be passed to :meth:`Project.analyze_and_model
    <datarobot.models.Project.analyze_and_model>` via the ``partitioning_method`` parameter. To see
    the full partitioning use :meth:`DatetimePartitioning.get_optimized
    <datarobot.DatetimePartitioning.get_optimized>`.

    Attributes
    ----------
    datetime_partitioning_id : str
        the id of the datetime partitioning to use
    project_id : str
        the id of the project the datetime partitioning is associated with
    """

    _converter = t.Dict(
        {
            t.Key("datetime_partitioning_id"): String(),
            t.Key("project_id"): String(),
        }
    ).ignore_extra("*")

    def __init__(self, datetime_partitioning_id: str, project_id: str):
        self.datetime_partitioning_id = datetime_partitioning_id
        self.project_id = project_id

    def _keys_with_defaults(self) -> List[str]:
        """These keys have default values in the API so they will always be present when starting
        a project. Make sure we these values are set if they are present in the datetime
        partitioning input."""
        return [
            "unsupervised_mode",
            "treat_as_exponential",
            "autopilot_data_selection_method",
            "use_supervised_feature_reduction",
            "use_time_series",
            "disable_holdout",
            "model_splits",
        ]

    def collect_payload(self) -> Dict[str, Any]:
        payload = {
            "datetime_partitioning_id": self.datetime_partitioning_id,
            "cv_method": CV_METHOD.DATETIME,
        }
        datetime_partitioning_input = DatetimePartitioning.get_input_data(
            self.project_id, self.datetime_partitioning_id
        )
        input_payload = datetime_partitioning_input.collect_payload()
        for key in self._keys_with_defaults():
            if key in input_payload and input_payload[key] is not None:
                payload[key] = input_payload[key]

        return payload

    def prep_payload(self, project_id: str, max_wait: int = DEFAULT_MAX_WAIT) -> None:
        pass

    def update(self, **kwargs: Any) -> NoReturn:
        raise InvalidUsageError
