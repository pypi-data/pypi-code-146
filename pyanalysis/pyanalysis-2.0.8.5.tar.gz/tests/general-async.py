# sanity check
import os
import random
import string
from hashlib import sha256

import pytest

from pyanalysis.asyncio.client import PaClient

print(pytest.__version__)


@pytest.mark.asyncio
async def test_connectivity():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    assert await pa_checker.health()


@pytest.mark.asyncio
async def test_connectivity_with():
    async with PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    ) as pa_checker:
        assert await pa_checker.health()


@pytest.mark.asyncio
async def test_get_user():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    me = await pa_checker.me()
    assert me.get("username")
    assert me.get("email")
    assert me.get("disabled") in (True, False)
    assert me.get("disabled") is False  # heh, this check we definitely need)
    assert (
        me.get("password") == "<Hidden>"
    )  # no, you cannot use this password, it's just to prevent leak
    plan = me.get("plan")
    assert plan
    assert plan.get("month_plan")
    assert plan.get("used")


@pytest.mark.asyncio
async def test_use_token():
    pa_checker1 = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    # Need to mention: token obtaining in async version will occur after first api request
    # So we need to do something, e.g. check us
    await pa_checker1.me()
    pa_checker1_token = pa_checker1._session.headers["Authorization"].split(
        " ", maxsplit=1
    )[1]
    pa_checker2 = PaClient(token=pa_checker1_token)
    me = await pa_checker2.me()
    assert me.get("username")


@pytest.mark.asyncio
async def test_wrong_credentials():
    try:
        PaClient(
            username="".join(random.choices(string.ascii_letters, k=16)),
            password="do not use this password :)",
        )
        return False
    except Exception:
        return True


@pytest.mark.asyncio
async def test_known_package():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = await pa_checker.find_package("requests")
    assert resp.get("status")
    assert resp.get("why")
    assert resp.get("weights_by_versions")
    assert resp.get("verdicts_by_versions")
    assert resp.get("files")
    assert resp.get("rules_score")


@pytest.mark.asyncio
async def test_known_package_with_version():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = await pa_checker.find_package("requests", "2.11.1")
    assert resp.get("status")
    assert resp.get("why")
    assert resp.get("weights_by_versions")
    assert len(resp.get("weights_by_versions")) == 1
    assert resp.get("verdicts_by_versions")
    assert len(resp.get("verdicts_by_versions")) == 1
    assert resp.get("files")
    assert resp.get("rules_score")


@pytest.mark.asyncio
async def test_non_existent_package():

    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = await pa_checker.find_package(
        "".join(random.choices(string.ascii_letters, k=16))
    )
    assert resp.get("status") == "Not found"
    assert "404 Status code on pypi.org" in resp.get("why")


@pytest.mark.asyncio
async def test_non_existent_version():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = await pa_checker.find_package("requests", "0.0.0.0.0")
    assert resp.get("status") == "Not found"
    assert "This package with your package_ver not found" in resp.get("why")
    print(resp)


@pytest.mark.asyncio
async def test_knowledge_base_get_file():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = await pa_checker.kb_package("requests", "2.11.1")
    assert resp.get("data")
    package_data = resp.get("data")[0]  # if it is only one package with this version
    file_resp = await pa_checker.kb_file_meta(file_sha256=package_data.get("py")[0])
    file_hash = file_resp.get("data").get("_id")
    assert file_hash == package_data.get("py")[0]

    file_data = await pa_checker.kb_file_bytes(file_sha256=file_hash)
    assert file_hash == sha256(file_data).hexdigest()


@pytest.mark.asyncio
async def test_knowledge_base_non_existent_package():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = await pa_checker.kb_package(
        "".join(random.choices(string.ascii_letters, k=16))
    )
    assert resp.get("status") == "Not found"
    assert "404 Status code on pypi.org" in resp.get("why")


@pytest.mark.asyncio
async def test_knowledge_base_non_existent_version():

    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = await pa_checker.kb_package("requests", "0.0.0.0.0")
    assert resp.get("status") == "Not found"
    assert "This package with your package_ver not found" in resp.get("why")


@pytest.mark.asyncio
async def test_knowledge_base_get_packave_version_list():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = await pa_checker.kb_package_versions("requests")
    assert resp.get("data")
    one_data = resp.get("data")[0]
    assert one_data.get("project") == "requests"
    assert one_data.get("project_ver")
    assert one_data.get("download_url")
    assert one_data.get("creation_date")


@pytest.mark.asyncio
async def test_knowledge_base_get_packave_history():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = await pa_checker.kb_package_history("requests")
    assert resp.get("data")
    one_data = resp.get("data")[0]
    assert one_data.get("project_name") == "requests"
    assert one_data.get("description")


@pytest.mark.asyncio
async def test_knowledge_base_get_file_releases():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = await pa_checker.kb_package("requests", "2.11.1")
    assert resp.get("data")
    package_data = resp.get("data")[0]  # if it is only one package with this version

    file_resp = await pa_checker.kb_file_releases(file_sha256=package_data.get("py")[0])
    #  raise Exception( f"{package_data}\n\n{file_resp}")
    assert any(
        package_data.get("_id") == fresp.get("_id") for fresp in file_resp.get("data")
    )
