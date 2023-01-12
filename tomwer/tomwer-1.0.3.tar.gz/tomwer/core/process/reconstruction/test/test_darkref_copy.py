import os
from tomwer.core.process.reconstruction.darkref.darkrefscopy import DarkRefsCopy
from tomwer.core.utils.scanutils import MockHDF5
import pytest


@pytest.mark.parametrize(
    "process_only_copy_scan_without_raw, process_only_dkrf_scan_without_raw",
    ((False, False), (True, False), (False, True), (True, True)),
)
@pytest.mark.parametrize(
    "process_only_copy_scan_with_raw, process_only_dkrf_scan_with_raw",
    ((False, False), (True, False), (False, True), (True, True)),
)
def test_register_and_copy_darks_and_flats(
    tmp_path,
    process_only_copy_scan_with_raw,
    process_only_dkrf_scan_with_raw,
    process_only_copy_scan_without_raw,
    process_only_dkrf_scan_without_raw,
):
    """
    Test registration and copy of darks and flats
    """
    scan_folder_with_raw = tmp_path / "test_dir_1"
    scan_folder_without_raw = tmp_path / "test_dir_2"
    save_dir = tmp_path / "save_dir"
    for my_dir in (save_dir, scan_folder_with_raw, scan_folder_without_raw):
        os.makedirs(my_dir)

    scan_with_raw = MockHDF5(
        scan_path=scan_folder_with_raw,
        create_ini_dark=True,
        create_ini_ref=True,
        create_final_ref=False,
        n_proj=10,
        n_ini_proj=10,
        dim=12,
    ).scan
    scan_without_raw = MockHDF5(
        scan_path=scan_folder_without_raw,
        create_ini_dark=False,
        create_ini_ref=False,
        create_final_ref=False,
        n_proj=10,
        n_ini_proj=10,
        dim=12,
    ).scan

    # get task ready
    process_with_raw = DarkRefsCopy(
        inputs={
            "data": scan_with_raw,
            "save_dir": save_dir,
            "process_only_copy": process_only_copy_scan_with_raw,
            "process_only_dkrf": process_only_dkrf_scan_with_raw,
        }
    )
    # test processing with flat and dark materials
    process_with_raw.run()
    if process_only_copy_scan_with_raw:
        assert scan_with_raw.load_reduced_darks() in (None, {})
        assert scan_with_raw.load_reduced_flats() in (None, {})
    else:
        assert scan_with_raw.load_reduced_darks() not in (None, {})
        assert scan_with_raw.load_reduced_flats() not in (None, {})

    # test processing without flat and dark materials (where copy can happen)
    process_without_raw = DarkRefsCopy(
        inputs={
            "data": scan_without_raw,
            "save_dir": save_dir,
            "process_only_copy": process_only_copy_scan_without_raw,
            "process_only_dkrf": process_only_dkrf_scan_without_raw,
        }
    )

    process_without_raw.run()
    if process_only_copy_scan_with_raw or process_only_dkrf_scan_without_raw:
        assert scan_without_raw.load_reduced_darks() in (None, {})
        assert scan_without_raw.load_reduced_flats() in (None, {})
    elif process_only_dkrf_scan_without_raw:
        assert scan_without_raw.load_reduced_darks() not in (None, {})
        assert scan_without_raw.load_reduced_flats() not in (None, {})
