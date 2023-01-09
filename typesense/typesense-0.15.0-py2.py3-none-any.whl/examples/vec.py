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
        "name": "color",
        "type": "string",
    },
]
client.collections.create(
    {
        "name": COLLECTION,
        "fields": fields,
    }
)

products = [
    {"title": "Cool trousers", "color": "blue"},
]

client.collections[COLLECTION].documents.import_(products, {"action": "create"})

hits = client.collections[COLLECTION].documents.search(
    {
        "q": "trouzers",
        "query_by": "title,color",
        "query_by_weights": "2,3",
        "num_typos": "2,0",
    }
)["hits"]

print(len(hits))