from glob import glob
from os import path, getcwd, chdir
from posixpath import join as posix_join
from datetime import datetime
import numpy as np
from h5py import VirtualSource, VirtualLayout
from silx.io.dictdump import dicttoh5, dicttonx
from silx.io.url import DataUrl
from tomoscan.io import HDF5File
from tomoscan.esrf import EDFVolume, HDF5Volume, TIFFVolume, MultiTIFFVolume, JP2KVolume
from tomoscan.esrf.volume.jp2kvolume import has_glymur as __have_jp2k__
from tomoscan.esrf import RawVolume
from .. import version as nabu_version
from ..utils import merged_shape, deprecation_warning
from ..misc.utils import rescale_data
from .utils import check_h5py_version, convert_dict_values


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

    def __init__(self, fname, entry=None, filemode="a", overwrite=False):
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
        self._filemode = filemode
        # TODO: notify file mode is deprecated
        self.overwrite = overwrite
        check_h5py_version()

    def _set_entry(self, entry):
        self.entry = entry or "entry"
        data_path = posix_join("/", self.entry)
        self.data_path = data_path

    def _write_npadday(self, result, volume, nx_info):
        if result.ndim == 2:
            result = result.reshape(1, result.shape[0], result.shape[1])
        volume.data = result

        self._update_volume_metadata(volume)

        volume.save()
        results_path = posix_join(nx_info["nx_process_path"], "results", nx_info["data_name"])
        process_name = nx_info["process_name"]
        process_info = nx_info["process_info"]
        process_info.update({
            f"{process_name}/results@NX_class": "NXdata",
            f"{process_name}/results@signal": nx_info["data_name"],
        })
        if nx_info.get("is_frames_stack", True):
            process_info.update({f"{process_name}/results@interpretation": "image"})
        # prepare the direct access plots
        process_info.update({
            f"{process_name}@default": "results",
            "@default": f"{process_name}/results",
        })
        return results_path

    def _write_dict(self, result, volume, nx_info):
        self._update_volume_metadata(volume)
        volume.save_metadata() # if result is a dictionary then we only have some metadata to be saved
        results_path = posix_join(nx_info["nx_process_path"], "results")
        proc_result_key = posix_join(nx_info["process_name"], "results")
        proc_result = convert_dict_values(result, {None: "None"})
        process_info = nx_info["process_info"]
        process_info.update({proc_result_key: proc_result})
        return results_path

    def _write_virtual_layout(self, result, volume, nx_info):
        # TODO: add test on tomoscan to ensure this use case is handled
        volume.data = result
        self._update_volume_metadata(volume)
        volume.save()
        results_path = posix_join(nx_info["nx_process_path"], "results", nx_info["data_name"])
        return results_path

    @staticmethod
    def _update_volume_metadata(volume):
        if volume.metadata is not None:
            volume.metadata = convert_dict_values(
                volume.metadata,
                {None: "None"},
            )

    def write(
        self, result, process_name, processing_index=0, config=None, data_name="data", is_frames_stack=True
    ) -> str:
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
            config.update({"@NX_class": "NXcollection"})

        nabu_process_info = {
            "@NX_class": "NXentry",
            f"{process_name}@NX_class": "NXprocess",
            f"{process_name}/program": "nabu",
            f"{process_name}/version": nabu_version,
            f"{process_name}/date": get_datetime(),
            f"{process_name}/sequence_index": np.int32(processing_index),
        }

        # Create HDF5Volume object with initial information
        volume = HDF5Volume(
            data_url=DataUrl(
                file_path=self.fname,
                data_path=f"{nx_process_path}/results/{data_name}",
                scheme="silx",
            ),
            metadata_url=DataUrl(
                file_path=self.fname,
                data_path=f"{nx_process_path}/configuration",
            ),
            metadata=config,
            overwrite=self.overwrite,
        )
        if isinstance(result, dict):
            write_method = self._write_dict
        elif isinstance(result, np.ndarray):
            write_method = self._write_npadday
        elif isinstance(result, VirtualLayout):
            write_method = self._write_virtual_layout
        else:
            raise TypeError(f"'result' must be a dict, numpy array or h5py.VirtualLayout, not {type(result)}")
        nx_info = {
            "process_name": process_name,
            "nx_process_path": nx_process_path,
            "process_info": nabu_process_info,
            "data_name": data_name,
            "is_frames_stack": is_frames_stack,
        }
        results_path = write_method(result, volume, nx_info)

        dicttonx(
            nabu_process_info,
            h5file=self.fname,
            h5path=entry_path,
            update_mode="replace",
            mode="a",
        )
        return results_path


