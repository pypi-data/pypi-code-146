import pytest

from privateprefs.core.cli import main

test_key = "test key"
test_key2 = "test key2"
test_value = "test value"
test_value2 = "test value2"


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # set up
    main(["delete", "--all"])
    yield
    # tear down
    main(["delete", "--all"])


def test__save(capsys):
    with capsys.disabled():
        main(["save", test_key, test_value])
    main(["load", test_key])
    capture = capsys.readouterr()
    assert capture.out.__contains__(test_value)


def test__load(capsys):
    with capsys.disabled():
        main(["save", test_key, test_value])
    main(["load", test_key])
    capture = capsys.readouterr()
    assert capture.out.__contains__(test_value)


def test__list(capsys):
    with capsys.disabled():
        main(["save", test_key, test_value])
    main(["list"])
    capture = capsys.readouterr()
    contains_test_key = capture.out.__contains__(test_key)
    contains_test_value = capture.out.__contains__(test_value)
    assert all([contains_test_key, contains_test_value])


def test__list__empty(capsys):
    main(["list"])
    capture = capsys.readouterr()
    displays_empty_list = capture.out.__contains__("no key-value pairs saved")
    assert displays_empty_list


def test__delete__all(capsys):
    with capsys.disabled():
        main(["save", test_key, test_value])
        main(["save", test_key2, test_value2])
    main(["delete", "--all"])
    capture = capsys.readouterr()
    all_key_value_deleted = capture.out.__contains__("all key-value pairs deleted")
    assert all_key_value_deleted


def test__delete__key(capsys):
    with capsys.disabled():
        main(["save", test_key, test_value])
    main(["delete", test_key])
    capture = capsys.readouterr()
    test_value_deleted = capture.out.__contains__(test_value)
    assert test_value_deleted


def test__delete__no_args_error(capsys):
    try:
        main(["delete"])
    except SystemExit:
        assert True
    else:
        assert False
