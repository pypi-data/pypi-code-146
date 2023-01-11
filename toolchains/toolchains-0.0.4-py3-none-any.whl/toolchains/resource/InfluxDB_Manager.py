#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import inspect
import socket
from urllib.parse import urlparse
from datetime import datetime
import influxdb_client
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
# from influxdb_client.client.write_api import ASYNCHRONOUS
# from pprint import pprint
# from influxdb_client import AuthorizationsApi
# from influxdb_client import client

# toolchain 넣을때 남기고
from pawnlib.config.globalconfig import pawnlib_config as pawn
from pawnlib.resource import net
from pawnlib.typing import date_utils
from pawnlib.output import *
from pawnlib.output.color_print import PrintRichTable


def ifdb_time_date():
    return '%s' % datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


def p_log(text, level='info', is_view=False, logging=True):
    cf = inspect.currentframe()
    line_number = cf.f_back.f_lineno
    func_name = cf.f_back.f_code.co_name

    print_color = {
        "info": "green",
        "error": "red",
        "warning": "magenta",
        "debug": "yellow",
    }

    log_text = f'{func_name}.{line_number} | {text}'
    if is_view:
        cprint(log_text, color=print_color[level.lower()])

    if logging:
        if level.lower() == 'info' and pawn.app_logger:
            pawn.app_logger.info(log_text)

        if level.lower() == 'debug' and pawn.app_logger:
            pawn.app_logger.debug(log_text)

        if level.lower() == 'error' and pawn.error_logger:
            pawn.error_logger.error(log_text)


