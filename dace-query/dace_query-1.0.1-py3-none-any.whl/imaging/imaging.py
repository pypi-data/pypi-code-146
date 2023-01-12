from __future__ import annotations

import json
import logging
from typing import Union, Optional

from astropy.coordinates import SkyCoord, Angle
from astropy.table import Table
from numpy import ndarray
from pandas import DataFrame

from dace_query import Dace, DaceClass

IMAGING_DEFAULT_LIMIT = 100000


class ImagingClass:
    """
    The imaging class.
    Use to retrieve data from the imaging module.

    **An imaging instance is already provided, to use it :**

    >>> from dace_query.imaging import Imaging

    """

    __ACCEPTED_FILE_TYPES = ['ns', 'snr', 'dl', 'hc', 'pa', 'master', 'all']
    __IMAGING_FILENAMES = {'NS': 'ns.fits',
                           'SNR': 'snr.fits',
                           'DL': 'dl.rdb',
                           'PA': 'PA.rdb',
                           'MASTER': 'master.fits',
                           'HC': 'hc.fits'}

    def __init__(self, dace_instance: Optional[DaceClass] = None):
        """
        Create a configurable imaging obejct which uses a specified dace instance.

        :param dace_instance: A dace object
        :type dace_instance: Optional[DaceClass]

        >>> from dace_query.imaging import ImagingClass
        >>> imaging_class = ImagingClass()
        """
        self.__OBS_API = 'obs-webapp'

        self.log = logging.getLogger("Imaging")
        self.log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        if dace_instance is None:
            self.dace = Dace
        elif isinstance(dace_instance, DaceClass):
            self.dace = dace_instance
        else:
            raise Exception("Dace instance is not valid")

    def query_database(self,
                       limit: Optional[int] = IMAGING_DEFAULT_LIMIT,
                       filters: Optional[dict] = None,
                       sort: Optional[dict] = None,
                       output_format: Optional[str] = None) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Query the imaging database to retrieve data in the chosen format.

        :param limit: Maximum number of rows to return
        :type limit: Optional[int]
        :param filters: Filters to apply to the query
        :type filters: Optional[dict]
        :param sort: Sort order to apply to the query
        :type sort: Optional[dict]
        :param output_format: Type of data returns
        :type output_format: Optional[str]
        :return: The desired data in the chosen output format
        :rtype: dict[str, ndarray] or DataFrame or Table or dict

        >>> from dace_query.imaging import Imaging
        >>> values = Imaging.query_database()

        """

        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__OBS_API,
                endpoint='observation/search/imaging',
                params={
                    'limit': str(limit),
                    'filters': json.dumps(filters),
                    'sort': json.dumps(sort)}
            ), output_format=output_format)

    def query_region(self,
                     sky_coord: SkyCoord,
                     angle: Angle,
                     filters: Optional[dict] = None,
                     output_format: Optional[str] = None) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Query a region, based on SkyCoord and Angle objects, in the imaging database and retrieve data in the chosen
        format.

        Filters and sorting order can be applied to the query via named arguments (see :doc:`query_options`).

        All available formats are defined in this section (see :doc:`output_format`).

        :param sky_coord: Sky coordinates object from the astropy module
        :type sky_coord: SkyCoord
        :param angle: Angle object from the astropy module
        :type angle: Angle
        :param filters: Filters to apply to the query
        :type filters: Optional[dict]
        :param output_format: Type of data returns
        :type output_format: Optional[str]
        :return: The desired data in the chosen output format
        :rtype: dict[str, ndarray] or DataFrame or Table or dict

        >>> from dace_query.imaging import Imaging
        >>> from astropy.coordinates import SkyCoord, Angle
        >>> from astropy import units as u
        >>> sky_coord, angle = SkyCoord("02:12:20.6774","-46:48:58.9566", unit=(u.hourangle, u.deg)), Angle('0.045d')
        >>> values = Imaging.query_region(sky_coord=sky_coord, angle=angle)
        """

        coordinate_filter_dict = self.dace.transform_coordinates_to_dict(sky_coord, angle)
        filters_with_coordinates = {}
        if filters is not None:
            filters_with_coordinates.update(filters)
        filters_with_coordinates.update(coordinate_filter_dict)
        return self.query_database(filters=filters_with_coordinates, output_format=output_format)

    def download(self,
                 file_type: str,
                 filters: Optional[dict] = None,
                 output_directory: Optional[str] = None,
                 output_filename: Optional[str] = None) -> None:
        """
        Download specified file type from the imaging module.

        Available file types are [ 'ns', 'snr', 'dl', 'hc', 'pa', 'master', 'all' ].

        * **ns :** non saturated
        * **snr :** signal-to-noise ratio
        * **dl :** detection limit (.rdb file)
        * **hc :** high contrast
        * **pa :** Parallactic angle (.rdb file)
        * **master :** master
        * **all :** all files

        Filters and sorting order can be applied to the query via named arguments (see :doc:`query_options`).


        :param file_type: File type
        :type file_type: str
        :param filters: Filters to apply to the query
        :type filters: Optional[dict]
        :param output_directory: The directory where files will be saved
        :type output_directory: Optional[str]
        :param output_filename: The filename for the download
        :type output_filename: Optional[str]
        :return: None

        >>> from dace_query.imaging import Imaging
        >>> filters_to_use = {'file_rootpath':{'contains':'sphere/SPHERE-DRS/DRS-1.0/reduced/2018-08-19/SPHERE_IRDIS.2018-08-19T07:03:54.679_H2.fits' }}
        >>> # Imaging.download(file_type='ns', filters=filters_to_use, output_directory='/tmp', output_filename='files.tar.gz')

        """

        if file_type not in self.__ACCEPTED_FILE_TYPES:
            raise ValueError('file_type must be one of these values : ' + ','.join(self.__ACCEPTED_FILE_TYPES))
        if filters is None:
            filters = {}

        imaging_data = self.query_database(filters=filters, output_format='dict')
        files = imaging_data['file_rootpath']
        download_response = self.dace.request_post(
            api_name=self.__OBS_API,
            endpoint='download/prepare/imaging',
            data=json.dumps({
                'fileType': file_type,
                'files': files
            })
        )
        if not download_response:
            return None
        download_id = download_response['values'][0]
        self.dace.persist_file_on_disk(
            api_name=self.__OBS_API,
            obs_type='imaging',
            download_id=download_id,
            output_directory=output_directory,
            output_filename=output_filename
        )

    def get_image(self,
                  fits_file: str,
                  file_type: str,
                  output_directory: Optional[str] = None,
                  output_filename: Optional[str] = None) -> None:
        """
        Download a certain fits imaging files specified by named arguments.

        Available file types are [ 'ns', 'snr', 'dl', 'hc', 'pa', 'master', 'all' ].

        * **ns :** non saturated
        * **snr :** signal-to-noise ratio
        * **dl :** detection limit (.rdb file)
        * **hc :** high contrast
        * **pa :** Parallactic angle (.rdb file)
        * **master :** master
        * **all :** all files

        :param fits_file: The root fits file to download
        :type fits_file: str
        :param file_type: The file type to download
        :type file_type: str
        :param output_directory: The directory where files will be saved
        :type output_directory: Optional[str]
        :param output_filename: The filename for the download
        :type output_filename: Optional[str]
        :return: None

        >>> from dace_query.imaging import Imaging
        >>> fits_file_to_download, file_type = 'sphere/SPHERE-DRS/DRS-1.0/reduced/2018-08-19/SPHERE_IRDIS.2018-08-19T07:03:54.679_H2.fits', 'hc'
        >>> # Imaging.get_image(fits_file=fits_file_to_download, file_type=file_type, output_directory='/tmp', output_filename='imaging.fits')
        """

        file_type = str(file_type).upper()
        # url = '/imaging/file?filepath=' + fits_file + '&filterType=' + file_type
        self.dace.download_file(
            api_name=self.__OBS_API,
            endpoint='observation/imaging/file',
            params={
                'filepath': fits_file,
                'filterType': file_type
            },
            output_directory=output_directory,
            output_filename=output_filename
        )


Imaging: ImagingClass = ImagingClass()
"""Imaging instance"""
