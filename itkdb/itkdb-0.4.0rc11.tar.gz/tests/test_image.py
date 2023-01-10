from __future__ import annotations

import pytest

import itkdb


@pytest.fixture()
def response(mocker):
    response = mocker.MagicMock()
    response.headers = {"content-disposition": "inline; filename=myfilename.ext"}
    response.content = b"Some binary content that pretends to be an image"
    return response


def test_make_image(response):
    image = itkdb.models.Image.from_response(response)
    assert isinstance(image, itkdb.models.Image)
    assert image.filename == "myfilename.ext"
    assert len(image.getvalue()) == 48


def test_save_image(tmpdir, response):
    image = itkdb.models.Image.from_response(response)
    temp = tmpdir.join("saved_image.jpg")
    nbytes = image.save(filename=temp.strpath)
    assert nbytes == 48
