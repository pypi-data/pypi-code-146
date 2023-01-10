from looqbox.global_calling import GlobalCalling
from looqbox.objects.visual.looq_table import ObjTable
from looqbox.database.objects.sql_thread_manager import SqlThreadManager
from looqbox.database.objects.connection_jdbc import JDBCConnection
from looqbox.database.objects.connection_big_query import BigQueryConnection
from looqbox.database.objects.connection_mongo import MongoConnection
from looqbox.database.objects.connection_base import BaseConnection
from looqbox.database.database_exceptions import ConnectionTypeNotFound
from multipledispatch import dispatch
import json
import os


__all__ = ["sql_in", "connect", "sql_execute", "sql_between", "sql_close", "sql_execute_parallel",
           "add_to_parallel_batch"]

query_parallel_batch = list()

@dispatch(str)
def connect(connection_name: str, parameter_as_json=False, use_all_jars=True) -> BaseConnection:
    """
    Execute a connection in a database.

    :param connection_name: String with the database name
    :param parameter_as_json: Set if the parameters will be in JSON format or not
    :param use_all_jars: If set as True, the connection will import all available jars, allowing connection with
                         different database within the same JVM.
                         If this flag is set as False only the connection required jar will be loaded, thus the
                         connection is going to become prone to error, in case another database technology
                         (e.g. another driver, use another version for the same driver) is used, the Looqbox Kernel
                         will crash due the lack of the correct jar(s) file(s).
                         Therefore, setting use_all_jars as False is recommended for tests purpose or for an advanced
                         user.
    :return: A Connection object
    """

    connection = _connection_factory(connection_name, parameter_as_json, use_all_jars)
    connection.connect()
    return connection


@dispatch(list)
def connect(connection_name: list, parameter_as_json=False, use_all_jars=True) -> list[BaseConnection]:
    """
    Execute a connection in a database.

    :param connection_name: List of database names
    :param parameter_as_json: Set if the parameters will be in JSON format or not
    :param use_all_jars: If set as True, the connection will import all available jars, allowing connection with
                         different database within the same JVM.
                         If this flag is set as False only the connection required jar will be loaded, thus the
                         connection is going to become prone to error, in case another database technology
                         (e.g. another driver, use another version for the same driver) is used, the Looqbox Kernel
                         will crash due the lack of the correct jar(s) file(s).
                         Therefore, setting use_all_jars as False is recommended for tests purpose or for an advanced
                         user.
    :return: A Connection object
    """
    #TODO marcar como deprecated
    connections = []
    for connection in connection_name:
        current_connection = _connection_factory(connection, parameter_as_json, use_all_jars)
        current_connection.connect()
        connections.append(current_connection)
    return connections


@dispatch(BaseConnection)
def connect(connection_name: BaseConnection) -> BaseConnection:
    """
    Returned the connection that are already created.
    :param connection_name: ObjectConnection
    """
    return connection_name


def _get_connection_type(connection, parameter_as_json):
    """
        Get credentials for a list of connections.
        :param connection: String or list of database names
        :param parameter_as_json: Set if the parameters will be in JSON format or not
        :return: A Connection object
    """
    connection_credential = _get_connection_file()

    try:
        if not parameter_as_json:
            connection_credential = GlobalCalling.looq.connection_config[connection]
        else:
            connection_credential = connection_credential[connection]
    except:
        raise Exception(
            "Connection " + connection + " not found in the file " + GlobalCalling.looq.connection_file)
    return connection_credential.get("type", "").lower()


def _get_connection_file() -> dict:
    try:
        if isinstance(GlobalCalling.looq.connection_config, dict):
            file_connections = GlobalCalling.looq.connection_config
        else:
            file_connections = open(GlobalCalling.looq.connection_config)
            file_connections = json.load(file_connections)
    except FileNotFoundError:
        raise Exception("File connections.json not found")
    return file_connections


def _connection_factory(connection_name: str, parameter_as_json: bool, use_all_jars: bool) -> BaseConnection:

    connection_type = _get_connection_type(connection_name, parameter_as_json=parameter_as_json)

    connections_factory = {
        "jdbc": JDBCConnection,
        "mongo_db": MongoConnection,
        "big_query": BigQueryConnection
    }

    if connection_type in connections_factory.keys():
        return connections_factory[connection_type](connection_name,
                                                    parameter_as_json=parameter_as_json,
                                                    use_all_jars=use_all_jars)
    else:
        raise ConnectionTypeNotFound("\nConnection type is not supported")


