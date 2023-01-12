import re
import os
import json
import requests
import base64
import logging

from qbeast import predefs
from qbeast.config import get_bearer_token, ENDPOINT

s3_regex = re.compile(predefs.s3_pattern)


class CuratorAPIResponse:
    def __init__(self, status_code, message):
        self.code = status_code
        self.message = message
    
    def expected_code(self, expected_code):
        """Checks if the response code is the expected one. Updates the success attribute accordingly"""
        self.success = self.code == expected_code



""" API METHODS """

def _internal_send_post(path, json_data):
    # Prepare requests
    headers = dict()
    headers["Authorization"] = f"Bearer {get_bearer_token()}"

    req = requests.post(f"{ENDPOINT}{path}",
                        headers=headers,
                        json=json_data)
    try:
        response_msg = req.json()
    except json.JSONDecodeError as e:
        response_msg = req.text
        logging.error(response_msg)
        exit(1)

    return CuratorAPIResponse(req.status_code, response_msg)


def _internal_send_get(path, json_data):
    # Prepare requests
    headers = dict()
    headers["Authorization"] = f"Bearer {get_bearer_token()}"

    req = requests.get(f"{ENDPOINT}{path}",
                       headers=headers,
                       json=json_data)

    try:
        response_msg = req.json()
    except json.JSONDecodeError as e:
        response_msg = req.text
        logging.error(response_msg)
        exit(1)

    return CuratorAPIResponse(req.status_code, response_msg)


def _internal_send_patch(path, json_data):
    # Prepare requests
    headers = dict()
    headers["Authorization"] = f"Bearer {get_bearer_token()}"

    req = requests.patch(f"{ENDPOINT}{path}",
                            headers=headers,
                            json=json_data) 
    if req.status_code == 200:
        return CuratorAPIResponse(req.status_code, "")
    try:
        response_msg = req.json()
    except json.JSONDecodeError as e:
        response_msg = req.text
        logging.error(response_msg)
        exit(1)
    return CuratorAPIResponse(req.status_code, response_msg)


def _internal_send_delete(path, json_data):
    # Prepare requests
    headers = dict()
    headers["Authorization"] = f"Bear {get_bearer_token()}"

    req = requests.delete(f"{ENDPOINT}{path}",
                            headers=headers,
                            json=json_data)
    if req.status_code == 204:
        return CuratorAPIResponse(req.status_code, "")
    try:
        response_msg = req.json()
    except json.JSONDecodeError as e:
        response_msg = req.text
        logging.error(response_msg)
        exit(1)

    return CuratorAPIResponse(req.status_code, response_msg)


def get_presigned_url_post(filename, type):
    json_body = {"filename": filename, "type": type}
    success, reply = _internal_send_post(f'/curator/sync-project', json_body)
    return success, reply



""" GETTERS """


def get_projects():
    api_resp = _internal_send_get(f'/curator/projects', None)
    api_resp.expected_code(200)
    return api_resp


def get_project(project_name):
    api_resp = _internal_send_get(f'/curator/projects/{project_name}', None)
    api_resp.expected_code(200)
    return api_resp

def get_snapshots(project_name):
    api_resp = _internal_send_get(f'/curator/projects/{project_name}/snapshots', None)
    api_resp.expected_code(200)
    return api_resp

def get_snapshot(project_name, snapshot_version):
    api_resp = _internal_send_get(f'/curator/projects/{project_name}/snapshots/{snapshot_version}', None)
    api_resp.expected_code(200)
    return api_resp

def get_deployments(project_name):
    api_resp = _internal_send_get(f'/curator/projects/{project_name}/deployments', None)
    api_resp.expected_code(200)
    return api_resp

def get_deployment(project_name, snapshot_version, deployment_name):
    api_resp = _internal_send_get(f'/curator/projects/{project_name}/snapshots/{snapshot_version}/deployments/{deployment_name}', None)
    api_resp.expected_code(200)
    return api_resp

def get_runs(project_name, snapshot_version, deployment_name):
    api_resp = _internal_send_get(f'/curator/projects/{project_name}/snapshots/{snapshot_version}/deployments/{deployment_name}/runs', None)
    api_resp.expected_code(200)
    return api_resp

