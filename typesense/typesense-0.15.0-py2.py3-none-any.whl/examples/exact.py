import random
import string

import typesense


def random_string(len: int = 24) -> str:
    return "".join(random.choice(string.ascii_lowercase + "#{}|") for _ in range(len))


COLLECTION = "example"
client = typesense.Client(
    {
        "api_key": "abcd",
        "nodes": [{"host": "localhost", "port": "8108", "protocol": "http"}],
        "connection_timeout_seconds": 5,
    }
)

# client.keys().generateScopedSearchKey('abcde12345', {'filter_by': 'user_id:1000'})
# dV+fBfH5QFBPdkChN9wnlcioi2m/CKke+iOzwY1PBEo=abcd{"filter_by":"user_id:1000"}
# +U0uFmHsWl2lrODIZML7mGBpKS7f49eIl8FALjyN3zc=abcd{"filter_by": "user_id:1000"}
# iRpOk/1pgGdg0+RA0007EVWYx4dfbMG7VwIBeWo8908=abcd{"filter_by":"company_id:124"}

scoped_key = client.keys.generate_scoped_search_key('abcde12345', {"filter_by":"user_id:1000"})
print(scoped_key)
print(scoped_key.decode('utf-8'))