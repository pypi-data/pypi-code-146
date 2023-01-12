"""
database connection and data manipulation base classes
======================================================

This module is providing generic base classes and helper methods to implement and integrate
any database driver that is compatible to the :pep:`Python DB API <249>`. The base classes
are providing already all attributes and methods to handle database connections,
data selections and manipulations.

Additionally this package is defining generalized interfaces to switch dynamically
between databases without the need to adapt the code of your application - simply by selecting
another database connector class within your :ref:`configuration files <config-files>`.


basic usage
-----------

The abstract base class :class:`DbBase` allows you to implement a db-specific class with few
lines of code. Simply inherit from :class:`DbBase` and implement a :meth:`~DbBase.connect`
method that is setting the :attr:`~DbBase.conn` instance attribute to a
:pep:`Python DB API <249>` compatible connection object.

For a fictive specific database driver package `SpecificDbDriver` that is providing a `connect`
method, a minimal example would look like::

    from ae.db_core import DbBase
    ...
    class SpecificDb(DbBase):
        def connect(self) -> str:
            self.last_err_msg = ''
            try:
               self.conn = SpecificDbDriver.connect(**self.connect_params())
            except Exception as ex:
                self.last_err_msg = f"SpecificDb-connect() error: {ex} for {self}"
            else:
                self.create_cursor()
           return self.last_err_msg

The helper method :meth:`~DbBase.connect_params` provided by this module is helping you to merge
any specified database system credentials and features into a dict to be passed as connection parameters
to the database-specific connection class/function/factory of the database driver.

Another helper :meth:`~DbBase.create_cursor` provided by :class:`DbBase` can be used in the
:meth:`~DbBase.connect` method to create a Python DB API-compatible cursor object and
assign it to the :attr:`~DbBase.curs` attribute.

In this implementation your class SpecificDb does automatically also inherit useful methods from :class:`DbBase`
to execute :meth:`INSERT <DbBase.insert>`, :meth:`DELETE <DbBase.delete>`,
:meth:`UPDATE <DbBase.update>` and :meth:`UPSERT <DbBase.upsert>` commands,
to run :meth:`SELECT <DbBase.select>` queries and
to call :meth:`stored procedures <DbBase.call_proc>`.

.. hint::
    Examples of an implementation of a specific database class are e.g. the portion packages
    :mod:`ae.db_pg` for Postgres and :mod:`ae.db_ora` for Oracle.


connection parameters
---------------------

:class:`DbBase` supports the following connection parameter keys:

    * **user** : user name or database account name.
    * **password** : user account password.
    * **dbname** : name of the database to connect.
    * **host** : host name or IP address of the database server.
    * **port**: port number of the database server.

Some database drivers are using default values for most of these connection parameters,
if they are not specified. The mandatory connection parameters can differ for different database
drivers. Most of them need at least a user name and password.

.. hint::
    Most database drivers like e.g. `psycopg2 <http://initd.org/psycopg/docs/module.html>`_ or
    `pg8000 <https://kite.com/python/docs/pg8000.connect>`_ for Postgres databases
    are supporting all of these connection parameter keys. For others like e.g.
    `cx_Oracle <https://cx-oracle.readthedocs.io/en/7.2/module.html>`_ which are not supporting
    some of them (like e.g. `host` and `dbname`) you may also need to overwrite the
    :meth:`~DbBase.connect_params` method to convert/adopt unsupported connection parameter keys.

Alternatively you can provide the connection parameters needed by the database driver connector
with a single database url string in the
`SQLAlchemy Database URL format <https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls>`_::

    dialect+driver://user:password@host:port/dbname

So if your connection parameters dict - respective your database system credentials and features -
providing a `url` key then :meth:`~DbBase.connect_params` will parse and split the url into
separate connection parameters.

.. note::
    When you specify a connection parameter as separate key and also within the `url` value
    then the separate key value will have preference. The scheme part (dialect+driver) including
    the following colon character of the URL string are not evaluated and can be omitted.


bind variables format
---------------------

Bind variables in your sql query strings have to be formatted in the
:pep:`named parameter style <249#paramstyle>`. If your database driver is only supporting the
`pyformat` parameter style, then overload the __init__ method and set the :attr:`~DbBase.param_style`
to ``'pyformat'`` and all sql query strings will be automatically converted by :class:`DbBase`
before they get sent to the database::

    class SpecificDb(DbBase):
        def __init__(self, ...)
            super().__init__(...)
            self.param_style = 'pyformat'
        ...

"""
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Dict, List, Optional, Sequence, Tuple
import urllib.parse

