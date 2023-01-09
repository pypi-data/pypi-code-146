import json
import os
from shutil import which

import questionary

from servicefoundry.lib.clients.shell_client import Shell
from servicefoundry.logger import logger


def check_or_install_dependencies(dependencies):
    """
    Takes a list of dependencies and validates if they're present in the system
    """
    for dep in dependencies:
        if not which(dep):
            raise Exception(f"{dep} not found")
        else:
            logger.info(f"{dep} found on local system")


def execute_kubectl_apply_file(file_path):
    return Shell().execute_shell_command(
        [
            which("kubectl"),
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
        [which("kubectl"), "config", "get-contexts", "--no-headers", "--output", "name"]
    )
    contexts_list = kube_contexts.splitlines()
    selected_context = questionary.select(
        f"Please select the cluster where you want to install Truefoundry: ",
        choices=contexts_list,
    ).ask()
    # Set the selected kubecontext as the current kubecontext
    Shell().execute_shell_command(
        [which("kubectl"), "config", "set-context", selected_context]
    )
    logger.info(f"Set current context as {selected_context}")
    return selected_context


# This functions checks if the input crd_name is already installed in the cluster


def check_if_crd_installed(name, crd_name) -> bool:
    try:
        check_crd = Shell().execute_shell_command(
            [
                which("kubectl"),
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
        namespace = Shell().execute_shell_command(
            [which("kubectl"), "get", "namespace", "truefoundry", "-ojson"]
        )
        raise Exception(
            """truefoundry namespace already present on cluster. Maybe truefoundry is already installed on this cluster?
            If not, please delete the namespace and try again"""
        )
    except:
        logger.info("Truefoundry not installed on the cluster")
        return


def create_namespace_if_not_exists(namespace_name: str):
    try:
        namespace = Shell().execute_shell_command(
            [which("kubectl"), "create", "namespace", namespace_name]
        )
    except Exception as e:
        logger.info(e)
        return


def execute_nats_bootstrap_script():
    if os.path.exists("./nsc"):
        raise Exception(
            "nsc directory already exists. Please delete that before proceeding"
        )
    Shell().execute_shell_command(
        ["sh", "./servicefoundry/lib/infra/nats-bootstrap.sh"]
    )
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
        logger.error(e)
        return


def apply_k8s_secret(self, name, namespace, items, labels=None):
    secret_obj = {
        "apiVersion": "v1",
        "kind": "Secret",
        "type": "Opaque",
        "metadata": {"name": name, "namespace": namespace},
        "stringData": items,
    }
    if labels != None:
        secret_obj["metadata"]["labels"] = labels
    print(execute_kubectl_apply(self.kubeconfig_location, secret_obj))
