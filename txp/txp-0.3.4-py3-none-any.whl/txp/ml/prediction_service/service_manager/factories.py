from typing import List, Dict
from txp.ml.common.tasks.slic.slic_patch_recognition_classifier import SlicPatchRecognitionTask
from txp.ml.prediction_service.state_managers.axionlog import RayBasicAxionlogGateAsset
from txp.ml.prediction_service.state_managers.gao import RayBasicGaoAsset
from txp.ml.prediction_service.state_managers.beer_showrrom_states import RayBasicShowroomBeerAsset
from txp.ml.prediction_service.state_managers.showroom import RayBasicShowroomVibrationAsset
from txp.ml.prediction_service.state_managers.mock_state_manager import RayMockAsset
from txp.ml.common.tasks.vibration_baseline.vibration_basic_task import VibrationBasicTask
from txp.ml.common.tasks.mock.mock_task import MockTask
from txp.common.ml.tasks import AssetTask
import logging


class TaskFactory:
    """
        Tasks factory used for creating all ml task objects.
    """
    @staticmethod
    def create_task(task_definition: AssetTask, credentials_str):
        # TODO: this cases of task_type should come from firestore

        task_type = task_definition.task_type
        if task_type == 'VibrationBasicTask':
            logging.info(f"Creating task for VibrationBasicTask")
            return VibrationBasicTask(task_definition, credentials_str)
        elif task_type == 'VibrationBasicGradientBoostTask':
            logging.info(f"Creating task for VibrationBasicGradientBoostTask")
            return VibrationBasicTask(task_definition, credentials_str, decision_tree_policy=False)
        elif task_type == 'SlicPatchRecognitionTask':
            logging.info(f"Creating task for SlicPatchRecognitionTask")
            return SlicPatchRecognitionTask(task_definition, credentials_str)
        elif task_type == 'MockTask':
            return MockTask(task_definition, credentials_str)
        else:
            logging.info(f"Task type not supported for task: {task_definition.dict()}")

    @staticmethod
    def create_tasks_for_asset(asset_id, assets_config, credentials_str):
        tasks = {}
        for task in assets_config[asset_id]['tasks'].values():
            task_definition = AssetTask(**task)
            tasks[task['task_id']] = TaskFactory.create_task(task_definition, credentials_str)
        return tasks

    @staticmethod
    def create_tasks(assets_config, state_managers, credentials_str):
        tasks = {}
        for asset_id in assets_config:
            if assets_config[asset_id]["state_manager"] not in state_managers:
                continue
            tasks = {**tasks, **TaskFactory.create_tasks_for_asset(asset_id, assets_config, credentials_str)}
        for task in tasks.values():
            if not task.is_ready():
                logging.info(f"Error starting task for task_id: {task.task_id}")
            else:
                logging.info(f"Task {task.task_id} ready")
        return tasks


class StateManagerFactory:
    """
        Tasks factory used for creating all ml state manager objects.
    """

    @staticmethod
    def create_state_managers(assets_config, credentials_str, backup_collection_name, events_and_states_dataset,
                              notifications_topic, reports_topic):
        state_managers = {}
        for asset_id in assets_config:
            state_m = StateManagerFactory.create_state_manager_for_asset(asset_id, assets_config[asset_id],
                                                                         credentials_str, backup_collection_name,
                                                                         events_and_states_dataset, notifications_topic,
                                                                         reports_topic)
            if state_m is not None:
                state_managers[assets_config[asset_id]["state_manager"]] = state_m

        return state_managers

    @staticmethod
    def create_state_manager_for_asset(asset_id, asset_config, credentials_str, backup_collection_name,
                                       events_and_states_dataset, notifications_topic, reports_topic):
        state_manager_id = asset_config["state_manager"]
        tasks = []
        for task in asset_config["tasks"].values():
            tasks.append(task["task_id"])

        if "motor_lab_sm" == state_manager_id:
            return RayBasicShowroomVibrationAsset.remote(asset_id, tasks, events_and_states_dataset,
                                                         backup_collection_name, notifications_topic, reports_topic,
                                                         credentials_str)
        elif "beer_lab_sm" == state_manager_id:
            asset_tasks: Dict[str, AssetTask] = dict(map(
                lambda tpl: (tpl[0], AssetTask(**tpl[1])),
                asset_config["tasks"].items()
            ))
            return RayBasicShowroomBeerAsset.remote(asset_id, tasks, events_and_states_dataset, backup_collection_name,
                                                    notifications_topic, reports_topic, credentials_str, asset_tasks)
        elif "gao_sm" == state_manager_id:
            asset_tasks: List[AssetTask] = list(map(
                lambda task_dict: AssetTask(**task_dict),
                asset_config["tasks"].values()
            ))
            return RayBasicGaoAsset.remote(asset_id, tasks, events_and_states_dataset, backup_collection_name,
                                           asset_tasks, notifications_topic, reports_topic, credentials_str)
        elif "axionlog_sm" == state_manager_id:
            asset_tasks: List[AssetTask] = list(map(
                lambda task_dict: AssetTask(**task_dict),
                asset_config["tasks"].values()
            ))
            return RayBasicAxionlogGateAsset.remote(asset_id, tasks, events_and_states_dataset, backup_collection_name,
                                                    asset_tasks, notifications_topic, reports_topic, credentials_str)

        elif "mock_sm" == state_manager_id:
            return RayMockAsset.remote(asset_id, tasks, events_and_states_dataset, backup_collection_name,
                                       notifications_topic, reports_topic, credentials_str)
        else:
            logging.info(f"state manager not supported, state_manager_id: {state_manager_id}, asset_id: {asset_id}")
            return None