from ae.dynamicod import try_eval                               # type: ignore  # for mypy
from ae.lockname import NamedLocks                              # type: ignore  # for mypy
from ae.sys_core import SystemBase, SystemConnectorBase         # type: ignore  # for mypy


__version__ = '0.3.14'


NAMED_BIND_VAR_PREFIX: str = ':'        #: character to mark a bind variable in a sql query
CHK_BIND_VAR_PREFIX: str = 'CV_'
""" bind variable name prefix, to allow for same column/-name a new/separate value in e.g. the SET clause and
an old value in the WHERE clause. Gets added to bind variables in filters/chk_values and extra where clauses. """


def connect_args_from_params(conn_params: Dict[str, Any]) -> Tuple[Dict[str, str], List[str]]:
    """ split dict with database connection parameters into credentials and features.

    :param conn_params:     connection params dict.
    :return:                tuple of credentials dict and features list.
    """
    credentials = {}
    features = []
    for arg_name, arg_val in conn_params.items():
        if isinstance(arg_val, str):
            credentials[arg_name] = arg_val
        elif not isinstance(arg_val, bool):
            features.append(f"{arg_name}={arg_val!r}")
        elif arg_val:
            features.append(arg_name)
    return credentials, features


def _normalize_col_values(col_values: Dict[str, Any]) -> Dict[str, Any]:
    """ convert empty strings into real None values.

    :param col_values:          dict of column values (dict key is the column name).
    :return:                    col_values dict where empty values got replaced with None (also in original dict).
    """
    for key, val in col_values.items():
        if isinstance(val, str) and not val:
            col_values[key] = None
    return col_values


def _prepare_in_clause(sql: str, bind_vars: Optional[Dict[str, Any]] = None,
                       additional_col_values: Optional[Dict[str, Any]] = None) -> Tuple[str, Dict[str, Any]]:
    """ replace list bind variables used in an IN clause with separate bind variables for each list item.

    :param sql:                     query to be executed.
    :param bind_vars:               dict of all available bind variables for the execution.
    :param additional_col_values:   additional bind variables.
    :return:                        tuple of adapted query string and joined bind variables.
    """
    new_bind_vars = deepcopy(additional_col_values or {})
    if bind_vars:
        for key, val in bind_vars.items():
            if isinstance(val, list):  # expand IN clause bind list variable to separate bind variables
                var_list = [key + '_' + str(_) for _ in range(len(val))]
                in_vars = ','.join([NAMED_BIND_VAR_PREFIX + c for c in var_list])
                sql = sql.replace(NAMED_BIND_VAR_PREFIX + key, in_vars)
                for var_val in zip(var_list, val):
                    new_bind_vars[var_val[0]] = var_val[1]
            else:
                new_bind_vars[key] = val
    return sql, new_bind_vars


