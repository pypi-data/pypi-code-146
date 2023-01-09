import json
from pathlib import Path

import pytest
from requests import Response

from compredict.client import api
from compredict.connection import Connection
from compredict.resources import Task


@pytest.fixture(scope='session')
def api_client():
    api_client = api.get_instance(token='sometoken', validate=False)
    return api_client


@pytest.fixture(scope='session')
def connection():
    connection = Connection(url="https://core.compredict.ai/api/")
    return connection


@pytest.fixture(scope='session')
def connection_with_fail_on_true():
    connection_with_fail_on_true = Connection(url="https://core.compredict.ai/api/")
    connection_with_fail_on_true.fail_on_error = True
    return connection_with_fail_on_true


@pytest.fixture(scope="session")
def unsucessful_content():
    unsucessful_content = {
        'error': "True",
        'error_msg': 'Bad request'

    }
    return unsucessful_content


@pytest.fixture(scope="session")
def successful_content():
    successful_content = {
        "error": "False",
        "result": "some result"
    }
    return successful_content


@pytest.fixture(scope="session")
def successful_cancel_task_response():
    successful_task_response = {
        "job_id": '35f438fd-6c4d-42a1-8ad0-dfa8dbfcf5da',
        "status": 'Canceled',
        "callback_param": None
    }
    return successful_task_response


@pytest.fixture(scope='session')
def task():
    task = Task()
    return task


@pytest.fixture(scope='session')
def object():
    object = {
        "status": "In Progress"
    }
    return object


@pytest.fixture(scope='session')
def data():
    data = {"1": [346.5, 6456.6, 56.7], "2": [343.4, 34.6, 45.7]}
    return data


@pytest.fixture(scope='session')
def versions():
    versions = [{
        'version': '1.3.0',
        'change_description': 'New features added',
        'results': 'All the requests will be send to queue system',
        'features_format': [],
        'output_format': []
    },
        {
            'version': '1.4.0',
            'change_description': 'Even more features added',
            'results': 'All the requests will be send to queue system',
            'features_format': [],
            'output_format': []
        }]
    return versions


@pytest.fixture(scope='session')
def result():
    result = {
        'reference': '12jffd',
        'status': "Finished",
        'results': []
    }
    return result


@pytest.fixture(scope='session')
def algorithm():
    algorithm = {
        'id': 'mass_estimation',
        'name': 'Mass Estimation',
        'description': 'Some description',
        'versions': [{'mass_estimation': '1.0.0'}, {'mass_estimation': '2.0.0'}],
        'evaluations': []
    }
    return algorithm


@pytest.fixture(scope='session')
def generated_token():
    return {"access": "sometokenvalue", "refresh": "somerefreshtokenvalue"}


@pytest.fixture(scope='session')
def response_factory():
    def response_factory(status_code: int, content: dict, url: str = None):
        response = Response()
        response.status_code = status_code
        response._content = json.dumps(content).encode('utf-8')
        response.url = url
        return response

    return response_factory


@pytest.fixture(scope="session")
def response_400(unsucessful_content, response_factory):
    return response_factory(400, unsucessful_content)


@pytest.fixture(scope="session")
def response_500(unsucessful_content, response_factory):
    return response_factory(500, unsucessful_content)


@pytest.fixture(scope="session")
def response_200(successful_content, response_factory):
    return response_factory(200, successful_content, 'https://core.compredict.ai/api/v1/algorithms/56')


@pytest.fixture(scope="session")
def response_202_cancelled_task(successful_cancel_task_response, response_factory):
    return response_factory(202, successful_cancel_task_response,
                            "https://core.compredict.ai/api/v1/algorithms/tasks/56")


@pytest.fixture(scope="session")
def response_404_task_not_found(unsucessful_content, response_factory):
    return response_factory(404, unsucessful_content, "https://core.compredict.ai/api/v1/algorithms/tasks/56")


@pytest.fixture(scope="session")
def response_200_with_versions(versions, response_factory):
    return response_factory(200, versions, 'https://core.compredict.ai/api/v1/algorithms/56')


@pytest.fixture(scope="session")
def response_200_with_version(versions, response_factory):
    return response_factory(200, versions[0], 'https://core.compredict.ai/api/v1/algorithms/56')


@pytest.fixture(scope="session")
def response_200_with_result(result, response_factory):
    return response_factory(200, result, 'https://core.compredict.ai/api/v1/algorithms/56')


@pytest.fixture(scope="session")
def response_200_with_algorithm(algorithm, response_factory):
    return response_factory(200, algorithm, 'https://core.compredict.ai/api/v1/algorithms/56')


@pytest.fixture(scope="session")
def response_200_with_algorithms(algorithm, response_factory):
    algorithms = [algorithm, algorithm, algorithm]
    return response_factory(200, algorithms, 'https://core.compredict.ai/api/v1/algorithms/56')


@pytest.fixture(scope="session")
def response_200_with_job_id(response_factory):
    content = {"job_id": "s1o2m3e4-jobid"}
    return response_factory(200, content, 'https://core.compredict.ai/api/v1/algorithms/example-slug/fit')


@pytest.fixture(scope='session')
def response_200_with_tokens_generated(response_factory, generated_token):
    return response_factory(200, generated_token, 'https://core.compredict.ai/api/v2/token/')


@pytest.fixture(scope='session')
def response_200_with_refreshed_token(response_factory):
    refreshed_token = {'access': 'refreshedtoken'}
    return response_factory(200, refreshed_token, 'https://core.compredict.ai/api/v2/token/refresh')


@pytest.fixture(scope='session')
def response_400_with_credentials_error(response_factory):
    error = {
        "status": False,
        "errors": [
            "features : Input name: `username` is mandatory but not provided!"
        ]
    }
    return response_factory(400, error, 'https://core.compredict.ai/api/v2/token/')


@pytest.fixture(scope='session')
def response_400_with_wrong_refresh_token(response_factory):
    error = {
        "status": False,
        "errors": [
            "features : Input name: `refresh` is invalid!"
        ]
    }
    return response_factory(400, error, 'https://core.compredict.ai/api/v2/token/refresh/')


@pytest.fixture(scope='session')
def response_200_token_verified(response_factory):
    verified = {}
    return response_factory(200, verified, 'https://core.compredict.ai/api/v2/token/verify/')


@pytest.fixture(scope='session')
def response_429_throttling_error(response_factory):
    error = {
        "status": False,
        "error": "Request was throttled. Expected available in 6 seconds."
    }
    return response_factory(429, error, 'https://core.compredict.ai/api/v2/token/verify/')


@pytest.fixture(scope="session")
def response_502_with_html():
    html_file = Path(__file__).resolve().parent / "media/test.txt"
    response_502_with_html = Response()
    response_502_with_html.status_code = 502
    response_502_with_html._content = html_file.read_bytes()
    return response_502_with_html


@pytest.fixture(scope="session")
def response_200_with_url(successful_content):
    response_200_with_url = Response()
    response_200_with_url.status_code = 200
    response_200_with_url._content = json.dumps(successful_content).encode('utf-8')
    response_200_with_url.url = 'https://core.compredict.ai/api/v1/algorithms/56/graph'
    response_200_with_url.headers['Content-Type'] = 'image/png'
    return response_200_with_url


@pytest.fixture(scope="session")
def features_path():
    features = Path(__file__).resolve().parent / "media/features.parquet"
    return features.__str__()


@pytest.fixture(scope="session")
def parameters_path():
    parameters = Path(__file__).resolve().parent / "media/parameters-example.json"
    return parameters.__str__()
