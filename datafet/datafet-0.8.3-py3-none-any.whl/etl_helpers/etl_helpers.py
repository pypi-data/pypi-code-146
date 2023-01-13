#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import gzip
import sys
import time
import uuid
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple

import pytz
from dateutil.relativedelta import relativedelta
from jinja2 import Template
from mypy_boto3_athena.client import AthenaClient
from mypy_boto3_s3.service_resource import Bucket, ObjectSummary, S3ServiceResource


def chunks(lst: List, n: int) -> List[List]:
    return [lst[i : i + n] for i in range(0, len(lst), n)]


def get_args(argv: List) -> Dict:
    return {pair[0]: pair[1] for pair in list(chunks(argv[1:], 2)) if len(pair) == 2}


def get_arg_or_def(args: Dict, arg_name: str, def_val: str) -> str:
    arg: Optional[str] = args.get(arg_name)
    if arg:
        return arg
    else:
        return def_val


def now() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # return datetime.now(ZoneInfo("Europe/Berlin")).strftime('%Y-%m-%d %H:%M:%S') 3.9


def utc_now() -> str:
    return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def get_min_max(dt: datetime.datetime) -> Tuple[datetime.datetime, datetime.datetime]:
    """
    Returns the first and the last moment of a day in UTC.

    Parameters:
        n (int): how many days back (1 = yesterday, 2 = the day before yesterday, etc.)

    Returns:
        datetime

    """
    timezone = pytz.timezone("UTC")
    min, max = (
        datetime.datetime.combine(dt, datetime.time.min),
        datetime.datetime.combine(dt, datetime.time.max),
    )
    return (timezone.localize(min), timezone.localize(max))


def set_boto_session(
    logger: Callable[[str], Tuple[int, str]],
    is_cloud: bool = True,
    profile_name: str = "default",
    region_name: str = "eu-west-1",
):
    if not is_cloud:
        import boto3

        logger(
            "Using local aws credential file with profile: {} in region {}".format(
                profile_name, region_name
            )
        )
        boto3.setup_default_session(profile_name=profile_name, region_name=region_name)
        logger("Sys path: {}".format(sys.path))
    else:
        sys.path.insert(0, "/glue/lib/installation")
        keys = [k for k in sys.modules.keys() if "boto" in k]
        for k in keys:
            if "boto" in k:
                del sys.modules[k]
        import boto3

        boto3.setup_default_session(region_name="eu-central-1")
        logger("Sys path: {}".format(sys.path))


def create_query_exectution_with_athena(
    logger: Callable[[str], Tuple[int, str]],
    athena_client: AthenaClient,
    query: str,
    catalog: str,
    database: str,
    workgroup: str,
):
    try:
        client_request_token = str(uuid.uuid4())
        query_execution = athena_client.start_query_execution(
            QueryString=query,
            ClientRequestToken=client_request_token,
            QueryExecutionContext={"Database": database, "Catalog": catalog},
            WorkGroup=workgroup,
        )
        return (True, query_execution)
    except Exception as e:
        logger(str(e))
        return (False, None)


LOOP_COUNTER_TO_SLOW_DOWN = 3
SHORT_SLEEP = 5
LONG_SLEEP = 16


def wait_for_query_results(
    logger: Callable[[str], Tuple[int, str]],
    athena_ui_base_url: str,
    athena_client: AthenaClient,
    query_execution: Dict,
):
    """
    This function waits for a Athena query execution to finish (succeed or fail)

    Parameters:
      logger (function): A function that has a string parameter, the content to be logged
      athena_ui_base_url (str): The base URL for the Athena UI
      athena_client  (AthenaClient): client that will be used to get the execution info
      query_execution: (Dict) The query execution that was previously created and should be monitored.

    Returns:
        Returns (True, query results) | (False, None) | (False, query execution failure)
    """
    try:
        query_execution_id = query_execution["QueryExecutionId"]
        query_execution_updated = athena_client.get_query_execution(
            QueryExecutionId=query_execution_id
        )

        loop_counter = 0
        while query_execution_updated["QueryExecution"]["Status"]["State"] in [
            "QUEUED",
            "RUNNING",
        ]:
            query_execution_updated = athena_client.get_query_execution(
                QueryExecutionId=query_execution_id
            )
            logger("Query: {} is still being executed".format(query_execution_id))
            if loop_counter > LOOP_COUNTER_TO_SLOW_DOWN:
                time.sleep(LONG_SLEEP)
            else:
                time.sleep(SHORT_SLEEP)
            loop_counter = 1

        if query_execution_updated["QueryExecution"]["Status"]["State"] == "FAILED":
            logger(
                "Query execution has failed for query execution id: {}".format(
                    query_execution_id
                )
            )
            logger("{}/{}".format(athena_ui_base_url, query_execution_id))
            return (False, query_execution_updated)
        else:
            query_results = athena_client.get_query_results(
                QueryExecutionId=query_execution_id
            )
            return (True, query_results)
    except Exception as e:
        logger(str(e))
        return (False, None)


# TODO: replace with log level based approach

# def debug_generator(is_debug: bool, fn: str, e: Any) -> Any:
#     if is_debug:
#         print("fn: {} element: {}".format(fn, e))
#     return e


