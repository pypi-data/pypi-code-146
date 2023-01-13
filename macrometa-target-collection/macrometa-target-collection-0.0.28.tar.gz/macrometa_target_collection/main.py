#!/usr/bin/env python3

import argparse
import asyncio
import io
import json
import sys
from asyncio import AbstractEventLoop
from datetime import datetime
from threading import Thread, Lock

import jsonschema
from adjust_precision_for_schema import adjust_decimal_precision_for_schema
from c8 import C8Client, DocumentInsertError
from c8.collection import StandardCollection
from jsonschema import Draft4Validator
from singer import get_logger

logger = get_logger('macrometa_target_collection')

DEFAULT_BATCH_SIZE_ROWS = 50
DEFAULT_BATCH_FLUSH_INTERVAL = 60
DEFAULT_MIN_BATCH_FLUSH_TIME_GAP = 60


class RecordBatch:
    """Class wrapping the record batch in order to make it thread safe."""

    def __init__(self, config: dict):
        self._list = list()
        self._lock = Lock()
        self.interval = config.get('batch_flush_interval', DEFAULT_BATCH_FLUSH_INTERVAL)
        self.last_executed_time = datetime.now()
        self.min_time_gap = config.get('batch_flush_min_time_gap', DEFAULT_MIN_BATCH_FLUSH_TIME_GAP)
        self.max_batch_size = config.get('batch_size_rows', DEFAULT_BATCH_SIZE_ROWS)

    def append(self, value) -> None:
        """Acquire the lock and add a record to the list."""
        with self._lock:
            self._list.append(value)

    def length(self) -> int:
        """Acquire the lock and return the number of items in the list."""
        with self._lock:
            return len(self._list)

    def flush(self) -> list:
        """Acquire the lock, create a copy of the existing batch,
        clear the existing batch, and return the copy."""
        with self._lock:
            c = self._list.copy()
            self._list.clear()
            return c


def emit_state(state):
    if state is not None:
        line = json.dumps(state)
        logger.debug('Emitting state {}'.format(line))
        sys.stdout.write("{}\n".format(line))
        sys.stdout.flush()


def try_upsert(collection: StandardCollection, record_batch: RecordBatch, force=False):
    if record_batch.length() >= record_batch.max_batch_size or force:
        to_insert = record_batch.flush()
        to_update = []
        for i, r in enumerate(collection.insert_many(to_insert)):
            if type(r) is DocumentInsertError:
                to_update.append(to_insert[i])
        if len(to_update) > 0:
            for i, r in enumerate(collection.update_many(to_update)):
                if type(r) is DocumentInsertError:
                    print(f'Failed to insert/update record: {to_update[i]}. {r}')
        record_batch.last_executed_time = datetime.now()


def try_delete(collection: StandardCollection, _key: str):
    try:
        collection.delete(_key)
    except Exception as e:
        logger.warn(f'Failed to delete record with _key: {_key}. {e}')


def persist_messages(collection: StandardCollection, messages: io.TextIOWrapper, record_batch: RecordBatch):
    state = None
    schemas = {}
    key_properties = {}
    validators = {}

    for message in messages:
        try:
            o = json.loads(message)
        except json.decoder.JSONDecodeError as e:
            logger.error(f"Unable to parse:\n{message}")
            raise e

        message_type = o['type']
        if message_type == 'RECORD':
            stream = o['stream']
            if stream not in schemas:
                raise Exception(f"A record for stream {stream} was encountered before a corresponding schema")

            try:
                validators[stream].validate((o['record']))
            except jsonschema.ValidationError as e:
                logger.error(f"Failed parsing the json schema for stream: {stream}.")
                raise e

            try:
                rec = o['record']
                try:
                    kps = key_properties[stream]
                    if len(kps) > 1:
                        logger.warn(f'Multiple key_properties found ({",".join(kps)}).'
                                    f' Only `{kps[0]}` will be considered.')
                    _key = rec[kps[0]].strip()
                    rec['_key'] = _key
                except:
                    _key = None
                if '_sdc_deleted_at' in rec:
                    if rec['_sdc_deleted_at']:
                        if _key:
                            try_delete(collection, _key)
                    else:
                        rec.pop('_sdc_deleted_at', None)
                        logger.info(f'record is {rec}')
                        record_batch.append(rec)
                else:
                    record_batch.append(rec)
            except TypeError as e:
                # TODO: This is temporary until json serializing issue for Decimals are fixed in pyC8
                logger.debug("pyC8 error occurred")
            state = None
            try_upsert(collection, record_batch)
        elif message_type == 'STATE':
            logger.debug('Setting state to {}'.format(o['value']))
            state = o['value']
        elif message_type == 'SCHEMA':
            stream = o['stream']
            schemas[stream] = o['schema']
            adjust_decimal_precision_for_schema(schemas[stream])
            validators[stream] = Draft4Validator((o['schema']))
            key_properties[stream] = o['key_properties']
        else:
            logger.warning("Unknown message type {} in message {}".format(o['type'], o))
    return state


def setup_batch_task(collection: StandardCollection, record_batch: RecordBatch) -> AbstractEventLoop:
    event_loop = asyncio.new_event_loop()
    Thread(target=start_background_loop, args=(event_loop,), daemon=True).start()
    asyncio.run_coroutine_threadsafe(process_batch(collection, record_batch), event_loop)
    return event_loop


async def process_batch(collection: StandardCollection, record_batch: RecordBatch) -> None:
    while True:
        await asyncio.sleep(record_batch.interval)
        timedelta = datetime.now() - record_batch.last_executed_time
        if timedelta.total_seconds() >= record_batch.min_time_gap:
            # if batch has records that need to be processed but haven't reached batch size then process them.
            try_upsert(collection, record_batch, force=True)


def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file')
    args = parser.parse_args()
    if args.config:
        with open(args.config) as input_json:
            config = json.load(input_json)
    else:
        raise Exception("Required '--config' parameter was not provided")
    region = config['region']
    fabric = config['fabric']
    apikey = config['api_key']
    target_collection = config['target_collection']
    client = C8Client(
        protocol='https',
        host=region,
        port=443,
        apikey=apikey,
        geofabric=fabric
    )
    if not client.has_collection(target_collection):
        client.create_collection(name=target_collection)
    collection = client.get_collection(target_collection)
    record_batch = RecordBatch(config)
    event_loop = setup_batch_task(collection, record_batch)
    input_messages = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    state = persist_messages(collection, input_messages, record_batch)
    # There can still be records in the `record_batch` which is not processed,
    # So, we have to force process it one last time before the workflow terminates.
    try_upsert(collection, record_batch, force=True)
    emit_state(state)
    event_loop.stop()
    logger.info("Exiting normally...")


if __name__ == '__main__':
    main()
