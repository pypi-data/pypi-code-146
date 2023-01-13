import os
from increment_package_version import get_current_version, increment_version


def reset_version(path_to_version_file: str) -> None:
    with open(path_to_version_file, "r+") as f:
        f.truncate(0)
        f.write("0.0.0")


def tag_version_as_pre_release(path_to_version_file: str) -> None:
    with open(path_to_version_file, "r+") as f:
        f.truncate(0)
        f.write("1.0.0-alpha")


def tag_version_as_incremented_pre_release(path_to_version_file: str) -> None:
    with open(path_to_version_file, "r+") as f:
        f.truncate(0)
        f.write("1.0.0-alpha1")


def test_get_current_version_return_none_for_no_pre_release(
    path_to_version_file: str = os.path.abspath("./test/test_version.txt"),
) -> None:
    _, _, pre_release_number = get_current_version(path_to_version_file)
    assert pre_release_number is None


def test_get_current_version_return_zero_pre_release_number(
    path_to_version_file: str = os.path.abspath("./test/test_version.txt"),
) -> None:
    tag_version_as_pre_release(path_to_version_file)
    _, _, pre_release_number = get_current_version(path_to_version_file)
    reset_version(path_to_version_file)
    assert pre_release_number == "0"


def test_get_current_version_return_incremented_pre_release_number(
    path_to_version_file: str = os.path.abspath("./test/test_version.txt"),
) -> None:
    tag_version_as_incremented_pre_release(path_to_version_file)
    _, _, pre_release_number = get_current_version(path_to_version_file)
    reset_version(path_to_version_file)
    assert pre_release_number == "1"


def test_increment_version_major_increment_in_test(
    path_to_version_file: str = os.path.abspath("./test/test_version.txt"),
) -> None:
    version, _, _ = get_current_version(path_to_version_file)
    major, minor, patch = version.split(".")
    expected_new_version = f"{int(major)+1}.{minor}.{patch}-alpha"
    commit_msg = "This is a major update with breaking changes, in test environment"
    new_version = increment_version(
        path_to_version_file, test=True, commit_msg=commit_msg
    )
    reset_version(path_to_version_file)
    assert new_version == expected_new_version


def test_increment_version_minor_increment_in_test(
    path_to_version_file: str = os.path.abspath("./test/test_version.txt"),
) -> None:
    version, _, _ = get_current_version(path_to_version_file)
    major, minor, patch = version.split(".")
    expected_new_version = f"{major}.{int(minor)+1}.{patch}-alpha"
    commit_msg = "This is a minor update without breaking changes, in test environment"
    new_version = increment_version(
        path_to_version_file, test=True, commit_msg=commit_msg
    )
    reset_version(path_to_version_file)
    assert new_version == expected_new_version


def test_increment_version_patch_increment_in_test(
    path_to_version_file: str = os.path.abspath("./test/test_version.txt"),
) -> None:
    version, _, _ = get_current_version(path_to_version_file)
    major, minor, patch = version.split(".")
    expected_new_version = f"{major}.{minor}.{int(patch)+1}-alpha"
    commit_msg = "This is a bugfix"
    new_version = increment_version(
        path_to_version_file, test=True, commit_msg=commit_msg
    )
    reset_version(path_to_version_file)
    assert new_version == expected_new_version


def test_increment_version_major_increment_in_prod(
    path_to_version_file: str = os.path.abspath("./test/test_version.txt"),
) -> None:
    os.environ["ENV"] = "test"
    version, _, _ = get_current_version(path_to_version_file)
    major, minor, patch = version.split(".")
    commit_msg = "This is a major update with breaking changes, in prod environment"
    increment_version(path_to_version_file, test=True, commit_msg=commit_msg)
    os.environ["ENV"] = "prod"
    new_version_in_prod = increment_version(
        path_to_version_file, test=True, commit_msg=""
    )
    expected_new_version = f"{int(major)+1}.{minor}.{patch}"
    reset_version(path_to_version_file)
    os.environ["ENV"] = "test"
    assert new_version_in_prod == expected_new_version


