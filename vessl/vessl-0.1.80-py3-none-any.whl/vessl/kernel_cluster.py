import base64
import socket
import subprocess
from platform import uname
from shutil import which
from time import sleep
from typing import List, Optional, Tuple

import docker
from kubernetes import client as k8sclient
from kubernetes import config
from kubernetes.config import KUBE_CONFIG_DEFAULT_LOCATION

from openapi_client.models import (
    ClusterUpdateAPIInput,
    ResponseKernelClusterInfo,
    ResponseKernelClusterNodeInfo,
)
from vessl import vessl_api
from vessl.organization import _get_organization_name
from vessl.util import logger
from vessl.util.config import DEFAULT_VESSL_DIR
from vessl.util.constant import CLUSTER_MODE_MULTI_NODE, CLUSTER_MODE_SINGLE
from vessl.util.exception import (
    ClusterNotFoundError,
    InvalidKernelClusterError,
    VesslApiException,
    VesslRuntimeException,
)


def create_cluster(
    cluster_name: str,
    kubernetes_namespace: str = "vessl",
    extra_helm_values: List[str] = [],
    kubeconfig_path: str = "",
    **kwargs,
) -> ResponseKernelClusterInfo:
    """Create a VESSL cluster by installing VESSL agent to given Kubernetes
    namespace. If you want to override the default organization, then pass
    `organization_name` as `**kwargs`.

    Args:
        cluster_name(str): Cluster name.
        kubernetes_namespace(str): Kubernetes namespace to install VESSL agent.
            defaults to "vessl".
        extra_helm_values(list[str]): Helm values to pass to cluster install
            command. See https://github.com/vessl-ai/cluster-resources/blob/main/helm-chart/values.yaml
            for available Helm values.
        kubeconfig_path(str): Path to kubeconfig file.

    Example:
        ```python
        vessl.install_cluster(
            cluster_name="seoul-cluster",
        )
        ```
    """
    agent_access_token = vessl_api.custom_cluster_key_api(
        organization_name=_get_organization_name(**kwargs),
    ).access_token

    logger.debug(f"cluster name: '{cluster_name}'")
    logger.debug(f"access token: '{agent_access_token}'")

    subprocess.check_call(
        [
            "helm",
            "repo",
            "add",
            "vessl",
            "https://vessl-ai.github.io/cluster-resources/helm-chart",
        ]
    )
    subprocess.check_call(["helm", "repo", "update"])

    cluster_install_command = [
        "helm",
        "install",
        "vessl",
        "vessl/cluster-resources",
        "--kubeconfig",
        kubeconfig_path,
        "--namespace",
        kubernetes_namespace,
        "--create-namespace",
        "--set",
        f"agent.clusterName={cluster_name}",
        "--set",
        f"agent.accessToken={agent_access_token}",
    ]

    for helm_value in extra_helm_values:
        cluster_install_command.extend(["--set", helm_value])

    # dcgm patch
    v1 = k8sclient.CoreV1Api()
    # @XXX(seokju) rough assumption: k0s user will install k0s nodes
    # if this becomes a problem, patch chart and cli.
    node = v1.list_node().items[0]
    if "k0s" in node.status.node_info.kubelet_version:
        cluster_install_command.extend(
            [
                "--set",
                ".metricsExporters.dcgmExporter.podResourcePath=/var/lib/k0s/kubelet/pod-resources",
            ]
        )

    subprocess.check_call(cluster_install_command)

    logger.warn(
        "VESSL cluster agent installed. Waiting for the agent to be connected with VESSL..."
    )
    for attempts in range(18):
        sleep(10)
        try:
            return vessl_api.custom_cluster_connectivity_api(
                organization_name=_get_organization_name(**kwargs),
                agent_access_token=agent_access_token,
            )
        except VesslApiException as e:
            if e.code == "NotFound":
                continue
            raise e

    raise ClusterNotFoundError(
        "Timeout for checking agent connection; Please check agent log for more information."
    )


def _check_cluster_install_dependencies(mode: str):
    """Check if dependencies required for cluster creation has installed on
    the machine."""
    if mode == CLUSTER_MODE_SINGLE:
        try:
            logger.debug("Cluster install: checking if Docker daemon is running")
            docker.from_env()
        except docker.errors.DockerException as e:
            raise VesslRuntimeException(
                f"Error response from Docker daemon: {repr(e)}; Please install Docker to run VESSL on your machine."
            )

    logger.debug("Cluster install: checking if Helm binary exists in local")
    if which("helm") is None:
        raise VesslRuntimeException(
            "Command 'helm' not found; Please install Helm to install VESSL cluster agent: https://helm.sh/"
        )


