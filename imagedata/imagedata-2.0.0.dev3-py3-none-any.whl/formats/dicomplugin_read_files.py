import gc

from memory_profiler import profile
from pympler import tracker
import os
import sys
import logging
import threading
import warnings
import numpy as np
from datetime import datetime, timedelta
import pydicom
import pydicom.pixel_data_handlers.numpy_handler
import pydicom.config
import pydicom.errors
from pydicom.datadict import tag_for_keyword
from pydicom.dataset import Dataset
from ..formats import CannotSort, NotImageError, INPUT_ORDER_FAULTY, input_order_to_dirname_str, \
    INPUT_ORDER_NONE, INPUT_ORDER_TIME, INPUT_ORDER_B, INPUT_ORDER_FA, INPUT_ORDER_TE
from ..axis import VariableAxis, UniformLengthAxis
from ..header import Header
from .dicomplugin_utils import getDicomAttribute, getOriginForSlice, choose_tag,\
    construct_basic_dicom, get_pixels_with_shape, UnknownTag, _reduce_shape

logger = logging.getLogger(__name__)
try:
    # pydicom >= 2.3
    pydicom.config.settings.reading_validation_mode = pydicom.config.IGNORE
    pydicom.config.settings.writing_validation_mode = pydicom.config.IGNORE
except AttributeError:
    # pydicom < 2.3
    pydicom.config.enforce_valid_values = False


class UnevenSlicesError(Exception):
    pass


