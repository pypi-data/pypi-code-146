"""Module containing DICOMSource class.

DICOMSource class handles loading of DICOM data.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import PIL
import numpy as np
import pandas as pd
import pydicom

from bitfount.data.datasources.base_source import FileSystemIterableSource
from bitfount.data.datasources.utils import OphthalmologyDataSourceArgs
from bitfount.data.exceptions import DataSourceError
from bitfount.utils import delegates

logger = logging.getLogger(__name__)


@delegates()
class DICOMSource(FileSystemIterableSource):
    """Data source for loading DICOM files.

    Args:
        path: The path to the directory containing the DICOM files.
        file_extension: The file extension of the DICOM files. Defaults to '.dcm'.
        ophthalmology_args: Arguments for ophthalmology data. If provided, the
            `oct_string` argument will be used to filter the DICOM files to only
            include those with the string in the filename. The `slo_string` argument
            meanwhile will be used to find SLO images with the same file name as the
            OCT images except with the `slo_string` replacing the `oct_string` in the
            filename. Defaults to None.
        **kwargs: Keyword arguments passed to the parent base classes.
    """

    def __init__(
        self,
        path: Union[os.PathLike, str],
        file_extension: Optional[str] = ".dcm",
        ophthalmology_args: Optional[OphthalmologyDataSourceArgs] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(path=path, file_extension=file_extension, **kwargs)
        self.ophthalmology_args = ophthalmology_args

        if not self.file_names:
            logger.warning(
                "Didn't detect any DICOM files in the provided directory that matched "
                "the provided criteria."
            )

    @property
    def file_names(self) -> List[str]:
        """Returns a list of file names in the directory."""
        file_names = super().file_names
        if self.ophthalmology_args:
            file_names = [
                i for i in file_names if self.ophthalmology_args.oct_string in i
            ]

        return file_names

    def _get_data(
        self, file_names: Optional[List[str]] = None, **kwargs: Any
    ) -> pd.DataFrame:
        """Loads and returns the DICOM dataframe.

        Args:
            file_names: The list of file names to load.

        Returns:
            The DICOM dataframe.
        """
        dicom_list: List[Dict[Union[int, str], Any]] = []
        images_2d, images_3d = False, False
        if file_names:
            full_data = False
        else:
            file_names = self.file_names
            full_data = True

        for filename in file_names:
            try:
                save_prefix = self._recreate_file_structure(filename, exist_ok=False)
            except FileExistsError:
                # If the directory already exists, this means it has already been parsed
                # and is already part of `self.data` which we will append to our
                # dataframe at the end of this method if `full_data` is True. It doesn't
                # matter if the contents of the directory actually exist or not here.
                if self._data_is_loaded and full_data:
                    continue

                # If the data has not been loaded but the file already exists, it must
                # have been created by a previous run. We will therefore load the data
                # from the file and append it to the dataframe.
                else:
                    save_prefix = self._recreate_file_structure(filename, exist_ok=True)

            ds = pydicom.dcmread(filename, force=True)
            data: Dict[Union[int, str], Any] = {}
            for elem in ds:
                if elem.name not in self._ignore_cols:
                    if elem.VR == "SQ":
                        # A DICOM file has different Value Representation (VR).
                        # Unfortunately we cannot support sequence data (SQ)
                        # for using it in dataframes, so we ignore those columns.
                        self._ignore_cols.append(elem.name)
                        logger.info(
                            f"Cannot process sequence data, ignoring column {elem.name}"
                        )
                    elif hasattr(elem, "VM") and elem.VM > 1:
                        # The Value Multiplicity of a Data Element specifies the number
                        # of Values that can be encoded in the Value Field of that Data
                        # Element. The VM of each Data Element is specified explicitly
                        # in PS3.6. If the number of Values that may be encoded in a
                        # Data Element is variable, it shall be represented by two
                        # numbers separated by a dash; e.g., "1-10" means that there
                        # may be 1 to 10 Values in the Data Element. Similar to the
                        # SQ case, dataframes do not support sequence data so we only
                        # take the first element.
                        data[elem.name] = elem[0]
                    elif elem.name != "Pixel Data":
                        # for all non-image fields, we take the value of the column
                        data[elem.name] = elem.value
                    elif elem.name == "Pixel Data":
                        # If there is an image, we get the pixel_array instead.
                        arr = ds.pixel_array
                        if int(ds.NumberOfFrames) > 1 and images_2d is False:
                            # If there is more than one frame, we load them separately
                            images_3d = True
                            for iter in range(int(ds.NumberOfFrames)):
                                # For each image in the 3d DICOM image,
                                # save each frame separately.
                                save_path = (
                                    save_prefix
                                    / f"{ds.PatientID}-{ds.StudyDate}-{ds.StudyTime}-{iter}.png"  # noqa: B950
                                )
                                if not save_path.exists():
                                    # But don't save images again if they have
                                    # already been saved once.
                                    self._save_PIL_image_to_path(
                                        ds, arr[iter], save_path
                                    )
                                # For each image we assign a column according to the
                                # frames order and write in the df the path where
                                # the image is saved.
                                data[f"Pixel Data {iter}"] = save_path
                        elif int(ds.NumberOfFrames) > 1 and images_2d is True:
                            # If we already processed at least one 2d image,
                            # we cannot process 3d images, so we raise an error.
                            raise (
                                DataSourceError(
                                    "The data provided has a mix of both 3d and 2d "
                                    "images. Please make sure that the files provided"
                                    " contains only 3d or only 2d images."
                                )
                            )
                        else:
                            if images_3d is True:
                                # If we already processed at least one 3d image,
                                # we cannot process 2d images, so we raise an error.
                                raise (
                                    DataSourceError(
                                        "The data provided has a mix of both 3d and 2d "
                                        "images. Please make sure that the files "
                                        "provided contains only 3d or only 2d images."
                                    )
                                )
                            images_2d = True
                            save_path = (
                                save_prefix
                                / f"{ds.PatientID}-{ds.StudyDate}-{ds.StudyTime}.png"
                            )
                            if not save_path.exists():
                                self._save_PIL_image_to_path(ds, arr, save_path)
                            data["Pixel Data"] = save_path
            if self.ophthalmology_args:
                # Ophthalmology specific, if include_slo is true we can
                # process SLO images as well.
                slo_filename = filename.replace(
                    self.ophthalmology_args.oct_string,
                    self.ophthalmology_args.slo_string,
                )
                # Check that the string has been replaced
                # and that the filename exists
                if os.path.exists(slo_filename) and filename != slo_filename:
                    slo_ds = pydicom.dcmread(slo_filename, force=True)
                    slo_path = save_prefix / (
                        f"{ds.PatientID}-{ds.StudyDate}-{ds.StudyTime}-"
                        + f"{self.ophthalmology_args.slo_string}.png"
                    )
                    if not slo_path.exists():
                        self._save_PIL_image_to_path(
                            slo_ds, slo_ds.pixel_array, slo_path
                        )
                    data["SLO Image Data"] = str(slo_path)
                else:
                    logger.warning(
                        "`include_slo` was set to True, but no corresponding "
                        "SLO file found. Make sure that your filename is the "
                        "same as the OCT file and SLO_IR replaces `OCT` for "
                        "the slo file."
                    )
            dicom_list.append(data)

        df = pd.DataFrame.from_records(dicom_list)
        if self._data_is_loaded and full_data:
            # If the data is already loaded and we want all the data, we append the new
            # data to the existing dataframe.
            return pd.concat([self.data, df], axis=0, ignore_index=True)

        return df

    @staticmethod
    def _get_LUT_value(data: np.ndarray, window: int, level: int) -> np.ndarray:
        """Apply the RGB Look-Up Table for the given data and window/level value."""
        return np.piecewise(
            data,
            [
                data <= (level - 0.5 - (window - 1) / 2),
                data > (level - 0.5 + (window - 1) / 2),
            ],
            [
                0,
                255,
                lambda data: ((data - (level - 0.5)) / (window - 1) + 0.5) * (255 - 0),
            ],
        )

    @staticmethod
    def _save_PIL_image_to_path(
        dataset: pydicom.FileDataset,
        pixel_array: np.ndarray,
        filename: Union[Path, str],
    ) -> None:
        """Get Image object from Python Imaging Library(PIL) and save it.

        Args:
            dataset: The DICOM data.
            pixel_array: The pixel array from the dataset.
            filename: The filepath where to save the image.
        """
        # We can only apply LUT if these window info exists
        if ("WindowWidth" not in dataset) or ("WindowCenter" not in dataset):
            bits = dataset.BitsAllocated
            samples = dataset.SamplesPerPixel
            # Different bits and samples configurations have different
            # modes for loading the images.
            if bits == 8 and samples == 1:
                mode = "L"
            elif bits == 8 and samples == 3:
                mode = "RGB"
            elif bits == 16:
                mode = "I;16"
            else:
                raise TypeError(
                    f"Don't know PIL mode for {bits} BitsAllocated "
                    f"and {samples} SamplesPerPixel"
                )

            size = (dataset.Columns, dataset.Rows)
            # Recommended to specify all details
            # by http://www.pythonware.com/library/pil/handbook/image.htm
            im = PIL.Image.frombuffer(mode, size, pixel_array, "raw", mode, 0, 1)
            im.save(filename, "PNG")
        else:
            ew = dataset.WindowWidth
            ec = dataset.WindowCenter
            image = DICOMSource._get_LUT_value(pixel_array, int(ew), int(ec))
            # Convert mode to L since LUT has only 256 values:
            #   http://www.pythonware.com/library/pil/handbook/image.htm
            im = PIL.Image.fromarray(image).convert("L")
            im.save(filename, "PNG")
