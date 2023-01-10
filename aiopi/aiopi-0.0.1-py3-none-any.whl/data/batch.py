import datetime
from typing import Generator, List, Union

import pendulum

from aiopi.exceptions import NoBatchFound
from aiopi.sdk import SDKClient
from aiopi.types import SDKSubBatch, SDKUnitBatch, SubBatchInfo, UnitBatchInfo



async def batch_search(
    client: SDKClient,
    unit_id: str,
    start_time: Union[str, datetime.datetime] = '-100d',
    end_time: Union[str, datetime.datetime] = '*',
    batch_id: str = '*',
    product: str = '*',
    procedure: str = '*',
    sub_batch: str = '*'
) -> List[UnitBatchInfo]:
    """Execute a PI batch search against the module DB. This method is thread safe."""
    start_time = start_time.isoformat() if isinstance(start_time, datetime.datetime) else start_time.lower()
    end_time = end_time.isoformat() if isinstance(end_time, datetime.datetime) else end_time.lower()

    with client.get_connection() as server:
        db = server.PIModuleDB
        unit_batches: List[SDKUnitBatch] = [
            client.unit_batch(batch) for batch in db.PIUnitBatchSearch(
                start_time,
                end_time,
                unit_id,
                batch_id,
                product,
                procedure,
                sub_batch
            )
        ]
        
        if not unit_batches:
            raise NoBatchFound()
        items = []
        
        for unit_batch in unit_batches:
            sub_batch_ref = []
            if unit_batch.PISubBatches.Count > 0:
                unit_sub_batches: List[SDKSubBatch] = [
                    client.sub_batch(batch) for batch in unit_batch.PISubBatches
                ]
                gen = sub_batch_generator()
                gen.__next__()
                while True:
                    try:
                        sub_item = gen.send(unit_sub_batches)
                    except StopIteration:
                        break
                    else:
                        if isinstance(sub_item, dict): # SubBatchInfo
                            sub_batch_ref.append(sub_item)
                        else: # SDKSubBatch
                            unit_sub_batches: List[SDKSubBatch] = [
                                client.sub_batch(batch)
                                for batch in sub_item.PISubBatches
                            ]
            
            unit_batch_info = {
                'unique_id': unit_batch.UniqueID,
                'batch_id': unit_batch.BatchID,
                'start_time': batch_date_to_isoformat(
                    unit_batch.StartTime.LocalDate.ToString()
                ),
                'end_time': batch_end_time(unit_batch),
                'product': unit_batch.Product,
                'procedure': unit_batch.ProcedureName,
                'sub_batches': sub_batch_ref
            }
            items.append(unit_batch_info)
        
        return items


def sub_batch_generator() -> Generator[Union[SubBatchInfo, SDKSubBatch], List[SDKSubBatch], None]:
    sub_batches = yield
    for sub_batch in sub_batches:
        sub_batch_ref = []
        if sub_batch.PISubBatches.Count > 0:
            sub_items: List[SDKSubBatch] = yield sub_batch
            gen = sub_batch_generator()
            gen.__next__()
            while True:
                try:
                    sub_item = gen.send(sub_items)
                except StopIteration:
                    break
                else:
                    if isinstance(sub_item, dict):
                        # bottom level sub batch
                        sub_batch_ref.append(sub_item)
                    else:
                        # sub batch contains sub batches
                        sub_items = yield sub_item
        out = {
            'unique_id': sub_batch.UniqueID,
            'name': sub_batch.Name,
            'start_time': batch_date_to_isoformat(
                sub_batch.StartTime.LocalDate.ToString()
            ),
            'end_time': batch_end_time(sub_batch),
            'sub_batches': sub_batch_ref
        }
        yield out


def batch_date_to_isoformat(timestamp: str) -> str:
    dt: datetime.datetime = pendulum.from_format(
        timestamp,
        'M/D/YYYY h:mm:ss A'
    ).replace(tzinfo=None)
    return dt.isoformat()


def batch_end_time(batch: Union[SDKUnitBatch, SDKSubBatch]) -> str:
    try:
        end_time = batch.EndTime.LocalDate.ToString()
    except AttributeError:
        end_time = None
    finally:
        if end_time is not None:
            end_time = batch_date_to_isoformat(end_time)
    return end_time