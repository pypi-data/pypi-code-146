from glob import glob
from os import path, getcwd, chdir
from posixpath import join as posix_join
from datetime import datetime
import numpy as np
from h5py import VirtualSource, VirtualLayout
from tomoscan.io import HDF5File
from tomoscan.esrf import EDFVolume
from tomoscan.esrf import HDF5Volume as _HDF5VolumeBase
from tomoscan.esrf import TIFFVolume as _TIFFVolumeBase, MultiTIFFVolume
from tomoscan.esrf import JP2KVolume as _JP2KVolumeBase
from .. import version as nabu_version
from ..utils import merged_shape, deprecation_warning
from ..misc.utils import rescale_data
from .utils import check_h5py_version, convert_dict_values
from silx.io.dictdump import dicttonx
try:
    from glymur import Jp2k, set_option as glymur_set_option
    from glymur.version import openjpeg_version, version as glymur_version
    __have_jp2k__ = True
except ImportError:
    __have_jp2k__ = False

def get_datetime():
    """
    Function used by some writers to indicate the current date.
    """
    return datetime.now().replace(microsecond=0).isoformat()


class Writer:
    """
    Base class for all writers.
    """
    def __init__(self, fname):
        self.fname = fname


    def get_filename(self):
        return self.fname


class NXProcessWriter(Writer):
    """
    A class to write Nexus file with a processing result.
    """
    def __init__(self, fname, entry=None, filemode=None, overwrite=False):
        """
        Initialize a NXProcessWriter.

        Parameters
        -----------
        fname: str
            Path to the HDF5 file.
        entry: str, optional
            Entry in the HDF5 file. Default is "entry"
        """
        super().__init__(fname)
        self._set_entry(entry)
        self.overwrite = overwrite
        check_h5py_version()
        if filemode is not None:
            deprecation_warning(
                "'filemode' is deprecated and has no effect", func_name="nxprocess_init"
            )


    def _set_entry(self, entry):
        self.entry = entry or "entry"
        data_path = posix_join("/", self.entry)
        self.data_path = data_path


    def write(self, result, process_name, processing_index=0, config=None, data_name="data", is_frames_stack=True) -> str:
        """
        Write the result in the current NXProcess group.

        Parameters
        ----------
        result: numpy.ndarray
            Array containing the processing result
        process_name: str
            Name of the processing
        processing_index: int
            Index of the processing (in a pipeline)
        config: dict, optional
            Dictionary containing the configuration.
        """
        entry_path = self.data_path
        nx_process_path = "/".join([entry_path, process_name])

        if config is not None:
            config.update(
                {
                    "@NX_class": "NXcollection",
                }
            )

        class HDF5Volume(_HDF5VolumeBase):
            # TODO: not a big fan of redefining a class to set the dataset name
            # but the default value "data" is the same as in tomoscan.
            # so it should be enough for automation
            DATA_DATASET_NAME = f"results/{data_name}"

        volume = HDF5Volume(
            file_path=self.fname,
            data_path=nx_process_path,
            metadata=config,
            overwrite=self.overwrite,
        )
        assert volume.data_url is not None

        # on which case
        if isinstance(result, dict):
            pass
        elif isinstance(result, np.ndarray):
            if result.ndim == 2:
                result = result.reshape(1, result.shape[0], result.shape[1])
            volume.data = result
        elif isinstance(result, VirtualLayout):
            # TODO: add test on tomoscan to ensure this use case is handled
            volume.data = result
        else:
            raise TypeError(f"result is expected to be a dict or a numpy arrau. Not {type(result)}")

        if volume.metadata is not None:
            volume.metadata = convert_dict_values(
                volume.metadata,
                {None: "None"},
            )
        # if result is a dictionary then we only have some metadata to be saved
        if isinstance(result, dict):
            volume.save_metadata()
            results_path = posix_join(nx_process_path, "results")
        else:
            volume.save()
            results_path = posix_join(nx_process_path, "results", data_name)

        # adding nabu specific information
        nabu_process_info = {
                "@NX_class": "NXentry",
                f"{process_name}@NX_class": "NXprocess",
                f"{process_name}/program": "nabu",
                f"{process_name}/version": nabu_version,
                f"{process_name}/date": get_datetime(),
                f"{process_name}/sequence_index": np.int32(processing_index),
        }
        if isinstance(result, np.ndarray):
            nabu_process_info.update(
                {
                    f"{process_name}/results@NX_class": "NXdata",
                    f"{process_name}/results@signal": data_name,
                }
            )
            if is_frames_stack:
                nabu_process_info.update(
                    {
                        f"{process_name}/results@interpretation": "image",

                    }
                )

            # prepare the direct access plots
            nabu_process_info.update(
                {
                    f"{process_name}@default": "results",
                    "@default": f"{process_name}/results",
                }
            )
        elif isinstance(result, dict):
            nabu_process_info.update(
                {
                    "/".join([f"{process_name}/results"]): convert_dict_values(
                        result,
                        {None: "None"},
                    ),
                }
            )

        dicttonx(
            nabu_process_info,
            h5file=self.fname,
            h5path=entry_path,
            update_mode="replace",
            mode="a",
        )
        return results_path


