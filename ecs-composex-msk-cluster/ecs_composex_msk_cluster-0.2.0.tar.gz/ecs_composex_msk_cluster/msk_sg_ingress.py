#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2022 John Mille <john@compose-x.io>

from __future__ import annotations

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .msk_cluster import MskCluster

from ecs_composex.common import get_nested_property
from troposphere import AccountId, FindInMap, GetAtt, If, NoValue, Ref

from .msk_cluster_conditions import (
    CLIENTS_USE_SASL_IAM_CON_T,
    CLIENTS_USE_SASL_SCRAM_CON_T,
    CLIENTS_USE_TLS_AUTH_CON_T,
    CLUSTER_PUBLICLY_ADDRESSED_CON_T,
)
from .msk_cluster_params import (
    MSK_CLUSTER_ADDRESSING_TYPE,
    MSK_CLUSTER_USE_SASL_IAM,
    MSK_CLUSTER_USE_SASL_SCRAM,
    MSK_CLUSTER_USE_TLS_AUTH,
    MSK_PORTS_MAPPING,
)


def str_to_bool(input_var: Union[str, bool]) -> bool:
    if isinstance(input_var, bool):
        return input_var
    elif isinstance(input_var, str):
        if input_var.lower() in ["true", "yes"]:
            return True
        return False
    return False


def allow_clients_sg_ingress(cluster) -> list[If]:
    rules: list = []

    for port_type, port in MSK_PORTS_MAPPING["Zookeeper"].items():
        rules.append(
            {
                "Description": f"Zookeeper {port_type} MSK",
                "FromPort": port,
                "ToPort": port,
                "SourceSecurityGroupId": GetAtt(
                    cluster.clients_security_group, "GroupId"
                ),
                "SourceSecurityGroupOwnerId": AccountId,
                "IpProtocol": 6,
            }
        )
    rules.append(
        If(
            CLIENTS_USE_SASL_IAM_CON_T,
            If(
                CLUSTER_PUBLICLY_ADDRESSED_CON_T,
                [
                    {
                        "Description": f"SASL IAM Public Access",
                        "FromPort": FindInMap("MSKPorts", "Public", "Iam"),
                        "ToPort": FindInMap("MSKPorts", "Public", "Iam"),
                        "SourceSecurityGroupId": GetAtt(
                            cluster.clients_security_group, "GroupId"
                        ),
                        "SourceSecurityGroupOwnerId": AccountId,
                        "IpProtocol": 6,
                    },
                    {
                        "Description": f"SASL IAM Private Access",
                        "FromPort": FindInMap("MSKPorts", "Private", "Iam"),
                        "ToPort": FindInMap("MSKPorts", "Private", "Iam"),
                        "SourceSecurityGroupId": GetAtt(
                            cluster.clients_security_group, "GroupId"
                        ),
                        "SourceSecurityGroupOwnerId": AccountId,
                        "IpProtocol": 6,
                    },
                ],
                {
                    "Description": f"SASL IAM Private Access",
                    "FromPort": FindInMap("MSKPorts", "Private", "Iam"),
                    "ToPort": FindInMap("MSKPorts", "Private", "Iam"),
                    "SourceSecurityGroupId": GetAtt(
                        cluster.clients_security_group, "GroupId"
                    ),
                    "SourceSecurityGroupOwnerId": AccountId,
                    "IpProtocol": 6,
                },
            ),
            NoValue,
        )
    )
    rules.append(
        If(
            CLIENTS_USE_SASL_SCRAM_CON_T,
            If(
                CLUSTER_PUBLICLY_ADDRESSED_CON_T,
                [
                    {
                        "Description": f"SASL SCRAM Public Access",
                        "FromPort": FindInMap("MSKPorts", "Public", "Scram"),
                        "ToPort": FindInMap("MSKPorts", "Public", "Scram"),
                        "SourceSecurityGroupId": GetAtt(
                            cluster.clients_security_group, "GroupId"
                        ),
                        "SourceSecurityGroupOwnerId": AccountId,
                        "IpProtocol": 6,
                    },
                    {
                        "Description": f"SASL SCRAM Private Access",
                        "FromPort": FindInMap("MSKPorts", "Private", "Scram"),
                        "ToPort": FindInMap("MSKPorts", "Private", "Scram"),
                        "SourceSecurityGroupId": GetAtt(
                            cluster.clients_security_group, "GroupId"
                        ),
                        "SourceSecurityGroupOwnerId": AccountId,
                        "IpProtocol": 6,
                    },
                ],
                {
                    "Description": f"SASL SCRAM Private Access",
                    "FromPort": FindInMap("MSKPorts", "Private", "Scram"),
                    "ToPort": FindInMap("MSKPorts", "Private", "Scram"),
                    "SourceSecurityGroupId": GetAtt(
                        cluster.clients_security_group, "GroupId"
                    ),
                    "SourceSecurityGroupOwnerId": AccountId,
                    "IpProtocol": 6,
                },
            ),
            NoValue,
        )
    )
    rules.append(
        If(
            CLIENTS_USE_TLS_AUTH_CON_T,
            If(
                CLUSTER_PUBLICLY_ADDRESSED_CON_T,
                [
                    {
                        "Description": f"TLS Authentication Public Access",
                        "FromPort": FindInMap("MSKPorts", "Public", "Tls"),
                        "ToPort": FindInMap("MSKPorts", "Public", "Tls"),
                        "SourceSecurityGroupId": GetAtt(
                            cluster.clients_security_group, "GroupId"
                        ),
                        "SourceSecurityGroupOwnerId": AccountId,
                        "IpProtocol": 6,
                    },
                    {
                        "Description": f"TLS Authentication Private Access",
                        "FromPort": FindInMap("MSKPorts", "Private", "Tls"),
                        "ToPort": FindInMap("MSKPorts", "Private", "Tls"),
                        "SourceSecurityGroupId": GetAtt(
                            cluster.clients_security_group, "GroupId"
                        ),
                        "SourceSecurityGroupOwnerId": AccountId,
                        "IpProtocol": 6,
                    },
                ],
                {
                    "Description": f"TLS Authentication Private Access",
                    "FromPort": FindInMap("MSKPorts", "Private", "Tls"),
                    "ToPort": FindInMap("MSKPorts", "Private", "Tls"),
                    "SourceSecurityGroupId": GetAtt(
                        cluster.clients_security_group, "GroupId"
                    ),
                    "SourceSecurityGroupOwnerId": AccountId,
                    "IpProtocol": 6,
                },
            ),
            NoValue,
        )
    )
    return rules


