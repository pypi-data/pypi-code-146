import pytest
import privateprefs.core.database as _db

test_key = "test key"
test_key2 = "test key2"
test_value = "test value"
test_value2 = "test value2"


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # set up
    _db.delete_all()
    yield
    # tear down
    _db.delete_all()


def test__save():
    _db.write(test_key, test_value)
    assert _db.read(test_key) == test_value


def test__read():
    _db.write(test_key, test_value)
    assert _db.read(test_key) == test_value


def test__read_keys__as_dict():
    _db.write(test_key, test_value)
    _db.write(test_key2, test_value2)
    key_values = _db.read_keys()
    assert key_values[test_key] == test_value and key_values[test_key2] == test_value2


def test__read_keys__as_dict__filtered():
    _db.write(test_key, test_value)
    _db.write(test_key2, test_value2)
    key_values = _db.read_keys(keys=[test_key2])
    assert key_values[test_key2] == test_value2 and len(key_values) == 1


def test__read_keys__as_list():
    _db.write(test_key, test_value)
    _db.write(test_key2, test_value2)
    key_values = _db.read_keys(return_as_list=True)
    assert key_values[0][1] == test_value and key_values[1][1] == test_value2


def test__read_keys__as_list__filtered():
    _db.write(test_key, test_value)
    _db.write(test_key2, test_value2)
    key_values = _db.read_keys(keys=[test_key2], return_as_list=True)
    assert key_values[0][1] == test_value2 and len(key_values) == 1


def test__delete():
    _db.write(test_key, test_value)
    _db.write(test_key2, test_value2)
    _db.delete(test_key)
    assert _db.read(test_key) is None and _db.read(test_key2) == test_value2


def test__delete_all():
    _db.write(test_key, test_value)
    _db.write(test_key2, test_value2)
    _db.delete_all()
    assert _db.read(test_key) is None


def test__delete_data_file():
    _db.write(test_key, test_value)
    dose_file_exists_before_delete = _db.PATH_TO_DATA_FILE.exists()
    _db._delete_data_file()
    dose_file_exists_after_delete = _db.PATH_TO_DATA_FILE.exists()
    assert dose_file_exists_before_delete is True
    assert dose_file_exists_after_delete is False


def test___delete_project_data_dir():
    _db.write(test_key, test_value)
    dose_dir_exists_before_delete = _db.PATH_TO_USER_DATA_PROJECT_DIR.exists()
    _db._delete_data_file()
    _db._delete_project_data_dir()
    dose_dir_exists_after_delete = _db.PATH_TO_USER_DATA_PROJECT_DIR.exists()
    assert dose_dir_exists_before_delete is True
    assert dose_dir_exists_after_delete is False


def test___delete_project_data_dir__mock_exists__true(mocker):
    mocker.patch(
        'privateprefs.core.database.pathlib.Path.exists',
        return_value=True
    )
    _db.write(test_key, test_value)
    _db._delete_data_file()
    _db._delete_project_data_dir()
    dose_dir_exists_after_delete = _db.PATH_TO_USER_DATA_PROJECT_DIR.exists()
    print(dose_dir_exists_after_delete)
    assert dose_dir_exists_after_delete is True


def test___delete_project_data_dir__mock_exists__false(mocker):
    mocker.patch(
        'privateprefs.core.database.pathlib.Path.exists',
        return_value=False
    )
    _db.write(test_key, test_value)
    _db._delete_data_file()
    _db._delete_project_data_dir()
    dose_dir_exists_after_delete = _db.PATH_TO_USER_DATA_PROJECT_DIR.exists()
    print(dose_dir_exists_after_delete)
    assert dose_dir_exists_after_delete is False


