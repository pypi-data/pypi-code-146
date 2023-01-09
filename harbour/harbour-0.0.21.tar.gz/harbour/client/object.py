import hashlib

class Object:

    def __init__(self, client, name, *args, **kwargs):

        self.client = client
        self.name = name

    def get(self, key, hash=False):
        """Returns a object"""

        if hash:
            key = hashlib.md5(key.encode()).digest().hex()

        request = {
            'method': 'GET',
            'endpoint': f'/{self.name}/{key}',
        }

        return self.client.request(request)

    def create(self, object, key=None, hash=False):
        """Creates a object"""

        request = {
            'method': 'POST',
        }

        if hash:
            key = hashlib.md5(key.encode()).digest().hex()

        # Switches the endpoint based on the key
        if key is None:

            request['endpoint'] = f'/{self.name}'

        else:

            request['endpoint'] = f'/{self.name}/{key}'

        # Compress and send
        if isinstance(object, (bytes, bytearray)):

            request['data'] = object

        elif isinstance(object, dict):

            request['json'] = object

        return self.client.request(request)
