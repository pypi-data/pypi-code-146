import os
import cv2
import copy
import json
import uuid
import base64
import pydicom
import numpy as np
from datetime import datetime
from pydicom.dataset import Dataset
from pydicom.valuerep import DSfloat
from pydicom.sequence import Sequence
from pydicom.multival import MultiValue
from pydicom.pixel_data_handlers.util import convert_color_space, apply_color_lut
from pydicom.pixel_data_handlers.util import apply_voi_lut


def encoding_heatmap(mask, thres=0.5):
    assert mask.max() <= 1
    assert mask.min() >= 0

    grad_cam = mask
    heatmap = cv2.applyColorMap(np.uint8(255 * np.clip(grad_cam - thres, 0, 1) / (1 - thres)), cv2.COLORMAP_JET)
    back_index = np.where(grad_cam < thres)
    heatmap[back_index] = 0
    b, g, r = cv2.split(heatmap)
    a = np.ones(b.shape, b.dtype) * 255
    a[back_index] = 0
    img_bgra = cv2.merge([b, g, r, a])
    cv2.imwrite('/tmp/tmp.png', img_bgra)
    heatmap_encoded = base64.b64encode(open("/tmp/tmp.png", "rb").read()).decode()
    os.remove('/tmp/tmp.png')
    return heatmap_encoded


def rgb2Lab(color):
    color_Lab = cv2.cvtColor(np.array([[color]]).astype(np.uint8), cv2.COLOR_RGB2Lab).squeeze()
    return [color_Lab[0] * 256, color_Lab[1] * 256, color_Lab[2] * 256]


def paste_image(report, cam, x, y, w, h, scale):
    x1 = int(x * scale)
    y1 = int(y * scale)
    w = int(w * scale)
    h = int(h * scale)
    x2 = x1 + w
    y2 = y1 + h
    paste_image = cam.resize((w, h))
    if cam.mode == 'RGBA':
        report.paste(paste_image, [x1, y1, x2, y2], paste_image)
    else:
        report.paste(paste_image, [x1, y1, x2, y2])

def read_dcm(ds):
    arr = ds.pixel_array
    mode = ds.PhotometricInterpretation
    if 'YBR_FULL' in mode:
        ori_image_array = convert_color_space(arr, mode, 'RGB')
    elif mode == 'PALETTE COLOR':
        ori_image_array = apply_color_lut(arr, ds)
    elif 'MONOCHROME' in mode:
        try:
            if ds.__contains__('RescaleIntercept') and ds.__contains__('RescaleSlope'):
                intercept = ds.RescaleIntercept
                slope = ds.RescaleSlope
            else:
                intercept = 0
                slope = 1
            out = slope * arr + intercept
        except:
            out = arr
            
        if ds.__contains__('WindowWidth') and ds.__contains__('WindowCenter'):
            if type(ds.WindowCenter) == DSfloat:
                wc = ds.WindowCenter
                ww = ds.WindowWidth
            else:
                wc = ds.WindowCenter[0]
                ww = ds.WindowWidth[0]

            wl = int(wc - 0.5 - (ww - 1) / 2)
            wu = int(wc - 0.5 + (ww - 1) / 2)

            out[np.where(out <= wl)] = wl
            out[np.where(out >= wu)] = wu
            
            ori_image_array = (out - wl) / (wu - wl)
            
        elif ds.__contains__('VOILUTSequence'):
            out = apply_voi_lut(out, ds)
            ori_image_array = out / ds.VOILUTSequence[0].LUTDescriptor[0]
            
        else:
            raise KeyError

        if mode == 'MONOCHROME1':
            ori_image_array = 1 - ori_image_array

        ori_image_array *= 255

    if ori_image_array.ndim != 3:
        ori_image_array = np.stack([ori_image_array] * 3, axis=-1)
    if ori_image_array.shape[-1] == 4:
        ori_image_array = ori_image_array[..., :3]

    return ori_image_array


