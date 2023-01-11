import os
import json

from rebapy import RelayClient

PRIVATE_KEY = os.getenv("PK")

if __name__ == "__main__":
    if not PRIVATE_KEY:
        raise Exception("Please set the PK environment variable")

    client = RelayClient(PRIVATE_KEY)

    while True:
        try:
            tx = client.read_tx()
            print(json.dumps(tx.as_dict(), indent=4))
        except KeyboardInterrupt:
            print("Exiting...")
            break
