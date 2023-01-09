from . import *
from .writer import TIFFWriter as StandardTIFFWriter
from os import path
from tifffile import TiffWriter
import numpy as np


class TIFFWriter(StandardTIFFWriter):  # pylint: disable=E0102
    def __init__(
        self,
        fname,
        multiframe=False,
        start_index=0,
        heights_above_stage_mm=None,
        filemode=None,
        append=False,
        big_tiff=None,
    ):
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
        heights_above_stage_mm: None or a list of heights
            if this parameters is given, the file names will be indexed with the height
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
        super().__init__(
            fname, multiframe=multiframe, start_index=start_index, filemode=filemode, append=append, big_tiff=big_tiff
        )
        self.heights_above_stage_mm = heights_above_stage_mm

    def _write_tiff(self, data, config=None, filename=None):
        # TODO metadata
        filename = filename or self.fname
        with TiffWriter(filename, bigtiff=self.big_tiff, append=self.append) as tif:
            tif.write(data)

    def write(self, data, *args, config=None, **kwargs):
        # Single image, or multiple image in the same file
        if self.multiframe:
            self._write_tiff(data, config=config)
        # Multiple image, one file per image
        else:
            if len(data.shape) == 2:
                data = np.array([data])
            dirname, rel_filename = path.split(self.fname)
            prefix, ext = path.splitext(rel_filename)
            for i in range(data.shape[0]):

                if self.heights_above_stage_mm is None:
                    curr_rel_filename = prefix + str("_%04d" % (self.start_index + i)) + ext
                else:
                    value_mm = self.heights_above_stage_mm[i]
                    if value_mm < 0:
                        sign = "-"
                        value_mm = -value_mm
                    else:
                        sign = ""

                    part_mm = int(value_mm)
                    rest_um = (value_mm - part_mm) * 1000
                    part_um = int(rest_um)
                    rest_nm = (rest_um - part_um) * 1000
                    part_nm = int(rest_nm)

                    curr_rel_filename = prefix + "_{}{:04d}p{:03d}{:03d}".format(sign, part_mm, part_um, part_nm) + ext

                fname = path.join(dirname, curr_rel_filename)

                self._write_tiff(data[i], filename=fname, config=None)

    def get_filename(self):
        if self.multiframe:
            return self.fname
        else:
            return path.dirname(self.fname)
