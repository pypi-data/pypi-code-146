""" MCLI Integration APT Packages """
import textwrap
from dataclasses import dataclass

from kubernetes import client

from mcli import config
from mcli.models import MCLIIntegration
from mcli.models.mcli_integration import IntegrationType
from mcli.objects.integrations.git_repo import MCLIGitRepoIntegration
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob

AGENT_DEBUG = 'AGENT_DEBUG'
AGENT_OPTIMIZATION_LEVEL = 'AGENT_OPTIMIZATION_LEVEL'


@dataclass
class MCLIMosaicMLAgentIntegration(MCLIIntegration):
    """MosaicML Agent Integration

    Will not do anything unless in INTERNAL mode and running with optimization_level > 0

    This is not added by users, rather it is appended to every run in mcli_job
    """
    optimization_level: int

    def add_to_job(self, kubernetes_job: MCLIK8sJob) -> bool:
        conf = config.MCLIConfig.load_config(safe=True)

        if not conf.internal:
            return True

        if not self.optimization_level:
            return True

        # Add mosaicml agent to python path
        kubernetes_job.add_env_var(client.V1EnvVar(
            name=AGENT_OPTIMIZATION_LEVEL,
            value=str(self.optimization_level),
        ))
        python_command = textwrap.dedent("""\
            import random
            with open('/'.join(random.__file__.split('/')[:-1])+'/usercustomize.py', 'w') as f:
                print('from importlib import util as _agent_util', file=f)
                print('if _agent_util.find_spec(\\"composer\\") is not None and _agent_util.find_spec(\\"magent\\") is not None:', file=f)
                print('    import magent', file=f)""")
        kubernetes_job.add_command(
            f'python -c "{python_command}"',
            'Agent installation failed',
        )

        # Add mosaicml-agent git repo
        agent_repo = MCLIGitRepoIntegration(
            integration_type=IntegrationType.git_repo,
            git_repo='mosaicml/mosaicml-agent',
            git_branch='main',
            path='/tmp/mosaicml-agent',
            pip_install='.',
        )
        agent_repo.add_to_job(kubernetes_job)
        return True
