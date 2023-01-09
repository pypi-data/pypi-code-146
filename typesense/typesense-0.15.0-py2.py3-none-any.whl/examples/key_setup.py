import typesense

COLLECTION = "example"
client = typesense.Client(
    {
        "api_key": "abcd",
        "nodes": [{"host": "localhost", "port": "8108", "protocol": "http"}],
        "connection_timeout_seconds": 2,
    }
)

try:
    client.collections[COLLECTION].delete()
except:
    pass

fields = [
    {
        "name": "title",
        "type": "string",
    },
    {
        "name": "group_id",
        "type": "string",
        "facet": True,
    },
]
client.collections.create(
    {
        "name": COLLECTION,
        "fields": fields,
    }
)

products = [
    {
        "id": "1",
        "title": "Harry Potter 1",
        "group_id": "hp",
    },
    {
        "id": "2",
        "title": "Harry Potter 2",
        "group_id": "hp",
    },
    {
        "id": "3",
        "title": "Lord of the Rings",
        "group_id": "lotr",
    },
]

client.collections[COLLECTION].documents.import_(products, {"action": "create"})

hits = client.collections[COLLECTION].documents.search(
    {
        "q": "*",
        "query_by": "title",
        "pinned_hits": "2:1",
        "group_by": "group_id",
    }
)["grouped_hits"]

for i, hit in enumerate(hits):
    print(f"Result {i} has group key {hit['group_key']}")
