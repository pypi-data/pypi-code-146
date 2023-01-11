"""Functionality to fetch/modify info in glue database"""
from typing import List, Dict

import boto3
import awswrangler as wr
import loguru

from dai_python_commons.dai_error import DaiGlueError


class GlueUtils:  # pylint: disable=too-few-public-methods
    """Used to fetch/modify info in glue database

    FUNCTIONS
        get_columns_info :func:`~dai_python_commons.GlueUtils.get_columns_info`
        get_partitions :func:`~dai_python_commons.GlueUtils.get_partitions`
        add_partitions :func:`~dai_python_commons.GlueUtils.add_partitions`
    """

    @staticmethod
    def get_columns_info(
        boto3_client, database_name: str, table_name: str
    ) -> List[dict]:
        """
        Gets a list with column information. Each element of the list is a dict including the Name, Type, Comment and
        Parameters
        :param boto3_client: Glue boto3 client
        :param database_name: Name of the database
        :param table_name: Name of the table
        :return: A list of dictionaries including column information. Example:
        [{"Name": "messageid", "Type": "string", "Comment": "The Message id", "Parameters": {}}]
        """
        table_info = boto3_client.get_table(DatabaseName=database_name, Name=table_name)
        columns_info = table_info["Table"]["StorageDescriptor"]["Columns"]

        return columns_info

    @staticmethod
    def get_partitions(
        glue_client,
        database_name: str,
        table_name: str,
        logger: loguru.logger,
        max_results=100,
    ) -> list:
        """
        Get information about all the partitions of the given table
        :param glue_client: Glue boto3 client with the region set
        :param database_name: Name of the database
        :param table_name: Name of the table
        :param logger: Logger object
        :param max_results: Maximum number of partitions to get when calling the Glue API
        :return: A list of structures including information about the partitions of database_name.table_name. For the
        the exact format see boto3 documentation for glue_client.get_partitions
        """
        logger.info(f"Getting partition information for {database_name}.{table_name}")

        def verify_response(resp):
            if resp["ResponseMetadata"]["HTTPStatusCode"] != 200:
                logger.error(
                    f"Error at getting partitions for {database_name}.{table_name}, response = {resp}"
                )
                raise DaiGlueError("GlueError!")

        response = glue_client.get_partitions(
            DatabaseName=database_name, TableName=table_name, MaxResults=max_results
        )
        verify_response(response)

        all_partitions = response["Partitions"]
        while "NextToken" in response and response["NextToken"]:
            response = glue_client.get_partitions(
                DatabaseName=database_name,
                TableName=table_name,
                MaxResults=max_results,
                NextToken=response["NextToken"],
            )
            verify_response(response)
            all_partitions += response["Partitions"]

        logger.info(f"Found {len(all_partitions)} partitions")

        return all_partitions

    @staticmethod
    def add_partitions(
        session,
        database_name: str,
        table_name: str,
        logger: loguru.logger,
        partitions2add: List[Dict[str, str]],
    ) -> None:
        """
        Add new partitions to a glue table
        :param session: Boto3 session
        :param database_name: Name of the database
        :param table_name: Name of the table
        :param logger: Logger object
        :param partitions2add: List of partitions to add in the format
        [{
        'Value': ['2022-10-16'],
        'Location': 's3://se-sl-tf-dai-dev-data-refined/tr/ib/0005/assignment/v1/data/atdatetime_dt=2022-10-16'
        }]
        :return: Nothing
        """
        logger.info(
            f"Adding {len(partitions2add)} partitions to {database_name}.{table_name}: {partitions2add}"
        )

        # make sure we have / at the end of the s3 path
        formatted = {}
        for partition in partitions2add:
            loc = (
                partition["Location"]
                if partition["Location"].endswith("/")
                else f"{partition['Location']}/"
            )
            formatted[loc] = partition["Value"]

        wr.catalog.add_parquet_partitions(
            database=database_name,
            table=table_name,
            partitions_values=formatted,
            boto3_session=session,
        )
        logger.info("Partitions added.")

    @staticmethod
    def get_table_location(session: boto3.session.Session, database_name: str, table_name: str) -> str:
        """
        Returns the s3 location of a Glue table. Note that it does not include the partitions paths. Example
        of answer: s3://se-sl-tf-dai-prod-data-refined/tr/ib/0005/apc/v1/data
        :param session: Boto3 session
        :param database_name: Name of the database
        :param table_name: Name of the table
        :return:
        """
        return wr.catalog.get_table_location(
            database=database_name, table=table_name, boto3_session=session
        )
