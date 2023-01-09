import json
import os
from shutil import which

import questionary

from servicefoundry.lib.binarydownloader import BinaryDependencies, BinaryName
from servicefoundry.lib.clients.shell_client import Shell
from servicefoundry.logger import logger

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def check_or_install_dependencies(dependencies):
    """
    Takes a list of dependencies and validates if they're present in the system
    If not present it tries to install the the binaries into troufoundry bin folder
    """
    for dep in dependencies:
        try:
            if which(dep):
                logger.info(f"{dep} found on local system")
            else:
                BinaryDependencies().which(BinaryName(dep))
                logger.info(f"{dep} installed automatically in .truefoundry/bin")
        except:
            raise Exception(
                f"Automated installation of {dep} not yet supported. Refer to docs for manual installation"
            )


def execute_kubectl_apply_file(file_path):
    return Shell().execute_shell_command(
        [
            BinaryDependencies().which(BinaryName.KUBECTL),
            "apply",
            "-f",
            file_path,
        ]
    )


def set_current_kubecontext():
    """
    This method lists down the current kubecontext available to the user and asks the user
    to select one kubecontext. If no kubecontexts are found, it throws an exception.
    If there is only one kubecontext found, it will select that kubecontext and print
    the message to the user. Once the user selects the kubecontext, it will set the selected
    context as the current context
    """
    kube_contexts = Shell().execute_shell_command(
        [
            BinaryDependencies().which(BinaryName.KUBECTL),
            "config",
            "get-contexts",
            "--no-headers",
            "--output",
            "name",
        ]
    )
    contexts_list = kube_contexts.splitlines()
    selected_context = questionary.select(
        f"Please select the cluster where you want to install Truefoundry: ",
        choices=contexts_list,
    ).ask()
    # Set the selected kubecontext as the current kubecontext
    Shell().execute_shell_command(
        [
            BinaryDependencies().which(BinaryName.KUBECTL),
            "config",
            "set-context",
            selected_context,
        ]
    )
    logger.info(f"Set current context as {selected_context}")
    return selected_context


# This functions checks if the input crd_name is already installed in the cluster


def check_if_crd_installed(name, crd_name) -> bool:
    try:
        check_crd = Shell().execute_shell_command(
            [
                BinaryDependencies().which(BinaryName.KUBECTL),
                "get",
                "crd",
                crd_name,
                "-ojson",
            ]
        )
        return True
    except:
        logger.info(f"{name} not installed on cluster. Moving ahead...")
        return False


def check_if_truefoundry_exists():
    # check if truefoundry namespace is present
    try:
        Shell().execute_shell_command(
            [
                BinaryDependencies().which(BinaryName.KUBECTL),
                "get",
                "secrets",
                "servicefoundry-server-env-secret",
                "-n",
                "truefoundry",
            ]
        )
        return True
    except:
        logger.info("Truefoundry not installed on the cluster")
        return False


def create_namespace_if_not_exists(namespace_name: str):
    try:
        namespace = Shell().execute_shell_command(
            [
                BinaryDependencies().which(BinaryName.KUBECTL),
                "create",
                "namespace",
                namespace_name,
            ]
        )
    except Exception as e:
        logger.info(e)
        return


def execute_nats_bootstrap_script():
    if os.path.exists("./nsc"):
        raise Exception(
            "nsc directory already exists. Please delete that before proceeding"
        )
    Shell().execute_shell_command(["sh", os.path.join(THIS_DIR, "nats-bootstrap.sh")])
    nats_controlplane_account_seed = ""
    with open("./nsc/tfy.seed", "r") as f:
        nats_controlplane_account_seed = f.readline()
    return nats_controlplane_account_seed


def delete_directory(dir):
    try:
        Shell().execute_shell_command(["rm", "-rf", dir])
    except Exception as e:
        logger.info(e)
        return


def install_argocd_chart(argocd_chart_version):
    logger.info("Installing ArgoCD")
    try:
        print(
            Shell().execute_shell_command(
                [
                    which("helm"),
                    "upgrade",
                    "--install",
                    "--namespace",
                    "argocd",
                    "--create-namespace",
                    "--repo",
                    "https://argoproj.github.io/argo-helm",
                    "argocd",
                    "argo-cd",
                    "--set",
                    "'server.extraArgs'='{--insecure}'",
                    "--version",
                    argocd_chart_version,
                ]
            )
        )
        logger.info("ArgoCD Installation Done")
    except Exception as e:
        raise Exception("Error installing ArgoCD helm chart. Please try again")
