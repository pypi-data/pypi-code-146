import json
import os

from servicefoundry.lib.config.config_manager import ConfigManager
from servicefoundry.lib.config.dict_questionaire import DictQuestionaire

# TODO: This should just return the input yaml to me


class InstallationConfig:
    def __init__(self, infra_config_file_path=None) -> None:

        if infra_config_file_path and os.path.exists(infra_config_file_path):
            with open(infra_config_file_path, "r") as config:
                infra_config = json.loads(config.read())
        else:
            infra_config = ConfigManager().get_config(ConfigManager.INSTALL_CONFIG)
        if infra_config:
            self.inputs = infra_config["inputs"]
            self.provisioning = infra_config["provisioning"]
            self.ubermold = infra_config["ubermold"]

    # User input needed for installation
    inputs = {
        "provider": None,
        # add all inputs here
    }
    # Config needed for the provisioning step where terraform is run
    provisioning = {
        "provider": None,
        # add all outputs here
    }
    # Config needed for the ubermold step where helm apply is run
    ubermold = {
        # add all outputs here
    }

    def populate_bootstrapping_config(self, target_repo_config, base_terragrunt_dir):
        # TODO: use new output manifest
        print("TODO: write the function")

    def populate_provisioning_config(self, provider: str):
        self.provisioning["provider"] = "aws"
        DictQuestionaire(self.provisioning["awsInputs"]).ask(
            custom_handlers={"externalNetworkConfig": self.__externalConfigHandler}
        )
        ConfigManager().save_config(ConfigManager.INFRA_CONFIG, self.toJSON())

    def toJSON(self):
        return {"provisioning": self.provisioning, "bootstrapping": self.bootstrapping}
