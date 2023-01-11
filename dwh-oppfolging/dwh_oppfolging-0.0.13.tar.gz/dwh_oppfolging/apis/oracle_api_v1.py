# pylint: disable=missing-module-docstring
import os
from functools import partial
from typing import Generator, Callable, Any
from datetime import datetime, timedelta
import oracledb
from oracledb.cursor import Cursor
from dwh_oppfolging.apis.secrets_api_v1 import get_secrets


def _fix_timestamp_inputtypehandler(cur, val, arrsize):
    if isinstance(val, datetime) and val.microsecond > 0:
        # pylint: disable=no-member
        return cur.var(oracledb.DB_TYPE_TIMESTAMP, arraysize=arrsize) # type: ignore
        # pylint: enable=no-member
    # No return value implies default type handling
    return None


def create_oracle_connection(user: str):
    """creates oracle connection with db access
    you have to call .commit() yourself"""
    user = user.upper()
    oracle_secrets = get_secrets()["ORACLE_ONPREM"][os.environ["ORACLE_ENV"]]
    con = oracledb.connect(  # type: ignore
        user=oracle_secrets[user+"_USER"],
        password=oracle_secrets[user+"_PW"],
        dsn=oracle_secrets["DSN"],
        encoding="utf-8",
        nencoding="utf-8",
    )
    con.inputtypehandler = _fix_timestamp_inputtypehandler
    return con


def log_etl(
    cur: Cursor,
    schema: str,
    table: str,
    etl_date: datetime,
    rows_inserted: int = -1,
    rows_updated: int = -1,
    rows_deleted: int = -1,
    log_text: str = "",
):
    """inserts into logging table, does not commit"""
    sql = f"insert into {schema}.etl_logg select :0,:1,:2,:3,:4,:5 from dual"
    cur.execute(sql, [table, etl_date, rows_inserted, rows_updated, rows_deleted, log_text])


def is_table_empty(cur: Cursor, schema: str, table: str) -> bool:
    """checks if rowcount is 0"""
    sql = f"select count(*) from {schema}.{table}"
    rowcount = cur.execute(sql).fetchone()[0]  # type: ignore
    return rowcount == 0


def is_table_stale(
    cur: Cursor,
    schema: str, table: str,
    max_hours_behind: int = 72,
    insert_date_column: str = "lastet_dato"
):
    """returns true if table insert date is old"""
    cur.execute(f"select max({insert_date_column}) from {schema}.{table}")
    insert_date: datetime | None = cur.fetchone()[0] # type: ignore
    if insert_date is None:
        return True
    return (datetime.today() - insert_date) >= timedelta(hours=max_hours_behind)


def is_workflow_stale(
    cur: Cursor,
    table_name: str,
    max_hours_behind: int = 24
):
    """returns true if last workflow did not succeed or is too old"""
    cur.execute(
        """
        with t as (
            select
                c.workflow_id workflow_id
                , trunc(c.end_time) updated
                , decode(c.run_err_code, 0, 1, 0) succeeded
                , row_number() over(partition by c.workflow_id order by c.end_time desc) rn
            from
                osddm_report_repos.mx_rep_targ_tbls a
            left join
                osddm_report_repos.mx_rep_sess_tbl_log b
                on a.table_id = b.table_id
            left join
                osddm_report_repos.mx_rep_wflow_run c
                on b.workflow_id = c.workflow_id
            where
                a.table_name = upper(:table_name)
        )
        select * from t where t.rn = 1
        """,
        table_name=table_name # type: ignore
    )
    try:
        row: tuple = cur.fetchone()[0] # type: ignore
        wflow_date: datetime = row[1]
        succeeded = bool(row[2])
    except (TypeError, IndexError) as exc:
        raise Exception(f"Workflow with target {table_name} not found") from exc
    if not succeeded:
        return False
    return (datetime.today().date() - wflow_date.date()) >= timedelta(hours=max_hours_behind)



def execute_stored_procedure(cur: Cursor, schema: str, package: str, procedure: str, *args, **kwargs):
    """execute stored psql procedure does"""
    name = ".".join((schema, package, procedure))
    cur.callproc(name, parameters=args, keyword_parameters=kwargs)


def update_table_from_sql(
    cur: Cursor,
    schema: str,
    table: str,
    update_sql: str,
    bind_today: bool = True,
    bind_name: str = "etl_date",
    enable_logging: bool = True
):
    """basic update of table using provided sql
    if bind_today is set then today() is bound to variable :<bind_name>
    (default: etl_date)
    note that some bind names like "today", and "date" cannot be used.
    """
    today = datetime.today()
    count_sql = f"select count(*) from {schema}.{table}"
    num_rows_old = cur.execute(count_sql).fetchone()[0] # type: ignore
    if bind_today:
        cur.execute(update_sql, {bind_name: today}) # type: ignore
    else:
        cur.execute(update_sql)
    num_rows_new = cur.execute(count_sql).fetchone()[0] # type: ignore
    rows_inserted = num_rows_new - num_rows_old
    rows_updated = cur.rowcount - 1
    print("inserted", rows_inserted, "new records")
    print("updated", rows_updated, "existing records")
    if enable_logging:
        log_etl(cur, schema, table, today, rows_inserted, rows_updated)
        print("logged etl for", table)


def insert_to_table_batched(
    cur: Cursor,
    schema: str,
    table: str,
    batch_factory: Callable[..., Generator[list[dict[str, Any]], None, None]],
    needs_insert_date: bool = True,
    needs_last_modified_date: bool = False,
    last_modified_date_name: str = "",
    skip_on_columns: list[str] | None = None,
    enable_logging: bool = True
):
    """inserts to table in batches generated by the batch factory
    it is assumed that the number and name of columns in each row of each batch remain constant

    if need_insert_date is set,
        insert_date will be sent as a keyword parameter to the batch factory (useful for lastet_dato)
    if needs_last_modified_date is set,
        this date will be fetched from the table in the column given (useful for oppdatert_dato_kilde)
        and then sent as a keyword parameter to the batch factory
        If the table is empty, it defaults to datetime(1900, 1, 1)
    if skip_on_columns are given,
        the rows which whose skip on columns have values already existing in the table
        will not be inserted (useful for hash uniqueness)
    """
    insert_date = datetime.today()
    insert_sql = ""
    insert_fmt = f"insert into {schema}.{table} targ " + "(targ.{col_names}) select (:{col_binds}) from dual src"
    if skip_on_columns is not None and len(skip_on_columns) > 0:
        insert_fmt += (
            f" where not exists (select null from {schema}.{table} t where "
            + " and ".join(f"t.{col} = :{col}" for col in skip_on_columns)
            + " )"
        )
    mod_date_sql = f"select max({last_modified_date_name}) from {schema}.{table}"
    rows_inserted = 0
    if needs_insert_date:
        batch_factory = partial(batch_factory, insert_date=insert_date)
    if needs_last_modified_date:
        last_modified_date = cur.execute(mod_date_sql).fetchone()[0] # type: ignore
        batch_factory = partial(batch_factory, last_modified_date=last_modified_date)
    for batch in batch_factory():
        if not insert_sql:
            cols = [*(batch[0])]
            col_names = ",targ.".join(cols)
            col_binds = ",:".join(cols)
            insert_sql = insert_fmt.format(col_names=col_names, col_binds=col_binds)
        cur.executemany(insert_sql, batch)
        rows_inserted += cur.rowcount
        print("inserted", cur.rowcount, "rows")
    if enable_logging:
        log_etl(cur, schema, table, insert_date, rows_inserted)
        print("logged etl for", table)
