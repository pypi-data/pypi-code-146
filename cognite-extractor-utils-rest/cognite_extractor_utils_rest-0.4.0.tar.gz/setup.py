# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['rest']

package_data = \
{'': ['*']}

install_requires = \
['cognite-extractor-utils>=3.0.2,<4.0.0', 'requests>=2.27.0,<3.0.0']

setup_kwargs = {
    'name': 'cognite-extractor-utils-rest',
    'version': '0.4.0',
    'description': 'REST extention for the Cognite extractor-utils framework',
    'long_description': '# Cognite `extractor-utils` REST extension\n\nThe REST extension for [Cognite `extractor-utils`](https://github.com/cognitedata/python-extractor-utils) provides a way\nto easily write your own extractors for RESTful source systems.\n\nThe library is currently under development, and should not be used in production environments yet.\n\n\n## Overview\n\nThe REST extension for extractor utils templetizes how the extractor will make HTTP requests to the source,\nautomatically serializes the response into user-defined DTO classes, and handles uploading of data to CDF.\n\nThe only part of the extractor necessary to for a user to implement are\n\n * Describing how HTTP requests should be constructed using pre-built function decorators\n * Describing the response schema using Python `dataclass`es\n * Implementing a mapping from the source data model to the CDF data model\n\nFor example, consider [CDF\'s Events API](https://docs.cognite.com/api/v1/#operation/listEvents) as a source. We could\ndescribe the response schema as an `EventsList` dataclass:\n\n``` python\n@dataclass\nclass RawEvent:\n    externalId: Optional[str]\n    dataSetId: Optional[int]\n    startTime: Optional[int]\n    endTime: Optional[int]\n    type: Optional[str]\n    subtype: Optional[str]\n    description: Optional[str]\n    metadata: Optional[Dict[str, str]]\n    assetIds: Optional[List[Optional[int]]]\n    source: Optional[str]\n    id: Optional[int]\n    lastUpdatedTime: Optional[int]\n    createdTime: Optional[int]\n\n\n@dataclass\nclass EventsList:\n    items: List[RawEvent]\n    nextCursor: Optional[str]\n```\n\nWe can then write a handler that takes in one of these `EventList`s, and returns CDF Events, as represented by instances\nof the `Event` class from the `cognite.extractorutils.rest.typing` module.\n\n\n``` python\nextractor = RestExtractor(\n    name="Event extractor",\n    description="Extractor from CDF events to CDF events",\n    version="1.0.0",\n    base_url=f"https://api.cognitedata.com/api/v1/projects/{os.environ[\'COGNITE_PROJECT\']}/",\n    headers={"api-key": os.environ["COGNITE_API_KEY"]},\n)\n\n@extractor.get("events", response_type=EventsList)\ndef get_events(events: EventsList) -> Generator[Event, None, None]:\n    for event in events.items:\n        yield Event(\n            external_id=f"testy-{event.id}",\n            description=event.description,\n            start_time=event.startTime,\n            end_time=event.endTime,\n            type=event.type,\n            subtype=event.subtype,\n            metadata=event.metadata,\n            source=event.source,\n        )\n\nwith extractor:\n    extractor.run()\n\n```\n\nA full example is provided in the [`example.py`](./example.py) file.\n\n### Lists at the root\nUsing Python dataclasses we\'re not able to express JSON structures where the root element \nis a list. To get around that responses of this nature will be automatically converted to something which can be modeled with Python dataclasses. \n\nA JSON structure containing a list as it\'s root element will be converted to an object containing a single key, "items", which has the original JSON list as it\'s value, as in the example below.\n\n```\n[{"object_id": 1}, {"object_id": 2}, {"object_id": 3}]\n```\n\nwill be converted to \n\n```\n{\n    "items": [{"object_id": 1}, {"object_id": 2}, {"object_id": 3}]\n}\n```\n\n## Contributing\n\nWe use [poetry](https://python-poetry.org) to manage dependencies and to administrate virtual environments. To develop\n`extractor-utils`, follow the following steps to set up your local environment:\n\n 1. Install poetry: (add `--user` if desirable)\n    ```\n    $ pip install poetry\n    ```\n 2. Clone repository:\n    ```\n    $ git clone git@github.com:cognitedata/python-extractor-utils-rest.git\n    ```\n 3. Move into the newly created local repository:\n    ```\n    $ cd python-extractor-utils-rest\n    ```\n 4. Create virtual environment and install dependencies:\n    ```\n    $ poetry install\n    ```\n\nAll code must pass typing and style checks to be merged. It is recommended to install pre-commit hooks to ensure that\nthese checks pass before commiting code:\n\n```\n$ poetry run pre-commit install\n```\n\nThis project adheres to the [Contributor Covenant v2.0](https://www.contributor-covenant.org/version/2/0/code_of_conduct/)\nas a code of conduct.\n\n',
    'author': 'Mathias Lohne',
    'author_email': 'mathias.lohne@cognite.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cognitedata/python-extractor-utils-rest',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
