import os
import numpy as np
from silx.io.url import DataUrl
from tomoscan.io import HDF5File
from tomoscan.esrf.scan.hdf5scan import HDF5TomoScan
from ..utils import check_supported, is_writeable


def get_frame_possible_urls(dataset_info, user_dir, output_dir, frame_type):
    """
    Return a list with the possible location of reduced dark/flat frames.

    Parameters
    ----------
    dataset_info: DatasetAnalyzer object
        DatasetAnalyzer object: data structure containing information on the parsed dataset
    user_dir: str or None
        User-provided directory location for the reduced frames.
    output_dir: str or None
        Output processing directory
    frame_type: str
        Frame type, can be "flats" or "darks".
    """
    check_supported(frame_type, ["flats", "darks"], "frame type")

    h5scan = dataset_info.dataset_scanner  # tomoscan object
    if frame_type == "flats":
        dataurl_default_template = h5scan.REDUCED_FLATS_DATAURLS[0]
    else:
        dataurl_default_template = h5scan.REDUCED_DARKS_DATAURLS[0]

    def make_dataurl(dirname):
        # The template formatting should be done by tomoscan in principle, but this complicates logging.
        rel_file_path = dataurl_default_template.file_path().format(
            scan_prefix=dataset_info.dataset_scanner.get_dataset_basename()
        )
        return DataUrl(
            file_path=os.path.join(dirname, rel_file_path),
            data_path=dataurl_default_template.data_path(),
            data_slice=dataurl_default_template.data_slice(),  # not sure if needed
            scheme="silx",
        )

    urls = {"user": None, "dataset": None, "output": None}

    if user_dir is not None:
        urls["user"] = make_dataurl(user_dir)

    # tomoscan.esrf.scan.hdf5scan.REDUCED_{DARKS|FLATS}_DATAURLS.file_path() is a relative path
    # Create a absolute path instead
    urls["dataset"] = make_dataurl(os.path.dirname(h5scan.master_file))

    if output_dir is not None:
        urls["output"] = make_dataurl(output_dir)

    return urls


def get_metadata_url(url, frame_type):
    """
    Return the url of the metadata stored alongside flats/darks
    """
    check_supported(frame_type, ["flats", "darks"], "frame type")
    template_url = getattr(HDF5TomoScan, "REDUCED_%s_METADATAURLS" % frame_type.upper())[0]
    return DataUrl(
        file_path=url.file_path(),
        data_path=template_url.data_path(),
        scheme="silx",
    )


def tomoscan_load_reduced_frames(dataset_info, frame_type, url):
    tomoscan_method = getattr(dataset_info.dataset_scanner, "load_reduced_%s" % frame_type)
    return tomoscan_method(
        inputs_urls=[url],
        return_as_url=True,
        return_info=True,
        metadata_input_urls=[get_metadata_url(url, frame_type)],
    )


def tomoscan_save_reduced_frames(dataset_info, frame_type, url, frames, info):
    tomoscan_method = getattr(dataset_info.dataset_scanner, "save_reduced_%s" % frame_type)
    kwargs = {"%s_infos" % frame_type: info}
    return tomoscan_method(
        frames, output_urls=[url], metadata_output_urls=[get_metadata_url(url, frame_type)], **kwargs
    )


