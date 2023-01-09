from memory_profiler import profile
import numpy as np
import logging
import pydicom.datadict
import pydicom.dataset
import pydicom.uid
from pydicom.datadict import tag_for_keyword


root = "2.16.578.1.37.1.1.4"
logger = logging.getLogger(__name__)


class UnknownTag(Exception):
    pass


class FilesGivenForMultipleURLs(Exception):
    pass


class NoDICOMAttributes(Exception):
    pass


class ValueErrorWrapperPrecisionError(Exception):
    pass


def setDicomAttribute(dictionary, tag, value):
    """Set a given DICOM attribute to the provided value.

    Ignore if no real dicom header exists.

    Args:
        dictionary: image dictionary
        tag: DICOM tag of addressed attribute.
        value: Set attribute to this value.
    """
    if dictionary is not None:
        for _slice in dictionary:
            for tg, fname, im in dictionary[_slice]:
                if tag not in im:
                    vr = pydicom.datadict.dictionary_VR(tag)
                    im.add_new(tag, vr, value)
                else:
                    im[tag].value = value


def getDicomAttribute(dictionary, tag, slice=0):
    """Get DICOM attribute from first image for given slice.

    Args:
        dictionary: image dictionary
        tag: DICOM tag of requested attribute.
        slice: which slice to access. Default: slice=0
    """
    # logger.debug("getDicomAttribute: tag", tag, ", slice", slice)
    assert dictionary is not None, "dicomplugin.getDicomAttribute: dictionary is None"
    # tg, fname, im = self.DicomHeaderDict[slice][0]
    tg, fname, im = dictionary[slice][0]
    if tag in im:
        return im[tag].value
    else:
        return None


def removePrivateTags(dictionary):
    """Remove private DICOM attributes.

    Ignore if no real dicom header exists.

    Args:
        dictionary: image dictionary
    """
    if dictionary is not None:
        for _slice in dictionary:
            for tg, fname, im in dictionary[_slice]:
                im.remove_private_tags()


def getOriginForSlice(dictionary, slice):
    """Get origin of given slice.

    Args:
        dictionary: image dictionary
        slice: slice number (int)
    Returns:
        z,y,x: coordinate for origin of given slice (np.array)
    """

    origin = getDicomAttribute(dictionary, tag_for_keyword("ImagePositionPatient"), slice)
    if origin is not None:
        x = float(origin[0])
        y = float(origin[1])
        z = float(origin[2])
        return np.array([z, y, x])
    return None


def choose_tag(input_options, tag, default):
    # Example: _tag = choose_tag(self, 'b', 'csa_header')
    if tag in input_options:
        return input_options[tag]
    else:
        return default


def construct_basic_dicom(template=None, filename='NA', sop_ins_uid=None):

    # Populate required values for file meta information
    file_meta = pydicom.dataset.FileMetaDataset()
    if template is not None:
        file_meta.MediaStorageSOPClassUID = template.SOPClassUID
    if sop_ins_uid is not None:
        file_meta.MediaStorageSOPInstanceUID = sop_ins_uid
    file_meta.ImplementationClassUID = "%s.1" % root
    file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian

    # Create the FileDataset instance
    # (initially no data elements, but file_meta supplied)
    ds = pydicom.dataset.FileDataset(
        filename,
        {},
        file_meta=file_meta,
        preamble=b"\0" * 128)
    return ds


