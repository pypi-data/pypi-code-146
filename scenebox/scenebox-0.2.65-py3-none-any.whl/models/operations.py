from abc import ABC, abstractmethod
from typing import Optional, List, Union, NamedTuple, Any, Dict

from .annotation import Annotation, BoundingBoxAnnotation, PolygonAnnotation, PointAnnotation, LineAnnotation, \
    SegmentationAnnotation
from ..clients import SceneEngineClient
from ..constants import AssetsConstants, JobConstants, AnnotationGroups, AnnotationTypes
from ..custom_exceptions import OperationError
from ..tools.logger import get_logger
from ..tools.misc import get_md5_from_string

logger = get_logger(__name__)


class ParameterDataType:
    INT = "int"
    FLOAT = "float"
    STR = "str"
    BOOL = "bool"
    DICT = "dict"
    LIST_FLOAT = "list_float"
    LIST_INT = "list_int"
    LIST_STR = "list_str"


class BaseParameter:
    def __init__(self, field_name: str, field_data_type: str):
        self.field_name = field_name
        self.field_data_type = field_data_type

    def _validate_datatype(self, value):
        if self.field_data_type == ParameterDataType.INT:
            assert isinstance(value, int)
        elif self.field_data_type == ParameterDataType.FLOAT:
            assert isinstance(value, float)
        elif self.field_data_type == ParameterDataType.STR:
            assert isinstance(value, str)
        elif self.field_data_type == ParameterDataType.BOOL:
            assert isinstance(value, bool)
        elif self.field_data_type == ParameterDataType.DICT:
            assert isinstance(value, dict)
        elif self.field_data_type == ParameterDataType.LIST_FLOAT:
            assert isinstance(value, list)
            for item in value:
                assert isinstance(item, float)
        elif self.field_data_type == ParameterDataType.LIST_INT:
            assert isinstance(value, list)
            for item in value:
                assert isinstance(item, int)
        elif self.field_data_type == ParameterDataType.LIST_STR:
            assert isinstance(value, list)
            for item in value:
                assert isinstance(item, str)
        else:
            raise ValueError("Invalid data type definition for parameter {}".format(self.field_name))

    def as_dict(self):
        return self.__dict__


class RangeParameter(BaseParameter):
    def __init__(self,
                 field_name: str,
                 field_data_type: str,
                 min_value: Union[float, int],
                 max_value: Union[float, int],
                 default_value: Optional[Union[float, int]] = None):

        # UI is created as a slider
        super().__init__(field_name=field_name, field_data_type=field_data_type)
        self.min_value = min_value
        self.max_value = max_value
        self.default_value = default_value
        self.parameter_type = "range_parameter"

    def validate(self, value):

        assert value is not None
        self._validate_datatype(value)
        assert self.min_value <= value <= self.max_value, \
            "Incorrect value for {}. Must be in range [{}, {}]".format(
                self.field_name, self.min_value, self.max_value)


class FieldValueParameter(BaseParameter):
    # If values are provided, UI is a one-of-many choice
    # If not, this is a value input from the user
    def __init__(self,
                 field_name: str,
                 field_data_type: str,
                 values: Optional[List[Union[int, str]]] = None,
                 default_value: Optional[Union[float, int, str, List[float], List[int], List[str]]] = None):

        super().__init__(field_name=field_name, field_data_type=field_data_type)
        self.values = values
        self.default_value = default_value
        self.parameter_type = "field_value_parameter"

    def validate(self, value):
        self._validate_datatype(value)
        if self.values:
            if isinstance(value, list):
                for item in value:
                    assert item in self.values, \
                        "Invalid value for {}. Choose one of {}".format(self.field_name, self.values)
            else:
                assert value in self.values, \
                    "Invalid value for {}. Choose one of {}".format(self.field_name, self.values)


class RawParameter(BaseParameter):
    # For parameters that are read as json or dictionaries
    def __init__(self,
                 field_name: str,
                 default_value: Optional[dict] = None):

        super().__init__(field_name=field_name, field_data_type=ParameterDataType.DICT)
        self.default_value = default_value
        self.parameter_type = "raw_parameter"

    def validate(self, value):
        self._validate_datatype(value)