def handle_msk_auth_parameters(cluster: MskCluster) -> None:
    properties: list = [
        (
            "ClientAuthentication.Sasl.Scram.Enabled",
            str_to_bool,
            MSK_CLUSTER_USE_SASL_SCRAM,
        ),
        (
            "ClientAuthentication.Sasl.Iam.Enabled",
            str_to_bool,
            MSK_CLUSTER_USE_SASL_IAM,
        ),
        (
            "ClientAuthentication.Tls.Enabled",
            str_to_bool,
            MSK_CLUSTER_USE_TLS_AUTH,
        ),
    ]
    for auth_property in properties:
        resource, prop, value = get_nested_property(
            cluster.cfn_resource,
            auth_property[0],
        )
        if prop and value:
            cluster.stack.Parameters.update(
                {auth_property[2].title: str(auth_property[1](value))}
            )
            setattr(resource, prop, Ref(auth_property[2]))


def handle_msk_auth_settings(cluster: MskCluster):
    setattr(
        cluster.security_group,
        "SecurityGroupIngress",
        allow_clients_sg_ingress(cluster),
    )
    resource, prop, value = get_nested_property(
        cluster.cfn_resource,
        "BrokerNodeGroupInfo.ConnectivityInfo.PublicAccess.Type",
    )
    if value and value == "SERVICE_PROVIDED_EIPS":
        cluster.stack.Parameters.update({MSK_CLUSTER_ADDRESSING_TYPE.title: "PUBLIC"})
    handle_msk_auth_parameters(cluster)
