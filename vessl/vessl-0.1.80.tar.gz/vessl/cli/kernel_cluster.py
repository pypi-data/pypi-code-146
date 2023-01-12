from typing import List

import click

from openapi_client.models import ResponseKernelClusterInfo
from vessl.cli._base import VesslGroup, vessl_argument, vessl_option
from vessl.cli._util import (
    Endpoint,
    format_string,
    generic_prompter,
    print_data,
    print_table,
    prompt_choices,
)
from vessl.cli.organization import organization_name_option
from vessl.kernel_cluster import (
    _check_cluster_install_dependencies,
    _check_existing_vessl_installation,
    _install_k0s_in_docker,
    _load_cluster_kubeconfig,
    create_cluster,
    delete_cluster,
    list_cluster_nodes,
    list_clusters,
    read_cluster,
    rename_cluster,
)
from vessl.organization import _get_organization_name
from vessl.util.constant import CLUSTER_MODE_SINGLE
from vessl.util.exception import VesslRuntimeException


def cluster_name_prompter(ctx: click.Context, param: click.Parameter, value: str) -> str:
    clusters = list_clusters()
    return prompt_choices("Cluster", [x.name for x in clusters])


def custom_cluster_name_prompter(ctx: click.Context, param: click.Parameter, value: str) -> str:
    clusters = list_clusters()
    clusters = [x for x in clusters if not x.is_savvihub_managed]
    return prompt_choices("Cluster", [x.name for x in clusters])


@click.command(name="cluster", cls=VesslGroup)
def cli():
    pass


@cli.vessl_command()
@vessl_option(
    "--name",
    type=click.STRING,
    required=True,
    help="Name of the cluster. (e.g. 'seoul-cluster')",
)
@vessl_option(
    "--mode",
    type=click.STRING,
    default="single",
    help="Cluster installation mode; single|multinode. If mode=single, VESSL will be installed in a Docker container as a single-node mode.",
)
@vessl_option(
    "--kubernetes-namespace",
    type=click.STRING,
    default="vessl",
    help="Kubernetes namespace to install VESSL agent (default: vessl)",
)
@vessl_option(
    "--extra-helm-values",
    type=click.STRING,
    multiple=True,
    default=[],
    help="Extra Helm values to pass when installing VESSL agent.",
)
@organization_name_option
def create(name: str, mode: str, kubernetes_namespace: str, extra_helm_values: List[str]):
    _check_cluster_install_dependencies(mode)
    loaded, (config_path, context) = _load_cluster_kubeconfig(mode)
    if not loaded:
        if mode == CLUSTER_MODE_SINGLE:
            click.confirm(
                f"Kubernetes cluster not found; install kubernetes-in-docker on the machine?",
                abort=True,
            )
            config_path, context = _install_k0s_in_docker()
        else:
            raise VesslRuntimeException(
                "Kubernetes cluster not found; Please configure valid kubeconfig file location by KUBECONFIG envvar or install Kubernetes on the machine."
            )

    vessl_installation_info = _check_existing_vessl_installation()
    if vessl_installation_info is not None:
        print_cluster_data(vessl_installation_info)
        return

    input_data = {
        "VESSL cluster name": name,
        "Kubeconfig path": config_path,
        "Current kubernetes context": context,
        "Kubernetes namespace": kubernetes_namespace,
    }
    if extra_helm_values and len(extra_helm_values) > 0:
        input_data["Extra Helm values"] = ", ".join(extra_helm_values)

    print_data(input_data)
    click.confirm(
        f"Are you sure you want to install VESSL agent on current Kubernetes cluster?",
        abort=True,
    )
    vessl_installation_info = create_cluster(
        cluster_name=name,
        kubernetes_namespace=kubernetes_namespace,
        kubeconfig_path=config_path,
        extra_helm_values=extra_helm_values,
    )
    print(f"cluster {name} created!")
    print_cluster_data(vessl_installation_info)


@cli.vessl_command()
@vessl_argument("name", type=click.STRING, required=True, prompter=cluster_name_prompter)
@organization_name_option
def read(name: str):
    cluster = read_cluster(cluster_name=name)
    print_cluster_data(cluster)