########################################################################################
## Legacy code for NXProcessWriter - to be removed once the new code is battle-tested ##
########################################################################################


def h5_write_object(h5group, key, value, overwrite=False, default_val=None):
    existing_val = h5group.get(key, default_val)
    if existing_val is not default_val:
        if not overwrite:
            raise OSError("Unable to create link (name already exists): %s" % h5group.name)
        else:
            h5group.pop(key)
    h5group[key] = value


class LegacyNXProcessWriter(Writer):
    """
    A class to write Nexus file with a processing result.
    """

    def __init__(self, fname, entry=None, filemode="a", overwrite=False):
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
        self._filemode = filemode
        self.overwrite = overwrite
        check_h5py_version()

    def _set_entry(self, entry):
        self.entry = entry or "entry"
        data_path = posix_join("/", self.entry)
        self.data_path = data_path

    def write(self, result, process_name, processing_index=0, config=None, data_name="data", is_frames_stack=True):
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
        swmr = self._filemode == "r"
        with HDF5File(self.fname, self._filemode, swmr=swmr) as fid:
            nx_entry = fid.require_group(self.data_path)
            if "NX_class" not in nx_entry.attrs:
                nx_entry.attrs["NX_class"] = "NXentry"

            nx_process = nx_entry.require_group(process_name)
            nx_process.attrs["NX_class"] = "NXprocess"

            metadata = {
                "program": "nabu",
                "version": nabu_version,
                "date": get_datetime(),
                "sequence_index": np.int32(processing_index),
            }
            for key, val in metadata.items():
                h5_write_object(nx_process, key, val, overwrite=self.overwrite)

            if config is not None:
                export_dict_to_h5(
                    config, self.fname, posix_join(nx_process.name, "configuration"), overwrite_data=True, mode="a"
                )
                nx_process["configuration"].attrs["NX_class"] = "NXcollection"
            if isinstance(result, dict):
                results_path = posix_join(nx_process.name, "results")
                export_dict_to_h5(result, self.fname, results_path, overwrite_data=self.overwrite, mode="a")
            else:
                nx_data = nx_process.require_group("results")
                results_path = nx_data.name
                nx_data.attrs["NX_class"] = "NXdata"
                nx_data.attrs["signal"] = data_name

                results_data_path = posix_join(results_path, data_name)
                if self.overwrite and results_data_path in fid:
                    del fid[results_data_path]

                if isinstance(result, VirtualLayout):
                    nx_data.create_virtual_dataset(data_name, result)
                else:  # assuming array-like
                    nx_data[data_name] = result
                if is_frames_stack:
                    nx_data[data_name].attrs["interpretation"] = "image"
                nx_data.attrs["signal"] = data_name

            # prepare the direct access plots
            nx_process.attrs["default"] = "results"
            if "default" not in nx_entry.attrs:
                nx_entry.attrs["default"] = posix_join(nx_process.name, "results")
            # Return the internal path to "results"
            return results_path


########################################################################################
########################################################################################
########################################################################################