def scan_directory(input_path): 
    paths = sorted(list(input_path.glob('*.dcm')))
    study_instance_uids = {}
    for path in paths:
        ds = pydicom.dcmread(str(path), force=True)
        study_uid = ds.StudyInstanceUID
        series_uid = ds.SeriesInstanceUID
        if study_uid in study_instance_uids:
            if series_uid in study_instance_uids[study_uid]:
                study_instance_uids[study_uid][series_uid].append(path)
            else:
                study_instance_uids[study_uid].update(
                    {
                        series_uid: [path]
                    }
                )

        else:
            study_instance_uids.update(
                {
                    study_uid: {
                        series_uid: [path]
                    }
                }
            )
    return study_instance_uids


def make_dataset(input_dicom, product_name, app_name, app_version, result_dcm_format='SC', use_uid=None, preferred_charset=''):
    ds = Dataset()
    copy_dicom_tags(ds, copy.deepcopy(input_dicom), result_dcm_format)
    set_dicom_tags(ds, product_name, app_name, app_version, result_dcm_format)
    if preferred_charset:
        convert_charset(ds, preferred_charset)
    set_time(ds, result_dcm_format)
    set_uids(ds, input_dicom, use_uid, result_dcm_format)
    ds.preamble = input_dicom.preamble
    ds.file_meta.MediaStorageSOPClassUID = ds.SOPClassUID
    ds.file_meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
    return ds


def convert_charset(dicom, preferred_charset):
    python_encode_type = pydicom.charset.convert_encodings(dicom.SpecificCharacterSet)[0]
    python_decode_type = pydicom.charset.convert_encodings(preferred_charset)[0]
    for tag in ['InstitutionName', 'PatientName', 'StudyDescription']:
        if dicom.__contains__(tag):
            raw_value = dicom[tag].value
            encoded_value = raw_value.encode(python_encode_type)
            decoded_value = encoded_value.decode(python_decode_type)
            setattr(dicom, tag, decoded_value)


def copy_dicom_tags(dicom, input_dicom, result_dcm_format='SC'):
    type1_elements = [
        'StudyInstanceUID', # General Study
        # 'SpecificCharacterSet',
    ]

    type2_elements = [
        'PatientName', # Patient
        'PatientID',
        'PatientBirthDate',
        'PatientSex',
        'StudyDate', # General Study
        'StudyTime',
        'ReferringPhysicianName',
        'StudyID',
        'AccessionNumber',
        'StudyDescription', # for SC
    ]
    if result_dcm_format == 'SC':
        type2_elements += [
            'Rows',
            'Columns',
            'PixelSpacing',
        ]
    elif result_dcm_format == 'GSPS':
        type2_elements += [
        ]

    type3_elements = [
        'PatientAge', # Patient Study
        'PatientSize',
        'PatientWeight',
        'InstitutionName',
        'StudyComments',
    ]
    if result_dcm_format == 'SC':
        type3_elements += [
            'ViewPosition',
            'Laterality',
            'ImagerPixelSpacing',
        ]
    elif result_dcm_format == 'GSPS':
        type3_elements += [
        ]
    private_elements = [
        (0x3355, 0x0010), # Priave Creator
        (0x3355, 0x1001), # AET
        (0x3355, 0x1002), # DEEPAIReqType
        (0x3355, 0x1003), # DEEPAIReqCharset
    ]

    dicom.file_meta = input_dicom.file_meta
    for tag in type1_elements:
        if dicom.__contains__(tag):
            assert dicom[tag].value in ['', input_dicom[tag].value]
        else:
            assert input_dicom.__contains__(tag)
            dicom.add(input_dicom.data_element(tag))

    tag = 'SpecificCharacterSet'
    if input_dicom.__contains__(tag):
        if type(input_dicom.SpecificCharacterSet) == MultiValue:
            dicom.SpecificCharacterSet = input_dicom.SpecificCharacterSet[-1]
        else:
            dicom.add(input_dicom.data_element(tag))
    else:
        dicom.SpecificCharacterSet = 'ISO_IR 100'

    for tag in type2_elements:
        if dicom.__contains__(tag):
            assert dicom[tag].value in ['', input_dicom[tag].value]
        else:
            if input_dicom.__contains__(tag):
                dicom.add(input_dicom.data_element(tag))
            else:
                setattr(dicom, tag, '')

    for tag in type3_elements:
        if dicom.__contains__(tag):
            assert dicom[tag].value == input_dicom[tag].value
        else:
            if input_dicom.__contains__(tag):
                dicom.add(input_dicom.data_element(tag))

    for tag in private_elements:
        if tag in dicom:
            assert dicom[tag].value == input_dicom[tag].value
        else:
            if tag in input_dicom:
                dicom[tag] = input_dicom[tag]