def create_virtual_layout(files_or_pattern, h5_path, base_dir=None, axis=0):
    """
    Create a HDF5 virtual layout.

    Parameters
    ----------
    files_or_pattern: str or list
        A list of file names, or a wildcard pattern.
        If a list is provided, it will not be sorted! This will have to be
        done before calling this function.
    h5_path: str
        Path inside the HDF5 input file(s)
    base_dir: str, optional
        Base directory when using relative file names.
    axis: int, optional
        Data axis to merge. Default is 0.
    """
    prev_cwd = None
    if base_dir is not None:
        prev_cwd = getcwd()
        chdir(base_dir)
    if isinstance(files_or_pattern, str):
        files_list = glob(files_or_pattern)
        files_list.sort()
    else: # list
        files_list = files_or_pattern
    if files_list == []:
        raise ValueError("Nothing found as pattern %s" % files_or_pattern)
    virtual_sources = []
    shapes = []
    for fname in files_list:
        with HDF5File(fname, "r", swmr=True) as fid:
            shape = fid[h5_path].shape
        vsource = VirtualSource(fname, name=h5_path, shape=shape)
        virtual_sources.append(vsource)
        shapes.append(shape)
    total_shape = merged_shape(shapes, axis=axis)

    virtual_layout = VirtualLayout(
        shape=total_shape,
        dtype='f'
    )
    start_idx = 0
    for vsource, shape in zip(virtual_sources, shapes):
        n_imgs = shape[axis]
        # Perhaps there is more elegant
        if axis == 0:
            virtual_layout[start_idx:start_idx + n_imgs] = vsource
        elif axis == 1:
            virtual_layout[:, start_idx:start_idx + n_imgs, :] = vsource
        elif axis == 2:
            virtual_layout[:, :, start_idx:start_idx + n_imgs] = vsource
        else:
            raise ValueError("Only axis 0,1,2 are supported")
        #
        start_idx += n_imgs

    if base_dir is not None:
        chdir(prev_cwd)
    return virtual_layout



def merge_hdf5_files(
    files_or_pattern, h5_path, output_file, process_name,
    output_entry=None, output_filemode="a", data_name="data",
    processing_index=0, config=None, base_dir=None,
    axis=0, overwrite=False
):
    """
    Parameters
    -----------
    files_or_pattern: str or list
        A list of file names, or a wildcard pattern.
        If a list is provided, it will not be sorted! This will have to be
        done before calling this function.
    h5_path: str
        Path inside the HDF5 input file(s)
    output_file: str
        Path of the output file
    process_name: str
        Name of the process
    output_entry: str, optional
        Output HDF5 root entry (default is "/entry")
    output_filemode: str, optional
        File mode for output file. Default is "a" (append)
    processing_index: int, optional
        Processing index for the output file. Default is 0.
    config: dict, optional
        Dictionary describing the configuration needed to get the results.
    base_dir: str, optional
        Base directory when using relative file names.
    axis: int, optional
        Data axis to merge. Default is 0.
    overwrite: bool, optional
        Whether to overwrite already existing data in the final file.
        Default is False.
    """
    if base_dir is not None:
        prev_cwd = getcwd()
    virtual_layout = create_virtual_layout(files_or_pattern, h5_path, base_dir=base_dir, axis=axis)
    nx_file = NXProcessWriter(
        output_file,
        entry=output_entry, filemode=output_filemode, overwrite=overwrite
    )
    nx_file.write(
        virtual_layout,
        process_name,
        processing_index=processing_index,
        config=config,
        data_name=data_name,
        is_frames_stack=True
    )
    if base_dir is not None and prev_cwd != getcwd():
        chdir(prev_cwd)


