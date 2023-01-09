import pandas as pd

from warpzone.tablestorage.operations import TableOperations


def entities_to_pandas(entities: list, keep_keys: bool = False):
    df = pd.DataFrame.from_records(entities)

    if not keep_keys:
        df = df.drop(columns=["PartitionKey", "RowKey"])

    return df


def pandas_to_table_operations(
    df: pd.DataFrame,
    partition_keys: list[str],
    row_keys: list[str],
    operation_type: str = "upsert",
) -> TableOperations:
    """Convert dataframe into table storage operations.

    Args:
        df (pd.DataFrame): Dataframe of interest.
        partition_keys (typing.List[str]): List of partition keys.
        row_keys (typing.List[str]): List of row keys.
        operation_type (str): The opeartion you want done on the entities.
            Possible values are:
                - 'insert'
                - 'update'
                - 'upsert'

    Returns:
        TableOperations: TableOperation object that can be executed.
    """
    datetime_columns = df.select_dtypes(["datetime", "datetimetz"]).columns

    for column in datetime_columns:
        df[column] = df[column].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        df[f"{column}@odata.type"] = "Edm.DateTime"

    df["PartitionKey"] = df[partition_keys].agg("_".join, axis=1)
    df["RowKey"] = df[row_keys].agg("_".join, axis=1)

    table_operations = TableOperations()
    for _, partition_group in df.groupby(partition_keys):
        entities = partition_group.to_dict("records")
        table_operations.add(entities, operation_type)

    return table_operations
