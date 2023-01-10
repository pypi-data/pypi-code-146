"""get_runs SDK for Kubernetes"""
from __future__ import annotations

import datetime as dt
import logging
from concurrent.futures import Future
from typing import Any, Dict, List, NamedTuple, Optional, Sequence, Set, Union, overload

import yaml
from typing_extensions import Literal

from mcli.api.engine.engine import run_kube_in_threadpool
from mcli.api.model.run import Run
from mcli.config import MCLIConfig
from mcli.models.mcli_cluster import Cluster
from mcli.models.run_config import FinalRunConfig
from mcli.serverside.clusters.gpu_type import GPUType
from mcli.serverside.job.mcli_job import RUN_CONFIG_FILE_NAME, MCLIJobType
from mcli.utils.utils_epilog import ContextPodStatus
from mcli.utils.utils_kube import KubeContext, list_config_maps_across_contexts, list_pods_across_contexts
from mcli.utils.utils_kube_labels import extract_label_values, label
from mcli.utils.utils_run_status import RunStatus

logger = logging.getLogger(__name__)

__all__ = ['get_runs']


class RunComponents(NamedTuple):
    """Grouping of a run's pods and configmap
    """
    pods: List[Dict[str, Any]]
    config_map: Optional[Dict[str, Any]] = None


CONFIG_NOT_FOUND = {'error': 'Config not found!'}
"""Singleton for when a run's corresponding FinalRunConfig cannot be found in the cluster
"""


def _get_runs_kube(
    runs: Optional[List[str]] = None,
    clusters: Optional[List[str]] = None,
    gpu_types: Optional[List[str]] = None,
    gpu_nums: Optional[List[int]] = None,
    statuses: Optional[List[str]] = None,
) -> Future[List[Run]]:
    """Get runs from all registered Kubernetes clusters
    """

    # Setup filters for kubernetes
    # Filter clusters
    conf = MCLIConfig.load_config(safe=True)
    if clusters is not None:
        chosen_clusters: List[Cluster] = []
        looking_for: Set[str] = set(clusters)
        for cluster in conf.clusters:
            if cluster.name in looking_for:
                looking_for.discard(cluster.name)
                chosen_clusters.append(cluster)
            if not looking_for:
                break
        if looking_for:
            logger.warning(f'Ignoring unknown cluster(s): {", ".join(sorted(list(looking_for)))}')
        if not chosen_clusters:
            raise RuntimeError(f'No clusters found matching filter: {", ".join(clusters)}')
    else:
        chosen_clusters = conf.clusters

    # Filter by names, gpu types and gpu num using labels
    # Filter to any pod with the "job" label present, by default
    labels: Dict[str, Optional[Union[str, List[str]]]] = {label.mosaic.JOB: None}
    if runs is not None:
        labels[label.mosaic.JOB] = list(runs)

    # Filter instances
    if gpu_types is not None:
        labels[label.mosaic.compute_selectors.LABEL_GPU_TYPE] = list(gpu_types)

    if gpu_nums is not None:
        labels[label.mosaic.compute_selectors.LABEL_GPU_NUM] = [str(i) for i in gpu_nums]

    # Use only the Kubernetes contexts for the clusters we want
    contexts = [p.to_kube_context() for p in chosen_clusters]

    res = run_kube_in_threadpool(_threaded_get_runs, contexts, labels, statuses)
    return res


def _threaded_get_runs(contexts: List[KubeContext],
                       labels: Dict[str, Optional[Union[str, List[str]]]],
                       statuses: Optional[Sequence[str]] = None) -> List[Run]:
    """Function to be called in a thread to return runs from the provided contexts that
    match the provided labels.
    """

    all_pods, _ = list_pods_across_contexts(contexts=contexts, labels=labels)
    if not all_pods:
        return []

    all_cms, _ = list_config_maps_across_contexts(contexts=contexts, labels=labels)
    run_components = _group_objects_by_label(all_pods, all_cms)

    return _run_from_components(run_components, statuses)


def _group_objects_by_label(
    pods: List[Dict[str, Any]],
    config_maps: List[Dict[str, Any]],
) -> Dict[str, RunComponents]:
    """Group pods and configmaps according to their value for the job label
    """

    group_by = label.mosaic.JOB

    cm_grouping: Dict[str, Dict[str, Any]] = {}
    labels: Dict[str, str]
    for cm in config_maps:
        labels = cm['metadata'].get('labels', {})
        key = labels.get(group_by, '-')
        if cm.get('data', {}).get(RUN_CONFIG_FILE_NAME):
            cm_grouping[key] = cm

    pod_grouping: Dict[str, List[Dict[str, Any]]] = {}
    for p in pods:
        labels = p['metadata'].get('labels', {})
        key = labels.get(group_by, '-')
        if key not in pod_grouping:
            pod_grouping[key] = []
        pod_grouping[key].append(p)

    return {
        key: RunComponents(pods=pods, config_map=cm_grouping.get(key, CONFIG_NOT_FOUND))
        for key, pods in pod_grouping.items()
    }


