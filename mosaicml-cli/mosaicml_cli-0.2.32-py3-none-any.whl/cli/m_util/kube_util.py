""" mcli util in kubernetes """

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Generator, List, Optional, cast

import yaml
from kubernetes import client
from kubernetes import config as k8s_config
from kubernetes.client.api_client import ApiClient
from rich.style import Style
from rich.table import Table

from mcli import config
from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay
from mcli.models.mcli_cluster import Cluster
from mcli.utils.utils_kube_labels import label

IGNORE_NAMESPACES_EXACT = [
    'default',
    'fleet-system',
    'ingress-nginx',
    'security-scan',
    'nick',
    'nodekiller',
    'jenkins',
    'jenkinsnext',
    'mining',
    'avery-daemons',
    'mosaicml-orchestration',
]
IGNORE_NAMESPACES_START = [
    'cattle',
    'kube',
    'it',
]


def _valid_namespace(namespace: str) -> bool:
    if namespace in IGNORE_NAMESPACES_EXACT:
        return False
    for start in IGNORE_NAMESPACES_START:
        if namespace.startswith(start):
            return False
    return True


# TODO: refactor into regex if this gets unmanagable
IGNORE_NODES_START = [
    'infra-',
    'c16m',
]
IGNORE_NODES_CONTAINS = [
    'controller-pool',
]


def _valid_node(node_name: str) -> bool:
    for start in IGNORE_NODES_START:
        if node_name.startswith(start):
            return False

    for contains in IGNORE_NODES_CONTAINS:
        if contains in node_name:
            return False

    return True


def _print_timedelta(delta: timedelta):
    # strftime cannot be used with timedelta

    seconds = delta.total_seconds()
    if seconds < 60:
        return f'{int(seconds)}s'
    elif seconds < 3600:
        return f'{int(seconds/60)}min'
    elif seconds < 24 * 3600:
        return f'{int(seconds/3600)}hr'
    else:
        return f'{int(seconds/3600/24)}d'


@dataclass
class NodeInfo(MCLIDisplayItem):
    name: str
    display_name: str
    gpus_used: int
    gpus_available: int
    cpus_used: int
    cpus_available: int

    def to_dict(self) -> Dict[str, Any]:
        node = super().to_dict()
        # override display name to be used as name in display
        node['name'] = node.pop('display_name')
        return node


def get_row_color(node: dict) -> Optional[str]:
    """Get the row color using the serialized NodeInfo data
    """
    gpus_used = int(node.get("gpus_used", 0))
    gpus_available = int(node.get("gpus_available", 0))

    if gpus_available == 0:
        return "bright_black"  # gray
    elif gpus_used < gpus_available:
        return "green"

    # don't return a color and override the row (depends on terminal settings)
    return None


class NodeInfoDisplay(MCLIGetDisplay):
    """Display information about the node
    """

    def __init__(self, nodes: List[NodeInfo]):
        self.nodes = nodes

    def __iter__(self) -> Generator[NodeInfo, None, None]:
        for node in self.nodes:
            yield node

    def to_table(self, items: List[Dict[str, Any]]) -> Table:
        """Overrides MCLIGetDisplay.to_table to have custom node colors by row using rich style
        """

        def _to_str(obj: Any) -> str:
            return yaml.safe_dump(obj, default_flow_style=None).strip() if not isinstance(obj, str) else obj

        column_names = self.override_column_ordering or [key for key, val in items[0].items() if val and key != 'name']

        data_table = Table(box=None, pad_edge=False)
        data_table.add_column('NAME', justify='left', no_wrap=True)

        for column_name in column_names:
            data_table.add_column(column_name.upper())

        for item in items:
            row_args = {}
            data_row = tuple(_to_str(item[key]) for key in column_names)
            color = get_row_color(item)
            if color is not None:
                row_args["style"] = Style(color=color)
            data_table.add_row(item['name'], *data_row, **row_args)

        return data_table


_UNASSIGNED_NODE_NAME = 'Unassigned'


@dataclass
class JobInfo(MCLIDisplayItem):
    """Job Info to display
    """

    name: str
    user: str
    age: str

    # note: display item can have multiple rows per job for multinode jobs
    node_name: str
    gpus_used: int
    cpus_used: int

    status: str

    @property
    def is_active(self) -> bool:
        # Assumes everything not Running, Succeeded, and Failed is pending
        return self.status == 'Running'

    def to_dict(self) -> Dict[str, Any]:
        job = super().to_dict()
        if not self.is_active:
            job.pop('node_name')
        return job

    def clear_for_multinode(self):
        """Removes common values when job is running on multiple nodes
        """
        self.name = ''
        self.user = ''
        self.age = ''


class JobInfoDisplay(MCLIGetDisplay):

    def __init__(self, jobs: List[JobInfo]):
        self.jobs = sorted(jobs, key=lambda j: j.name)

    def __iter__(self) -> Generator[JobInfo, None, None]:
        last_job_name = ''
        for job in self.jobs:
            if job.name == last_job_name:
                job.clear_for_multinode()
            else:
                last_job_name = job.name

            yield job


