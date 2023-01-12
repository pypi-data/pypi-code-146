from review_recommender import parse
from unittest.mock import patch
import pytest
import argparse

@patch('sys.argv', ['main', 'owner', 'repo', '10', 'token'])
def test_parse():
    owner, repo, pullNumber, token = parse()
    assert owner == 'owner'
    assert pullNumber == 10
    assert repo == 'repo'
    assert token == 'token'
