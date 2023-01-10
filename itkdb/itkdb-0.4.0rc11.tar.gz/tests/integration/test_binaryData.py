from __future__ import annotations

import betamax

import itkdb


def test_get_image(auth_session):
    with betamax.Betamax(auth_session).use_cassette("test_binaryData.test_get_image"):
        response = auth_session.get(
            "uu-app-binarystore/getBinaryData",
            json={
                "code": "bc2eccc58366655352582970d3f81bf46f15a48cf0cb98d74e21463f1dc4dcb9"
            },
        )
        assert response
        assert response.status_code == 200
        assert response.headers.get("content-type").startswith("image")


def test_get_image_model(auth_client, tmpdir):
    with betamax.Betamax(auth_client).use_cassette("test_binaryData.test_get_image"):
        image = auth_client.get(
            "uu-app-binarystore/getBinaryData",
            json={
                "code": "bc2eccc58366655352582970d3f81bf46f15a48cf0cb98d74e21463f1dc4dcb9"
            },
        )
        assert isinstance(image, itkdb.models.Image)
        assert image.filename == "PB6.CR2"
        assert image.format == "cr2"
        temp = tmpdir.join("saved_image.cr2")
        nbytes = image.save(filename=temp.strpath)
        assert nbytes == 1166


def test_get_plain_text(auth_session):
    with betamax.Betamax(auth_session).use_cassette(
        "test_binaryData.test_get_plainText"
    ):
        response = auth_session.get(
            "uu-app-binarystore/getBinaryData",
            json={
                "code": "5fd40be3b9f9ada57fa47fe4d8b3c48b26055d5d1c6306d76eb2181d20089879"
            },
        )
        assert response
        assert response.status_code == 200
        assert response.headers.get("content-type").startswith("text")


def test_get_plain_text_model(auth_client, tmpdir):
    with betamax.Betamax(auth_client).use_cassette(
        "test_binaryData.test_get_plainText"
    ):
        text = auth_client.get(
            "uu-app-binarystore/getBinaryData",
            json={
                "code": "5fd40be3b9f9ada57fa47fe4d8b3c48b26055d5d1c6306d76eb2181d20089879"
            },
        )
        assert isinstance(text, itkdb.models.Text)
        assert text.filename == "for_gui test3.txt"
        assert text.format == "txt"
        temp = tmpdir.join("saved_text.txt")
        nbytes = text.save(filename=temp.strpath)
        assert nbytes == 23


def test_issue4(auth_session):
    with betamax.Betamax(auth_session).use_cassette("test_binaryData.test_issue4"):
        response = auth_session.get(
            "uu-app-binarystore/getBinaryData",
            json={
                "code": "fe4f85dd3740c53956c22bb4324065b8",
                "contentDisposition": "attachment",
            },
        )
        assert response
        assert response.status_code == 200
        assert response.headers.get("content-type").startswith("text")


def test_issue4_model(auth_client, tmpdir):
    with betamax.Betamax(auth_client).use_cassette("test_binaryData.test_issue4"):
        text = auth_client.get(
            "uu-app-binarystore/getBinaryData",
            json={
                "code": "fe4f85dd3740c53956c22bb4324065b8",
                "contentDisposition": "attachment",
            },
        )
        assert isinstance(text, itkdb.models.Text)
        assert text.filename == "VPA37913-W00221_Striptest_Segment_4_001.dat"
        assert text.format == "dat"
        temp = tmpdir.join("saved_text.dat")
        nbytes = text.save(filename=temp.strpath)
        assert nbytes == 1000


def test_get_zipfile(auth_session):
    with betamax.Betamax(auth_session).use_cassette(
        "test_binaryData.test_get_zipfile", preserve_exact_body_bytes=True
    ):
        response = auth_session.get(
            "uu-app-binarystore/getBinaryData",
            json={"code": "143b2c7182137ff619968f4cc41a18ca"},
        )
        assert response
        assert response.status_code == 200
        assert response.headers.get("content-type").startswith("application/zip")
        assert len(response.content) == 226988


def test_get_zipfile_model(auth_client, tmpdir):
    with betamax.Betamax(auth_client).use_cassette("test_binaryData.test_get_zipfile"):
        zipfile = auth_client.get(
            "uu-app-binarystore/getBinaryData",
            json={"code": "143b2c7182137ff619968f4cc41a18ca"},
        )
        assert isinstance(zipfile, itkdb.models.ZipFile)
        assert zipfile.filename == "configuration_MODULETHERMALCYCLING.zip"
        assert zipfile.format == "zip"
        temp = tmpdir.join("saved_zipfile.zip")
        nbytes = zipfile.save(filename=temp.strpath)
        assert nbytes == 226988


def test_get_image_model_eos(tmpdir, auth_client):
    with betamax.Betamax(auth_client).use_cassette(
        "test_binaryData.test_get_image_model_eos", preserve_exact_body_bytes=True
    ):

        auth = auth_client.post(
            "https://itkpd2eos.unicornuniversity.net/generate-token?path=/eos/atlas/test/itkpd/c/c/c/cccac749f4f3d5e493a0186ca9e42803"
        )
        image = auth_client.get(
            f'https://eosatlas.cern.ch/eos/atlas/test/itkpd/c/c/c/cccac749f4f3d5e493a0186ca9e42803?authz={auth["token"]}',
            verify=itkdb.data / "CERN_chain.pem",
        )

        assert isinstance(image, itkdb.models.Image)
        assert image.filename is None
        assert image.format == "jpg"
        temp = tmpdir.join("saved_image.jpg")
        nbytes = image.save(filename=temp.strpath)
        assert nbytes == 125
