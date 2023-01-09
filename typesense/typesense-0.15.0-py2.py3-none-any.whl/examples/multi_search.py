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
        "name": "gender",
        "type": "string",
    },
]
client.collections.create(
    {
        "name": COLLECTION,
        "fields": fields,
    }
)

a = client.collections[COLLECTION].synonyms.upsert(
    "foobar", {"synonyms": ["blazer", "suit"]}
)
assert a["synonyms"] == ["blazer", "suit"], "Did the synonym upsert fail?"

a = client.collections[COLLECTION].synonyms.upsert(
    "foobar2", {"synonyms": ["man", "male"]}
)
assert a["synonyms"] == ["man", "male"], "Did the synonym upsert fail?"

products = [
    {"title": "Beautiful Blazer", "gender": "Male"},
]

client.collections[COLLECTION].documents.import_(products, {"action": "create"})

queries = [
    # ("blazer male", "Should match immediately"),
    ("blazer man", "Should match with synonym male<->man"),
    # ("suit male", "Should match with synonym blazer<->suit"),
    # ("suit man", "Should match with synonyms blazer<->suit and male<->man"),
]

for q, desc in queries:
    hits = client.collections[COLLECTION].documents.search(
        {
            "q": q,
            "query_by": "title,gender",
            "drop_tokens_threshold": 0,
        }
    )["hits"]
    print(f'Got {len(hits)} results for "{q}" ({desc})')
