import pytest
from unittest.mock import patch
import requests_cache
from review_recommender.data_retriveal import RepoRetriveal
from review_recommender.ranker import getRanking
import os
import requests
dirname = os.path.dirname(__file__)

DBPATH = os.path.join(dirname, 'data/test_db')
test_cache = requests_cache.CachedSession(DBPATH, allowable_codes=(200, 404))

def side_effect( url, params=None):
    headers = {"Accept": "application/vnd.github+json"}
    r = test_cache.get(url, headers=headers,
                    params=params,
                    timeout=10)
    r.raise_for_status()
    return r.json()

@patch('review_recommender.data_retriveal.RepoRetriveal.getFromUrl')
def test_getRanking(mock_request):
    mock_request.side_effect = side_effect
    repo = RepoRetriveal('opencv', 'opencv')
    scores = getRanking(repo, 23008, 10, 10)
    #print(scores.getSorted())
    rank = scores.getSorted()

    assert 'alalek' in rank and 'asmorkalov' in rank

@patch('review_recommender.data_retriveal.RepoRetriveal.getFromUrl')
def test_getRanking_bad_number(mock_request):
    mock_request.side_effect = side_effect
    repo = RepoRetriveal('opencv', 'opencv')
    with pytest.raises(requests.HTTPError):
        scores = getRanking(repo, -1, 10, 10)

@patch('review_recommender.data_retriveal.RepoRetriveal.getFromUrl')
def test_getRanking_bad_repo(mock_request):
    mock_request.side_effect = side_effect
    repo = RepoRetriveal('badrepo', 'badrepo')
    with pytest.raises(requests.HTTPError):
        scores = getRanking(repo, 23008, 10, 10)