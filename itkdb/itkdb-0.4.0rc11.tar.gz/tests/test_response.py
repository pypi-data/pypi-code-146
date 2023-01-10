from __future__ import annotations

import itkdb


def test_paged_response_falsey(mocker):
    session = mocker.MagicMock()
    response = mocker.MagicMock()
    response.json = mocker.MagicMock(
        return_value={"pageInfo": {"pageIndex": 0, "pageSize": 1000, "total": 0}}
    )

    paged = itkdb.responses.PagedResponse(session, response)
    assert paged.total == 0
    assert paged.page_index == 0
    assert paged.page_size == 1000
    assert not paged


def test_paged_response_truthy(mocker):
    session = mocker.MagicMock()
    response = mocker.MagicMock()
    response.json = mocker.MagicMock(
        return_value={"pageInfo": {"pageIndex": 0, "pageSize": 1000, "total": 1}}
    )

    paged = itkdb.responses.PagedResponse(session, response)
    assert paged.total == 1
    assert paged.page_index == 0
    assert paged.page_size == 1000
    assert paged
