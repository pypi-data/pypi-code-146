import json

import pytest

from unchanged import verify


def test_json_dict(approve):
    verify(
        data=json.dumps({'x': 3, 'y': 40}), 
        path='tests/approved/json_dict.json', 
        approve_diff=approve
    )

def test_json_dict_fails():
    with pytest.raises(AssertionError):
        verify(
            data=json.dumps({'x': 120, 'y': 40, 'z': 1}), 
            path='tests/approved/json_dict.json', 
        )