def sql_execute(connection: str | BaseConnection, query, replace_parameters=None, close_connection=True,
                show_query=False, null_as=None, add_quotes=False, cache_time=None):
    """
    Function to execute a query inside the connection informed. The result of the query will be
    transformed into a ObjTable to be used inside the response.


    :param connection: Connection name or object
    :param query: sql script to query result set (in Big Query or JDBC database), for a Mongo use, the query parameter
    must be defined as followed:
    query = {"collection": "example",
             "query": {"store":10},
             "fields": {"_id": 0, "name": 1, "sales": 1}
            }
    :param replace_parameters: List of parameters to be used in the query. These parameters will replace the numbers
    wit h `` in the query.
        Example:
            replace_parameters = [par1, par2, par3, par4]
            query = "select * from bd where par1=`1` and par2=`2` and par3=`3` and par4=`4`

            In this case the values of `1`, `2`, `3`, `4` will be replaced by par1, par2, par3, par4 respectively (using
            the order of the list in replace_parameters).

    :param close_connection: Define if automatically closes the connection
    :param show_query: Print the query in the console
    :param null_as: Default value to fill null values in the result set
    :param add_quotes: Involves replaced parameters with quotes
    Example:
        replace_parameters = [par1]
            query = "select * from db where par1=`1`"
        For add_quotes = True
            query = "select * from db where par1='par1'"
        For add_quotes = False
            query = "select * from db where par1=par1"
    :param cache_time: Time to leave of cache file in seconds, one might set up to 300 seconds
    :return: A Looqbox ObjTable with the data retrieved from the query
    """

    query = _sql_replace_parameters(query, replace_parameters, add_quotes)

    print_query(query, show_query)

    query_dataframe = ObjTable(null_as=null_as)

    connection = connect(connection)

    connection.set_query_script(query)

    connection.execute(cache_time)

    query_dataframe.data = connection.retrieved_data

    query_dataframe = _count_rows_and_columns(query_dataframe)

    if close_connection:
        connection.close_connection()

    return query_dataframe


def _count_rows_and_columns(query_dataframe):
    query_dataframe.rows = query_dataframe.data.shape[0]
    query_dataframe.cols = query_dataframe.data.shape[1]
    return query_dataframe


def print_query(query, show_query):
    test_mode = GlobalCalling.looq.test_mode

    if show_query and test_mode:
        print(query)


def _sql_replace_parameters(query, replace_parameters, replace_with_quotes=False):
    """
    This function get the query and replace all the values between backticks to the values in the replace_parameters
    list, the values are substituted using the order in replace parameters, for example, the `1` in the query will be
    substituted by the value replace_parameters[0] and so goes on.
    Example:
        query = "select * from database where x = `1` and z = `3` and y = `2`"
        replace_parameters = [30, 50, 60}

        returns = "select * from database where x = 30 and z = 60 and y = 50"

    :param query: Query to be changed
    :param replace_parameters: List that contains the values to substitute
    :param replace_with_quotes=False: Involves replaced parameters with quotes
    :return: Query with the values changed
    """

    if replace_parameters is None:
        return query

    separator = '"' if replace_with_quotes else ""

    for replace in range(len(replace_parameters)):
        query = query.replace('`' + str((replace + 1)) + '`', separator + str(replace_parameters[replace]) + separator)
    return query


def sql_in(query=None, values_list=None):
    """
    Transform the list in values_list to be used inside an IN statement of the SQL.
    Example:
        values_list = [1,2,3,4,5]
        query = 'select * from database where' + sql_in(" col in", values_list)

        "select * from database where col in (1, 2, 3, 4, 5)"


    :param query: Query header with the first part of the query
    :param values_list: list to be transformed as an IN format
    :return: query concatenated with values_list as an IN format
    """
    if values_list is None:
        return ""

    if not isinstance(values_list, list):
        values_list = [values_list]
    elif len(values_list) == 0:
        return ""

    separated_list = str(values_list).replace('[', '(').replace(']', ')')

    if query is None:
        return separated_list
    else:
        return query + " " + separated_list


def sql_between(query=None, values_list=None):
    """
    Transform the list in values_list to be used as a between statement of the SQL.
    Example:
        values_list = ['2018-01-01', '2018-02-02']
        query = 'select * from database where sql_between(' date', date_int)'

        "select * from database where date between '2018-01-01' and '2018-02-02')"


    :param query: Query header with the first part of the query
    :param values_list: list to be used in a between statement
    :return: query concatenated with values_list as a between statement
    """
    if values_list is None:
        return ""

    if len(values_list) != 2:
        raise Exception("To use sql_between values_list must be of two positions")

    if not isinstance(values_list, list):
        values_list = [values_list]

    if isinstance(values_list[0], int) or isinstance(values_list[1], int):
        between_query = query + " between " + str(values_list[0]) + " and " + str(values_list[1])
    else:
        between_query = query + " between '" + values_list[0] + "' and '" + values_list[1] + "'"

    return between_query