class InfluxDbManager:
    def __init__(self, db_url='http://localhost', db_port='8086', token=None, org_id=None, org=None,
                 bucket_name=None, is_debug=False):

        """
        This Class influxDB handler Manager
        DB Insert data, create DB, Delete DB, Delete table, Delete data

        :param db_url : Database connection url (required) /  (ex) http://localhost
        :param db_port : Database connection port (default : 8086)
        :param token : Database User API Token (required)
        :param org_id : Database User Organization ID
        :param org : Database User Organization name
        :param bucket_name: InfluxDB Bucket(DB) name

        Example:
            .. code-block:: python

                import InfluxDbManager

                # Unknown org or org_id...
                idm = InfluxDbManager(db_url={db_url}, db_port={db_port}, token={token}, bucket_name={bucket_name})

                # known org or org_id...
                idm = InfluxDbManager(
                                      db_url={db_url}, db_port={db_port},
                                      token={token}, bucket_name={bucket_name},
                                      org='test_bucket', [org_id='f9b1daf51df75272']
                                     )

                # insert data
                idm.insert_data(
                                bucket_name={bucket_name}, table_name={table_name},
                                field_name={field_name}, field_value={value},
                                tags_values=dict( key: value ),
                                db_create_if_missing=[True|False]
                                )

        """
        self.db_url = db_url
        self.db_port = db_port
        self.token = token
        self.org_id = org_id
        self.org = org
        self.bucket_name = bucket_name

        # self.db_client = None
        # self.db_bucket_api = None
        # self.db_delete_api = None
        # self.db_authorizations_api = None

        self.db_user_authorizations = None
        self.db_user = None
        self.db_user_id = None

        self.pub_ip_addr = net.get_public_ip()
        self.exists_bucket = False

        # user token check
        if not self.token:
            e_msg = f'Not found influx DB User Authentication Token'
            p_log(e_msg, level='error')
            raise OSError(e_msg)
        self.db_url_check()
        self.db_init()
        p_log(f'influx DB Connection URL : {self.db_url},', level='info')

    def db_url_check(self,):
        url_match = "(http|https)\\:\\/\\/([a-z]|[0-9]).*"
        if not re.match(url_match, self.db_url):
            self.db_url = f'http://{self.db_url}'

        # port in URL Check
        url_port_match = f"{url_match}:([0-9]){1,5}"
        if not re.match(url_port_match, self.db_url):
            self.db_url = f'{self.db_url}:{self.db_port}'
        p_log(f'DB URL : {self.db_url}', level='debug')
        self.health_check(check_type='port')

    def _connect(self):
        # self.db_client = InfluxDBClient(url=self.db_url, token=self.token, org_id=self.org_id, org=self.org)
        # return self.db_client
        return InfluxDBClient(url=self.db_url, token=self.token, org_id=self.org_id, org=self.org)

    def _bucket_api(self):
        return self._connect().buckets_api()

    def _delete_api(self):
        return self._connect().delete_api()

    def _auth_api(self):
        return self._connect().authorizations_api()

    def _write_api(self):
        return self._connect().write_api(write_options=SYNCHRONOUS)

    def _query_api(self):
        return self._connect().query_api()

    def _close(self):
        self._connect().close()

    def db_init(self):
        init_reload = False

        if self.health_check(check_type='ping'):
            self.db_user_authorizations = self._auth_api().find_authorizations()

            if not self.org or not self.org_id:
                if not self.org:
                    p_log(f'org is not be found, so a find(or setting) is org', level='debug')
                    self.org = self.db_user_authorizations[0].org
                    init_reload = True
                else:
                    if self.org != self.db_user_authorizations[0].org:
                        p_log(f'org name is different..({self.org} != {self.db_user_authorizations[0].org})',
                              level='error')

                if not self.org_id:
                    p_log(f'org_id is not be found, so a find(or setting) is org_id', level='debug')
                    self.org_id = self.db_user_authorizations[0].org_id
                    p_log(f'org_id : {self.org_id} ', level='debug')
                    init_reload = True
                else:
                    if self.org_id != self.db_user_authorizations[0].org_id:
                        p_log(f'org_id is different..({self.org_id} != {self.db_user_authorizations[0].org_id})',
                              level='error')

                if init_reload:
                    p_log(f'reload function \"db_init\"', level='debug')
                    self.db_init()

            if not init_reload:
                self.db_user = self.db_user_authorizations[0].user
                self.db_user_id = self.db_user_authorizations[0].user_id
                p_log(f'DB user organization info '
                      f'\n - org : {self.org}'
                      f'\n - org_id : {self.org_id}'
                      f'\n - user : {self.db_user}'
                      f'\n - user_id: {self.db_user_id}', level='info')

    def health_check(self, check_type="ping", udp=False):
        result = None
        if check_type.lower() == "ping":
            # if self.db_client.ping():
            if self._connect().ping():
                p_log(f'Connected InfluxDB instance : Success', level='info')
                return True
            else:
                p_log(f'Connected InfluxDB instance : Fail', level='error')
                raise ConnectionRefusedError(f'Connection Refused => {self.db_url}')

        if check_type.lower() == "port":
            # udp = socket.SOCK_DGRAM , tcp = socket.SOCK_STREAM
            socket_type = socket.SOCK_DGRAM if udp else socket.SOCK_STREAM
            timeout_seconds = 1
            sock = socket.socket(socket.AF_INET, socket_type)
            sock.settimeout(timeout_seconds)

            try:
                result = sock.connect_ex((urlparse(self.db_url).hostname, int(self.db_port)))
            except OSError as e:
                err_msg = f'Port check Fail - {urlparse(self.db_url).hostname} , {int(self.db_port)}'
                raise OSError(f'{e}\n - {err_msg}')
            finally:
                if result == 0:
                    p_log(f"Port ({self.db_port}) received successfully", level='info')
                    sock.shutdown(socket.SHUT_RDWR)
                    sock.close()
                    return True
                else:
                    p_log(f"Port({self.db_port}) received failed", level='error')
                    err_msg = f'[Errno {result}] Connection refused ' \
                              f'- {urlparse(self.db_url).hostname}, {int(self.db_port)}'
                    raise ConnectionRefusedError(err_msg)

    def check_db(self, bucket_name=None):
        p_log(f'check influxDB bucket find : {bucket_name}', level='debug')
        # return self.db_bucket_api.find_bucket_by_name(bucket_name)
        return self._bucket_api().find_bucket_by_name(bucket_name)

    # Todo
    # get bucket list  - finished
    def get_list(self, bucket_list=False, measurement_list=False):
        return_value = None
        if bucket_list:
            buckets_list = []
            # results = self.db_bucket_api.find_buckets().buckets
            results = self._bucket_api().find_buckets().buckets
            for bucket_item in results:
                r_dict = {
                    "bucket_name": bucket_item.name,
                    "ibucket_id": bucket_item.id,
                    "org_id": bucket_item.org_id,
                    "type": bucket_item.type,
                    "desc": bucket_item.description
                }
                buckets_list.append(r_dict)

            PrintRichTable(title="Bucket Lists", data=buckets_list)
            return_value = buckets_list

        if measurement_list:
            table_list = []
            table_list_query = f"""
                import \"influxdata/influxdb/schema\"
                schema.measurements(bucket: \"{self.bucket_name}\")
            """
            # tables = self.db_client.query_api().query(org=self.org, query=table_list_query)
            tables = self._query_api().query(org=self.org, query=table_list_query)
            for table in tables:
                for row in table:
                    r_dict = {"measurements": row.values['_value']}
                    table_list.append(r_dict)

            PrintRichTable(title="measurementsTable", data=table_list)
            return_value = table_list

        self._close()
        return return_value

    # create bucket
    def create_db(self, bucket_name=None):
        """
        It creates a bucket(database).

        :param bucket_name: The name of the bucket to create
        :return: The return value is a dict with the following keys
        """
        bucket_name = bucket_name if bucket_name else self.bucket_name

        if not bucket_name:
            err_msg = f'Not setting for bucket_name'
            p_log(f'{err_msg}', level='error')
            raise ValueError(err_msg)

        if self.check_db(bucket_name):
            rst = f'Already create is Bucket(DB) : {bucket_name}'
            p_log(f'{rst}', level='debug')
        else:
            p_log(f'Create InfluxDB Bucket(DB) : {bucket_name}', level='debug')
            rst = self._bucket_api().create_bucket(bucket_name=bucket_name, org=self.org, )

        self.exists_bucket = True
        self._close()

        return rst

    # delete bucket
    def delete_db(self, bucket_name=None):
        """
        Delete the bucket(DB).

        :param bucket_name: The name of the bucket to be deleted
        :return: The return value is a list of objects.
        """
        if bucket_name:
            find_rst = self.check_db(bucket_name)
            if find_rst:
                p_log(f'Delete Bucket(DB) : {bucket_name}', level='info')
                p_log(f'{find_rst}', level='debug')
                # self.db_bucket_api.delete_bucket(find_rst.id)
                self._bucket_api().delete_bucket(find_rst.id)

                if self.exists_bucket:
                    p_log(f'self.exists_bucket value change {self.exists_bucket} => \"False\"',
                          level='info', logging=False)
                    self.exists_bucket = False
                return True
            else:
                p_log(f'Not Delete Bucket(Is Not found bucket) : {bucket_name}', level='warning')
                return False
        else:
            p_log(f'Not Delete Bucket(Is Null bucket Name)', level='warning')
            return False

    # delete measurement(table) or data
    def delete_data(self, bucket_name=None, table_name=None, start_time=None, end_time=None, predicates=None, org=None):
        """
        Delete {table(_measurement)} or {matching tag name and values} from a bucket

        :param bucket_name: Delete criteria Bucket name (DB name)
        :param table_name: Delete criteria Measurement(table) name,
                           None or Null is All _measurement(table)
        :param predicates: Delete data value (ex tag_name=\"tag_value\")
        :param start_time: Delete Criteria Start Time
        :param end_time: Delete Criteria End Time
        :param org: organization name

        Delete predicates rule:
            Delete predicates do not support regular expressions.
            Delete predicates do not support the OR logical operator.
            Delete predicates only support equality (=), not inequality (!=).
            Delete predicates can use any column or tag except _time , _field, or _value.

        Example:
            .. code-block:: python
        """

        bucket_name = bucket_name if bucket_name else self.bucket_name
        org = org if org else self.org

        delete_table_name = f'_measurement=\"{table_name}\"' if table_name else ''
        delete_predicates = predicates if predicates else ''

        if predicates:
            if delete_table_name:
                delete_table_name += ' AND'

            if "_measurement" in delete_predicates:
                p_log(f'delete_table_name value Null change....{delete_table_name} -> Null', level='debug')
                delete_table_name = ''

        delete_value = f'{delete_table_name} {delete_predicates}'

        if bucket_name and table_name:
            delete_start_time = start_time if start_time else "1970-01-01T00:00:00Z"

            if end_time:
                reg_text = '20([0-9]){2}-([01])([0-9])-([0-3])([0-9])T([0-2])([0-9]):([0-2])([0-9]):([0-2])([0-9])Z'
                if re.match(reg_text, end_time):
                    delete_stop_time = end_time
                else:
                    err_msg = f'No format  end time -> ex) {ifdb_time_date()}'
                    p_log(err_msg, level='debug')
                    raise ValueError(err_msg)
            else:
                delete_stop_time = f'{ifdb_time_date()}'

            p_log(f'delete a measurement(table) from a bucket(db) | bucket={bucket_name}, measurement={table_name}, '
                  f'delete_start_time={delete_start_time}, delete_end_time={delete_stop_time}, '
                  f'predicates={delete_value}',
                  level='info')

            try:
                self._delete_api().delete(delete_start_time, delete_stop_time, delete_value, bucket_name, org)
            except influxdb_client.rest.ApiException as e:
                p_log(f'{e}', level='debug')
            finally:
                self._close()
        else:
            p_log(f'Bucket or measurement(table) name is Null', level="info", logging=False)

    def insert_data(self, bucket_name=None, table_name=None,
                    field_name=None, field_value=None,
                    tags_values=None, db_create_if_missing=True):
        """
        It inserts data into the database.

        :param bucket_name: The name of the bucket to be created
        :param table_name: The name of the table to insert data into
        :param field_name: The name of the field to be inserted
        :param field_value: The value of the field to be inserted
        :param tags_values: This is a dictionary that contains the tags you want to use
        :param db_create_if_missing: If the database does not exist, create it, defaults to True (optional)
        :return: The return value is a list of dictionaries. Each dictionary represents a row in the query result.
        """

        bucket_name = bucket_name if bucket_name else self.bucket_name

        p_log(f'self.exists_bucket is {self.exists_bucket}', level='debug')
        if not self.exists_bucket:
            if not self.check_db(bucket_name=bucket_name):
                if db_create_if_missing:
                    p_log(f'Create Bucket(DB) : {bucket_name}')
                    self.create_db(bucket_name=bucket_name)
                    self.exists_bucket = True
                else:
                    p_log(f'db_create_if_missing value is {db_create_if_missing}', level='error')
            else:
                self.exists_bucket = True

        if not table_name:
            p_log(f'default measurement(table_name) is {date_utils.todaydate()}', level='info')
            table_name = f"{date_utils.todaydate()}"

        if not tags_values:
            tags_values = {
                "hostname": f'{net.get_hostname()}',
                "ip_address": f'{self.pub_ip_addr}',
                # "date": f'{date_utils.todaydate(date_type="ms")}'
            }

        if field_name and field_value:
            write_rst = None
            # write_api = self._connect().write_api(write_options=SYNCHRONOUS)
            record = [
                {
                    "measurement": table_name,
                    "tags": tags_values,
                    "fields": {
                        field_name: field_value
                        # Todo  여러개가 들어 갈수 있도록
                        # https://github.com/influxdata/influxdb-client-python#writes
                    }
                }
            ]

            p_log(record, level='debug')

            try:
                # write_rst = self.write_api.write(bucket=bucket_name, record=record, org=self.org)
                write_rst = self._write_api().write(bucket=bucket_name, record=record, org=self.org)
            except Exception as e:
                p_log(f'Exception Error : {e}', level='error')
            finally:
                self._close()
                if not write_rst:
                    p_log(f'Write Success - {write_rst}', level='info')
                    return True
                else:
                    p_log(f'Write Error - {write_rst}', level='error')
                    return False
        else:
            p_log(f'field_name({field_name}) OR field_value({field_value}) is None!!', level='info')

    def query_data(self,
                   bucket_name=None, table_name=None, start_time="-10m", stop_time='now()',
                   filter_column: list['str'] = None, return_type='list', query=None):
        """
        > This function queries data from a table in a bucket

        :param bucket_name: The name of the bucket you want to query
        :param table_name: The name of the table you want to query
        :param start_time: The time to start the query.  This can be a relative time (e.g. "-10m" for 10 minutes ago)
                           or an absolute time (e.g. "2020-01-01T00:00:00Z").
                           The default is 10 minutes ago, defaults to -10m (optional)
        :param stop_time: The time to stop the query.  This can be a relative time (e.g. "-1m" for 1 minutes ago)
                          or an absolute time (e.g. "2020-01-01T00:00:00Z").
                          The default is now time, defaults to now() (optional)
        :param filter_column: The value of the influxDB columns filter.  The default is ["_field", "_value"]
                              And, If the value is only "all", all columns are output.
        :param return_type: The type of the return is list or json type. The default is "list"
        :param query: The query to run

        Example:

            .. code-block:: python

            # only _measurement all data query , return type list and Not filter column
            influx_query = f'from(bucket:"{bucket_name}")' \
                           f'|> range(start: -6h)'

            query_result = idm.query_data(table_name='test_table', query=influx_query,
                                          filter_column='all', return_type='list')

            # only _measurement all data query , return type json \
            # and Default filter column ('_measurement', '_field', '_value')
            query_result = idm.query_data(table_name='test_table', query=influx_query, return_type='json')

            # null is Query, All bucket data query
            influx_query = None

            # All bucket data query (default Query start time = -10m)
            query_result = idm.query_data(filter_column=['all'], return_type='list')

            # All bucket data query (Qeury start time = -6h) and return type to json
            query_result = idm.query_data(query=influx_query, filter_column='all',
                                          start_time='-6h', return_type='json')

        """

        results = None
        # query_api = self.db_client.query_api()
        bucket_name = bucket_name if bucket_name else self.bucket_name
        table_query = f' |> filter(fn:(r) => r._measurement == \"{table_name}\")' if table_name else ''

        if not query:
            query = f'from(bucket:"{bucket_name}") ' \
                    f'|> range(start: {start_time}, stop: {stop_time})' \
                    f'{table_query}'
        else:
            query = query

        p_log(f'{query}', level='debug')
        # cprint(f'{query}', color='red')
        result = self._query_api().query(org=self.org, query=query)

        if isinstance(filter_column, str) and filter_column.lower() == 'all':
            p_log(f'filter_column type is {type(filter_column)}'
                  f'change  type str to list', level='info')
            filter_column = [filter_column]

        if not filter_column:
            filter_column = ['_measurement', '_field', '_value']

        p_log(f'column type is {type(filter_column)}', level='debug')
        p_log(filter_column, level='debug')

        if filter_column[0] == 'all':
            # cprint('column is all .......', color='magenta')
            if return_type.lower() == 'list':
                results = result.to_values(columns=None)
            elif return_type.lower() == 'json':
                results = result.to_json()
        else:
            # cprint('column is Not all .......', color='magenta')
            if return_type.lower() == 'list':
                results = result.to_values(columns=filter_column)
            elif return_type.lower() == 'json':
                results = result.to_json(columns=filter_column)

        del query
        return results


