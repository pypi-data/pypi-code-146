from time import sleep
import grpc
import json, jsonlines
from beartype.typing import Generator, Union
from loguru import logger
from google.protobuf.timestamp_pb2 import Timestamp
from fsai_grpc_api.protos import utils_pb2
from fsai_grpc_api.protos import category_api_pb2, category_api_pb2_grpc
from fsai_grpc_api.protos import detection_api_pb2, detection_api_pb2_grpc
from fsai_grpc_api.protos import (
    detection_instance_api_pb2,
    detection_instance_api_pb2_grpc,
)
from fsai_grpc_api.protos import feature_api_pb2, feature_api_pb2_grpc
from fsai_grpc_api.protos import image_api_pb2, image_api_pb2_grpc
from fsai_grpc_api.protos import source_api_pb2, source_api_pb2_grpc
from fsai_grpc_api.protos import query_api_pb2, query_api_pb2_grpc
from fsai_grpc_api.protos import workflow_api_pb2, workflow_api_pb2_grpc
from fsai_shared_funcs.proto_helpers.json_format import MessageToDict
from pydash import get
from beartype import beartype
import dateutil.parser
from fsai_shared_funcs.time_helper import get_pb_ts_from_datetime


@beartype
def get_manifest_reader(fsai_manifest_path: str):
    # Open the fsai_manifest_path
    with jsonlines.open(fsai_manifest_path) as reader:

        # Read the next line in the file
        for line in reader.iter(type=dict, skip_invalid=True):

            # Return the line
            yield line


class ManifestStorageConnectionManager:
    @beartype
    def __init__(self, server: str = "localhost:8080") -> None:
        self.server = server
        self.connect()

    @beartype
    def connect(self) -> None:
        # Open the gRPC channel
        self.channel = grpc.insecure_channel(self.server)

    @beartype
    def disconnect(self) -> None:
        try:
            # Close the gRPC channel
            self.channel.close()
        except:
            pass

    @beartype
    def get_api_clients(self) -> dict:

        logger.info("Resetting/Reconnecting to gRPC server...")

        self.disconnect()
        self.connect()

        # Create api stub (clients)
        return {
            "category": category_api_pb2_grpc.CategoryApiStub(self.channel),
            "feature": feature_api_pb2_grpc.FeatureApiStub(self.channel),
            "detection": detection_api_pb2_grpc.DetectionApiStub(self.channel),
            "detection_instance": detection_instance_api_pb2_grpc.DetectionInstanceApiStub(
                self.channel
            ),
            "image": image_api_pb2_grpc.ImageApiStub(self.channel),
            "source": source_api_pb2_grpc.SourceApiStub(self.channel),
            "query": query_api_pb2_grpc.QueryApiStub(self.channel),
            "workflow": workflow_api_pb2_grpc.WorkflowApiStub(self.channel),
        }