# def debug_generator_bytes(is_debug: bool, fn: str, e: bytes) -> bytes:
#     if is_debug:
#         print("fn: {} bytes length: {}".format(fn, len(e)))
#     return e


# def debug_generator_list(is_debug: bool, fn: str, e: List) -> List:
#     if is_debug:
#         print("fn: {} list length: {}".format(fn, len(e)))
#     return e


def get_previous_day(n: int) -> datetime.datetime:
    """
    Returns the previous UTC day where n determines how many days ago

    Parameters:
        n (int): how many days back (1 = yesterday, 2 = the day before yesterday, etc.)

    Returns:
        datetime

    """
    return datetime.datetime.utcnow().replace(tzinfo=pytz.utc) + relativedelta(days=-n)


def get_first_and_last_moment_of_a_day(
    dt: datetime.datetime,
) -> Tuple[datetime.datetime, datetime.datetime]:
    """
    Returns the first and the last moment of a day in UTC.

    Parameters:

    Returns:


    """
    timezone = pytz.timezone("UTC")
    min, max = (
        datetime.datetime.combine(dt, datetime.time.min),
        datetime.datetime.combine(dt, datetime.time.max),
    )
    return (timezone.localize(min), timezone.localize(max))


def get_all_objects_generator(
    bucket: Bucket, logs_prefix: str
) -> Generator[ObjectSummary, None, None]:
    """
    Creates a generator that returns S3 objects

    Parameters:
        bucket (Bucket): the s3 bucket where the files are located
        logs_prefix (str): the prefix where the logs are

    Returns:
        Generator[ObjectSummary, None, None]

    """
    return (o for o in bucket.objects.filter(Prefix=logs_prefix))


def is_object_created_at(
    s3_object: ObjectSummary, day_min_max: Tuple[datetime.datetime, datetime.datetime]
) -> bool:
    """
    Returns true if the objects creation date is within a day boundary (both check is inclusive) otherwise returns false

    Parameters:
        s3_object (ObjectSummary): a S3 object
        day_min_max (Tuple[datetime, datetime]): first and last moment of a day

    Returns:
        bool

    """
    # YAPF breaks down if inlining all of these
    last_modified = s3_object.last_modified
    day_min, day_max = day_min_max[0], day_min_max[1]
    return last_modified >= day_min and last_modified <= day_max


def get_filtered_objects_generator(
    objects_generator: Generator[ObjectSummary, None, None],
    day_min_max: Tuple[datetime.datetime, datetime.datetime],
) -> Generator:
    """
    Returns a Generator that contains the elements that are matching the day boundaries specified by day_min_max

    Parameters:
        objects_generator (Generator[ObjectSummary, None, None]): Generator containing ObjectSummaries
        day_min_max (Tuple[datetime, datetime]): a tuple that contains the first and the last moment of a day

    Returns:
       Generator[ObjectSummary, None, None])

    """
    return (o for o in objects_generator if is_object_created_at(o, day_min_max))


def get_downloaded_unzipped_content_generator(
    s3_objects_generator: Generator[ObjectSummary, None, None]
) -> Generator[bytes, None, None]:
    """
    Returns a Generator that contains the unzipped log lines, represented as bytes of a s3_object (a gzipped log file)

    Parameters:
        objects_generator (Generator[ObjectSummary, None, None]): Generator containing ObjectSummaries


    Returns:
       Generator[bytes, None, None])

    """
    return (
        gzip.decompress(s3_object.get()["Body"].read())
        for s3_object in s3_objects_generator
    )


def get_split_lines_generator(
    file_content_generator: Generator[bytes, None, None]
) -> Generator[List[str], None, None]:
    """
    Returns a Generator that contains all the lines (List[str]) except the first two (headers) of a log file

    Parameters:
        file_content_generator (Generator[bytes, None, None]): Generator containing file contents


    Returns:
       Generator[List[str], None, None])

    """
    return (
        one_file.decode("utf-8").split("\n")[2:] for one_file in file_content_generator
    )


def get_split_fields_generator(
    split_lines_generator: Generator[List[str], None, None]
) -> Generator[List[str], None, None]:
    """
    Returns a Generator

    Parameters:
        file_content_generator (Generator[bytes, None, None]): Generator containing file contents


    Returns:
       Generator[List, None, None])

    """
    for lines in split_lines_generator:
        for line in lines:
            if line:
                yield line.split("\t")


def get_all_objects_with_predicate_generator(
    bucket: Bucket, prefix: str, predicate_fn: Callable[[ObjectSummary], bool]
):
    """
    Creates a generator that returns S3 objects and a predicate value as a tuple.

    Parameters:
        bucket (Bucket): the s3 bucket where the files are located
        logs_prefix (str): the prefix where the logs are
        predicate_fn: (Callable[[ObjectSummary], bool]): a function that gets an objectsummary and returns a bool based on its (the objectsummary) properties

    Returns:
        Generator[(ObjectSummary, bool), None, None]

    """
    return ((o, predicate_fn(o)) for o in bucket.objects.filter(Prefix=prefix))