class BooleanParameter(BaseParameter):
    # UI is a single checkbox
    def __init__(self,
                 field_name: str,
                 default_value: Optional[bool] = None):

        super().__init__(field_name=field_name, field_data_type=ParameterDataType.BOOL)
        self.default_value = default_value
        self.parameter_type = "boolean_parameter"

    def validate(self, value):
        self._validate_datatype(value)


class OperationPayloadEntity:
    def __init__(self, field_name: str, field_data_type: str):
        self.field_name = field_name
        self.field_data_type = field_data_type

    def as_dict(self):
        return self.__dict__


class SetsList(OperationPayloadEntity):
    def __init__(self,
                 content_asset_types: List[str]):

        super().__init__(field_name="sets", field_data_type=ParameterDataType.LIST_STR)
        for asset_type in content_asset_types:
            assert asset_type in AssetsConstants.VALID_ASSETS
        self.content_asset_types = content_asset_types
        self.payload_type = "sets_list"

    def validate(self,
                 values,
                 sec: SceneEngineClient):

        assert isinstance(values, list) or isinstance(values, tuple)
        sets_amc = sec.get_asset_manager(asset_type=AssetsConstants.SETS_ASSET_ID)
        for set_id in values:
            if sets_amc.exists(id=set_id):
                set_metadata = sets_amc.get_metadata(id=set_id)
                assert set_metadata["assets_type"] in self.content_asset_types, "Incorrect asset type " \
                    "for input set. Need {}. Found {}".format(self.content_asset_types,
                                                              set_metadata["assets_type"])
            else:
                raise OperationError("set with id {} does not exist".format(set_id))


class PhaseEntity:
    def __init__(self,
                 name: str,
                 param_schema: List[BaseParameter]):

        self.name = name
        self.param_schema = param_schema

    def validate(self, phase_name: str, params: dict):
        assert self.name == phase_name

        param_name_schema_map = {param.field_name: param for param in self.param_schema}
        for param_name, value in params.items():
            param_schema_object = param_name_schema_map.get(param_name)
            assert param_schema_object, "Parameter schema for {} is not defined".format(param_name)
            param_schema_object.validate(value)

    def as_dict(self):
        self_as_dict = {
            "name": self.name,
        }

        params_list = []
        for param in self.param_schema:
            params_list.append(param.as_dict())

        self_as_dict["param_schema"] = params_list

        return self_as_dict


