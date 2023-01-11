# Author: MetariumProject

# local libraries
from .base import SubstrateBaseEncoder


class SubstrateScribeEncoder(SubstrateBaseEncoder):

    FUNCTION_CALL = "update_scribe_authority_status"

    def is_valid_data(self, data:dict={}):
        # check if data has the required keys
        assert "scribe" in data and isinstance(data["scribe"], str)
        assert "status" in data and isinstance(data["status"], bool)
        # return true
        return True

    def compose_call(self, data:dict={}):
        return self.metarium_node.compose_call(
            call_module=self.__class__.SUBSTRATE_EXTRINSIC,
            call_function=self.__class__.FUNCTION_CALL,
            call_params={
                "scribe": data["scribe"],
                "status": data["status"]
            }
        )