def get_pixels(im):
    """Get pixels from image object.

    Args:
        im: dicom image
    Returns:
        si: numpy array
    """

    _use_float = False
    try:
        # logger.debug("Set si[{}]".format(idx))
        if 'RescaleSlope' in im and 'RescaleIntercept' in im:
            _use_float = abs(im.RescaleSlope - 1) > 1e-4 or abs(im.RescaleIntercept) > 1e-4
        if _use_float:
            si = float(im.RescaleSlope) * im.pixel_array.astype(float) + \
                     float(im.RescaleIntercept)
        else:
            # pixels = im.pixel_array.copy()
            si = im.pixel_array
        # si = np.ndarray(pixels.shape, dtype=pixels.dtype, buffer=pixels)
        # si[:] = pixels
        # si = np.array(pixels)
    except UnboundLocalError:
        # A bug in pydicom appears when reading binary images
        if im.BitsAllocated == 1:
            logger.debug(
                "Binary image, image.shape={}, image shape=({},{},{})".format(
                    im.shape, im.NumberOfFrames, im.Rows, im.Columns))
            # try:
            #    image.decompress()
            # except NotImplementedError as e:
            #    logger.error("Cannot decompress pixel data: {}".format(e))
            #    raise
            _myarr = np.frombuffer(im.PixelData, dtype=np.uint8)
            # Reverse bit order, and copy the array to get a
            # contiguous array
            bits = np.unpackbits(_myarr).reshape(-1, 8)[:, ::-1].copy()
            si = np.fliplr(
                bits.reshape(
                    1, im.NumberOfFrames, im.Rows, im.Columns))
            if _use_float:
                si = float(im.RescaleSlope) * si + float(im.RescaleIntercept)
        else:
            raise
    # Delete pydicom's pixel data to save memory
    # im._pixel_array = None
    # if 'PixelData' in im:
    #    im[0x7fe00010].value = None
    #    im[0x7fe00010].is_undefined_length = True
    # im.PixelData = None
    return si


@profile
def get_pixels_with_shape(im, shape):
    """Get pixels from image object. Reshape image to given shape

    Args:
        im: dicom image
        shape: requested image shape
    Returns:
        si: numpy array of given shape
    """

    _use_float = False
    try:
        # logger.debug("Set si[{}]".format(idx))
        if 'RescaleSlope' in im and 'RescaleIntercept' in im:
            _use_float = abs(im.RescaleSlope - 1) > 1e-4 or abs(im.RescaleIntercept) > 1e-4
        if _use_float:
            pixels = float(im.RescaleSlope) * im.pixel_array.astype(float) + \
                     float(im.RescaleIntercept)
        else:
            pixels = im.pixel_array.copy()
        if shape != pixels.shape:
            # This happens only when images in a series have varying shape
            # Place the pixels in the upper left corner of the matrix
            assert len(shape) == len(pixels.shape), \
                "Shape of matrix ({}) differ from pixel shape ({})".format(
                    shape, pixels.shape)
            # Assume that pixels can be expanded to match si shape
            si = np.zeros(shape, pixels.dtype)
            roi = []
            for d in pixels.shape:
                roi.append(slice(d))
            roi = tuple(roi)
            si[roi] = pixels
        else:
            si = pixels
    except UnboundLocalError:
        # A bug in pydicom appears when reading binary images
        if im.BitsAllocated == 1:
            logger.debug(
                "Binary image, image.shape={}, image shape=({},{},{})".format(
                    im.shape, im.NumberOfFrames, im.Rows, im.Columns))
            # try:
            #    image.decompress()
            # except NotImplementedError as e:
            #    logger.error("Cannot decompress pixel data: {}".format(e))
            #    raise
            _myarr = np.frombuffer(im.PixelData, dtype=np.uint8)
            # Reverse bit order, and copy the array to get a
            # contiguous array
            bits = np.unpackbits(_myarr).reshape(-1, 8)[:, ::-1].copy()
            si = np.fliplr(
                bits.reshape(
                    1, im.NumberOfFrames, im.Rows, im.Columns))
            if _use_float:
                si = float(im.RescaleSlope) * si + float(im.RescaleIntercept)
        else:
            raise
    # Delete pydicom's pixel data to save memory
    # image._pixel_array = None
    # if 'PixelData' in image:
    #    image[0x7fe00010].value = None
    #    image[0x7fe00010].is_undefined_length = True
    return si


def _reduce_shape(si, axes=None):
    """Reduce shape when leading shape(s) are 1.

    Will not reduce to less than 2-dimensional image.
    Also reduce axes when reducing shape.

    Args:
        si[...]: Series array
    Raises:
        ValueError: tags for dataset is not time tags
    """

    # Color image?
    mindim = 2
    if si.shape[-1] == 3:
        mindim += 1

    while si.ndim > mindim:
        if si.shape[0] == 1:
            si.shape = si.shape[1:]
            if axes is not None:
                del axes[0]
        else:
            break
