import datetime
import logging
import time

import dateutil.parser

from ..circuit_serialization import encode_circuit
from ..exceptions import DeqartBaseException

logger = logging.getLogger("deqart-python-sdk")

_SINGLE_REQUEST_LIMIT = 100


def search_jobs(_connection, run_status=None, created_later_than=None):
    if created_later_than is None:
        parsed_created_later_than = None
    elif isinstance(created_later_than, str):

        parsed_created_later_than = dateutil.parser.parse(created_later_than)
        if parsed_created_later_than.tzinfo is None:
            logger.warning(
                "created_later_than is a str object without timezone info, assuming UTC timezone"
            )
            parsed_created_later_than = parsed_created_later_than.replace(
                tzinfo=datetime.timezone.utc
            )
        parsed_created_later_than = parsed_created_later_than.isoformat()
    elif isinstance(created_later_than, datetime.datetime):
        if created_later_than.tzinfo is None:
            raise DeqartBaseException(
                0, "created_later_than is a datetime object without timezone info"
            )
        parsed_created_later_than = created_later_than.isoformat()
    else:
        raise DeqartBaseException(
            0, "created_later_than should be None, str, or datetime.datetime object"
        )

    params = {
        "limit": _SINGLE_REQUEST_LIMIT,
        "run_status": run_status,
        "created_later_than": parsed_created_later_than,
    }
    result_dict = {"data": []}
    while True:
        response = _connection.send_request(req_type="GET", path="/jobs", params=params)
        if not response.ok:
            raise DeqartBaseException(
                response.status_code, "Couldn't search jobs " + response.text
            )
        response = response.json()

        results = response["data"]
        result_dict["data"] += results
        result_dict["total_count"] = response["total_count"]

        if len(results) < _SINGLE_REQUEST_LIMIT:
            break

        params["offset"] = len(result_dict["data"])
    return result_dict


def estimate_job_runtime(_connection, circuit):
    encoded_circuit = encode_circuit(circuit)
    params = {"estimate_only": True, "circuit": encoded_circuit}
    response = _connection.send_request(req_type="POST", path="/jobs", json_req=params)
    if not response.ok:
        raise DeqartBaseException(
            response.status_code,
            "Couldn't estimate job. " + response.json()["error_message"],
        )
    return response.json()["data"]


def submit_job(_connection, circuit, job_name=None):
    encoded_circuit = encode_circuit(circuit)
    params = {"circuit": encoded_circuit, "job_name": job_name}
    response = _connection.send_request(req_type="POST", path="/jobs", json_req=params)
    if not response.ok:
        raise DeqartBaseException(
            response.status_code, "Couldn't submit job " + response.text
        )
    return response.json()["data"]


def cancel_job(_connection, job_id):
    response = _connection.send_request(
        req_type="PATCH", path=f"/jobs/{job_id}", json_req={"cancel": True}
    )
    if not response.ok:
        raise DeqartBaseException(
            response.status_code, "Couldn't cancel job " + response.text
        )
    return response.json()["data"]


def get(_connection, job_id):
    response = _connection.send_request(req_type="GET", path=f"/jobs/{job_id}")
    if not response.ok:
        raise DeqartBaseException(
            response.status_code, "Couldn't get job " + response.text
        )
    return response.json()["data"]


def wait_for_job(_connection, job_id):
    i = 1
    while True:
        response = _connection.send_request(req_type="GET", path=f"/jobs/{job_id}")
        if not response.ok:
            raise DeqartBaseException(
                response.status_code, "Couldn't wait for job " + response.text
            )
        response = response.json()["data"]
        if response["run_status"] not in [
            "FAILED_VALIDATION",
            "COMPLETED",
            "CANCELED",
            "TERMINATED",
            "NOT_ENOUGH_FUNDS",
        ]:
            if i == 1:
                time.sleep(2.0)
            elif i == 2:
                time.sleep(5.0)
            else:
                time.sleep(10.0)
        else:
            return response
        i += 1
