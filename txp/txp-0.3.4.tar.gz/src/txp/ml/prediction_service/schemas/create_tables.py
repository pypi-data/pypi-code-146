from google.cloud import bigquery
from google.oauth2 import service_account
import json
import sys

CREDENTIALS_PATH = "../../../txp_cloud/pipelines/credentials/pub_sub_to_bigquery_credentials.json"
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)


def create_table(table, dataset):
    project = credentials.project_id
    table_id = f"{project}.{dataset}.{table}"
    f = open(f'{table}.json')
    schema = json.load(f)
    client.delete_table(table_id, not_found_ok=True)
    table = bigquery.Table(table_id, schema=schema)
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.HOUR,
        field="partition_timestamp",
        expiration_ms=13824000000
    )
    table.clustering_fields = ["tenant_id", "asset_id"]
    client.create_table(table)
    f.close()


def main():
    args = sys.argv[1:]
    if not len(args):
        print("Dataset not specified")
        return
    dataset = args[0]
    create_table("events", dataset)
    create_table("states", dataset)


if __name__ == "__main__":
    main()
