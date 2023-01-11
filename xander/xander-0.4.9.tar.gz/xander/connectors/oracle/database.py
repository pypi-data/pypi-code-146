import logging

import cx_Oracle
import cx_Oracle as oracle
import numpy as np
import pandas
from dateutil.parser import parse
from dotenv import load_dotenv

# Load environment variables
from pandas._libs.tslibs.np_datetime import OutOfBoundsDatetime
from tqdm import tqdm

load_dotenv()


def is_date(value, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param value: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """

    try:
        # Try to parse the date
        parse(value, fuzzy=fuzzy)
        return True

    except OutOfBoundsDatetime:
        # Return false if the value is not a date
        return True

    except ValueError:
        # Return false if the value is not a date
        return False


def is_string(value):
    """
    Check if the values is a string.

    :param value: obj, value to be validated
    :return: True or False
    """

    return isinstance(value, str)


def is_number(value):
    """
    Check if the value is a number.

    :param value: obj, value to be validated
    :return: True or False
    """

    try:
        # Try to convert the value in a float number
        float(value)
        return True

    except:
        return False


class Oracle:
    """
    Database Oracle class interface.
    It contains all methods to access and query an oracle database.
    """

    def __init__(self, ip_address, port, sid, service_name, username, password, drivers):

        # Init Oracle drivers if needed
        try:
            # Initialize the Oracle Client
            oracle.init_oracle_client(lib_dir=drivers)
        except cx_Oracle.ProgrammingError:
            pass

        # Get the ip address of the database from the environment variables
        self.database_ip_address = ip_address

        # Get the port of the database from the environment variables
        self.database_port = port

        # Get the SID of the database from the environment variables
        self.database_sid = sid

        # Get the Service Name of the database from the environment variables
        self.service_name = service_name

        # Get credentials of the database from the environment variables
        self.database_username = username
        self.database_password = password

        # Init the DNS TNS
        if self.service_name != "":
            self.dns_tns = oracle.makedsn(self.database_ip_address, self.database_port, service_name=self.service_name)
        else:
            self.dns_tns = oracle.makedsn(self.database_ip_address, self.database_port, self.database_sid)

    def get_tables(self):
        """
        Retunr the list of all tables in the database.
        """

        # fixed query to retrieve tables in the database
        query = "SELECT owner, table_name FROM all_tables"

        # Get query result
        res = self.fetch(query=query)

        # Clean the output
        tables = [c[1] for c in res if c[0] == 'CAVI_AT_ENRICHED']

        return tables

    def fetch(self, query):
        """
        Make a query using the parameters passed by the user.

        :param query: query to be executed
        :return: (True, result) if the query is successful otherwise (False, exception)
        """

        try:
            # Connect to the database
            with oracle.connect(self.database_username, self.database_password,
                                self.dns_tns, encoding="UTF-8") as connection:

                # Initialize the connection cursor
                cursor = connection.cursor()

                # Execute the query
                cursor.execute(query)

                # Use the fetchall() to retrieve all results in batch
                rows = cursor.fetchall()

                # Return True since everything is ok, and the result of the query.
                # The result is None if it is a write query
                return rows

        except Exception as e:
            logging.critical(f"[ORACLE] Error -> {e}", exc_info=e)

            # In case of exceptions the flag is set to False
            return None

    def push(self, query):
        """
        Make a query using the parameters passed by the user.

        :param query: query to be executed
        :return: True if the query is successful otherwise False
        """

        # Connect to the database
        with oracle.connect(self.database_username, self.database_password, self.dns_tns,
                            encoding="UTF-8") as connection:
            try:

                # Initialize the connection cursor
                cursor = connection.cursor()

                # Use the cursor to execute the query
                cursor.execute(query)

                # Commit the connection, closing it
                connection.commit()

                # Return True since everything is ok, and the result of the query.
                # The result is None if it is a write query
                return True, None

            except Exception as e:
                logging.critical(f"[ORACLE] Error -> {e}", exc_info=e)

                # Commit the connection, closing it
                connection.commit()

                # In case of exceptions the flag is set to False
                return False, e

    def push_many(self, table, dataset, batch_size=50000):
        """
        Make a batch insert query in the specified database.

        @param table: table name
        @param dataset: dataset to be inserted
        @param batch_size: batch size of the query
        @return: True or False
        """

        datas, data = [], []

        for i, line in tqdm(enumerate(dataset.values), total=len(dataset)):
            v = tuple([v if not (pandas.isna(v) or v is np.nan) else None for v in line])
            data.append(v)

            if i % batch_size == 0:
                datas.append(data)
                data = []

        if data:
            datas.append(data)

        # Connect to the database
        with oracle.connect(self.database_username, self.database_password, self.dns_tns,
                            encoding="UTF-8") as connection:
            try:
                # Initialize the connection cursor
                cursor = connection.cursor()

                # Create the list of columns to be placed in the query string
                columns = str(tuple(dataset.columns)).replace('\'', '').replace('/', '_')

                # Create the list of placeholders to be places in the query string
                placeholder = self.create_placeholders(dataset)

                # Generate the SQL statement
                sql = f"INSERT INTO {table} {columns} VALUES {placeholder}"

                # For each data batch make the write query
                for data in tqdm(datas, total=len(datas)):
                    cursor.executemany(sql, data)

                # Commit the connection, closing it
                connection.commit()

                # Return True since everything is ok, and the result of the query.
                # The result is None if it is a write query
                return True, None

            except Exception as e:
                logging.critical(f"[ORACLE] Error -> {e}", exc_info=e)

                # Commit the connection, closing it
                connection.commit()

                # In case of exceptions the flag is set to False
                return False, e

    @staticmethod
    def create_placeholders(dataset):
        """
        Create the list of placeholders for the batch insert query.

        @param dataset: target dataset
        @return: list of placeholders
        """

        placeholder = []
        for i in range(1, len(dataset.columns) + 1):
            # if 'date' in list(dataset.columns)[i - 1].lower() or 'data' in list(dataset.columns)[i - 1].lower() \
            #         or 'anno' in list(dataset.columns)[i - 1].lower():
            #
            #     placeholder.append(f"TO_DATE(:{i}, 'YYYY-MM-DD HH24:MI:SS')")
            # else:
            placeholder.append(f':{i}')
        placeholder = "(" + ", ".join(placeholder) + ")"

        return placeholder