def update_dataset_info_flats_darks(dataset_info, flatfield_mode, output_dir=None, darks_flats_dir=None):
    """
    Update a DatasetAnalyzer object with reduced flats/darks (hereafter "reduced frames").

    How the reduced frames are loaded/computed/saved will depend on the "flatfield_mode" parameter.

    The principle is the following:
    (1) Attempt at loading already-computed reduced frames (XXX_darks.h5 and XXX_flats.h5):
       - First check files in the user-defined directory 'darks_flats_dir'
       - Then try to load from files located alongside the .nx dataset (dataset directory)
       - Then try to load from output_dir, if provided
    (2) If loading fails, or flatfield_mode == "force_compute", compute the reduced frames.
    (3) Save these reduced frames
       - Save in darks_flats_dir, if provided by user
       - Otherwise, save in the data directory (next to the .nx file), if write access OK
       - Otherwise, save in output directory
    """
    if flatfield_mode is False:
        return
    logger = dataset_info.logger
    frames_types = ["darks", "flats"]

    reduced_frames_urls = {}
    for frame_type in frames_types:
        reduced_frames_urls[frame_type] = get_frame_possible_urls(dataset_info, darks_flats_dir, output_dir, frame_type)

    reduced_frames = dict.fromkeys(frames_types, None)

    #
    # Try to load frames
    #
    def load_reduced_frame(url, frame_type, frames_loaded, reduced_frames):
        if frames_loaded[frame_type]:
            return
        frames, info = tomoscan_load_reduced_frames(dataset_info, frame_type, url)
        if frames not in (None, {}):
            dataset_info.logger.info("Loaded %s from %s" % (frame_type, url.file_path()))
            frames_loaded[frame_type] = True
            reduced_frames[frame_type] = frames, info
        else:
            msg = "Could not load %s from %s" % (frame_type, url.file_path())
            logger.error(msg)

    frames_loaded = dict.fromkeys(frames_types, False)
    if flatfield_mode != "force-compute":
        for load_from in ["user", "dataset", "output"]:  # in that order
            for frame_type in frames_types:
                url = reduced_frames_urls[frame_type][load_from]
                if url is None:
                    continue  # cannot load from this source (eg. undefined folder)
                load_reduced_frame(url, frame_type, frames_loaded, reduced_frames)
            if all(frames_loaded.values()):
                break

    if not all(frames_loaded.values()) and flatfield_mode == "force-load":
        raise ValueError("Could not load darks/flats (using 'force-load')")

    #
    # COMPAT. Keep DataUrl - won't be needed in future versions when pipeline will use FlatField
    # instead of FlatFieldDataUrl
    frames_urls = reduced_frames.copy()
    #

    # Compute reduced frames, if needed
    #
    if reduced_frames["flats"] is None:
        reduced_frames["flats"] = dataset_info.dataset_scanner.compute_reduced_flats(return_info=True)
    if reduced_frames["darks"] is None:
        reduced_frames["darks"] = dataset_info.dataset_scanner.compute_reduced_darks(return_info=True)

    if reduced_frames["darks"][0] == {} or reduced_frames["flats"][0] == {}:
        raise ValueError(
            "Could not get any reduced flat/dark. This probably means that no already-reduced flats/darks were found and that the dataset itself does not have any flat/dark"
        )

    #
    # Save reduced frames
    #

    def save_reduced_frame(url, frame_type, frames_saved):
        frames, info = reduced_frames[frame_type]
        tomoscan_save_reduced_frames(dataset_info, frame_type, url, frames, info)
        dataset_info.logger.info("Saved reduced %s to %s" % (frame_type, url.file_path()))
        frames_saved[frame_type] = True

    frames_saved = dict.fromkeys(frames_types, False)
    if not all(frames_loaded.values()):
        for save_to in ["user", "dataset", "output"]:  # in that order
            for frame_type in frames_types:
                if frames_loaded[frame_type]:
                    continue # already loaded
                url = reduced_frames_urls[frame_type][save_to]
                if url is None:
                    continue  # cannot load from this source (eg. undefined folder)
                if not is_writeable(os.path.dirname(url.file_path())):
                    continue
                save_reduced_frame(url, frame_type, frames_saved)
                # COMPAT.
                if frames_urls[frame_type] is None:
                    frames_urls[frame_type] = tomoscan_load_reduced_frames(dataset_info, frame_type, url)
                #
            if all(frames_saved.values()):
                break

    dataset_info.flats = frames_urls["flats"][0]  # reduced_frames["flats"] # in future versions
    dataset_info.flats_srcurrent = frames_urls["flats"][1].machine_electric_current
    # This is an extra check to avoid having more than 1 (reduced) dark.
    # FlatField only works with exactly 1 (reduced) dark (having more than 1 series of darks makes little sense)
    # This is normally prevented by tomoscan HDF5FramesReducer, but let's add this extra check
    darks_ = frames_urls["darks"][0] # reduced_frames["darks"] # in future versions
    if len(darks_) > 1:
        dark_idx = sorted(darks_.keys())[0]
        dataset_info.logger.error("Found more that one series of darks. Keeping only the first one")
        darks_ = {dark_idx: darks_[dark_idx]}
    #
    dataset_info.darks = darks_
    dataset_info.darks_srcurrent = frames_urls["darks"][1].machine_electric_current



# tomoscan "compute_reduced_XX" is quite slow. If needed, here is an alternative implementation
def my_reduce_flats(di):
    res = {}
    with HDF5File(di.dataset_hdf5_url.file_path(), "r") as f:
        for data_slice in di.get_data_slices("flats"):
            data = f[di.dataset_hdf5_url.data_path()][data_slice.start : data_slice.stop]
            res[data_slice.start] = np.median(data, axis=0)
    return res
