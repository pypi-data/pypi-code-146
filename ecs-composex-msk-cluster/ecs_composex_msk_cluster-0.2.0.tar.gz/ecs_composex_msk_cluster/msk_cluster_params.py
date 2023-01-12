#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2022 John Mille <john@compose-x.io>

from ecs_composex.common.cfn_params import Parameter
from ecs_composex.vpc.vpc_params import SG_ID_TYPE

GROUP_LABELS: str = "MSK Settings"

MSK_CLUSTER_SG_PARAM_T = "MSKClusterSecurityGroup"
MSK_CLUSTER_SG_PARAM = Parameter(
    MSK_CLUSTER_SG_PARAM_T,
    group_label=GROUP_LABELS,
    return_value="GroupId",
    Type=SG_ID_TYPE,
)

MSK_CLUSTER_ARN_T = "ClusterArn"
MSK_CLUSTER_ARN = Parameter(MSK_CLUSTER_ARN_T, group_label=GROUP_LABELS, Type="String")
MSK_CLUSTER_CLIENTS_SHARED_SG_T = "MSKClientsSecurityGroup"
MSK_CLUSTER_CLIENTS_SHARED_SG = Parameter(
    MSK_CLUSTER_CLIENTS_SHARED_SG_T,
    return_value="GroupId",
    group_label=GROUP_LABELS,
    Type=SG_ID_TYPE,
    Description="MSK Clients Security Group",
)

MSK_CLUSTER_ADDRESSING_TYPE_T = "MskClusterNetworkAccessType"
MSK_CLUSTER_ADDRESSING_TYPE = Parameter(
    MSK_CLUSTER_ADDRESSING_TYPE_T,
    group_label=GROUP_LABELS,
    Type="String",
    AllowedValues=["PUBLIC", "PRIVATE"],
    Default="PRIVATE",
    Description="MSK Cluster public access is enabled",
)

MSK_CLUSTER_USE_SASL_IAM_T = "UseSaslIam"
MSK_CLUSTER_USE_SASL_IAM = Parameter(
    MSK_CLUSTER_USE_SASL_IAM_T,
    group_label=GROUP_LABELS,
    Type="String",
    AllowedValues=["True", "False"],
    Default="True",
    Description="Use IAM for SASL Authentication",
)
MSK_CLUSTER_USE_SASL_SCRAM_T = "UseSaslScram"
MSK_CLUSTER_USE_SASL_SCRAM = Parameter(
    MSK_CLUSTER_USE_SASL_SCRAM_T,
    group_label=GROUP_LABELS,
    Type="String",
    AllowedValues=["True", "False"],
    Default="True",
    Description="Use SCRAM for SASL Authentication",
)

MSK_CLUSTER_USE_TLS_AUTH_T = "UseSaslScram"
MSK_CLUSTER_USE_TLS_AUTH = Parameter(
    MSK_CLUSTER_USE_TLS_AUTH_T,
    group_label=GROUP_LABELS,
    Type="String",
    AllowedValues=["True", "False"],
    Default="False",
    Description="Use TLS for Authentication",
)

MSK_PORTS_MAPPING: dict = {
    "Private": {
        "Plaintext": 9092,
        "Tls": 9094,
        "Scram": 9096,
        "Iam": 9098,
    },
    "Public": {
        "Plaintext": 9192,
        "Tls": 9194,
        "Scram": 9096,
        "Iam": 9198,
    },
    "Zookeeper": {"Plaintext": 2181, "Tls": 2182},
}

CONTROL_CLOUD_ATTR_MAPPING = {
    MSK_CLUSTER_ARN: "Arn",
    MSK_CLUSTER_SG_PARAM: "BrokerNodeGroupInfo::SecurityGroups::0",
}
