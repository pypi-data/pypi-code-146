import os
import sys
import cv2
import json
import uuid
import base64
import pydicom
import numpy as np
from io import BytesIO
from pydicom.dataset import Dataset
from PIL import ImageFont, Image, ImageDraw
import medical_image
from medical_image.utils import *


def init_json():
    return {
            "Height": None,
            "Width": None,
            "GraphicAnnotationSequence": [
                # {
                #     "GraphicLayer": None,
                #     "TextObjectSequence": [],
                #     "GraphicObjectSequence": [],
                #     "Probability": None,
                #     "Heatmap": None
                # }
            ],
            "SCArray": None,
            "ReportArray": None,
            "ImageComments": None,
            "Skipping": False
    }


def init_json_3D():
    return {
            "GraphicAnnotationSequence": [
                # {
                #     "GraphicLayer": None,
                #     "Objects": [],
                #     "Probability": None,
                # }
            ],
            "SCArray": None,
            "ReportArray": None,
            "ImageComments": None
    }


def test_2D(result_json):
    assert result_json["Height"]
    return True


class DicomModule(object):
    def __init__(self, web_json):
        self.read_config(web_json)
        self.device = os.environ['DEVICE']
        self.gpu_index = os.environ['GPU_IDX']
        self.init_models()

        self.product_name = web_json["product_name"] if web_json["product_name"] else 'TEST'
        self.app_name = web_json["model_name"] if web_json["model_name"] else 'TEST'
        self.app_version = web_json["configurations"]["udi"]["udi_pi"] if web_json["configurations"]["udi"]["udi_pi"] else 'TEST'

        self.graphic_layer_sequence = [
            get_graphic_layer_dataset('Logo', 0),
            get_graphic_layer_dataset('No Finding', 1)
        ]

        self.logo = Image.open(os.path.join(medical_image.__path__[0], 'logo/deepnoid.png'))
        self.colorbar = Image.open(os.path.join(medical_image.__path__[0], 'logo/colorbar.png'))

    def read_config(self, web_json):
        self.web_json = web_json
        self.write_version = True
        if 'visualization' in web_json['models']:
            self.web_vis = web_json['models']['visualization']
            if '@write_version' in self.web_vis:
                if self.web_vis['@write_version']['selected'] == 'Off':
                    self.write_version = False
        else:
            self.web_vis = None
        if 'secondary_capture' in web_json['models']:
            self.web_sc = web_json['models']['secondary_capture']
        else:
            self.web_sc = None
        if 'report' in web_json['models']:
            self.web_report = web_json['models']['report']
        else:
            self.web_report = None
        if 'grayscale_softcopy_presentation_state' in web_json['models']:
            self.web_gsps = web_json['models']['grayscale_softcopy_presentation_state']
        else:
            self.web_gsps = None
            
    def init_models(self):
        raise NotImplementedError

    def run(self, web_json, input_path, output_path):
        self.read_config(web_json)

        scanned_studies = scan_directory(input_path)
        study_uids = [key for key in scanned_studies.keys()]

        print(study_uids, flush=True)
        if len(study_uids) > 1:
            print(len(study_uids), flush=True)
            raise AssertionError
        study_uid = study_uids[0]

        study_paths = scanned_studies[study_uid]
        series_uids = [key for key in study_paths.keys()]

        ds_init = pydicom.dcmread(study_paths[series_uids[0]][0], force=True)

        use_web_config = True
        if 'AI_REQUEST_TAG' in os.environ and os.environ['AI_REQUEST_TAG']:
            if os.environ['AI_REQUEST_TAG'] == 'Private3355':
                if (0x3355, 0x1002) in ds_init:
                    try:
                        req_types = ds_init[0x3355, 0x1002].value.split('::')[-1].split('&')
                        preferred_charsets = ds_init[0x3355, 0x1003].value.split('::')[-1]
                        use_web_config = False
                    except:
                        pass
            elif os.environ['AI_REQUEST_TAG'] == 'StudyComments':
                if (0x0032, 0x4000) in ds_init:
                    try:
                        _, req_types, preferred_charsets = ds_init.StudyComments.split('::')[2::2]
                        req_types = req_types.split('&')
                        use_web_config = False
                    except:
                        pass
            else:
                raise KeyError
        if use_web_config:
            req_types = []
            if self.web_sc and self.web_sc['@create']['selected'] == 'On':
                req_types.append('Secondary-Capture')
            if self.web_report and self.web_report['@create']['selected'] == 'On':
                req_types.append('Report')
            if self.web_gsps and self.web_gsps['@create']['selected'] == 'On':
                req_types.append('GSPS')
            preferred_charsets = ''

        self.preferred_charsets = preferred_charsets.split('\\')[-1]
        print("req_types:", req_types)
        print("preferred_charsets:", self.preferred_charsets)

        referenced_series_sequence = []
        displayed_area_selection_sequence = []
        graphic_annotation_sequence = []
        VOI_LUT_sequence = []
        finding_sequences = []
        conversion_source_attributes_sequence = []

        self.generated_uuid = uuid.uuid4().int
        for series_uid in series_uids:
            series_paths = study_paths[series_uid]
            referenced_image_sequence = []
            finding_sequence = []
            for path in series_paths:
                ds = pydicom.dcmread(str(path), force=True)
                result_json = self.run_models(ds)
                if not result_json['Skipping']:
                    referenced_image = get_referenced_image_dataset(ds)
                    referenced_image_sequence.append(referenced_image)
                    conversion_source_attributes_sequence.append(referenced_image)
                    displayed_area_selection_sequence.append(get_displayed_area_selection(ds, [referenced_image]))
                    VOI_LUT_sequence.append(get_VOI_LUT_dataset(ds, [referenced_image]))

                    finding_sequence += self.update_gsps(graphic_annotation_sequence, referenced_image, result_json)
                    self.add_logo_annotation(graphic_annotation_sequence, referenced_image, result_json)

                    if 'Secondary-Capture' in req_types:
                        self.make_sc_dcm(ds, result_json, output_path)

            if len(finding_sequence):
                finding_sequences += finding_sequence
                referenced_series_sequence.append(get_referenced_series_dataset(series_uid, referenced_image_sequence))

        if len(finding_sequences) and ('GSPS' in req_types):
            self.make_gsps_dcm(
                ds,
                finding_sequences,
                displayed_area_selection_sequence,
                graphic_annotation_sequence,
                referenced_series_sequence,
                conversion_source_attributes_sequence,
                VOI_LUT_sequence,
                output_path
            )

    def make_sc_dcm(self, ds, result_json, output_path):
        # assert (type(result_json['InputArray']) == np.ndarray) or type(result_json['SCArray']) == np.ndarray
        referenced_image = get_referenced_image_dataset(ds)

        ds_sc = make_dataset(ds, self.product_name, self.app_name, self.app_version, 'SC', self.generated_uuid, self.preferred_charsets)
        ds_sc.WindowCenter = 128
        ds_sc.WindowWidth = 255
        if '@append_series_number' in self.web_sc:
            if self.web_sc['@append_series_number']['selected'] == 'On':
                ds_sc.SeriesNumber = self.web_sc['series_number']['value'] + str(ds.SeriesNumber)
            else:
                ds_sc.SeriesNumber = self.web_sc['series_number']['value']
        else:
            ds_sc.SeriesNumber = self.web_sc['series_number']['value']

        assert result_json['Height'] == ds.Rows
        assert result_json['Width'] == ds.Columns
        if type(result_json["SCArray"]) == np.ndarray:
            sc_array = result_json["SCArray"]
        else:
            assert "InputArray" not in result_json
            assert result_json["SCArray"] == None
            result_json['InputArray'] = read_dcm(ds)
            sc_array = self.make_sc_array(result_json)
        ds_sc.PixelData = self.draw_logo(sc_array, result_json['Width'], result_json['Height']).tobytes()
            
        ds_sc.Rows = result_json["Height"]
        ds_sc.Columns = result_json["Width"]

        if len(result_json["GraphicAnnotationSequence"]):
            finding_sequence = []
            for graphic_annotation in result_json["GraphicAnnotationSequence"]:
                dataset = Dataset()
                dataset.add_new((0x2021, 0x0010), 'LO', 'DEEPNOID')
                dataset.add_new((0x2021, 0x1009), 'UT', json.dumps({
                    'Name': graphic_annotation['GraphicLayer'],
                    'Probability': float(graphic_annotation['Probability'])
                }))
                dataset.ReferencedImageSequence = [referenced_image]
                finding_sequence.append(dataset)
            finding_sequence = sorted(finding_sequence, key=lambda seq: json.loads(seq[0x2021, 0x1009].value)['Probability'], reverse=True)
        else:
            dataset = Dataset()
            dataset.add_new((0x2021, 0x0010), 'LO', 'DEEPNOID')
            dataset.add_new((0x2021, 0x1009), 'UT', json.dumps({
                'Name': 'No Finding',
                'Probability': 0.0000
            }))
            dataset.ReferencedImageSequence = [referenced_image]
            finding_sequence = [dataset]

        set_private_tags(ds_sc, finding_sequence, self.app_name, self.app_version)
        if type(result_json['ImageComments']) == str:
            ds_sc.ImageComments = result_json['ImageComments']
        ds_sc.save_as(str(output_path / (ds_sc.SOPInstanceUID + '.dcm')))
        print(str(output_path / (ds_sc.SOPInstanceUID + '.dcm')))

    def make_sc_array(self, result_json):
        sfont = ImageFont.truetype(os.path.join(medical_image.__path__[0], 'fonts/NotoSansCJKkr-Medium.otf'), int(result_json['Height'] / 90))
        image = Image.fromarray(result_json['InputArray'].astype(np.uint8))
        img_editable = ImageDraw.Draw(image)

        ## GraphicObject
        contour_image_array = np.array(image)
        for graphic_annotation in result_json["GraphicAnnotationSequence"]:
            heatmap_str = graphic_annotation['Heatmap']
            if heatmap_str != None:
                heatmap = np.array(Image.open(BytesIO(base64.b64decode(heatmap_str))))
                heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGRA2BGR)
                contour_image_array = cv2.addWeighted(contour_image_array, 1, heatmap, float(self.web_vis['opacity']['value']), 0)

            for graphic_object in graphic_annotation['GraphicObjectSequence']:
                graphic_data = np.array(graphic_object['graphic_data'], np.int32)
                line_color = graphic_object['color'] if 'color' in graphic_object else (255, 255, 255)
                if 'thickness' in graphic_object:
                    line_thickness = graphic_object['thickness']
                else:
                    line_thickness = max(int(min(result_json['Width'], result_json['Height']) / 500), 1)
                    
                if line_thickness == -1:
                    if 'fill_opacity' in graphic_object:
                        opacity = graphic_object['fill_opacity']
                    else:
                        opacity = 1.0
                    line_color += (int(255 * opacity),)

                    image = Image.fromarray(contour_image_array)
                    img_editable = ImageDraw.Draw(image, 'RGBA')
                    img_editable.polygon(
                        [tuple(g) for g in graphic_data],
                        fill=line_color
                    )
                    contour_image_array = np.array(image)
                else:
                    if ('shadow_color' not in graphic_object) or (graphic_object['shadow_color'] != 'OFF'):
                        shadow_color = graphic_object['shadow_color'] if 'shadow_color' in graphic_object else (0, 0, 0)
                        contour_image_array = cv2.polylines(contour_image_array, [graphic_data], False, shadow_color, int(line_thickness * 2.5))
                    contour_image_array = cv2.polylines(contour_image_array, [graphic_data], False, line_color, line_thickness)

        image = Image.fromarray(contour_image_array)
        img_editable = ImageDraw.Draw(image, 'RGBA')
        ## TextObject
        for graphic_annotation in result_json["GraphicAnnotationSequence"]:
            for text_object in graphic_annotation['TextObjectSequence']:
                if 'font_type' in text_object:
                    font_type = text_object['font_type']
                else:
                    font_type = 'Medium'
                if 'font_scale' in text_object:
                    font_scale = text_object['font_scale']
                else:
                    font_scale = int(result_json['Height'] / 70)

                font = ImageFont.truetype(os.path.join(medical_image.__path__[0], f'fonts/NotoSansCJKkr-{font_type}.otf'), font_scale)
                text_color = text_object['color'] if 'color' in text_object else (255, 255, 255)
                msg = text_object['text_data']
                x, y, w, h = text_object['bbox']
                if ('shadow_color' not in text_object) or (text_object['shadow_color'] != 'OFF'):
                    mw, mh = font.getsize(msg)
                    shadow = int(mh / 20)
                    shadow_color = text_object['shadow_color'] if 'shadow_color' in text_object else (167, 167, 167)
                    img_editable.text((x + shadow, y + shadow), msg, shadow_color, font)
                img_editable.text((x, y), msg, text_color, font)

        ## Colorbar
        heatmaps = [g['Heatmap'] for g in result_json["GraphicAnnotationSequence"]]
        # if len(heatmaps) != heatmaps.count(""):
        if len(heatmaps) != heatmaps.count(None):
            w, h = self.colorbar.size
            w *= result_json['Height'] * 0.4 / 2472 * 1000 / 1757
            h *= result_json['Height'] * 0.4 / 2472 * 1000 / 1757
            x = result_json['Width'] * 0.03
            y = result_json['Height'] * 0.985 - h
            paste_image(image, self.colorbar, x, y, w, h, 1)
            hw, hh = sfont.getsize('High')
            img_editable.text((x, y - hh), 'Low', (255, 255, 255), sfont)
            img_editable.text((x + w - hw, y - hh), 'High', (255, 255, 255), sfont)
        
        return np.array(image)

    def draw_logo(self, arr, width, height):
        mfont = ImageFont.truetype(os.path.join(medical_image.__path__[0], 'fonts/NotoSansCJKkr-Medium.otf'), int(height / 70))
        lfont = ImageFont.truetype(os.path.join(medical_image.__path__[0], 'fonts/NotoSansCJKkr-Medium.otf'), int(height / 50))

        image = Image.fromarray(arr.astype(np.uint8))
        img_editable = ImageDraw.Draw(image, 'RGBA')

        msg = self.product_name
        if 'logo' in self.web_json:
            web_logo = self.web_json['logo']
            if "background_color" not in web_logo:
                web_logo["background_color"] = [0, 0, 0, 153]
        else:
            web_logo = {
                "location": "PREVIOUS",
                "background": "Off",
                "background_color": [0, 0, 0, 153],
                "write_version": self.write_version
            }
        if web_logo['write_version']:
            msg += ' v' + self.app_version

        if web_logo['location'] == 'PREVIOUS':
            logo_w = self.logo.size[0] * height * 0.55 / 2472
            logo_h = self.logo.size[1] * height * 0.55 / 2472
            logo_x = (width - logo_w) / 2
            logo_y = height * 0.945 - logo_h

            font = lfont
            mw, mh = font.getsize(msg)
            shadow = int(mh / 20)
            mx = (width - mw) / 2
            my = logo_y - mh
        else:
            font = mfont
            mw, mh = font.getsize(msg)
            shadow = int(mh / 20)
            logo_w = mw
            logo_h = self.logo.size[1] * mw / self.logo.size[0]
            if web_logo['location'] == 'RU':
                logo_x = width - logo_w
                logo_y = 0
            elif web_logo['location'] == 'MU':
                logo_x = (width - logo_w) / 2
                logo_y = 0
            elif web_logo['location'] == 'ML':
                logo_x = (width - logo_w) / 2
                logo_y = height * 0.999 - logo_h - mh
            else:
                raise NotImplementedError
            mx = logo_x
            my = logo_y + logo_h
            w = mw
            
        h = logo_h + mh

        if web_logo["background"] == "On":
            if web_logo['location'] == 'PREVIOUS':
                if logo_w > mw:
                    x = logo_x
                    w = logo_w
                else:
                    x = mx
                    w = mw
                y = my
                graphic_data = np.array([
                    [x-w*0.025, y-h*0.025],
                    [x-w*0.025, y+h*1.025],
                    [x+w*1.025, y+h*1.025],
                    [x+w*1.025, y-h*0.025]
                ])
            else:
                x = logo_x
                y = logo_y
                if web_logo['location'] == 'RU':
                    graphic_data = np.array([
                        [x-w*0.025, y],
                        [x-w*0.025, y+h*1.1],
                        [x+w, y+h*1.1],
                        [x+w, y]
                    ])
                elif web_logo['location'] == 'MU':
                    graphic_data = np.array([
                        [x-w*0.025, y],
                        [x-w*0.025, y+h*1.1],
                        [x+w*1.025, y+h*1.1],
                        [x+w*1.025, y]
                    ])
                elif web_logo['location'] == 'ML':
                    graphic_data = np.array([
                        [x-w*0.025, y-h*0.1],
                        [x-w*0.025, y+h],
                        [x+w*1.025, y+h],
                        [x+w*1.025, y-h*0.1]
                    ])
                else:
                    raise NotImplementedError
            img_editable.polygon(
                [tuple(g) for g in graphic_data],
                fill=tuple(web_logo["background_color"])
            )
        paste_image(image, self.logo, logo_x, logo_y, logo_w, logo_h, 1)
        img_editable.text((mx + shadow, my + shadow), msg, (167, 167, 167), font)
        img_editable.text((mx, my), msg, (255, 255, 255), font)
        return np.array(image)

    def update_gsps(self, graphic_annotation_sequence, referenced_image, result_json):
        def get_text_object_dcm(text_objects):
            text_object_sequence = []
            for text_object in text_objects:
                text_color = text_object['color'] if 'color' in text_object else [255, 255, 255]
                if 'shadow_color' not in text_object:
                    text_style = get_text_style_dataset(
                        color=text_color,
                        shadow_style='NORMAL',
                        shadow_color=[167, 167, 167],
                        shadow_offset=[int((text_object['bbox'][3] - text_object['bbox'][1]) / 20)] * 2
                    )
                elif text_object['shadow_color'] == 'OFF':
                    text_style = get_text_style_dataset(
                        color=text_color,
                        shadow_style='OFF'
                    )
                else:
                    text_style = get_text_style_dataset(
                        color=text_color,
                        shadow_style='NORMAL',
                        shadow_color=text_object['shadow_color'],
                        shadow_offset=[int((text_object['bbox'][3] - text_object['bbox'][1]) / 20)] * 2
                    )
                text_object_sequence.append(
                    get_text_object_dataset(
                        text_data=text_object["text_data"],
                        text_style=text_style,
                        bbox=text_object["bbox"]
                    )
                )
            return text_object_sequence

        def get_graphic_object_dcm(graphic_objects):
            graphic_object_sequence = []
            for graphic_object in graphic_objects:
                line_color = graphic_object['color'] if 'color' in graphic_object else [255, 255, 255]
                if 'shadow_color' not in graphic_object:
                    line_style = get_line_style_dataset(
                        color=line_color,
                        thickness=3.0,
                        shadow_style='OUTLINED',
                        shadow_color=[0, 0, 0],
                        shadow_offset=[6, 6]
                    )
                elif graphic_object['shadow_color'] == 'OFF':
                    line_style = get_line_style_dataset(
                        color=line_color,
                        thickness=3.0,
                        shadow_style='OFF'
                    )
                else:
                    line_style = get_line_style_dataset(
                        color=line_color,
                        thickness=3.0,
                        shadow_style='OUTLINED',
                        shadow_color=graphic_object['shadow_color'],
                        shadow_offset=[6, 6]
                    )
                graphic_object_sequence.append(
                    get_graphic_object_dataset(
                        graphic_data=list(graphic_object["graphic_data"].ravel()),
                        line_style=line_style
                    )
                )
            return graphic_object_sequence

        if len(result_json["GraphicAnnotationSequence"]):
            finding_sequence = []
            for graphic_annotation in result_json["GraphicAnnotationSequence"]:
                graphic_annotation_sequence.append(
                    get_graphic_annotation_dataset(
                        referenced_image_sequence=[referenced_image],
                        layer_name=graphic_annotation['GraphicLayer'],
                        text_object_sequence=get_text_object_dcm(graphic_annotation["TextObjectSequence"]),
                        graphic_object_sequence=get_graphic_object_dcm(graphic_annotation["GraphicObjectSequence"])
                    )
                )
                dataset = Dataset()
                dataset.add_new((0x2021, 0x0010), 'LO', 'DEEPNOID')
                if graphic_annotation['Heatmap'] == None:
                    heatmap_str = encoding_heatmap(np.zeros([result_json['Height'], result_json['Width']]), 0.5)
                    opacity = 0.5
                else:
                    heatmap_str = graphic_annotation['Heatmap']
                    opacity = self.web_vis['opacity']['value']
                dataset.add_new((0x2021, 0x1009), 'UT', json.dumps({
                    'Name': graphic_annotation['GraphicLayer'],
                    'Probability': float(graphic_annotation['Probability']),
                    'Heatmap': heatmap_str,
                    'BlendingRatio': float(opacity)
                }))
                dataset.ReferencedImageSequence = [referenced_image]
                finding_sequence.append(dataset)

        else:
            dataset = Dataset()
            dataset.add_new((0x2021, 0x0010), 'LO', 'DEEPNOID')
            dataset.add_new((0x2021, 0x1009), 'UT', json.dumps({
                'Name': 'No Finding',
                'Probability': 0.0000,
                'Heatmap': encoding_heatmap(np.zeros([result_json['Height'], result_json['Width']]), 0.5),
                'BlendingRatio': float(0.5)
            }))
            dataset.ReferencedImageSequence = [referenced_image]
            finding_sequence = [dataset]
        return finding_sequence

    def add_logo_object(self, text_object_sequence, result_json):
        mfont = ImageFont.truetype(os.path.join(medical_image.__path__[0], 'fonts/NotoSansCJKkr-Medium.otf'), int(result_json['Height'] / 50))
        ## Logo
        msg = 'D E E P N O I D'
        w0, h0 = mfont.getsize(msg)
        x = (result_json['Width'] - w0) / 2
        y = result_json['Height'] * 0.97 - h0
        shadow = int(h0 / 20)
        text_style = get_text_style_dataset(
            color=[255, 255, 255],
            shadow_style='NORMAL',
            shadow_color=[255, 255, 255],
            shadow_offset=[shadow, shadow],
        )
        text_object_sequence.append(
            get_text_object_dataset(
                text_data=msg,
                text_style=text_style,
                bbox=[x, y, x + w0, y + h0]
            )
        )

        ## App
        msg = self.product_name
        if self.write_version:
            msg += ' v.' + self.app_version
        w1, h1 = mfont.getsize(msg)
        x = (result_json['Width'] - w1) / 2
        y = result_json['Height'] * 0.965 - h0 - h1
        shadow = int(h1 / 20)
        text_style = get_text_style_dataset(
            color=[255, 255, 255],
            shadow_style='NORMAL',
            shadow_color=[255, 255, 255],
            shadow_offset=[shadow, shadow],
        )
        text_object_sequence.append(
            get_text_object_dataset(
                text_data=msg,
                text_style=text_style,
                bbox=[x, y, x + w1, y + h1]
            )
        )

    def add_logo_annotation(self, graphic_annotation_sequence, referenced_image, result_json):
        text_object_sequence = []
        self.add_logo_object(text_object_sequence, result_json)
        graphic_annotation = get_graphic_annotation_dataset(
            referenced_image_sequence=[referenced_image],
            layer_name='Logo',
            text_object_sequence=text_object_sequence,
            graphic_object_sequence=[]
        )
        graphic_annotation_sequence.append(graphic_annotation)

    def make_gsps_dcm(
        self,
        ds,
        finding_sequences,
        displayed_area_selection_sequence,
        graphic_annotation_sequence,
        referenced_series_sequence,
        conversion_source_attributes_sequence,
        VOI_LUT_sequence,
        output_path
        ):
        ds_gsps = make_dataset(ds, self.product_name, self.app_name, self.app_version, 'GSPS', self.generated_uuid, self.preferred_charsets)
        if '@append_series_number' in self.web_gsps:
            if self.web_gsps['@append_series_number']['selected'] == 'On':
                ds_gsps.SeriesNumber = self.web_gsps['series_number']['value'] + str(ds.SeriesNumber)
            else:
                ds_gsps.SeriesNumber = self.web_gsps['series_number']['value']
        else:
            ds_gsps.SeriesNumber = self.web_gsps['series_number']['value']
        ds_gsps.GraphicLayerSequence = self.graphic_layer_sequence

        if len(finding_sequences):
            finding_sequences = sorted(finding_sequences, key=lambda seq: json.loads(seq[0x2021, 0x1009].value)['Probability'], reverse=True)

        if ds.PhotometricInterpretation == 'MONOCHROME1':
            ds_gsps.PresentationLUTShape = 'INVERSE'

        set_private_tags(ds_gsps, finding_sequences, self.app_name, self.app_version)
        ds_gsps.DisplayedAreaSelectionSequence = displayed_area_selection_sequence
        ds_gsps.GraphicAnnotationSequence = graphic_annotation_sequence
        ds_gsps.ReferencedSeriesSequence = referenced_series_sequence
        ds_gsps.ConversionSourceAttributesSequence = conversion_source_attributes_sequence
        ds_gsps.SoftcopyVOILUTSequence = VOI_LUT_sequence

        ds_gsps.save_as(str(output_path / 'gsps.dcm'))
        print(str(output_path / 'gsps.dcm'))