class BaseOperation(ABC):
    """
    Abstract class for defining an Operation
    """

    def __init__(self, scene_engine_client: SceneEngineClient):
        """
        Definition the config, input, output, phase and parameter schemas for this operation here.
        config_schema: List[BaseParameter]
        Example:
            self.config_schema = [
                FieldValueParameter(field_name="my_input",
                                    default_value="value_1",
                                    field_data_type=ParameterDataType.STR),
                BooleanParameter(field_name="Do_More",
                                 default_value=False)
            ]

        input_schema: List[OperationPayloadEntity]
        Example:
            self.input_schema = [
                SetsList(content_asset_types=[AssetsConstants.IMAGES_ASSET_ID])
            ]

        output_schema: List[OperationPayloadEntity]
        Example:
            self.output_schema = [
                SetsList(content_asset_types=[AssetsConstants.IMAGES_ASSET_ID])
            ]

        phase_params_schema: List[PhaseEntity]
        Example:
            self.phase_params_schema = [
                PhaseEntity(name="phase_1",
                            param_schema=[
                                FIeldValueParameter(field_name="phase_input",
                                                    default_value="phase_value_1",
                                                    field_data_type=ParameterDataType.STR),
                                BooleanParameter(field_name="Do_More_Phase",
                                                 default_value=True)
                            ])
            ]
        """

        self.config_schema = None
        self.input_schema = None
        self.output_schema = None
        self.phase_params_schema = None
        self.sec = scene_engine_client

    def _serialized_config_schema(self) -> list:
        """
        Returns the config schema in json format
        """
        schema_list = []
        if self.config_schema:
            for param in self.config_schema:
                param_dict = param.as_dict()
                schema_list.append(param_dict)

        return schema_list

    def _serialized_input_schema(self) -> list:
        """
        Returns the input schema in json format
        """
        schema_list = []
        if self.input_schema:
            for entity in self.input_schema:
                entity_dict = entity.as_dict()
                schema_list.append(entity_dict)
            return schema_list
        else:
            raise OperationError("Operation missing input schema definition")

    def _serialized_output_schema(self) -> list:
        """
        Returns the output schema in json format
        """
        schema_list = []
        if self.output_schema:
            for entity in self.output_schema:
                entity_dict = entity.as_dict()
                schema_list.append(entity_dict)

        return schema_list

    def _serialized_phase_params_schema(self) -> list:
        """
        Returns the phase params schema in json format
        """
        schema_list = []
        if self.phase_params_schema:
            for entity in self.phase_params_schema:
                entity_dict = entity.as_dict()
                schema_list.append(entity_dict)
        return schema_list

    def _validate_input_payload(self, input_payload: dict):
        """
        Validates data before running the process.
        """
        # Validate config against schema
        payload_entity_name__schema_map = {payload_entity.field_name: payload_entity
                                           for payload_entity in self.input_schema}

        for payload_entity_name, values in input_payload.items():
            payload_schema_object = payload_entity_name__schema_map.get(payload_entity_name)
            assert payload_schema_object, "input payload schema for {} is not defined".format(
                payload_entity_name)
            payload_schema_object.validate(values=values,
                                           sec=self.sec)

    def _validate_output_payload(self, output_payload: dict):
        """
        Validates data after running the process.
        """
        # Validate config against schema
        if self.output_schema:
            payload_entity_name__schema_map = {payload_entity.field_name: payload_entity
                                               for payload_entity in self.output_schema}

            for payload_entity_name, values in output_payload.items():
                payload_schema_object = payload_entity_name__schema_map.get(payload_entity_name)
                assert payload_schema_object, "output payload schema for {} is not defined".format(
                    payload_entity_name)
                payload_schema_object.validate(values=values,
                                               sec=self.sec)
        else:
            assert not output_payload, "Operation is not expected to generate an output payload"

    def _validate_config(self, config: dict):
        """
        Validates every new config
        """
        # Validate config against schema
        param_name__schema_map = {param.field_name: param for param in self.config_schema}

        for param_name, value in config.items():
            param_schema_object = param_name__schema_map.get(param_name)
            assert param_schema_object, "Parameter schema for {} is not defined".format(param_name)
            param_schema_object.validate(value)

    def _validate_phase_params(self, phase_name: str, phase_params: dict):
        """
        Validates parameters for each phase of the operation
        """
        # Validate config against schema
        phase_name__param_schema_map = {phase.name: phase for phase in self.phase_params_schema}
        assert phase_name in phase_name__param_schema_map.keys(), "Invalid phase {}".format(phase_name)

        param_schema_object = phase_name__param_schema_map.get(phase_name)
        assert param_schema_object, "Parameter schema for phase {} is not defined".format(phase_name)
        param_schema_object.validate(phase_name, phase_params)

    def save_state(self,
                   instance_id: str,
                   state_dict: dict,
                   overwrite: bool = False):
        """
        Save state for an operation instance
        """
        current_state = {}
        if not overwrite:
            instance_meta = self.sec._get_operation_instance(operation_instance_id=instance_id)
            current_state = instance_meta["state_dict"] or {}

        # Merge two dictionaries
        current_state.update(state_dict)
        self.sec._update_operation_instance(operation_instance_id=instance_id,
                                            state_dict=current_state)

    def get_state(self,
                  instance_id: str) -> dict:
        """
        Get cuurent state of the operation instance
        """
        instance_meta = self.sec._get_operation_instance(operation_instance_id=instance_id)
        current_state = instance_meta.get("state_dict", {})

        return current_state

    @abstractmethod
    def process(self,
                instance_id: str,
                job_id: str,
                input_payload: dict,
                config: Optional[dict] = None,
                phase: Optional[str] = None,
                phase_payload: Optional[dict] = None) -> dict:

        if config:
            self._validate_config(config=config)

        if input_payload:
            self._validate_input_payload(input_payload=input_payload)

        if phase:
            self._validate_phase_params(phase_name=phase, phase_params=phase_payload)

        # Write operation login here
        output_payload = {}

        return output_payload


