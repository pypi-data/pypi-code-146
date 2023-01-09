import base64
import hashlib
import json
import os

import click
import requests

from harbour.client.parser import ImageNameParser
from harbour.client.object import Object
from harbour.client.artifact import Artifact


class Client:

    def __init__(self):

        # Builds a base session object
        self.session = requests.Session()

    def configure(self, domain, key, *args, **kwargs):
        """Creates a credentials file under ~/.harbour/credentials.json"""

        in_lambda = os.environ.get('IN_LAMBDA')

        if in_lambda:

            self.__domain = domain
            self.__key = key

            credentials = {
                'domain': domain,
                'key': key,
            }

            return credentials

        filedir = os.path.join(os.path.expanduser("~"), '.harbour')

        os.makedirs(filedir, exist_ok=True)

        filepath = os.path.join(filedir, 'credentials.json')

        with open(filepath, 'w+') as file:

            credentials = {
                'domain': domain,
                'key': key,
            }

            file.write(json.dumps(credentials, indent=3))

        credentials['filepath'] = filepath

        self.output(credentials)

        return credentials

    def authenticate(self):
        """Reads and stores the credentials in the object"""

        in_lambda = os.environ.get('IN_LAMBDA')

        if in_lambda:

            self.session.headers.update(
                {
                    'x-api-key': self.__key
                }
            )

            self.domain = self.__domain

            return self

        # Reads the credentials
        filepath = os.path.join(os.path.expanduser(
            "~"), '.harbour/credentials.json')

        with open(filepath, 'r') as file:

            self.__credentials = json.loads(file.read())

        # Injects it on the object
        self.session.headers.update(
            {
                'x-api-key': self.__credentials['key']
            }
        )

        self.domain = self.__credentials['domain']

        return self

    def request(self, request):
        """Requests a given endpoint"""

        self.authenticate()

        endpoint = request.pop('endpoint')
        endpoint = endpoint[1:] if endpoint.startswith('/') else endpoint

        request['url'] = f'https://{self.domain}/{endpoint}'

        response = self.session.request(**request)

        if response.status_code not in range(200, 399):

            raise Exception(
                f'[{request["url"]}]: ({response.status_code}) {response.reason}')

        else:
            return response.json()

    def output(self, message, *args, **kwargs):
        """Returns a formatted string output"""

        click.echo(json.dumps(message, indent=3))

    def object(self, name, *args, **kwargs):
        """Wrapper method to return objects"""

        return Object(self, name, *args, **kwargs)

    def register(self, path, name, *args, **kwargs):
        """Register a image against the repository"""

        # Parses the image name
        parser = ImageNameParser()
        image = parser.parse(name)

        # Checks if the image already exists. In this case, ask the user if
        # he wants to override it
        key = hashlib.md5(image.encode()).digest().hex()

        object = self.object('register').get(key)

        if object != {}:
            click.confirm('Image already exists. Overwrite?', abort=True)

        # Packages the code
        artifact = Artifact()

        filepath = artifact.package(path)

        # Requests the api to register the package
        with open(filepath, 'rb') as file:

            payload = base64.b64encode(file.read())

        object = self.object('register').create(key=image, object=payload)

        artifact.delete()

        entry = {
            'id': key,
            'image': image,
            'path': path,
            'name': name,
        }

        self.output(entry)

    def execute(self, image, *args, **kwargs):
        """Executes a image"""

        # Creates the image hash
        key = hashlib.md5(image.encode()).digest().hex()

        # Checks if the image exists
        object = self.object('register').get(key)

        if object is None:
            raise ValueError(f'Image {image} does not exists.')

        payload = {
            'image': key,
            **{k: v for k, v in kwargs.items() if v not in [None, {}, []]},
        }

        object = self.object('execution').create(payload)

        self.output(object)
