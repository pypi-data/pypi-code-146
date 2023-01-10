"""Helpers for Weights and Biases integration"""
import logging
from dataclasses import dataclass
from typing import Optional

from kubernetes import client

from mcli.models import MCLIIntegration
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob

logger = logging.getLogger(__name__)


class CometMLLabels():
    PROJECT_KEY = 'COMET_PROJECT_NAME'
    WORKSPACE_KEY = 'COMET_WORKSPACE'
    API_KEY = 'COMET_API_KEY'


label = CometMLLabels()


@dataclass
class MCLICometMLIntegration(MCLIIntegration):
    """CometML Integration
    """
    project_name: Optional[str] = None
    workspace: Optional[str] = None

    def add_to_job(self, kubernetes_job: MCLIK8sJob) -> bool:
        if self.project_name:
            logger.debug(f'Setting Comet project name env var: {label.PROJECT_KEY}={self.project_name}')
            kubernetes_job.add_env_var(env_var=client.V1EnvVar(
                name=label.PROJECT_KEY,
                value=self.project_name,
            ))

        if self.workspace:
            logger.debug(f'Setting Comet workspace env var: {label.WORKSPACE_KEY}={self.workspace}')
            kubernetes_job.add_env_var(env_var=client.V1EnvVar(
                name=label.WORKSPACE_KEY,
                value=self.workspace,
            ))

        return True