def _run_from_components(
    run_components: Dict[str, RunComponents],
    statuses: Optional[Sequence[str]] = None,
) -> List[Run]:
    """Extract the details for a :type Run: from a run's pods and configmaps
    """

    if statuses:
        valid_statuses = {RunStatus.from_string(status) for status in statuses}
    else:
        valid_statuses: Set[RunStatus] = set(RunStatus)

    dummy_run_data = {
        'run_uid': '',
    }

    runs: List[Run] = []
    for name, components in run_components.items():

        # There will always be at least one pod associated with a job
        pod = components.pods[0]

        # Extract pod status
        status = ContextPodStatus.aggregate([ContextPodStatus.from_pod_dict(pod_dict) for pod_dict in components.pods
                                            ]).state
        if status not in valid_statuses:
            continue

        run_data: Dict[str, Any] = dummy_run_data.copy()
        run_data['name'] = name
        run_data['status'] = status

        if components.config_map and components.config_map != CONFIG_NOT_FOUND:
            config = FinalRunConfig(**yaml.safe_load(components.config_map['data'][RUN_CONFIG_FILE_NAME]))
        else:
            config = _extract_run_config(pod)

        # Extract times
        run_data['created_at'] = dt.datetime.fromisoformat(pod['metadata']['creationTimestamp'])

        # Add optional start and stop times
        run_data['completed_at'] = _get_end_time(pod)
        run_data['started_at'] = _get_start_time(pod)

        # Add updated time
        run_data['updated_at'] = _get_update_time(pod)

        # Get job type
        run_data['_type'] = _get_job_type(pod)

        run_data['config'] = config
        runs.append(Run(**run_data))

    return runs


def _extract_run_config(pod: Dict[str, Any]) -> FinalRunConfig:
    """Extract the :type FinalRunConfig: as best we can from one of a run's pods

    NOTE: This is only used as a fallback for runs performed before the
    :type FinalRunConfig: was stored in the run's configmap. As such, we will only
    extract information relevant for `mcli get runs`.
    """

    config_data = {
        'run_id': '',
        'name': '',
        'cpus': -1,
        'image': '',
        'optimization_level': 0,
        'command': '',
        'integrations': [],
        'env_variables': [],
        'parameters': {},
    }

    pod_labels: Dict[str, str] = dict(pod['metadata'].get('labels', {}))
    labels_to_get = [label.compute.LABEL_mcli_cluster, label.compute.LABEL_GPU_TYPE, label.compute.LABEL_GPU_NUM]
    label_vals = extract_label_values(pod_labels, labels_to_get, default='-')
    config_data['gpu_type'] = label_vals[label.compute.LABEL_GPU_TYPE]
    config_data['gpu_num'] = int(label_vals[label.compute.LABEL_GPU_NUM])
    config_data['cluster'] = label_vals[label.compute.LABEL_mcli_cluster]

    # Try to get image
    try:
        image = pod['spec']['containers'][0]['image']
        config_data['image'] = image
    except (KeyError, IndexError):
        pass

    return FinalRunConfig(**config_data)


def _get_end_time(pod_dict: Dict[str, Any]) -> Optional[dt.datetime]:
    """Get a pod's end time from its container statuses
    """
    try:
        container_status = pod_dict['status']['containerStatuses'][0]
        terminated = container_status['state'].get('terminated')
        if terminated:
            return dt.datetime.fromisoformat(terminated['finishedAt'])
    except (KeyError, IndexError):
        pass


def _get_start_time(pod_dict: Dict[str, Any]) -> Optional[dt.datetime]:
    """Get a pod's start time

    note: pod startTime not the container start time. Useful for
    cost estimation and may be slightly less than container due
    to the time needed to pull the image inside the container
    """
    try:
        return dt.datetime.fromisoformat(pod_dict['status']['startTime'])
    except KeyError:
        pass


def _get_update_time(pod_dict: Dict[str, Any]) -> dt.datetime:
    """Get the last timestamp in metadata and status"""
    timestamps: List[dt.datetime] = [dt.datetime.fromisoformat(pod_dict['metadata']['creationTimestamp'])]

    status = pod_dict.get('status', {})

    # Get update time from each condition
    timestamps += [
        dt.datetime.fromisoformat(cond['lastTransitionTime'])
        for cond in status.get('conditions', [])
        if 'lastTransitionTime' in cond
    ]

    # Add container status
    if status.get('containerStatuses', []):
        container_status = status['containerStatuses'][0]
        state = container_status.get('state', {})
        if state.get('terminated'):
            timestamps.append(dt.datetime.fromisoformat(state['terminated']['finishedAt']))
        elif state.get('running'):
            timestamps.append(dt.datetime.fromisoformat(state['running']['startedAt']))

    return max(timestamps)


