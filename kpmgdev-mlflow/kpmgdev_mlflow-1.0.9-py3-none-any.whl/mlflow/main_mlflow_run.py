import os
import mlflow
from azureml.core import Workspace
from mlflow_utils_class import MlFlowMainLogging


# openxyl, azure-kpmgdev-mlflow


def mlflow_logging(workspace_location: str = 'local', workspace_dict: dict = None,
                   tracking_uri: str = "http://localhost:5000"):
    """

    :param:
        workspace_location:
        workspace_dict:
         tracking_uri: few types of uri can be, depend on the workspace location
            if the workspace_location = 'local':
                An HTTP URI like https://my-tracking-server:5000 (if mlflow_running_location = 'local' , tracking uri default ="http://localhost:5000")
    :return:
    """

    if workspace_location == 'azureml':
        ws = Workspace.get(name=workspace_dict['workspace_name'],
                           subscription_id=workspace_dict['subscription_id_name'],
                           resource_group=workspace_dict['resource_group'])

        tracking_uri = ws.get_mlflow_tracking_uri()

    mlflow.set_tracking_uri(tracking_uri)

    return MlFlowMainLogging