def set_uids(
        dicom,
        input_dicom,
        use_uid=None,
        result_dcm_format='SC'
    ):
    if not use_uid:
        use_uid = uuid.uuid4().int
    try:
        series_idx = int(input_dicom.SeriesNumber)
    except:
        series_idx = 1
    try:
        instance_idx = int(input_dicom.InstanceNumber)
    except:
        instance_idx = 1

    if result_dcm_format == 'SC':
        dicom.SeriesInstanceUID = '2.25.{:d}.1.{:d}'.format(series_idx, use_uid)
        dicom.SOPInstanceUID = '2.25.{:d}.1.{:d}.{:d}'.format(series_idx, instance_idx, use_uid)
        dicom.SeriesNumber = '99991' + str(series_idx)
        dicom.InstanceNumber = str(instance_idx)
    if result_dcm_format == 'RP':
        dicom.SeriesInstanceUID = '2.25.{:d}.2.{:d}'.format(series_idx, use_uid)
        dicom.SOPInstanceUID = '2.25.{:d}.2.{:d}.{:d}'.format(series_idx, instance_idx, use_uid)
        dicom.SeriesNumber = '99992' + str(series_idx)
        dicom.InstanceNumber = str(instance_idx)
    elif result_dcm_format == 'GSPS':
        dicom.SeriesInstanceUID = '2.25.0.0.{:d}'.format(use_uid)
        dicom.SOPInstanceUID = '2.25.0.0.0.{:d}'.format(use_uid)
        dicom.SeriesNumber = '999999999'
        dicom.InstanceNumber = '1'


def set_dicom_tags(dicom, product_name, app_name, app_version, result_dcm_format='SC'):
    series_tag_values = [
        ('SeriesDescription', product_name),
        ('Manufacturer', 'DEEPNOID'), # General Equipment
    ]
    if result_dcm_format in ['SC', 'RP']:
        series_tag_values += [
            ('Modality', 'OT'),  # General Series
            ('SOPClassUID', '1.2.840.10008.5.1.4.1.1.7'), # SOP Common,
            ('SamplesPerPixel', 3),
            ('PhotometricInterpretation', 'RGB'),
            ('BitsAllocated', 8),
            ('BitsStored', 8),
            ('HighBit', 7),
            ('PlanarConfiguration', 0),
            ('PixelRepresentation', 0), # 0: unsigned integer, 1: 2's complement
            ('RescaleSlope', '1'),
            ('RescaleIntercept', '0'),
            ('RescaleType', 'US'), # Unspecified
            ('ConversionType', 'WSD'), # Workstation, The equipment that placed the modified image into a DICOM SOP instance.
        ]
    elif result_dcm_format == 'GSPS':
        series_tag_values += [
            ('InstanceNumber', 1),
            ('Modality', 'PR'),
            ('SOPClassUID', "1.2.840.10008.5.1.4.1.1.11.1"), # SOP Common,
            ('SoftwareVersions', app_version),
            ('ContentLabel', app_name),
            ('ContentDescription', 'Detect Consolidation and Pneumothorax from CXR.'),
            ('ContentCreatorName', 'DEEPNOID'),
            ('PresentationLUTShape', 'IDENTITY'),
        ]

    for tag, value in series_tag_values:
        if dicom.__contains__(tag):
            assert dicom[tag].value == value
        else:
            setattr(dicom, tag, value)
              
    dicom.file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1'


def set_time(dicom, result_dcm_format='SC'):
    creation_date = datetime.now().date().strftime("%Y%m%d")
    creation_time = datetime.now().time().strftime("%H%M%S")
    series_tag_values = [
        ('SeriesDate', creation_date),
        ('SeriesTime', creation_time),
    ]
    if result_dcm_format in ['SC', 'RP']:
        series_tag_values += [
            ('DateOfSecondaryCapture', creation_date), # SC Image Module
            ('TimeOfSecondaryCapture', creation_time),
        ]
    elif result_dcm_format == 'GSPS':
        series_tag_values += [
            ('PresentationCreationDate', creation_date), # Presentation State Identification
            ('PresentationCreationTime', creation_time),
        ]
    for tag, value in series_tag_values:
        setattr(dicom, tag, value)