def _get_job_type(pod_dict: Dict[str, Any]) -> Optional[MCLIJobType]:
    """Extract the "job type" from the pod's labels
    """
    pod_labels: Dict[str, str] = dict(pod_dict['metadata'].get('labels', {}))
    labels_to_get = [label.mosaic.JOB_TYPE]
    label_vals = extract_label_values(pod_labels, labels_to_get, default='')
    job_type_str = label_vals.get(label.mosaic.JOB_TYPE)
    try:
        # Return if it's a valid label, otherwise leave as None
        return MCLIJobType(job_type_str)
    except:  # pylint: disable=bare-except
        return


@overload
def get_runs(
    runs: Optional[Union[List[str], List[Run]]] = None,
    clusters: Optional[Union[List[str], List[Cluster]]] = None,
    gpu_types: Optional[Union[List[str], List[GPUType]]] = None,
    gpu_nums: Optional[List[int]] = None,
    statuses: Optional[Union[List[str], List[RunStatus]]] = None,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> List[Run]:
    ...


@overload
def get_runs(
    runs: Optional[Union[List[str], List[Run]]] = None,
    clusters: Optional[Union[List[str], List[Cluster]]] = None,
    gpu_types: Optional[Union[List[str], List[GPUType]]] = None,
    gpu_nums: Optional[List[int]] = None,
    statuses: Optional[Union[List[str], List[RunStatus]]] = None,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[List[Run]]:
    ...


def get_runs(
    runs: Optional[Union[List[str], List[Run]]] = None,
    clusters: Optional[Union[List[str], List[Cluster]]] = None,
    gpu_types: Optional[Union[List[str], List[GPUType]]] = None,
    gpu_nums: Optional[List[int]] = None,
    statuses: Optional[Union[List[str], List[RunStatus]]] = None,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """Get a filtered list of runs

    List runs that have been launched in the MosaicML Cloud. The returned list will
    contain all of the details stored about the requested runs.

    Arguments:
        runs (``Optional[List[str] | List[``:class:`~mcli.api.model.run.Run` ``]]``):
            List of run names on which to get information
        clusters (``Optional[List[str] | List[``:class:`~mcli.models.mcli_cluster.Cluster` ``]]``):
            List of clusters to filter runs. This can be a list of str or
            :class:`~mcli.models.mcli_cluster.Cluster`
            objects. Only runs submitted to these clusters will be returned.
        gpu_types (``Optional[List[str] | List[``:class:`~mcli.serverside.clusters.gpu_type.GPUType` ``]]``):
            List of gpu types to filter runs. This can be a list of str or
            :class:`~mcli.serverside.clusters.gpu_type.GPUType`
            enums. Only runs scheduled on these GPUs will be returned.
        gpu_nums (``Optional[List[int]]``): List of gpu counts to filter runs. Only runs
            scheduled on this number of GPUs will be returned.
        statuses (``Optional[List[str]|List[``:class:`~mcli.utils.utils_run_status.RunStatus` ``]]``):
            List of run statuses to filter runs. This can be a list of str or
            :class:`~mcli.utils.utils_run_status.RunStatus` enums. Only runs currently in
            these phases will be returned.
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to :func:`get_runs` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the list of :class:`~mcli.api.model.run.Run` output,
            use ``return_value.result()`` with an optional ``timeout`` argument.

    Raises:
        :class:`~mcli.api.exceptions.MAPIException`: If connecting to MAPI, raised when
            a MAPI communication error occurs
        :class:`~mcli.api.exceptions.KubernetesException`: Raised when a Kubernetes error
            occurs when communicating with only 1 cluster
        ``RuntimeError``: Raised when some error occurs in calls to multiple Kubernetes clusters

    Returns:
        If future is False:
            A list of requested :class:`~mcli.api.model.run.Run` objects
        Otherwise:
            A :class:`~concurrent.futures.Future` for the list
    """

    # Coerce arg types to strings
    run_names: Optional[List[str]] = None
    if runs is not None:
        run_names = [r.name if isinstance(r, Run) else r for r in runs]

    if clusters is not None:
        clusters = [pl.name if isinstance(pl, Cluster) else pl for pl in clusters]
    elif runs:
        # If runs were specified, pull clusters from them to speed up kube calls
        known_clusters = {r.config.cluster for r in runs if isinstance(r, Run)}
        clusters = list(known_clusters) or None

    if gpu_types is not None:
        gpu_types = [gt.name if isinstance(gt, GPUType) else gt for gt in gpu_types]

    if statuses is not None:
        statuses = [st.name if isinstance(st, RunStatus) else st for st in statuses]

    runs_future = _get_runs_kube(run_names, clusters, gpu_types, gpu_nums, statuses)

    if not future:
        return runs_future.result(timeout=timeout)
    else:
        return runs_future