def sql_close(connection: BaseConnection) -> None:
    """
    Function to call a close_connection method, this method was kept for
    retro compatibility matters.
    """
    connection.close_connection()


def add_to_parallel_batch(connection: str | BaseConnection, query, replace_parameters=None, close_connection=True,
                          show_query=False, null_as=None, add_quotes=False, cache_time=None) -> None:
    """

    Function used to create the query parallel request used in `sql_execute_parallel`. This function should be called
    just like a sql_execute, using the same parameters.

    :param connection: Connection name or object
    :param query: sql script to query result set (in Big Query or JDBC database), for a Mongo use, the query parameter
    must be defined as followed:
    query = {"collection": "example",
             "query": {"store":10},
             "fields": {"_id": 0, "name": 1, "sales": 1}
            }
    :param replace_parameters: List of parameters to be used in the query. These parameters will replace the numbers
    wit h `` in the query.
        Example:
            replace_parameters = [par1, par2, par3, par4]
            query = "select * from bd where par1=`1` and par2=`2` and par3=`3` and par4=`4`

            In this case the values of `1`, `2`, `3`, `4` will be replaced by par1, par2, par3, par4 respectively (using
            the order of the list in replace_parameters).

    :param close_connection: Define if automatically closes the connection
    :param show_query: Print the query in the console
    :param null_as: Default value to fill null values in the result set
    :param add_quotes: Involves replaced parameters with quotes
    Example:
        replace_parameters = [par1]
            query = "select * from db where par1=`1`"
        For add_quotes = True
            query = "select * from db where par1='par1'"
        For add_quotes = False
            query = "select * from db where par1=par1"
    :param cache_time: Time to leave of cache file in seconds, one might set up to 300 seconds

    """
    #TODO convert list to dict and impklment UID
    #TODO implment map method
    current_query = {
        "connection": connection,
        "query": query,
        "replace_parameters": replace_parameters,
        "close_connection": close_connection,
        "show_query": show_query,
        "null_as": null_as,
        "add_quotes": add_quotes,
        "cache_time": cache_time
    }

    query_parallel_batch.append(current_query)


def sql_execute_parallel(sql_list=None, number_of_threads=None):
    """
    Function parallelize several queries executions. The queries results will be
    transformed into a list of ObjTable to be used inside the response.
    :param sql_list: List contain the queries that will be parallelized. The members of the
    list must contain the following keys:
     - connection: Connection alias or connection object;
     - query: Desired query to be performed (same structure used in sql_execute).
       And optionally may contain:
     - replace_parameters: List of parameters to be used in the query. These parameters will replace the numbers
       with `` in the query;
     - add_quotes: Involves replaced parameters with quotes;
     - show_query: Print the resulting query that will be executed.
    :param number_of_threads: Number of threads that going to be used.
    Example:
            obj_conn1 = {
                         "connection": "connection1",
                         "query":"Select * from table where NAME in (`1`)",
                         "replace_parameters": ["SOME NAME"],
                         "add_quotes": False,
                         "show_query": True
                        }
            obj_conn2 = {
                        "connection": "connection2",
                        "query":"SELECT * from table2"
                        }
            sql_list = [obj_conn1, obj_conn2]
            result_set = sql_execute_parallel(sql_list, number_of_threads=len(sql_list))
    :return: A list of Looqbox ObjTables with the data retrieved from the queries
    """

    sql_list = _get_sql_list(sql_list)

    number_of_threads = len(sql_list) if number_of_threads is None else number_of_threads
    query_manager = SqlThreadManager()
    batch_results = query_manager.parallel_execute(sql_list, number_of_threads=number_of_threads)
    query_parallel_batch.clear()

    return batch_results


def _get_sql_list(sql_list):
    if sql_list is None:
        return query_parallel_batch
    else:
        return sql_list


def reload_database_connection(conn_file_path=GlobalCalling.looq.connection_file):
    if os.path.isfile(conn_file_path):
        GlobalCalling.looq.connection_config = json.loads(conn_file_path)
    else:
        print("Missing connection file: " + GlobalCalling.looq.connection_file)
        GlobalCalling.looq.connection_config = None