def export_dict_to_h5(dic, h5file, h5path, overwrite_data=True, mode="a"):
    """
    Wrapper on top of silx.io.dictdump.dicttoh5 replacing None with "None"

    Parameters
    -----------
    dic: dict
        Dictionary containing the options
    h5file: str
        File name
    h5path: str
        Path in the HDF5 file
    overwrite_data: bool, optional
        Whether to overwrite data when writing HDF5. Default is True
    mode: str, optional
        File mode. Default is "a" (append).
    """
    modified_dic = convert_dict_values(
        dic,
        {None: "None"},
    )
    update_mode = {True: "modify", False: "add"}[bool(overwrite_data)]
    return dicttoh5(modified_dic, h5file=h5file, h5path=h5path, update_mode=update_mode, mode=mode)


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
    else:  # list
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

    virtual_layout = VirtualLayout(shape=total_shape, dtype="f")
    start_idx = 0
    for vsource, shape in zip(virtual_sources, shapes):
        n_imgs = shape[axis]
        # Perhaps there is more elegant
        if axis == 0:
            virtual_layout[start_idx : start_idx + n_imgs] = vsource
        elif axis == 1:
            virtual_layout[:, start_idx : start_idx + n_imgs, :] = vsource
        elif axis == 2:
            virtual_layout[:, :, start_idx : start_idx + n_imgs] = vsource
        else:
            raise ValueError("Only axis 0,1,2 are supported")
        #
        start_idx += n_imgs

    if base_dir is not None:
        chdir(prev_cwd)
    return virtual_layout