class DicomModule3D(object):
    def __init__(self, web_json):
        self.read_config(web_json)
        self.device = os.environ['DEVICE']
        self.gpu_index = os.environ['GPU_IDX']
        self.init_models()

        self.product_name = web_json["product_name"] if web_json["product_name"] else 'TEST'
        self.app_name = web_json["model_name"] if web_json["model_name"] else 'TEST'
        self.app_version = web_json["configurations"]["udi"]["udi_pi"] if web_json["configurations"]["udi"]["udi_pi"] else 'TEST'

        self.graphic_layer_sequence = [
            get_graphic_layer_dataset('Logo', 0),
            get_graphic_layer_dataset('No Finding', 1)
        ]

        self.logo = Image.open(os.path.join(medical_image.__path__[0], 'logo/deepnoid.png'))
        self.colorbar = Image.open(os.path.join(medical_image.__path__[0], 'logo/colorbar.png'))

    def read_config(self, web_json):
        self.web_json = web_json
        self.write_version = True
        if 'visualization' in web_json['models']:
            self.web_vis = web_json['models']['visualization']
            if '@write_version' in self.web_vis:
                if self.web_vis['@write_version']['selected'] == 'Off':
                    self.write_version = False
        else:
            self.web_vis = None
        if 'secondary_capture' in web_json['models']:
            self.web_sc = web_json['models']['secondary_capture']
        else:
            self.web_sc = None
        if 'report' in web_json['models']:
            self.web_report = web_json['models']['report']
        else:
            self.web_report = None
        # TODO 나중에 3D에서도 GSPS 적용할 수 있도록 수정
        if 'grayscale_softcopy_presentation_state' in web_json['models']:
            self.web_gsps = web_json['models']['grayscale_softcopy_presentation_state']
        else:
            self.web_gsps = None
            
    def init_models(self):
        raise NotImplementedError

    def run(self, web_json, input_path, output_path):
        self.read_config(web_json)
        if (self.device != os.environ['DEVICE']) or (self.gpu_index != os.environ['GPU_IDX']):
            print('Configuration of Device has been changed. Reload model.', flush=True)
            self.__delattr__('models')
            self.device = os.environ['DEVICE']
            self.gpu_index = os.environ['GPU_IDX']
            self.init_models()

        scanned_studies = scan_directory(input_path)
        study_uids = [key for key in scanned_studies.keys()]

        print(study_uids, flush=True)
        if len(study_uids) > 1:
            print(len(study_uids), flush=True)
            raise AssertionError
        study_uid = study_uids[0]

        study_paths = scanned_studies[study_uid]
        series_uids = [key for key in study_paths.keys()]

        ds_init = pydicom.dcmread(study_paths[series_uids[0]][0], force=True)

        use_web_config = True
        if 'AI_REQUEST_TAG' in os.environ and os.environ['AI_REQUEST_TAG']:
            if os.environ['AI_REQUEST_TAG'] == 'Private3355':
                if (0x3355, 0x1002) in ds_init:
                    try:
                        req_types = ds_init[0x3355, 0x1002].value.split('::')[-1].split('&')
                        preferred_charsets = ds_init[0x3355, 0x1003].value.split('::')[-1]
                        use_web_config = False
                    except:
                        pass
            elif os.environ['AI_REQUEST_TAG'] == 'StudyComments':
                if (0x0032, 0x4000) in ds_init:
                    try:
                        _, req_types, preferred_charsets = ds_init.StudyComments.split('::')[2::2]
                        req_types = req_types.split('&')
                        use_web_config = False
                    except:
                        pass
            else:
                raise KeyError
        if use_web_config:
            req_types = []
            if self.web_sc and self.web_sc['@create']['selected'] == 'On':
                req_types.append('Secondary-Capture')
            if self.web_report and self.web_report['@create']['selected'] == 'On':
                req_types.append('Report')
            if self.web_gsps and self.web_gsps['@create']['selected'] == 'On':
                req_types.append('GSPS')
            preferred_charsets = ''

        if 'GSPS' in req_types:
            # TODO 나중에 3D에서도 GSPS 적용할 수 있도록 수정
            raise NotImplementedError

        self.preferred_charsets = preferred_charsets.split('\\')[-1]
        print("req_types:", req_types)
        print("preferred_charsets:", self.preferred_charsets)

        referenced_series_sequence = []
        displayed_area_selection_sequence = []
        graphic_annotation_sequence = []
        VOI_LUT_sequence = []
        finding_sequences = []
        conversion_source_attributes_sequence = []

        self.generated_uuid = uuid.uuid4().int
        for series_uid in series_uids:
            series_paths = study_paths[series_uid]
            referenced_image_sequence = []
            finding_sequence = []
            ds_dict = {'path': series_paths[0].parent}
            for path in series_paths:
                ds = pydicom.dcmread(str(path), force=True)
                ds_dict[int(ds.InstanceNumber)] = ds

                referenced_image = get_referenced_image_dataset(ds)
                referenced_image_sequence.append(referenced_image)
                conversion_source_attributes_sequence.append(referenced_image)
                displayed_area_selection_sequence.append(get_displayed_area_selection(ds, [referenced_image]))
                VOI_LUT_sequence.append(get_VOI_LUT_dataset(ds, [referenced_image]))

                # finding_sequence = self.update_gsps(graphic_annotation_sequence, referenced_image, result_json)
                # self.add_logo_annotation(graphic_annotation_sequence, referenced_image, result_json)


            # finding_sequences += finding_sequence
            # referenced_series_sequence.append(get_referenced_series_dataset(series_uid, referenced_image_sequence))

            result_json = self.run_models(ds_dict)
            
            if 'Secondary-Capture' in req_types:
                self.make_sc_dcm(ds_dict, result_json, output_path)
            if 'Report' in req_types:
                report_array = result_json['ReportArray']
                if type(report_array) == list:  # 2 페이지 이상의 Report
                    for i,report_page_array in enumerate(report_array):
                        ds_i  = copy.deepcopy(ds)
                        ds_i.InstanceNumber = i+1
                        ds_rp = make_dataset(ds_i, self.product_name, self.app_name, self.app_version, 'RP', self.generated_uuid, self.preferred_charsets)
                        ds_rp.PixelData = report_page_array.tobytes()
                        ds_rp.Rows = report_page_array.shape[0]
                        ds_rp.Columns = report_page_array.shape[1]
                        ds_rp.save_as(str(output_path / (ds_rp.SOPInstanceUID + '.dcm')))
                elif type(report_array) == np.ndarray:
                    ds_rp = make_dataset(ds, self.product_name, self.app_name, self.app_version, 'RP', self.generated_uuid, self.preferred_charsets)
                    ds_rp.PixelData = report_array.tobytes()
                    ds_rp.Rows = report_array.shape[0]
                    ds_rp.Columns = report_array.shape[1]
                    ds_rp.save_as(str(output_path / (ds_rp.SOPInstanceUID + '.dcm')))
                else:
                    print('report array has wrong type : {}'.format(type(report_array)))
                    break

        if 'GSPS' in req_types:
            # TODO 나중에 3D에서도 GSPS 적용할 수 있도록 수정
            raise NotImplementedError

    def make_sc_dcm(self, ds_dict, result_json, output_path):
        # assert (type(result_json['InputArray']) == np.ndarray) or type(result_json['SCArray']) == np.ndarray
        instance_numbers = sorted([key for key in ds_dict.keys() if type(key) == int])
        if type(result_json["SCArray"]) == np.ndarray:
            result_sc_array = result_json["SCArray"]
            assert len(result_sc_array) == len(instance_numbers)

        object_numbers = {}
        for i, graphic_annotation in enumerate(result_json["GraphicAnnotationSequence"]):
            objects = graphic_annotation['Objects']
            _ins = [obj['instance_number'] for obj in objects]
            for _in in _ins:
                if _in in object_numbers:
                    object_numbers[_in][i] = _ins.index(_in)
                else:
                    object_numbers[_in] = {i: _ins.index(_in)}

        for j, instance_number in enumerate(instance_numbers):
            ds = ds_dict[instance_number]
            referenced_image = get_referenced_image_dataset(ds)

            ds_sc = make_dataset(ds, self.product_name, self.app_name, self.app_version, 'SC', self.generated_uuid, self.preferred_charsets)
            ds_sc.WindowCenter = 128
            ds_sc.WindowWidth = 255
            if '@append_series_number' in self.web_sc:
                if self.web_sc['@append_series_number']['selected'] == 'On':
                    ds_sc.SeriesNumber = self.web_sc['series_number']['value'] + str(ds.SeriesNumber)
                else:
                    ds_sc.SeriesNumber = self.web_sc['series_number']['value']
            else:
                ds_sc.SeriesNumber = self.web_sc['series_number']['value']

            objects = []
            if instance_number in object_numbers:
                for i in object_numbers[instance_number]:
                    objects.append(result_json["GraphicAnnotationSequence"][i]["Objects"][object_numbers[instance_number][i]])
            if type(result_json["SCArray"]) == np.ndarray:
                sc_array = result_json["SCArray"][j]
                width = int(ds.Columns)
                height = int(ds.Rows)
            else:
                sc_array, width, height = self.make_sc_array(ds, objects)
            ds_sc.PixelData = self.draw_logo(sc_array, width, height).tobytes()

            if len(objects):
                ds_sc.Rows = objects[0]['Height']
                ds_sc.Columns = objects[0]['Width']
            else:
                ds_sc.Rows = int(ds.Rows)
                ds_sc.Columns = int(ds.Columns)

            if len(result_json["GraphicAnnotationSequence"]):
                finding_sequence = []
                for i, graphic_annotation in enumerate(result_json["GraphicAnnotationSequence"]):
                    dataset = Dataset()
                    dataset.add_new((0x2021, 0x0010), 'LO', 'DEEPNOID')
                    dataset.add_new((0x2021, 0x1009), 'UT', json.dumps({
                        'Name': graphic_annotation['GraphicLayer'],
                        'Probability': float(graphic_annotation['Probability'])
                    }))
                    dataset.ReferencedImageSequence = [referenced_image]
                    finding_sequence.append(dataset)
                finding_sequence = sorted(finding_sequence, key=lambda seq: json.loads(seq[0x2021, 0x1009].value)['Probability'], reverse=True)
            else:
                dataset = Dataset()
                dataset.add_new((0x2021, 0x0010), 'LO', 'DEEPNOID')
                dataset.add_new((0x2021, 0x1009), 'UT', json.dumps({
                    'Name': 'No Finding',
                    'Probability': 0.0000
                }))
                dataset.ReferencedImageSequence = [referenced_image]
                finding_sequence = [dataset]

            set_private_tags(ds_sc, finding_sequence, self.app_name, self.app_version)
            if type(result_json['ImageComments']) == str:
                ds_sc.ImageComments = result_json['ImageComments']
            ds_sc.save_as(str(output_path / (ds_sc.SOPInstanceUID + '.dcm')))
            # print(str(output_path / (ds_sc.SOPInstanceUID + '.dcm')))

    def update_gsps(self, *args, **kwargs):
        raise NotImplementedError

    def make_sc_array(self, ds, objects):
        if len(objects):
            height = objects[0]['Height']
            width = objects[0]['Width']
        else:
            height = int(ds.Rows)
            width = int(ds.Columns)
        mfont = ImageFont.truetype(os.path.join(medical_image.__path__[0], 'fonts/NotoSansCJKkr-Medium.otf'), int(height / 50))
        image = Image.fromarray(read_dcm(ds).astype(np.uint8))
        img_editable = ImageDraw.Draw(image)

        for obj in objects:
            ## GraphicObject
            contour_image_array = np.array(image)
            for graphic_object in obj['GraphicObjectSequence']:
                graphic_data = np.array(graphic_object['graphic_data'], np.int32)
                line_color = graphic_object['color'] if 'color' in graphic_object else (255, 255, 255)
                if 'thickness' in graphic_object:
                    line_thickness = graphic_object['thickness']
                else:
                    line_thickness = max(int(min(width, height) / 500), 1)

                if line_thickness == -1:
                    if 'fill_opacity' in graphic_object:
                        opacity = graphic_object['fill_opacity']
                    else:
                        opacity = 1.0
                    line_color += (int(255 * opacity),)

                    image = Image.fromarray(contour_image_array)
                    img_editable = ImageDraw.Draw(image, 'RGBA')
                    img_editable.polygon(
                        [tuple(g) for g in graphic_data],
                        fill=line_color
                    )
                    contour_image_array = np.array(image)
                else:
                    if ('shadow_color' not in graphic_object) or (graphic_object['shadow_color'] != 'OFF'):
                        shadow_color = graphic_object['shadow_color'] if 'shadow_color' in graphic_object else (0, 0, 0)
                        contour_image_array = cv2.polylines(contour_image_array, [graphic_data], False, shadow_color, 10)
                    contour_image_array = cv2.polylines(contour_image_array, [graphic_data], False, line_color, max(int(min(width, height) / 500), 1))


            image = Image.fromarray(contour_image_array)
            img_editable = ImageDraw.Draw(image)
            ## TextObject
            for text_object in obj['TextObjectSequence']:
                if 'font_type' in text_object:
                    font_type = text_object['font_type']
                else:
                    font_type = 'Medium'
                if 'font_scale' in text_object:
                    font_scale = text_object['font_scale']
                else:
                    font_scale = int(height / 70)

                font = ImageFont.truetype(os.path.join(medical_image.__path__[0], f'fonts/NotoSansCJKkr-{font_type}.otf'), font_scale)

                text_color = text_object['color'] if 'color' in text_object else (255, 255, 255)
                msg = text_object['text_data']
                x, y, _, _ = text_object['bbox']
                if ('shadow_color' not in text_object) or (text_object['shadow_color'] != 'OFF'):
                    mw, mh = font.getsize(msg)
                    shadow = int(mh / 20)
                    shadow_color = text_object['shadow_color'] if 'shadow_color' in text_object else (167, 167, 167)
                    img_editable.text((x + shadow, y + shadow), msg, shadow_color, font)
                img_editable.text((x, y), msg, text_color, font)

        return np.array(image), width, height

    def draw_logo(self, arr, width, height):
        image = Image.fromarray(arr.astype(np.uint8))
        img_editable = ImageDraw.Draw(image)

        ## Logo
        logo_w = self.logo.size[0] * height * 0.55 / 2472
        logo_h = self.logo.size[1] * height * 0.55 / 2472
        x = (width - logo_w) / 2
        y = height * 0.945 - logo_h
        paste_image(image, self.logo, x, y, logo_w, logo_h, 1)

        ## App Info
        msg = self.product_name
        if self.write_version:
            msg += ' v' + self.app_version
        mfont = ImageFont.truetype(os.path.join(medical_image.__path__[0], 'fonts/NotoSansCJKkr-Medium.otf'), int(height / 50))
        mw, mh = mfont.getsize(msg)
        x = (width - mw) / 2
        y = height * 0.940 - logo_h - mh
        shadow = int(mh / 20)
        img_editable.text((x + shadow, y + shadow), msg, (167, 167, 167), mfont)
        img_editable.text((x, y), msg, (255, 255, 255), mfont)
        
        return np.array(image)

    def add_logo_object(self, text_object_sequence, result_json):
        mfont = ImageFont.truetype(os.path.join(medical_image.__path__[0], 'fonts/NotoSansCJKkr-Medium.otf'), int(result_json['Height'] / 50))
        ## Logo
        msg = 'D E E P N O I D'
        w0, h0 = mfont.getsize(msg)
        x = (result_json['Width'] - w0) / 2
        y = result_json['Height'] * 0.945 - h0
        shadow = int(h0 / 20)
        text_style = get_text_style_dataset(
            color=[255, 255, 255],
            shadow_style='NORMAL',
            shadow_color=[255, 255, 255],
            shadow_offset=[shadow, shadow],
        )
        text_object_sequence.append(
            get_text_object_dataset(
                text_data=msg,
                text_style=text_style,
                bbox=[x, y, x + w0, y + h0]
            )
        )

        ## App
        msg = self.product_name
        if self.write_version:
            msg += ' v.' + self.app_version
        w1, h1 = mfont.getsize(msg)
        x = (result_json['Width'] - w1) / 2
        y = result_json['Height'] * 0.940 - h0 - h1
        shadow = int(h1 / 20)
        text_style = get_text_style_dataset(
            color=[255, 255, 255],
            shadow_style='NORMAL',
            shadow_color=[255, 255, 255],
            shadow_offset=[shadow, shadow],
        )
        text_object_sequence.append(
            get_text_object_dataset(
                text_data=msg,
                text_style=text_style,
                bbox=[x, y, x + w1, y + h1]
            )
        )

    def add_logo_annotation(self, graphic_annotation_sequence, referenced_image, result_json):
        text_object_sequence = []
        self.add_logo_object(text_object_sequence, result_json)
        graphic_annotation = get_graphic_annotation_dataset(
            referenced_image_sequence=[referenced_image],
            layer_name='Logo',
            text_object_sequence=text_object_sequence,
            graphic_object_sequence=[]
        )
        graphic_annotation_sequence.append(graphic_annotation)

    def make_gsps_dcm(self, *args,**kwargs):
        raise NotImplementedError
