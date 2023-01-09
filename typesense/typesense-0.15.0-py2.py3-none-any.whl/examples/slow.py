# Demonstrates slowness after deleting data. Run it against a local docker container, that is started with the following command:
# docker run -p 8108:8108 typesense/typesense:0.23.0 --data-dir=/tmp --api-key=abcd

import json
import os
import sys
import typesense
import datetime
import time


def get_client():
    return typesense.Client({
        'api_key': 'abcd',
        'connection_timeout_seconds': 300,
        'nodes': [{
            'host': 'localhost',
            'port': '8108',
            'protocol': 'http',
        }],
    })


def check_collection_exists(client, name):
    for c in client.collections.retrieve():
        if c.get('name') == name:
            return True
    return False


def print_collection_names(client):
    coll_list = []
    for c in client.collections.retrieve():
        coll_list.append(c['name'])
    print(f"Collections: {coll_list}")


def cleanup_collection(client, name):
    print(f"{datetime.datetime.now()} starting to delete {name}")
    try:
        client.collections[name].delete()
    except Exception:
        while check_collection_exists(client, name):
            print("Waiting for the collection to be dropped")
            time.sleep(2)


def create_collection(client, name):
    resp = client.collections.create({
        'name': name,
        'fields': [
            {"name": "id", "type": "string"},
            {"name": "field1", "type": "string"},
            {"name": "field2", "type": "string"}
        ]
    })
    print(resp)


def load_small(client, name, ndocs):
    for i in range(1, ndocs):
        # print(f"{datetime.datetime.now()} {i} before insert into {name}")
        doc = {
            "id": str(i),
            "field1": "foo",
            "field2": "bar"
        }
        client.collections[name].documents.upsert(doc)
        #print(f"{datetime.datetime.now()} {i} after insert into {name}")
        if i % 10 == 0:
            print(f"{datetime.datetime.now()} {i} documents inserted in {name}")


def load_batch(client, name, batch_size, batches):
    print(f"{datetime.datetime.now()} Importing {batches} batches of size {batch_size} to collection {name}")
    doc_list = []
    for i in range(1, batches):
        for j in range(1, batch_size):
            id = batch_size * i + j
            doc = {
                "id": str(id),
                "field1": "foo",
                "field2": "bar"
            }
            doc_list.append(doc)
        print(f"{datetime.datetime.now()}  Batch {i} of {batches}")
        client.collections[name].documents.import_(doc_list)
        doc_list = []


def followup():
    client = get_client()
    # create_collection(client, "collx")
    # cleanup_collection(client, "collx")
    load_small(client, "coll1", 100)


def same_coll_del_write():
    client = get_client()
    cleanup_collection(client, "coll1")
    create_collection(client, "coll1")

    load_batch(client, "coll1", 100 * 1000, 100)

    cleanup_collection(client, "coll1")
    create_collection(client, "coll1")
    load_small(client, "coll1", 100)

def main():
    client = get_client()
    cleanup_collection(client, "coll1")
    cleanup_collection(client, "coll2")
    cleanup_collection(client, "coll3")

    create_collection(client, "coll1")
    create_collection(client, "coll2")
    create_collection(client, "coll3")

    print_collection_names(client)

    load_small(client, "coll1", 100)
    load_batch(client, "coll2", 100*1000, 100)

    cleanup_collection(client, "coll2")
    print_collection_names(client)
    load_small(client, "coll3", 100)

    cleanup_collection(client, "coll1")
    print_collection_names(client)
    create_collection(client, "coll1")
    load_small(client, "coll1", 100)

    # cleanup_collection(client, "coll1")
    # cleanup_collection(client, "coll2")
    # cleanup_collection(client, "coll3")


if __name__ == "__main__":
    # main()
    same_coll_del_write()
    # followup()