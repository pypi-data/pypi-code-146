from ...utils import *
from ...io.writer import Writers, NXProcessWriter
from ...io.tiffwriter_zmm import TIFFWriter
from ...resources.logger import LoggerOrPrint
from ...resources.utils import is_hdf5_extension
from os import path, mkdir
from ...utils import check_supported
from ..fallback_utils import WriterConfigurator
from ..params import files_formats

Writers["tif"] = TIFFWriter
Writers["tiff"] = TIFFWriter


class WriterConfiguratorHelical(WriterConfigurator):
    def _get_initial_writer_kwarg(self):
        if self.file_format in ["tif", "tiff"]:
            return {"heights_above_stage_mm": self.heights_above_stage_mm}
        else:
            return {}

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
        heights_above_stage_mm=None,
    ):
        self.heights_above_stage_mm = heights_above_stage_mm
        self.file_format = file_format
        super().__init__(
            output_dir,
            file_prefix,
            file_format=file_format,
            overwrite=overwrite,
            start_index=start_index,
            logger=logger,
            nx_info=nx_info,
            write_histogram=write_histogram,
            histogram_entry=histogram_entry,
            writer_options=writer_options,
            extra_options=extra_options,
        )
