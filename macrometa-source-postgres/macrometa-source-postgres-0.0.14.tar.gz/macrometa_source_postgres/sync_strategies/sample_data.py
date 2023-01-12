from functools import partial

import psycopg2
import psycopg2.extras
from singer import metadata

import macrometa_source_postgres.db as post_db
from macrometa_source_postgres.sync_strategies.common import should_sync_column


# pylint: disable=invalid-name,missing-function-docstring,too-many-locals,duplicate-code
def fetch_view(conn_info, stream, desired_columns, md_map):
    schema_name = md_map.get(()).get('schema-name')
    escaped_columns = map(post_db.prepare_columns_sql, desired_columns)
    samples = []
    with post_db.open_connection(conn_info) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor, name='stitch_cursor') as cur:
            cur.itersize = post_db.CURSOR_ITER_SIZE
            select_sql = f"SELECT {','.join(escaped_columns)} FROM " \
                         f"{post_db.fully_qualified_table_name(schema_name, stream['table_name'])}"
            cur.execute(select_sql)
            for rec in cur:
                rec_msg = post_db.selected_row_to_singer_message(stream, rec, None, desired_columns, None, md_map)
                samples.append(rec_msg.record)
    return samples


# pylint: disable=too-many-statements,duplicate-code
def fetch_table(conn_info, stream, desired_columns, md_map):
    schema_name = md_map.get(()).get('schema-name')
    escaped_columns = map(partial(post_db.prepare_columns_for_select_sql, md_map=md_map), desired_columns)
    samples = []
    with post_db.open_connection(conn_info) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor, name='c8_cursor') as cur:
            cur.itersize = post_db.CURSOR_ITER_SIZE
            fq_table_name = post_db.fully_qualified_table_name(schema_name, stream['table_name'])
            select_sql = f"""SELECT {','.join(escaped_columns)}, xmin::text::bigint
                              FROM {fq_table_name}
                             ORDER BY xmin::text ASC"""
            cur.execute(select_sql)
            for rec in cur:
                rec = rec[:-1]
                rec_msg = post_db.selected_row_to_singer_message(stream, rec, None, desired_columns, None, md_map)
                samples.append(rec_msg.record)
    return samples


def fetch_samples(conn_config, stream):
    """
    Fetch samples for the stream.
    """
    md_map = metadata.to_map(stream['metadata'])
    conn_config['dbname'] = md_map.get(()).get('database-name')
    desired_columns = [c for c in stream['schema']['properties'].keys() if should_sync_column(md_map, c)]
    desired_columns.sort()
    if len(desired_columns) == 0:
        # There are no columns selected for stream. So, skipping it.
        return []
    if md_map.get((), {}).get('is-view'):
        state = fetch_view(conn_config, stream, desired_columns, md_map)
    else:
        state = fetch_table(conn_config, stream, desired_columns, md_map)
    return state
