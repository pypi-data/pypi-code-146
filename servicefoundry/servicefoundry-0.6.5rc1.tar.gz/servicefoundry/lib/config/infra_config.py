import json
import os

import questionary

from servicefoundry.lib.clients.terragrunt_client import Terragrunt
from servicefoundry.lib.config.config_manager import ConfigManager
from servicefoundry.lib.config.dict_questionaire import DictQuestionaire


class InfraConfig:
    def __init__(
        self, terragrunt_client: Terragrunt, infra_config_file_path=None
    ) -> None:
        self.terragrunt_client = terragrunt_client
        if infra_config_file_path and os.path.exists(infra_config_file_path):
            with open(infra_config_file_path, "r") as config:
                infra_config = json.loads(config.read())
        else:
            infra_config = ConfigManager().get_config(ConfigManager.INFRA_CONFIG)
        if infra_config:
            self.provisioning = infra_config["provisioning"]
            self.bootstrapping = infra_config["bootstrapping"]

    def __externalConfigHandler(self):
        return questionary.confirm(
            f"Do you want to attach your own network: ", default=False
        ).ask()

    # Config needed for the provisioning step where terraform is run
    provisioning = {
        "provider": None,
        "awsInputs": {
            "remoteStateBucket": None,
            "region": "eu-west-1",
            "shortRegion": "euwe1",
            "remoteStateAwsProfile": None,
            "awsProfile": None,
            "accountId": None,
            "accountName": None,
            "clusterPrefix": "tfy-",
            "baseDomain": "truefoundry.com",
            "externalNetworkConfig": {
                "networkVpcId": None,
                "networkPublicSubnetsId": [],
                "networkPrivateSubnetsId": [],
            },
        },
    }
    # Config needed for the boostrapping step where helm apply is run
    bootstrapping = {
        "cluster": {
            "provider": None,
            "name": None,
            "region": None,
            "shortRegion": None,
            "baseDomain": None,
            "account": None,
            "endpoint": None,
        },
        "argoIamRole": None,
        "certificatesIamRole": None,
        "externalDnsIamRole": None,
        "awsComponents": {
            "awsEbsCsiDriverIamRole": None,
            "karpenter": {"iamRole": None, "instanceProfile": None},
        },
        "workloadComponents": {
            "tfyAgent": {
                "tenantName": None,
                "clusterToken": None,
                "controlPlaneUrl": None,
            }
        },
        "targetRepo": {
            "url": None,
            "branch": None,
            "path": None,
            "username": None,
            "password": None,
        },
        "monitoring": {
            "loki": {"bucketName": None, "roleArn": None},
            "prometheus": {"bucketName": None, "roleArn": None},
        },
        "controlPlaneComponents": {
            "controlPlaneUrl": None,
            "mlfoundry": {
                "enabled": False,
                "s3BucketName": None,
            },
            "mlmonitoring": {
                "enabled": False,
            },
            "servicefoundry": {
                "enabled": True,
                "s3BucketName": None,
            },
        },
    }

    def populate_bootstrapping_config(self, target_repo_config, base_terragrunt_dir):
        self.bootstrapping["cluster"]["account"] = self.provisioning["awsInputs"][
            "accountName"
        ]
        self.bootstrapping["cluster"]["provider"] = self.provisioning["provider"]
        self.bootstrapping["cluster"][
            "name"
        ] = self.terragrunt_client.fetch_terragrunt_output(
            os.path.join(base_terragrunt_dir, "cluster"), "cluster_id"
        )
        self.bootstrapping["cluster"]["region"] = self.provisioning["awsInputs"][
            "region"
        ]
        self.bootstrapping["cluster"]["shortRegion"] = self.provisioning["awsInputs"][
            "shortRegion"
        ]
        self.bootstrapping["cluster"]["baseDomain"] = self.provisioning["awsInputs"][
            "baseDomain"
        ]
        self.bootstrapping["cluster"][
            "endpoint"
        ] = self.terragrunt_client.fetch_terragrunt_output(
            os.path.join(base_terragrunt_dir, "cluster"), "cluster_endpoint"
        )

        self.bootstrapping[
            "argoIamRole"
        ] = self.terragrunt_client.fetch_terragrunt_output(
            os.path.join(base_terragrunt_dir, "cluster-app-argocd"),
            "argocd_iam_role_arn",
        )
        if not self.provisioning["awsInputs"]["externalNetworkConfig"]:
            self.bootstrapping[
                "certificatesIamRole"
            ] = self.terragrunt_client.fetch_terragrunt_output(
                os.path.join(base_terragrunt_dir, "cluster-iam-certmanager"),
                "iam_role_arn",
            )
            self.bootstrapping[
                "externalDnsIamRole"
            ] = self.terragrunt_client.fetch_terragrunt_output(
                os.path.join(base_terragrunt_dir, "cluster-iam-external-dns"),
                "iam_role_arn",
            )
        else:
            self.bootstrapping["certificatesIamRole"] = ""
            self.bootstrapping["externalDnsIamRole"] = ""
        self.bootstrapping["awsComponents"][
            "awsEbsCsiDriverIamRole"
        ] = self.terragrunt_client.fetch_terragrunt_output(
            os.path.join(base_terragrunt_dir, "cluster-iam-csi-ebs"), "iam_role_arn"
        )
        self.bootstrapping["awsComponents"]["karpenter"][
            "iamRole"
        ] = self.terragrunt_client.fetch_terragrunt_output(
            os.path.join(base_terragrunt_dir, "cluster-iam-karpenter"), "iam_role_arn"
        )
        self.bootstrapping["awsComponents"]["karpenter"][
            "instanceProfile"
        ] = self.terragrunt_client.fetch_terragrunt_output(
            os.path.join(base_terragrunt_dir, "cluster-iam-karpenter"),
            "iam_instance_profile_id",
        )
        install_workload = questionary.confirm(
            "Do you want to install workload components as well?", default=False
        ).ask()
        if install_workload:
            self.bootstrapping["workloadComponents"]["tfyAgent"][
                "tenantName"
            ] = questionary.text("Tenant name").ask()
            self.bootstrapping["workloadComponents"]["tfyAgent"][
                "clusterToken"
            ] = questionary.text("Cluster token").ask()
            self.bootstrapping["workloadComponents"]["tfyAgent"][
                "controlPlaneUrl"
            ] = questionary.text("Control plane url").ask()
        else:
            self.bootstrapping["workloadComponents"] = None

        install_control_plane = questionary.confirm(
            "Do you want to install control plane components as well?", default=False
        ).ask()
        if install_control_plane:
            self.bootstrapping["controlPlaneComponents"][
                "controlPlaneUrl"
            ] = questionary.text("Control plane url").ask()
            self.bootstrapping["controlPlaneComponents"]["mlfoundry"][
                "enabled"
            ] = questionary.confirm(
                "Do you want to install mlfoundry", default=False
            ).ask()
            if self.bootstrapping["controlPlaneComponents"]["mlfoundry"]["enabled"]:
                self.bootstrapping["controlPlaneComponents"]["mlfoundry"][
                    "s3BucketName"
                ] = self.terragrunt_client.fetch_terragrunt_output(
                    os.path.join(base_terragrunt_dir, "truefoundry-aws"),
                    "mlfoundry_bucket_id",
                )
            self.bootstrapping["controlPlaneComponents"]["mlmonitoring"][
                "enabled"
            ] = questionary.confirm(
                "Do you want to install mlmonitoring", default=False
            ).ask()
            self.bootstrapping["controlPlaneComponents"]["servicefoundry"][
                "enabled"
            ] = questionary.confirm(
                "Do you want to install servicefoundry", default=False
            ).ask()
            if self.bootstrapping["controlPlaneComponents"]["servicefoundry"][
                "enabled"
            ]:
                self.bootstrapping["controlPlaneComponents"]["servicefoundry"][
                    "s3BucketName"
                ] = self.terragrunt_client.fetch_terragrunt_output(
                    os.path.join(base_terragrunt_dir, "truefoundry-aws"),
                    "svcfoundry_bucket_id",
                )
            else:
                self.bootstrapping["controlPlaneComponents"]["servicefoundry"] = None
        else:
            self.bootstrapping["controlPlaneComponents"] = None

        self.bootstrapping["targetRepo"] = target_repo_config

        install_monitoring = questionary.confirm(
            "Do you want to install monitoring as well?", default=False
        ).ask()
        if install_monitoring:
            self.bootstrapping["monitoring"]["loki"][
                "bucketName"
            ] = self.terragrunt_client.fetch_terragrunt_output(
                os.path.join(base_terragrunt_dir, "cluster-app-loki"),
                "loki_bucket_name",
            )
            self.bootstrapping["monitoring"]["loki"][
                "roleArn"
            ] = self.terragrunt_client.fetch_terragrunt_output(
                os.path.join(base_terragrunt_dir, "cluster-app-loki"), "iam_role_arn"
            )
            self.bootstrapping["monitoring"]["prometheus"][
                "bucketName"
            ] = self.terragrunt_client.fetch_terragrunt_output(
                os.path.join(base_terragrunt_dir, "cluster-app-thanos"),
                "thanos_bucket_name",
            )
            self.bootstrapping["monitoring"]["prometheus"][
                "roleArn"
            ] = self.terragrunt_client.fetch_terragrunt_output(
                os.path.join(base_terragrunt_dir, "cluster-app-thanos"), "iam_role_arn"
            )
        else:
            self.bootstrapping["monitoring"] = None
        ConfigManager().save_config(ConfigManager.INFRA_CONFIG, self.toJSON())

    def populate_provisioning_config(self, provider: str):
        self.provisioning["provider"] = "aws"
        DictQuestionaire(self.provisioning["awsInputs"]).ask(
            custom_handlers={"externalNetworkConfig": self.__externalConfigHandler}
        )
        ConfigManager().save_config(ConfigManager.INFRA_CONFIG, self.toJSON())

    def toJSON(self):
        return {"provisioning": self.provisioning, "bootstrapping": self.bootstrapping}