def _rebind(chk_values: Optional[Dict[str, Any]] = None,
            where_group_order: str = "",
            bind_vars: Optional[Dict[str, Any]] = None,
            extra_bind: Optional[Dict[str, Any]] = None
            ) -> Tuple[Optional[Dict[str, Any]], str, Dict[str, Any]]:
    """ merge where_group_order string with chk_values filter dict and merge/rename bind variables.

    :param chk_values:          dict with column_name: value items, used to filter/restrict the resulting rows.

                                This method compiles this dict into a sql WHERE clause expression. If
                                you also passed additional sql clauses into the
                                :paramref:`~_rebind.where_group_order` then it will be merged with the
                                compiled expression. The names of the sql parameters and related bind variables
                                are build from the column names/keys of this dict, and will be prefixed with
                                :data:`CHK_BIND_VAR_PREFIX`.

                                Passing None or a empty dict to this and to the :paramref:`~_rebind.extra_bind`
                                arguments will disable any filtering. If only this argument is None/empty
                                then the first item of the :paramref:`~_rebind.extra_bind` dict will
                                be used as filter.
    :param where_group_order:   sql part with optional WHERE/GROUP/ORDER clauses (the part after the WHERE),
                                including bind variables in the :ref:`named parameter style <sql-parameter-style>`.
    :param bind_vars:           dict with bind variables (variable name has to be prefixed
                                in :paramref:`~_rebind.where_group_order` with :data:`CHK_BIND_VAR_PREFIX`).
    :param extra_bind:          additional dict with bind variables (variable name has NOT to be prefixed/adapted
                                in :paramref:`~_rebind.where_group_order` argument).
    :return:                    tuple of corrected/rebound values of chk_values, where_group_order and bind_vars.
    """
    rebound_vars: Dict[str, Any] = {}  # use new instance to not change callers bind_vars dict

    if extra_bind is not None:
        rebound_vars.update(extra_bind)
        if not chk_values:
            def_pkey: list = [next(iter(extra_bind.items()))]  # use first dict item as pkey check value
            chk_values = dict(def_pkey)  # mypy+PyCharm: merging this with previous code line shows type error

    if chk_values:
        rebound_vars.update({CHK_BIND_VAR_PREFIX + k: v for k, v in chk_values.items()})
        extra_where = " AND ".join([f"{k} = {NAMED_BIND_VAR_PREFIX}{CHK_BIND_VAR_PREFIX}{k}"
                                    for k in chk_values.keys()])
        if not where_group_order:
            where_group_order = extra_where
        elif where_group_order.upper().startswith(('GROUP BY', 'ORDER BY')):
            where_group_order = f"{extra_where} {where_group_order}"
        else:
            where_group_order = f"({extra_where}) AND {where_group_order}"

    if not where_group_order:
        where_group_order = '1=1'

    if bind_vars:
        rebound_vars.update({CHK_BIND_VAR_PREFIX + k: v for k, v in bind_vars.items()})

    return chk_values, where_group_order, rebound_vars


