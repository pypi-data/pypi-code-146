from cgitb import text
import uuid
from logging import ERROR, DEBUG
from httpx import Response

from common.lineage.lineage_client import LineageClient

async def test_lineage_client_check_log_level_debug():
    boto3_client = LineageClient(atlas_endpoint="test", username='test', password='test')
    assert boto3_client.logger.level == ERROR

    await boto3_client.debug_on()
    assert boto3_client.logger.level == DEBUG


async def test_lineage_client_check_log_level_ERROR():
    boto3_client = LineageClient(atlas_endpoint="test", username='test', password='test')
    await boto3_client.debug_on()
    assert boto3_client.logger.level == DEBUG
    
    await boto3_client.debug_off()
    assert boto3_client.logger.level == ERROR

# since the client just a wrapup so here only test the error handling
async def test_lineage_client_create_entity_fail(mocker):
    lineage_client = LineageClient(atlas_endpoint="test", username='test', password='test')

    error_msg = "invalid payload"
    fake_res = Response(status_code=400, text=error_msg)
    _ = mocker.patch("httpx.AsyncClient.post", return_value=fake_res)

    try:
        _ = await lineage_client.update_entity(str(uuid.uuid4()), "test2.py", "test/test2.py", 500, "test2",
            "test2", "project_code", 'test_type')
    except Exception as e:
        assert str(e) == f"Fail to create entity in Atlas with error: {error_msg}"

# since the client just a wrapup so here only test the error handling
async def test_lineage_client_delete_entity_fail(mocker):
    lineage_client = LineageClient(atlas_endpoint="test", username='test', password='test')

    error_msg = "invalid payload"
    fake_res = Response(status_code=400, text=error_msg)
    _ = mocker.patch("httpx.AsyncClient.delete", return_value=fake_res)

    try:
        _ = await lineage_client.delete_entity(str(uuid.uuid4()), 'test_type')
    except Exception as e:
        assert str(e) == f"Fail to delete entity in Atlas with error: {error_msg}"

# since the client just a wrapup so here only test the error handling
async def test_lineage_client_create_lineage_fail(mocker):
    lineage_client = LineageClient(atlas_endpoint="test", username='test', password='test')

    error_msg = "invalid payload"
    fake_res = Response(status_code=400, text=error_msg)
    _ = mocker.patch("httpx.AsyncClient.post", return_value=fake_res)

    try:
        _ = await lineage_client.create_lineage(
            str(uuid.uuid4()),
            str(uuid.uuid4()),
            "test_input",
            "test_output",
            "project_code",
            "copy",
            'test_type'
        )
    except Exception as e:
        assert str(e) == f"Fail to create lineage in Atlas with error: {error_msg}"

# since the client just a wrapup so here only test the error handling
async def test_lineage_client_get_lineage_fail(mocker):
    lineage_client = LineageClient(atlas_endpoint="test", username='test', password='test')

    error_msg = "invalid payload"
    fake_res = Response(status_code=400, text=error_msg)
    _ = mocker.patch("httpx.AsyncClient.get", return_value=fake_res)

    try:
        _ = await lineage_client.get_lineage(str(uuid.uuid4()), 'test_type')
    except Exception as e:
        assert str(e) == f"Fail to get lineage in Atlas with error: {error_msg}"