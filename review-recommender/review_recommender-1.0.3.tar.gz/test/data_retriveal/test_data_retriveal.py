import pytest
import json
import requests
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from review_recommender.data_retriveal import *
import os
dirname = os.path.dirname(__file__)

DATAPATH = os.path.join(dirname, 'data/')
BASEPULLURL = 'https://api.github.com/repos/chaoss/grimoirelab-perceval/pulls/10'
COMMITURL = 'https://api.github.com/repos/chaoss/grimoirelab-perceval/commits/'
COMMITSHA = 'f7cec4254eac3e10c4c75d54b9d5c4d6d88ccd6e'
PULLFILESURL = BASEPULLURL + '/files'


URL2FILENAME = {BASEPULLURL: 'pull_request_10_response.json',
                BASEPULLURL + '/reviews': 'pull_request_10_comments_response.json',
                COMMITURL + COMMITSHA: 'commit.json',
                BASEPULLURL + '/files': 'pull_files.json',
                PULLFILESURL: 'pull_10_files.json',
                'file1_url': 'file1.json',
                'file2_url': 'file2.json'}

def loadJsonFile(filename):
    with open(DATAPATH + filename) as f:
        response = json.load(f)
    return response

def side_effect(url, headers, params, timeout):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    try:
        mock_response.json.return_value = loadJsonFile(URL2FILENAME[url])
    except KeyError:
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.HTTPError()
    return mock_response

class TestSingleRetriveal:

    @patch('requests.Session.get')
    def test_getPullByNumber(self, mock_request):
        repo = RepoRetriveal('chaoss', 'grimoirelab-perceval') 
        
        mock_request.side_effect = side_effect

        pull = repo.getPullByNumber(10)
        assert pull == RepoRetriveal.PullRequest(number=10, 
                                                author_login='albertinisg', 
                                                reviewers=set(['sduenas']), 
                                                date=datetime(2016, 2, 9, 15, 2, 38, tzinfo=timezone.utc))

    @patch('requests.Session.get')
    def test_getPullByNumber_badrepo(self, mock_request):
        repo = RepoRetriveal('badowner', 'badrepo')
        mock_request.side_effect = side_effect
        with pytest.raises(requests.HTTPError):
            repo.getPullByNumber(10)

    @patch('requests.Session.get')
    def test_getCommitBySha(self, mock_request):
        repo = RepoRetriveal('chaoss', 'grimoirelab-perceval')
        mock_request.side_effect = side_effect
        commit = repo.getCommitBySha('f7cec4254eac3e10c4c75d54b9d5c4d6d88ccd6e')
        filesInfo = loadJsonFile('commit.json')['files']
        assert commit == RepoRetriveal.Commit(sha='f7cec4254eac3e10c4c75d54b9d5c4d6d88ccd6e', 
                                                author_login='sduenas', 
                                                filesInfo=filesInfo, 
                                                date=datetime(2022, 11, 7, 9, 0, 33, tzinfo=timezone.utc))
       
class TestIterables:
    @patch('review_recommender.data_retriveal.RepoRetriveal.getPullByNumber')
    def test_getPullIterable(self, mock_method):
        repo = RepoRetriveal('owner', 'repo')
        mock_method.return_value = None

        numberRetrieved = 0
        for pull in repo.getPullIterable(100, 30):
            numberRetrieved += 1
        
        assert numberRetrieved == 30
    
    @patch('review_recommender.data_retriveal.RepoRetriveal.getPullByNumber')
    def test_getPullIterable(self, mock_method):
        repo = RepoRetriveal('owner', 'repo')
        mock_method.return_value = None

        numberRetrieved = 0
        for pull in repo.getPullIterable(10, 30):
            numberRetrieved += 1
        
        assert numberRetrieved == 9

    @pytest.mark.parametrize('numberRequested', [101, 30])
    @patch('review_recommender.data_retriveal.RepoRetriveal.getFromUrl')
    @patch('review_recommender.data_retriveal.RepoRetriveal.getCommitBySha')
    def test_getCommitIterable(self, mock_method, mock_request, numberRequested):
        repo = RepoRetriveal('owner', 'repo')
        mock_request.return_value = [{'sha': 'fakesha'}] * 100
        mock_method.return_value = RepoRetriveal.Commit('fake_sha', 'author', [], datetime.now())

        numberRetrieved = 0
        for commit in repo.getCommitsIterable(datetime.now(), numberRequested):
            numberRetrieved += 1
        
        assert numberRetrieved == numberRequested

class TestFileRetriveal:

    @patch('requests.Session.get')
    def test_getPullFiles(self, mock_request):
        mock_request.side_effect = side_effect

        repo = RepoRetriveal('chaoss', 'grimoirelab-perceval')
        pull = repo.getPullByNumber(10)
        files = repo.getPullFiles(pull)

        assert files[0] == RepoRetriveal.RepoFile('perceval/backend.py', 'content1')
        assert files[1] == RepoRetriveal.RepoFile('perceval/backends/core/github.py', 'content2')

    @patch('requests.Session.get')
    def test_getCommitFiles(self, mock_request):
        mock_request.side_effect = side_effect

        repo = RepoRetriveal('chaoss', 'grimoirelab-perceval')
        commit = repo.getCommitBySha('f7cec4254eac3e10c4c75d54b9d5c4d6d88ccd6e')
        files = repo.getCommitFiles(commit)

        assert files[0] == RepoRetriveal.RepoFile('NEWS', 'content1')
        assert files[1] == RepoRetriveal.RepoFile('perceval/_version.py', 'content2')
        