class ManifestStorageHelper:
    @beartype
    def __init__(
        self,
        grpc_manager: ManifestStorageConnectionManager,
        manifest_reader: Generator,
    ) -> None:
        self.grpc_manager = grpc_manager
        self.grpc_clients = self.grpc_manager.get_api_clients()
        self.manifest_reader = manifest_reader

    @beartype
    def get_height(self, detection: dict) -> float:
        height = get(detection, "inferred.adjusted_height", 0)

        if height == None:
            return float(0)

        return float(height)

    @beartype
    def get_lat_lon(self, detection: dict) -> tuple[float, float]:
        lat = get(detection, "inferred.best_lat")
        lon = get(detection, "inferred.best_lon")
        return lat, lon

    # Move to helper library
    @beartype
    def string_to_pb_timestamp(self, detected_at: Union[str, None]) -> Timestamp:

        try:
            # If this is a string then try to build proto timestamp
            if isinstance(detected_at, str):
                datetime = dateutil.parser.parse(detected_at)
                return get_pb_ts_from_datetime(datetime)
        except:
            pass

        # Get the current timestamp as protobuf
        timestamp = Timestamp()
        timestamp.GetCurrentTime()

        return timestamp

    @beartype
    def find_or_create_workflow(self, name: str) -> Union[int, None]:

        # Create the workflow request
        req = workflow_api_pb2.WorkflowRequest(
            name=name,
        )

        # Find or create the workflow
        workflow = self.grpc_clients["workflow"].FindOrCreateWorkflow(req)

        # Get the workflow id from the database
        workflow_id = get(workflow, "id", None)

        # Return the workflow id
        return workflow_id

    @beartype
    def get_part_id(self, line: dict) -> Union[int, None]:
        # Get the workflow part id from the line
        part_id = get(line, "workflow.part_id", None)

        return part_id

    @beartype
    def get_source_detection_id(self, line: dict) -> Union[str, None]:
        # Get the source detection id from the line
        source_detection_id = get(line, "source.id", None)

        return str(source_detection_id)

    @beartype
    def find_or_create_image(self, line: dict) -> Union[int, None]:
        # If no image object then return None
        if get(line, "image", None) == None:
            return None

        # Get the image bbox_coord
        geo_bbox = get(line, "bbox_coord", None)

        # Create the image request
        req = image_api_pb2.FindOrCreateImageRequest(
            image=image_api_pb2.Image(
                name=get(line, "image.name", None),
                width=get(line, "image.width", None),
                height=get(line, "image.height", None),
                geo_bbox=utils_pb2.GeoBbox(**geo_bbox),
            )
        )
        # Find or create the image
        response = self.grpc_clients["image"].FindOrCreateImage(req)

        # Convert the message to a dict
        response = MessageToDict(
            response,
            preserving_proto_field_name=True,
        )

        # Access the image id
        image_id = response["image"]["id"]

        # Return the image id
        return image_id

    @beartype
    def get_detection_geo_bbox(self, detection: dict) -> Union[dict, None]:
        return get(detection, "bbox_coord", None)

    @beartype
    def find_or_create_feature(self, line: dict) -> Union[int, None]:

        # If no feature object then return None
        if get(line, "feature", None) == None:
            return None

        # Create the feature request
        req = feature_api_pb2.FeatureRequest(
            vendor_name="maxar",
            vendor_id=get(line, "feature.feature_id", ""),
            feature=json.dumps(get(line, "feature", {})),
        )

        # Find or create the feature
        feature = self.grpc_clients["feature"].FindOrCreateFeature(req)

        return feature.id

    @beartype
    def find_or_create_category(self, detection: dict) -> int:

        # Setup the category request
        req = category_api_pb2.CategoryRequest(
            name=get(detection, "category.name"),
        )
        category = self.grpc_clients["category"].FindOrCreateCategory(req)

        return category.id

    @beartype
    def find_or_create_detection(
        self,
        lat: float,
        lon: float,
        category_id: int,
    ) -> int:
        # Setup the detection source request
        req = detection_api_pb2.DetectionRequest(
            geo_point=utils_pb2.GeoPoint(
                lat=lat,
                lon=lon,
            ),
            category_id=category_id,
        )
        detection = self.grpc_clients["detection"].FindOrCreateDetection(req)

        logger.info("Insert Detection: {}".format(MessageToDict(detection)))

        return detection.id

    @beartype
    def update_detection_instance_geo_bbox(
        self, detection_instance_id: int, geo_bbox: Union[dict, None]
    ) -> Union[int, None]:

        if geo_bbox == None:
            return None

        # Setup the detection instance request
        req = detection_instance_api_pb2.UpdateDetectionInstanceGeoBboxRequest(
            detection_instance=detection_instance_api_pb2.DetectionInstance(
                id=detection_instance_id,
                geo_bbox=utils_pb2.GeoBbox(**geo_bbox),
            ),
        )

        try:
            response = self.grpc_clients[
                "detection_instance"
            ].UpdateDetectionInstanceGeoBbox(req)

            response = MessageToDict(
                response,
                preserving_proto_field_name=True,
            )

            logger.info("Updated Detection Instance GeoBbox: {}".format(response))

            detection_instance_id = response["detection_instance"]["id"]

            return detection_instance_id

        except Exception as e:
            logger.debug(e)

        return None

    @beartype
    def find_or_create_detection_instance(
        self,
        workflow_id: Union[int, None],
        part_id: Union[int, None],
        image_id: Union[int, None],
        detection_id: int,
        feature_id: Union[int, None],
        source_id: int,
        source_detection_id: Union[str, None],
        score: float,
        height: float,
        height_inferred: bool,
        detected_at: Timestamp,
    ) -> int:
        # Setup the detection instance request
        req = detection_instance_api_pb2.FindOrCreateDetectionInstanceRequest(
            detection_instance=detection_instance_api_pb2.DetectionInstance(
                workflow_id=workflow_id,
                part_id=part_id,
                image_id=image_id,
                detection_id=detection_id,
                feature_id=feature_id,
                source_id=source_id,
                source_detection_id=source_detection_id,
                score=score,
                height=height,
                height_inferred=height_inferred,
                detected_at=detected_at,
            )
        )

        response = self.grpc_clients[
            "detection_instance"
        ].FindOrCreateDetectionInstance(req)

        response = MessageToDict(
            response,
            preserving_proto_field_name=True,
        )

        logger.info("Insert Detection Instance: {}".format(response))

        detection_instance_id = response["detection_instance"]["id"]

        return detection_instance_id

    @beartype
    def find_or_create_source(self, name: str) -> int:
        # Setup the detection source request
        req = source_api_pb2.SourceRequest(name=name)

        source = self.grpc_clients["source"].FindOrCreateSource(req)

        logger.info("Insert Detection Source: {}".format(MessageToDict(source)))

        return source.id

    @beartype
    def get_detected_at_str(self, line: dict, detection: dict) -> Union[str, None]:

        feature_aquisition_date: str = get(line, "feature.acquisition_date", None)

        # Return the feature acquisition date if it exists
        if feature_aquisition_date != None:
            return feature_aquisition_date

        detected_at: str = get(detection, "detected_at", None)

        # Return the detected at date if it exists
        if detected_at != None:
            return detected_at

        return None

    @beartype
    def process(self, workflow_name: str, source_name: str) -> None:

        workflow_id = self.find_or_create_workflow(
            name=workflow_name,
        )

        source_id = self.find_or_create_source(
            name=source_name,
        )

        for idx, line in enumerate(self.manifest_reader, start=1):

            # Reset the api client every 100 images to balance the load
            # Todo: Make 250 configurable
            if idx % 250 == 0:

                logger.info("Processed {} images".format(idx))

                self.grpc_clients = self.grpc_manager.get_api_clients()

            feature_id = self.find_or_create_feature(line)

            part_id = self.get_part_id(line)

            source_detection_id = self.get_source_detection_id(line)

            image_id = self.find_or_create_image(line)

            for detection in line["detections"]:

                lat, lon = self.get_lat_lon(detection)

                height = self.get_height(detection)

                height_inferred = False if height == 0 else True

                geo_bbox = self.get_detection_geo_bbox(detection)

                detected_at_str = self.get_detected_at_str(line, detection)

                ##############################
                # Find or create data via api
                ##############################
                category_id = self.find_or_create_category(detection)

                detection_id = self.find_or_create_detection(
                    lat=lat, lon=lon, category_id=category_id
                )

                # Setup the detection instance request
                detection_instance_id = self.find_or_create_detection_instance(
                    workflow_id=workflow_id,
                    part_id=part_id,
                    image_id=image_id,
                    detection_id=detection_id,
                    feature_id=feature_id,
                    source_id=source_id,
                    source_detection_id=source_detection_id,
                    score=detection["score"],
                    height=height,
                    height_inferred=height_inferred,
                    detected_at=self.string_to_pb_timestamp(detected_at_str),
                )

                self.update_detection_instance_geo_bbox(
                    detection_instance_id=detection_instance_id, geo_bbox=geo_bbox
                )