def test_increment_version_minor_increment_in_prod(
    path_to_version_file: str = os.path.abspath("./test/test_version.txt"),
) -> None:
    os.environ["ENV"] = "test"
    version, _, _ = get_current_version(path_to_version_file)
    major, minor, patch = version.split(".")
    commit_msg = "This is a minor update without breaking changes, in prod environment"
    increment_version(path_to_version_file, test=True, commit_msg=commit_msg)
    os.environ["ENV"] = "prod"
    new_version_in_prod = increment_version(
        path_to_version_file, test=True, commit_msg=""
    )
    expected_new_version = f"{major}.{int(minor)+1}.{patch}"
    reset_version(path_to_version_file)
    os.environ["ENV"] = "test"
    assert new_version_in_prod == expected_new_version


def test_increment_version_patch_increment_in_prod(
    path_to_version_file: str = os.path.abspath("./test/test_version.txt"),
) -> None:
    os.environ["ENV"] = "test"
    version, _, _ = get_current_version(path_to_version_file)
    major, minor, patch = version.split(".")
    commit_msg = "This is just a patch in prod"
    increment_version(path_to_version_file, test=True, commit_msg=commit_msg)
    os.environ["ENV"] = "prod"
    new_version_in_prod = increment_version(
        path_to_version_file, test=True, commit_msg=""
    )
    expected_new_version = f"{major}.{minor}.{int(patch)+1}"
    reset_version(path_to_version_file)
    os.environ["ENV"] = "test"
    assert new_version_in_prod == expected_new_version


def test_increment_version_is_pre_release(
    path_to_version_file: str = os.path.abspath("./test/test_version.txt"),
) -> None:
    tag_version_as_pre_release(path_to_version_file)
    _, is_pre_release, _ = get_current_version(path_to_version_file)
    reset_version(path_to_version_file)
    assert is_pre_release


def test_increment_version_increment_increment_pre_release_keep_version_constant(
    path_to_version_file: str = os.path.abspath("./test/test_version.txt"),
) -> None:
    tag_version_as_pre_release(path_to_version_file)
    version, _, pre_release_version_before_commit = get_current_version(
        path_to_version_file
    )
    commit_msg = "This is only a pre-release"
    increment_version(path_to_version_file, test=True, commit_msg=commit_msg)
    new_version, _, pre_release_version_after_commit = get_current_version(
        path_to_version_file
    )
    reset_version(path_to_version_file)
    if (
        pre_release_version_before_commit is not None
        and pre_release_version_after_commit is not None
    ):
        assert new_version == version and str(
            int(pre_release_version_after_commit)
        ) == str(int(pre_release_version_before_commit) + 1)
    else:
        assert False


def test_increment_version_increment_incremented_pre_release_keep_version_constant(
    path_to_version_file: str = os.path.abspath("./test/test_version.txt"),
) -> None:
    tag_version_as_incremented_pre_release(path_to_version_file)
    version, _, pre_release_version_before_commit = get_current_version(
        path_to_version_file
    )
    commit_msg = "This is only a pre-release"
    increment_version(path_to_version_file, test=True, commit_msg=commit_msg)
    new_version, _, pre_release_version_after_commit = get_current_version(
        path_to_version_file
    )
    reset_version(path_to_version_file)
    if (
        pre_release_version_before_commit is not None
        and pre_release_version_after_commit is not None
    ):
        assert (
            new_version == version
            and int(pre_release_version_after_commit)
            == int(pre_release_version_before_commit) + 1
        )
    else:
        assert False


def test_increment_version_increment_pre_release_version(
    path_to_version_file: str = os.path.abspath("./test/test_version.txt"),
) -> None:
    tag_version_as_incremented_pre_release(path_to_version_file)
    version, _, pre_release_number = get_current_version(path_to_version_file)
    major, minor, patch = version.split(".")
    if pre_release_number is not None:
        expected_version = f"{major}.{minor}.{patch}-alpha{int(pre_release_number)+1}"
        commit_msg = "This is a pre-release: only increment alpha number"
        new_version = increment_version(
            path_to_version_file, test=True, commit_msg=commit_msg
        )
        reset_version(path_to_version_file)
        assert new_version == expected_version
    else:
        assert False