class OperationPriorities:
    HIGH_PRIORITY_OPERATION = "high_priority_operation"
    LOW_PRIORITY_OPERATION = "low_priority_operation"


class ExternalAnnotator(ABC):
    """Base annotation class. Inherited by all annotator classes."""

    # SceneBox authentication (for SceneEngineClient, AssetManagerClient, etc.)
    def __init__(self,
                 scene_engine_client: SceneEngineClient,
                 annotator_name: str,
                 operation_instance_id: str):

        # All connections to external annotators need the following scenebox data:
        self.sec = scene_engine_client
        self.annotator_name = annotator_name
        self.sets_amc = self.sec.get_asset_manager(AssetsConstants.SETS_ASSET_ID)
        self.images_amc = self.sec.get_asset_manager(AssetsConstants.IMAGES_ASSET_ID)
        self.annotations_amc = self.sec.get_asset_manager(AssetsConstants.ANNOTATIONS_ASSET_ID)
        self.instance_id = operation_instance_id

    def create_output_annotation_sets(self,
                                      input_set_ids: List[str]) -> dict:
        """
        Creates a set to collect the annotations for each input set and returns a map
        of {input_set: output_set}
        """

        input_output_set_map = {}
        input_set_id_to_meta = self.sets_amc.get_metadata_in_batch(ids=input_set_ids,
                                                                   source_selected_fields=["id", "name"])

        for input_set_id, input_set_meta in input_set_id_to_meta.items():
            output_set_name = f"{input_set_id}_{self.instance_id}"
            output_set_id = get_md5_from_string(output_set_name)

            if not self.sets_amc.exists(id=output_set_id):
                output_set_id = self.sec.create_set(name=output_set_name,
                                                    id=output_set_id,
                                                    asset_type=AssetsConstants.ANNOTATIONS_ASSET_ID,
                                                    origin_set_id=input_set_id)
            input_output_set_map[input_set_id] = output_set_id

        return input_output_set_map

    @abstractmethod
    def get_possible_receive_types(self,
                                   image_id_to_annotations: Dict[str, List[Annotation]]) -> List[str]:
        raise NotImplementedError(f"Possible receive type recognition from {self.annotator_name} "
                                  f"has not yet been implemented.")

    @abstractmethod
    def send_images_to_annotator(self,
                                 input_set_id: str,
                                 config: Dict[str, Any],
                                 send_images_payload: Dict[str, Any],
                                 job_id: str):
        raise NotImplementedError(f"Sending images to {self.annotator_name} has not yet been implemented.")

    @abstractmethod
    def receive_image_annotations(self,
                                  input_output_set_map: dict,
                                  receive_annotations_payload: Dict[str, Any],
                                  config: Dict[str, Any],
                                  job_id: str):
        raise NotImplementedError(f"Receiving images from {self.annotator_name} has not yet been implemented.")

    def send_data_to_annotator(self,
                               job_id: str,
                               input_set_ids: List[str],
                               config: dict,
                               send_data_payload: dict):

        job = self.sec.get_job_manager(job_id=job_id)
        if job.get_status() != JobConstants.STATUS_RUNNING:
            job.run()

        for input_set_id in input_set_ids:
            set_metadata = self.sets_amc.get_metadata(input_set_id)
            media_type = set_metadata.get("assets_type")

            if media_type == AssetsConstants.IMAGES_ASSET_ID:
                self.send_images_to_annotator(input_set_id=input_set_id,
                                              job_id=job_id,
                                              config=config,
                                              send_images_payload=send_data_payload)
            else:
                raise NotImplementedError(f"Sending assets of type {media_type} to {self.annotator_name} "
                                          f"is not supported.")

    def receive_annotations_from_annotator(self,
                                           job_id: str,
                                           config: dict,
                                           input_set_ids: List[str],
                                           receive_annotations_payload: dict):
        media_types = []
        input_output_set_map = self.create_output_annotation_sets(input_set_ids=input_set_ids)
        default_annotation_type = config.get("annotation_type")

        for input_set_id in input_set_ids:
            set_metadata = self.sets_amc.get_metadata(input_set_id)
            media_types = set_metadata.get("assets_type")

        if AssetsConstants.IMAGES_ASSET_ID in media_types:
            image_id_to_annotations = \
                self.receive_image_annotations(job_id=job_id,
                                               config=config,
                                               input_output_set_map=input_output_set_map,
                                               receive_annotations_payload=receive_annotations_payload)

            possible_receive_types = self.get_possible_receive_types(image_id_to_annotations=image_id_to_annotations)

            self.update_image_annotations(input_set_ids=input_set_ids,
                                          default_annotation_type=default_annotation_type,
                                          image_id_to_annotations=image_id_to_annotations,
                                          receive_annotations_payload=receive_annotations_payload,
                                          possible_receive_types=possible_receive_types,
                                          input_output_set_map=input_output_set_map,
                                          job_id=job_id)

        elif any([AssetsConstants.IMAGES_ASSET_ID != media_type for media_type in media_types]):
            raise NotImplementedError(f"Media types other than images are not supported for receive."
                                      f"Given media types: {media_types}")

        return list(input_output_set_map.values())

    def _clean_image_meta_with_same_provider(self,
                                             provider: str,
                                             image_id_to_metadata: Dict[str, Any],
                                             possible_receive_types: List[str]):
        annotation_ids_to_remove = []

        for image_id, image_metadata in image_id_to_metadata.items():
            new_annotation_meta = []
            new_annotations = []

            for annotation_summary in image_metadata.get("annotations_meta", []):
                annotation_id = annotation_summary["id"]
                if annotation_summary.get("provider") == provider \
                        and annotation_summary.get("type") in possible_receive_types:
                    annotation_ids_to_remove.append(annotation_id)
                else:
                    new_annotation_meta.append(annotation_summary)
                    new_annotations.append(annotation_id)

            self.images_amc.update_metadata(id=image_id,
                                            metadata={"annotations": new_annotations,
                                                      "annotations_meta": new_annotation_meta},
                                            replace_sets=True)

        if annotation_ids_to_remove:
            self.annotations_amc.delete_with_list(assets_list=annotation_ids_to_remove,
                                                  wait_for_completion=True)

    def save_operation_state(self,
                             state_dict: dict,
                             overwrite: bool = False):
        """
        Save the state of an operation instance
        """
        current_state = {}
        if not overwrite:
            instance_meta = self.sec._get_operation_instance(operation_instance_id=self.instance_id)
            current_state = instance_meta["state_dict"] or {}

        # Merge two dictionaries
        state_dict.update(current_state)
        self.sec._update_operation_instance(operation_instance_id=self.instance_id,
                                            state_dict=state_dict)

    def get_operation_state(self) -> dict:
        """
        Get cuurent state of the operation instance
        """
        instance_meta = self.sec._get_operation_instance(operation_instance_id=self.instance_id)
        current_state = instance_meta.get("state_dict", {})

        return current_state

    def update_lidar_annotations(self):
        raise NotImplementedError()

    def update_video_annotations(self):
        raise NotImplementedError()

    def update_image_annotations(self,
                                 input_set_ids: List[str],
                                 receive_annotations_payload: dict,
                                 default_annotation_type: str,
                                 image_id_to_annotations: Dict[str, List[Annotation]],
                                 possible_receive_types: List[str],
                                 input_output_set_map: dict,
                                 job_id: str,
                                 add_default_annotations: bool = True):

        provider = receive_annotations_payload.get("annotation_provider", self.annotator_name)
        version = receive_annotations_payload.get("annotation_version", None)
        image_ids = []

        job = self.sec.get_job_manager(job_id=job_id)
        job_progress = job.get_progress()

        job.update_stage("Getting image metadata")
        job.update_progress(progress=job_progress + 0.4 * (100 - job_progress))

        for set_ in input_set_ids:
            query = {"filters": [
                        {
                          "field": "sets",
                          "values": [set_],
                          "filter_out": False
                        }
                     ]
                    }
            image_ids.extend(self.images_amc.search_assets_large(query=query))

        image_id_to_metadata = self.images_amc.get_metadata_in_batch(
            ids=image_ids,
            source_selected_fields=["id", "annotations", "annotations_meta"]
        )

        job.update_stage("Preparing image metadata for new annotations")
        job.update_progress(progress=job_progress + 0.8 * (100 - job_progress))
        self._clean_image_meta_with_same_provider(provider=provider,
                                                  image_id_to_metadata=image_id_to_metadata,
                                                  possible_receive_types=possible_receive_types)

        if add_default_annotations:
            job.update_stage("Appending default annotations")
            job.update_progress(progress=job_progress + 0.9 * (100 - job_progress))
            image_id_to_annotations = self.append_default_annotations(image_id_to_annotations=image_id_to_annotations,
                                                                      default_type=default_annotation_type,
                                                                      provider=provider,
                                                                      version=version,
                                                                      media_type=AssetsConstants.IMAGES_ASSET_ID,
                                                                      input_set_ids=input_set_ids,
                                                                      input_output_set_map=input_output_set_map)

        job.update_stage("Uploading annotations into SceneBox")
        job.update_progress(progress=job_progress + 0.95 * (100 - job_progress))
        self.sec.add_annotations(annotations=[annotation for annotation_list in image_id_to_annotations.values()
                                              for annotation in annotation_list if annotation],
                                 annotations_to_objects=True)

    @staticmethod
    def create_empty_annotation(
            default_type: str,
            asset_id: str,
            media_type: str,
            provider: str,
            version: str,
            output_set_id: str) -> Annotation:

        kwargs = {"id": f"{provider}_{asset_id}_{default_type}",
                  "asset_id": asset_id,
                  "media_type": media_type,
                  "provider": provider,
                  "annotation_group": AnnotationGroups.GROUND_TRUTH,
                  "set_id": output_set_id,
                  "version": version}

        if default_type == AnnotationTypes.TWO_D_BOUNDING_BOX:
            return BoundingBoxAnnotation(bounding_boxes=[], **kwargs)
        elif default_type == AnnotationTypes.POLYGON:
            return PolygonAnnotation(polygons=[], **kwargs)
        elif default_type == AnnotationTypes.POINT:
            return PointAnnotation(points=[], **kwargs)
        elif default_type == AnnotationTypes.LINE:
            return LineAnnotation(lines=[], **kwargs)
        elif default_type == AnnotationTypes.SEGMENTATION:
            return SegmentationAnnotation(labels=[],
                                          mask_colors=[],
                                          mask_urls=[],
                                          **kwargs)
        else:
            raise TypeError(f"Default annotation type {default_type} not recognized.")

    def append_default_annotations(self,
                                   image_id_to_annotations: Dict[str, List[Annotation]],
                                   default_type: str,
                                   provider: str,
                                   media_type: str,
                                   version: str,
                                   input_set_ids: List[str],
                                   input_output_set_map: dict) -> Dict[str, List[Annotation]]:

        image_ids = list(image_id_to_annotations.keys())
        input_set_id_to_metadata = self.sets_amc.get_metadata_in_batch(ids=input_set_ids)
        image_id_to_metadata = self.images_amc.get_metadata_in_batch(ids=image_ids,
                                                                     source_selected_fields=["id", "annotations",
                                                                                             "annotations_meta",
                                                                                             "sets"])
        for image_id, annotations in image_id_to_annotations.items():

            if not annotations:
                if media_type == AssetsConstants.IMAGES_ASSET_ID:
                    sets_meta = image_id_to_metadata[image_id].get("sets")
                else:
                    raise NotImplementedError()

                # Lazy matching: assume there is only one match between input sets and the current asset
                input_set_id = input_set_ids[0]  # Default in case no match is found
                output_set_id = input_output_set_map[input_set_id]
                for input_set_id, input_set_metadata in input_set_id_to_metadata.items():
                    input_set_name = input_set_metadata.get("name")
                    if any([set_ == input_set_name for set_ in sets_meta]):
                        break

                default_annotation = self.create_empty_annotation(
                    asset_id=image_id,
                    default_type=default_type,
                    media_type=media_type,
                    provider=provider,
                    version=version,
                    output_set_id=output_set_id)

                if default_annotation.id not in image_id_to_metadata.get("annotations", []):
                    image_id_to_annotations[image_id].append(default_annotation)

        return image_id_to_annotations
