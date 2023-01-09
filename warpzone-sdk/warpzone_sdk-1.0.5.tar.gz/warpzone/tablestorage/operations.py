from collections import defaultdict

from .helpers import chunkify


class TableOperations:
    def __init__(self, max_chunk_size: int = 100) -> None:
        self._max_chunk_size = max_chunk_size
        self._partitions = defaultdict(list)

    def add(self, entities: list[dict], operation_mode: str) -> None:
        """Add operations you want to execute to the table storage.

        Args:
            entities (typing.List[typing.Dict]): A list of json entities.
            operation_mode (str): The opeartion you want done on the entities.
                Possible values are:
                    - 'insert'
                    - 'update'
                    - 'delete'
                    - 'upsert'

        Raises:
            ValueError: If the enitity does not contain the required fields.
        """
        for entity in entities:
            try:
                partition_key = entity.get("PartitionKey")
                row_key = entity.get("RowKey")
            except KeyError:
                raise ValueError("Entity must have a PartitionKey and RowKey property.")

            if operation_mode == "delete":
                entity = {"PartitionKey": partition_key, "RowKey": row_key}

            self._partitions[partition_key].append((operation_mode, entity))

    def __iter__(self):
        chunks = []
        for _, operations in self._partitions.items():
            partion_chunks = chunkify(operations, self._max_chunk_size)
            chunks.extend(partion_chunks)

        return iter(chunks)

    def __len__(self):
        return sum(len(partition) for partition in self._partitions.values())