def _convert_cpus(cpu):
    if isinstance(cpu, str) and cpu.endswith('m'):
        return cpu[:-1]
    return cpu


def get_node_display_name(metadata: Dict[str, Any], default: str = '-') -> str:
    labels = metadata.get('labels', {})
    return labels.get(label.mosaic.NODE_DISPLAY_NAME, default)


def get_nodes(cl: client.CoreV1Api, api: ApiClient) -> List[NodeInfo]:
    nodes = cl.list_node()

    node_list: List[NodeInfo] = []
    for node in nodes.items:
        node_data: Dict[str, Any] = cast(Dict[str, Any], api.sanitize_for_serialization(node))
        metadata = node_data.get('metadata', {})
        allocatable = node_data.get('status', {}).get('allocatable', {})
        name = metadata.get('name', '-')
        data = {
            'name': name,
            'display_name': get_node_display_name(metadata, default=name),
            'gpus_used': 0,
            'gpus_available': int(allocatable.get(label.nvidia.GPU, 0)),
            'cpus_used': 0,
            'cpus_available': int(_convert_cpus(allocatable.get('cpu', 0))),
        }
        node_list.append(NodeInfo(**data))
    node_list = [x for x in node_list if _valid_node(node_name=x.name)]
    node_list = sorted(node_list, key=lambda d: d.name)
    return node_list


def get_jobs_from_namespace(cl: client.CoreV1Api, api: ApiClient, namespace: str) -> List[JobInfo]:

    jobs: List[JobInfo] = []
    try:
        pods = cl.list_namespaced_pod(namespace=namespace,
                                      field_selector='status.phase!=Succeeded,status.phase!=Failed')
    except Exception as _:  # pylint: disable=broad-except
        return jobs

    for pod in pods.items:
        pod_data: Dict[str, Any] = cast(Dict[str, Any], api.sanitize_for_serialization(pod))

        metadata = pod_data.get('metadata', {})
        labels = metadata.get('labels', {})
        name = labels.get(label.mosaic.JOB, '-')
        # Assuming one container per pod
        spec = pod_data.get('spec', {})
        node_name = spec.get('nodeName', _UNASSIGNED_NODE_NAME)
        containers = spec.get('containers', [])
        if len(containers) == 0:
            continue
        container = containers[0]
        req_resources = container.get('resources', {}).get('requests', {}) or {}
        status = pod_data.get('status', {})
        start_time = str(status.get('startTime', metadata.get('creationTimestamp')))
        if start_time and start_time != 'None':
            age = _print_timedelta(datetime.now(timezone.utc) - datetime.fromisoformat(start_time))
        else:
            age = ''

        data = {
            'name': name,
            'user': namespace,
            'age': age,
            'node_name': node_name,
            'gpus_used': int(req_resources.get(label.nvidia.GPU, 0)),
            'cpus_used': int(_convert_cpus(req_resources.get('cpu', '0'))),
            'status': status.get('phase', ''),
        }
        jobs.append(JobInfo(**data))

    return jobs


def get_util(clusters: List[str], **kwargs) -> int:
    del kwargs

    load_config = config.MCLIConfig.load_config()
    filtered_clusters: List[Cluster] = [x for x in load_config.clusters if x.name in clusters or not clusters]
    for c in filtered_clusters:
        api = k8s_config.new_client_from_config(context=c.kubernetes_context, config_file=str(config.MCLI_KUBECONFIG))
        cl = client.CoreV1Api(api_client=api)
        node_list: List[NodeInfo] = get_nodes(cl=cl, api=api)
        all_jobs: List[JobInfo] = []

        namespaces = [str(n.metadata.name) for n in cl.list_namespace().items]
        namespaces = [x for x in namespaces if _valid_namespace(x)]

        for namespace in namespaces:
            jobs = get_jobs_from_namespace(cl, api, namespace)
            all_jobs += jobs

        active_jobs = [x for x in all_jobs if x.is_active]
        pending_jobs = [x for x in all_jobs if not x.is_active]
        for job in active_jobs:
            matched_nodes = [x for x in node_list if x.name == job.node_name]
            if len(matched_nodes) != 1:
                continue

            node = matched_nodes[0]
            node.gpus_used += job.gpus_used
            node.cpus_used += job.cpus_used

            # update jobinfo to use node display name rather than actual node name
            job.node_name = node.display_name

        free_nodes_count = sum(1 if n.gpus_used < n.gpus_available else 0 for n in node_list)

        if len(filtered_clusters) > 1:
            print('-' * 50, c.name, '-' * 50)
        print('Nodes:')
        display = NodeInfoDisplay(nodes=node_list)
        display.print(OutputDisplay.TABLE)
        print(f'\nNumber of Free Nodes: {free_nodes_count:,}')

        print('\nActive Runs:')
        active_job_display = JobInfoDisplay(jobs=active_jobs)
        active_job_display.print(OutputDisplay.TABLE)

        print('\nPending Runs:')
        pending_job_display = JobInfoDisplay(jobs=pending_jobs)
        pending_job_display.print(OutputDisplay.TABLE)

    return 0
