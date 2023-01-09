import json
import os
import shutil
import tempfile
from shutil import which

import chevron
import questionary
import yaml
from pydantic import BaseModel

from servicefoundry.lib.clients.cookiecutter_client import CookieCutter
from servicefoundry.lib.clients.git_client import GitClient, GitRepo
from servicefoundry.lib.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.lib.clients.shell_client import Shell
from servicefoundry.lib.clients.terragrunt_client import Terragrunt
from servicefoundry.lib.config.config_manager import ConfigManager
from servicefoundry.lib.config.dict_questionaire import DictQuestionaire
from servicefoundry.lib.config.installation_config import InstallationConfig
from servicefoundry.lib.infra.utils import (
    check_if_crd_installed,
    check_or_install_dependencies,
    create_namespace_if_not_exists,
    delete_directory,
    execute_kubectl_apply_file,
    execute_nats_bootstrap_script,
    install_argocd_chart,
    set_current_kubecontext,
)
from servicefoundry.logger import logger


class HelmRepo(BaseModel):
    # Helm repo name
    name: str
    # The helm repository URL
    url: str
    # Token to access the helm repo
    token: str


class InfraController:
    __infra_config = {}
    __tfy_helm_repo = {}
    terragrunt_client = None
    helm_client = None

    def __init__(self, dry_run, config_file_path):
        if config_file_path:
            with open(config_file_path, "r") as config:
                self.__infra_config = yaml.safe_load(config)
        else:
            raise Exception("Input config file needs to be provided")
        self.git_client = GitClient()
        self.dry_run = dry_run

    # Ask questions to user to compose the input infra config
    def ask_infra_config_from_user(self):
        print("Let's get the infra setup for Truefoundry")
        return {}

    def __apply_terragrunt(self, base_terragrunt_dir):
        if not questionary.confirm(
            "Do you want to continue with infra creation: ", default=True
        ).ask():
            return
        # TODO A terragrunt repo which can cache the outputs for each module. This would reduce the number of output calls
        self.terragrunt_client = Terragrunt()
        self.terragrunt_client.apply_all(base_terragrunt_dir)

    def __install_argocd(self, target_repo: GitRepo, target_repo_path: str):
        logger.info("====== Installing ArgoCD manifests========")
        if not questionary.confirm(
            f"""Have you already merged the commit to the main branch in {target_repo.repo_url}.
            Please make sure that is done before proceeding here. """,
            default=True,
        ).ask():
            return

        logger.info(
            f"""We will bootstrap ArgoCD to sync all the configuration present
            at {target_repo.repo_url}/{target_repo_path} to the
            Kubernetes cluster"""
        )

        input_argo_file = "./servicefoundry/lib/infra/argo-bootstrap.mustache"
        output_argo_file = "argo-bootstrap.yaml"
        with open(input_argo_file, "r") as input_f, open(
            output_argo_file, "w"
        ) as output_f:
            output_f.write(
                chevron.render(
                    input_f,
                    {
                        "tfy_helm_repo_url": self.__tfy_helm_repo.url,
                        "tfy_helm_repo_token": self.__tfy_helm_repo.token,
                        "target_repo_url": target_repo.repo_url,
                        "target_repo_username": target_repo.username,
                        "target_repo_password": target_repo.password,
                        "target_repo_path": target_repo_path,
                    },
                )
            )
        # Apply the argo configuration to Kubernetes
        logger.info("Applying the argocd app to Kubernetes")
        execute_kubectl_apply_file(output_argo_file)
        logger.info("Kubernetes Spec for ArgoCD application applied. Please check ")

    # This function clones the target repo and return the clone_dir path
    def __clone_target_repo(self, target_repo: GitRepo):
        target_repo_clone_dir = os.path.join(tempfile.mkdtemp(), "target-repo")
        logger.info(
            f"""We will clone the {target_repo.repo_url} at {target_repo_clone_dir}.
            Please make sure you have permissions to clone and push to the repository
            from your local machine."""
        )
        if not questionary.confirm(
            "Proceed with cloning the repo: ", default=True
        ).ask():
            return
        # We will need to remove any credentials associated with the repo
        # since we assume that local machine has the credentials to push to that repo.
        target_repo_without_creds = GitRepo(
            repo_url=target_repo.repo_url,
            git_ref=target_repo.git_ref,
            username="",
            password="",
        )
        GitClient().clone_repo(target_repo_without_creds, target_repo_clone_dir)
        logger.info(f"Cloned target repo at {target_repo_clone_dir}")
        return target_repo_clone_dir

    def create_infra_using_terraform(self):
        logger.info(
            """
            We will install the Truefoundry infrastructure on the provided cloud account.
            Truefoundry can be installed on AWS, GCP or Azure cloud infra.
            The steps below will guide you through the installation process. If you are
            confused about any of the steps, please refer to docs at
            https://docs.truefoundry.com/docs/deploy-on-own-cloud-overview or contact us on
            Slack at https://truefoundry.slack.com/signup#/domain-signup
            """
        )

        # We have the input infra config. We use the input infra_config to get terraform inputs from server.
        response = ServiceFoundryServiceClient().process_infra(self.__infra_config)

        # Inputs for Terraform code
        terraform_inputs = response["terraform_inputs"]
        # Truefoundry template repo credentials
        template_git_repo = GitRepo.parse_obj(response["template_git_repo"])
        # Target Repo where to commit the terraform code
        target_repo = GitRepo(
            repo_url=response["target_repo"]["url"],
            git_ref=response["target_repo"]["branch"],
            username=response["target_repo"]["username"],
            password=response["target_repo"]["password"],
        )
        target_repo_path = response["target_repo"]["terraform_path"]

        # Clone the template code repo
        logger.info(
            "Cloning truefoundry template repo. git needs to be installed on the local system"
        )
        check_or_install_dependencies(["git"])
        clone_dir = os.path.join(tempfile.mkdtemp(), "tfy-repo")

        self.git_client.clone_repo(template_git_repo, clone_dir)
        logger.info(f"Template repo cloned at: {clone_dir}")

        # Create cookiecutter.json file and render cookiecutter template
        cookiecutter_dir = os.path.join("infrastructure", terraform_inputs["provider"])

        cookiecutter_client = CookieCutter(clone_dir, directory=cookiecutter_dir)
        with open(
            os.path.join(clone_dir, cookiecutter_dir, "cookiecutter.json"), "w"
        ) as file:
            file.write(json.dumps(terraform_inputs, indent=2))
        rendered_code_path = cookiecutter_client.run(destination_dir=clone_dir)
        print("The terraform code can be found at: " + rendered_code_path)

        # apply terragrunt
        tf_env_path = os.path.join(
            rendered_code_path,
            terraform_inputs["subscription"]["name"],
            terraform_inputs["location"]["name"],
            terraform_inputs["env"]["cluster_prefix"],
        )
        self.__apply_terragrunt(tf_env_path)
        logger.info(f"Terragrunt infra provisioning done")

        # We are skipping the step of generating the kubeconfig. We will ask the user
        # to do it manually for now - and assume that the kubeconfig is present at the
        # user's machine. Later we can do the kubeconfig generation maybe in the terraform
        # layer

        print(f"""Infrastructure has been provisioned successfully""")
        # TODO: Test the below part
        # Clone target repo
        target_repo_clone_dir = os.path.join(tempfile.mkdtemp(), "target-repo")
        self.git_client.clone_repo(target_repo, target_repo_clone_dir)
        logger.info(f"Cloned target repo at {target_repo_clone_dir}")

        # TODO: Log all relevant terragrunt outputs

        # Copy the terraform code folder into the path of target repo
        shutil.copytree(
            rendered_code_path,
            os.path.join(target_repo_clone_dir, target_repo_path),
        )
        # Push the content to Github
        GitClient().commit_all_changes(target_repo_clone_dir, target_repo.git_ref)

    def setup_kubernetes_cluster(self):
        # We have the input infra config. We use the input infra_config to get terraform inputs from server.
        response = ServiceFoundryServiceClient().process_infra(self.__infra_config)

        # Truefoundry template repo credentials
        template_git_repo = GitRepo.parse_obj(response["template_git_repo"])
        ubermold_inputs = response["ubermold_inputs"]
        ubermold_inputs["project_slug"] = "tfy-k8s-config"
        target_repo = GitRepo(
            repo_url=response["target_repo"]["url"],
            git_ref=response["target_repo"]["branch"],
            username=response["target_repo"]["username"],
            password=response["target_repo"]["password"],
        )
        self.__tfy_helm_repo = HelmRepo.parse_obj(response["tfy_helm_repo"])
        target_repo_path = response["target_repo"]["k8s_path"]

        logger.info(
            """We will need kubectl and helm to be installed on local system to be able
                    to install truefoundry on the Kubernetes cluster"""
        )

        check_or_install_dependencies(["kubectl", "helm"])

        logger.info(
            "Set the current kubecontext to the cluster where you want to install Truefoundry"
        )
        set_current_kubecontext()

        # If istio is already present, ask user if they want to move ahead with their own istio configuration
        if check_if_crd_installed("istio", "virtualservices.networking.istio.io"):
            logger.info(
                """"Istio is already installed on this cluster.
                        If istio was installed via Truefoundry previously, then you can go ahead - else
                        Truefoundry's istio installation ca wipe out your existing Istio configuration."""
            )
            if not questionary.confirm(
                "Are you ready to go ahead with existing istio installation: ",
                default=True,
            ).ask():
                return

        # Install ArgoCD in the cluster if its not already installed
        if not check_if_crd_installed("argocd", "applications.argoproj.io"):
            install_argocd_chart("5.16.13")

        # Clone tfy-template_repo template and overwrite supermold values
        clone_dir = os.path.join(tempfile.mkdtemp(), "tfy-repo")
        logger.info(f"Cloning template repo at {clone_dir}")
        self.git_client.clone_repo(template_git_repo, clone_dir)

        cookiecutter_dir = "k8s"

        # Ask the user if they want to change the cookiecutter configuration
        cookiecutter_config_path = os.path.join(clone_dir, "k8s", "cookiecutter.json")
        logger.info(
            f"""The configuration of Kubernetes is at {cookiecutter_config_path}. Feel free to modify it
                    to decide what you want installed in your Kubernetes cluster. You can modify and save it in
                    place."""
        )

        if not questionary.confirm(
            "Are you ready to go ahead with the installation config: ", default=True
        ).ask():
            return

        # Render the cookiecutter configuration
        cookiecutter_client = CookieCutter(clone_dir, directory="k8s")
        rendered_code_path = cookiecutter_client.run(
            destination_dir=os.path.join(clone_dir, "k8s")
        )
        print("The kubernetes code can be found at: " + rendered_code_path)

        # Clone target repo
        target_repo_clone_dir = self.__clone_target_repo(target_repo)

        # Copy the k8s configuration folder into the path of target repo
        shutil.copytree(
            os.path.join(clone_dir, "k8s", ubermold_inputs["project_slug"]),
            os.path.join(target_repo_clone_dir, target_repo_path),
            dirs_exist_ok=True,
        )
        # Push the content to Github
        GitClient().commit_all_changes(target_repo_clone_dir, target_repo.git_ref)

        logger.info(
            f"""We have committed the changes to {target_repo.repo_url} in the branch: {target_repo.git_ref}.
            Please merge that branch to main branch"""
        )

        # Add this repo as a repository in ArgoCD
        self.__install_argocd(target_repo, target_repo_path)

        return

    def setup_tfy_control_plane(self):
        print("""We will create the secrets for the tfy-control-plane""")

        response = ServiceFoundryServiceClient().process_infra(self.__infra_config)

        image_pull_secret = response["image_pull_secret"]

        check_or_install_dependencies(["kubectl", "helm", "nsc"])
        logger.info(
            "Set the current kubecontext to the cluster where you want to install Truefoundry"
        )
        set_current_kubecontext()

        # Create namespace truefoundry if it doesn't exist
        create_namespace_if_not_exists("truefoundry")

        # Execute nats bootstrap script and get the seed
        nats_controlplane_account_seed = execute_nats_bootstrap_script()

        input_tfy_file = "./servicefoundry/lib/infra/tfy-control-plane.mustache"
        output_tfy_file = "tfy-control-plane.yaml"
        with open(input_tfy_file, "r") as input_f, open(
            output_tfy_file, "w"
        ) as output_f:
            output_f.write(
                chevron.render(
                    input_f,
                    {
                        "truefoundry_db_host": self.__infra_config["tfy_control_plane"][
                            "params"
                        ]["truefoundry_db_host"],
                        "truefoundry_db_username": self.__infra_config[
                            "tfy_control_plane"
                        ]["params"]["truefoundry_db_username"],
                        "truefoundry_db_password": self.__infra_config[
                            "tfy_control_plane"
                        ]["params"]["truefoundry_db_password"],
                        "truefoundry_db_name": self.__infra_config["tfy_control_plane"][
                            "params"
                        ]["truefoundry_db_name"],
                        "nats_controlplane_account_seed": nats_controlplane_account_seed,
                        "truefoundry_svc_account_api_key": self.__infra_config[
                            "tfy_control_plane"
                        ]["params"]["truefoundry_svc_account_api_key"],
                        "image_pull_secret": image_pull_secret,
                    },
                )
            )

        execute_kubectl_apply_file(output_tfy_file)
        delete_directory("./nsc")
        logger.info(
            f"Created secrets in the truefoundry namespace with values at {output_tfy_file}"
        )
        logger.info(
            "Truefoundry control plane bootstrap complete! Pods in truefoundry namespace should start up in a few seconds!"
        )
        return

    def setup_tfy_agent(self):
        logger.info("Installing tfy control plane")
