import logging
from pkg_resources import get_distribution, DistributionNotFound
from executor_dkr._config import DAG_NAME, DAG_VERSION, DockerResource  # noqa: F401
try:
    __version__ = get_distribution("executor-dkr").version
except DistributionNotFound:
    __version__ = 'local'

K8S_DAG = 'com.daggerml.resource.k8s'
K8S_VERSION = 1


logger = logging.getLogger(__name__)


def build(dag, resource):
    """build a docker image

    Parameters
    ----------
    dag : daggerml.Dag
        the dag that this image will be built for
    resource : executor_s3.S3Resource
        a tarball stored on s3 with a Dockerfile at its root.

    Returns
    -------
    DockerResource
        the docker image
    """
    fn = dag.load(DAG_NAME, DAG_VERSION)
    return fn(resource)


def run(dag, image, *args):
    """run a docker image on kubernetes

    Parameters
    ----------
    dag : daggerml.Dag
        the dag that this image will be built for
    image : DockerResource
        the docker image you want to run

    Returns
    -------
    Node
        the result of running that image
    """
    k8s = dag.load(K8S_DAG, K8S_VERSION)
    f = dag.from_py([k8s, image])
    return f(*args)