def _load_cluster_kubeconfig(
    mode: str,
) -> Tuple[bool, Tuple[Optional[str], Optional[str]]]:
    """Find and load kubeconfig for VESSL cluster installation.

    Returns:
        True, if valid kubernetes config has loaded
        False, if no valid kubernetes config has found
    """
    cluster_kubeconfig = _get_cluster_kubeconfig()
    config_files = [cluster_kubeconfig] if cluster_kubeconfig else []
    if mode == CLUSTER_MODE_MULTI_NODE:
        config_files.append("/var/lib/k0s/pki/admin.conf")
    config_files.append(KUBE_CONFIG_DEFAULT_LOCATION)

    for config_file in config_files:
        try:
            config.load_kube_config(config_file)
            _, current_context = config.list_kube_config_contexts(config_file)
            logger.info(
                f"Using kubeconfig from file: {config_file} / context: {current_context['name']}"
            )
            return True, (config_file, current_context["name"])
        except config.config_exception.ConfigException as e:
            logger.warn(f"Cluster install: load kubeconfig from {config_file} failed: {repr(e)}")

    return False, (None, None)


def _install_k0s_in_docker() -> Tuple[str, str]:
    """Install k0s-in-Docker on local machine."""
    logger.info(f"Installing k0s-in-docker ...")
    k0s_config = """apiVersion: k0s.k0sproject.io/v1beta1
kind: ClusterConfig
metadata:
  name: k0s
spec:
  api:
    extraArgs:
      service-node-port-range: 32639-32767
"""
    kwargs = {
        "name": "vessl-k0s",
        "environment": {"K0S_CONFIG": k0s_config},
        "hostname": f"vessl-k0s-{socket.gethostname()}",
        "ports": {
            "6443/tcp": 6443,
        },
        "privileged": True,
        "volumes": {
            "/var/lib/k0s": {
                "bind": "/var/lib/k0s",
                "mode": "rw",
            },
        },
    }
    for i in range(32639, 32768):
        kwargs["ports"][f"{i}/tcp"] = i

    # Add extra arguments for arm64 machines
    if uname().machine == "arm64":
        logger.debug("System is using CPU with arm64 architecture; adding additional kwargs")
        kwargs["environment"]["ETCD_UNSUPPORTED_ARCH"] = "arm64"

    client = docker.from_env()

    # Add extra arguments for docker container running on Docker Desktop
    if client.info().get("OperatingSystem", "") == "Docker Desktop":
        logger.debug("Docker is running on Docker Desktop; adding additional kwargs")
        kwargs["cgroupns"] = "host"
        kwargs["volumes"]["/sys/fs/cgroup"] = {
            "bind": "/sys/fs/cgroup",
            "mode": "rw",
        }

    # Run k0s container
    container = client.containers.run(
        detach=True,
        image="docker.io/k0sproject/k0s:v1.23.9-k0s.0",
        command="k0s controller --single --no-taints --config /etc/k0s/config.yaml",
        **kwargs,
    )

    # Wait for the container to be ready
    node_ready = False
    trial_limit = 10
    for trial in range(trial_limit):
        logger.info(f"Checking for the k0s-in-docker node to be ready... ({trial+1}/{trial_limit})")
        res = container.exec_run(
            "bash -c 'k0s kubectl get nodes --no-headers=true | grep -v NotReady | wc -l'",
            stream=False,
            demux=True,
        )
        output, err = res.output
        if output:
            logger.debug(output.decode("utf-8"))
            nodes = output.decode("utf-8").strip()
            if nodes == "1":
                node_ready = True
                break
        if err:
            logger.debug(err.decode("utf-8"))
        sleep(10)
    if not node_ready:
        container.kill()
        raise VesslRuntimeException("Timeout while waiting for k0s-in-docker node. Please retry.")

    # Get kubeconfig, keep at /opt/vessl/cluster_kubeconfig.yaml for later
    logger.debug("Acquiring kubeconfig")
    res = container.exec_run("cat /var/lib/k0s/pki/admin.conf", stream=False, demux=True)
    output, _ = res.output
    kubeconfig = output.decode("utf-8")
    kubeconfig_filename = f"{DEFAULT_VESSL_DIR}/cluster_kubeconfig.yaml"
    with open(kubeconfig_filename, "w") as f:
        f.write(kubeconfig)

    vessl_api.config_loader.cluster_kubeconfig = kubeconfig_filename
    config.load_kube_config(kubeconfig_filename)
    _, current_context = config.list_kube_config_contexts(kubeconfig_filename)
    logger.info(f"k0s-in-docker is ready! Saved kubeconfig at {kubeconfig_filename} for later use.")
    return kubeconfig_filename, current_context["name"]


