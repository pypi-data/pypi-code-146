""" Test Platform """
from typing import Tuple

import pytest

from mcli.models.mcli_cluster import Cluster
from mcli.serverside.clusters.cluster import GenericK8sCluster, InvalidPriorityError, PriorityLabel
from mcli.serverside.clusters.instance_type import InstanceType
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob


@pytest.fixture
def mcli_job():
    job = MCLIK8sJob.empty('test')
    job.container.image = 'alpine'
    job.container.command = ['sleep', 'infinity']
    return job


@pytest.fixture(autouse=True)
def fake_secrets(mocker):
    from mcli.serverside.clusters import cluster
    mocker.patch.object(cluster.SecretManager, 'add_secrets_to_job', return_val=None)


def test_priority_label_ensure_enum():

    assert PriorityLabel.ensure_enum(PriorityLabel.low).name == 'low'
    assert PriorityLabel.ensure_enum('low').name == 'low'

    with pytest.raises(ValueError):
        PriorityLabel.ensure_enum(12345)  # type: ignore

    with pytest.raises(ValueError):
        PriorityLabel.ensure_enum('safasdfasdz')


def get_cluster_and_instance(cluster_name: str) -> Tuple[GenericK8sCluster, InstanceType]:
    # Get k8s cluster
    mcli_cluster = Cluster(cluster_name, cluster_name, 'test')
    k8s_cluster = GenericK8sCluster.from_mcli_cluster(mcli_cluster)

    # Get instance type
    first_instance = list(k8s_cluster.allowed_instances.instance_type_map.values())[0]

    return k8s_cluster, first_instance


@pytest.mark.parametrize('priority_name', ('low', 'standard', 'high'))
def test_get_specs_priority(
    mcli_job: MCLIK8sJob,
    priority_name: str,
):
    """Test that r1z1 cluster priorities get set properly within the resulting job spec

    Args:
        mcli_job: Simple MCLIK8sJob
        priority_name (str): Priority class name
    """
    # Get r1z1 cluster and instance
    k8s_cluster, instance_type = get_cluster_and_instance('r1z1')

    # Get specs with priority_class
    k8s_cluster.prepare_kubernetes_job_for_cluster(
        kubernetes_job=mcli_job,
        instance_type=instance_type,
        priority_class=priority_name,
    )

    # Validate correct priority class
    assert mcli_job.pod_spec.priority_class_name == k8s_cluster.priority_class_labels[priority_name]


def test_get_specs_priority_default(mcli_job: MCLIK8sJob):
    """Test that r1z1 cluster priorities properly handle a priority of None as default

    Args:
        mcli_job: Simple MCLIK8sJob
    """
    # Get r1z1 cluster and instance
    k8s_cluster, instance_type = get_cluster_and_instance('r1z1')

    # Get specs with priority_class
    k8s_cluster.prepare_kubernetes_job_for_cluster(
        kubernetes_job=mcli_job,
        instance_type=instance_type,
        priority_class=None,
    )

    # Validate correct priority class
    assert k8s_cluster.default_priority_class is not None
    default_priority = k8s_cluster.priority_class_labels[k8s_cluster.default_priority_class]
    assert mcli_job.pod_spec.priority_class_name == default_priority


@pytest.mark.parametrize('cluster_name', ['r7z4'])
def test_get_specs_priority_none(
    mcli_job: MCLIK8sJob,
    cluster_name: str,
):
    """Test that a few clusters priorities properly handle a priority of None

    Args:
        mcli_job: Simple MCLIK8sJob
        cluster_name (str): Name of the cluster
    """
    # Get cluster and instance
    k8s_cluster, instance_type = get_cluster_and_instance(cluster_name)

    # Get specs with priority_class
    k8s_cluster.prepare_kubernetes_job_for_cluster(
        kubernetes_job=mcli_job,
        instance_type=instance_type,
        priority_class=None,
    )

    # Validate correct priority class
    assert mcli_job.pod_spec.priority_class_name == None


@pytest.mark.parametrize('cluster_name', ('r1z1', 'r7z1'))
def test_get_specs_priority_invalid(
    mcli_job: MCLIK8sJob,
    cluster_name: str,
):
    """Test that a few clusters priorities properly handle an incorrect priority name

    Args:
        mcli_job: Simple MCLIK8sJob
        cluster_name (str): Name of the cluster
    """
    # Get cluster and instance
    k8s_cluster, instance_type = get_cluster_and_instance(cluster_name)

    # Raises InvalidPriorityError
    with pytest.raises(InvalidPriorityError):
        k8s_cluster.prepare_kubernetes_job_for_cluster(
            kubernetes_job=mcli_job,
            instance_type=instance_type,
            priority_class='not-a-real-priority',
        )


@pytest.mark.parametrize('cluster_name', ('r1z2', 'r7z7', 'r10z1'))
def test_sys_ptrace_added(mcli_job: MCLIK8sJob, cluster_name: str):
    # Get cluster and instance
    k8s_cluster, instance_type = get_cluster_and_instance(cluster_name)

    # Get specs with security context
    k8s_cluster.prepare_kubernetes_job_for_cluster(
        kubernetes_job=mcli_job,
        instance_type=instance_type,
    )

    # Validate correct capabilities
    assert "SYS_PTRACE" in mcli_job.container.security_context.capabilities.add


@pytest.mark.parametrize('cluster_name', ('r7z5',))
def test_sys_ptrace_not_added(mcli_job: MCLIK8sJob, cluster_name: str):
    # Get cluster and instance
    k8s_cluster, instance_type = get_cluster_and_instance(cluster_name)

    # Get specs without ptrace
    k8s_cluster.prepare_kubernetes_job_for_cluster(
        kubernetes_job=mcli_job,
        instance_type=instance_type,
    )

    # Validate correct priority class
    try:
        # capabilities MAY exist for other reasons. Great if they don't, though
        caps = mcli_job.container.security_context.capabilities.add
    except:
        pass
    else:
        # If caps did exist, at least make sure SYS_PTRACE not in them
        assert "SYS_PTRACE" not in caps


INTERACTIVE_CLUSTERS = ['r1z2', 'r7z7', 'r8z2', 'r10z1']
NONINTERACTIVE_CLUSTERS = ['r1z1', 'r7z2']


@pytest.mark.parametrize('cluster_name', INTERACTIVE_CLUSTERS)
def test_clusters_interactive(cluster_name: str):
    cluster = Cluster(name=cluster_name, kubernetes_context=cluster_name, namespace='test')
    k8s_cluster = GenericK8sCluster.from_mcli_cluster(cluster)
    assert k8s_cluster.interactive is True


@pytest.mark.parametrize('cluster_name', NONINTERACTIVE_CLUSTERS)
def test_clusters_noninteractive(cluster_name: str):
    cluster = Cluster(name=cluster_name, kubernetes_context=cluster_name, namespace='test')
    k8s_cluster = GenericK8sCluster.from_mcli_cluster(cluster)
    assert k8s_cluster.interactive is False
