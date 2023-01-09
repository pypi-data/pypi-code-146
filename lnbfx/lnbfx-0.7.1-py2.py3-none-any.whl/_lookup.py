import json
from collections import namedtuple
from urllib.request import urlretrieve

pipeline_json, _ = urlretrieve("https://lamindb-test.s3.amazonaws.com/pipelines.json")
with open(pipeline_json) as file:
    PIPELINES = json.load(file)


def _lookup(values: dict):
    """Look up a list of values via tab completion."""
    nt = namedtuple("Pipeline", list(values.keys()))  # type: ignore
    return nt(**{key: value for key, value in values.items()})


class lookup:
    pipeline = _lookup(values=PIPELINES)
