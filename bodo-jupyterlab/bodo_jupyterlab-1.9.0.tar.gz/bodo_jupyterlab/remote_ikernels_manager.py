from cachetools import TTLCache, cached
from cachetools.keys import hashkey
from remote_ikernel.manage import (
    add_kernel,
    delete_kernel,
    get_existing_kernel_specs,
)

from .platform import PlatformClusterManager
from .config import KERNEL_NAME, KERNEL_DIR, KERNEL_CMD, KERNEL_CLEANUP_PERIOD_SECONDS
import random

KERNEL_METADATA_CLUSTER_UUID_FIELD = "BodoClusterUUID"
KERNEL_METADATA_HOSTNAME_FIELD = "hostname"


def kernel_for_cluster_exists(cluster_uuid: str):
    existing_kernel_specs = get_existing_kernel_specs()
    for _, spec in existing_kernel_specs.items():
        kernel_cluster_uuid = spec.metadata.get(
            KERNEL_METADATA_CLUSTER_UUID_FIELD, None
        )
        if kernel_cluster_uuid and kernel_cluster_uuid == cluster_uuid:
            return True

    return False


def get_kernel_for_cluster(cluster_uuid: str):
    existing_kernel_specs = get_existing_kernel_specs()
    for kernel_name, spec in existing_kernel_specs.items():
        kernel_cluster_uuid = spec.metadata.get(
            KERNEL_METADATA_CLUSTER_UUID_FIELD, None
        )
        kernel_hostname = spec.metadata.get(KERNEL_METADATA_HOSTNAME_FIELD, None)
        if kernel_cluster_uuid and kernel_cluster_uuid == cluster_uuid:
            return kernel_hostname, kernel_name
    raise KeyError(f"Could not find kernel spec for cluster_uuid: {cluster_uuid}")


def get_remote_kernel_name_for_cluster(
    cluster_uuid,
    hostnames,
    logger,
    tunnel_host,
    tunnel_host_user,
    cluster_user,
    ssh_key_fname=None,
):
    logging_prefix = f"[GetKernelNameForCluster][UUID: {cluster_uuid}]"
    logger.info(f"{logging_prefix} hostname: {hostnames}")
    # Check if a kernelspec for this cluster already exists
    if kernel_for_cluster_exists(cluster_uuid):
        logger.info(f"{logging_prefix} Found an existing remote kernel")
        hostname, kname = get_kernel_for_cluster(cluster_uuid)
        logger.info(f"{logging_prefix} Existing kernel: {kname}, hostname: {hostname}")
        # Check that this hostname is valid
        if hostname in hostnames:
            logger.info(
                f"{logging_prefix} {hostname} is a valid host. Returning kernel: {kname}"
            )
            return kname
        # If not a valid hostname anymore, delete this kernelspec
        else:
            logger.info(
                f"{logging_prefix} Deleting kernel {kname} since the hostname is not valid anymore."
            )
            delete_kernel(kname)

    # If not select a hostname randomly and create a remote kernel for it
    selected_hostname = random.choice(hostnames)
    logger.info(
        f"{logging_prefix} Couldn't find any existing kernels. Randomly selected {selected_hostname} as the kernel host."
    )
    kernel_name = add_remote_kernel(
        selected_hostname,
        cluster_uuid,
        cluster_user,
        ssh_key_fname,
        tunnel_host=tunnel_host,
        tunnel_host_user=tunnel_host_user,
    )
    logger.info(f"{logging_prefix} Created kernel: {kernel_name}")
    logger.info(f"{logging_prefix} Returing kernel_name: {kernel_name}")
    return kernel_name


def add_remote_kernel(
    hostname,
    cluster_uuid,
    cluster_user=None,
    ssh_key_fname=None,
    dryrun=False,
    tunnel_host=None,
    tunnel_host_user=None,
):
    # If username isn't set for hostname or tunnel_host set it to default
    if "@" not in hostname and cluster_user:
        hostname = f"{cluster_user}@{hostname}"
    if tunnel_host and "@" not in tunnel_host and tunnel_host_user:
        tunnel_host = f"{tunnel_host_user}@{tunnel_host}"

    kernel_name, _ = add_kernel(
        interface="ssh",
        name=KERNEL_NAME,
        kernel_cmd=KERNEL_CMD,
        host=hostname,
        launch_args=f"-i {ssh_key_fname}" if ssh_key_fname else None,
        kerneldir=KERNEL_DIR,
        dryrun=dryrun,
        tunnel_hosts=[tunnel_host] if tunnel_host else None,
        metadata={
            KERNEL_METADATA_CLUSTER_UUID_FIELD: cluster_uuid,
            KERNEL_METADATA_HOSTNAME_FIELD: hostname,
        },
    )
    return kernel_name


# Can only be called once every KERNEL_CLEANUP_PERIOD_SECONDS seconds
@cached(
    cache=TTLCache(maxsize=2, ttl=KERNEL_CLEANUP_PERIOD_SECONDS),
    key=lambda logger, cluster_uuids: hashkey("A"),
)
def cleanup_kernelspecs(logger, active_cluster_uuids):
    """
    Clean up kernel specs jupyter instance
    :param logger: Logger object
    :param active_cluster_uuids: Set of all cluster uuids that are not in FAILED/TERMINATED state
    """
    logging_prefix = "[KernelSpecs Cleanup]"
    logger.info(f"{logging_prefix} Starting...")
    logger.info(f"{logging_prefix} cluster_uuids: {active_cluster_uuids}")

    # Get existing remote kernel specs
    existing_kernel_specs = get_existing_kernel_specs()
    logger.info(f"{logging_prefix} existing_kernel_specs: {existing_kernel_specs}")

    # If the cluster UUID associated with any of the existing kernel specs
    # is not an active cluster, then remove it
    for kernel_name, spec in existing_kernel_specs.items():
        kernel_cluster_uuid = spec.metadata.get(
            KERNEL_METADATA_CLUSTER_UUID_FIELD, None
        )
        if kernel_cluster_uuid and kernel_cluster_uuid not in active_cluster_uuids:
            logger.info(f"{logging_prefix} Deleting kernel {kernel_name}")
            delete_kernel(kernel_name)