class TIFFWriter(Writer):
    def __init__(self, fname, multiframe=False, start_index=0, filemode=None, append=False, big_tiff=None):
        """
        Tiff writer.

        Parameters
        -----------
        fname: str
            Path to the output file name
        multiframe: bool, optional
            Whether to write all data in one single file. Default is False.
        start_index: int, optional
            When writing a stack of images, each image is written in a dedicated file
            (unless multiframe is set to True).
            In this case, the output is a series of files `filename_0000.tif`,
            `filename_0001.tif`, etc. This parameter is the starting index for
            file names.
            This option is ignored when multiframe is True.
        filemode: str, optional
            DEPRECATED. Will be ignored. Please refer to 'append'
        append: bool, optional
            Whether to append data to the file rather than overwriting. Default is False.
        big_tiff: bool, optional
            Whether to write in "big tiff" format: https://www.awaresystems.be/imaging/tiff/bigtiff.html
            Default is True when multiframe is True.
            Note that default "standard" tiff cannot exceed 4 GB.

        Notes
        ------
        If multiframe is False (default), then each image will be written in a
        dedicated tiff file.
        """
        super().__init__(fname)
        self.multiframe = multiframe
        self.start_index = start_index
        self.append = append
        if big_tiff is None:
            big_tiff = multiframe
        if multiframe and not big_tiff:
            # raise error ?
            print("big_tiff was set to False while multiframe was set to True. This will probably be problematic.")
        self.big_tiff = big_tiff
        # Compat.
        self.filemode = filemode
        if filemode is not None:
            deprecation_warning("Ignored parameter 'filemode'. Please use the 'append' parameter")

    def write(self, data, *args, config=None, **kwargs):
        ext = None
        if not isinstance(data, np.ndarray):
            raise TypeError(f"data is expected to be a numpy array and not {type(data)}")
        # Single image, or multiple image in the same file
        if self.multiframe:
            volume = MultiTIFFVolume(
                self.fname,
                data=data,
                metadata={
                    "config": config,
                },
            )
            file_path = self.fname
        # Multiple image, one file per image
        else:
            if data.ndim == 2 or (data.ndim == 3 and data.shape[0] == 1):
                data = data.reshape(1, data.shape[0], data.shape[1])
                file_path = self.fname
                volume = MultiTIFFVolume(
                    self.fname,
                    data=data,
                    metadata={
                        "config": config,
                    },
                )
            else:
                file_path, ext = path.splitext(self.fname)
                # as in nabu the base name of the tiff file can be different from the folder name we
                # need to redefine it. For interoperability with the rest of the tomotools suites
                # it must highly recommended that they stay the same.
                # TODO: to somplify think we must ensure this the case by default
                # (ensure that if no output is provided then we lay back to having the output file name prefix being the folder name)
                class TIFFVolume(_TIFFVolumeBase):
                    # we are not ensure that the output directory name is the base name of the file_path
                    DEFAULT_DATA_DATA_PATH_PATTERN = path.basename(file_path) + "_{index_zfill4}" + ext

                volume = TIFFVolume(
                    path.dirname(file_path),
                    data=data,
                    metadata={
                        "config": config,
                    },
                    start_index=self.start_index,
                )

        volume.save()


class EDFWriter(Writer):
    def __init__(self, fname, start_index=0, filemode="w"):
        """
        EDF (ESRF Data Format) writer.

        Parameters
        -----------
        fname: str
            Path to the output file name
        start_index: int, optional
            When writing a stack of images, each image is written in a dedicated file
            In this case, the output is a series of files `filename_0000.tif`,
            `filename_0001.edf`, etc. This parameter is the starting index for
            file names.
        """
        super().__init__(fname)
        self.filemode = filemode
        self.start_index = start_index

    def write(self, data, *args, config=None, **kwargs):
        if not isinstance(data, np.ndarray):
            raise TypeError(f"data is expected to be a numpy array and not {type(data)}")
        header = {
            "software": "nabu",
            "data": get_datetime(),
        }
        if data.ndim == 2:
            data = data.reshape(1, data.shape[0], data.shape[1])

        volume = EDFVolume(
            path.dirname(self.fname),
            data=data,
            start_index=self.start_index,
            header=header
        )
        volume.save()


