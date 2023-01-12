#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2022 John Mille <john@compose-x.io>

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from troposphere import Template

from troposphere import Condition, Equals, If, Not, Or, Ref

from .msk_cluster_params import (
    MSK_CLUSTER_ADDRESSING_TYPE,
    MSK_CLUSTER_USE_SASL_IAM,
    MSK_CLUSTER_USE_SASL_SCRAM,
    MSK_CLUSTER_USE_TLS_AUTH,
)

CLUSTER_PUBLICLY_ADDRESSED_CON_T = "MskClusterPubliclyAddressed"
CLUSTER_PUBLICLY_ADDRESSED_CON = Equals(Ref(MSK_CLUSTER_ADDRESSING_TYPE), "PUBLIC")

CLUSTER_PRIVATE_ONLY_CON_T = "MskClusterPrivateOnly"
CLUSTER_PRIVATE_ONLY_CON = Not(Condition(CLUSTER_PUBLICLY_ADDRESSED_CON_T))

CLIENTS_USE_SASL_IAM_CON_T = "UseSaslIamCondition"
CLIENTS_USE_SASL_IAM_CON = Equals(Ref(MSK_CLUSTER_USE_SASL_IAM), "True")

CLIENTS_USE_SASL_SCRAM_CON_T = "UseSaslIamCondition"
CLIENTS_USE_SASL_SCRAM_CON = Equals(Ref(MSK_CLUSTER_USE_SASL_SCRAM), "True")

CLIENTS_USE_TLS_AUTH_CON_T = "UseTlsAuthCondition"
CLIENTS_USE_TLS_AUTH_CON = Equals(Ref(MSK_CLUSTER_USE_TLS_AUTH), "True")
