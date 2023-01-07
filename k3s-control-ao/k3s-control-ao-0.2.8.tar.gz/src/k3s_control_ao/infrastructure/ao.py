from typing import List, Union
import requests, json
from ddd_objects.infrastructure.repository_impl import error_factory
from ddd_objects.domain.exception import return_codes
from .do import (
    DeploymentSettingDO,
    ReleaseNodeInfoDO,
    ConditionDO,
    ConfigMapDO,
    ConfigMapUserSettingDO,
    DeploymentDO,
    IngressDO,
    JobDO,
    JobSettingDO,
    NamespaceDO,
    NodeCreationItemDO,
    NodeCreationRequestDO,
    NodeInfoDO,
    NodeMetaDO, 
    NodeUserSettingDO,
    PersistentVolumeClaimDO,
    PersistentVolumeDO,
    PodContainerDO,
    PodDO,
    PodLogSettingDO,
    SecretDO,
    SecretUserSettingDO,
    ServiceDO,
    StorageClassDO
)

class K3SController:
    def __init__(self, ip: str, port: int, token: str) -> None:
        self.url = f"http://{ip}:{port}"
        self.header = {"api-token":token}

    def _check_error(self, status_code, info):
        if status_code>299:
            if isinstance(info['detail'], str):
                return_code = return_codes['OTHER_CODE']
                error_traceback = info['detail']
            else:
                return_code = info['detail']['return_code']
                error_traceback = info['detail']['error_traceback']
            raise error_factory.make(return_code)(error_traceback)

    def check_connection(self, timeout=3):
        response=requests.get(f'{self.url}', headers=self.header, timeout=timeout)
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        if info['message']=='Hello World':
            return True
        else:
            return False

    def create_node(self, condition: ConditionDO, node_user_setting: NodeUserSettingDO, timeout=1200):
        data = {
            "condition": condition.dict(),
            "node_user_setting": node_user_setting.dict()
        }
        data = json.dumps(data)
        response=requests.post(f'{self.url}/node', headers=self.header, data=data, timeout=timeout)
        infos = json.loads(response.text)
        self._check_error(response.status_code, infos)
        return [NodeInfoDO(**info) for info in infos]

    def clear_node(self, node_name: str, timeout=60):
        response=requests.delete(f'{self.url}/node/node_name/{node_name}', 
                    headers=self.header, timeout=timeout)
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return info

    def delete_nodes(self, node_infos: List[ReleaseNodeInfoDO], timeout=60):
        data = [info.dict() for info in node_infos]
        data = json.dumps(data)
        response=requests.delete(f'{self.url}/nodes', headers=self.header, data=data, timeout=timeout)
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return info

    def cordon(self, node_name:str, timeout=3):
        response = requests.get(f'{self.url}/node/cordon/node_name/{node_name}', 
            headers=self.header, timeout=timeout)
        succeed = json.loads(response.text)
        self._check_error(response.status_code, succeed)
        return succeed

    def get_nodes_by_name(self, node_name:str, timeout=10):
        response=requests.get(f'{self.url}/nodes/node_name/{node_name}', 
            headers=self.header, timeout=timeout)
        infos = json.loads(response.text)
        self._check_error(response.status_code, infos)
        return [NodeInfoDO(**info) for info in infos]

    def get_node_metas(self,  timeout=7):
        response=requests.get(f'{self.url}/node_metas', 
            headers=self.header, timeout=timeout)
        infos = json.loads(response.text)
        self._check_error(response.status_code, infos)
        return [NodeMetaDO(**meta) for meta in infos]

    def add_node_label(self, node_name: str, key: str, value: str, timeout=3)->bool:
        response=requests.post(f'{self.url}/label/node_name/{node_name}/key/{key}/value/{value}', 
            headers=self.header, timeout=timeout)
        infos = json.loads(response.text)
        self._check_error(response.status_code, infos)
        return infos

    def get_namespaces(self,  timeout=10):
        response=requests.get(f'{self.url}/namespaces', 
            headers=self.header, timeout=timeout)
        infos = json.loads(response.text)
        self._check_error(response.status_code, infos)
        return [NamespaceDO(**namespace) for namespace in infos]

    def create_namespace(self,  namespace_name: str, timeout=10):
        response=requests.post(
            f'{self.url}/namespace/namespace_name/{namespace_name}', 
            headers=self.header, timeout=timeout)
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return info

    def create_secrets(
        self, 
        secret_user_settings: List[SecretUserSettingDO],
        timeout=300
    ):
        data = [setting.dict() for setting in secret_user_settings]
        data = json.dumps(data)
        response=requests.post(
            f'{self.url}/secrets', 
            headers=self.header, data=data, timeout=timeout)
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return info

    def get_secrets(self, namespace_name: str, timeout=10):
        response=requests.get(
            f'{self.url}/secrets/namespace_name/{namespace_name}', 
            headers=self.header, timeout=timeout)
        infos = json.loads(response.text)
        self._check_error(response.status_code, infos)
        return [SecretDO(**s) for s in infos]

    def create_config_maps(
        self, 
        config_map_user_settings: List[ConfigMapUserSettingDO],
        timeout=10
    ):
        data = [setting.dict() for setting in config_map_user_settings]
        data = json.dumps(data)
        response=requests.post(
            f'{self.url}/config_maps', 
            headers=self.header, data=data, timeout=timeout)
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return info

    def get_config_maps(self, namespace_name:str, timeout=10):
        response=requests.get(
            f'{self.url}/config_maps/namespace_name/{namespace_name}', 
            headers=self.header, timeout=timeout)
        infos = json.loads(response.text)
        self._check_error(response.status_code, infos)
        return [ConfigMapDO(**s) for s in infos]

    def get_deployments(self, namespace_name:str, timeout=10):
        response=requests.get(
            f'{self.url}/deployments/namespace_name/{namespace_name}', 
            headers=self.header, timeout=timeout)
        infos = json.loads(response.text)
        self._check_error(response.status_code, infos)
        return [DeploymentDO(**s) for s in infos]

    def get_ingresses(self, namespace_name:str, timeout=30):
        response=requests.get(
            f'{self.url}/ingresses/namespace_name/{namespace_name}', 
            headers=self.header, timeout=timeout)
        infos = json.loads(response.text)
        self._check_error(response.status_code, infos)
        return [IngressDO(**s) for s in infos]

    def get_pods(self, namespace_name:str, timeout=30):
        response=requests.get(
            f'{self.url}/pods/namespace_name/{namespace_name}', 
            headers=self.header, timeout=timeout)
        infos = json.loads(response.text)
        self._check_error(response.status_code, infos)
        return [PodDO(**s) for s in infos]

    def delete_pod(self, namespace_name:str, pod_name:str, timeout=5):
        response=requests.delete(
            f'{self.url}/pod/namespace_name/{namespace_name}/pod_name/{pod_name}', 
            headers=self.header, timeout=timeout)
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return info

    def get_services(self, namespace_name:str, timeout=30):
        response=requests.get(
            f'{self.url}/services/namespace_name/{namespace_name}', 
            headers=self.header, timeout=timeout)
        infos = json.loads(response.text)
        self._check_error(response.status_code, infos)
        return [ServiceDO(**s) for s in infos]

    def get_pod_containers(self, namespace_name:str, timeout=30):
        response=requests.get(
            f'{self.url}/pod_containers/namespace_name/{namespace_name}', 
            headers=self.header, timeout=timeout)
        infos = json.loads(response.text)
        self._check_error(response.status_code, infos)
        return [PodContainerDO(**s) for s in infos]

    def get_jobs(self, namespace_name:str, timeout=10):
        response=requests.get(
            f'{self.url}/jobs/namespace_name/{namespace_name}', 
            headers=self.header, timeout=timeout)
        infos = json.loads(response.text)
        self._check_error(response.status_code, infos)
        return [JobDO(**s) for s in infos]

    def create_deployment(self, deployment_setting: DeploymentSettingDO, timeout=10):
        data = json.dumps(deployment_setting.dict())
        response=requests.post(
            f'{self.url}/deployment', 
            headers=self.header, data=data, timeout=timeout)
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return DeploymentDO(**info)
        
    def create_job(self, job_setting:JobSettingDO, timeout=10):
        data = json.dumps(job_setting.dict())
        response=requests.post(
            f'{self.url}/job', 
            headers=self.header, data=data, timeout=timeout)
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return JobDO(**info)
    
    def get_pod_log(
        self, 
        pod_log_setting: PodLogSettingDO,
        timeout:int=10
    ):
        data = json.dumps(pod_log_setting.dict())
        response=requests.get(
            f'{self.url}/log', 
            headers=self.header, data=data,timeout=timeout)
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return info


    def delete_deployment(
        self,
        namespace_name:str,
        deployment_name:str,
        timeout:int=10
    ):
        response=requests.delete(
            f'{self.url}/deployment/namespace_name/{namespace_name}/deployment_name/{deployment_name}', 
            headers=self.header, timeout=timeout)
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return info

    def delete_job(
        self,
        namespace_name:str,
        job_name:str,
        timeout:int=10
    ):
        response=requests.delete(
            f'{self.url}/job/namespace_name/{namespace_name}/job_name/{job_name}', 
            headers=self.header, timeout=timeout)
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return info

    def create_storage_class(
        self,
        storage_class: StorageClassDO,
        timeout: int = 3
    ):
        data = json.dumps(storage_class.dict())
        response = requests.post(
            f'{self.url}/storage_class',
            headers=self.header, data=data, timeout=timeout
        )
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return info

    def delete_storage_class(
        self,
        storage_class_name: str,
        timeout: int = 3
    ):
        response = requests.delete(
            f'{self.url}/storage_class/storage_class_name/{storage_class_name}',
            headers=self.header, timeout=timeout
        )
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return info

    def create_persistent_volume(
        self,
        persistent_volume: PersistentVolumeDO,
        timeout: int = 3
    ):
        data = json.dumps(persistent_volume.dict())
        response = requests.post(
            f'{self.url}/persistent_volume',
            headers=self.header, data=data, timeout=timeout
        )
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return info

    def delete_persistent_volume(
        self,
        persistent_volume_name: str,
        timeout: int = 3
    ):
        response = requests.delete(
            f'{self.url}/persistent_volume/persistent_volume_name/{persistent_volume_name}',
            headers=self.header, timeout=timeout
        )
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return info

    def create_persistent_volume_claim(
        self,
        persistent_volume_claim: PersistentVolumeClaimDO,
        timeout: int = 5
    ):
        data = json.dumps(persistent_volume_claim.dict())
        response = requests.post(
            f'{self.url}/persistent_volume_claim',
            headers=self.header, data=data, timeout=timeout
        )
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return info

    def delete_persistent_volume_claim(
        self,
        namespace_name: str,
        persistent_volume_claim_name: str,
        timeout: int = 5
    ):
        response = requests.delete(
            f'{self.url}/persistent_volume_claim/namespace_name/{namespace_name}/persistent_volume_claim_name/{persistent_volume_claim_name}',
            headers=self.header, timeout=timeout
        )
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return info

    def send_node_creation_request(self, request: NodeCreationRequestDO, timeout=3):
        data = json.dumps(request.dict())
        response=requests.post(f'{self.url}/node/request', 
            headers=self.header, data=data, timeout=timeout)
        id = json.loads(response.text)
        self._check_error(response.status_code, id)
        if id is None:
            return None
        else:
            return id

    def find_node_creation_item(self, id: str, timeout=3):
        response=requests.get(f'{self.url}/node/item/id/{id}', 
            headers=self.header, timeout=timeout)
        item = json.loads(response.text)
        self._check_error(response.status_code, item)
        return NodeCreationItemDO(**item)

    def find_unprocessed_node_creation_item(self, timeout=3):
        response=requests.get(f'{self.url}/node/item/unprocessed', 
            headers=self.header, timeout=timeout)
        item = json.loads(response.text)
        self._check_error(response.status_code, item)
        if item is None:
            return None
        else:
            return NodeCreationItemDO(**item)

    def update_node_creation_item(self, item:NodeCreationItemDO, timeout=10):
        data = json.dumps(item.dict())
        response=requests.put(f'{self.url}/node/item', 
            headers=self.header, data=data, timeout=timeout)
        succeed = json.loads(response.text)
        self._check_error(response.status_code, succeed)
        return succeed

    def clear_node_creation_item(self, timeout=3):
        response=requests.get(f'{self.url}/node/item/clear', 
            headers=self.header, timeout=timeout)
        n = json.loads(response.text)
        self._check_error(response.status_code, n)
        return n

    def delete_node_creation_item(self, item_id:str, timeout=3):
        response=requests.delete(f'{self.url}/node/item/id/{item_id}', 
            headers=self.header, timeout=timeout)
        succeed = json.loads(response.text)
        self._check_error(response.status_code, succeed)
        return succeed

    def delete_namespace(self, namespace_name:str, timeout=10):
        response=requests.delete(f'{self.url}/namespace/namespace_name/{namespace_name}', 
            headers=self.header, timeout=timeout)
        succeed = json.loads(response.text)
        self._check_error(response.status_code, succeed)
        return succeed