""" The MCLI Kubernetes Job Abstraction """
from typing import TYPE_CHECKING, Dict, List, NamedTuple, Optional

from kubernetes import client
from kubernetes.client.api_client import ApiClient
from ruamel import yaml

from mcli.serverside.job.mcli_k8s_config_map_typing import MCLIK8sConfigMap
from mcli.serverside.job.mcli_k8s_job_typing import MCLIK8sJobTyping

if TYPE_CHECKING:
    from mcli.models.mcli_secret import Secret


class MCLIVolume(NamedTuple):
    volume: client.V1Volume
    volume_mount: client.V1VolumeMount


class MCLIConfigMap(NamedTuple):
    config_map: MCLIK8sConfigMap
    config_volume: MCLIVolume


class MCLIK8sJob(MCLIK8sJobTyping):
    """ MCLI Job K8s Abstraction

    The collection of functions we use internally to modify and make
    changes to a K8s Job


    """

    def add_volume(self, volume: MCLIVolume):
        """Add an Volume to a k8s Job

        Args:
            volume: the MCLIVolume to add (includes volume and mount)
        """
        self.pod_volumes.append(volume.volume)
        self.container_volume_mounts.append(volume.volume_mount)

    def add_env_var(
        self,
        env_var: client.V1EnvVar,
    ):
        """Add an Environment Variable to a k8s Job

        Args:
            env_var: the Environment Variable to add
        """
        self.environment_variables.append(env_var)

    def add_port(
        self,
        port: client.V1ContainerPort,
    ):
        """Open an additional port in the primary container

        Args:
            port (client.V1ContainerPort): Port to open, specified as a V1ContainerPort
        """
        self.ports.append(port)

    def add_secret(self, secret: 'Secret'):
        secret.add_to_job(self)

    def add_capabilities(self, capabilities: List[str]):
        """Add the requested capabilities to the main container
        """
        # Create security context
        if self.container.security_context is None:
            self.container.security_context = client.V1SecurityContext()
        sc = self.container.security_context

        # Add requested capabilities
        if sc.capabilities is None:
            sc.capabilities = client.V1Capabilities()
        caps = (sc.capabilities.add or []) + capabilities
        sc.capabilities.add = caps

        # Set for the primary container
        self.container.security_context = sc

    def add_affinity(
        self,
        key: str,
        exists: bool = False,
        in_values: Optional[List[str]] = None,
        not_in_values: Optional[List[str]] = None,
    ):
        if exists:
            selector = client.V1NodeSelectorRequirement(
                key=key,
                operator='Exists',
            )
        elif in_values:
            selector = client.V1NodeSelectorRequirement(
                key=key,
                operator='In',
                values=in_values,
            )
        elif not_in_values:
            selector = client.V1NodeSelectorRequirement(
                key=key,
                operator='NotIn',
                values=not_in_values,
            )
        else:
            raise RuntimeError("No valid node affinities requested")

        term = client.V1NodeSelectorTerm(match_expressions=[selector])

        affinity = self.pod_spec.affinity or client.V1Affinity()
        self.pod_spec.affinity = affinity

        node_affinity = affinity.node_affinity or client.V1NodeAffinity()
        affinity.node_affinity = node_affinity

        req = node_affinity.required_during_scheduling_ignored_during_execution
        new_term = client.V1NodeSelectorTerm(match_expressions=[selector])
        if not req:
            req = client.V1NodeSelector(node_selector_terms=[new_term])
        else:
            terms = req.node_selector_terms or []
            # If term already exists, append to expression
            if terms:
                term = terms[0]
                term.match_expressions = term.match_expressions or []
                term.match_expressions.append(selector)
            else:
                term = new_term
                terms.append(term)
            req.node_selector_terms = terms
        node_affinity.required_during_scheduling_ignored_during_execution = req

    def add_affinities(self, selectors: Dict[str, List[str]]):
        """Add the given dictionary of node selectors to the job as node affinities
        """
        for key, values in selectors.items():
            self.add_affinity(key, in_values=values)

    def set_privileged(self, privileged: bool = True):
        """Set the primary container's privileged mode
        """
        if self.container.security_context is None:
            self.container.security_context = client.V1SecurityContext()
        self.container.security_context.privileged = privileged

    def add_command(
        self,
        command: str,
        error_message: str,
        required: bool = True,
    ):
        existing_command = self.container.command_string
        # Temporarily remove set -e
        existing_command = existing_command.replace('set -e;', '')
        if required:
            error_case = f'( echo { error_message } && exit 1 )'
        else:
            error_case = f'( echo { error_message }) '
        new_command = f'set -e; {command} || {error_case};'
        self.container.command_string = new_command + existing_command

    def __str__(self) -> str:

        api = ApiClient()
        data = api.sanitize_for_serialization(self)
        return yaml.dump(data)