class DbBase(SystemConnectorBase, ABC):
    """ abstract database connector base class for the `ae` namespace database system layers.

    This class inherits from :class:`~ae.sys_core.SystemConnectorBase` the following attributes:

        **system**: instance of the related :class:`ae-sys_core.SystemBase` class.

        **console_app**: instance of the :class:`application <ae.console_app.ConsoleApp>` using this database system.

        **last_err_msg**: the error message string of the last error or an empty string
        if no error occurred in the last database action/operation.
    """
    def __init__(self, system: SystemBase):
        """ create instance of generic database object (base class for real database like e.g. postgres or oracle).

        :param system:      :class:`~ae.sys_core.SystemBase` instance. Providing useful attributes, like e.g.:

                            **credentials**: dict with database driver specific account credentials.

                            **features**: list of features. Features will also be passed as connection parameters
                            to the database driver. The main differences to credentials are that a feature without
                            any value will be interpreted as boolean True and that features can have any value that
                            can be specified as a literal (like int or even datetime).

                            **console_app**: instance of the :class:`application <ae.console_app.ConsoleApp>`
                            using this database system.
        """
        super().__init__(system)    # init self.system and self.console_app

        self.conn = None                    #: database driver connection
        self.curs = None                    #: database driver cursor

        self.param_style: str = 'named'     #: database driver bind variable/parameter style

    @abstractmethod
    def connect(self) -> str:
        """ sub-class has to implement this connect method """

    def _adapt_sql(self, sql: str, bind_vars: Dict[str, Any]) -> str:
        """ replace the parameter style of bind variables from `pyformat` into `named`.

        :param sql:         query to scan for named bind variables.
        :param bind_vars:   dict of all available bind variables.
        :return:            adapted query string.

        .. _sql-parameter-style:

        .. note::
            For database drivers - like psycopg2 - that are support only the `pyformat` parameter style syntax
            (in the format ``%(bind_var)s``) the sql query string will be adapted, by converting all bind variables
            from the parameter style `named` into `pyformat`.

            The returned query will be unchanged for all other database drivers (that are directly supporting
            the `named` parameter style).

        """
        new_sql = sql
        if self.param_style == 'pyformat':
            for key in bind_vars.keys():
                new_sql = new_sql.replace(NAMED_BIND_VAR_PREFIX + key, '%(' + key + ')s')
        return new_sql

    def call_proc(self, proc_name: str, proc_args: Sequence, ret_dict: Optional[Dict[str, Any]] = None) -> str:
        """ execute stored procedure on database server.

        :param proc_name:   name of the stored procedure.
        :param proc_args:   tuple of parameters/arguments passed to the stored procedure.
        :param ret_dict:    optional dict - if passed then the dict item with the key `return` will be
                            set/updated to the value returned from the stored procedure/database.
        :return:            empty string if no error occurred else the error message.
        """
        self.last_err_msg = ""
        try:
            assert self.curs is not None, f"call_proc(): cursor is not initialized for {self}"      # mypy
            ret = self.curs.callproc(proc_name, proc_args)
            if ret_dict is not None:
                ret_dict['return'] = ret
        except Exception as ex:
            self.last_err_msg = f"call_proc() error: {ex} for {self}"
        return self.last_err_msg

    def close(self, commit: bool = True) -> str:
        """ close the connection to the database driver and server.

        :param commit:  pass False to prevent commit (and also execute rollback) before closure of connection.
        :return:        empty string if no error occurred else the error message.
        """
        self.last_err_msg = ""
        if self.conn:
            if commit:
                self.last_err_msg = self.commit()
            else:
                self.last_err_msg = self.rollback()
            try:
                if self.curs:
                    self.curs.close()
                    self.curs = None
                    self.console_app.dpo(f"close(): cursor closed for {self}")
                self.conn.close()
                self.conn = None
                self.console_app.dpo(f"close(): connection closed for {self}")
            except Exception as ex:
                self.last_err_msg += f"close() error: {ex} for {self}"
        return self.last_err_msg

    def connect_params(self) -> Dict[str, Any]:
        """ merges self.system.credentials with self.system.features into a database driver connection parameters dict.

        :return:    new dict with the items from self.system.credentials and then extended with the entries of
                    self.system.features.

                    Credential values are always of type str, only features can be of any type. Features without
                    a specified value are set True. All keys of the returned dict will be in lower-case.
        """
        conn_dict = {k.lower(): v for k, v in self.system.credentials.items()}
        for feat in [_ for _ in self.system.features if _]:
            key_val = feat.split('=', maxsplit=1)
            conn_dict[key_val[0].lower()] = try_eval(key_val[1]) if len(key_val) > 1 else True

        if 'url' in conn_dict:
            url_parts = urllib.parse.urlparse(conn_dict.pop('url'))
            if 'user' not in conn_dict and url_parts.username:
                conn_dict['user'] = url_parts.username
            if 'password' not in conn_dict and url_parts.password:
                conn_dict['password'] = url_parts.password
            if 'host' not in conn_dict and url_parts.hostname:
                conn_dict['host'] = url_parts.hostname
            if 'port' not in conn_dict and url_parts.port:
                conn_dict['port'] = url_parts.port
            if 'dbname' not in conn_dict and url_parts.path:
                conn_dict['dbname'] = url_parts.path[1:]      # remove leading slash character (path root)

        return conn_dict

    def create_cursor(self):
        """ allow sub-class to create Python DB API-conform database driver cursor """
        try:
            self.curs = self.conn.cursor()
            self.console_app.dpo(f"create_cursor(): database cursor created for {self}")
        except Exception as ex:
            self.last_err_msg = f"create_cursor() error: {ex} for {self}"

    def cursor_description(self) -> Optional[str]:
        """ return description text if opened cursor or None if cursor is closed or not yet opened. """
        if self.curs is not None:
            return self.curs.description
        return None

    def fetch_all(self) -> Sequence[Tuple]:
        """ fetch all the rows found from the last executed SELECT query.

        :return:        empty list on error or if query result is empty, else a list of database rows.
        """
        self.last_err_msg = ""
        rows: Sequence = []
        try:
            assert self.curs is not None, f"fetch_all(): cursor is not initialized for {self}"      # mypy
            rows = self.curs.fetchall()
            self.console_app.dpo(f"fetch_all(), 1st of {len(rows)} recs: {rows[:1]} for {self}")
        except Exception as ex:
            self.last_err_msg = f"fetch_all() exception: {ex} for {self}"
            self.console_app.po(self.last_err_msg)
        return rows

    def fetch_value(self, col_idx: int = 0) -> Any:
        """ fetch the value of a column of the first/next row of the found rows of the last SELECT query.

        :param col_idx:     index of the column with the value to fetch and return.
        :return:            value of the column at index :paramref:`~.fetch_value.col_idx`.
        """
        self.last_err_msg = ""
        val = None
        try:
            assert self.curs is not None, f"fetch_value(): cursor is not initialized for {self}"        # mypy
            values = self.curs.fetchone()
            if values:
                val = values[col_idx]
            self.console_app.dpo(f"fetch_value() retrieved values: {values}[{col_idx}]={val!r} for {self}")
        except Exception as ex:
            assert self.curs is not None, f"fetch_value()-EXCEPT: cursor is not initialized for {self}"
            self.last_err_msg = \
                f"fetch_value()[{col_idx}] exception: {ex}; status message={self.curs.statusmessage} for {self}"
            self.console_app.po(self.last_err_msg)
        return val

    def execute_sql(self, sql: str, commit: bool = False, bind_vars: Optional[Dict[str, Any]] = None) -> str:
        """ execute sql query with optional bind variables.

        :param sql:         sql query to execute.
        :param commit:      pass True to execute a COMMIT command directly after the query execution.
        :param bind_vars:   optional dict with bind variables.
        :return:            empty string if no error occurred else the error message.
        """
        action = sql.split()[0]
        if action.startswith(('--', '/*')):
            action = 'SCRIPT'
        elif action.upper().startswith('CREATE'):
            action += ' ' + sql.split()[1]

        if self.conn or not self.connect():     # lazy connection
            self.last_err_msg = ""
            sql, bind_vars = _prepare_in_clause(sql, bind_vars)
            sql = self._adapt_sql(sql, bind_vars)
            try:
                assert self.curs is not None, f"execute_sql(): cursor is not initialized for {self}"    # mypy
                if bind_vars:
                    self.curs.execute(sql, bind_vars)
                else:
                    # if no bind vars then call without to prevent error "'dict' object does not support indexing"
                    # .. in scripts with the % char (like e.g. dba_create_audit.sql)
                    self.curs.execute(sql)
                assert self.conn is not None, f"execute_sql(): connection is not initialized for {self}"    # mypy
                if commit:
                    self.conn.commit()
                self.console_app.dpo(f"execute_sql({sql}, {bind_vars}) {action} rows={self.curs.rowcount}"
                                     f" desc:{self.curs.description} for {self}")

            except Exception as ex:
                self.last_err_msg += f"execute_sql() {action} error={ex}; {sql}, {bind_vars} for {self}"

        if self.last_err_msg and self.console_app.debug:
            self.console_app.po(self.last_err_msg)

        return self.last_err_msg

    def delete(self, table_name: str, chk_values: Optional[Dict[str, Any]] = None, where_group_order: str = '',
               bind_vars: Optional[Dict[str, Any]] = None, commit: bool = False) -> str:
        """ execute a DELETE command against a table.

        :param table_name:          name of the database table.
        :param chk_values:          dict of column names/values to identify the record(s) to delete.
        :param where_group_order:   extra sql added after the WHERE clause (merged with chk_values by :meth:`._rebind`).
                                    This string can include additional WHERE expressions with extra bind variables.
        :param bind_vars:           dict of extra bind variables (key=variable name, value=value).
        :param commit:              bool value to specify if commit should be done. Pass True to commit.
        :return:                    last error message or empty string if no errors occurred.
        """
        chk_values, where_group_order, bind_vars = _rebind(chk_values, where_group_order, bind_vars)
        sql = f"DELETE FROM {table_name} WHERE {where_group_order}"

        assert chk_values is not None, f"delete(): chk_values cannot be None for {self}"    # mypy
        with self.thread_lock_init(table_name, chk_values):
            self.execute_sql(sql, commit=commit, bind_vars=bind_vars)

        return self.last_err_msg

    def insert(self, table_name: str, col_values: Dict[str, Any], returning_column: str = '',
               commit: bool = False) -> str:
        """ execute an INSERT command to add one record to a database table.

        :param table_name:          name of the database table.
        :param col_values:          dict of inserted column values with the column name as key.
        :param returning_column:    name of column which value will be returned by next fetch_all/fetch_value() call.
        :param commit:              bool value to specify if commit should be done. Pass True to commit.
        :return:                    last error message or empty string if no errors occurred.
        """
        _normalize_col_values(col_values)
        sql = f"INSERT INTO {table_name} (" + ", ".join(col_values.keys()) \
              + ") VALUES (" + ", ".join([NAMED_BIND_VAR_PREFIX + c for c in col_values.keys()]) + ")"
        if returning_column:
            sql += " RETURNING " + returning_column
        return self.execute_sql(sql, commit=commit, bind_vars=col_values)

    def select(self, from_join: str = "", cols: Sequence[str] = (), chk_values: Optional[Dict[str, Any]] = None,
               where_group_order: str = '', bind_vars: Optional[Dict[str, Any]] = None, hints: str = '') -> str:
        """ execute a SELECT query against a database table.

        :param from_join:           name(s) of the involved database table(s), optional with JOIN clause(s).
                                    Passing an empty string results in a SELECT statement without the FROM keyword.
        :param cols:                sequence of the column names that will be selected and included in the resulting
                                    data-rows.
        :param chk_values:          dict of column names/values to identify selected record(s).
        :param where_group_order:   extra sql added after the WHERE clause (merged with chk_values by :meth:`._rebind`).
                                    This string can include additional WHERE expressions with extra bind variables,
                                    ORDER BY and GROUP BY expressions. These special/extra bind variables have to be
                                    specified in the :paramref:`~.upsert.bind_vars` argument and have to be
                                    prefixed with the string `'CV_'` in the WHERE clause (see also the
                                    :data:`CHK_BIND_VAR_PREFIX` data constant in this module).
        :param bind_vars:           dict of extra bind variables (key=variable name, value=value).
        :param hints:               optional SELECT optimization hint string.
        :return:                    last error message or empty string if no errors occurred.
                                    Use the methods :meth:`.fetch_all` or :meth:`.fetch_value` to retrieve
                                    the resulting data-rows.
        """
        if not cols:
            cols = list('*')
        chk_values, where_group_order, bind_vars = _rebind(chk_values, where_group_order, bind_vars)
        if from_join:
            from_join = " FROM " + from_join
        sql = f"SELECT {hints} {','.join(cols)}{from_join} WHERE {where_group_order}"
        return self.execute_sql(sql, bind_vars=bind_vars)

    def update(self, table_name: str, col_values: Dict[str, Any], chk_values: Optional[Dict[str, Any]] = None,
               where_group_order: str = '', bind_vars: Optional[Dict[str, Any]] = None,
               commit: bool = False, locked_cols: Sequence[str] = ()) -> str:
        """ execute an UPDATE command against a database table.

        :param table_name:          name of the database table.
        :param col_values:          dict of inserted/updated column values with the column name as key.
        :param chk_values:          dict of column names/values to identify affected record(s).
                                    If not passed then the first name/value of :paramref:`~update.col_values` is
                                    used as primary key check/filter value.
        :param where_group_order:   extra sql added after the WHERE clause (merged with chk_values by :meth:`._rebind`).
                                    This string can include additional WHERE expressions with extra bind variables,
                                    ORDER BY and GROUP BY expressions. These special/extra bind variables have to be
                                    specified in the :paramref:`~.upsert.bind_vars` argument and have to be
                                    prefixed with the string `'CV_'` (see also the :data:`CHK_BIND_VAR_PREFIX`
                                    data constant in this module).
        :param bind_vars:           dict of extra bind variables (key=variable name, value=value).
        :param commit:              bool value to specify if commit should be done. Pass True to commit.
        :param locked_cols:         list of column names not be overwritten on update of column value is not empty.
        :return:                    last error message or empty string if no errors occurred.
        """
        _normalize_col_values(col_values)
        chk_values, where_group_order, bind_vars = _rebind(chk_values, where_group_order, bind_vars,
                                                           extra_bind=col_values)
        sql = "UPDATE " + table_name \
              + " SET " + ", ".join([
                  f"{col} = " + (f"COALESCE({col}, {NAMED_BIND_VAR_PREFIX}{col})" if col in locked_cols else
                                 f"{NAMED_BIND_VAR_PREFIX}{col}")
                  for col in col_values.keys()])
        if where_group_order:
            sql += " WHERE " + where_group_order

        assert chk_values is not None, f"update(): chk_values cannot be None (passed col_values) for {self}"    # mypy
        with self.thread_lock_init(table_name, chk_values):
            self.execute_sql(sql, commit=commit, bind_vars=bind_vars)

        return self.last_err_msg

    def upsert(self, table_name: str, col_values: Dict[str, Any], chk_values: Dict[str, Any],
               where_group_order: str = '', bind_vars: Optional[Dict[str, Any]] = None,
               returning_column: str = '', commit: bool = False, locked_cols: Sequence[str] = (),
               multiple_row_update: bool = True) -> str:
        """ execute an INSERT or UPDATE command against a record of a database table (UPDATE if record already exists).

        :param table_name:          name of the database table.
        :param col_values:          dict of inserted/updated column values with the column name as key.
        :param chk_values:          dict of column names/values to identify affected record(s), also used to
                                    check if record already exists (and data has to updated instead of inserted).
                                    If not passed then the first name/value of col_values is used as primary key
                                    check/filter value.
        :param where_group_order:   extra sql added after the WHERE clause (merged with chk_values by :meth:`._rebind`).
                                    This string can include additional WHERE expressions with extra bind variables,
                                    ORDER BY and GROUP BY expressions. These special/extra bind variables have to be
                                    specified in the :paramref:`~.upsert.bind_vars` argument and have to be
                                    prefixed with the string `'CV_'` in the query string (see also the
                                    :data:`CHK_BIND_VAR_PREFIX` data constant in this module).
        :param bind_vars:           dict of extra bind variables (key=variable name, value=value).
        :param returning_column:    name of column which value will be returned by next fetch_all/fetch_value() call.
        :param commit:              bool value to specify if commit should be done. Pass True to commit record changes.
        :param locked_cols:         list of column names not be overwritten on update of column value is not empty.
        :param multiple_row_update: allow update of multiple records with the same chk_values.
        :return:                    last error message or empty string if no errors occurred.
        """
        _normalize_col_values(col_values)

        with self.thread_lock_init(table_name, chk_values):
            if not self.select(table_name, ["count(*)"],
                               chk_values=chk_values, where_group_order=where_group_order, bind_vars=bind_vars):
                count = self.fetch_value()
                if not self.last_err_msg:
                    if count == 1 or (multiple_row_update and count > 1):
                        if not self.update(table_name, col_values, chk_values=chk_values,
                                           where_group_order=where_group_order, bind_vars=bind_vars,
                                           commit=commit, locked_cols=locked_cols) \
                                and returning_column:
                            self.select(table_name, [returning_column],
                                        chk_values=chk_values, where_group_order=where_group_order, bind_vars=bind_vars)
                    elif count == 0:
                        col_values.update(chk_values)
                        self.insert(table_name, col_values, returning_column=returning_column, commit=commit)
                    else:               # count not in (0, 1) and multi_row_update ==
                        self.last_err_msg = f"upsert(): SELECT COUNT(*) returned {count}; args={table_name}, " \
                                            f"{col_values}, {chk_values}, {where_group_order}, {bind_vars} for {self}"
        return self.last_err_msg

    def commit(self, reset_last_err_msg: bool = False) -> str:
        """ commit the current transaction if the database driver supports/implements a commit method.

        :param reset_last_err_msg:  pass True to reset the last error message of this instance before the commit.
        :return:                    last error message or empty string if no error happened.
        """
        if reset_last_err_msg:
            self.last_err_msg = ""

        if self.conn and getattr(self.conn, 'commit', None):
            try:
                assert self.conn is not None, f"rollback(): connection is not initialized for {self}"   # mypy
                self.conn.commit()
                self.console_app.dpo(f"commit() on {self}")
            except Exception as ex:
                self.last_err_msg = f"commit() error: {ex} for {self}"

        return self.last_err_msg

    def rollback(self, reset_last_err_msg: bool = False) -> str:
        """ roll the current transaction back if the DB driver supports transactions and does have a rollback method.

        :param reset_last_err_msg:  pass True to reset the last error message of this instance before the rollback.
        :return:                    last error message or empty string if no error happened.
        """
        if reset_last_err_msg:
            self.last_err_msg = ""

        if self.conn and getattr(self.conn, 'rollback', None):
            try:
                assert self.conn is not None, f"rollback(): connection is not initialized for {self}"   # mypy
                self.conn.rollback()
                self.console_app.dpo(f"rollback() on {self}")
            except Exception as ex:
                self.last_err_msg = f"rollback() error: {ex} for {self}"

        return self.last_err_msg

    def get_row_count(self) -> int:
        """ determine rowcount of last executed query.

        :return:    the number of affected rows of the last query.
        """
        assert self.curs is not None, f"get_row_count(): cursor is not initialized for {self}"      # mypy
        return self.curs.rowcount

    def selected_column_names(self) -> List[str]:
        """ determine the column names fo the last executed SELECT query.

        :return:    list of column names - order by column index.
        """
        curs_desc = self.cursor_description()
        col_names = []
        if curs_desc:
            for col_desc in curs_desc:
                col_names.append(col_desc[0])
        return col_names

    @staticmethod
    def thread_lock_init(table_name: str, chk_values: Dict[str, Any]) -> NamedLocks:
        """ created named locking instance for passed table and filter/check expression.

        :return:    :class:`~.lockname.NamedLocks` instance for this table and filter.
        """
        return NamedLocks(table_name + str(sorted(chk_values.items())))