def test_run():
    import time
    from pawnlib.builder import generator
    # token = 'S3TSolQ0qyATlErhDU-OUqpNecmZCBI3hIuM36uiWCXgjqqhGxCJQXgi3lg6DXzBqxG4i_px-7EWbXkKwgRhDg=='
    # db_address = 'http://20.20.6.5'
    # db_port = '8086'

    def print_banner(**kwargs):
        banner = generator.generate_banner(
            app_name=kwargs.get('app_name'),
            description=kwargs.get('description'),
            version=kwargs.get('version'),
            author=kwargs.get('author'),
            font=kwargs.get('font') if kwargs.get('font') else 'big',
            return_type=kwargs.get('return_type') if kwargs.get('return_type') else 'string'
        )
        print(banner)

    print_banner(app_name="InfluxDB\nTEST", description="Influxdb Testing..")

    token = 'my-super-secret-auth-token'
    db_address = 'http://20.20.6.96'
    db_port = '80'
    bucket_name = 'my-bucket'
    idm = InfluxDbManager(token=token, bucket_name=bucket_name, db_url=db_address,
                          db_port=db_port, org='my-org', )

    idm.get_list(bucket_list=True)
    for i in range(1, 10):
        p_log(f'[test]db write: field_name=test{i}, field_value=[{i}] test{date_utils.todaydate(date_type="ms")}',
              level='warning')
        idm.insert_data(table_name='test_table',
                        field_name=f'test{i}',
                        field_value=f'[{i}] test{date_utils.todaydate(date_type="ms")}',
                        db_create_if_missing=True)
        idm.insert_data(table_name='test_table1',
                        field_name=f'test{i}',
                        field_value=f'[{i}] test{date_utils.todaydate(date_type="ms")}',
                        db_create_if_missing=True)
        idm.insert_data(table_name='test_table2',
                        field_name=f'test{i}',
                        field_value=f'[{i}] test{date_utils.todaydate(date_type="ms")}',
                        db_create_if_missing=True)
        idm.insert_data(table_name='test_table',
                        field_name=f'1{i}',
                        field_value=f'1{i}',
                        db_create_if_missing=True)
    idm.insert_data(table_name='test_table',
                    field_name=int(11),
                    field_value=int(11),
                    db_create_if_missing=True)

    p_log(f'[test]db query', level='info')
    query = f'from(bucket:"{bucket_name}")' \
            f'|> range(start: -6h)'

    aa = idm.query_data(table_name='test_table', query=query)
    print(f'[test]query 1 - {type(aa)} \n {aa}')
    print("<" * 100, "\n", "+" * 100)

    aa = idm.query_data()
    print(f'[test]query 2 - {type(aa)} \n {aa}')
    # pprint(aa, indent=4)
    print("\n\n", "+#" * 100)

    # aa = idm.query_data(table_name='test_table', query=query, filter_column='all', return_type='list')
    aa = idm.query_data(table_name='test_table', query=query, return_type='json')
    print(f'[test]query 3 - {type(aa)} \n {aa}')
    print("\n", "+" * 100, "\n", "-" * 100)

    # aa = idm.query_data(filter_column='all', return_type='list')
    aa = idm.query_data(return_type='json', query=None, filter_column='all', start_time='-6h')
    print(f'[test]query 4 - {type(aa)} \n {aa}')
    idm.get_list(measurement_list=True)

    cprint(f'[test]db create', color='magenta')
    idm.create_db(bucket_name="test_db")
    time.sleep(10)
    idm.get_list(bucket_list=True)

    cprint(f'[test]db delete', color='magenta')
    idm.delete_db(bucket_name='test_db')
    idm.get_list(bucket_list=True)

    cprint(f'[test]measurement delete(table delete)', color='magenta')
    idm.delete_data(table_name='test_table')
    idm.get_list(measurement_list=True)
    #
    idm._close()


if __name__ == '__main__':
    LOG_DIR = f"{file.get_real_path(__file__)}/logs"
    APP_NAME = 'InfluxDB_Manager'
    STDOUT = True

    pawn.set(
        PAWN_LOGGER=dict(
            # log_level='DEBUG',
            log_path=LOG_DIR,
            stdout=STDOUT,
            use_hook_exception=False,
        ),
        app_name=APP_NAME,
        version="0.0.1",
        app_data={}
    )

    test_run()