def merge_hdf5_files(
    files_or_pattern,
    h5_path,
    output_file,
    process_name,
    output_entry=None,
    output_filemode="a",
    data_name="data",
    processing_index=0,
    config=None,
    base_dir=None,
    axis=0,
    overwrite=False,
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
    nx_file = LegacyNXProcessWriter(output_file, entry=output_entry, filemode=output_filemode, overwrite=overwrite)
    nx_file.write(
        virtual_layout,
        process_name,
        processing_index=processing_index,
        config=config,
        data_name=data_name,
        is_frames_stack=True,
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
                append=self.append,
            )
            file_path = self.fname
        # Multiple image, one file per image
        else:
            if data.ndim == 2:
                data = data.reshape(1, data.shape[0], data.shape[1])
            file_path, ext = path.splitext(self.fname)
            volume = TIFFVolume(
                path.dirname(file_path),
                volume_basename=path.basename(file_path),
                data=data,
                metadata={
                    "config": config,
                },
                start_index=self.start_index,
                data_extension=ext.lstrip("."),
                overwrite=True,
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

        volume = EDFVolume(path.dirname(self.fname), data=data, start_index=self.start_index, header=header)
        volume.save()


class JP2Writer(Writer):
    def __init__(
        self,
        fname,
        start_index=0,
        filemode="wb",
        psnr=None,
        cratios=None,
        auto_convert=True,
        float_clip_values=None,
        n_threads=None,
        overwrite=False,
        single_file=True,
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
        if not (__have_jp2k__):
            raise ValueError("Need glymur python package and libopenjp2 library")
        self.n_threads = n_threads
        # self.setup_multithread_encoding(n_threads=n_threads, what_if_not_available="ignore")
        self.filemode = filemode
        self.start_index = start_index
        self.single_file = single_file
        self.auto_convert = auto_convert
        if psnr is not None and np.isscalar(psnr):
            psnr = [psnr]
        self.psnr = psnr
        self.cratios = cratios
        self._vmin = None
        self._vmax = None
        self.overwrite = overwrite
        self.clip_float = False
        if float_clip_values is not None:
            self._float_clip_min, self._float_clip_max = float_clip_values
            self.clip_float = True

    def write(self, data, *args, **kwargs):
        if not isinstance(data, np.ndarray):
            raise TypeError(f"data is expected to be a numpy array and not {type(data)}")

        if data.ndim == 2:
            data = data.reshape(1, data.shape[0], data.shape[1])

        if self.single_file and data.ndim == 3 and data.shape[0] == 1:
            # case we will have a single file as output
            data_url = DataUrl(
                file_path=path.dirname(self.fname),
                data_path=self.fname,
                scheme=JP2KVolume.DEFAULT_DATA_SCHEME,
            )
            metadata_url = DataUrl(
                file_path=path.dirname(self.fname),
                data_path=f"{path.dirname(self.fname)}/{path.basename(self.fname)}_info.txt",
                scheme=JP2KVolume.DEFAULT_METADATA_SCHEME,
            )
            volume_basename = None
            folder = None
            extension = None
        else:
            # case we need to save it as set of file
            file_path, ext = path.splitext(self.fname)
            data_url = None
            metadata_url = None
            volume_basename = path.basename(file_path)
            folder = path.dirname(self.fname)
            extension = ext.lstrip(".")

        volume = JP2KVolume(
            folder=folder,
            start_index=self.start_index,
            cratios=self.cratios,
            psnr=self.psnr,
            n_threads=self.n_threads,
            volume_basename=volume_basename,
            data_url=data_url,
            metadata_url=metadata_url,
            data_extension=extension,
            overwrite=self.overwrite,
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



class HSTVolWriter(Writer):
    """
    A writer to mimic PyHST2 ".vol" files
    """

    def __init__(self, fname, append=False, **kwargs):
        super().__init__(fname)
        self.append = append
        self._vol_writer = RawVolume(fname, overwrite=True, append=append)

    @staticmethod
    def generate_metadata(data, **kwargs):
        n_z, n_y, n_x = data.shape
        metadata = {
            "NUM_X": n_x,
            "NUM_Y": n_y,
            "NUM_Z": n_z,
            "voxelSize": kwargs.get("voxelSize", 40.0),
            "BYTEORDER": "LOWBYTEFIRST",
            "ValMin": kwargs.get("ValMin", 0.0),
            "ValMax": kwargs.get("ValMin", 1.0),
            "s1": 0.0,
            "s2": 0.0,
            "S1": 0.0,
            "S2": 0.0,
        }
        return metadata

    @staticmethod
    def sanitize_metadata(metadata):
        # To be fixed in RawVolume
        for what in ["NUM_X", "NUM_Y", "NUM_Z"]:
            metadata[what] = int(metadata[what])
        for what in ["voxelSize", "ValMin", "ValMax", "s1", "s2", "S1", "S2"]:
            metadata[what] = float(metadata[what])


    def write(self, data, *args, config=None, **kwargs):
        existing_metadata = self._vol_writer.load_metadata()
        new_metadata = self.generate_metadata(data)
        if len(existing_metadata) == 0 or not(self.append):
            # first write or append==False
            metadata = new_metadata
        else:
            # append write ; update metadata
            metadata = existing_metadata.copy()
            self.sanitize_metadata(metadata)
            metadata["NUM_Z"] += new_metadata["NUM_Z"]
        self._vol_writer.data = data
        self._vol_writer.metadata = metadata
        self._vol_writer.save()
        # Also save .xml
        self._vol_writer.save_metadata(
            url=DataUrl(
                scheme="lxml",
                file_path=self._vol_writer.metadata_url.file_path().replace(".info", ".xml"),
            )
        )


class NPYWriter(Writer):
    def write(self, result, *args, **kwargs):
        np.save(self.fname, result)


class NPZWriter(Writer):
    def write(self, result, *args, **kwargs):
        save_args = {"result": result}
        config = kwargs.get("config", None)
        if config is not None:
            save_args["configuration"] = config
        np.savez(self.fname, **save_args)


Writers = {
    "h5": LegacyNXProcessWriter,
    "hdf5": LegacyNXProcessWriter,
    "nx": LegacyNXProcessWriter,
    "nexus": LegacyNXProcessWriter,
    "npy": NPYWriter,
    "npz": NPZWriter,
    "tif": TIFFWriter,
    "tiff": TIFFWriter,
    "j2k": JP2Writer,
    "jp2": JP2Writer,
    "jp2k": JP2Writer,
    "edf": EDFWriter,
    "vol": HSTVolWriter,
}
