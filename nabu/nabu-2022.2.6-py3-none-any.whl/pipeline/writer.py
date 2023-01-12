from os import path
from pathlib import Path as pathlib_Path
from posixpath import join as posixjoin
from silx.io.dictdump import dicttonx
from tomoscan.esrf import HDF5Volume, TIFFVolume, MultiTIFFVolume, EDFVolume, JP2KVolume
from ..resources.logger import LoggerOrPrint
from ..io.writer import get_datetime, LegacyNXProcessWriter as NabuNXProcessWriter
from ..io.utils import convert_dict_values
from .. import version as nabu_version
from ..resources.utils import is_hdf5_extension

#
# There are still multiple issues:
#   - When using HDF5, we still have to do self.file_prefix += str("_%05d" % self.start_index)
#     because we are writing partial files. This should be done by tomoscan but it's likely incompatible
#     with its current architecture
#   - _configure_metadata() is too long, and somehow duplicates what is done in LegacyNXProcessWriter.
#   - LegacyNXProcessWriter still has to be used for writing 1D data (histogram)
#
#  All in all, tomoscan.esrf.volume does not seem to make things simpler, at least for HDF5.
#


class WriterManager:

    """
    This class is a wrapper on top of all "writers".
    It will create the right "writer" with all the necessary options, and the histogram writer.

    The layout is the following.

    For "single-file volume" formats (HDF5, big tiff):
       bigtiff:
         output_dir/file_prefix.tiff (bigtiff)
       hdf5:
         [output_dir/file_prefix/file_prefix_{%05d}.h5]   (partial results)
         output_dir/file_prefix.h5 (master file)

    For "one file per slice" formats (tiff, jp2, edf)
      output_dir/file_prefix_%05d.{ext}


    When saving intermediate steps (eg. sinogram): HDF5 format is always used.
    So the layout is

      [output_dir/sinogram_file_prefix/sinogram_file_prefix_%05d.h5] (partial results)
      output_dir/sinogram_file_prefix.h5 (master file)
    """

    _overwrite_warned = False

    def __init__(
        self,
        output_dir,
        file_prefix,
        file_format="hdf5",
        overwrite=False,
        start_index=0,
        logger=None,
        metadata=None,
        histogram=False,
        extra_options=None,
    ):
        """
        Create a Writer from a set of parameters.

        Parameters
        ----------
        output_dir: str
            Directory where the file(s) will be written.
        file_prefix: str
            File prefix (without leading path)
        start_index: int, optional
            Index to start the files numbering (filename_0123.ext).
            Default is 0.
            Ignored for HDF5 extension.
        logger: nabu.resources.logger.Logger, optional
            Logger object
        metadata: dict, optional
            Metadata, eg. information on various processing steps. For HDF5, it will go to "configuration"
        histogram: bool, optional
            Whether to also write a histogram of data. If set to True, it will configure
            an additional "writer".
        extra_options: dict, optional
            Other advanced options to pass to Writer class.
        """
        self.overwrite = overwrite
        self.start_index = start_index
        self.logger = LoggerOrPrint(logger)
        self.histogram = histogram
        self.extra_options = extra_options or {}

        self.is_hdf5_output = is_hdf5_extension(file_format)
        self.is_bigtiff = file_format in ["tiff", "tif"] and any(
            [self.extra_options.get(opt, False) for opt in ["tiff_single_file", "use_bigtiff"]]
        )

        self.file_prefix = file_prefix
        self._set_output_dir(output_dir)
        self._set_file_name(file_format)
        self._configure_metadata(metadata)

        # tomoscan.esrf.volume arguments
        def _get_writer_kwargs_single_frame():
            return {
                "folder": self.output_dir,
                "volume_basename": self.file_prefix,
                "start_index": self.start_index,
                "overwrite": self.overwrite,
            }

        def _get_writer_kwargs_multi_frames():
            return {
                "file_path": self.fname,
                "overwrite": self.overwrite,
            }

        if self.is_hdf5_output:
            writer = HDF5Volume
            writer_kwargs = _get_writer_kwargs_multi_frames()
            writer_kwargs.update(
                {
                    "data_path": posixjoin(self._h5_entry, self._h5_process_name),
                }
            )
        elif file_format in ["tiff", "tif"]:
            if self.is_bigtiff:
                writer = MultiTIFFVolume
                writer_kwargs = _get_writer_kwargs_multi_frames()
                writer_kwargs.update({"append": self.extra_options.get("single_tiff_initialized", False)})
            else:
                writer = TIFFVolume
                writer_kwargs = _get_writer_kwargs_single_frame()
                writer_kwargs.update(
                    {
                        "folder": self.output_dir,
                        "volume_basename": self.file_prefix,
                        "overwrite": True,
                    }
                )
        elif file_format == "edf":
            writer = EDFVolume
            writer_kwargs = _get_writer_kwargs_single_frame()
        elif file_format in ["jp2k", "j2k", "jp2000", "jpeg2000"]:
            writer = JP2KVolume
            writer_kwargs = _get_writer_kwargs_single_frame()
        else:
            raise ValueError("Unsupported file format: %s" % file_format)
        self.writer = writer(**writer_kwargs)
        self._init_histogram_writer()

    def _set_output_dir(self, output_dir):
        # This class is generally used to create partial files, i.e files containing a subset of the processed volume.
        # In this case, the files containing partial results are stored in a sub-directory with the same file prefix.
        # Otherwise, everything is put in a single file (for now it's only the case for "big tiff").
        self.is_partial_file = not (self.is_bigtiff)
        if self.is_partial_file:
            output_dir = path.join(output_dir, self.file_prefix)

        self.output_dir = output_dir
        if path.exists(self.output_dir):
            if not (path.isdir(self.output_dir)):
                raise ValueError(
                    "Unable to create directory %s: already exists and is not a directory" % self.output_dir
                )
        else:
            self.logger.debug("Creating directory %s" % self.output_dir)
            pathlib_Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def _set_file_name(self, file_format):
        if self.is_hdf5_output:
            # HDF5Volume() does not have a "start_index" parameter, so we have to handle it here
            # (HDF5 files are partial files that are eventually merged into a master file,
            # so they have a _%05d suffix)
            self.file_prefix += str("_%05d" % self.start_index)
        self.file_format = file_format
        self.fname = path.join(self.output_dir, self.file_prefix + "." + file_format)
        if path.exists(self.fname):
            err = "File already exists: %s" % self.fname
            if self.overwrite:
                if not (self.__class__._overwrite_warned):
                    self.logger.warning(err + ". It will be overwritten as requested in configuration")
                    self.__class__._overwrite_warned = True
            else:
                self.logger.fatal(err)
                raise ValueError(err)

    def _configure_metadata(self, metadata):
        metadata = metadata or {}
        self.metadata = convert_dict_values(metadata, {None: "None"})
        if self.is_hdf5_output:
            self.metadata.update({"@NX_class": "NXcollection"})  # should be done by tomoscan...
            self._h5_entry = self.metadata.get("entry", "entry")
            self._h5_process_name = process_name = self.metadata.get("process_name", "reconstruction")
            # Metadata in {entry}/reconstruction. Can be written now.
            nabu_process_info = {
                "@NX_class": "NXentry",
                "@default": f"{process_name}/results",
                f"{process_name}@NX_class": "NXprocess",
                f"{process_name}/program": "nabu",
                f"{process_name}/version": nabu_version,
                f"{process_name}/date": get_datetime(),
                f"{process_name}/sequence_index": self.metadata.get("processing_index", 0),
                f"{process_name}@default": "results",
            }
            dicttonx(
                nabu_process_info,
                h5file=self.fname,
                h5path=self._h5_entry,
                update_mode="replace",
                mode="a",
            )
            # Metadata in {entry}/reconstruction/results. Will be written after data.
            self._h5_results_metadata = {
                f"{process_name}/results@NX_class": "NXdata",
                f"{process_name}/results@signal": "data",  # TODO "data_path" ?
                f"{process_name}/results@interpretation": "image",
                f"{process_name}/results/data@interpretation": "image",
            }

    def _init_histogram_writer(self):
        if not self.histogram:
            return
        hist_entry = self.metadata.get("entry", "entry")
        separate_histogram_file = not (self.is_hdf5_output)
        if separate_histogram_file:
            fmode = "w"
            hist_fname = path.join(self.output_dir, "histogram_%05d.hdf5" % self.start_index)
        else:
            fmode = "a"
            hist_fname = self.fname
        # Nabu's NXProcessWriter has to be used here, as histogram is not 3D
        self.histogram_writer = NabuNXProcessWriter(
            hist_fname,
            entry=hist_entry,
            filemode=fmode,
            overwrite=True,
        )

    def write_histogram(self, data, config=None, processing_index=1):
        if not (self.histogram):
            return
        self.histogram_writer.write(
            data,
            "histogram",
            processing_index=processing_index,
            config=config,
            is_frames_stack=False,
            direct_access=False,
        )

    def _write_metadata(self):
        self.writer.metadata = self.metadata
        self.writer.save_metadata()
        if self.is_hdf5_output:
            dicttonx(
                self._h5_results_metadata,
                h5file=self.fname,
                h5path=self._h5_entry,
                update_mode="replace",
                mode="a",
            )

    def write_data(self, data):
        self.writer.data = data
        self.writer.save()
        self._write_metadata()
