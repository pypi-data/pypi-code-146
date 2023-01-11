import datetime
from importlib.resources import Package

import yaml

from truera.client.cli.cli_utils import ModelType
from truera.client.errors import PackageVerificationException

DATAROBOT_V1_FLAVOR = "datarobot_jar_v1"
DATAROBOT_V2_FLAVOR = "datarobot_jar_v2"


class DataRobotMLmodelTemplate(yaml.YAMLObject):

    def noop(self, *args, **kw):
        pass

    yaml.emitter.Emitter.process_tag = noop

    def __init__(
        self, jar_file_name: str, model_package_id: str, model_type: ModelType
    ):
        assert model_type in [ModelType.Datarobot_v1, ModelType.Datarobot_v2]
        flavor_str = DATAROBOT_V1_FLAVOR if model_type == ModelType.Datarobot_v1 else DATAROBOT_V2_FLAVOR
        self.flavors = {
            flavor_str:
                {
                    "model_jar": jar_file_name,
                    "model_package_id": model_package_id
                }
        }
        self.utc_time_created = datetime.datetime.utcnow().isoformat()
        if model_type == ModelType.Datarobot_v2:
            DataRobotMLmodelTemplate.validate_v2_naming(
                jar_file_name, model_package_id
            )

    @staticmethod
    def validate_v2_naming(jar_file_name: str, model_package_id: str):
        if jar_file_name != model_package_id + ".jar":
            msg = "For DataRobot models using the v2 prediction API, the `model_package_id` must match the name of the provided jar file!"
            msg += f"\nProvided jar name: {jar_file_name}. Provided model package ID: {model_package_id}"
            raise PackageVerificationException(msg)

    @staticmethod
    def validate_flavor(flavor):
        if "model_jar" not in flavor:
            raise PackageVerificationException(
                "Missing `model_jar` field of DataRobot MLmodel file!"
            )

        if "model_package_id" not in flavor:
            raise PackageVerificationException(
                "Missing `model_package_id` field of DataRobot MLmodel file!"
            )

    @staticmethod
    def validate_mlmodel_yaml(model_yaml):
        if "flavors" not in model_yaml:
            raise PackageVerificationException(
                "Provided MLmodel file does not have model flavor set."
            )

        flavors = model_yaml.get("flavors")
        if DATAROBOT_V1_FLAVOR in flavors:
            DataRobotMLmodelTemplate.validate_flavor(
                flavors.get(DATAROBOT_V1_FLAVOR)
            )
        elif DATAROBOT_V2_FLAVOR in flavors:
            flavor = flavors.get(DATAROBOT_V2_FLAVOR)
            DataRobotMLmodelTemplate.validate_flavor(flavor)
            DataRobotMLmodelTemplate.validate_v2_naming(
                flavor["model_jar"], flavor["model_package_id"]
            )
        else:
            raise PackageVerificationException(
                f"MLmodel flavor {flavors} is not a valid DataRobot model flavor!"
            )
