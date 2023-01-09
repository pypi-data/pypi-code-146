def before_run(self, adapter, selected_uids):
    from dbt.node_types import RunHookType
    from datetime import datetime, timezone
    import uuid
    self._sync_id = str(uuid.uuid4())
    execution_time = datetime.now(timezone.utc).isoformat()
    self._execution_time = execution_time

    # We use the execution time as the run_id
    # so each run is unique but we dont use an arbitrary uuid
    self._run_id = execution_time
    with adapter.connection_named('master'):
        self.create_schemas(adapter, selected_uids)
        self.populate_adapter_cache(adapter)
        self.defer_to_manifest(adapter, selected_uids)
        self.safe_run_hooks(adapter, RunHookType.Start, {})


# overrides https://github.com/dbt-labs/dbt-bigquery/blob/main/dbt/adapters/bigquery/connections.py#L442
def execute(self, sql, auto_begin=False, fetch=None):
    from dbt.clients import agate_helper

    from alvin_integration.producers.dbt.lineage.extractors.bigquery import (
        AlvinBigQueryAdapterResponse,
    )

    sql = self._add_query_comment(sql)
    # auto_begin is ignored on bigquery, and only included for consistency
    query_job, iterator = self.raw_execute(sql, fetch=fetch)

    if fetch:
        table = self.get_table_from_response(iterator)
    else:
        table = agate_helper.empty_table()

    message = 'OK'
    code = None
    num_rows = None
    bytes_processed = None

    if query_job.statement_type == 'CREATE_VIEW':
        code = 'CREATE VIEW'

    elif query_job.statement_type == 'CREATE_TABLE_AS_SELECT':
        conn = self.get_thread_connection()
        client = conn.handle
        query_table = client.get_table(query_job.destination)
        code = 'CREATE TABLE'
        num_rows = query_table.num_rows
        num_rows_formated = self.format_rows_number(num_rows)
        bytes_processed = query_job.total_bytes_processed
        processed_bytes = self.format_bytes(bytes_processed)
        message = f'{code} ({num_rows_formated} rows, {processed_bytes} processed)'

    elif query_job.statement_type == 'SCRIPT':
        code = 'SCRIPT'
        bytes_processed = query_job.total_bytes_processed
        message = f'{code} ({self.format_bytes(bytes_processed)} processed)'

    elif query_job.statement_type in ['INSERT', 'DELETE', 'MERGE']:
        code = query_job.statement_type
        num_rows = query_job.num_dml_affected_rows
        num_rows_formated = self.format_rows_number(num_rows)
        bytes_processed = query_job.total_bytes_processed
        processed_bytes = self.format_bytes(bytes_processed)
        message = f'{code} ({num_rows_formated} rows, {processed_bytes} processed)'

    response = AlvinBigQueryAdapterResponse(
        _message=message,
        rows_affected=num_rows,
        code=code,
        bytes_processed=bytes_processed,
        job_id=query_job.job_id if hasattr(query_job, "job_id") else None,
    )

    return response, table