def get_run(project_name, snapshot_version, deployment_name, run_id):
    api_resp = _internal_send_get(f'/curator/projects/{project_name}/snapshots/{snapshot_version}/deployments/{deployment_name}/runs/{run_id}', None)
    api_resp.expected_code(200)
    return api_resp

def get_run_logs(project_name, snapshot_version, deployment_name, run_id):
    api_resp = _internal_send_get(f'/curator/projects/{project_name}/snapshots/{snapshot_version}/deployments/{deployment_name}/runs/{run_id}/logs', None)
    api_resp.expected_code(200)
    return api_resp


""" SETTERS """


def post_project(name, description):
    json_body = {"name": name, "description": description}
    api_resp = _internal_send_post(f'/curator/projects', json_body)
    api_resp.expected_code(201)
    return api_resp

def patch_project(name, description):
    json_body = {"description": description}
    api_resp = _internal_send_patch(f'/curator/projects/{name}', json_body)
    api_resp.expected_code(200)
    return api_resp

def delete_project(name):
    api_resp = _internal_send_delete(f'/curator/projects/{name}', None)
    api_resp.expected_code(204)
    return api_resp

def post_snapshot(project_name, file_location, snapshot_version):
    with open(file_location, 'rb') as f:
        file_data = f.read()
        encoded_file_data = base64.b64encode(file_data).decode('utf-8')
        json_body = {"project_name": project_name, "archive": encoded_file_data, "version": snapshot_version}
    api_resp = _internal_send_post(f'/curator/projects/{project_name}/snapshots', json_body)
    api_resp.expected_code(201)
    return api_resp
    

def patch_snapshot(project_name, snapshot_version, description):
    json_body = {"description": description}
    api_resp = _internal_send_patch(f'/curator/projects/{project_name}/snapshots/{snapshot_version}', json_body)
    api_resp.expected_code(200)
    return api_resp

def delete_snapshot(project_name, snapshot_version):
    api_resp = _internal_send_delete(f'/curator/projects/{project_name}/snapshots/{snapshot_version}', None)
    api_resp.expected_code(204)
    return api_resp

def post_deployment(project_name, snapshot_version):
    json_body = {"project_name": project_name, "snapshot_version": snapshot_version}
    api_resp = _internal_send_post(f'/curator/projects/{project_name}/snapshots/{snapshot_version}/deployments', json_body)
    api_resp.expected_code(201)
    return api_resp

def patch_deployment(project_name, snapshot_version, deployment_name, description):
    json_body = {"description": description}
    api_resp = _internal_send_patch(f'/curator/projects/{project_name}/snapshots/{snapshot_version}/deployments/{deployment_name}', json_body)
    api_resp.expected_code(200)
    return api_resp

def delete_deployment(project_name, snapshot_version, deployment_name):
    api_resp = _internal_send_delete(f'/curator/projects/{project_name}/snapshots/{snapshot_version}/deployments/{deployment_name}', None)
    api_resp.expected_code(204)
    return api_resp

def post_run(project_name, snapshot_version, deployment_name):
    json_body = {"project_name": project_name, "snapshot_version": snapshot_version, "deployment_name": deployment_name}
    api_resp = _internal_send_post(f'/curator/projects/{project_name}/snapshots/{snapshot_version}/deployments/{deployment_name}/runs', json_body)
    api_resp.expected_code(201)
    return api_resp

def patch_run(project_name, snapshot_version, deployment_name, run_id):
    json_body = {"status": "aborted"}
    api_resp = _internal_send_patch(f'/curator/projects/{project_name}/snapshots/{snapshot_version}/deployments/{deployment_name}/runs/{run_id}', json_body)
    api_resp.expected_code(200)
    return api_resp

def delete_run(project_name, snapshot_version, deployment_name, run_id):
    api_resp = _internal_send_delete(f'/curator/projects/{project_name}/snapshots/{snapshot_version}/deployments/{deployment_name}/runs/{run_id}', None)
    api_resp.expected_code(204)
    return api_resp




