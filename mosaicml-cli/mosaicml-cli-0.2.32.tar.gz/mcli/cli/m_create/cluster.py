"""CLI creator for clusters"""
import argparse
import logging
import textwrap
from typing import Callable, List, Optional, Set

from kubernetes.config.config_exception import ConfigException

from mcli.api.exceptions import InputDisabledError, ValidationError
from mcli.config import MESSAGE, MCLIConfig, MCLIConfigError
from mcli.models import Cluster
from mcli.objects.secrets.cluster_secret import SecretManager
from mcli.utils.utils_interactive import choose_one, input_disabled, simple_prompt
from mcli.utils.utils_kube import KubeContext, get_kube_contexts
from mcli.utils.utils_logging import FAIL, OK, console
from mcli.utils.utils_string_functions import validate_rfc1123_name

logger = logging.getLogger(__name__)
INPUT_DISABLED_MESSAGE = ('Incomplete cluster. Please provide a name, context and namespace if running with '
                          '`--no-input`. Check `mcli create cluster --help` for more information.')

CLUSTER_EXAMPLES = """

Examples:

# Choose a cluster from a list of options
mcli create cluster

# Add the rXzX cluster
mcli create cluster rXzX

# Add a cluster with a custom name and namespace
mcli create cluster rXzX --name my-cluster --namespace my-user-namespace
"""


class ClusterValidationError(ValidationError):
    """Cluster could not be configured with the provided values
    """


class ClusterFillError(ValidationError):
    """Cluster could not have its details filled in
    """


class ClusterFiller():
    """Interactive filler for cluster data
    """

    @staticmethod
    def fill_context(available_contexts: List[KubeContext]) -> KubeContext:

        def print_kube_context(x):
            return x.name

        return choose_one('Which cluster would you like to set up?', available_contexts, formatter=print_kube_context)

    @staticmethod
    def fill_namespace(default: str, validate: Callable[[str], bool]) -> str:
        return simple_prompt('Which namespace will you be using?', default=default, validate=validate)


class ClusterValidator():
    """Validation methods for cluster data

    Raises:
        ClusterValidationError: Raised for any validation error for cluster data
    """

    @staticmethod
    def validate_contexts_available(contexts: List[KubeContext]) -> bool:
        if not contexts:
            raise ClusterValidationError('All clusters from your kubeconfig file have already been added.')
        return True

    @classmethod
    def validate_context_exists(cls, context: KubeContext, available_contexts: List[KubeContext]) -> bool:
        return cls.validate_context_name_exists(context.name, [kc.name for kc in available_contexts])

    @staticmethod
    def validate_context_name_exists(context_name: str, available_context_names: List[str]) -> bool:
        if context_name not in available_context_names:
            raise ClusterValidationError(f'No context named {context_name}. Available contexts are '
                                         f'{sorted(available_context_names)}')
        return True

    @staticmethod
    def validate_context_supported(context_name: str) -> bool:
        # pylint: disable-next=import-outside-toplevel
        from mcli.serverside.clusters.cluster import GenericK8sCluster
        if context_name not in GenericK8sCluster.get_k8s_context_map():
            raise ClusterValidationError(f'Context named {context_name} currently unsupported.')
        return True

    @staticmethod
    def validate_cluster_name_available(name: str, cluster_names: Set[str]) -> bool:
        if name in cluster_names:
            raise ClusterValidationError(f'Existing cluster. Cluster named {name} already exists. Please '
                                         f'choose something not in {sorted(list(cluster_names))}')
        return True

    @staticmethod
    def validate_namespace_rfc1123(namespace: str) -> bool:
        is_valid = validate_rfc1123_name(namespace)
        if not is_valid:
            raise ClusterValidationError(f'Invalid Kubernetes namespace. {is_valid.message}')
        return True


class ClusterCreator(ClusterValidator, ClusterFiller):
    """Creates clusters for the CLI
    """

    @staticmethod
    def get_all_clusters() -> List[Cluster]:
        conf: MCLIConfig = MCLIConfig.load_config()
        return conf.clusters

    @staticmethod
    def get_available_contexts(clusters: List[Cluster]):
        cluster_contexts = [x.kubernetes_context for x in clusters]
        kube_contexts = get_kube_contexts()
        return [x for x in kube_contexts if x.name not in cluster_contexts]

    @staticmethod
    def shortened_cluster_name_default(name: str) -> str:
        if len(name.split('-')) > 1:
            return name.split('-')[0]
        return name

    def create_all(self,) -> List[Cluster]:
        created_clusters = []
        all_clusters = self.get_all_clusters()
        unregistered_contexts = self.get_available_contexts(all_clusters)
        self.validate_contexts_available(unregistered_contexts)
        for unregistered_context in unregistered_contexts:
            cluster = self.create(
                name=None,
                kubernetes_context=unregistered_context.name,
                namespace=None,
            )
            created_clusters.append(cluster)
        return created_clusters

    def create(
        self,
        name: Optional[str],
        kubernetes_context: Optional[str],
        namespace: Optional[str],
    ) -> Cluster:
        all_clusters = self.get_all_clusters()
        cluster_names = {x.name for x in all_clusters}

        unregistered_contexts = self.get_available_contexts(all_clusters)
        self.validate_contexts_available(unregistered_contexts)
        available_context_map = {kc.name: kc for kc in unregistered_contexts}

        # Validate provided arguments
        new_context = None
        if kubernetes_context:
            self.validate_context_name_exists(kubernetes_context, list(available_context_map.keys()))
            new_context = available_context_map[kubernetes_context]

        if name:
            self.validate_cluster_name_available(name, cluster_names)

        if namespace:
            self.validate_namespace_rfc1123(namespace)

        # Fill remaining details
        if not new_context:
            new_context = self.fill_context(unregistered_contexts)
        name = name or self.shortened_cluster_name_default(new_context.name)

        if not namespace:
            namespace = new_context.namespace or self.fill_namespace(
                default='default',
                validate=self.validate_namespace_rfc1123,
            )

        self.validate_context_supported(new_context.name)
        return Cluster(name=name, kubernetes_context=new_context.name, namespace=namespace)