class JP2Writer(Writer):
    def __init__(
        self, fname, start_index=0, filemode="wb",
        psnr=None, cratios=None, auto_convert=True, float_clip_values=None, n_threads=None
    ):
        """
        JPEG2000 writer. This class requires the python package `glymur` and the
        library `libopenjp2`.

        Parameters
        -----------
        fname: str
            Path to the output file name
        start_index: int, optional
            When writing a stack of images, each image is written in a dedicated file
            The output is a series of files `filename_0000.tif`, `filename_0001.tif`, etc.
            This parameter is the starting index for file names.
        psnr: list of int, optional
            The PSNR (Peak Signal-to-Noise ratio) for each jpeg2000 layer.
            This defines a quality metric for lossy compression.
            The number "0" stands for lossless compression.
        cratios: list of int, optional
            Compression ratio for each jpeg2000 layer
        auto_convert: bool, optional
            Whether to automatically cast floating point data to uint16.
            Default is True.
        float_clip_values: tuple of floats, optional
            If set to a tuple of two values (min, max), then each image values will be clipped
            to these minimum and maximum values.
        n_threads: int, optional
            Number of threads to use for encoding. Default is the number of available threads.
            Needs libopenjpeg >= 2.4.0.
        """
        super().__init__(fname)
        if not(__have_jp2k__):
            raise ValueError("Need glymur python package and libopenjp2 library")
        self.n_threads = n_threads
        # self.setup_multithread_encoding(n_threads=n_threads, what_if_not_available="ignore")
        # self.filemode = filemode
        self.start_index = start_index
        self.auto_convert = auto_convert
        if psnr is not None and np.isscalar(psnr):
            psnr = [psnr]
        self.psnr = psnr
        self.cratios = cratios
        self._vmin = None
        self._vmax = None
        self.clip_float = False
        if float_clip_values is not None:
            self._float_clip_min, self._float_clip_max = float_clip_values
            self.clip_float = True

    def write(self, data, *args, **kwargs):
        if not isinstance(data, np.ndarray):
            raise TypeError(f"data is expected to be a numpy array and not {type(data)}")

        if data.ndim == 2:
            data = data.reshape(1, data.shape[0], data.shape[1])

        if data.ndim == 3 and data.shape[0] == 1:
            # TODO: add an option with of without pattern instead ? This would look more "reliable"
            class JP2KVolume(_JP2KVolumeBase):
                # we are not ensure that the output directory name is the base name of the file_path
                DEFAULT_DATA_DATA_PATH_PATTERN = self.fname
        else:
            file_path, ext = path.splitext(self.fname)
            # as in nabu the base name of the tiff file can be different from the folder name we
            # need to redefine it. For interoperability with the rest of the tomotools suites
            # it must highly recommended that they stay the same.
            # TODO: to somplify think we must ensure this the case by default
            # (ensure that if no output is provided then we lay back to having the output file name prefix being the folder name)
            class JP2KVolume(_JP2KVolumeBase):
                # we are not ensure that the output directory name is the base name of the file_path
                DEFAULT_DATA_DATA_PATH_PATTERN = path.basename(file_path) + "_{index_zfill4}" + ext

        volume = JP2KVolume(
            folder=path.dirname(self.fname),
            start_index=self.start_index,
            cratios=self.cratios,
            psnr=self.psnr,
            n_threads=self.n_threads,
        )

        if data.dtype != np.uint16 and self.auto_convert:
            if self.clip_float:
                data = np.clip(data, self._float_clip_min, self._float_clip_max)
            data = rescale_data(data, 0, 65535, data_min=self._vmin, data_max=self._vmax)
            data = data.astype(np.uint16)

        volume.data = data
        config = kwargs.get("config", None)
        if config is not None:
            volume.metadata = {"config": config}
        volume.save()


Writers = {
    "h5": NXProcessWriter,
    "hdf5": NXProcessWriter,
    "nx": NXProcessWriter,
    "nexus": NXProcessWriter,
    "tif": TIFFWriter,
    "tiff": TIFFWriter,
    "j2k": JP2Writer,
    "jp2": JP2Writer,
    "jp2k": JP2Writer,
    "edf": EDFWriter,
}