def set_private_tags(dicom, finding_sequence, app_name, app_version):
    result_js = {
        'FormatVersion': '1.0',
        'Date': dicom.SeriesDate,
        'Time': dicom.SeriesTime,
        'Vendor': 'DEEPNOID',
        'Service': 'DEEP:AI',
        'Model': app_name,
        'Version': app_version
    }
    block = dicom.private_block(0x2021, 'DEEPNOID', create=True)
    block.add_new(0x01, 'LO', "DEEPNOID")
    block.add_new(0x02, 'LO', 'DEEP:AI')
    block.add_new(0x03, 'LO', app_name)
    block.add_new(0x04, 'LO', app_version)
    block.add_new(0x05, 'SS', 1)
    block.add_new(0x06, 'SS', 1)
    block.add_new(0x08, 'UT', json.dumps(result_js))
    block.add_new(0x11, 'SQ', Sequence(finding_sequence))

def get_referenced_image_dataset(input_dicom):
    dataset = Dataset()
    dataset.ReferencedSOPClassUID = input_dicom.SOPClassUID # (0008:1150)
    dataset.ReferencedSOPInstanceUID = input_dicom.SOPInstanceUID # (0008:1155)
    return dataset


def get_referenced_series_dataset(series_instance_uid, referenced_image_sequence):
    dataset = Dataset()
    dataset.SeriesInstanceUID = series_instance_uid
    dataset.ReferencedImageSequence = referenced_image_sequence
    return dataset


def get_graphic_layer_dataset(layer_name, layer_order):
    assert type(layer_name) == str
    assert type(layer_order) == int
    dataset = Dataset()
    dataset.GraphicLayer = layer_name
    dataset.GraphicLayerOrder = layer_order
    return dataset


def get_text_style_dataset(
    style='SOLID',
    color=[255, 255, 255],
    horizontal_align='CENTER',
    vertical_align='CENTER',
    shadow_style='NORMAL',
    shadow_color=[127, 127, 127],
    shadow_offset=[3, 3],
    shadow_opacity=1.0,
    ):
    
    assert style in ['SOLID', 'DASHED']
    assert shadow_style in ['NORMAL', 'OUTLINED', 'OFF']
    
    dataset = Dataset()
    dataset.CSSFontName = 'Malgun Gothic'
    dataset.TextColorCIELabValue = rgb2Lab(color)
    dataset.HorizontalAlignment = horizontal_align
    dataset.VerticalAlignment = vertical_align
    dataset.Underlined = 'N'
    dataset.Bold = 'N'
    dataset.Italic = 'N'
    dataset.ShadowStyle = shadow_style
    if shadow_style != 'OFF':
        dataset.ShadowColorCIELabValue = rgb2Lab(shadow_color)
        dataset.ShadowOffsetX = shadow_offset[0]
        dataset.ShadowOffsetY = shadow_offset[1]
        dataset.ShadowOpacity = shadow_opacity
    return dataset

def get_line_style_dataset(
    color,
    thickness,
    style='SOLID',
    opacity=1.0,
    off_color=[0, 0, 0],
    off_opacity=0.0,
    shadow_style='OUTLINED',
    shadow_color=[127, 127, 127],
    shadow_offset=[3, 3],
    shadow_opacity=1.0
    ):
    
    assert style in ['SOLID', 'DASHED']
    assert shadow_style in ['NORMAL', 'OUTLINED', 'OFF']
    
    dataset = Dataset()
    dataset.PatternOnColorCIELabValue = rgb2Lab(color)
    dataset.PatternOnOpacity = opacity
    dataset.LineThickness = thickness
    dataset.LineDashingStyle = style
    if style == 'DASHED':
        dataset.PaternOffColorCIELabValue = rgb2Lab(off_color)
        dataset.PatternOffOpacity = off_opacity
        # dataset.LinePattern = 00FFH 
    dataset.ShadowStyle = shadow_style
    dataset.ShadowColorCIELabValue = rgb2Lab(shadow_color)
    dataset.ShadowOffsetX = shadow_offset[0]
    dataset.ShadowOffsetY = shadow_offset[1]
    dataset.ShadowOpacity = shadow_opacity
    return dataset

