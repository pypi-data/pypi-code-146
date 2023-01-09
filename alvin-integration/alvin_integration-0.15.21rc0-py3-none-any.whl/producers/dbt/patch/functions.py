# overrides https://github.com/dbt-labs/dbt-core/blob/main/core/dbt/task/run.py#L418
# payload based on https://github.com/OpenLineage/OpenLineage/blob/main/integration/dbt/scripts/dbt-ol
from alvin_integration.helper import log_verbose


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
    with adapter.connection_named("master"):
        required_schemas = self.get_model_schemas(adapter, selected_uids)
        self.create_schemas(adapter, required_schemas)
        self.populate_adapter_cache(adapter, required_schemas)
        self.defer_to_manifest(adapter, selected_uids)
        self.safe_run_hooks(adapter, RunHookType.Start, {})


def after_run(self, adapter, results):
    log_verbose("start after_run")
    # in on-run-end hooks, provide the value 'database_schemas', which is a
    # list of unique (database, schema) pairs that successfully executed
    # models were in. For backwards compatibility, include the old
    # 'schemas', which did not include database information.
    import uuid

    from alvin_integration.adapter import AlvinLineageBackendAdapter
    from dbt.contracts.results import NodeStatus
    from dbt.node_types import RunHookType

    database_schema_set = {
        (r.node.database, r.node.schema)
        for r in results
        if r.node.is_relational
        and r.status not in (NodeStatus.Error, NodeStatus.Fail, NodeStatus.Skipped)
    }

    self._total_executed += len(results)

    extras = {
        "schemas": list({s for _, s in database_schema_set}),
        "results": results,
        "database_schemas": list(database_schema_set),
    }
    with adapter.connection_named("master"):
        self.safe_run_hooks(adapter, RunHookType.End, extras)

    # Wrap it up around a try/except so we never break DBT execution
    try:
        backend_adapter = AlvinLineageBackendAdapter()

        import os

        airflow_platform_id = os.environ.get("ALVIN_AIRFLOW_PLATFORM_ID")
        alvin_dbt_platform_id = os.environ.get("ALVIN_DBT_PLATFORM_ID")

        log_verbose(f"airflow_platform_id: {airflow_platform_id}")
        log_verbose(f"alvin_dbt_platform_id: {alvin_dbt_platform_id}")

        summary = {
            "platform_id": alvin_dbt_platform_id,
            "airflow_platform_id": airflow_platform_id,
            "project_id": results[0].node.package_name,
            "nodes": [],
            "execution_time": self._execution_time,
            "sync_id": self._sync_id,
            "run_id": self._run_id,
        }
        for result in results:
            adapter_response = result.adapter_response
            payload = {
                "event_time": adapter_response.get("event_time"),
                "started": adapter_response.get("started"),
                "ended": adapter_response.get("ended"),
                "event_type": result.status.upper(),
                "producer": "alvin.ai",
                "run": {
                    "run_id": self._run_id,
                },
                "job": {
                    "job_id": adapter_response.get("job_id"),
                    "job_name": f"dbt-run-{result.node.package_name}",
                },
                "adapter": "bigquery",
                "job_id": adapter_response.get("job_id"),
                "project_id": result.node.database,  # This isn't the DBT project ID, this is the Bigquery project id...
                "database": result.node.database,
                "code": adapter_response.get("code"),
                "compiled_sql": result.node.compiled_sql
                if hasattr(result.node, "compiled_sql")
                else None,
                "raw_sql": result.node.raw_sql
                if hasattr(result.node, "raw_sql")
                else None,
                "thread_id": result.thread_id,
                "execution_time": result.execution_time,
                "failures": result.failures,
                "message": result.message,
                "package_name": result.node.package_name,
                "root_path": result.node.root_path,
                "schema": result.node.schema,
                "fqn": result.node.fqn,
                "unique_id": result.node.unique_id,
                "path": result.node.path,
                "original_file_path": result.node.original_file_path,
                "name": result.node.name,
                "alias": result.node.alias,
                "resource_type": result.node.resource_type,
                "dependencies": result.node.depends_on.nodes,
            }

            simplified_node = {
                "id": result.node.name,
                "fqn": result.node.fqn,
                "dependencies": result.node.depends_on.nodes,
                "payload": payload
            }
            summary["nodes"].append(simplified_node)

        log_verbose("start send dbt integration request")
        backend_adapter.send_data(summary, "api/dbt/v1/metadata")
        log_verbose("end send dbt integration request")
    except Exception:
        import traceback
        log_verbose(f"Default Callback Error: {traceback.format_exc()}")


# overrides https://github.com/dbt-labs/dbt-bigquery/blob/main/dbt/adapters/bigquery/connections.py#L442
def execute(self, sql, auto_begin=False, fetch=None):
    from alvin_integration.producers.dbt.lineage.extractors.bigquery import (
        AlvinBigQueryAdapterResponse,
    )
    from dbt.clients import agate_helper

    from datetime import datetime, timezone
    event_time = datetime.now(timezone.utc)

    sql = self._add_query_comment(sql)
    # auto_begin is ignored on bigquery, and only included for consistency
    query_job, iterator = self.raw_execute(sql, fetch=fetch)

    if fetch:
        table = self.get_table_from_response(iterator)
    else:
        table = agate_helper.empty_table()

    message = "OK"
    code = None
    num_rows = None
    bytes_processed = None

    if query_job.statement_type == "CREATE_VIEW":
        code = "CREATE VIEW"

    elif query_job.statement_type == "CREATE_TABLE_AS_SELECT":
        conn = self.get_thread_connection()
        client = conn.handle
        query_table = client.get_table(query_job.destination)
        code = "CREATE TABLE"
        num_rows = query_table.num_rows
        num_rows_formated = self.format_rows_number(num_rows)
        bytes_processed = query_job.total_bytes_processed
        processed_bytes = self.format_bytes(bytes_processed)
        message = f"{code} ({num_rows_formated} rows, {processed_bytes} processed)"

    elif query_job.statement_type == "SCRIPT":
        code = "SCRIPT"
        bytes_processed = query_job.total_bytes_processed
        message = f"{code} ({self.format_bytes(bytes_processed)} processed)"

    elif query_job.statement_type in ["INSERT", "DELETE", "MERGE", "UPDATE"]:
        code = query_job.statement_type
        num_rows = query_job.num_dml_affected_rows
        num_rows_formated = self.format_rows_number(num_rows)
        bytes_processed = query_job.total_bytes_processed
        processed_bytes = self.format_bytes(bytes_processed)
        message = f"{code} ({num_rows_formated} rows, {processed_bytes} processed)"

    elif query_job.statement_type == "SELECT":
        conn = self.get_thread_connection()
        client = conn.handle
        # use anonymous table for num_rows
        query_table = client.get_table(query_job.destination)
        code = "SELECT"
        num_rows = query_table.num_rows
        num_rows_formated = self.format_rows_number(num_rows)
        bytes_processed = query_job.total_bytes_processed
        processed_bytes = self.format_bytes(bytes_processed)
        message = f"{code} ({num_rows_formated} rows, {processed_bytes} processed)"

    response = AlvinBigQueryAdapterResponse(
        event_time=event_time,
        _message=message,
        rows_affected=num_rows,
        code=code,
        bytes_processed=bytes_processed,
        started=query_job.started,
        ended=query_job.ended,
        job_id=query_job.job_id if hasattr(query_job, "job_id") else None,
    )

    return response, table
