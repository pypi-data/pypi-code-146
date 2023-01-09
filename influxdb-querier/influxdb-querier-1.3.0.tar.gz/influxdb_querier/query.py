from typing import Union, Tuple, Iterable, AnyStr

import influxdb.resultset
import influxdb_datalogger

from .tag import Tag
from .clauses import Select, Where, From, Limit, Group
from .client import InfluxClient
from .functions import QueryFunction


class Query(str):
    """
    Class that represents a query for InfluxDB. Combined from different clauses.

    Also contains some inner classes to help construct a query.
    """
    def __new__(cls, select_clause, from_clause, where_clause=None, group_clause=None, limit_clause=None):
        clauses = [select_clause, from_clause, where_clause, group_clause, limit_clause]
        query = " ".join([clause for clause in clauses if clause])
        obj = super().__new__(cls, query)
        obj.select_clause = select_clause
        obj.from_clause = from_clause
        obj.where_clause = where_clause
        obj.group_clause = group_clause
        obj.limit_clause = limit_clause
        return obj.strip()


def query_influx(influx_client: InfluxClient,
                 *measurements: Union[influxdb_datalogger.Measurement, str],
                 fields: Union[tuple, str] = None,
                 tags: Union[set, list, tuple] = None,
                 groups: Union[str, tuple] = None,
                 limit: int = None,
                 query_function: QueryFunction = None,
                 query: Union[Query, str] = None,
                 select_clause: str = None,
                 from_clause: str = None,
                 where_clause: str = None,
                 group_clause: str = None,
                 limit_clause: str = None) -> influxdb.resultset.ResultSet:
    f"""
    Parses data from InfluxDB based on input passed to the function.

    Args:
        influx_client: An InfluxClient object that is built using IP, port, and database name for the influxdb instance.
        *measurements: Some measurements as {influxdb_datalogger.Measurement} or str to select data from.
        fields: A tuple of fields, or a single field as a string to select data for.
        tags: A set of tag-keys with tag-values to filter data for.
        groups: An optional argument for tags to group the result by. Set `groups="*"` to get all groups.
        limit: An optional argument to limit the amount of results from the database.
        query_function: An optional argument to define a function to use in the select clause. This function wraps a given field.
        query: An optional query that has been pre-defined already. Can be either a string or a Query-object.
        select_clause: An optional argument for defining a SELECT-clause that has been hard coded.
        from_clause: An optional argument for defining a FROM-clause that has been hard coded.
        where_clause: An optional argument for defining a WHERE-clause that has been hard coded.
        group_clause: An optional argument for defining a GROUP-clause that has been hard coded.
        limit_clause: An optional argument for defining a LIMIT-clause that has been hard coded.

    Returns:
        A ResultSet object containing the result from the query to InfluxDB.
    """
    if not query:
        query = build_query(*measurements, fields=fields, tags=tags, groups=groups, limit=limit, query_function=query_function,
                            select_clause=select_clause, from_clause=from_clause, where_clause=where_clause, group_clause=group_clause, limit_clause=limit_clause)

    http_request = f"{influx_client.protocol}://{influx_client.ip}:{influx_client.port}/query?q={query}&db={influx_client.database}"

    influx_client.log(f"{'=' * len(str(http_request))}")
    influx_client.log(f"{http_request}")

    result = influx_client.client.query(query)
    assert isinstance(result, influxdb.resultset.ResultSet)

    return result


def build_query(*measurements: Union[influxdb_datalogger.Measurement, AnyStr],
                fields: Union[Iterable[Union[influxdb_datalogger.Field, AnyStr]], influxdb_datalogger.Field, AnyStr] = None,
                tags: Union[Iterable[Tag], Tag] = None,
                groups: Union[Tuple[AnyStr, ...], AnyStr] = None,
                limit: int = None,
                query_function: QueryFunction = None,
                select_clause: AnyStr = None,
                from_clause: AnyStr = None,
                where_clause: AnyStr = None,
                group_clause: AnyStr = None,
                limit_clause: AnyStr = None) -> AnyStr:
    """
    Builds a query for InfluxDB based on some input.

    Args:
        *measurements: Some measurements to select data from. Added to the ``FROM`` clause.
        fields: A tuple of fields, or a single field as a string to select data for. Added to the ``SELECT`` clause.
        tags: A dictionary of tag-keys with tag-values to filter data for. Added to the ``WHERE`` clause.
        limit: An optional argument to limit the amount of results from the database. Added to the ``LIMIT`` clause.
        groups: An optional argument for tags to group the result by. Set groups="*" to get all groups. Added to the ``GROUP`` clause.
        query_function: An optional argument to define a function to use in the select clause. This function wraps a given field.
        select_clause: An optional argument for defining a SELECT-clause that has been hard coded.
        from_clause: An optional argument for defining a FROM-clause that has been hard coded.
        where_clause: An optional argument for defining a WHERE-clause that has been hard coded.
        group_clause: An optional argument for defining a GROUP-clause that has been hard coded.
        limit_clause: An optional argument for defining a LIMIT-clause that has been hard coded.

    Returns:
        A query as a string for InfluxDB based on the input to the function.
    """

    if not select_clause:
        if isinstance(fields, str):
            select_clause = Select.build(fields, query_function=query_function)
        else:
            select_clause = Select.build(*fields, query_function=query_function)

    if not from_clause:
        from_clause = From.build(*measurements)

    if not where_clause:
        if tags is None:
            pass
        elif isinstance(tags, Tag):
            where_clause = Where.build(tags)
        else:
            where_clause = Where.build(*tags)

    if not group_clause:
        if groups is None:
            pass
        elif isinstance(groups, str):
            group_clause = Group.build(groups)
        else:
            group_clause = Group.build(*groups)

    if not limit_clause:
        limit_clause = Limit.build(limit)

    query = Query(select_clause=select_clause,
                  from_clause=from_clause,
                  where_clause=where_clause,
                  group_clause=group_clause,
                  limit_clause=limit_clause)

    return query
