import datetime
import json
import uuid
from typing import TYPE_CHECKING
import time

from .constants import BOX_ANNOTATION, OPERATION_TYPE_ANNOTATION, OPERATION_MODE_AUTO, META_UPDATE_REQUEST_BATCH_SIZE, \
    POLYGON_ANNOTATION, LINE_ANNOTATION
from .keys import IMAGES, IMAGE, ANNOTATIONS, BBOX, BOX_BOUNDARIES_AND_DIMENSIONS, X, Y, W, H, POINTS, LABEL, \
    LABEL_TEXT, REF, KEY, COLOR, ATTRIBUTE_VALUES, METADATA, TEXTS, TYPE, ID, SHAPE_ID, CREATED_AT, OBJECT_KEY, \
    ANNOTATION_OBJECTS, DATA, IS_USER_ANNOTATED, UPDATED_AT, LINE, POLYGON, CONFIDENCE
from .logger import get_debug_logger
from .label import Label

if TYPE_CHECKING:
    from . import DatalakeClient

annotation_logger = get_debug_logger('Annotation')


class Annotation:
    def __init__(self, client: "DatalakeClient"):
        self._client = client

    @staticmethod
    def format_bbox_annotation(annotation_object_input, annotation_object_output):
        if BBOX in annotation_object_input and len(annotation_object_input[BBOX]) == 4:
            x = annotation_object_input[BBOX][0]
            y = annotation_object_input[BBOX][1]
            width = annotation_object_input[BBOX][2]
            height = annotation_object_input[BBOX][3]

            annotation_object_output[BOX_BOUNDARIES_AND_DIMENSIONS] = {
                X: x,
                Y: y,
                W: width,
                H: height
            }
            annotation_object_output[POINTS] = [
                [x, y],
                [x + width, y],
                [x + width, y + height],
                [x, y + height]
            ]

    @staticmethod
    def format_line_annotation(annotation_object_input, annotation_object_output):
        if LINE in annotation_object_input:
            # calculate coordinates
            annotation_object_output[POINTS] = annotation_object_input[LINE]

    @staticmethod
    def format_polygon_annotation(annotation_object_input, annotation_object_output):
        if POLYGON in annotation_object_input:
            # calculate coordinates
            annotation_object_output[POINTS] = annotation_object_input[POLYGON]

    def upload_annotation_json(
            self,
            storage_base_path: str,
            operation_id: str,
            file_path: str,
            annotation_geometry: str,
            operation_mode: int,
            is_normalized: bool
    ):

        session_uuid = str(datetime.datetime.now().timestamp())

        # load json file
        f = open(file_path)
        annotation_data = json.load(f)
        f.close()

        # get labels,attributes,values in the json files as a dictionary
        label_attribute_values_dict = Label.get_label_attribute_values_dict(annotation_data)
        annotation_logger.debug('retrieving datalake label references started')
        label_references = self._client.datalake_interface.find_datalake_label_references(label_attribute_values_dict)
        annotation_logger.debug('retrieving datalake label references finished')

        # To make sure metadata is processed before annotations.
        # In case this method is called just after file upload
        time.sleep(90)

        # format data to call datalake operation data update API
        meta_updates_list = []
        request_batch_size = META_UPDATE_REQUEST_BATCH_SIZE
        total_images_count = len(annotation_data[IMAGES])
        uploaded_images_count = 0
        annotation_logger.debug(f'total images count with annotation data: {total_images_count}')

        for image in annotation_data[IMAGES]:
            if storage_base_path is None:
                object_key = f'{image[IMAGE]}'
            else:
                if storage_base_path.endswith('/'):
                    object_key = f'{storage_base_path}{image[IMAGE]}'
                else:
                    object_key = f'{storage_base_path}/{image[IMAGE]}'
            annotation_objects = []
            i = 1
            for annotation in image[ANNOTATIONS]:
                annotation_object = {}
                # calculate coordinates and other dimensions
                if annotation_geometry == BOX_ANNOTATION:
                    self.format_bbox_annotation(annotation, annotation_object)
                elif annotation_geometry == POLYGON_ANNOTATION:
                    self.format_polygon_annotation(annotation, annotation_object)
                elif annotation_geometry == LINE_ANNOTATION:
                    self.format_line_annotation(annotation, annotation_object)
                else:
                    break

                # assign annotation geometry type, ids, timestamps, confidence, etc.
                annotation_object_uuid = uuid.uuid4()
                annotation_object[ID] = f'shape_{annotation_object_uuid}'
                annotation_object[SHAPE_ID] = i
                i += 1
                annotation_object[CREATED_AT] = {'$date': str(datetime.datetime.now())}
                annotation_object[TYPE] = annotation_geometry
                if CONFIDENCE in annotation:
                    annotation_object[CONFIDENCE] = annotation[CONFIDENCE]

                try:
                    # assign label class
                    annotation_object[LABEL] = {
                        LABEL: label_references[annotation[LABEL]][REF],
                        LABEL_TEXT: annotation[LABEL],
                        KEY: label_references[annotation[LABEL]][REF],
                        COLOR: label_references[annotation[LABEL]][COLOR],
                        ATTRIBUTE_VALUES: {}
                    }
                    # assign label attribute and values
                    if METADATA in annotation:
                        for attr, val in annotation[METADATA].items():
                            try:
                                attr_ref = label_references[annotation[LABEL]][TEXTS][attr][REF]
                                val_ref = label_references[annotation[LABEL]][TEXTS][attr][TEXTS][val]
                                annotation_object[LABEL][ATTRIBUTE_VALUES][attr_ref] = val_ref
                            except (TypeError, KeyError, Exception) as te:
                                print(f"An Error Occurred at attribute value reference finding for object_key: "
                                      f"{object_key}", te)
                                continue

                    annotation_objects.append(annotation_object)
                except (TypeError, KeyError, Exception) as te:
                    print(f"An Error Occurred at label class reference finding for object_key: {object_key}", te)
                    continue

            meta_update_data = {
                ANNOTATION_OBJECTS: annotation_objects,
                IS_USER_ANNOTATED: False,
            }
            meta_updates = {
                OBJECT_KEY: object_key,
                DATA: meta_update_data
            }
            meta_updates_list.append(meta_updates)

            # call datalake operation data update API if batch size equals,
            # this is to reduce memory consumption & to stop request body size exceeding
            if len(meta_updates_list) == request_batch_size:
                uploaded_images_count = uploaded_images_count + len(meta_updates_list)
                annotation_logger.debug(f'uploading annotation data of batch size: {len(meta_updates_list)}')
                meta_update_response = self._client.datalake_interface.upload_metadata_updates(
                    meta_updates_list,
                    OPERATION_TYPE_ANNOTATION,
                    operation_mode,
                    operation_id,
                    is_normalized,
                    session_uuid,
                    total_images_count,
                    uploaded_images_count
                )
                annotation_logger.debug(f'annotation data uploaded images count: {uploaded_images_count}')

                meta_updates_list = []

        # call datalake operation data update API
        # this will handle final batch
        uploaded_images_count = uploaded_images_count + len(meta_updates_list)
        annotation_logger.debug(f'uploading annotation data of batch size: {len(meta_updates_list)}')
        meta_update_response = self._client.datalake_interface.upload_metadata_updates(
            meta_updates_list,
            OPERATION_TYPE_ANNOTATION,
            operation_mode,
            operation_id,
            is_normalized,
            session_uuid,
            total_images_count,
            uploaded_images_count
        )
        annotation_logger.debug(f'annotation data uploaded images count: {uploaded_images_count}')

    def remove_collection_annotations(self, collection_id, model_run_id):
        session_uuid = str(datetime.datetime.now().timestamp())
        meta_update_response = self._client.datalake_interface.remove_modelrun_collection_annotation(collection_id, model_run_id, session_uuid)
        print('delete annotation status: ',meta_update_response)
        return meta_update_response