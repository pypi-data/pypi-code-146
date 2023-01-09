""" This module is  meant to contain classes which are in the process of being superseed by new classes depending on recent packages 
    with fast development cycles in order to be able to  fall-back in two cases : 
             -- the new packages, or one of their parts,  break from one version to another.
             -- For parts of Nabu which need some extra time to adapt.    
"""
from ..resources.logger import LoggerOrPrint
from ..utils import check_supported
from ..io.writer import Writers, LegacyNXProcessWriter
from ..resources.utils import is_hdf5_extension
from os import path, mkdir
from .params import files_formats


class WriterConfigurator:
    """No dependency on  tomoscan for this class. The new class would be WriterManager which depend on tomoscan."""

    _overwrite_warned = False

    def __init__(
        self,
        output_dir,
        file_prefix,
        file_format="hdf5",
        overwrite=False,
        start_index=None,
        logger=None,
        nx_info=None,
        write_histogram=False,
        histogram_entry="entry",
        writer_options=None,
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
        nx_info: dict, optional
            Dictionary containing the nexus information.
        write_histogram: bool, optional
            Whether to also write a histogram of data. If set to True, it will configure
            an additional "writer".
        histogram_entry: str, optional
            Name of the HDF5 entry for the output histogram file, if write_histogram is True.
            Ignored if the output format is already HDF5 : in this case, nx_info["entry"] is taken.
        writer_options: dict, optional
            Other advanced options to pass to Writer class.
        """
        self.logger = LoggerOrPrint(logger)
        self.start_index = start_index
        self.write_histogram = write_histogram
        self.overwrite = overwrite
        writer_options = writer_options or {}
        self.extra_options = extra_options or {}

        check_supported(file_format, list(Writers.keys()), "output file format")

        self._set_output_dir(output_dir)
        self._set_file_name(file_prefix, file_format)

        # Init Writer
        writer_cls = Writers[file_format]
        writer_args = [self.fname]
        writer_kwargs = self._get_initial_writer_kwarg()
        self._writer_exec_args = []
        self._writer_exec_kwargs = {}
        self._is_hdf5_output = is_hdf5_extension(file_format)

        if self._is_hdf5_output:
            writer_kwargs["entry"] = nx_info["entry"]
            writer_kwargs["filemode"] = "a"
            writer_kwargs["overwrite"] = overwrite
            self._writer_exec_args.append(nx_info["process_name"])
            self._writer_exec_kwargs["processing_index"] = nx_info["processing_index"]
            self._writer_exec_kwargs["config"] = nx_info["config"]
        else:
            writer_kwargs["start_index"] = self.start_index
            if writer_options.get("tiff_single_file", False) and "tif" in file_format:
                do_append = writer_options.get("single_tiff_initialized", False)
                writer_kwargs.update({"multiframe": True, "append": do_append})

        if files_formats.get(file_format, None) == "jp2":
            cratios = self.extra_options.get("jpeg2000_compression_ratio", None)
            if cratios is not None:
                cratios = [cratios]
            writer_kwargs["cratios"] = cratios
            writer_kwargs["float_clip_values"] = self.extra_options.get("float_clip_values", None)
        self.writer = writer_cls(*writer_args, **writer_kwargs)

        if self.write_histogram and not (self._is_hdf5_output):
            self._init_separate_histogram_writer(histogram_entry)

    def _get_initial_writer_kwarg(self):
        return {}

    def _set_output_dir(self, output_dir):
        self.output_dir = output_dir
        if path.exists(self.output_dir):
            if not (path.isdir(self.output_dir)):
                raise ValueError(
                    "Unable to create directory %s: already exists and is not a directory" % self.output_dir
                )
        else:
            self.logger.debug("Creating directory %s" % self.output_dir)
            mkdir(self.output_dir)

    def _set_file_name(self, file_prefix, file_format):
        self.file_prefix = file_prefix
        self.file_format = file_format
        self.fname = path.join(self.output_dir, file_prefix + "." + file_format)
        if path.exists(self.fname):
            err = "File already exists: %s" % self.fname
            if self.overwrite:
                if not (WriterConfigurator._overwrite_warned):
                    self.logger.warning(err + ". It will be overwritten as requested in configuration")
                    WriterConfigurator._overwrite_warned = True
            else:
                self.logger.fatal(err)
                raise ValueError(err)

    def _init_separate_histogram_writer(self, hist_entry):
        hist_fname = path.join(self.output_dir, "histogram_%04d.hdf5" % self.start_index)
        self.histogram_writer = LegacyNXProcessWriter(
            hist_fname,
            entry=hist_entry,
            filemode="w",
            overwrite=True,
        )

    def get_histogram_writer(self):
        if not (self.write_histogram):
            return None
        if self._is_hdf5_output:
            return self.writer
        else:
            return self.histogram_writer

    def write_data(self, data):
        self.writer.write(data, *self._writer_exec_args, **self._writer_exec_kwargs)