class ReadFiles(threading.Thread):
    # some_lock = threading.Lock()

    def __init__(self, queue, sources, input_order, opts, skip_pixels=False):
        super().__init__()
        self.queue = queue
        self.sources = sources
        self.input_order = input_order
        self.opts = opts
        self.skip_pixels = skip_pixels
        self.daemon = True

    def run(self) -> None:
        try:
            hdr, si = self.read_files(
                self.sources, self.input_order, self.opts, self.skip_pixels)
            self.queue.put((hdr, si))
            del hdr, si
        except Exception as e:
            self.queue.put(e)
        return

    def read_files(self, sources, input_order, opts, skip_pixels=False):
        """Read DICOM objects

        Args:
            self: DICOMPlugin instance
            sources: list of sources to image data
            input_order: sort order
            opts: input options (dict)
            skip_pixels: Do not read pixel data (default: False)
        Returns:
            Tuple of
                - image_dict: dict where sliceLocations are keys
                - hdr: header
                - shape: required shape of image data
        """

        logger.debug('DICOMPlugin.read_files: sources %s' % sources)
        # try:
        image_dict, hdr, shape = self.get_dicom_files(sources, input_order, opts,
                                                      skip_pixels=skip_pixels)
        # except UnevenSlicesError:
        #    raise
        # except FileNotFoundError:
        #    raise
        # except ValueError:
        #    #import traceback
        #    #traceback.print_exc()
        #    #logger.info("process_member: Could not read {}".format(member_name))
        #    raise NotImageError(
        #        'Does not look like a DICOM file: {}'.format(sources))
        # except Exception as e:
        #    logger.debug('DICOMPlugin.read_headers: Exception {}'.format(e))
        #    raise

        if skip_pixels:
            si = None
        else:
            # Extract pixel data
            si = self.construct_pixel_array(image_dict, hdr, shape, opts=opts)

        self.extractDicomAttributes(image_dict, hdr)

        return hdr, si

    @profile
    def construct_pixel_array(self, image_dict, hdr, shape, opts={}):
        memory_tracker = tracker.SummaryTracker()
        # Look-up first image to determine pixel type
        # tag, member_name, im = hdr.DicomHeaderDict[0][0]
        tag, member_name, im = image_dict[0][0]
        # print('read: im 0: refcount {}'.format(sys.getrefcount(im)))
        hdr.photometricInterpretation = 'MONOCHROME2'
        if 'PhotometricInterpretation' in im:
            hdr.photometricInterpretation = im.PhotometricInterpretation
        matrix_dtype = np.uint16
        if 'PixelRepresentation' in im:
            if im.PixelRepresentation == 1:
                matrix_dtype = np.int16
        if 'RescaleSlope' in im and 'RescaleIntercept' in im and \
                (abs(im.RescaleSlope - 1) > 1e-4 or abs(im.RescaleIntercept) > 1e-4):
            matrix_dtype = float
        elif im.BitsAllocated == 8:
            matrix_dtype = np.uint8
        logger.debug("DICOMPlugin.read: matrix_dtype %s" % matrix_dtype)
        _color = 1 if hdr.color else 0
        # if hdr.color:
            # _color = 1
            # hdr.color = True
            # shape = shape + (im.SamplesPerPixel,)
            # hdr.axes.append(
            #     VariableAxis(
            #         'rgb',
            #         ['r', 'g', 'b']
            #     )
            # )
            # ds.SamplesPerPixel = 1
            # ds.PixelRepresentation = 0
            # try:
            #    ds.PhotometricInterpretation = arr.photometricInterpretation
            #    if arr.photometricInterpretation == 'RGB':
            #        ds.SamplesPerPixel = 3
            #        ds.PlanarConfiguration = 0
            # except ValueError:
            #    ds.PhotometricInterpretation = 'MONOCHROME2'

        logger.debug("SOPClassUID: {}".format(
            getDicomAttribute(hdr.DicomHeaderDict, tag_for_keyword("SOPClassUID"))))
        logger.debug("TransferSyntaxUID: {}".format(
            getDicomAttribute(hdr.DicomHeaderDict, tag_for_keyword("TransferSyntaxUID"))))

        # Load DICOM image data
        logger.debug('DICOMPlugin.read: shape {}'.format(shape))
        print('construct_pixel_array:')
        memory_tracker.print_diff()
        si = np.zeros(shape, matrix_dtype)
        print('construct_pixel_array: etter np.zeros')
        memory_tracker.print_diff()
        # process = psutil.Process()
        # print(process.memory_info())
        # for _slice in hdr.DicomHeaderDict:
        for _slice in image_dict:
            # noinspection PyUnusedLocal
            # _done = [False for x in range(len(hdr.DicomHeaderDict[_slice]))]
            _done = [False for x in range(len(image_dict[_slice]))]
            # for tag, member_name, im in hdr.DicomHeaderDict[_slice]:
            for tag, member_name, im in image_dict[_slice]:
                # print('read: im 1: refcount {}'.format(sys.getrefcount(im)))
                tgs = np.array(hdr.tags[_slice])
                idx = np.where(tgs == tag)[0][0]
                if _done[idx] and \
                        'AcceptDuplicateTag' in opts and \
                        opts['AcceptDuplicateTag'] == 'True':
                    while _done[idx]:
                        idx += 1
                _done[idx] = True
                if 'NumberOfFrames' in im:
                    if im.NumberOfFrames == 1:
                        idx = (idx, _slice)
                else:
                    idx = (idx, _slice)
                # Simplify index when image is 3D, remove tag index
                if si.ndim == 3 + _color:
                    idx = idx[1:]
                # Do not read file again
                # with archive.open(member, mode='rb') as f:
                #     if issubclass(type(f), pydicom.dataset.Dataset):
                #         im = f
                #     else:
                #         im = pydicom.filereader.dcmread(f)
                try:
                    im.decompress()
                    print('construct_pixel_array: etter decompress')
                    memory_tracker.print_diff()
                except NotImplementedError as e:
                    print("Cannot decompress pixel data: {}".format(e))
                    logger.error("Cannot decompress pixel data: {}".format(e))
                    raise
                try:
                    si[idx] = get_pixels_with_shape(im, si[idx].shape)
                    # si[idx] = pydicom.pixel_data_handlers.numpy_handler.get_pixeldata(im).reshape(
                    #     si[idx].shape
                    # )
                    print('construct_pixel_array: etter get_pixeldata')
                    memory_tracker.print_diff()
                except Exception as e:
                    print("Cannot read pixel data: {}".format(e))
                    logger.warning("Cannot read pixel data: {}".format(e))
                    raise
                del im
                print('construct_pixel_array: etter del im')
                memory_tracker.print_diff()
        del image_dict
        print('construct_pixel_array: etter del image_dict')
        memory_tracker.print_diff()
        gc.collect()
        print('construct_pixel_array: etter del gc.collect()')
        memory_tracker.print_diff()

        # Simplify shape
        _reduce_shape(si, hdr.axes)
        logger.debug('DICOMPlugin_read_files.construct_pixel_array: si {}'.format(si.shape))

        return si

    def get_dicom_files(self, sources, input_order, opts=None, skip_pixels=False):
        """Get DICOM objects.

        Args:
            self: DICOMPlugin instance
            sources: list of sources to image data
            input_order: Determine how to sort the input images
            opts: options (dict)
            skip_pixels: Do not read pixel data (default: False)
        Returns:
            Tuple of
                - sorted_headers: dict where sliceLocations are keys
                - hdr: Header
                - shape: tuple
        """
        logger.debug("DICOMPlugin.get_dicom_files: sources: {} {}".format(
            type(sources), sources))

        image_dict = {}
        for source in sources:
            archive = source['archive']
            scan_files = source['files']
            logger.debug("DICOMPlugin.get_dicom_files: archive: {}".format(archive))
            # if scan_files is None or len(scan_files) == 0:
            #     scan_files = ['*']
            logger.debug("get_dicom_files: source: {} {}".format(type(source), source))
            logger.debug("get_dicom_files: scan_files: {}".format(scan_files))
            for path in archive.getnames(scan_files):
                logger.debug("get_dicom_files: member: {}".format(path))
                if os.path.basename(path) == "DICOMDIR":
                    continue
                # logger.debug("get_dicom_headers: calling archive.getmembers: {}".format(
                #     len(path)))
                member = archive.getmembers([path, ])
                # logger.debug("get_dicom_headers: returned from archive.getmembers: {}".format(
                #     len(member)))
                if len(member) != 1:
                    raise IndexError('Should not be multiple files for a filename')
                member = member[0]
                try:
                    with archive.open(member, mode='rb') as f:
                        logger.debug('DICOMPlugin.get_dicom_files: process_file {}'.format(
                            member))
                        self.process_file(image_dict, archive, path, f, opts,
                                          skip_pixels=skip_pixels)
                except Exception as e:
                    logger.debug('DICOMPlugin.get_dicom_files: Exception {}'.format(e))
                    raise
        return self.sort_images(image_dict, input_order, opts)

    def sort_images(self, header_dict, input_order, opts):
        """Sort DICOM images.

        Args:
            self: DICOMPlugin instance
            header_dict: dict where sliceLocations are keys
            input_order: determine how to sort the input images
            opts: options (dict)
        Returns:
            Tuple of
                - sorted_headers
                - hdr
                    - input_format
                    - input_order
                    - slices
                    - sliceLocations
                    - DicomHeaderDict
                    - tags
                - shape
        """

        def _copy_headers(sorted_headers):
            def all_except_pixeldata_callback(dataset, data_element):
                if data_element.tag.group == 0x7fe0:
                    # print('tag (SKIP): {}'.format(data_element.tag))
                    pass
                else:
                    # print('tag: {}'.format(data_element.tag))
                    ds[data_element.tag] = dataset[data_element.tag]

            headers = {}
            for s in sorted(sorted_headers):
                headers[s] = []
                for tg, member_name, im in sorted_headers[s]:
                    ds = construct_basic_dicom()
                    im.walk(all_except_pixeldata_callback)
                    headers[s].append((tg, member_name, ds))
            return headers

        hdr = Header()
        hdr.input_format = 'dicom'
        hdr.input_order = input_order
        sliceLocations = sorted(header_dict)
        # hdr.slices = len(sliceLocations)
        hdr.sliceLocations = sliceLocations

        # Verify same number of images for each slice
        if len(header_dict) == 0:
            raise ValueError("No DICOM images found.")
        count = np.zeros(len(header_dict), dtype=int)
        islice = 0
        for sloc in sorted(header_dict):
            count[islice] += len(header_dict[sloc])
            islice += 1
        logger.debug("sort_images: tags per slice: {}".format(count))
        accept_uneven_slices = accept_duplicate_tag = False
        if 'accept_uneven_slices' in opts and \
                opts['accept_uneven_slices'] == 'True':
            accept_uneven_slices = True
        if 'accept_duplicate_tag' in opts and \
                opts['accept_duplicate_tag'] == 'True':
            accept_duplicate_tag = True
        if min(count) != max(count) and accept_uneven_slices:
            logger.error("sort_images: tags per slice: {}".format(count))
            raise UnevenSlicesError("Different number of images in each slice.")

        # Extract all tags and sort them per slice
        tag_list = {}
        islice = 0
        for sloc in sorted(header_dict):
            tag_list[islice] = []
            i = 0
            for archive, filename, im in sorted(header_dict[sloc]):
                # print('sort_images: im 0: refcount {}'.format(sys.getrefcount(im)))
                try:
                    tag = self._get_tag(im, input_order, opts)
                except KeyError:
                    if input_order == INPUT_ORDER_FAULTY:
                        tag = i
                    else:
                        raise CannotSort('Tag not found in dataset')
                except Exception:
                    raise
                if tag is None:
                    raise CannotSort("Tag {} not found in data".format(input_order))
                if tag not in tag_list[islice] or accept_duplicate_tag:
                    tag_list[islice].append(tag)
                else:
                    raise CannotSort("Duplicate tag ({}): {}".format(input_order, tag))
                i += 1
            islice += 1
        for islice in range(len(header_dict)):
            tag_list[islice] = sorted(tag_list[islice])
        # Sort images based on position in tag_list
        sorted_headers = {}
        islice = 0
        # Allow for variable sized slices
        frames = None
        rows = columns = 0
        i = 0
        for sloc in sorted(header_dict):
            # Pre-fill sorted_headers
            sorted_headers[islice] = [False for _ in range(count[islice])]
            for archive, filename, im in sorted(header_dict[sloc]):
                # print('sort_images: im 1: refcount {}'.format(sys.getrefcount(im)))
                if input_order == INPUT_ORDER_FAULTY:
                    tag = i
                else:
                    tag = self._get_tag(im, input_order, opts)
                idx = tag_list[islice].index(tag)
                if sorted_headers[islice][idx]:
                    # Duplicate tag
                    if accept_duplicate_tag:
                        while sorted_headers[islice][idx]:
                            idx += 1
                    else:
                        print("WARNING: Duplicate tag", tag)
                # sorted_headers[islice].insert(idx, (tag, (archive,filename), image))
                # noinspection PyTypeChecker
                sorted_headers[islice][idx] = (tag, (archive, filename), im)
                rows = max(rows, im.Rows)
                columns = max(columns, im.Columns)
                if 'NumberOfFrames' in im:
                    frames = im.NumberOfFrames
                i += 1
            islice += 1
        hdr.DicomHeaderDict = _copy_headers(sorted_headers)
        hdr.tags = tag_list
        nz = len(header_dict)
        if frames is not None and frames > 1:
            nz = frames
        if len(tag_list[0]) > 1:
            shape = (len(tag_list[0]), nz, rows, columns)
        else:
            shape = (nz, rows, columns)
        spacing = self.__get_voxel_spacing(sorted_headers)
        ipp = getDicomAttribute(sorted_headers, tag_for_keyword('ImagePositionPatient'))
        if ipp is not None:
            ipp = np.array(list(map(float, ipp)))[::-1]  # Reverse xyz
        else:
            ipp = np.array([0, 0, 0])
        axes = list()
        if len(tag_list[0]) > 1:
            axes.append(
                VariableAxis(
                    input_order_to_dirname_str(input_order),
                    tag_list[0])
            )
        axes.append(UniformLengthAxis(
            'slice',
            ipp[0],
            nz,
            spacing[0]))
        axes.append(UniformLengthAxis(
            'row',
            ipp[1],
            rows,
            spacing[1]))
        axes.append(UniformLengthAxis(
            'column',
            ipp[2],
            columns,
            spacing[2]))
        hdr.color = False
        if 'SamplesPerPixel' in im and im.SamplesPerPixel == 3:
            _color = 1
            hdr.color = True
            shape = shape + (im.SamplesPerPixel,)
            hdr.axes.append(
                VariableAxis(
                    'rgb',
                    ['r', 'g', 'b']
                )
            )
        hdr.axes = axes
        return sorted_headers, hdr, shape

    def process_file(self, image_dict, archive, member_name, member, opts, skip_pixels=False):
        if issubclass(type(member), pydicom.dataset.Dataset):
            im = member
        else:
            try:
                im = pydicom.filereader.dcmread(member, stop_before_pixels=skip_pixels)
            except pydicom.errors.InvalidDicomError:
                return

        if 'input_serinsuid' in opts and opts['input_serinsuid']:
            if im.SeriesInstanceUID != opts['input_serinsuid']:
                return
        if 'input_echo' in opts and opts['input_echo']:
            if int(im.EchoNumbers) != int(opts['input_echo']):
                return

        try:
            sloc = float(im.SliceLocation)
        except AttributeError:
            logger.debug('DICOMPlugin.process_file: Calculate SliceLocation')
            try:
                sloc = self._calculate_slice_location(im)
            except ValueError:
                sloc = 0
        logger.debug('DICOMPlugin.process_file: {} SliceLocation {}'.format(member, sloc))

        if sloc not in image_dict:
            image_dict[sloc] = []
        image_dict[sloc].append((archive, member_name, im))
        # print('process_file: im 1: refcount {}'.format(sys.getrefcount(im)))
        # logger.debug("process_file: added sloc {} {}".format(sloc, member_name))
        # logger.debug("process_file: image_dict len: {}".format(len(image_dict)))

    def extractDicomAttributes(self, dictionary, hdr):
        """Extract DICOM attributes

        Args:
            self: DICOMPlugin instance
            dictionary: image dictionary
            hdr: header
        Returns:
            hdr: header
                - seriesNumber
                - seriesDescription
                - imageType
                - spacing
                - orientation
                - imagePositions
                - axes
        """
        hdr.studyInstanceUID = \
            getDicomAttribute(dictionary, tag_for_keyword('StudyInstanceUID'))
        hdr.studyID = \
            getDicomAttribute(dictionary, tag_for_keyword('StudyID'))
        hdr.seriesInstanceUID = \
            getDicomAttribute(dictionary, tag_for_keyword('SeriesInstanceUID'))
        frame_uid = getDicomAttribute(dictionary, tag_for_keyword('FrameOfReferenceUID'))
        if frame_uid:
            hdr.frameOfReferenceUID = frame_uid
        hdr.SOPClassUID = getDicomAttribute(dictionary, tag_for_keyword('SOPClassUID'))
        hdr.seriesNumber = getDicomAttribute(dictionary, tag_for_keyword('SeriesNumber'))
        hdr.seriesDescription = getDicomAttribute(dictionary, tag_for_keyword('SeriesDescription'))
        hdr.imageType = getDicomAttribute(dictionary, tag_for_keyword('ImageType'))

        hdr.accessionNumber = getDicomAttribute(dictionary, tag_for_keyword('AccessionNumber'))
        hdr.patientName = getDicomAttribute(dictionary, tag_for_keyword('PatientName'))
        hdr.patientID = getDicomAttribute(dictionary, tag_for_keyword('PatientID'))
        hdr.patientBirthDate = getDicomAttribute(dictionary, tag_for_keyword('PatientBirthDate'))

        hdr.spacing = self.__get_voxel_spacing(dictionary)

        # Image position (patient)
        # Reverse orientation vectors from (x,y,z) to (z,y,x)
        iop = getDicomAttribute(dictionary, tag_for_keyword("ImageOrientationPatient"))
        if iop is not None:
            hdr.orientation = np.array((iop[2], iop[1], iop[0],
                                        iop[5], iop[4], iop[3]))

        # Extract imagePositions
        hdr.imagePositions = {}
        for _slice in dictionary:
            hdr.imagePositions[_slice] = getOriginForSlice(dictionary, _slice)

    def _get_tag(self, im, input_order, opts):

        if input_order is None:
            return 0
        if 'input_options' in opts:
            input_options = opts['input_options']
        else:
            input_options = opts
        if input_order == INPUT_ORDER_NONE:
            return 0
        elif input_order == INPUT_ORDER_TIME:
            time_tag = choose_tag(input_options, 'time', 'AcquisitionTime')
            # if 'TriggerTime' in opts:
            #    return(float(image.TriggerTime))
            # elif 'InstanceNumber' in opts:
            #    return(float(image.InstanceNumber))
            # else:
            if im.data_element(time_tag).VR == 'TM':
                time_str = im.data_element(time_tag).value
                if '.' in time_str:
                    tm = datetime.strptime(time_str, "%H%M%S.%f")
                else:
                    tm = datetime.strptime(time_str, "%H%M%S")
                td = timedelta(hours=tm.hour,
                               minutes=tm.minute,
                               seconds=tm.second,
                               microseconds=tm.microsecond)
                return td.total_seconds()
            else:
                return float(im.data_element(time_tag).value)
        elif input_order == INPUT_ORDER_B:
            b_tag = choose_tag(input_options, 'b', 'DiffusionBValue')
            try:
                return float(im.data_element(b_tag).value)
            except (KeyError, TypeError):
                pass
            b_tag = choose_tag(input_options, 'b', 'csa_header')
            if b_tag == 'csa_header':
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=UserWarning)
                    import nibabel.nicom.csareader as csa
                csa_head = csa.get_csa_header(im)
                try:
                    value = csa.get_b_value(csa_head)
                except TypeError:
                    raise CannotSort("Unable to extract b value from header.")
            else:
                value = float(im.data_element(b_tag).value)
            return value
        elif input_order == INPUT_ORDER_FA:
            fa_tag = choose_tag(input_options, 'fa', 'FlipAngle')
            return float(im.data_element(fa_tag).value)
        elif input_order == INPUT_ORDER_TE:
            te_tag = choose_tag(input_options, 'te', 'EchoTime')
            return float(im.data_element(te_tag).value)
        else:
            # User-defined tag
            if input_order in opts:
                _tag = opts[input_order]
                return float(im.data_element(_tag).value)
        raise (UnknownTag("Unknown input_order {}.".format(input_order)))

    def __get_voxel_spacing(self, dictionary):
        # Spacing
        pixel_spacing = getDicomAttribute(dictionary, tag_for_keyword("PixelSpacing"))
        dy = 1.0
        dx = 1.0
        if pixel_spacing is not None:
            # Notice that DICOM row spacing comes first, column spacing second!
            dy = float(pixel_spacing[0])
            dx = float(pixel_spacing[1])
        try:
            dz = float(getDicomAttribute(dictionary, tag_for_keyword("SpacingBetweenSlices")))
        except TypeError:
            try:
                dz = float(getDicomAttribute(dictionary, tag_for_keyword("SliceThickness")))
            except TypeError:
                dz = 1.0
        return np.array([dz, dy, dx])

