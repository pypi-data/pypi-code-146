from __future__ import annotations

import betamax

import itkdb


def test_list_test_types(auth_session):
    with betamax.Betamax(auth_session).use_cassette("test_tests.test_list_test_types"):
        response = auth_session.get(
            "listTestTypes", json={"project": "S", "componentType": "HYBRID"}
        )
        assert response.status_code == 200
        response = response.json()
        assert response
        assert "pageItemList" in response
        assert "componentType" in response
        assert "pageInfo" in response
        assert "uuAppErrorMap" in response


def test_create_attachment_image_eos(tmpdir, auth_client, monkeypatch):
    monkeypatch.setattr(auth_client, "_use_eos", True)

    image = itkdb.data / "1x1.jpg"
    with betamax.Betamax(auth_client).use_cassette(
        "test_tests.test_create_attachment_image_eos"
    ):

        testRun_before = auth_client.get(
            "getTestRun",
            json={"testRun": "5dde2c1279bc5c000a61d5e2", "outputType": "object"},
        )

        with image.open("rb") as fp:
            data = {
                "testRun": "5dde2c1279bc5c000a61d5e2",
                "title": "MyTestAttachment",
                "description": "This is a test attachment descriptor",
                "type": "file",
                "url": image,
            }
            attachment = {"data": (image.name, fp, "image/jpeg")}

            auth_client.post("createTestRunAttachment", data=data, files=attachment)

        testRun_after = auth_client.get(
            "getTestRun",
            json={"testRun": "5dde2c1279bc5c000a61d5e2", "outputType": "object"},
        )

        assert len(testRun_after["attachments"]) == 1 + len(
            testRun_before["attachments"]
        )
