import httpx
import pytest

@pytest.mark.asyncio
async def test_get_request():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://httpbin.org/get")
        assert response.status_code == 200
        assert response.json()["args"] == {}
