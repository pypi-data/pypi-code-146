import base64
import time
from pathlib import Path

from proxmoxer import ProxmoxAPI
from requests.exceptions import ConnectionError

from .exceptions import ProxmoxMissingPermissionError, ProxmoxVMNotFoundError, ProxmoxConnectionError
from .types import ExecStatus


class Proxmox:
    def __init__(self, host: str, user: str, realm: str, token_name: str, token_secret: str, verify_ssl: bool = True):
        self.api = ProxmoxAPI(
            host=host,
            user=f'{user}@{realm}',
            token_name=token_name,
            token_value=token_secret,
            verify_ssl=verify_ssl,
        )

        try:
            self.api.version.get()
        except ConnectionError as exc:
            raise ProxmoxConnectionError(f'Could not connect to Proxmox API at {self.api._backend.get_base_url()}') from exc

    def check_permission(self, path: str, permission: str):
        permissions = self.api.access.permissions.get(path=path)[path]
        if permission not in permissions:
            raise ProxmoxMissingPermissionError(path, permission)

    def get_vm_by_name(self, vm_name: str) -> dict:
        vm_list = self.api.cluster.resources.get(type='vm')
        vm = [vm for vm in vm_list if vm['name'] == vm_name]

        if len(vm) == 0:
            raise ProxmoxVMNotFoundError(vm_name)

        return dict(vm[0])

    def get_vm_by_id(self, vm_id: int) -> dict:
        vm_list = self.api.cluster.resources.get(type='vm')
        vm = [vm for vm in vm_list if vm['vmid'] == vm_id]

        if len(vm) == 0:
            raise ProxmoxVMNotFoundError(vm_id)

        return dict(vm[0])

    def exec(self, node: str, vm_id: int, command: str) -> int:
        exec_res = self.api.nodes(node).qemu(vm_id).agent.exec.post(command=command)
        return int(exec_res['pid'])

    def check_exec_status(self, node: str, vm_id: int, pid: int, timeout: int = 120) -> ExecStatus:
        start = time.time()
        now = time.time()

        while now - start < timeout:
            exec_status = self.api.nodes(node).qemu(vm_id).agent('exec-status').get(pid=pid)
            if exec_status.get('exited', 0) == 1:
                return ExecStatus(exitcode=exec_status.get('exitcode'), out_data=exec_status.get('out-data'))
            else:
                time.sleep(1)
                continue
        else:
            raise TimeoutError(f'Could not get result of process {pid} on {vm_id} within {timeout} seconds.')

    def file_write(self, node: str, vm_id: int, file_path: Path, content: bytes):
        content_encoded = base64.b64encode(content)
        self.api.nodes(node).qemu(vm_id).agent('file-write').post(content=content_encoded, file=file_path, encode=0)
