import time
import mysql.connector
from mysql.connector import errorcode, pooling
from paketmutfak.utils.functions.general import init_extra_log_params, generate_uid
from paketmutfak.utils.constants.error_codes import MessageCode


class PmMysqlBaseClass:
    _instance = None
    host = None
    port = None
    user = None
    password = None
    database = None
    pool_name = None
    table_name = None
    pm_logger = None
    pool_size = 10

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, host, port, user, password, database, pool_name, pm_logger, pool_size=10):
        if cls._instance is None:
            print('Creating new instance')
            cls._instance = cls.__new__(cls)
            cls.pm_logger = pm_logger

            res = {}
            cls.host = host
            cls.port = port
            cls.user = user
            cls.password = password
            cls.database = database
            cls.pool_name = pool_name
            cls.pool_size = pool_name

            res["host"] = cls.host
            res["port"] = cls.port
            res["user"] = cls.user
            res["password"] = cls.password
            res["database"] = cls.database

            pool = pooling.MySQLConnectionPool(
                pool_name=pool_name,
                pool_size=pool_size,
                pool_reset_session=True,
                **res)
            cls.pool = pool
        return cls._instance

    @staticmethod
    def close(conn, cursor):
        """
        A method used to close connection of mysql.
        :param conn:
        :param cursor:
        :return:
        """
        cursor.close()
        conn.close()

    def _get_connection(self):
        conn = None
        cursor = None
        try:
            conn, cursor = self.get_connection_conn_cursor()

        except mysql.connector.PoolError:
            if conn:
                self.close(conn, cursor)
            return {"log_id": "log_id", "status": "BAD", "status_code": "BAD"}
        except Exception as exp:
            if conn:
                self.close(conn, cursor)
            respond = self.database_error_handling_to_log(error=exp, sql_statement="")
            return respond

    def execute(self, sql, args=None, commit=False, column_names=False):
        """
        Execute db sql, it could be with args and with out args. The usage is
        similar with execute() function in module pymysql.
        :param sql: sql clause
        :param args: args need by sql clause
        :param commit: whether to commit
        :param column_names: is it return column name as output
        :return: if commit, return None, else, return result
        """
        # get connection form connection pool instead of create one.
        conn = None
        cursor = None
        try:
            conn, cursor = self.get_connection_conn_cursor()

            if args:
                cursor.execute(sql, args)
            else:
                cursor.execute(sql)
            if commit is True:
                conn.commit()
                row_count = cursor.rowcount
                self.close(conn, cursor)
                return row_count
            else:
                res = cursor.fetchall()
                if column_names:
                    num_fields = len(cursor.description)
                    field_names = []
                    if num_fields > 0:
                        field_names = [i[0] for i in cursor.description]
                    self.close(conn, cursor)
                    return res, field_names
                else:
                    self.close(conn, cursor)
                    return res
        except mysql.connector.PoolError:
            if conn:
                self.close(conn, cursor)
            return {"log_id": "log_id", "status": "BAD", "status_code": "BAD"}
        except mysql.connector.Error as err:
            if conn:
                self.close(conn, cursor)
            respond = self.database_error_handling_to_log(error=err, sql_statement=sql)
            return respond
        except Exception as exp:
            if conn:
                self.close(conn, cursor)
            respond = self.database_error_handling_to_log(error=exp, sql_statement=sql)
            return respond

    def executemany(self, sql, args, commit=False):
        """
        Execute with many args. Similar with executemany() function in pymysql.
        args should be db sequence.
        :param sql: sql clause
        :param args: args
        :param commit: commit or not.
        :return: if commit, return None, else, return result
        """
        # get connection form connection pool instead of create one.
        conn = None
        cursor = None
        try:
            conn, cursor = self.get_connection_conn_cursor()
            cursor.executemany(sql, args)
            if commit is True:
                conn.commit()
                row_count = cursor.rowcount
                self.close(conn, cursor)
                return row_count
            else:
                res = cursor.fetchall()
                self.close(conn, cursor)
                return res
        except mysql.connector.PoolError as poolErr:
            if conn:
                self.close(conn, cursor)
            log_id = generate_uid()
            self.pm_logger.error(msg=f"get_connection error: {poolErr}",
                                 extra=init_extra_log_params(log_id=log_id,
                                                             table_name="",
                                                             db_name=self.database))
            return {"log_id": log_id, "status": "BAD", "status_code": "BAD"}
        except mysql.connector.Error as err:
            if conn:
                self.close(conn, cursor)
            respond = self.database_error_handling_to_log(error=err, sql_statement=sql)
            return respond
        except Exception as exp:
            if conn:
                self.close(conn, cursor)
            respond = self.database_error_handling_to_log(error=exp, sql_statement=sql)
            return respond

    def get_connection_conn_cursor(self, timeout=10, retry_period=0.1):
        try:
            conn, cursor = self._get_connection_conn_cursor_helper()

            if timeout < retry_period:
                return {"message_code": "Timeout must be greater than retry period"}, 400

            max_retry_count = int(timeout / retry_period)
            attempt_count = 0
            while cursor is None and attempt_count < max_retry_count:
                conn, cursor = self._get_connection_conn_cursor_helper()
                attempt_count += 1
                time.sleep(retry_period)

        except Exception as exp:
            respond = self.database_error_handling_to_log(error=exp, sql_statement="Connection Pool Error")
            return respond, None
        else:
            return conn, cursor

    def _get_connection_conn_cursor_helper(self):
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor()
        except mysql.connector.Error as err:
            respond = self.database_error_handling_to_log(error=err, sql_statement="Connection Pool Error")
            return respond, None
        except Exception as exp:
            respond = self.database_error_handling_to_log(error=exp, sql_statement="Connection Pool Error")
            return respond, None
        else:
            return conn, cursor

    def executemany_without_commit(self, conn, cursor, sql, args):
        try:
            cursor.executemany(sql, args)
            row_count = cursor.rowcount
        except mysql.connector.PoolError as poolErr:
            if conn:
                self.close(conn, cursor)
            log_id = generate_uid()
            self.pm_logger.error(msg=f"get_connection error: {poolErr}",
                                 extra=init_extra_log_params(log_id=log_id,
                                                             table_name="",
                                                             db_name=self.database))
            return {"log_id": log_id, "status": "BAD", "status_code": "BAD"}
        except mysql.connector.Error as err:
            if conn:
                self.close(conn, cursor)
            respond = self.database_error_handling_to_log(error=err, sql_statement=sql)
            return respond
        except Exception as exp:
            if conn:
                self.close(conn, cursor)
            respond = self.database_error_handling_to_log(error=exp, sql_statement=sql)
            return respond
        else:
            return row_count

    def execute_without_commit(self, conn, cursor, sql, args=None):
        try:
            if args:
                cursor.execute(sql, args)
            else:
                cursor.execute(sql)

            row_count = cursor.rowcount
        except mysql.connector.PoolError as poolErr:
            if conn:
                self.close(conn, cursor)
            log_id = generate_uid()
            self.pm_logger.error(msg=f"get_connection error: {poolErr}",
                                 extra=init_extra_log_params(log_id=log_id,
                                                             table_name="",
                                                             db_name=self.database))
            return {"log_id": log_id, "status": "BAD", "status_code": "BAD"}
        except mysql.connector.Error as err:
            if conn:
                self.close(conn, cursor)
            respond = self.database_error_handling_to_log(error=err, sql_statement=sql)
            return respond
        except Exception as exp:
            if conn:
                self.close(conn, cursor)
            respond = self.database_error_handling_to_log(error=exp, sql_statement=sql)
            return respond
        else:
            return row_count

    def commit_without_execute(self, conn, cursor):
        try:
            conn.commit()
            if conn:
                self.close(conn, cursor)

            row_count = cursor.rowcount
        except mysql.connector.PoolError as poolErr:
            if conn:
                self.close(conn, cursor)
            log_id = generate_uid()
            self.pm_logger.error(msg=f"get_connection error: {poolErr}",
                                 extra=init_extra_log_params(log_id=log_id,
                                                             table_name="",
                                                             db_name=self.database))
            return {"log_id": log_id, "status": "BAD", "status_code": "BAD"}
        except mysql.connector.Error as err:
            if conn:
                self.close(conn, cursor)
            respond = self.database_error_handling_to_log(error=err, sql_statement="")
            return respond
        except Exception as exp:
            if conn:
                self.close(conn, cursor)
            respond = self.database_error_handling_to_log(error=exp, sql_statement="")
            return respond
        else:
            return row_count

    def callprocedure(self, proc_name, args_array, commit=True):
        """
        :param commit:
        :param proc_name: procedure name
        :param args_array: args
        :return: if commit, return None, else, return result
        """
        conn = None
        cursor = None
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor()

            cursor.callproc(proc_name, args_array)
            if commit is False:  # TODO: Procedureden veri çekme durumu ile ilgili test yapılmalı
                for result in cursor.stored_results():
                    print("++", result.fetchall())
            elif commit is True:
                for result in cursor.stored_results():  # Hata mesajı
                    return {"status_code": "BAD", "error_message": result.fetchall()[0]}
        except mysql.connector.PoolError as poolErr:
            if conn:
                self.close(conn, cursor)
            log_id = generate_uid()
            self.pm_logger.error(msg=f"get_connection error: {poolErr}",
                                 extra=init_extra_log_params(log_id=log_id,
                                                             table_name="",
                                                             db_name=self.database))
            return {"log_id": log_id, "status": "BAD", "status_code": "BAD"}
        except mysql.connector.Error as err:
            if conn:
                self.close(conn, cursor)
            respond = self.database_error_handling_to_log(error=err, sql_statement=proc_name)
            return respond
        except Exception as exp:
            if conn:
                self.close(conn, cursor)
            respond = self.database_error_handling_to_log(error=exp, sql_statement=proc_name)
            return respond
        else:
            return
        finally:
            if conn.is_connected():
                self.close(conn, cursor)

    def database_error_handling_to_log(self, error, sql_statement):
        pm_db_errno = -1
        if "errno" in error.__dict__:
            pm_db_errno = error.errno
            if error.errno == errorcode.ER_BAD_TABLE_ERROR:
                log_message = {'status': 'BAD',
                               'error_message': f"Error : {error}",
                               'sql_statement': sql_statement}
            elif error.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                log_message = {'status': 'BAD',
                               'error_message': f"Error : {error}",
                               'sql_statement': sql_statement}
            elif error.errno == errorcode.ER_PARSE_ERROR:
                log_message = {'status': 'BAD',
                               'error_message': f"Error : {error}",
                               'sql_statement': sql_statement}
            elif error.errno == errorcode.ER_BAD_FIELD_ERROR:
                log_message = {'status': 'BAD',
                               'error_message': f"Error : {error}",
                               'sql_statement': sql_statement}
            elif error.errno == errorcode.ER_WRONG_FIELD_WITH_GROUP:
                log_message = {'status': 'BAD',
                               'error_message': f"Error : {error}",
                               'sql_statement': sql_statement}
            elif error.errno == errorcode.ER_DUP_FIELDNAME:
                log_message = {'status': 'BAD',
                               'error_message': f"Error : {error}",
                               'sql_statement': sql_statement}
            elif error.errno == errorcode.ER_DUP_KEYNAME:
                log_message = {'status': 'BAD',
                               'error_message': f"Error : {error}",
                               'sql_statement': sql_statement}
            elif error.errno == errorcode.ER_NO_SUCH_TABLE:
                log_message = {'status': 'BAD',
                               'error_message': f"Error : {error}",
                               'sql_statement': sql_statement}
            else:
                log_message = {'status': 'BAD',
                               'error_message': f"Error : {error}",
                               'sql_statement': sql_statement,
                               'errno': error.errno}
        else:
            log_message = {'status': 'BAD', 'error_message': f"Something went wrong on : "}

        log_id = generate_uid()
        self.pm_logger.error(msg=log_message.get("error_message"),
                             extra=init_extra_log_params(log_id=log_id,
                                                         table_name="",
                                                         sql_statement=sql_statement,
                                                         db_name=self.database,
                                                         sql_error_code=pm_db_errno,
                                                         error_code=MessageCode.UNEXPECTED_ERROR_ON_SERVICE_MESSAGE))

        return {"log_id": log_id,
                "status_code": "BAD",
                "sql_error_code": pm_db_errno,
                "error_message": log_message.get("error_message")}
