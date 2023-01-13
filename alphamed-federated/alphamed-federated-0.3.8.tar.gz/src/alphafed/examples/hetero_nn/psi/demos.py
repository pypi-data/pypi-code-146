"""PSI demos."""

import random
from typing import List
from uuid import uuid4
from .. import DEV_TASK_ID


_INTERSECTION = [
    'a4806a79-9889-4f7f-99ea-d19cdbd802db',
    '5a41580e-fc37-4cdb-8387-5830d8a913b8',
    '00ae3122-2274-4218-b027-db77f5132ea3',
    'eb8f17d6-e742-498e-becb-5fbffdad8929',
    'ee123794-d916-436b-8828-8e6dae45c700',
    'fb6eff99-3395-4f07-9c79-e444011c07fb'
]


def get_task_id() -> str:
    return DEV_TASK_ID


def get_ids() -> List[str]:
    ids = _INTERSECTION.copy()
    ids.remove(random.choice(_INTERSECTION))
    ids.append(str(uuid4()))
    return ids