@cli.vessl_command()
@organization_name_option
def list():
    clusters = list_clusters()
    print_table(
        clusters,
        ["ID", "Name", "Type", "Status", "K8s Master Endpoint", "K8s Namespace"],
        lambda x: [
            x.id,
            x.name,
            "Managed" if x.is_savvihub_managed else "Custom",
            x.status.replace("-", " "),
            format_string(x.name),
            format_string(x.kubernetes_namespace),
        ],
    )


@cli.vessl_command()
@vessl_argument("name", type=click.STRING, required=True, prompter=custom_cluster_name_prompter)
@organization_name_option
def delete(name: str):
    click.confirm(f"Are you sure you want to delete '{name}'?", abort=True)
    cluster = read_cluster(cluster_name=name)
    data = delete_cluster(cluster_id=cluster.id)
    print(f"Deleted '{name}'.")
    print(f"Note that this command does NOT destroy your kubernetes cluster.")
    print(f"If you want to destroy the cluster installed with VESSL CLI,")
    print(f"try execute the following in the shell (note that this is NOT RECOVERABLE).")
    print(f"$ docker stop vessl-k0s && docker rm vessl-k0s")
    print(
        f'$ docker run -it --rm --privileged --pid=host alpine nsenter -t 1 -m -- sh -c "rm -rfv /var/lib/k0s"'
    )


@cli.vessl_command()
@vessl_argument("name", type=click.STRING, required=True, prompter=custom_cluster_name_prompter)
@vessl_argument("new_name", type=click.STRING, required=True, prompter=generic_prompter("New name"))
@organization_name_option
def rename(name: str, new_name: str):
    cluster = read_cluster(cluster_name=name)
    cluster = rename_cluster(cluster_id=cluster.id, new_cluster_name=new_name)
    print(f"Renamed '{name}' to '{cluster.name}'.")


@cli.vessl_command()
@vessl_argument("name", type=click.STRING, required=True, prompter=custom_cluster_name_prompter)
@organization_name_option
def list_nodes(name: str):
    cluster = read_cluster(cluster_name=name)
    cluster_nodes = list_cluster_nodes(cluster_id=cluster.id)
    print_table(
        cluster_nodes,
        ["ID", "Name", "CPU Limits", "GPU Limits", "Memory Limits"],
        lambda x: [x.id, x.name, x.cpu_limits, x.gpu_limits, x.memory_limits],
    )


def cluster_id_prompter(ctx: click.Context, param: click.Parameter, value: str) -> int:
    clusters = list_clusters()
    cluster = prompt_choices(
        "Cluster",
        [(f"{x.name}", x) for x in clusters],
    )
    ctx.obj["cluster"] = cluster
    return cluster.id


def cluster_name_prompter(ctx: click.Context, param: click.Parameter, value: str) -> str:
    clusters = list_clusters()
    cluster = prompt_choices(
        "Cluster",
        [(f"{x.name}", x) for x in clusters],
    )
    ctx.obj["cluster"] = cluster
    return cluster.name


def cluster_name_callback(ctx: click.Context, param: click.Parameter, value: str) -> str:
    if "cluster" not in ctx.obj:
        ctx.obj["cluster"] = read_cluster(value)
    return value


def print_cluster_data(cluster: ResponseKernelClusterInfo, **kwargs):
    print_data(
        {
            "Name": cluster.name,
            "Dashboard URL": Endpoint.cluster.format(_get_organization_name(**kwargs), cluster.id),
            "Type": "VESSL-managed" if cluster.is_savvihub_managed else "Custom",
            "Region": format_string(cluster.region),
            "Status": cluster.status.replace("-", " "),
            "K8s Master Endpoint": format_string(cluster.name),
            "K8s Namespace": format_string(cluster.kubernetes_namespace),
            "K8s Service Type": cluster.kubernetes_service_type,
        }
    )


cluster_option = vessl_option(
    "-c",
    "--cluster",
    type=click.STRING,
    required=True,
    prompter=cluster_name_prompter,
    callback=cluster_name_callback,
    help="Must be specified before resource-related options (`--resource`, `--processor`, ...).",
)