def create_new_cluster(
    name: Optional[str] = None,
    kubernetes_context: Optional[str] = None,
    namespace: Optional[str] = None,
    all_clusters: bool = False,
    no_input: bool = False,
    **kwargs,
) -> int:
    """Create a new cluster

    All required variables can be provided directly. If they are not provided, they will
    be requested interactively from the user unless `no_input` is `True`.

    Args:
        name: Name of the cluster. Defaults to None.
        kubernetes_context: Name of the associated kubernetes context. Defaults to None.
        namespace: Namespace of the associated kubernetes context. Defaults to None.
        no_input: If True, all required data must be provided since no interactive user
            input is allowed. Defaults to False.

    Returns:
        0 if creation succeeded, else 1
    """
    del kwargs

    creator = ClusterCreator()
    new_clusters_created = ''
    with input_disabled(no_input):
        try:
            if all_clusters:
                if name or kubernetes_context or namespace:
                    raise ValueError('When creating clusters with --all, not other arguments are allowed')
                all_created_clusters = creator.create_all()
                for created_cluster in all_created_clusters:
                    _setup_k8s_cluster(created_cluster)
                    _sync_cluster(created_cluster)
                new_clusters_created = ', '.join([x.name for x in all_created_clusters])
            else:
                new_cluster = create_one_cluster(creator,
                                                 name=name,
                                                 kubernetes_context=kubernetes_context,
                                                 namespace=namespace)
                new_clusters_created = new_cluster.name
        except MCLIConfigError:
            logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
            return 1
        except InputDisabledError:
            logger.error(INPUT_DISABLED_MESSAGE)
            return 1
        except ClusterValidationError as e:
            logger.error(f'{FAIL} {e}')
            return 1
        except ConfigException:
            logger.error(f'{FAIL} Could not find a valid kubeconfig file. If you think this is wrong, double-check '
                         'your `$KUBECONFIG` environment variable.')
            return 1

    logger.info(f'{OK} Created cluster: {new_clusters_created}')
    return 0


def create_one_cluster(
    creator: ClusterCreator,
    name: Optional[str] = None,
    kubernetes_context: Optional[str] = None,
    namespace: Optional[str] = None,
) -> Cluster:
    """Creates a single cluster and returns the new cluster that was created
    """
    new_cluster = creator.create(name=name, kubernetes_context=kubernetes_context, namespace=namespace)
    _setup_k8s_cluster(new_cluster)
    _sync_cluster(new_cluster)
    return new_cluster


def configure_cluster_argparser(parser: argparse.ArgumentParser):
    """Add cluster creation arguments to the argparser
    """

    parser.add_argument(
        'kubernetes_context',
        nargs='?',
        metavar='CONTEXT',
        help='The Kubernetes context the cluster should use. If omitted, you will be given a list of options',
    )
    parser.add_argument('--name', help='Optional name to give the cluster. Defaults to CONTEXT.')
    parser.add_argument('--namespace',
                        help=textwrap.dedent("""
        Namespace that should be used within the given Kubernetes context. Defaults to the namespace associated
        with the specified context, if one exists."""))

    parser.add_argument('--all',
                        default=False,
                        action='store_true',
                        dest='all_clusters',
                        help='Create all available clusters.  Defaults to false')


def _setup_k8s_cluster(cluster: Cluster):
    """Run K8s cluster setup
    """
    # pylint: disable-next=import-outside-toplevel
    from mcli.serverside.clusters.cluster import ClusterSetupError, GenericK8sCluster
    k8s_cluster = GenericK8sCluster.from_mcli_cluster(cluster)
    try:
        k8s_cluster.setup()
    except ClusterSetupError as e:
        logger.warning(f'{FAIL} Cluster setup failed with error: {e}')


def _sync_cluster(cluster: Cluster):
    config = MCLIConfig.load_config()
    config.clusters.append(cluster)
    secret_manager = SecretManager(config.clusters[0])

    # Sync all secrets
    with console.status(f'Syncing secrets to cluster {cluster.name}'):
        for cluster_secret in secret_manager.get_secrets():
            with Cluster.use(cluster):
                cluster_secret.create(cluster.namespace)

    config.save_config()