def get_fill_style_dataset(
        color,
        off_color=[127, 127, 127],
        opacity=1.0,
        off_opacity=0.0,
        fill_mode='SOLID'
    ):
    assert fill_mode in ['SOLID', 'STIPPELED']
    dataset = Dataset()
    dataset.PatternOnColorCIELabValue = rgb2Lab(color)
    dataset.PatternOnOpacity = opacity
    dataset.FillMode = fill_mode
    if fill_mode == 'STIPPELED':
        dataset.PatternOffColorCIELabValue = rgb2Lab(off_color)
        dataset.PatternOffOpacity = off_opacity
        # dataset.FillPattern = 
    return dataset


def get_graphic_annotation_dataset(
        referenced_image_sequence,
        layer_name,
        text_object_sequence=None,
        graphic_object_sequence=None
    ):
    assert (text_object_sequence is not None) or (graphic_object_sequence is not None)

    dataset = Dataset()
    dataset.ReferencedImageSequence = referenced_image_sequence
    dataset.GraphicLayer = layer_name
    if text_object_sequence is not None:
        dataset.TextObjectSequence = text_object_sequence
    if graphic_object_sequence is not None:
        dataset.GraphicObjectSequence = graphic_object_sequence
    return dataset

def get_text_object_dataset(
        text_data,
        bbox, # (x1, y1, x2, y2)
        text_style,
        boundingbox_annotation_units='PIXEL',
        horizontal_justification='CENTER'
    ):
    dataset = Dataset()
    dataset.BoundingBoxAnnotationUnits = boundingbox_annotation_units
    dataset.BoundingBoxTopLeftHandCorner = [bbox[0], bbox[1]]
    dataset.BoundingBoxBottomRightHandCorner = [bbox[2], bbox[3]]
    dataset.BoundingBoxTextHorizontalJustification = horizontal_justification

    dataset.TextStyleSequence = Sequence([text_style])
    dataset.UnformattedTextValue = text_data
    return dataset

def get_displayed_area_selection(ds, referenced_image_sequence):
    dataset = Dataset()
    dataset.ReferencedImageSequence = referenced_image_sequence
    dataset.PixelOriginInterpretation = 'FRAME'
    dataset.DisplayedAreaTopLeftHandCorner = [1, 1]
    dataset.DisplayedAreaBottomRightHandCorner = [ds.Columns, ds.Rows]
    dataset.PresentationSizeMode = 'SCALE TO FIT'
    dataset.PresentationPixelSpacing = ds.PixelSpacing if 'PixelSpacing' in ds else [1, 1]
    return dataset

def get_graphic_object_dataset(
        graphic_data,
        line_style,
        fill_style=None,
        graphic_annotation_units='PIXEL',
        graphic_dimensions=2,
        graphic_type='POLYLINE',
        graphic_filled='N'
    ):
    assert graphic_annotation_units in ['PIXEL', 'DISPLAY', 'MATRIX']
    assert graphic_type in ['POINT', 'POLYLINE', 'INTERPOLATED', 'CIRCLE', 'ELLIPSE']
    assert graphic_filled in ['Y', 'N']
    dataset = Dataset()
    dataset.GraphicAnnotationUnits = graphic_annotation_units
    dataset.GraphicDimensions = graphic_dimensions
    dataset.NumberOfGraphicPoints = int(len(graphic_data) / graphic_dimensions)
    dataset.GraphicData = graphic_data
    dataset.GraphicType = graphic_type
    dataset.GraphicFilled = graphic_filled
    dataset.LineStyleSequence = Sequence([line_style])
    if fill_style:
        dataset.FillStyleSequence = Sequence([fill_style])
    return dataset


def get_VOI_LUT_dataset(
        input_dicom,
        referenced_image_sequence,
    ):
    dataset = Dataset()
    dataset.ReferencedImageSequence = referenced_image_sequence

    if input_dicom.__contains__('WindowWidth') and input_dicom.__contains__('WindowCenter'):
        dataset.WindowCenter = input_dicom.WindowCenter
        dataset.WindowWidth = input_dicom.WindowWidth
    elif input_dicom.__contains__('VOILUTSequence'):
        dataset.VOILUTSequence = input_dicom.VOILUTSequence
    else:
        raise KeyError
    
    return dataset