def _check_existing_vessl_installation(**kwargs) -> ResponseKernelClusterInfo:
    """Check if there is existing vessl installation in current Kubernetes
    cluster."""

    # Find secret with name=vessl-agent, annotation=vessl
    try:
        v1 = k8sclient.CoreV1Api()
        vessl_secret: k8sclient.V1Secret = v1.read_namespaced_secret(
            name="vessl-agent", namespace="vessl"
        )
    except k8sclient.ApiException as e:
        if e.status != 404:
            raise VesslRuntimeException("Error while communicating with kubernetes.")
        return None

    # VESSL agent token is found - there is existing cluster in current kubernetes cluster
    logger.warn("Existing VESSL cluster installation found! getting cluster information...")
    vessl_access_token = vessl_secret.data.get("access-token")
    if vessl_access_token is None:
        raise InvalidKernelClusterError(
            "Kubernetes secret for VESSL found, but secret does not have access-token"
        )
    vessl_access_token = base64.b64decode(vessl_access_token)
    logger.debug(f"access token: {vessl_access_token}")
    return vessl_api.custom_cluster_connectivity_api(
        organization_name=_get_organization_name(**kwargs),
        agent_access_token=vessl_access_token,
    )


def read_cluster(cluster_name: str, **kwargs) -> ResponseKernelClusterInfo:
    """Read cluster in the default organization. If you want to override the
    default organization, then pass `organization_name` as `**kwargs`.

    Args:
        cluster_name(str): Cluster name.

    Example:
        ```python
        vessl.read_cluster(
            cluster_name="seoul-cluster",
        )
        ```
    """
    kernel_clusters = list_clusters(**kwargs)
    kernel_clusters = {x.name: x for x in kernel_clusters}

    if cluster_name not in kernel_clusters:
        raise InvalidKernelClusterError(f"Kernel cluster not found: {cluster_name}")
    return kernel_clusters[cluster_name]


def list_clusters(**kwargs) -> List[ResponseKernelClusterInfo]:
    """List clusters in the default organization. If you want to override the
    default organization, then pass `organization_name` as `**kwargs`.

    Example:
        ```python
        vessl.list_clusters()
        ```
    """
    return vessl_api.cluster_list_api(
        organization_name=_get_organization_name(**kwargs),
    ).clusters


def delete_cluster(cluster_id: int, **kwargs) -> object:
    """Delete custom cluster in the default organization. If you want to
    override the default organization, then pass `organization_name` as
    `**kwargs`.

    Args:
        cluster_id(int): Cluster ID.

    Example:
        ```python
        vessl.delete_cluster(
            cluster_id=1,
        )
        ```
    """
    return vessl_api.cluster_delete_api(
        cluster_id=cluster_id,
        organization_name=_get_organization_name(**kwargs),
    )


def rename_cluster(cluster_id: int, new_cluster_name: str, **kwargs) -> ResponseKernelClusterInfo:
    """Rename custom cluster in the default organization. If you want to
    override the default organization, then pass `organization_name` as
    `**kwargs`.

    Args:
        cluster_id(int): Cluster ID.
        new_cluster_name(str): Cluster name to change.

    Example:
        ```python
        vessl.rename_cluster(
            cluster_id=1,
            new_cluster_name="seoul-cluster-2",
        )
        ```
    """
    return vessl_api.cluster_update_api(
        cluster_id=cluster_id,
        organization_name=_get_organization_name(**kwargs),
        custom_cluster_update_api_input=ClusterUpdateAPIInput(
            name=new_cluster_name,
        ),
    )


def list_cluster_nodes(cluster_id: int, **kwargs) -> List[ResponseKernelClusterNodeInfo]:
    """List custom cluster nodes in the default organization. If you want to
    override the default organization, then pass `organization_name` as
    `**kwargs`.

    Args:
        cluster_id(int): Cluster ID.

    Example:
        ```python
        vessl.list_cluster_nodes(
            cluster_id=1,
        )
        ```
    """
    return vessl_api.custom_cluster_node_list_api(
        cluster_id=cluster_id,
        organization_name=_get_organization_name(**kwargs),
    ).nodes


def _get_cluster_kubeconfig(**kwargs) -> str:
    cluster_kubeconfig = kwargs.get("cluster_kubeconfig")
    if cluster_kubeconfig is not None:
        return cluster_kubeconfig
    if vessl_api.cluster_kubeconfig is not None:
        return vessl_api.cluster_kubeconfig

    return ""
