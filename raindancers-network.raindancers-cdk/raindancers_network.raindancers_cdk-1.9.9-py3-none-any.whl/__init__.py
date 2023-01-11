'''
# Raindancers Network Construct Library...

The raindancers network package contains  constructs that construct to provide easy to use abstractions, particually for using in an enterprise network, with Transit Gateways, Cloudwan, Network Firewalls.

Note: This Construct Library is functional, but there is no promise thate that breaking changes could occur.    While this construct is highly opinionated, it seeks to solve a wide set of scenerios that its author has faced, and problems that others have described.   The author of this construct encourages and welcome PR's.  Please raise an issue to start

The EnterpriseVPC provides addtional methods from the standard ec2.Vpc construct, while maintaining compatiblity, so it can be used with other constructs that use the ec2.Vpc

A getting started example provides guidence in using the constructs.

* [Getting Started](./docs/gettingstarted.md)
* [Deploying VPC with Cloudwan](./docs/deployVpcts.md)
* [Create A shared Egress VPC](./docs/egress.md)

Slack:  A good way to to get help with this construct, is to join the [cdk.dev] (https://cdk.dev/) slack channel.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk
import aws_cdk.aws_dynamodb
import aws_cdk.aws_ec2
import aws_cdk.aws_networkfirewall
import aws_cdk.aws_networkmanager
import aws_cdk.aws_route53
import aws_cdk.aws_route53resolver
import aws_cdk.aws_s3
import aws_cdk.aws_sns
import aws_cdk.custom_resources
import constructs


@jsii.data_type(
    jsii_type="raindancers-network.AddCoreRoutesProps",
    jsii_struct_bases=[],
    name_mapping={
        "attachment_id": "attachmentId",
        "core_name": "coreName",
        "description": "description",
        "destination_cidr_blocks": "destinationCidrBlocks",
        "policy_table_arn": "policyTableArn",
        "segments": "segments",
    },
)
class AddCoreRoutesProps:
    def __init__(
        self,
        *,
        attachment_id: builtins.str,
        core_name: builtins.str,
        description: builtins.str,
        destination_cidr_blocks: typing.Sequence[builtins.str],
        policy_table_arn: builtins.str,
        segments: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param attachment_id: 
        :param core_name: 
        :param description: 
        :param destination_cidr_blocks: 
        :param policy_table_arn: 
        :param segments: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AddCoreRoutesProps.__init__)
            check_type(argname="argument attachment_id", value=attachment_id, expected_type=type_hints["attachment_id"])
            check_type(argname="argument core_name", value=core_name, expected_type=type_hints["core_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument destination_cidr_blocks", value=destination_cidr_blocks, expected_type=type_hints["destination_cidr_blocks"])
            check_type(argname="argument policy_table_arn", value=policy_table_arn, expected_type=type_hints["policy_table_arn"])
            check_type(argname="argument segments", value=segments, expected_type=type_hints["segments"])
        self._values: typing.Dict[str, typing.Any] = {
            "attachment_id": attachment_id,
            "core_name": core_name,
            "description": description,
            "destination_cidr_blocks": destination_cidr_blocks,
            "policy_table_arn": policy_table_arn,
            "segments": segments,
        }

    @builtins.property
    def attachment_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("attachment_id")
        assert result is not None, "Required property 'attachment_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def core_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("core_name")
        assert result is not None, "Required property 'core_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_cidr_blocks(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("destination_cidr_blocks")
        assert result is not None, "Required property 'destination_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def policy_table_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("policy_table_arn")
        assert result is not None, "Required property 'policy_table_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def segments(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("segments")
        assert result is not None, "Required property 'segments' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddCoreRoutesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.AddR53ZoneProps",
    jsii_struct_bases=[],
    name_mapping={"zone": "zone", "central_vpc": "centralVpc"},
)
class AddR53ZoneProps:
    def __init__(
        self,
        *,
        zone: builtins.str,
        central_vpc: typing.Optional[aws_cdk.aws_ec2.Vpc] = None,
    ) -> None:
        '''
        :param zone: 
        :param central_vpc: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AddR53ZoneProps.__init__)
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
            check_type(argname="argument central_vpc", value=central_vpc, expected_type=type_hints["central_vpc"])
        self._values: typing.Dict[str, typing.Any] = {
            "zone": zone,
        }
        if central_vpc is not None:
            self._values["central_vpc"] = central_vpc

    @builtins.property
    def zone(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("zone")
        assert result is not None, "Required property 'zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def central_vpc(self) -> typing.Optional[aws_cdk.aws_ec2.Vpc]:
        '''
        :stability: experimental
        '''
        result = self._values.get("central_vpc")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.Vpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddR53ZoneProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.AddRoutesProps",
    jsii_struct_bases=[],
    name_mapping={
        "cidr": "cidr",
        "description": "description",
        "destination": "destination",
        "subnet_groups": "subnetGroups",
        "cloudwan_name": "cloudwanName",
        "network_firewall_arn": "networkFirewallArn",
    },
)
class AddRoutesProps:
    def __init__(
        self,
        *,
        cidr: typing.Sequence[builtins.str],
        description: builtins.str,
        destination: "Destination",
        subnet_groups: typing.Sequence[builtins.str],
        cloudwan_name: typing.Optional[builtins.str] = None,
        network_firewall_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Propertys for Adding Routes in VPC.

        :param cidr: 
        :param description: 
        :param destination: 
        :param subnet_groups: 
        :param cloudwan_name: 
        :param network_firewall_arn: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AddRoutesProps.__init__)
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument subnet_groups", value=subnet_groups, expected_type=type_hints["subnet_groups"])
            check_type(argname="argument cloudwan_name", value=cloudwan_name, expected_type=type_hints["cloudwan_name"])
            check_type(argname="argument network_firewall_arn", value=network_firewall_arn, expected_type=type_hints["network_firewall_arn"])
        self._values: typing.Dict[str, typing.Any] = {
            "cidr": cidr,
            "description": description,
            "destination": destination,
            "subnet_groups": subnet_groups,
        }
        if cloudwan_name is not None:
            self._values["cloudwan_name"] = cloudwan_name
        if network_firewall_arn is not None:
            self._values["network_firewall_arn"] = network_firewall_arn

    @builtins.property
    def cidr(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cidr")
        assert result is not None, "Required property 'cidr' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination(self) -> "Destination":
        '''
        :stability: experimental
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast("Destination", result)

    @builtins.property
    def subnet_groups(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnet_groups")
        assert result is not None, "Required property 'subnet_groups' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cloudwan_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cloudwan_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_firewall_arn(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("network_firewall_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddRoutesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.ApplianceMode")
class ApplianceMode(enum.Enum):
    '''(experimental) Propertys for Appliance Mode.

    :stability: experimental
    '''

    ENABLED = "ENABLED"
    '''(experimental) enable Connecting VPC to TransitGateway in Appliance Mode.

    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.AssociationMethod")
class AssociationMethod(enum.Enum):
    '''(experimental) Association Methods.

    :stability: experimental
    '''

    CONSTANT = "CONSTANT"
    '''
    :stability: experimental
    '''
    TAG = "TAG"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="raindancers-network.AttachToCloudWanProps",
    jsii_struct_bases=[],
    name_mapping={
        "core_network_name": "coreNetworkName",
        "segment_name": "segmentName",
        "appliance_mode": "applianceMode",
        "attachment_subnet_group": "attachmentSubnetGroup",
    },
)
class AttachToCloudWanProps:
    def __init__(
        self,
        *,
        core_network_name: builtins.str,
        segment_name: builtins.str,
        appliance_mode: typing.Optional[builtins.bool] = None,
        attachment_subnet_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Propertys for Attaching to a Cloudwan Core Network.

        :param core_network_name: (experimental) corenetworkName.
        :param segment_name: 
        :param appliance_mode: 
        :param attachment_subnet_group: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AttachToCloudWanProps.__init__)
            check_type(argname="argument core_network_name", value=core_network_name, expected_type=type_hints["core_network_name"])
            check_type(argname="argument segment_name", value=segment_name, expected_type=type_hints["segment_name"])
            check_type(argname="argument appliance_mode", value=appliance_mode, expected_type=type_hints["appliance_mode"])
            check_type(argname="argument attachment_subnet_group", value=attachment_subnet_group, expected_type=type_hints["attachment_subnet_group"])
        self._values: typing.Dict[str, typing.Any] = {
            "core_network_name": core_network_name,
            "segment_name": segment_name,
        }
        if appliance_mode is not None:
            self._values["appliance_mode"] = appliance_mode
        if attachment_subnet_group is not None:
            self._values["attachment_subnet_group"] = attachment_subnet_group

    @builtins.property
    def core_network_name(self) -> builtins.str:
        '''(experimental) corenetworkName.

        :stability: experimental
        '''
        result = self._values.get("core_network_name")
        assert result is not None, "Required property 'core_network_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def segment_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("segment_name")
        assert result is not None, "Required property 'segment_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def appliance_mode(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("appliance_mode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def attachment_subnet_group(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("attachment_subnet_group")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttachToCloudWanProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.AttachToTransitGatewayProps",
    jsii_struct_bases=[],
    name_mapping={
        "transit_gateway": "transitGateway",
        "applicance_mode": "applicanceMode",
        "attachment_subnet_group": "attachmentSubnetGroup",
    },
)
class AttachToTransitGatewayProps:
    def __init__(
        self,
        *,
        transit_gateway: aws_cdk.aws_ec2.CfnTransitGateway,
        applicance_mode: typing.Optional[ApplianceMode] = None,
        attachment_subnet_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Propertys to attach the Vpc To Transit Gateway.

        :param transit_gateway: (experimental) the TransitGateway to connect to.
        :param applicance_mode: (experimental) Will this be connected in appliance mode ( used if you have Network Firewalls ).
        :param attachment_subnet_group: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AttachToTransitGatewayProps.__init__)
            check_type(argname="argument transit_gateway", value=transit_gateway, expected_type=type_hints["transit_gateway"])
            check_type(argname="argument applicance_mode", value=applicance_mode, expected_type=type_hints["applicance_mode"])
            check_type(argname="argument attachment_subnet_group", value=attachment_subnet_group, expected_type=type_hints["attachment_subnet_group"])
        self._values: typing.Dict[str, typing.Any] = {
            "transit_gateway": transit_gateway,
        }
        if applicance_mode is not None:
            self._values["applicance_mode"] = applicance_mode
        if attachment_subnet_group is not None:
            self._values["attachment_subnet_group"] = attachment_subnet_group

    @builtins.property
    def transit_gateway(self) -> aws_cdk.aws_ec2.CfnTransitGateway:
        '''(experimental) the TransitGateway to connect to.

        :stability: experimental
        '''
        result = self._values.get("transit_gateway")
        assert result is not None, "Required property 'transit_gateway' is missing"
        return typing.cast(aws_cdk.aws_ec2.CfnTransitGateway, result)

    @builtins.property
    def applicance_mode(self) -> typing.Optional[ApplianceMode]:
        '''(experimental) Will this be connected in appliance mode ( used if you have Network Firewalls ).

        :stability: experimental
        '''
        result = self._values.get("applicance_mode")
        return typing.cast(typing.Optional[ApplianceMode], result)

    @builtins.property
    def attachment_subnet_group(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("attachment_subnet_group")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttachToTransitGatewayProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.AttachmentCondition")
class AttachmentCondition(enum.Enum):
    '''(experimental) Attachment Conditions.

    :stability: experimental
    '''

    ANY = "ANY"
    '''
    :stability: experimental
    '''
    RESOURCE_ID = "RESOURCE_ID"
    '''
    :stability: experimental
    '''
    ACCOUNT_ID = "ACCOUNT_ID"
    '''
    :stability: experimental
    '''
    REGION = "REGION"
    '''
    :stability: experimental
    '''
    ATTACHMENT_TYPE = "ATTACHMENT_TYPE"
    '''
    :stability: experimental
    '''
    TAG_EXISTS = "TAG_EXISTS"
    '''
    :stability: experimental
    '''
    TAG_VALUE = "TAG_VALUE"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="raindancers-network.AttachmentConditions",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "key": "key",
        "operator": "operator",
        "value": "value",
    },
)
class AttachmentConditions:
    def __init__(
        self,
        *,
        type: AttachmentCondition,
        key: typing.Optional[builtins.str] = None,
        operator: typing.Optional["Operators"] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) an attachmentconditions.

        :param type: 
        :param key: 
        :param operator: 
        :param value: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AttachmentConditions.__init__)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[str, typing.Any] = {
            "type": type,
        }
        if key is not None:
            self._values["key"] = key
        if operator is not None:
            self._values["operator"] = operator
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type(self) -> AttachmentCondition:
        '''
        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(AttachmentCondition, result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional["Operators"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional["Operators"], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttachmentConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.AttachmentPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "conditions": "conditions",
        "rule_number": "ruleNumber",
        "condition_logic": "conditionLogic",
        "description": "description",
    },
)
class AttachmentPolicy:
    def __init__(
        self,
        *,
        action: typing.Union["AttachmentPolicyAction", typing.Dict[str, typing.Any]],
        conditions: typing.Sequence[typing.Union[AttachmentConditions, typing.Dict[str, typing.Any]]],
        rule_number: jsii.Number,
        condition_logic: typing.Optional["ConditionLogic"] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) an attachment policy.

        :param action: 
        :param conditions: 
        :param rule_number: 
        :param condition_logic: 
        :param description: 

        :stability: experimental
        '''
        if isinstance(action, dict):
            action = AttachmentPolicyAction(**action)
        if __debug__:
            type_hints = typing.get_type_hints(AttachmentPolicy.__init__)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument rule_number", value=rule_number, expected_type=type_hints["rule_number"])
            check_type(argname="argument condition_logic", value=condition_logic, expected_type=type_hints["condition_logic"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[str, typing.Any] = {
            "action": action,
            "conditions": conditions,
            "rule_number": rule_number,
        }
        if condition_logic is not None:
            self._values["condition_logic"] = condition_logic
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def action(self) -> "AttachmentPolicyAction":
        '''
        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("AttachmentPolicyAction", result)

    @builtins.property
    def conditions(self) -> typing.List[AttachmentConditions]:
        '''
        :stability: experimental
        '''
        result = self._values.get("conditions")
        assert result is not None, "Required property 'conditions' is missing"
        return typing.cast(typing.List[AttachmentConditions], result)

    @builtins.property
    def rule_number(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("rule_number")
        assert result is not None, "Required property 'rule_number' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def condition_logic(self) -> typing.Optional["ConditionLogic"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("condition_logic")
        return typing.cast(typing.Optional["ConditionLogic"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttachmentPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.AttachmentPolicyAction",
    jsii_struct_bases=[],
    name_mapping={"association_method": "associationMethod", "segment": "segment"},
)
class AttachmentPolicyAction:
    def __init__(
        self,
        *,
        association_method: AssociationMethod,
        segment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Attachment Policy Action.

        :param association_method: (experimental) The Assocation Method.
        :param segment: (experimental) The Segment this applies to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AttachmentPolicyAction.__init__)
            check_type(argname="argument association_method", value=association_method, expected_type=type_hints["association_method"])
            check_type(argname="argument segment", value=segment, expected_type=type_hints["segment"])
        self._values: typing.Dict[str, typing.Any] = {
            "association_method": association_method,
        }
        if segment is not None:
            self._values["segment"] = segment

    @builtins.property
    def association_method(self) -> AssociationMethod:
        '''(experimental) The Assocation Method.

        :stability: experimental
        '''
        result = self._values.get("association_method")
        assert result is not None, "Required property 'association_method' is missing"
        return typing.cast(AssociationMethod, result)

    @builtins.property
    def segment(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Segment this applies to.

        :stability: experimental
        '''
        result = self._values.get("segment")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttachmentPolicyAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AwsServiceEndPoints(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.AwsServiceEndPoints",
):
    '''(experimental) Provisions a set of AWS Service Endpoints in a VPC.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        services: typing.Sequence[aws_cdk.aws_ec2.InterfaceVpcEndpointAwsService],
        subnet_group: builtins.str,
        vpc: aws_cdk.aws_ec2.Vpc,
        dynamo_db_gateway_interface: typing.Optional[builtins.bool] = None,
        s3_gateway_interface: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: The scope that this construct is created in.
        :param id: Id for the construct.
        :param services: (experimental) An arry of InterfaceVPCEndpoints.
        :param subnet_group: (experimental) Subnet Group in which to create the service. Typically a subnet Dedicated to the task
        :param vpc: (experimental) The vpc in which the service is created.
        :param dynamo_db_gateway_interface: (experimental) indicate true for a Dynamo Gateway Interface.
        :param s3_gateway_interface: (experimental) indicate true for a S3 Gateway Interface.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AwsServiceEndPoints.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AwsServiceEndPointsProps(
            services=services,
            subnet_group=subnet_group,
            vpc=vpc,
            dynamo_db_gateway_interface=dynamo_db_gateway_interface,
            s3_gateway_interface=s3_gateway_interface,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="raindancers-network.AwsServiceEndPointsProps",
    jsii_struct_bases=[],
    name_mapping={
        "services": "services",
        "subnet_group": "subnetGroup",
        "vpc": "vpc",
        "dynamo_db_gateway_interface": "dynamoDBGatewayInterface",
        "s3_gateway_interface": "s3GatewayInterface",
    },
)
class AwsServiceEndPointsProps:
    def __init__(
        self,
        *,
        services: typing.Sequence[aws_cdk.aws_ec2.InterfaceVpcEndpointAwsService],
        subnet_group: builtins.str,
        vpc: aws_cdk.aws_ec2.Vpc,
        dynamo_db_gateway_interface: typing.Optional[builtins.bool] = None,
        s3_gateway_interface: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties to create a set of AWS service Endpoints.

        :param services: (experimental) An arry of InterfaceVPCEndpoints.
        :param subnet_group: (experimental) Subnet Group in which to create the service. Typically a subnet Dedicated to the task
        :param vpc: (experimental) The vpc in which the service is created.
        :param dynamo_db_gateway_interface: (experimental) indicate true for a Dynamo Gateway Interface.
        :param s3_gateway_interface: (experimental) indicate true for a S3 Gateway Interface.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AwsServiceEndPointsProps.__init__)
            check_type(argname="argument services", value=services, expected_type=type_hints["services"])
            check_type(argname="argument subnet_group", value=subnet_group, expected_type=type_hints["subnet_group"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument dynamo_db_gateway_interface", value=dynamo_db_gateway_interface, expected_type=type_hints["dynamo_db_gateway_interface"])
            check_type(argname="argument s3_gateway_interface", value=s3_gateway_interface, expected_type=type_hints["s3_gateway_interface"])
        self._values: typing.Dict[str, typing.Any] = {
            "services": services,
            "subnet_group": subnet_group,
            "vpc": vpc,
        }
        if dynamo_db_gateway_interface is not None:
            self._values["dynamo_db_gateway_interface"] = dynamo_db_gateway_interface
        if s3_gateway_interface is not None:
            self._values["s3_gateway_interface"] = s3_gateway_interface

    @builtins.property
    def services(self) -> typing.List[aws_cdk.aws_ec2.InterfaceVpcEndpointAwsService]:
        '''(experimental) An arry of InterfaceVPCEndpoints.

        :stability: experimental
        '''
        result = self._values.get("services")
        assert result is not None, "Required property 'services' is missing"
        return typing.cast(typing.List[aws_cdk.aws_ec2.InterfaceVpcEndpointAwsService], result)

    @builtins.property
    def subnet_group(self) -> builtins.str:
        '''(experimental) Subnet Group in which to create the service.

        Typically a subnet Dedicated to the task

        :stability: experimental
        '''
        result = self._values.get("subnet_group")
        assert result is not None, "Required property 'subnet_group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.Vpc:
        '''(experimental) The vpc in which the service is created.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.Vpc, result)

    @builtins.property
    def dynamo_db_gateway_interface(self) -> typing.Optional[builtins.bool]:
        '''(experimental) indicate true for a Dynamo Gateway Interface.

        :stability: experimental
        '''
        result = self._values.get("dynamo_db_gateway_interface")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def s3_gateway_interface(self) -> typing.Optional[builtins.bool]:
        '''(experimental) indicate true for a S3 Gateway Interface.

        :stability: experimental
        '''
        result = self._values.get("s3_gateway_interface")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsServiceEndPointsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.CloudWanRoutingProtocolProps",
    jsii_struct_bases=[],
    name_mapping={
        "subnet_groups": "subnetGroups",
        "accept_route_filter": "acceptRouteFilter",
        "deny_route_filter": "denyRouteFilter",
    },
)
class CloudWanRoutingProtocolProps:
    def __init__(
        self,
        *,
        subnet_groups: typing.Sequence[builtins.str],
        accept_route_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        deny_route_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param subnet_groups: 
        :param accept_route_filter: 
        :param deny_route_filter: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CloudWanRoutingProtocolProps.__init__)
            check_type(argname="argument subnet_groups", value=subnet_groups, expected_type=type_hints["subnet_groups"])
            check_type(argname="argument accept_route_filter", value=accept_route_filter, expected_type=type_hints["accept_route_filter"])
            check_type(argname="argument deny_route_filter", value=deny_route_filter, expected_type=type_hints["deny_route_filter"])
        self._values: typing.Dict[str, typing.Any] = {
            "subnet_groups": subnet_groups,
        }
        if accept_route_filter is not None:
            self._values["accept_route_filter"] = accept_route_filter
        if deny_route_filter is not None:
            self._values["deny_route_filter"] = deny_route_filter

    @builtins.property
    def subnet_groups(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnet_groups")
        assert result is not None, "Required property 'subnet_groups' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def accept_route_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("accept_route_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deny_route_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("deny_route_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudWanRoutingProtocolProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudWanTGW(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.CloudWanTGW",
):
    '''(experimental) Create a TransitGateway That is attached to Cloudwan.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        amazon_side_asn: builtins.str,
        attachment_segment: builtins.str,
        cloudwan: "CoreNetwork",
        description: builtins.str,
        cloud_wan_cidr: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_route_in_segments: typing.Optional[typing.Sequence[builtins.str]] = None,
        tg_cidr: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: scope in which the resource is c.
        :param id: -
        :param amazon_side_asn: 
        :param attachment_segment: 
        :param cloudwan: 
        :param description: 
        :param cloud_wan_cidr: 
        :param default_route_in_segments: 
        :param tg_cidr: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CloudWanTGW.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TGWOnCloudWanProps(
            amazon_side_asn=amazon_side_asn,
            attachment_segment=attachment_segment,
            cloudwan=cloudwan,
            description=description,
            cloud_wan_cidr=cloud_wan_cidr,
            default_route_in_segments=default_route_in_segments,
            tg_cidr=tg_cidr,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addDXGateway")
    def add_dx_gateway(
        self,
        dxgatewayname: builtins.str,
        dxgateway_asn: jsii.Number,
    ) -> builtins.str:
        '''(experimental) provision a DX Gateway and attach it to the transit gateway.

        :param dxgatewayname: The name of the dxgateway.
        :param dxgateway_asn: An ASN for the Dxgateway.

        :return: Direct Connect gatewayId

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CloudWanTGW.add_dx_gateway)
            check_type(argname="argument dxgatewayname", value=dxgatewayname, expected_type=type_hints["dxgatewayname"])
            check_type(argname="argument dxgateway_asn", value=dxgateway_asn, expected_type=type_hints["dxgateway_asn"])
        return typing.cast(builtins.str, jsii.invoke(self, "addDXGateway", [dxgatewayname, dxgateway_asn]))

    @jsii.member(jsii_name="adds2sVPN")
    def adds2s_vpn(
        self,
        name: builtins.str,
        *,
        customer_gateway: aws_cdk.aws_ec2.CfnCustomerGateway,
        vpnspec: typing.Union["VpnSpecProps", typing.Dict[str, typing.Any]],
        sampleconfig: typing.Optional[typing.Union["SampleConfig", typing.Dict[str, typing.Any]]] = None,
        tunnel_inside_cidr: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel_ipam_pool: typing.Optional[aws_cdk.aws_ec2.CfnIPAMPool] = None,
    ) -> None:
        '''(experimental) Creates a Site To Site IPSec VPN between the Transit Gateway and Customer Gateway, using a defined set of VPn Properties.

        :param name: A name to identify the vpn.
        :param customer_gateway: (experimental) The customer gateway where the vpn will terminate.
        :param vpnspec: (experimental) a VPN specification for the VPN.
        :param sampleconfig: (experimental) Optionally provide a sampleconfig specification.
        :param tunnel_inside_cidr: (experimental) Specify a pair of concrete Cidr's for the tunnel. Only use one of tunnelInsideCidr or tunnelIpmamPool
        :param tunnel_ipam_pool: (experimental) Specify an ipam pool to allocated the tunnel address's from. Use only one of tunnelInsideCidr or tunnelIpamPool

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CloudWanTGW.adds2s_vpn)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        vpnprops = VpnProps(
            customer_gateway=customer_gateway,
            vpnspec=vpnspec,
            sampleconfig=sampleconfig,
            tunnel_inside_cidr=tunnel_inside_cidr,
            tunnel_ipam_pool=tunnel_ipam_pool,
        )

        return typing.cast(None, jsii.invoke(self, "adds2sVPN", [name, vpnprops]))

    @jsii.member(jsii_name="createDirectConnectGatewayAssociation")
    def create_direct_connect_gateway_association(
        self,
        dxgateway_id: builtins.str,
    ) -> builtins.str:
        '''
        :param dxgateway_id: Id of a DX gateway that.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CloudWanTGW.create_direct_connect_gateway_association)
            check_type(argname="argument dxgateway_id", value=dxgateway_id, expected_type=type_hints["dxgateway_id"])
        return typing.cast(builtins.str, jsii.invoke(self, "createDirectConnectGatewayAssociation", [dxgateway_id]))

    @builtins.property
    @jsii.member(jsii_name="cloudwanTgAttachmentId")
    def cloudwan_tg_attachment_id(self) -> builtins.str:
        '''(experimental) the AttachmentId between the Transit Gateway and the cloudwan.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "cloudwanTgAttachmentId"))

    @builtins.property
    @jsii.member(jsii_name="transitGateway")
    def transit_gateway(self) -> aws_cdk.aws_ec2.CfnTransitGateway:
        '''(experimental) The created Transit Gateway.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_ec2.CfnTransitGateway, jsii.get(self, "transitGateway"))

    @builtins.property
    @jsii.member(jsii_name="tgcidr")
    def tgcidr(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The Cidr Ranges assigned to the transit Gateway.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tgcidr"))

    @builtins.property
    @jsii.member(jsii_name="tgDXattachmentId")
    def tg_d_xattachment_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) the AttachmentId between the Transit Gateway and DX ( if any ).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tgDXattachmentId"))

    @tg_d_xattachment_id.setter
    def tg_d_xattachment_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CloudWanTGW, "tg_d_xattachment_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tgDXattachmentId", value)


@jsii.enum(jsii_type="raindancers-network.ConditionLogic")
class ConditionLogic(enum.Enum):
    '''(experimental) Conditon Logic.

    :stability: experimental
    '''

    AND = "AND"
    '''
    :stability: experimental
    '''
    OR = "OR"
    '''
    :stability: experimental
    '''


class CoreNetwork(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.CoreNetwork",
):
    '''(experimental) Create a CoreNework for a Cloudwan.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        asn_ranges: typing.Sequence[builtins.str],
        core_name: builtins.str,
        edge_locations: typing.Sequence[typing.Mapping[typing.Any, typing.Any]],
        global_network: aws_cdk.aws_networkmanager.CfnGlobalNetwork,
        policy_description: builtins.str,
        inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpn_ecmp_support: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param asn_ranges: (experimental) a list of of asn's that can be used.
        :param core_name: (experimental) core name.
        :param edge_locations: (experimental) list of edgeLocaitons.
        :param global_network: (experimental) Which Global Network.
        :param policy_description: (experimental) a decription for the policy Document.
        :param inside_cidr_blocks: (experimental) List of InsideCidr Blocks.
        :param vpn_ecmp_support: (experimental) support VpnECmp.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CoreNetwork.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CoreNetworkProps(
            asn_ranges=asn_ranges,
            core_name=core_name,
            edge_locations=edge_locations,
            global_network=global_network,
            policy_description=policy_description,
            inside_cidr_blocks=inside_cidr_blocks,
            vpn_ecmp_support=vpn_ecmp_support,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addSegment")
    def add_segment(
        self,
        *,
        name: builtins.str,
        allow_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        deny_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        edge_locations: typing.Optional[typing.Sequence[typing.Mapping[typing.Any, typing.Any]]] = None,
        isolate_attachments: typing.Optional[builtins.bool] = None,
        require_attachment_acceptance: typing.Optional[builtins.bool] = None,
    ) -> "CoreNetworkSegment":
        '''(experimental) Add a segment to the core network.

        :param name: (experimental) Name of the Segment.
        :param allow_filter: (experimental) A list of denys.
        :param deny_filter: (experimental) a List of denys.
        :param description: (experimental) A description of the of the segement.
        :param edge_locations: (experimental) A list of edge locations where the segement will be avaialble. Not that the locations must also be included in the core network edge ( CNE )
        :param isolate_attachments: (experimental) Set true if attached VPCS are isolated from each other.
        :param require_attachment_acceptance: (experimental) Set true if the attachment needs approval for connection. Currently not supported and requires an automation step

        :stability: experimental
        '''
        props = Segment(
            name=name,
            allow_filter=allow_filter,
            deny_filter=deny_filter,
            description=description,
            edge_locations=edge_locations,
            isolate_attachments=isolate_attachments,
            require_attachment_acceptance=require_attachment_acceptance,
        )

        return typing.cast("CoreNetworkSegment", jsii.invoke(self, "addSegment", [props]))

    @jsii.member(jsii_name="share")
    def share(
        self,
        *,
        allow_external_principals: builtins.bool,
        principals: typing.Sequence[builtins.str],
        tags: typing.Optional[typing.Sequence[aws_cdk.Tag]] = None,
    ) -> None:
        '''(experimental) Create a CoreNetwork Sharing.

        :param allow_external_principals: 
        :param principals: 
        :param tags: 

        :stability: experimental
        '''
        props = CoreNetworkShare(
            allow_external_principals=allow_external_principals,
            principals=principals,
            tags=tags,
        )

        return typing.cast(None, jsii.invoke(self, "share", [props]))

    @jsii.member(jsii_name="updatePolicy")
    def update_policy(self) -> None:
        '''(experimental) Update the corewan policy after actions, segments are added.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "updatePolicy", []))

    @builtins.property
    @jsii.member(jsii_name="cfnCoreNetwork")
    def cfn_core_network(self) -> aws_cdk.aws_networkmanager.CfnCoreNetwork:
        '''(experimental) The corenetwork object.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_networkmanager.CfnCoreNetwork, jsii.get(self, "cfnCoreNetwork"))

    @builtins.property
    @jsii.member(jsii_name="coreName")
    def core_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "coreName"))

    @builtins.property
    @jsii.member(jsii_name="policyTable")
    def policy_table(self) -> aws_cdk.aws_dynamodb.Table:
        '''(experimental) THe dynamo table holding the policy.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_dynamodb.Table, jsii.get(self, "policyTable"))

    @builtins.property
    @jsii.member(jsii_name="policyTableName")
    def policy_table_name(self) -> builtins.str:
        '''(experimental) Name of the Dynamo Table holding the policy.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyTableName"))

    @builtins.property
    @jsii.member(jsii_name="policyTableServiceToken")
    def policy_table_service_token(self) -> builtins.str:
        '''(experimental) The policyTable Lamba's Service Token.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyTableServiceToken"))

    @builtins.property
    @jsii.member(jsii_name="updateProviderToken")
    def update_provider_token(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "updateProviderToken"))

    @update_provider_token.setter
    def update_provider_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CoreNetwork, "update_provider_token").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateProviderToken", value)


@jsii.data_type(
    jsii_type="raindancers-network.CoreNetworkProps",
    jsii_struct_bases=[],
    name_mapping={
        "asn_ranges": "asnRanges",
        "core_name": "coreName",
        "edge_locations": "edgeLocations",
        "global_network": "globalNetwork",
        "policy_description": "policyDescription",
        "inside_cidr_blocks": "insideCidrBlocks",
        "vpn_ecmp_support": "vpnEcmpSupport",
    },
)
class CoreNetworkProps:
    def __init__(
        self,
        *,
        asn_ranges: typing.Sequence[builtins.str],
        core_name: builtins.str,
        edge_locations: typing.Sequence[typing.Mapping[typing.Any, typing.Any]],
        global_network: aws_cdk.aws_networkmanager.CfnGlobalNetwork,
        policy_description: builtins.str,
        inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpn_ecmp_support: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) CoreNetwork Properties.

        :param asn_ranges: (experimental) a list of of asn's that can be used.
        :param core_name: (experimental) core name.
        :param edge_locations: (experimental) list of edgeLocaitons.
        :param global_network: (experimental) Which Global Network.
        :param policy_description: (experimental) a decription for the policy Document.
        :param inside_cidr_blocks: (experimental) List of InsideCidr Blocks.
        :param vpn_ecmp_support: (experimental) support VpnECmp.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CoreNetworkProps.__init__)
            check_type(argname="argument asn_ranges", value=asn_ranges, expected_type=type_hints["asn_ranges"])
            check_type(argname="argument core_name", value=core_name, expected_type=type_hints["core_name"])
            check_type(argname="argument edge_locations", value=edge_locations, expected_type=type_hints["edge_locations"])
            check_type(argname="argument global_network", value=global_network, expected_type=type_hints["global_network"])
            check_type(argname="argument policy_description", value=policy_description, expected_type=type_hints["policy_description"])
            check_type(argname="argument inside_cidr_blocks", value=inside_cidr_blocks, expected_type=type_hints["inside_cidr_blocks"])
            check_type(argname="argument vpn_ecmp_support", value=vpn_ecmp_support, expected_type=type_hints["vpn_ecmp_support"])
        self._values: typing.Dict[str, typing.Any] = {
            "asn_ranges": asn_ranges,
            "core_name": core_name,
            "edge_locations": edge_locations,
            "global_network": global_network,
            "policy_description": policy_description,
        }
        if inside_cidr_blocks is not None:
            self._values["inside_cidr_blocks"] = inside_cidr_blocks
        if vpn_ecmp_support is not None:
            self._values["vpn_ecmp_support"] = vpn_ecmp_support

    @builtins.property
    def asn_ranges(self) -> typing.List[builtins.str]:
        '''(experimental) a list of of asn's that can be used.

        :stability: experimental
        '''
        result = self._values.get("asn_ranges")
        assert result is not None, "Required property 'asn_ranges' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def core_name(self) -> builtins.str:
        '''(experimental) core name.

        :stability: experimental
        '''
        result = self._values.get("core_name")
        assert result is not None, "Required property 'core_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def edge_locations(self) -> typing.List[typing.Mapping[typing.Any, typing.Any]]:
        '''(experimental) list of edgeLocaitons.

        :stability: experimental
        '''
        result = self._values.get("edge_locations")
        assert result is not None, "Required property 'edge_locations' is missing"
        return typing.cast(typing.List[typing.Mapping[typing.Any, typing.Any]], result)

    @builtins.property
    def global_network(self) -> aws_cdk.aws_networkmanager.CfnGlobalNetwork:
        '''(experimental) Which Global Network.

        :stability: experimental
        '''
        result = self._values.get("global_network")
        assert result is not None, "Required property 'global_network' is missing"
        return typing.cast(aws_cdk.aws_networkmanager.CfnGlobalNetwork, result)

    @builtins.property
    def policy_description(self) -> builtins.str:
        '''(experimental) a decription for the policy Document.

        :stability: experimental
        '''
        result = self._values.get("policy_description")
        assert result is not None, "Required property 'policy_description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def inside_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of InsideCidr Blocks.

        :stability: experimental
        '''
        result = self._values.get("inside_cidr_blocks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpn_ecmp_support(self) -> typing.Optional[builtins.bool]:
        '''(experimental) support VpnECmp.

        :stability: experimental
        '''
        result = self._values.get("vpn_ecmp_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CoreNetworkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CoreNetworkSegment(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.CoreNetworkSegment",
):
    '''(experimental) Create a Network Segment in a core network.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        props: "ICoreNetworkSegmentProps",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CoreNetworkSegment.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addAttachmentPolicy")
    def add_attachment_policy(
        self,
        *,
        action: typing.Union[AttachmentPolicyAction, typing.Dict[str, typing.Any]],
        conditions: typing.Sequence[typing.Union[AttachmentConditions, typing.Dict[str, typing.Any]]],
        rule_number: jsii.Number,
        condition_logic: typing.Optional[ConditionLogic] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Add an AttachmentPolicy to a segment.

        :param action: 
        :param conditions: 
        :param rule_number: 
        :param condition_logic: 
        :param description: 

        :stability: experimental
        '''
        props = AttachmentPolicy(
            action=action,
            conditions=conditions,
            rule_number=rule_number,
            condition_logic=condition_logic,
            description=description,
        )

        return typing.cast(None, jsii.invoke(self, "addAttachmentPolicy", [props]))

    @jsii.member(jsii_name="addSegmentAction")
    def add_segment_action(
        self,
        *,
        action: "SegmentActionType",
        description: builtins.str,
        destination_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
        except_: typing.Optional[typing.Sequence[builtins.str]] = None,
        mode: typing.Optional["SegmentActionMode"] = None,
        share_with: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    ) -> None:
        '''(experimental) Add an Action to the Segment, ( Share or Route ).

        :param action: 
        :param description: 
        :param destination_cidr_blocks: 
        :param destinations: 
        :param except_: 
        :param mode: 
        :param share_with: 

        :stability: experimental
        '''
        props = SegmentAction(
            action=action,
            description=description,
            destination_cidr_blocks=destination_cidr_blocks,
            destinations=destinations,
            except_=except_,
            mode=mode,
            share_with=share_with,
        )

        return typing.cast(None, jsii.invoke(self, "addSegmentAction", [props]))

    @jsii.member(jsii_name="addSimpleAttachmentPolicy")
    def add_simple_attachment_policy(
        self,
        *,
        rule_number: jsii.Number,
        account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rule_number: 
        :param account: 

        :stability: experimental
        '''
        props = SimpleAttachmentPolicyProps(rule_number=rule_number, account=account)

        return typing.cast(None, jsii.invoke(self, "addSimpleAttachmentPolicy", [props]))

    @jsii.member(jsii_name="addSimpleShareAction")
    def add_simple_share_action(
        self,
        *,
        description: builtins.str,
        share_with: typing.Union[builtins.str, typing.Sequence["CoreNetworkSegment"]],
    ) -> None:
        '''
        :param description: 
        :param share_with: 

        :stability: experimental
        '''
        props = SimpleShareActionProps(description=description, share_with=share_with)

        return typing.cast(None, jsii.invoke(self, "addSimpleShareAction", [props]))

    @builtins.property
    @jsii.member(jsii_name="policyTableServiceToken")
    def policy_table_service_token(self) -> builtins.str:
        '''(experimental) Service token for.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyTableServiceToken"))

    @builtins.property
    @jsii.member(jsii_name="segmentName")
    def segment_name(self) -> builtins.str:
        '''(experimental) the name for the segment.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "segmentName"))


@jsii.data_type(
    jsii_type="raindancers-network.CoreNetworkShare",
    jsii_struct_bases=[],
    name_mapping={
        "allow_external_principals": "allowExternalPrincipals",
        "principals": "principals",
        "tags": "tags",
    },
)
class CoreNetworkShare:
    def __init__(
        self,
        *,
        allow_external_principals: builtins.bool,
        principals: typing.Sequence[builtins.str],
        tags: typing.Optional[typing.Sequence[aws_cdk.Tag]] = None,
    ) -> None:
        '''(experimental) CoreNetworkShare.

        :param allow_external_principals: 
        :param principals: 
        :param tags: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CoreNetworkShare.__init__)
            check_type(argname="argument allow_external_principals", value=allow_external_principals, expected_type=type_hints["allow_external_principals"])
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[str, typing.Any] = {
            "allow_external_principals": allow_external_principals,
            "principals": principals,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def allow_external_principals(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        result = self._values.get("allow_external_principals")
        assert result is not None, "Required property 'allow_external_principals' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def principals(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("principals")
        assert result is not None, "Required property 'principals' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.Tag]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.Tag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CoreNetworkShare(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.DPDTimeoutAction")
class DPDTimeoutAction(enum.Enum):
    '''(experimental) Dead Peer Detection Timeout Actions.

    :stability: experimental
    '''

    CLEAR = "CLEAR"
    '''(experimental) Clear the Session.

    :stability: experimental
    '''
    NONE = "NONE"
    '''(experimental) Do nothing.

    :stability: experimental
    '''
    RESTART = "RESTART"
    '''(experimental) Restart The Session.

    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.Destination")
class Destination(enum.Enum):
    '''(experimental) The Destinations for Adding Routes.

    :stability: experimental
    '''

    CLOUDWAN = "CLOUDWAN"
    '''(experimental) route to the cloudwan that the vpc is attached to.

    :stability: experimental
    '''
    TRANSITGATEWAY = "TRANSITGATEWAY"
    '''(experimental) route to the transitGateway that the vpc is attached to.

    :stability: experimental
    '''
    NWFIREWALL = "NWFIREWALL"
    '''
    :stability: experimental
    '''


class EnterpriseVpc(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.EnterpriseVpc",
):
    '''(experimental) Enteprise VPC's take the stock ec2.Vpc and provide numerous convience methods primarly related to connecting to internal networks.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        vpc: aws_cdk.aws_ec2.Vpc,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EnterpriseVpc.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EnterpriseVpcProps(vpc=vpc)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addCoreRoutes")
    def add_core_routes(
        self,
        *,
        attachment_id: builtins.str,
        core_name: builtins.str,
        description: builtins.str,
        destination_cidr_blocks: typing.Sequence[builtins.str],
        policy_table_arn: builtins.str,
        segments: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param attachment_id: 
        :param core_name: 
        :param description: 
        :param destination_cidr_blocks: 
        :param policy_table_arn: 
        :param segments: 

        :stability: experimental
        '''
        props = AddCoreRoutesProps(
            attachment_id=attachment_id,
            core_name=core_name,
            description=description,
            destination_cidr_blocks=destination_cidr_blocks,
            policy_table_arn=policy_table_arn,
            segments=segments,
        )

        return typing.cast(None, jsii.invoke(self, "addCoreRoutes", [props]))

    @jsii.member(jsii_name="addR53Zone")
    def add_r53_zone(
        self,
        *,
        zone: builtins.str,
        central_vpc: typing.Optional[aws_cdk.aws_ec2.Vpc] = None,
    ) -> None:
        '''
        :param zone: 
        :param central_vpc: 

        :stability: experimental
        '''
        props = AddR53ZoneProps(zone=zone, central_vpc=central_vpc)

        return typing.cast(None, jsii.invoke(self, "addR53Zone", [props]))

    @jsii.member(jsii_name="addRoutes")
    def add_routes(
        self,
        *,
        cidr: typing.Sequence[builtins.str],
        description: builtins.str,
        destination: Destination,
        subnet_groups: typing.Sequence[builtins.str],
        cloudwan_name: typing.Optional[builtins.str] = None,
        network_firewall_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Add routes to SubnetGroups ( by implication their routing tables ).

        :param cidr: 
        :param description: 
        :param destination: 
        :param subnet_groups: 
        :param cloudwan_name: 
        :param network_firewall_arn: 

        :stability: experimental
        '''
        props = AddRoutesProps(
            cidr=cidr,
            description=description,
            destination=destination,
            subnet_groups=subnet_groups,
            cloudwan_name=cloudwan_name,
            network_firewall_arn=network_firewall_arn,
        )

        return typing.cast(None, jsii.invoke(self, "addRoutes", [props]))

    @jsii.member(jsii_name="attachToCloudWan")
    def attach_to_cloud_wan(
        self,
        *,
        core_network_name: builtins.str,
        segment_name: builtins.str,
        appliance_mode: typing.Optional[builtins.bool] = None,
        attachment_subnet_group: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''(experimental) attachToCloudWan will attach a VPC to CloudWan, in a particular Segment.

        :param core_network_name: (experimental) corenetworkName.
        :param segment_name: 
        :param appliance_mode: 
        :param attachment_subnet_group: 

        :stability: experimental
        '''
        props = AttachToCloudWanProps(
            core_network_name=core_network_name,
            segment_name=segment_name,
            appliance_mode=appliance_mode,
            attachment_subnet_group=attachment_subnet_group,
        )

        return typing.cast(builtins.str, jsii.invoke(self, "attachToCloudWan", [props]))

    @jsii.member(jsii_name="attachToTransitGateway")
    def attach_to_transit_gateway(
        self,
        *,
        transit_gateway: aws_cdk.aws_ec2.CfnTransitGateway,
        applicance_mode: typing.Optional[ApplianceMode] = None,
        attachment_subnet_group: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''(experimental) Attach a vpc to a transit gateway, possibly in appliance mode Its intended purpose is provide a.

        :param transit_gateway: (experimental) the TransitGateway to connect to.
        :param applicance_mode: (experimental) Will this be connected in appliance mode ( used if you have Network Firewalls ).
        :param attachment_subnet_group: 

        :stability: experimental
        '''
        props = AttachToTransitGatewayProps(
            transit_gateway=transit_gateway,
            applicance_mode=applicance_mode,
            attachment_subnet_group=attachment_subnet_group,
        )

        return typing.cast(builtins.str, jsii.invoke(self, "attachToTransitGateway", [props]))

    @jsii.member(jsii_name="cloudWanRoutingProtocol")
    def cloud_wan_routing_protocol(
        self,
        *,
        subnet_groups: typing.Sequence[builtins.str],
        accept_route_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        deny_route_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Enable CloudWanRoutingProtocol.

        :param subnet_groups: 
        :param accept_route_filter: 
        :param deny_route_filter: 

        :stability: experimental
        '''
        props = CloudWanRoutingProtocolProps(
            subnet_groups=subnet_groups,
            accept_route_filter=accept_route_filter,
            deny_route_filter=deny_route_filter,
        )

        return typing.cast(None, jsii.invoke(self, "cloudWanRoutingProtocol", [props]))

    @jsii.member(jsii_name="createFlowLog")
    def create_flow_log(
        self,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        local_athena_querys: typing.Optional[builtins.bool] = None,
        one_minute_flow_logs: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Create Enterprise VPC Flow Logs (to central log account) and advanced diagnostics with Athena Querys.

        :param bucket: (experimental) the central s3 location for enterprise flow logs.
        :param local_athena_querys: (experimental) create in Account Athena Querys for flow logs.
        :param one_minute_flow_logs: (experimental) 1 minute resolution.

        :stability: experimental
        '''
        props = FlowLogProps(
            bucket=bucket,
            local_athena_querys=local_athena_querys,
            one_minute_flow_logs=one_minute_flow_logs,
        )

        return typing.cast(None, jsii.invoke(self, "createFlowLog", [props]))

    @jsii.member(jsii_name="shareSubnetGroup")
    def share_subnet_group(
        self,
        *,
        account: builtins.str,
        subnet_groups: typing.Sequence[builtins.str],
    ) -> None:
        '''(experimental) Share a subnetGroup with another AWS Account.

        :param account: 
        :param subnet_groups: 

        :stability: experimental
        '''
        props = ShareSubnetGroupProps(account=account, subnet_groups=subnet_groups)

        return typing.cast(None, jsii.invoke(self, "shareSubnetGroup", [props]))

    @builtins.property
    @jsii.member(jsii_name="addRoutesProvider")
    def add_routes_provider(self) -> aws_cdk.custom_resources.Provider:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.custom_resources.Provider, jsii.get(self, "addRoutesProvider"))

    @builtins.property
    @jsii.member(jsii_name="attachToCloudwanProvider")
    def attach_to_cloudwan_provider(self) -> aws_cdk.custom_resources.Provider:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.custom_resources.Provider, jsii.get(self, "attachToCloudwanProvider"))

    @builtins.property
    @jsii.member(jsii_name="tgWaiterProvider")
    def tg_waiter_provider(self) -> aws_cdk.custom_resources.Provider:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.custom_resources.Provider, jsii.get(self, "tgWaiterProvider"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.Vpc:
        '''(experimental) the ec2.Vpc that is passed in as property.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_ec2.Vpc, jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="cloudWanCoreId")
    def cloud_wan_core_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudWanCoreId"))

    @cloud_wan_core_id.setter
    def cloud_wan_core_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(EnterpriseVpc, "cloud_wan_core_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudWanCoreId", value)

    @builtins.property
    @jsii.member(jsii_name="cloudWanName")
    def cloud_wan_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) the Name of the cloudwan that the VPC is attached to.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudWanName"))

    @cloud_wan_name.setter
    def cloud_wan_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(EnterpriseVpc, "cloud_wan_name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudWanName", value)

    @builtins.property
    @jsii.member(jsii_name="cloudWanSegment")
    def cloud_wan_segment(self) -> typing.Optional[builtins.str]:
        '''(experimental) the Name of the Cloudwan segment that the vpc is attached to.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudWanSegment"))

    @cloud_wan_segment.setter
    def cloud_wan_segment(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(EnterpriseVpc, "cloud_wan_segment").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudWanSegment", value)

    @builtins.property
    @jsii.member(jsii_name="cloudWanVpcAttachmentId")
    def cloud_wan_vpc_attachment_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) AttachmentId when the vpc is attached to a Cloudwan.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudWanVpcAttachmentId"))

    @cloud_wan_vpc_attachment_id.setter
    def cloud_wan_vpc_attachment_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(EnterpriseVpc, "cloud_wan_vpc_attachment_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudWanVpcAttachmentId", value)

    @builtins.property
    @jsii.member(jsii_name="transitGWAttachmentID")
    def transit_gw_attachment_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) AttachmentId when the vpc is attached to a transitGateway.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transitGWAttachmentID"))

    @transit_gw_attachment_id.setter
    def transit_gw_attachment_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(EnterpriseVpc, "transit_gw_attachment_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitGWAttachmentID", value)

    @builtins.property
    @jsii.member(jsii_name="transitGWID")
    def transit_gwid(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Id of the transitgateway that the VPC is attached to.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transitGWID"))

    @transit_gwid.setter
    def transit_gwid(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(EnterpriseVpc, "transit_gwid").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitGWID", value)

    @builtins.property
    @jsii.member(jsii_name="vpcAttachmentCR")
    def vpc_attachment_cr(self) -> typing.Optional[aws_cdk.CustomResource]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[aws_cdk.CustomResource], jsii.get(self, "vpcAttachmentCR"))

    @vpc_attachment_cr.setter
    def vpc_attachment_cr(self, value: typing.Optional[aws_cdk.CustomResource]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(EnterpriseVpc, "vpc_attachment_cr").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcAttachmentCR", value)

    @builtins.property
    @jsii.member(jsii_name="vpcAttachmentId")
    def vpc_attachment_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcAttachmentId"))

    @vpc_attachment_id.setter
    def vpc_attachment_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(EnterpriseVpc, "vpc_attachment_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcAttachmentId", value)

    @builtins.property
    @jsii.member(jsii_name="vpcAttachmentSegmentName")
    def vpc_attachment_segment_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcAttachmentSegmentName"))

    @vpc_attachment_segment_name.setter
    def vpc_attachment_segment_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(EnterpriseVpc, "vpc_attachment_segment_name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcAttachmentSegmentName", value)


@jsii.data_type(
    jsii_type="raindancers-network.EnterpriseVpcProps",
    jsii_struct_bases=[],
    name_mapping={"vpc": "vpc"},
)
class EnterpriseVpcProps:
    def __init__(self, *, vpc: aws_cdk.aws_ec2.Vpc) -> None:
        '''(experimental) Propertys for an Enterprise VPC.

        :param vpc: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EnterpriseVpcProps.__init__)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.Vpc:
        '''
        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.Vpc, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnterpriseVpcProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Evpc(
    aws_cdk.aws_ec2.Vpc,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.Evpc",
):
    '''(experimental) Extends the ec2.Vpc construct to provide additional functionality - support for using AWS IPAM - methods for integration - Flow logs and Athena Querys - Create and share 53 zones.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        attach_to_core_network_segment: typing.Optional[builtins.str] = None,
        central_resolving_vpc: typing.Optional[builtins.bool] = None,
        disable_flowlog: typing.Optional[builtins.bool] = None,
        internet_gateway: typing.Optional[builtins.bool] = None,
        ipam_pool_id: typing.Optional[builtins.str] = None,
        netmask_length: typing.Optional[jsii.Number] = None,
        one_minute_flow_logs: typing.Optional[builtins.bool] = None,
        r53_internal_zone_name: typing.Optional[builtins.str] = None,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[builtins.str] = None,
        default_instance_tenancy: typing.Optional[aws_cdk.aws_ec2.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[aws_cdk.aws_ec2.FlowLogOptions, typing.Dict[str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[aws_cdk.aws_ec2.GatewayVpcEndpointOptions, typing.Dict[str, typing.Any]]]] = None,
        ip_addresses: typing.Optional[aws_cdk.aws_ec2.IIpAddresses] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        nat_gateway_provider: typing.Optional[aws_cdk.aws_ec2.NatProvider] = None,
        nat_gateways: typing.Optional[jsii.Number] = None,
        nat_gateway_subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
        reserved_azs: typing.Optional[jsii.Number] = None,
        subnet_configuration: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_ec2.SubnetConfiguration, typing.Dict[str, typing.Any]]]] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[aws_cdk.aws_ec2.VpnConnectionOptions, typing.Dict[str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param attach_to_core_network_segment: (experimental) the cloudwan core network segment name that this vpc will be attached to.
        :param central_resolving_vpc: (experimental) Set true if this is the central resolving Vpc.
        :param disable_flowlog: (experimental) Set true to disable centralised Flow Logs.
        :param internet_gateway: (experimental) An Internet Gateway will only be created if true.
        :param ipam_pool_id: (experimental) the ipam pool id that the Vpc's allocation will get created in.
        :param netmask_length: (experimental) a netmask value that is in the range 16 to 28.
        :param one_minute_flow_logs: (experimental) Set true for 1 minute aggregation on flow logs. (default is 10 minutes )
        :param r53_internal_zone_name: (experimental) Name of an internal Route53 Zone that is associated with this voc.
        :param availability_zones: Availability zones this VPC spans. Specify this option only if you do not specify ``maxAzs``. Default: - a subset of AZs of the stack
        :param cidr: (deprecated) The CIDR range to use for the VPC, e.g. '10.0.0.0/16'. Should be a minimum of /28 and maximum size of /16. The range will be split across all subnets per Availability Zone. Default: Vpc.DEFAULT_CIDR_RANGE
        :param default_instance_tenancy: The default tenancy of instances launched into the VPC. By setting this to dedicated tenancy, instances will be launched on hardware dedicated to a single AWS customer, unless specifically specified at instance launch time. Please note, not all instance types are usable with Dedicated tenancy. Default: DefaultInstanceTenancy.Default (shared) tenancy
        :param enable_dns_hostnames: Indicates whether the instances launched in the VPC get public DNS hostnames. If this attribute is true, instances in the VPC get public DNS hostnames, but only if the enableDnsSupport attribute is also set to true. Default: true
        :param enable_dns_support: Indicates whether the DNS resolution is supported for the VPC. If this attribute is false, the Amazon-provided DNS server in the VPC that resolves public DNS hostnames to IP addresses is not enabled. If this attribute is true, queries to the Amazon provided DNS server at the 169.254.169.253 IP address, or the reserved IP address at the base of the VPC IPv4 network range plus two will succeed. Default: true
        :param flow_logs: Flow logs to add to this VPC. Default: - No flow logs.
        :param gateway_endpoints: Gateway endpoints to add to this VPC. Default: - None.
        :param ip_addresses: The Provider to use to allocate IP Space to your VPC. Options include static allocation or from a pool. Default: ec2.IpAddresses.cidr
        :param max_azs: Define the maximum number of AZs to use in this region. If the region has more AZs than you want to use (for example, because of EIP limits), pick a lower number here. The AZs will be sorted and picked from the start of the list. If you pick a higher number than the number of AZs in the region, all AZs in the region will be selected. To use "all AZs" available to your account, use a high number (such as 99). Be aware that environment-agnostic stacks will be created with access to only 2 AZs, so to use more than 2 AZs, be sure to specify the account and region on your stack. Specify this option only if you do not specify ``availabilityZones``. Default: 3
        :param nat_gateway_provider: What type of NAT provider to use. Select between NAT gateways or NAT instances. NAT gateways may not be available in all AWS regions. Default: NatProvider.gateway()
        :param nat_gateways: The number of NAT Gateways/Instances to create. The type of NAT gateway or instance will be determined by the ``natGatewayProvider`` parameter. You can set this number lower than the number of Availability Zones in your VPC in order to save on NAT cost. Be aware you may be charged for cross-AZ data traffic instead. Default: - One NAT gateway/instance per Availability Zone
        :param nat_gateway_subnets: Configures the subnets which will have NAT Gateways/Instances. You can pick a specific group of subnets by specifying the group name; the picked subnets must be public subnets. Only necessary if you have more than one public subnet group. Default: - All public subnets.
        :param reserved_azs: Define the number of AZs to reserve. When specified, the IP space is reserved for the azs but no actual resources are provisioned. Default: 0
        :param subnet_configuration: Configure the subnets to build for each AZ. Each entry in this list configures a Subnet Group; each group will contain a subnet for each Availability Zone. For example, if you want 1 public subnet, 1 private subnet, and 1 isolated subnet in each AZ provide the following:: new ec2.Vpc(this, 'VPC', { subnetConfiguration: [ { cidrMask: 24, name: 'ingress', subnetType: ec2.SubnetType.PUBLIC, }, { cidrMask: 24, name: 'application', subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS, }, { cidrMask: 28, name: 'rds', subnetType: ec2.SubnetType.PRIVATE_ISOLATED, } ] }); Default: - The VPC CIDR will be evenly divided between 1 public and 1 private subnet per AZ.
        :param vpc_name: The VPC name. Since the VPC resource doesn't support providing a physical name, the value provided here will be recorded in the ``Name`` tag Default: this.node.path
        :param vpn_connections: VPN connections to this VPC. Default: - No connections.
        :param vpn_gateway: Indicates whether a VPN gateway should be created and attached to this VPC. Default: - true when vpnGatewayAsn or vpnConnections is specified
        :param vpn_gateway_asn: The private Autonomous System Number (ASN) for the VPN gateway. Default: - Amazon default ASN.
        :param vpn_route_propagation: Where to propagate VPN routes. Default: - On the route tables associated with private subnets. If no private subnets exists, isolated subnets are used. If no isolated subnets exists, public subnets are used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Evpc.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EvpcProps(
            attach_to_core_network_segment=attach_to_core_network_segment,
            central_resolving_vpc=central_resolving_vpc,
            disable_flowlog=disable_flowlog,
            internet_gateway=internet_gateway,
            ipam_pool_id=ipam_pool_id,
            netmask_length=netmask_length,
            one_minute_flow_logs=one_minute_flow_logs,
            r53_internal_zone_name=r53_internal_zone_name,
            availability_zones=availability_zones,
            cidr=cidr,
            default_instance_tenancy=default_instance_tenancy,
            enable_dns_hostnames=enable_dns_hostnames,
            enable_dns_support=enable_dns_support,
            flow_logs=flow_logs,
            gateway_endpoints=gateway_endpoints,
            ip_addresses=ip_addresses,
            max_azs=max_azs,
            nat_gateway_provider=nat_gateway_provider,
            nat_gateways=nat_gateways,
            nat_gateway_subnets=nat_gateway_subnets,
            reserved_azs=reserved_azs,
            subnet_configuration=subnet_configuration,
            vpc_name=vpc_name,
            vpn_connections=vpn_connections,
            vpn_gateway=vpn_gateway,
            vpn_gateway_asn=vpn_gateway_asn,
            vpn_route_propagation=vpn_route_propagation,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addRouteForPrivateSubnetstoCloudWan")
    def add_route_for_private_subnetsto_cloud_wan(
        self,
        destination_cidr: builtins.str,
        core_network_id: builtins.str,
    ) -> None:
        '''(experimental) Add a route to routing tables attached to the private subnets.

        :param destination_cidr: cidr eg, 0.0.0.0/0.
        :param core_network_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Evpc.add_route_for_private_subnetsto_cloud_wan)
            check_type(argname="argument destination_cidr", value=destination_cidr, expected_type=type_hints["destination_cidr"])
            check_type(argname="argument core_network_id", value=core_network_id, expected_type=type_hints["core_network_id"])
        return typing.cast(None, jsii.invoke(self, "addRouteForPrivateSubnetstoCloudWan", [destination_cidr, core_network_id]))

    @jsii.member(jsii_name="addRouteForPrivateSubnetstoinstance")
    def add_route_for_private_subnetstoinstance(
        self,
        destination_cidr: builtins.str,
        instance_id: builtins.str,
    ) -> None:
        '''(experimental) Add routes in private Subnets to a instance.

        Use this for routing to a network appliance.

        :param destination_cidr: -
        :param instance_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Evpc.add_route_for_private_subnetstoinstance)
            check_type(argname="argument destination_cidr", value=destination_cidr, expected_type=type_hints["destination_cidr"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
        return typing.cast(None, jsii.invoke(self, "addRouteForPrivateSubnetstoinstance", [destination_cidr, instance_id]))

    @jsii.member(jsii_name="addRouteForPrivateSubnetstoTransitGateway")
    def add_route_for_private_subnetsto_transit_gateway(
        self,
        destination_cidr: builtins.str,
        transit_gateway_id: builtins.str,
    ) -> None:
        '''(experimental) Add routes for Private Subnets to a Transit Gateway.

        :param destination_cidr: -
        :param transit_gateway_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Evpc.add_route_for_private_subnetsto_transit_gateway)
            check_type(argname="argument destination_cidr", value=destination_cidr, expected_type=type_hints["destination_cidr"])
            check_type(argname="argument transit_gateway_id", value=transit_gateway_id, expected_type=type_hints["transit_gateway_id"])
        return typing.cast(None, jsii.invoke(self, "addRouteForPrivateSubnetstoTransitGateway", [destination_cidr, transit_gateway_id]))

    @jsii.member(jsii_name="addRouteForPublicSubnetstoCloudWan")
    def add_route_for_public_subnetsto_cloud_wan(
        self,
        destination_cidr: builtins.str,
        core_network_id: builtins.str,
    ) -> None:
        '''(experimental) Add routes to routing tables associated with publicSubnets to Cloudwan.

        :param destination_cidr: -
        :param core_network_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Evpc.add_route_for_public_subnetsto_cloud_wan)
            check_type(argname="argument destination_cidr", value=destination_cidr, expected_type=type_hints["destination_cidr"])
            check_type(argname="argument core_network_id", value=core_network_id, expected_type=type_hints["core_network_id"])
        return typing.cast(None, jsii.invoke(self, "addRouteForPublicSubnetstoCloudWan", [destination_cidr, core_network_id]))

    @jsii.member(jsii_name="addRoutetoFirewall")
    def add_routeto_firewall(
        self,
        destination_cidr: builtins.str,
        subnetgroup: builtins.str,
        fw_arn: builtins.str,
    ) -> None:
        '''(experimental) Add routes to point at Network Firewalls, for specific subnetGroups.

        this will place routes on a per AZ basis

        :param destination_cidr: -
        :param subnetgroup: -
        :param fw_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Evpc.add_routeto_firewall)
            check_type(argname="argument destination_cidr", value=destination_cidr, expected_type=type_hints["destination_cidr"])
            check_type(argname="argument subnetgroup", value=subnetgroup, expected_type=type_hints["subnetgroup"])
            check_type(argname="argument fw_arn", value=fw_arn, expected_type=type_hints["fw_arn"])
        return typing.cast(None, jsii.invoke(self, "addRoutetoFirewall", [destination_cidr, subnetgroup, fw_arn]))

    @jsii.member(jsii_name="associateSharedRoute53ResolverRules")
    def associate_shared_route53_resolver_rules(
        self,
        owner: builtins.str,
        updatetopic: typing.Optional[aws_cdk.aws_sns.Topic] = None,
    ) -> None:
        '''(experimental) Associate any rules shared to this vpc.

        :param owner: -
        :param updatetopic: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Evpc.associate_shared_route53_resolver_rules)
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument updatetopic", value=updatetopic, expected_type=type_hints["updatetopic"])
        return typing.cast(None, jsii.invoke(self, "associateSharedRoute53ResolverRules", [owner, updatetopic]))

    @jsii.member(jsii_name="associateVPCZonewithCentralVPC")
    def associate_vpc_zonewith_central_vpc(self) -> None:
        '''(experimental) Associate the internal R53 Zone with the Central VPC, for Org wide resolution.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "associateVPCZonewithCentralVPC", []))

    @jsii.member(jsii_name="attachToCloudWan")
    def attach_to_cloud_wan(
        self,
        core_network_name: builtins.str,
        segment: builtins.str,
    ) -> builtins.str:
        '''(experimental) Attach the VPC to a cloud wan segment.

        :param core_network_name: -
        :param segment: -

        :return: transport attachment id

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Evpc.attach_to_cloud_wan)
            check_type(argname="argument core_network_name", value=core_network_name, expected_type=type_hints["core_network_name"])
            check_type(argname="argument segment", value=segment, expected_type=type_hints["segment"])
        return typing.cast(builtins.str, jsii.invoke(self, "attachToCloudWan", [core_network_name, segment]))

    @jsii.member(jsii_name="attachVpcToTGApplianceMode")
    def attach_vpc_to_tg_appliance_mode(
        self,
        transit_gateway: aws_cdk.aws_ec2.CfnTransitGateway,
        cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> builtins.str:
        '''(experimental) Attach a VPC to a Transit Gateway in Appliance mode.

        Primarly used when the VPC is being used as a centralised egress with firewalls
        A workaround to the problem of their not being support for Appliance mode connections to cloudwan

        :param transit_gateway: -
        :param cidrs: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Evpc.attach_vpc_to_tg_appliance_mode)
            check_type(argname="argument transit_gateway", value=transit_gateway, expected_type=type_hints["transit_gateway"])
            check_type(argname="argument cidrs", value=cidrs, expected_type=type_hints["cidrs"])
        return typing.cast(builtins.str, jsii.invoke(self, "attachVpcToTGApplianceMode", [transit_gateway, cidrs]))

    @jsii.member(jsii_name="createConnectAttachment")
    def create_connect_attachment(
        self,
        core_network_id: builtins.str,
        transport_attachment_id: builtins.str,
    ) -> builtins.str:
        '''(experimental) Create a connect Attachment to Cloudwan for Appliances.

        :param core_network_id: -
        :param transport_attachment_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Evpc.create_connect_attachment)
            check_type(argname="argument core_network_id", value=core_network_id, expected_type=type_hints["core_network_id"])
            check_type(argname="argument transport_attachment_id", value=transport_attachment_id, expected_type=type_hints["transport_attachment_id"])
        return typing.cast(builtins.str, jsii.invoke(self, "createConnectAttachment", [core_network_id, transport_attachment_id]))

    @builtins.property
    @jsii.member(jsii_name="lookUpProvider")
    def look_up_provider(self) -> aws_cdk.custom_resources.Provider:
        '''(experimental) Custom resource provider for looking up Cloudwan.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.custom_resources.Provider, jsii.get(self, "lookUpProvider"))

    @builtins.property
    @jsii.member(jsii_name="centralResolvingVpc")
    def central_resolving_vpc(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If this is a private zone.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "centralResolvingVpc"))

    @builtins.property
    @jsii.member(jsii_name="ipamAllocationId")
    def ipam_allocation_id(self) -> typing.Optional[aws_cdk.aws_ec2.CfnIPAMAllocation]:
        '''(experimental) the Ipam Allocation provider for this vpc.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.CfnIPAMAllocation], jsii.get(self, "ipamAllocationId"))

    @builtins.property
    @jsii.member(jsii_name="linknetSubnetIds")
    def linknet_subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) list of subnetIds that are used for connecting to the Cloudwan.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "linknetSubnetIds"))

    @builtins.property
    @jsii.member(jsii_name="privateR53Zone")
    def private_r53_zone(self) -> typing.Optional[aws_cdk.aws_route53.HostedZone]:
        '''(experimental) Private Zone.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_route53.HostedZone], jsii.get(self, "privateR53Zone"))

    @builtins.property
    @jsii.member(jsii_name="privateR53ZoneId")
    def private_r53_zone_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Private Zone Id.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateR53ZoneId"))


@jsii.data_type(
    jsii_type="raindancers-network.EvpcProps",
    jsii_struct_bases=[aws_cdk.aws_ec2.VpcProps],
    name_mapping={
        "availability_zones": "availabilityZones",
        "cidr": "cidr",
        "default_instance_tenancy": "defaultInstanceTenancy",
        "enable_dns_hostnames": "enableDnsHostnames",
        "enable_dns_support": "enableDnsSupport",
        "flow_logs": "flowLogs",
        "gateway_endpoints": "gatewayEndpoints",
        "ip_addresses": "ipAddresses",
        "max_azs": "maxAzs",
        "nat_gateway_provider": "natGatewayProvider",
        "nat_gateways": "natGateways",
        "nat_gateway_subnets": "natGatewaySubnets",
        "reserved_azs": "reservedAzs",
        "subnet_configuration": "subnetConfiguration",
        "vpc_name": "vpcName",
        "vpn_connections": "vpnConnections",
        "vpn_gateway": "vpnGateway",
        "vpn_gateway_asn": "vpnGatewayAsn",
        "vpn_route_propagation": "vpnRoutePropagation",
        "attach_to_core_network_segment": "attachToCoreNetworkSegment",
        "central_resolving_vpc": "centralResolvingVpc",
        "disable_flowlog": "disableFlowlog",
        "internet_gateway": "internetGateway",
        "ipam_pool_id": "ipamPoolId",
        "netmask_length": "netmaskLength",
        "one_minute_flow_logs": "oneMinuteFlowLogs",
        "r53_internal_zone_name": "r53InternalZoneName",
    },
)
class EvpcProps(aws_cdk.aws_ec2.VpcProps):
    def __init__(
        self,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[builtins.str] = None,
        default_instance_tenancy: typing.Optional[aws_cdk.aws_ec2.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[aws_cdk.aws_ec2.FlowLogOptions, typing.Dict[str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[aws_cdk.aws_ec2.GatewayVpcEndpointOptions, typing.Dict[str, typing.Any]]]] = None,
        ip_addresses: typing.Optional[aws_cdk.aws_ec2.IIpAddresses] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        nat_gateway_provider: typing.Optional[aws_cdk.aws_ec2.NatProvider] = None,
        nat_gateways: typing.Optional[jsii.Number] = None,
        nat_gateway_subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
        reserved_azs: typing.Optional[jsii.Number] = None,
        subnet_configuration: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_ec2.SubnetConfiguration, typing.Dict[str, typing.Any]]]] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[aws_cdk.aws_ec2.VpnConnectionOptions, typing.Dict[str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]]] = None,
        attach_to_core_network_segment: typing.Optional[builtins.str] = None,
        central_resolving_vpc: typing.Optional[builtins.bool] = None,
        disable_flowlog: typing.Optional[builtins.bool] = None,
        internet_gateway: typing.Optional[builtins.bool] = None,
        ipam_pool_id: typing.Optional[builtins.str] = None,
        netmask_length: typing.Optional[jsii.Number] = None,
        one_minute_flow_logs: typing.Optional[builtins.bool] = None,
        r53_internal_zone_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for Creating an enterprise Vpc which extend ec2.Vpc.

        :param availability_zones: Availability zones this VPC spans. Specify this option only if you do not specify ``maxAzs``. Default: - a subset of AZs of the stack
        :param cidr: (deprecated) The CIDR range to use for the VPC, e.g. '10.0.0.0/16'. Should be a minimum of /28 and maximum size of /16. The range will be split across all subnets per Availability Zone. Default: Vpc.DEFAULT_CIDR_RANGE
        :param default_instance_tenancy: The default tenancy of instances launched into the VPC. By setting this to dedicated tenancy, instances will be launched on hardware dedicated to a single AWS customer, unless specifically specified at instance launch time. Please note, not all instance types are usable with Dedicated tenancy. Default: DefaultInstanceTenancy.Default (shared) tenancy
        :param enable_dns_hostnames: Indicates whether the instances launched in the VPC get public DNS hostnames. If this attribute is true, instances in the VPC get public DNS hostnames, but only if the enableDnsSupport attribute is also set to true. Default: true
        :param enable_dns_support: Indicates whether the DNS resolution is supported for the VPC. If this attribute is false, the Amazon-provided DNS server in the VPC that resolves public DNS hostnames to IP addresses is not enabled. If this attribute is true, queries to the Amazon provided DNS server at the 169.254.169.253 IP address, or the reserved IP address at the base of the VPC IPv4 network range plus two will succeed. Default: true
        :param flow_logs: Flow logs to add to this VPC. Default: - No flow logs.
        :param gateway_endpoints: Gateway endpoints to add to this VPC. Default: - None.
        :param ip_addresses: The Provider to use to allocate IP Space to your VPC. Options include static allocation or from a pool. Default: ec2.IpAddresses.cidr
        :param max_azs: Define the maximum number of AZs to use in this region. If the region has more AZs than you want to use (for example, because of EIP limits), pick a lower number here. The AZs will be sorted and picked from the start of the list. If you pick a higher number than the number of AZs in the region, all AZs in the region will be selected. To use "all AZs" available to your account, use a high number (such as 99). Be aware that environment-agnostic stacks will be created with access to only 2 AZs, so to use more than 2 AZs, be sure to specify the account and region on your stack. Specify this option only if you do not specify ``availabilityZones``. Default: 3
        :param nat_gateway_provider: What type of NAT provider to use. Select between NAT gateways or NAT instances. NAT gateways may not be available in all AWS regions. Default: NatProvider.gateway()
        :param nat_gateways: The number of NAT Gateways/Instances to create. The type of NAT gateway or instance will be determined by the ``natGatewayProvider`` parameter. You can set this number lower than the number of Availability Zones in your VPC in order to save on NAT cost. Be aware you may be charged for cross-AZ data traffic instead. Default: - One NAT gateway/instance per Availability Zone
        :param nat_gateway_subnets: Configures the subnets which will have NAT Gateways/Instances. You can pick a specific group of subnets by specifying the group name; the picked subnets must be public subnets. Only necessary if you have more than one public subnet group. Default: - All public subnets.
        :param reserved_azs: Define the number of AZs to reserve. When specified, the IP space is reserved for the azs but no actual resources are provisioned. Default: 0
        :param subnet_configuration: Configure the subnets to build for each AZ. Each entry in this list configures a Subnet Group; each group will contain a subnet for each Availability Zone. For example, if you want 1 public subnet, 1 private subnet, and 1 isolated subnet in each AZ provide the following:: new ec2.Vpc(this, 'VPC', { subnetConfiguration: [ { cidrMask: 24, name: 'ingress', subnetType: ec2.SubnetType.PUBLIC, }, { cidrMask: 24, name: 'application', subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS, }, { cidrMask: 28, name: 'rds', subnetType: ec2.SubnetType.PRIVATE_ISOLATED, } ] }); Default: - The VPC CIDR will be evenly divided between 1 public and 1 private subnet per AZ.
        :param vpc_name: The VPC name. Since the VPC resource doesn't support providing a physical name, the value provided here will be recorded in the ``Name`` tag Default: this.node.path
        :param vpn_connections: VPN connections to this VPC. Default: - No connections.
        :param vpn_gateway: Indicates whether a VPN gateway should be created and attached to this VPC. Default: - true when vpnGatewayAsn or vpnConnections is specified
        :param vpn_gateway_asn: The private Autonomous System Number (ASN) for the VPN gateway. Default: - Amazon default ASN.
        :param vpn_route_propagation: Where to propagate VPN routes. Default: - On the route tables associated with private subnets. If no private subnets exists, isolated subnets are used. If no isolated subnets exists, public subnets are used.
        :param attach_to_core_network_segment: (experimental) the cloudwan core network segment name that this vpc will be attached to.
        :param central_resolving_vpc: (experimental) Set true if this is the central resolving Vpc.
        :param disable_flowlog: (experimental) Set true to disable centralised Flow Logs.
        :param internet_gateway: (experimental) An Internet Gateway will only be created if true.
        :param ipam_pool_id: (experimental) the ipam pool id that the Vpc's allocation will get created in.
        :param netmask_length: (experimental) a netmask value that is in the range 16 to 28.
        :param one_minute_flow_logs: (experimental) Set true for 1 minute aggregation on flow logs. (default is 10 minutes )
        :param r53_internal_zone_name: (experimental) Name of an internal Route53 Zone that is associated with this voc.

        :stability: experimental
        '''
        if isinstance(nat_gateway_subnets, dict):
            nat_gateway_subnets = aws_cdk.aws_ec2.SubnetSelection(**nat_gateway_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(EvpcProps.__init__)
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument default_instance_tenancy", value=default_instance_tenancy, expected_type=type_hints["default_instance_tenancy"])
            check_type(argname="argument enable_dns_hostnames", value=enable_dns_hostnames, expected_type=type_hints["enable_dns_hostnames"])
            check_type(argname="argument enable_dns_support", value=enable_dns_support, expected_type=type_hints["enable_dns_support"])
            check_type(argname="argument flow_logs", value=flow_logs, expected_type=type_hints["flow_logs"])
            check_type(argname="argument gateway_endpoints", value=gateway_endpoints, expected_type=type_hints["gateway_endpoints"])
            check_type(argname="argument ip_addresses", value=ip_addresses, expected_type=type_hints["ip_addresses"])
            check_type(argname="argument max_azs", value=max_azs, expected_type=type_hints["max_azs"])
            check_type(argname="argument nat_gateway_provider", value=nat_gateway_provider, expected_type=type_hints["nat_gateway_provider"])
            check_type(argname="argument nat_gateways", value=nat_gateways, expected_type=type_hints["nat_gateways"])
            check_type(argname="argument nat_gateway_subnets", value=nat_gateway_subnets, expected_type=type_hints["nat_gateway_subnets"])
            check_type(argname="argument reserved_azs", value=reserved_azs, expected_type=type_hints["reserved_azs"])
            check_type(argname="argument subnet_configuration", value=subnet_configuration, expected_type=type_hints["subnet_configuration"])
            check_type(argname="argument vpc_name", value=vpc_name, expected_type=type_hints["vpc_name"])
            check_type(argname="argument vpn_connections", value=vpn_connections, expected_type=type_hints["vpn_connections"])
            check_type(argname="argument vpn_gateway", value=vpn_gateway, expected_type=type_hints["vpn_gateway"])
            check_type(argname="argument vpn_gateway_asn", value=vpn_gateway_asn, expected_type=type_hints["vpn_gateway_asn"])
            check_type(argname="argument vpn_route_propagation", value=vpn_route_propagation, expected_type=type_hints["vpn_route_propagation"])
            check_type(argname="argument attach_to_core_network_segment", value=attach_to_core_network_segment, expected_type=type_hints["attach_to_core_network_segment"])
            check_type(argname="argument central_resolving_vpc", value=central_resolving_vpc, expected_type=type_hints["central_resolving_vpc"])
            check_type(argname="argument disable_flowlog", value=disable_flowlog, expected_type=type_hints["disable_flowlog"])
            check_type(argname="argument internet_gateway", value=internet_gateway, expected_type=type_hints["internet_gateway"])
            check_type(argname="argument ipam_pool_id", value=ipam_pool_id, expected_type=type_hints["ipam_pool_id"])
            check_type(argname="argument netmask_length", value=netmask_length, expected_type=type_hints["netmask_length"])
            check_type(argname="argument one_minute_flow_logs", value=one_minute_flow_logs, expected_type=type_hints["one_minute_flow_logs"])
            check_type(argname="argument r53_internal_zone_name", value=r53_internal_zone_name, expected_type=type_hints["r53_internal_zone_name"])
        self._values: typing.Dict[str, typing.Any] = {}
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if cidr is not None:
            self._values["cidr"] = cidr
        if default_instance_tenancy is not None:
            self._values["default_instance_tenancy"] = default_instance_tenancy
        if enable_dns_hostnames is not None:
            self._values["enable_dns_hostnames"] = enable_dns_hostnames
        if enable_dns_support is not None:
            self._values["enable_dns_support"] = enable_dns_support
        if flow_logs is not None:
            self._values["flow_logs"] = flow_logs
        if gateway_endpoints is not None:
            self._values["gateway_endpoints"] = gateway_endpoints
        if ip_addresses is not None:
            self._values["ip_addresses"] = ip_addresses
        if max_azs is not None:
            self._values["max_azs"] = max_azs
        if nat_gateway_provider is not None:
            self._values["nat_gateway_provider"] = nat_gateway_provider
        if nat_gateways is not None:
            self._values["nat_gateways"] = nat_gateways
        if nat_gateway_subnets is not None:
            self._values["nat_gateway_subnets"] = nat_gateway_subnets
        if reserved_azs is not None:
            self._values["reserved_azs"] = reserved_azs
        if subnet_configuration is not None:
            self._values["subnet_configuration"] = subnet_configuration
        if vpc_name is not None:
            self._values["vpc_name"] = vpc_name
        if vpn_connections is not None:
            self._values["vpn_connections"] = vpn_connections
        if vpn_gateway is not None:
            self._values["vpn_gateway"] = vpn_gateway
        if vpn_gateway_asn is not None:
            self._values["vpn_gateway_asn"] = vpn_gateway_asn
        if vpn_route_propagation is not None:
            self._values["vpn_route_propagation"] = vpn_route_propagation
        if attach_to_core_network_segment is not None:
            self._values["attach_to_core_network_segment"] = attach_to_core_network_segment
        if central_resolving_vpc is not None:
            self._values["central_resolving_vpc"] = central_resolving_vpc
        if disable_flowlog is not None:
            self._values["disable_flowlog"] = disable_flowlog
        if internet_gateway is not None:
            self._values["internet_gateway"] = internet_gateway
        if ipam_pool_id is not None:
            self._values["ipam_pool_id"] = ipam_pool_id
        if netmask_length is not None:
            self._values["netmask_length"] = netmask_length
        if one_minute_flow_logs is not None:
            self._values["one_minute_flow_logs"] = one_minute_flow_logs
        if r53_internal_zone_name is not None:
            self._values["r53_internal_zone_name"] = r53_internal_zone_name

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Availability zones this VPC spans.

        Specify this option only if you do not specify ``maxAzs``.

        :default: - a subset of AZs of the stack
        '''
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cidr(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The CIDR range to use for the VPC, e.g. '10.0.0.0/16'.

        Should be a minimum of /28 and maximum size of /16. The range will be
        split across all subnets per Availability Zone.

        :default: Vpc.DEFAULT_CIDR_RANGE

        :deprecated: Use ipAddresses instead

        :stability: deprecated
        '''
        result = self._values.get("cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_instance_tenancy(
        self,
    ) -> typing.Optional[aws_cdk.aws_ec2.DefaultInstanceTenancy]:
        '''The default tenancy of instances launched into the VPC.

        By setting this to dedicated tenancy, instances will be launched on
        hardware dedicated to a single AWS customer, unless specifically specified
        at instance launch time. Please note, not all instance types are usable
        with Dedicated tenancy.

        :default: DefaultInstanceTenancy.Default (shared) tenancy
        '''
        result = self._values.get("default_instance_tenancy")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.DefaultInstanceTenancy], result)

    @builtins.property
    def enable_dns_hostnames(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the instances launched in the VPC get public DNS hostnames.

        If this attribute is true, instances in the VPC get public DNS hostnames,
        but only if the enableDnsSupport attribute is also set to true.

        :default: true
        '''
        result = self._values.get("enable_dns_hostnames")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_dns_support(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the DNS resolution is supported for the VPC.

        If this attribute is false, the Amazon-provided DNS server in the VPC that
        resolves public DNS hostnames to IP addresses is not enabled. If this
        attribute is true, queries to the Amazon provided DNS server at the
        169.254.169.253 IP address, or the reserved IP address at the base of the
        VPC IPv4 network range plus two will succeed.

        :default: true
        '''
        result = self._values.get("enable_dns_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def flow_logs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_ec2.FlowLogOptions]]:
        '''Flow logs to add to this VPC.

        :default: - No flow logs.
        '''
        result = self._values.get("flow_logs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_ec2.FlowLogOptions]], result)

    @builtins.property
    def gateway_endpoints(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_ec2.GatewayVpcEndpointOptions]]:
        '''Gateway endpoints to add to this VPC.

        :default: - None.
        '''
        result = self._values.get("gateway_endpoints")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_ec2.GatewayVpcEndpointOptions]], result)

    @builtins.property
    def ip_addresses(self) -> typing.Optional[aws_cdk.aws_ec2.IIpAddresses]:
        '''The Provider to use to allocate IP Space to your VPC.

        Options include static allocation or from a pool.

        :default: ec2.IpAddresses.cidr
        '''
        result = self._values.get("ip_addresses")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.IIpAddresses], result)

    @builtins.property
    def max_azs(self) -> typing.Optional[jsii.Number]:
        '''Define the maximum number of AZs to use in this region.

        If the region has more AZs than you want to use (for example, because of
        EIP limits), pick a lower number here. The AZs will be sorted and picked
        from the start of the list.

        If you pick a higher number than the number of AZs in the region, all AZs
        in the region will be selected. To use "all AZs" available to your
        account, use a high number (such as 99).

        Be aware that environment-agnostic stacks will be created with access to
        only 2 AZs, so to use more than 2 AZs, be sure to specify the account and
        region on your stack.

        Specify this option only if you do not specify ``availabilityZones``.

        :default: 3
        '''
        result = self._values.get("max_azs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nat_gateway_provider(self) -> typing.Optional[aws_cdk.aws_ec2.NatProvider]:
        '''What type of NAT provider to use.

        Select between NAT gateways or NAT instances. NAT gateways
        may not be available in all AWS regions.

        :default: NatProvider.gateway()
        '''
        result = self._values.get("nat_gateway_provider")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.NatProvider], result)

    @builtins.property
    def nat_gateways(self) -> typing.Optional[jsii.Number]:
        '''The number of NAT Gateways/Instances to create.

        The type of NAT gateway or instance will be determined by the
        ``natGatewayProvider`` parameter.

        You can set this number lower than the number of Availability Zones in your
        VPC in order to save on NAT cost. Be aware you may be charged for
        cross-AZ data traffic instead.

        :default: - One NAT gateway/instance per Availability Zone
        '''
        result = self._values.get("nat_gateways")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nat_gateway_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        '''Configures the subnets which will have NAT Gateways/Instances.

        You can pick a specific group of subnets by specifying the group name;
        the picked subnets must be public subnets.

        Only necessary if you have more than one public subnet group.

        :default: - All public subnets.
        '''
        result = self._values.get("nat_gateway_subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    @builtins.property
    def reserved_azs(self) -> typing.Optional[jsii.Number]:
        '''Define the number of AZs to reserve.

        When specified, the IP space is reserved for the azs but no actual
        resources are provisioned.

        :default: 0
        '''
        result = self._values.get("reserved_azs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def subnet_configuration(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.SubnetConfiguration]]:
        '''Configure the subnets to build for each AZ.

        Each entry in this list configures a Subnet Group; each group will contain a
        subnet for each Availability Zone.

        For example, if you want 1 public subnet, 1 private subnet, and 1 isolated
        subnet in each AZ provide the following::

           new ec2.Vpc(this, 'VPC', {
              subnetConfiguration: [
                 {
                   cidrMask: 24,
                   name: 'ingress',
                   subnetType: ec2.SubnetType.PUBLIC,
                 },
                 {
                   cidrMask: 24,
                   name: 'application',
                   subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
                 },
                 {
                   cidrMask: 28,
                   name: 'rds',
                   subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
                 }
              ]
           });

        :default:

        - The VPC CIDR will be evenly divided between 1 public and 1
        private subnet per AZ.
        '''
        result = self._values.get("subnet_configuration")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_ec2.SubnetConfiguration]], result)

    @builtins.property
    def vpc_name(self) -> typing.Optional[builtins.str]:
        '''The VPC name.

        Since the VPC resource doesn't support providing a physical name, the value provided here will be recorded in the ``Name`` tag

        :default: this.node.path
        '''
        result = self._values.get("vpc_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpn_connections(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_ec2.VpnConnectionOptions]]:
        '''VPN connections to this VPC.

        :default: - No connections.
        '''
        result = self._values.get("vpn_connections")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_ec2.VpnConnectionOptions]], result)

    @builtins.property
    def vpn_gateway(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether a VPN gateway should be created and attached to this VPC.

        :default: - true when vpnGatewayAsn or vpnConnections is specified
        '''
        result = self._values.get("vpn_gateway")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpn_gateway_asn(self) -> typing.Optional[jsii.Number]:
        '''The private Autonomous System Number (ASN) for the VPN gateway.

        :default: - Amazon default ASN.
        '''
        result = self._values.get("vpn_gateway_asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpn_route_propagation(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.SubnetSelection]]:
        '''Where to propagate VPN routes.

        :default:

        - On the route tables associated with private subnets. If no
        private subnets exists, isolated subnets are used. If no isolated subnets
        exists, public subnets are used.
        '''
        result = self._values.get("vpn_route_propagation")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_ec2.SubnetSelection]], result)

    @builtins.property
    def attach_to_core_network_segment(self) -> typing.Optional[builtins.str]:
        '''(experimental) the cloudwan core network segment name that this vpc will be attached to.

        :stability: experimental
        '''
        result = self._values.get("attach_to_core_network_segment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def central_resolving_vpc(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set true if this is the central resolving Vpc.

        :stability: experimental
        '''
        result = self._values.get("central_resolving_vpc")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def disable_flowlog(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set true to disable centralised Flow Logs.

        :stability: experimental
        '''
        result = self._values.get("disable_flowlog")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def internet_gateway(self) -> typing.Optional[builtins.bool]:
        '''(experimental) An Internet Gateway will only be created if true.

        :stability: experimental
        '''
        result = self._values.get("internet_gateway")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ipam_pool_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) the ipam pool id that the Vpc's allocation will get created in.

        :stability: experimental
        '''
        result = self._values.get("ipam_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def netmask_length(self) -> typing.Optional[jsii.Number]:
        '''(experimental) a netmask value that is in the range 16 to 28.

        :stability: experimental
        '''
        result = self._values.get("netmask_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def one_minute_flow_logs(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set true for 1 minute aggregation on flow logs.

        (default is 10 minutes )

        :stability: experimental
        '''
        result = self._values.get("one_minute_flow_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def r53_internal_zone_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of an internal Route53 Zone that is associated with this voc.

        :stability: experimental
        '''
        result = self._values.get("r53_internal_zone_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EvpcProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.FlowLogProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "local_athena_querys": "localAthenaQuerys",
        "one_minute_flow_logs": "oneMinuteFlowLogs",
    },
)
class FlowLogProps:
    def __init__(
        self,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        local_athena_querys: typing.Optional[builtins.bool] = None,
        one_minute_flow_logs: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties for flow logs *.

        :param bucket: (experimental) the central s3 location for enterprise flow logs.
        :param local_athena_querys: (experimental) create in Account Athena Querys for flow logs.
        :param one_minute_flow_logs: (experimental) 1 minute resolution.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FlowLogProps.__init__)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument local_athena_querys", value=local_athena_querys, expected_type=type_hints["local_athena_querys"])
            check_type(argname="argument one_minute_flow_logs", value=one_minute_flow_logs, expected_type=type_hints["one_minute_flow_logs"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
        }
        if local_athena_querys is not None:
            self._values["local_athena_querys"] = local_athena_querys
        if one_minute_flow_logs is not None:
            self._values["one_minute_flow_logs"] = one_minute_flow_logs

    @builtins.property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        '''(experimental) the central s3 location for enterprise flow logs.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.IBucket, result)

    @builtins.property
    def local_athena_querys(self) -> typing.Optional[builtins.bool]:
        '''(experimental) create in Account Athena Querys for flow logs.

        :stability: experimental
        '''
        result = self._values.get("local_athena_querys")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def one_minute_flow_logs(self) -> typing.Optional[builtins.bool]:
        '''(experimental) 1 minute resolution.

        :stability: experimental
        '''
        result = self._values.get("one_minute_flow_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FlowLogProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GetTunnelAddressPair(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.GetTunnelAddressPair",
):
    '''(experimental) Allocate a pair of /30 networks CIDRS for use in Ipsec VPN Tunnels.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        ipam_pool_id: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param scope: scope in which this resource is created.
        :param id: scope id of the resoruce.
        :param ipam_pool_id: (experimental) The IPAM Pool Id from which the assginment will be made from.
        :param name: (experimental) The Name used by IPAM to record the allocation.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(GetTunnelAddressPair.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GetTunnelAddressPairProps(ipam_pool_id=ipam_pool_id, name=name)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="assignedCidrPair")
    def assigned_cidr_pair(self) -> typing.List[builtins.str]:
        '''(experimental) returns 2 cidr blocks as an array to be used by an IPsec Tunnel.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "assignedCidrPair"))


@jsii.data_type(
    jsii_type="raindancers-network.GetTunnelAddressPairProps",
    jsii_struct_bases=[],
    name_mapping={"ipam_pool_id": "ipamPoolId", "name": "name"},
)
class GetTunnelAddressPairProps:
    def __init__(self, *, ipam_pool_id: builtins.str, name: builtins.str) -> None:
        '''(experimental) Properties for obtaining an IPAM assigned address pair for use on IPsec VPN Tunnels.

        :param ipam_pool_id: (experimental) The IPAM Pool Id from which the assginment will be made from.
        :param name: (experimental) The Name used by IPAM to record the allocation.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(GetTunnelAddressPairProps.__init__)
            check_type(argname="argument ipam_pool_id", value=ipam_pool_id, expected_type=type_hints["ipam_pool_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[str, typing.Any] = {
            "ipam_pool_id": ipam_pool_id,
            "name": name,
        }

    @builtins.property
    def ipam_pool_id(self) -> builtins.str:
        '''(experimental) The IPAM Pool Id from which the assginment will be made from.

        :stability: experimental
        '''
        result = self._values.get("ipam_pool_id")
        assert result is not None, "Required property 'ipam_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The Name used by IPAM to record the allocation.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GetTunnelAddressPairProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="raindancers-network.ICoreNetworkSegmentProps")
class ICoreNetworkSegmentProps(typing_extensions.Protocol):
    '''(experimental) Properties creating a Corenetwork Segment.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="policyTableServiceToken")
    def policy_table_service_token(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="segmentName")
    def segment_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="updateDependsOn")
    def update_depends_on(self) -> typing.List[aws_cdk.CustomResource]:
        '''
        :stability: experimental
        '''
        ...

    @update_depends_on.setter
    def update_depends_on(self, value: typing.List[aws_cdk.CustomResource]) -> None:
        ...


class _ICoreNetworkSegmentPropsProxy:
    '''(experimental) Properties creating a Corenetwork Segment.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "raindancers-network.ICoreNetworkSegmentProps"

    @builtins.property
    @jsii.member(jsii_name="policyTableServiceToken")
    def policy_table_service_token(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyTableServiceToken"))

    @builtins.property
    @jsii.member(jsii_name="segmentName")
    def segment_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "segmentName"))

    @builtins.property
    @jsii.member(jsii_name="updateDependsOn")
    def update_depends_on(self) -> typing.List[aws_cdk.CustomResource]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[aws_cdk.CustomResource], jsii.get(self, "updateDependsOn"))

    @update_depends_on.setter
    def update_depends_on(self, value: typing.List[aws_cdk.CustomResource]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(ICoreNetworkSegmentProps, "update_depends_on").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateDependsOn", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICoreNetworkSegmentProps).__jsii_proxy_class__ = lambda : _ICoreNetworkSegmentPropsProxy


@jsii.enum(jsii_type="raindancers-network.IkeVersion")
class IkeVersion(enum.Enum):
    '''(experimental) Ike Version for S2S VPN.

    :stability: experimental
    '''

    IKEV1 = "IKEV1"
    '''(experimental) Use IKEv1.

    :stability: experimental
    '''
    IKEV2 = "IKEV2"
    '''(experimental) Use IKEv2.

    :stability: experimental
    '''


class IpsecTunnelPool(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.IpsecTunnelPool",
):
    '''(experimental) Creates an IPAM pool to assign address's for IPsec VPNS.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cidr: builtins.str,
        description: builtins.str,
        ipam_scope_id: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param scope: scope in which this resource is defined.
        :param id: id of the resource.
        :param cidr: (experimental) The Cidr range for pools to be created from eg, 169.254.100.0/27 The cidr must be in the 169.254.0.0/16 range and must be a minimum of a /29 and a maximum of /24. It must also not overlap the AWS reserved ranges. T
        :param description: (experimental) the description used by IPAM to describe the pool.
        :param ipam_scope_id: (experimental) The IPAM Scope Id to use to create the Pool.
        :param name: (experimental) the name used by IPAM to identify the pool.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IpsecTunnelPool.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IpsecTunnelPoolProps(
            cidr=cidr, description=description, ipam_scope_id=ipam_scope_id, name=name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="ipampool")
    def ipampool(self) -> aws_cdk.aws_ec2.CfnIPAMPool:
        '''(experimental) returns the created ipam Pool.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_ec2.CfnIPAMPool, jsii.get(self, "ipampool"))


@jsii.data_type(
    jsii_type="raindancers-network.IpsecTunnelPoolProps",
    jsii_struct_bases=[],
    name_mapping={
        "cidr": "cidr",
        "description": "description",
        "ipam_scope_id": "ipamScopeId",
        "name": "name",
    },
)
class IpsecTunnelPoolProps:
    def __init__(
        self,
        *,
        cidr: builtins.str,
        description: builtins.str,
        ipam_scope_id: builtins.str,
        name: builtins.str,
    ) -> None:
        '''(experimental) Properties for defining a IPAM Pool specifically for IPSec VPN Tunnels.

        :param cidr: (experimental) The Cidr range for pools to be created from eg, 169.254.100.0/27 The cidr must be in the 169.254.0.0/16 range and must be a minimum of a /29 and a maximum of /24. It must also not overlap the AWS reserved ranges. T
        :param description: (experimental) the description used by IPAM to describe the pool.
        :param ipam_scope_id: (experimental) The IPAM Scope Id to use to create the Pool.
        :param name: (experimental) the name used by IPAM to identify the pool.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IpsecTunnelPoolProps.__init__)
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument ipam_scope_id", value=ipam_scope_id, expected_type=type_hints["ipam_scope_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[str, typing.Any] = {
            "cidr": cidr,
            "description": description,
            "ipam_scope_id": ipam_scope_id,
            "name": name,
        }

    @builtins.property
    def cidr(self) -> builtins.str:
        '''(experimental) The Cidr range for pools to be created from    eg, 169.254.100.0/27 The cidr must be in the 169.254.0.0/16 range and must be a minimum of a /29 and a maximum of /24.

        It must also not overlap the AWS reserved ranges. T

        :stability: experimental
        '''
        result = self._values.get("cidr")
        assert result is not None, "Required property 'cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> builtins.str:
        '''(experimental) the description used by IPAM to describe the pool.

        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ipam_scope_id(self) -> builtins.str:
        '''(experimental) The IPAM Scope Id to use to create the Pool.

        :stability: experimental
        '''
        result = self._values.get("ipam_scope_id")
        assert result is not None, "Required property 'ipam_scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) the name used by IPAM to identify the pool.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IpsecTunnelPoolProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkFirewall(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.NetworkFirewall",
):
    '''(experimental) Creates Network Firewalls.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        firewall_name: builtins.str,
        firewall_policy: aws_cdk.aws_networkfirewall.CfnFirewallPolicy,
        subnet_group: builtins.str,
        vpc: aws_cdk.aws_ec2.Vpc,
    ) -> None:
        '''
        :param scope: Scope.
        :param id: id.
        :param firewall_name: (experimental) the name that will be given to the firewall.
        :param firewall_policy: (experimental) the firewalls policy.
        :param subnet_group: (experimental) the subnetGroup where the firewall will be created.
        :param vpc: (experimental) the the vpc where the Network firewall is placed.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NetworkFirewall.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NetworkFirewallProps(
            firewall_name=firewall_name,
            firewall_policy=firewall_policy,
            subnet_group=subnet_group,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="endPointIds")
    def end_point_ids(self) -> typing.List[builtins.str]:
        '''(experimental) Gateway Endpoints for the Firewalls.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "endPointIds"))

    @builtins.property
    @jsii.member(jsii_name="firewallArn")
    def firewall_arn(self) -> builtins.str:
        '''(experimental) Arn of the firewall.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallArn"))

    @builtins.property
    @jsii.member(jsii_name="firewallId")
    def firewall_id(self) -> builtins.str:
        '''(experimental) Firewall ID.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallId"))


@jsii.data_type(
    jsii_type="raindancers-network.NetworkFirewallProps",
    jsii_struct_bases=[],
    name_mapping={
        "firewall_name": "firewallName",
        "firewall_policy": "firewallPolicy",
        "subnet_group": "subnetGroup",
        "vpc": "vpc",
    },
)
class NetworkFirewallProps:
    def __init__(
        self,
        *,
        firewall_name: builtins.str,
        firewall_policy: aws_cdk.aws_networkfirewall.CfnFirewallPolicy,
        subnet_group: builtins.str,
        vpc: aws_cdk.aws_ec2.Vpc,
    ) -> None:
        '''(experimental) Propertys of a Network Firewall.

        :param firewall_name: (experimental) the name that will be given to the firewall.
        :param firewall_policy: (experimental) the firewalls policy.
        :param subnet_group: (experimental) the subnetGroup where the firewall will be created.
        :param vpc: (experimental) the the vpc where the Network firewall is placed.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NetworkFirewallProps.__init__)
            check_type(argname="argument firewall_name", value=firewall_name, expected_type=type_hints["firewall_name"])
            check_type(argname="argument firewall_policy", value=firewall_policy, expected_type=type_hints["firewall_policy"])
            check_type(argname="argument subnet_group", value=subnet_group, expected_type=type_hints["subnet_group"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[str, typing.Any] = {
            "firewall_name": firewall_name,
            "firewall_policy": firewall_policy,
            "subnet_group": subnet_group,
            "vpc": vpc,
        }

    @builtins.property
    def firewall_name(self) -> builtins.str:
        '''(experimental) the name that will be given to the firewall.

        :stability: experimental
        '''
        result = self._values.get("firewall_name")
        assert result is not None, "Required property 'firewall_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def firewall_policy(self) -> aws_cdk.aws_networkfirewall.CfnFirewallPolicy:
        '''(experimental) the firewalls policy.

        :stability: experimental
        '''
        result = self._values.get("firewall_policy")
        assert result is not None, "Required property 'firewall_policy' is missing"
        return typing.cast(aws_cdk.aws_networkfirewall.CfnFirewallPolicy, result)

    @builtins.property
    def subnet_group(self) -> builtins.str:
        '''(experimental) the subnetGroup where the firewall will be created.

        :stability: experimental
        '''
        result = self._values.get("subnet_group")
        assert result is not None, "Required property 'subnet_group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.Vpc:
        '''(experimental) the the vpc where the Network firewall is placed.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.Vpc, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkFirewallProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.Operators")
class Operators(enum.Enum):
    '''(experimental) Operatior COnditons for Attachments.

    :stability: experimental
    '''

    EQUALS = "EQUALS"
    '''
    :stability: experimental
    '''
    NOTEQUALS = "NOTEQUALS"
    '''
    :stability: experimental
    '''
    CONTAINS = "CONTAINS"
    '''
    :stability: experimental
    '''
    BEGINS_WITH = "BEGINS_WITH"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="raindancers-network.OutboundForwardingRule",
    jsii_struct_bases=[],
    name_mapping={"domain": "domain", "forward_to": "forwardTo"},
)
class OutboundForwardingRule:
    def __init__(
        self,
        *,
        domain: builtins.str,
        forward_to: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param domain: (experimental) domain to forward.
        :param forward_to: (experimental) array of ip address's to forward request to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(OutboundForwardingRule.__init__)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument forward_to", value=forward_to, expected_type=type_hints["forward_to"])
        self._values: typing.Dict[str, typing.Any] = {
            "domain": domain,
            "forward_to": forward_to,
        }

    @builtins.property
    def domain(self) -> builtins.str:
        '''(experimental) domain to forward.

        :stability: experimental
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def forward_to(self) -> typing.List[builtins.str]:
        '''(experimental) array of ip address's to forward request to.

        :stability: experimental
        '''
        result = self._values.get("forward_to")
        assert result is not None, "Required property 'forward_to' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OutboundForwardingRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.OutsideIpAddressType")
class OutsideIpAddressType(enum.Enum):
    '''(experimental) Specify the use of public or private IP address's for Site to Site VPN.

    :stability: experimental
    '''

    PRIVATE = "PRIVATE"
    '''(experimental) Use Private IPv4 Address from the Transit Gateways IP address Pool.

    :stability: experimental
    '''
    PUBLIC = "PUBLIC"
    '''(experimental) Use Public IPv4 Address Assigned by AWS.

    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.Phase1DHGroupNumbers")
class Phase1DHGroupNumbers(enum.Enum):
    '''
    :stability: experimental
    '''

    DH2 = "DH2"
    '''
    :stability: experimental
    '''
    DH14 = "DH14"
    '''
    :stability: experimental
    '''
    DH15 = "DH15"
    '''
    :stability: experimental
    '''
    DH16 = "DH16"
    '''
    :stability: experimental
    '''
    DH17 = "DH17"
    '''
    :stability: experimental
    '''
    DH18 = "DH18"
    '''
    :stability: experimental
    '''
    DH19 = "DH19"
    '''
    :stability: experimental
    '''
    DH20 = "DH20"
    '''
    :stability: experimental
    '''
    DH21 = "DH21"
    '''
    :stability: experimental
    '''
    DH22 = "DH22"
    '''
    :stability: experimental
    '''
    DH23 = "DH23"
    '''
    :stability: experimental
    '''
    DH24 = "DH24"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.Phase1EncryptionAlgorithms")
class Phase1EncryptionAlgorithms(enum.Enum):
    '''
    :stability: experimental
    '''

    AES128 = "AES128"
    '''
    :stability: experimental
    '''
    AES256 = "AES256"
    '''
    :stability: experimental
    '''
    AES128_GCM_16 = "AES128_GCM_16"
    '''
    :stability: experimental
    '''
    AES256_GCM_16 = "AES256_GCM_16"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.Phase1IntegrityAlgorithms")
class Phase1IntegrityAlgorithms(enum.Enum):
    '''
    :stability: experimental
    '''

    SHA1 = "SHA1"
    '''
    :stability: experimental
    '''
    SHA2_256 = "SHA2_256"
    '''
    :stability: experimental
    '''
    SHA2_384 = "SHA2_384"
    '''
    :stability: experimental
    '''
    SHA2_512 = "SHA2_512"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.Phase2DHGroupNumbers")
class Phase2DHGroupNumbers(enum.Enum):
    '''
    :stability: experimental
    '''

    DH2 = "DH2"
    '''
    :stability: experimental
    '''
    DH5 = "DH5"
    '''
    :stability: experimental
    '''
    DH14 = "DH14"
    '''
    :stability: experimental
    '''
    DH15 = "DH15"
    '''
    :stability: experimental
    '''
    DH16 = "DH16"
    '''
    :stability: experimental
    '''
    DH17 = "DH17"
    '''
    :stability: experimental
    '''
    DH18 = "DH18"
    '''
    :stability: experimental
    '''
    DH19 = "DH19"
    '''
    :stability: experimental
    '''
    DH20 = "DH20"
    '''
    :stability: experimental
    '''
    DH21 = "DH21"
    '''
    :stability: experimental
    '''
    DH22 = "DH22"
    '''
    :stability: experimental
    '''
    DH23 = "DH23"
    '''
    :stability: experimental
    '''
    DH24 = "DH24"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.Phase2EncryptionAlgorithms")
class Phase2EncryptionAlgorithms(enum.Enum):
    '''
    :stability: experimental
    '''

    AES128 = "AES128"
    '''
    :stability: experimental
    '''
    AES256 = "AES256"
    '''
    :stability: experimental
    '''
    AES128_GCM_16 = "AES128_GCM_16"
    '''
    :stability: experimental
    '''
    AES256_GCM_16 = "AES256_GCM_16"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.Phase2IntegrityAlgorithms")
class Phase2IntegrityAlgorithms(enum.Enum):
    '''
    :stability: experimental
    '''

    SHA1 = "SHA1"
    '''
    :stability: experimental
    '''
    SHA2_256 = "SHA2_256"
    '''
    :stability: experimental
    '''
    SHA2_384 = "SHA2_384"
    '''
    :stability: experimental
    '''
    SHA2_512 = "SHA2_512"
    '''
    :stability: experimental
    '''


class R53Resolverendpoints(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.R53Resolverendpoints",
):
    '''(experimental) Create Route53 Resolver Endpoints for MultiVPC and Hybrid DNS Resolution.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        subnet_group: builtins.str,
        vpc: aws_cdk.aws_ec2.Vpc,
        outbound_forwarding_rules: typing.Optional[typing.Sequence[typing.Union[OutboundForwardingRule, typing.Dict[str, typing.Any]]]] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: the scope in which these resources are craeted.
        :param id: the id of the construct.
        :param subnet_group: (experimental) the subnetgroup to place the resolvers in.
        :param vpc: (experimental) the vpc that the resolvers will be placed in.
        :param outbound_forwarding_rules: (experimental) An array of Internal domains that can be centrally resolved in this VPC.
        :param tag_value: (experimental) Value for Sharing.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(R53Resolverendpoints.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = R53ResolverendpointsProps(
            subnet_group=subnet_group,
            vpc=vpc,
            outbound_forwarding_rules=outbound_forwarding_rules,
            tag_value=tag_value,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="inboundResolver")
    def inbound_resolver(self) -> aws_cdk.aws_route53resolver.CfnResolverEndpoint:
        '''(experimental) inbound resolver.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_route53resolver.CfnResolverEndpoint, jsii.get(self, "inboundResolver"))

    @inbound_resolver.setter
    def inbound_resolver(
        self,
        value: aws_cdk.aws_route53resolver.CfnResolverEndpoint,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(R53Resolverendpoints, "inbound_resolver").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inboundResolver", value)

    @builtins.property
    @jsii.member(jsii_name="inboundResolversIp")
    def inbound_resolvers_ip(
        self,
    ) -> typing.List[aws_cdk.aws_route53resolver.CfnResolverRule.TargetAddressProperty]:
        '''(experimental) list of Resolver IP address's.

        :stability: experimental
        '''
        return typing.cast(typing.List[aws_cdk.aws_route53resolver.CfnResolverRule.TargetAddressProperty], jsii.get(self, "inboundResolversIp"))

    @inbound_resolvers_ip.setter
    def inbound_resolvers_ip(
        self,
        value: typing.List[aws_cdk.aws_route53resolver.CfnResolverRule.TargetAddressProperty],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(R53Resolverendpoints, "inbound_resolvers_ip").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inboundResolversIp", value)

    @builtins.property
    @jsii.member(jsii_name="outboundResolver")
    def outbound_resolver(self) -> aws_cdk.aws_route53resolver.CfnResolverEndpoint:
        '''(experimental) outbound resolver.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_route53resolver.CfnResolverEndpoint, jsii.get(self, "outboundResolver"))

    @outbound_resolver.setter
    def outbound_resolver(
        self,
        value: aws_cdk.aws_route53resolver.CfnResolverEndpoint,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(R53Resolverendpoints, "outbound_resolver").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outboundResolver", value)


@jsii.data_type(
    jsii_type="raindancers-network.R53ResolverendpointsProps",
    jsii_struct_bases=[],
    name_mapping={
        "subnet_group": "subnetGroup",
        "vpc": "vpc",
        "outbound_forwarding_rules": "outboundForwardingRules",
        "tag_value": "tagValue",
    },
)
class R53ResolverendpointsProps:
    def __init__(
        self,
        *,
        subnet_group: builtins.str,
        vpc: aws_cdk.aws_ec2.Vpc,
        outbound_forwarding_rules: typing.Optional[typing.Sequence[typing.Union[OutboundForwardingRule, typing.Dict[str, typing.Any]]]] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties to for creating inbound resolvers.

        :param subnet_group: (experimental) the subnetgroup to place the resolvers in.
        :param vpc: (experimental) the vpc that the resolvers will be placed in.
        :param outbound_forwarding_rules: (experimental) An array of Internal domains that can be centrally resolved in this VPC.
        :param tag_value: (experimental) Value for Sharing.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(R53ResolverendpointsProps.__init__)
            check_type(argname="argument subnet_group", value=subnet_group, expected_type=type_hints["subnet_group"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument outbound_forwarding_rules", value=outbound_forwarding_rules, expected_type=type_hints["outbound_forwarding_rules"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[str, typing.Any] = {
            "subnet_group": subnet_group,
            "vpc": vpc,
        }
        if outbound_forwarding_rules is not None:
            self._values["outbound_forwarding_rules"] = outbound_forwarding_rules
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def subnet_group(self) -> builtins.str:
        '''(experimental) the subnetgroup to place the resolvers in.

        :stability: experimental
        '''
        result = self._values.get("subnet_group")
        assert result is not None, "Required property 'subnet_group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.Vpc:
        '''(experimental) the vpc that the resolvers will be placed in.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.Vpc, result)

    @builtins.property
    def outbound_forwarding_rules(
        self,
    ) -> typing.Optional[typing.List[OutboundForwardingRule]]:
        '''(experimental) An array of Internal domains that can be centrally resolved in this VPC.

        :stability: experimental
        '''
        result = self._values.get("outbound_forwarding_rules")
        return typing.cast(typing.Optional[typing.List[OutboundForwardingRule]], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''(experimental) Value for Sharing.

        :stability: experimental
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "R53ResolverendpointsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.ResolverDirection")
class ResolverDirection(enum.Enum):
    '''(experimental) Direction of Resolver.

    :stability: experimental
    '''

    INBOUND = "INBOUND"
    '''(experimental) Resolver is Inbound.

    :stability: experimental
    '''
    OUTBOUND = "OUTBOUND"
    '''(experimental) Resolver is outbound.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="raindancers-network.SampleConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "device_type": "deviceType",
        "ike_version": "ikeVersion",
    },
)
class SampleConfig:
    def __init__(
        self,
        *,
        bucket: aws_cdk.aws_s3.Bucket,
        device_type: "VpnDeviceType",
        ike_version: IkeVersion,
    ) -> None:
        '''(experimental) An interface that defines a set of Sample Configurations.

        :param bucket: (experimental) The S3 bucket where to place the sample configurations.
        :param device_type: (experimental) the type of device of the customer gateway.
        :param ike_version: (experimental) create configs for IKE1 or IKE2.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SampleConfig.__init__)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument device_type", value=device_type, expected_type=type_hints["device_type"])
            check_type(argname="argument ike_version", value=ike_version, expected_type=type_hints["ike_version"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
            "device_type": device_type,
            "ike_version": ike_version,
        }

    @builtins.property
    def bucket(self) -> aws_cdk.aws_s3.Bucket:
        '''(experimental) The S3 bucket where to place the sample configurations.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.Bucket, result)

    @builtins.property
    def device_type(self) -> "VpnDeviceType":
        '''(experimental) the type of device of the customer gateway.

        :stability: experimental
        '''
        result = self._values.get("device_type")
        assert result is not None, "Required property 'device_type' is missing"
        return typing.cast("VpnDeviceType", result)

    @builtins.property
    def ike_version(self) -> IkeVersion:
        '''(experimental) create configs for IKE1 or IKE2.

        :stability: experimental
        '''
        result = self._values.get("ike_version")
        assert result is not None, "Required property 'ike_version' is missing"
        return typing.cast(IkeVersion, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SampleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.Segment",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allow_filter": "allowFilter",
        "deny_filter": "denyFilter",
        "description": "description",
        "edge_locations": "edgeLocations",
        "isolate_attachments": "isolateAttachments",
        "require_attachment_acceptance": "requireAttachmentAcceptance",
    },
)
class Segment:
    def __init__(
        self,
        *,
        name: builtins.str,
        allow_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        deny_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        edge_locations: typing.Optional[typing.Sequence[typing.Mapping[typing.Any, typing.Any]]] = None,
        isolate_attachments: typing.Optional[builtins.bool] = None,
        require_attachment_acceptance: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Segment Properties.

        :param name: (experimental) Name of the Segment.
        :param allow_filter: (experimental) A list of denys.
        :param deny_filter: (experimental) a List of denys.
        :param description: (experimental) A description of the of the segement.
        :param edge_locations: (experimental) A list of edge locations where the segement will be avaialble. Not that the locations must also be included in the core network edge ( CNE )
        :param isolate_attachments: (experimental) Set true if attached VPCS are isolated from each other.
        :param require_attachment_acceptance: (experimental) Set true if the attachment needs approval for connection. Currently not supported and requires an automation step

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Segment.__init__)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allow_filter", value=allow_filter, expected_type=type_hints["allow_filter"])
            check_type(argname="argument deny_filter", value=deny_filter, expected_type=type_hints["deny_filter"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument edge_locations", value=edge_locations, expected_type=type_hints["edge_locations"])
            check_type(argname="argument isolate_attachments", value=isolate_attachments, expected_type=type_hints["isolate_attachments"])
            check_type(argname="argument require_attachment_acceptance", value=require_attachment_acceptance, expected_type=type_hints["require_attachment_acceptance"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if allow_filter is not None:
            self._values["allow_filter"] = allow_filter
        if deny_filter is not None:
            self._values["deny_filter"] = deny_filter
        if description is not None:
            self._values["description"] = description
        if edge_locations is not None:
            self._values["edge_locations"] = edge_locations
        if isolate_attachments is not None:
            self._values["isolate_attachments"] = isolate_attachments
        if require_attachment_acceptance is not None:
            self._values["require_attachment_acceptance"] = require_attachment_acceptance

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) Name of the Segment.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of denys.

        :stability: experimental
        '''
        result = self._values.get("allow_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deny_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) a List of denys.

        :stability: experimental
        '''
        result = self._values.get("deny_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the of the segement.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edge_locations(
        self,
    ) -> typing.Optional[typing.List[typing.Mapping[typing.Any, typing.Any]]]:
        '''(experimental) A list of edge locations where the segement will be avaialble.

        Not that the
        locations must also be included in the core network edge ( CNE )

        :stability: experimental
        '''
        result = self._values.get("edge_locations")
        return typing.cast(typing.Optional[typing.List[typing.Mapping[typing.Any, typing.Any]]], result)

    @builtins.property
    def isolate_attachments(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set true if attached VPCS are isolated from each other.

        :stability: experimental
        '''
        result = self._values.get("isolate_attachments")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def require_attachment_acceptance(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set true if the attachment needs approval for connection.

        Currently not supported
        and requires an automation step

        :stability: experimental
        '''
        result = self._values.get("require_attachment_acceptance")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Segment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.SegmentAction",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "description": "description",
        "destination_cidr_blocks": "destinationCidrBlocks",
        "destinations": "destinations",
        "except_": "except",
        "mode": "mode",
        "share_with": "shareWith",
    },
)
class SegmentAction:
    def __init__(
        self,
        *,
        action: "SegmentActionType",
        description: builtins.str,
        destination_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
        except_: typing.Optional[typing.Sequence[builtins.str]] = None,
        mode: typing.Optional["SegmentActionMode"] = None,
        share_with: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    ) -> None:
        '''(experimental) Segmment ACtions.

        :param action: 
        :param description: 
        :param destination_cidr_blocks: 
        :param destinations: 
        :param except_: 
        :param mode: 
        :param share_with: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SegmentAction.__init__)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument destination_cidr_blocks", value=destination_cidr_blocks, expected_type=type_hints["destination_cidr_blocks"])
            check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
            check_type(argname="argument except_", value=except_, expected_type=type_hints["except_"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument share_with", value=share_with, expected_type=type_hints["share_with"])
        self._values: typing.Dict[str, typing.Any] = {
            "action": action,
            "description": description,
        }
        if destination_cidr_blocks is not None:
            self._values["destination_cidr_blocks"] = destination_cidr_blocks
        if destinations is not None:
            self._values["destinations"] = destinations
        if except_ is not None:
            self._values["except_"] = except_
        if mode is not None:
            self._values["mode"] = mode
        if share_with is not None:
            self._values["share_with"] = share_with

    @builtins.property
    def action(self) -> "SegmentActionType":
        '''
        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("SegmentActionType", result)

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("destination_cidr_blocks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def destinations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("destinations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def except_(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("except_")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def mode(self) -> typing.Optional["SegmentActionMode"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional["SegmentActionMode"], result)

    @builtins.property
    def share_with(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("share_with")
        return typing.cast(typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SegmentAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.SegmentActionMode")
class SegmentActionMode(enum.Enum):
    '''(experimental) Segment Action Mode.

    :stability: experimental
    '''

    ATTACHMENT_ROUTE = "ATTACHMENT_ROUTE"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.SegmentActionType")
class SegmentActionType(enum.Enum):
    '''(experimental) Segment Action Type.

    :stability: experimental
    '''

    SHARE = "SHARE"
    '''
    :stability: experimental
    '''
    CREATE_ROUTE = "CREATE_ROUTE"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="raindancers-network.ShareSubnetGroupProps",
    jsii_struct_bases=[],
    name_mapping={"account": "account", "subnet_groups": "subnetGroups"},
)
class ShareSubnetGroupProps:
    def __init__(
        self,
        *,
        account: builtins.str,
        subnet_groups: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param account: 
        :param subnet_groups: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ShareSubnetGroupProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument subnet_groups", value=subnet_groups, expected_type=type_hints["subnet_groups"])
        self._values: typing.Dict[str, typing.Any] = {
            "account": account,
            "subnet_groups": subnet_groups,
        }

    @builtins.property
    def account(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_groups(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnet_groups")
        assert result is not None, "Required property 'subnet_groups' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ShareSubnetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.SimpleAttachmentPolicyProps",
    jsii_struct_bases=[],
    name_mapping={"rule_number": "ruleNumber", "account": "account"},
)
class SimpleAttachmentPolicyProps:
    def __init__(
        self,
        *,
        rule_number: jsii.Number,
        account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rule_number: 
        :param account: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SimpleAttachmentPolicyProps.__init__)
            check_type(argname="argument rule_number", value=rule_number, expected_type=type_hints["rule_number"])
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
        self._values: typing.Dict[str, typing.Any] = {
            "rule_number": rule_number,
        }
        if account is not None:
            self._values["account"] = account

    @builtins.property
    def rule_number(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("rule_number")
        assert result is not None, "Required property 'rule_number' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SimpleAttachmentPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.SimpleShareActionProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "share_with": "shareWith"},
)
class SimpleShareActionProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        share_with: typing.Union[builtins.str, typing.Sequence[CoreNetworkSegment]],
    ) -> None:
        '''
        :param description: 
        :param share_with: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SimpleShareActionProps.__init__)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument share_with", value=share_with, expected_type=type_hints["share_with"])
        self._values: typing.Dict[str, typing.Any] = {
            "description": description,
            "share_with": share_with,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def share_with(self) -> typing.Union[builtins.str, typing.List[CoreNetworkSegment]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("share_with")
        assert result is not None, "Required property 'share_with' is missing"
        return typing.cast(typing.Union[builtins.str, typing.List[CoreNetworkSegment]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SimpleShareActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.StartupAction")
class StartupAction(enum.Enum):
    '''(experimental) Startup Action for S2S VPN.

    :stability: experimental
    '''

    START = "START"
    '''(experimental) AWS end to Intiate Startup.

    :stability: experimental
    '''
    ADD = "ADD"
    '''(experimental) Do not attempt to startup.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="raindancers-network.TGWOnCloudWanProps",
    jsii_struct_bases=[],
    name_mapping={
        "amazon_side_asn": "amazonSideAsn",
        "attachment_segment": "attachmentSegment",
        "cloudwan": "cloudwan",
        "description": "description",
        "cloud_wan_cidr": "cloudWanCidr",
        "default_route_in_segments": "defaultRouteInSegments",
        "tg_cidr": "tgCidr",
    },
)
class TGWOnCloudWanProps:
    def __init__(
        self,
        *,
        amazon_side_asn: builtins.str,
        attachment_segment: builtins.str,
        cloudwan: CoreNetwork,
        description: builtins.str,
        cloud_wan_cidr: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_route_in_segments: typing.Optional[typing.Sequence[builtins.str]] = None,
        tg_cidr: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Properties for a TWGOnCloudWan.

        :param amazon_side_asn: 
        :param attachment_segment: 
        :param cloudwan: 
        :param description: 
        :param cloud_wan_cidr: 
        :param default_route_in_segments: 
        :param tg_cidr: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TGWOnCloudWanProps.__init__)
            check_type(argname="argument amazon_side_asn", value=amazon_side_asn, expected_type=type_hints["amazon_side_asn"])
            check_type(argname="argument attachment_segment", value=attachment_segment, expected_type=type_hints["attachment_segment"])
            check_type(argname="argument cloudwan", value=cloudwan, expected_type=type_hints["cloudwan"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument cloud_wan_cidr", value=cloud_wan_cidr, expected_type=type_hints["cloud_wan_cidr"])
            check_type(argname="argument default_route_in_segments", value=default_route_in_segments, expected_type=type_hints["default_route_in_segments"])
            check_type(argname="argument tg_cidr", value=tg_cidr, expected_type=type_hints["tg_cidr"])
        self._values: typing.Dict[str, typing.Any] = {
            "amazon_side_asn": amazon_side_asn,
            "attachment_segment": attachment_segment,
            "cloudwan": cloudwan,
            "description": description,
        }
        if cloud_wan_cidr is not None:
            self._values["cloud_wan_cidr"] = cloud_wan_cidr
        if default_route_in_segments is not None:
            self._values["default_route_in_segments"] = default_route_in_segments
        if tg_cidr is not None:
            self._values["tg_cidr"] = tg_cidr

    @builtins.property
    def amazon_side_asn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("amazon_side_asn")
        assert result is not None, "Required property 'amazon_side_asn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attachment_segment(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("attachment_segment")
        assert result is not None, "Required property 'attachment_segment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloudwan(self) -> CoreNetwork:
        '''
        :stability: experimental
        '''
        result = self._values.get("cloudwan")
        assert result is not None, "Required property 'cloudwan' is missing"
        return typing.cast(CoreNetwork, result)

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_wan_cidr(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cloud_wan_cidr")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_route_in_segments(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("default_route_in_segments")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tg_cidr(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("tg_cidr")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TGWOnCloudWanProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.TunnelInsideIpVersion")
class TunnelInsideIpVersion(enum.Enum):
    '''(experimental) Determine if this is an IPv4 or IPv6 Tunnel.

    :stability: experimental
    '''

    IPV4 = "IPV4"
    '''(experimental) Use IPv4.

    :stability: experimental
    '''
    IPV6 = "IPV6"
    '''(experimental) Use IPv6.

    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.VpnDeviceType")
class VpnDeviceType(enum.Enum):
    '''(experimental) Remote end Device Types.

    :stability: experimental
    '''

    CHECKPOINT_R77_10 = "CHECKPOINT_R77_10"
    '''(experimental) Checkpoint R77_10.

    :stability: experimental
    '''
    CHECKPOINT_R80_10 = "CHECKPOINT_R80_10"
    '''
    :stability: experimental
    '''
    CISCO_ISR_12_4 = "CISCO_ISR_12_4"
    '''
    :stability: experimental
    '''
    CISCO_ASR_12_4 = "CISCO_ASR_12_4"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="raindancers-network.VpnProps",
    jsii_struct_bases=[],
    name_mapping={
        "customer_gateway": "customerGateway",
        "vpnspec": "vpnspec",
        "sampleconfig": "sampleconfig",
        "tunnel_inside_cidr": "tunnelInsideCidr",
        "tunnel_ipam_pool": "tunnelIpamPool",
    },
)
class VpnProps:
    def __init__(
        self,
        *,
        customer_gateway: aws_cdk.aws_ec2.CfnCustomerGateway,
        vpnspec: typing.Union["VpnSpecProps", typing.Dict[str, typing.Any]],
        sampleconfig: typing.Optional[typing.Union[SampleConfig, typing.Dict[str, typing.Any]]] = None,
        tunnel_inside_cidr: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel_ipam_pool: typing.Optional[aws_cdk.aws_ec2.CfnIPAMPool] = None,
    ) -> None:
        '''(experimental) Properties for S2S VPN.

        :param customer_gateway: (experimental) The customer gateway where the vpn will terminate.
        :param vpnspec: (experimental) a VPN specification for the VPN.
        :param sampleconfig: (experimental) Optionally provide a sampleconfig specification.
        :param tunnel_inside_cidr: (experimental) Specify a pair of concrete Cidr's for the tunnel. Only use one of tunnelInsideCidr or tunnelIpmamPool
        :param tunnel_ipam_pool: (experimental) Specify an ipam pool to allocated the tunnel address's from. Use only one of tunnelInsideCidr or tunnelIpamPool

        :stability: experimental
        '''
        if isinstance(vpnspec, dict):
            vpnspec = VpnSpecProps(**vpnspec)
        if isinstance(sampleconfig, dict):
            sampleconfig = SampleConfig(**sampleconfig)
        if __debug__:
            type_hints = typing.get_type_hints(VpnProps.__init__)
            check_type(argname="argument customer_gateway", value=customer_gateway, expected_type=type_hints["customer_gateway"])
            check_type(argname="argument vpnspec", value=vpnspec, expected_type=type_hints["vpnspec"])
            check_type(argname="argument sampleconfig", value=sampleconfig, expected_type=type_hints["sampleconfig"])
            check_type(argname="argument tunnel_inside_cidr", value=tunnel_inside_cidr, expected_type=type_hints["tunnel_inside_cidr"])
            check_type(argname="argument tunnel_ipam_pool", value=tunnel_ipam_pool, expected_type=type_hints["tunnel_ipam_pool"])
        self._values: typing.Dict[str, typing.Any] = {
            "customer_gateway": customer_gateway,
            "vpnspec": vpnspec,
        }
        if sampleconfig is not None:
            self._values["sampleconfig"] = sampleconfig
        if tunnel_inside_cidr is not None:
            self._values["tunnel_inside_cidr"] = tunnel_inside_cidr
        if tunnel_ipam_pool is not None:
            self._values["tunnel_ipam_pool"] = tunnel_ipam_pool

    @builtins.property
    def customer_gateway(self) -> aws_cdk.aws_ec2.CfnCustomerGateway:
        '''(experimental) The customer gateway where the vpn will terminate.

        :stability: experimental
        '''
        result = self._values.get("customer_gateway")
        assert result is not None, "Required property 'customer_gateway' is missing"
        return typing.cast(aws_cdk.aws_ec2.CfnCustomerGateway, result)

    @builtins.property
    def vpnspec(self) -> "VpnSpecProps":
        '''(experimental) a VPN specification for the VPN.

        :stability: experimental
        '''
        result = self._values.get("vpnspec")
        assert result is not None, "Required property 'vpnspec' is missing"
        return typing.cast("VpnSpecProps", result)

    @builtins.property
    def sampleconfig(self) -> typing.Optional[SampleConfig]:
        '''(experimental) Optionally provide a sampleconfig specification.

        :stability: experimental
        '''
        result = self._values.get("sampleconfig")
        return typing.cast(typing.Optional[SampleConfig], result)

    @builtins.property
    def tunnel_inside_cidr(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Specify a pair of concrete Cidr's for the tunnel.

        Only use one of tunnelInsideCidr or tunnelIpmamPool

        :stability: experimental
        '''
        result = self._values.get("tunnel_inside_cidr")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel_ipam_pool(self) -> typing.Optional[aws_cdk.aws_ec2.CfnIPAMPool]:
        '''(experimental) Specify an ipam pool to allocated the tunnel address's from.

        Use only one of tunnelInsideCidr or tunnelIpamPool

        :stability: experimental
        '''
        result = self._values.get("tunnel_ipam_pool")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.CfnIPAMPool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.VpnSpecProps",
    jsii_struct_bases=[],
    name_mapping={
        "dpd_timeout_action": "dpdTimeoutAction",
        "dpd_timeout_seconds": "dpdTimeoutSeconds",
        "enable_acceleration": "enableAcceleration",
        "enable_logging": "enableLogging",
        "ike_versions": "ikeVersions",
        "local_ipv4_network_cidr": "localIpv4NetworkCidr",
        "outside_ip_address_type": "outsideIpAddressType",
        "phase1_dh_group_numbers": "phase1DHGroupNumbers",
        "phase1_encryption_algorithms": "phase1EncryptionAlgorithms",
        "phase1_integrity_algorithms": "phase1IntegrityAlgorithms",
        "phase1_lifetime_seconds": "phase1LifetimeSeconds",
        "phase2_dh_group_numbers": "phase2DHGroupNumbers",
        "phase2_encryption_algorithms": "phase2EncryptionAlgorithms",
        "phase2_integrity_algorithms": "phase2IntegrityAlgorithms",
        "phase2_life_time_seconds": "phase2LifeTimeSeconds",
        "rekey_fuzz_percentage": "rekeyFuzzPercentage",
        "rekey_margin_time_seconds": "rekeyMarginTimeSeconds",
        "remote_ipv4_network_cidr": "remoteIpv4NetworkCidr",
        "replay_window_size": "replayWindowSize",
        "startup_action": "startupAction",
        "static_routes_only": "staticRoutesOnly",
        "tunnel_inside_ip_version": "tunnelInsideIpVersion",
    },
)
class VpnSpecProps:
    def __init__(
        self,
        *,
        dpd_timeout_action: typing.Optional[DPDTimeoutAction] = None,
        dpd_timeout_seconds: typing.Optional[jsii.Number] = None,
        enable_acceleration: typing.Optional[builtins.bool] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        ike_versions: typing.Optional[typing.Sequence[IkeVersion]] = None,
        local_ipv4_network_cidr: typing.Optional[builtins.str] = None,
        outside_ip_address_type: typing.Optional[OutsideIpAddressType] = None,
        phase1_dh_group_numbers: typing.Optional[typing.Sequence[Phase1DHGroupNumbers]] = None,
        phase1_encryption_algorithms: typing.Optional[typing.Sequence[Phase1EncryptionAlgorithms]] = None,
        phase1_integrity_algorithms: typing.Optional[typing.Sequence[Phase1IntegrityAlgorithms]] = None,
        phase1_lifetime_seconds: typing.Optional[jsii.Number] = None,
        phase2_dh_group_numbers: typing.Optional[typing.Sequence[Phase2DHGroupNumbers]] = None,
        phase2_encryption_algorithms: typing.Optional[typing.Sequence[Phase2EncryptionAlgorithms]] = None,
        phase2_integrity_algorithms: typing.Optional[typing.Sequence[Phase2IntegrityAlgorithms]] = None,
        phase2_life_time_seconds: typing.Optional[jsii.Number] = None,
        rekey_fuzz_percentage: typing.Optional[jsii.Number] = None,
        rekey_margin_time_seconds: typing.Optional[jsii.Number] = None,
        remote_ipv4_network_cidr: typing.Optional[builtins.str] = None,
        replay_window_size: typing.Optional[jsii.Number] = None,
        startup_action: typing.Optional[StartupAction] = None,
        static_routes_only: typing.Optional[typing.Union[builtins.bool, aws_cdk.IResolvable]] = None,
        tunnel_inside_ip_version: typing.Optional[TunnelInsideIpVersion] = None,
    ) -> None:
        '''(experimental) THe properties for a S2S Ipsec Vpn Connection https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateVpnConnection.html.

        :param dpd_timeout_action: Default: CLEAR The action to take after DPD timeout occurs. Specify restart to restart the IKE initiation. Specify clear to end the IKE session.
        :param dpd_timeout_seconds: Default: 30 The number of seconds after which a DPD timeout occurs.
        :param enable_acceleration: (experimental) Indicate whether to enable acceleration for the VPN connection.
        :param enable_logging: (experimental) Enable CloudwatchLogging for the S2S VPN.
        :param ike_versions: (experimental) The IKE versions that are permitted for the VPN tunnel.
        :param local_ipv4_network_cidr: Default: 0.0.0.0/0 The IPv4 CIDR on the AWS side of the VPN connection.
        :param outside_ip_address_type: Default: PUBLIC The type of IPv4 address assigned to the outside interface of the customer gateway device.
        :param phase1_dh_group_numbers: (experimental) One or more Diffie-Hellman group numbers that are permitted for the VPN tunnel for phase 1 IKE negotiations.
        :param phase1_encryption_algorithms: (experimental) One or more encryption algorithms that are permitted for the VPN tunnel for phase 1 IKE negotiations.
        :param phase1_integrity_algorithms: (experimental) One or more integrity algorithms that are permitted for the VPN tunnel for phase 1 IKE negotiations.
        :param phase1_lifetime_seconds: (experimental) The lifetime for phase 1 of the IKE negotiation, in seconds.
        :param phase2_dh_group_numbers: (experimental) One or more Diffie-Hellman group numbers that are permitted for the VPN tunnel for phase 2 IKE negotiations.
        :param phase2_encryption_algorithms: (experimental) One or more encryption algorithms that are permitted for the VPN tunnel for phase 2 IKE negotiations.
        :param phase2_integrity_algorithms: (experimental) One or more integrity algorithms that are permitted for the VPN tunnel for phase 2 IKE negotiations.
        :param phase2_life_time_seconds: (experimental) The lifetime for phase 2 of the IKE negotiation, in seconds.
        :param rekey_fuzz_percentage: Default: 100 The percentage of the rekey window (determined by RekeyMarginTimeSeconds) during which the rekey time is randomly selected.
        :param rekey_margin_time_seconds: Default: 540 The margin time, in seconds, before the phase 2 lifetime expires, during which the AWS side of the VPN connection performs an IKE rekey. The exact time of the rekey is randomly selected based on the value for RekeyFuzzPercentage.
        :param remote_ipv4_network_cidr: Default: 0.0.0.0/0 The IPv4 CIDR on the Remote side of the VPN connection.
        :param replay_window_size: Default: 1024 The number of packets in an IKE replay window.
        :param startup_action: (experimental) The action to take when the establishing the tunnel for the VPN connection. By default, your customer gateway device must initiate the IKE negotiation and bring up the tunnel. Specify start for AWS to initiate the IKE negotiation.
        :param static_routes_only: (experimental) Indicate if this will only use Static Routes Only.
        :param tunnel_inside_ip_version: Default: IPV4 Indicate whether the VPN tunnels process IPv4 or IPv6 traffic.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(VpnSpecProps.__init__)
            check_type(argname="argument dpd_timeout_action", value=dpd_timeout_action, expected_type=type_hints["dpd_timeout_action"])
            check_type(argname="argument dpd_timeout_seconds", value=dpd_timeout_seconds, expected_type=type_hints["dpd_timeout_seconds"])
            check_type(argname="argument enable_acceleration", value=enable_acceleration, expected_type=type_hints["enable_acceleration"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument ike_versions", value=ike_versions, expected_type=type_hints["ike_versions"])
            check_type(argname="argument local_ipv4_network_cidr", value=local_ipv4_network_cidr, expected_type=type_hints["local_ipv4_network_cidr"])
            check_type(argname="argument outside_ip_address_type", value=outside_ip_address_type, expected_type=type_hints["outside_ip_address_type"])
            check_type(argname="argument phase1_dh_group_numbers", value=phase1_dh_group_numbers, expected_type=type_hints["phase1_dh_group_numbers"])
            check_type(argname="argument phase1_encryption_algorithms", value=phase1_encryption_algorithms, expected_type=type_hints["phase1_encryption_algorithms"])
            check_type(argname="argument phase1_integrity_algorithms", value=phase1_integrity_algorithms, expected_type=type_hints["phase1_integrity_algorithms"])
            check_type(argname="argument phase1_lifetime_seconds", value=phase1_lifetime_seconds, expected_type=type_hints["phase1_lifetime_seconds"])
            check_type(argname="argument phase2_dh_group_numbers", value=phase2_dh_group_numbers, expected_type=type_hints["phase2_dh_group_numbers"])
            check_type(argname="argument phase2_encryption_algorithms", value=phase2_encryption_algorithms, expected_type=type_hints["phase2_encryption_algorithms"])
            check_type(argname="argument phase2_integrity_algorithms", value=phase2_integrity_algorithms, expected_type=type_hints["phase2_integrity_algorithms"])
            check_type(argname="argument phase2_life_time_seconds", value=phase2_life_time_seconds, expected_type=type_hints["phase2_life_time_seconds"])
            check_type(argname="argument rekey_fuzz_percentage", value=rekey_fuzz_percentage, expected_type=type_hints["rekey_fuzz_percentage"])
            check_type(argname="argument rekey_margin_time_seconds", value=rekey_margin_time_seconds, expected_type=type_hints["rekey_margin_time_seconds"])
            check_type(argname="argument remote_ipv4_network_cidr", value=remote_ipv4_network_cidr, expected_type=type_hints["remote_ipv4_network_cidr"])
            check_type(argname="argument replay_window_size", value=replay_window_size, expected_type=type_hints["replay_window_size"])
            check_type(argname="argument startup_action", value=startup_action, expected_type=type_hints["startup_action"])
            check_type(argname="argument static_routes_only", value=static_routes_only, expected_type=type_hints["static_routes_only"])
            check_type(argname="argument tunnel_inside_ip_version", value=tunnel_inside_ip_version, expected_type=type_hints["tunnel_inside_ip_version"])
        self._values: typing.Dict[str, typing.Any] = {}
        if dpd_timeout_action is not None:
            self._values["dpd_timeout_action"] = dpd_timeout_action
        if dpd_timeout_seconds is not None:
            self._values["dpd_timeout_seconds"] = dpd_timeout_seconds
        if enable_acceleration is not None:
            self._values["enable_acceleration"] = enable_acceleration
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if ike_versions is not None:
            self._values["ike_versions"] = ike_versions
        if local_ipv4_network_cidr is not None:
            self._values["local_ipv4_network_cidr"] = local_ipv4_network_cidr
        if outside_ip_address_type is not None:
            self._values["outside_ip_address_type"] = outside_ip_address_type
        if phase1_dh_group_numbers is not None:
            self._values["phase1_dh_group_numbers"] = phase1_dh_group_numbers
        if phase1_encryption_algorithms is not None:
            self._values["phase1_encryption_algorithms"] = phase1_encryption_algorithms
        if phase1_integrity_algorithms is not None:
            self._values["phase1_integrity_algorithms"] = phase1_integrity_algorithms
        if phase1_lifetime_seconds is not None:
            self._values["phase1_lifetime_seconds"] = phase1_lifetime_seconds
        if phase2_dh_group_numbers is not None:
            self._values["phase2_dh_group_numbers"] = phase2_dh_group_numbers
        if phase2_encryption_algorithms is not None:
            self._values["phase2_encryption_algorithms"] = phase2_encryption_algorithms
        if phase2_integrity_algorithms is not None:
            self._values["phase2_integrity_algorithms"] = phase2_integrity_algorithms
        if phase2_life_time_seconds is not None:
            self._values["phase2_life_time_seconds"] = phase2_life_time_seconds
        if rekey_fuzz_percentage is not None:
            self._values["rekey_fuzz_percentage"] = rekey_fuzz_percentage
        if rekey_margin_time_seconds is not None:
            self._values["rekey_margin_time_seconds"] = rekey_margin_time_seconds
        if remote_ipv4_network_cidr is not None:
            self._values["remote_ipv4_network_cidr"] = remote_ipv4_network_cidr
        if replay_window_size is not None:
            self._values["replay_window_size"] = replay_window_size
        if startup_action is not None:
            self._values["startup_action"] = startup_action
        if static_routes_only is not None:
            self._values["static_routes_only"] = static_routes_only
        if tunnel_inside_ip_version is not None:
            self._values["tunnel_inside_ip_version"] = tunnel_inside_ip_version

    @builtins.property
    def dpd_timeout_action(self) -> typing.Optional[DPDTimeoutAction]:
        '''
        :default: CLEAR The action to take after DPD timeout occurs. Specify restart to restart the IKE initiation. Specify clear to end the IKE session.

        :stability: experimental
        '''
        result = self._values.get("dpd_timeout_action")
        return typing.cast(typing.Optional[DPDTimeoutAction], result)

    @builtins.property
    def dpd_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''
        :default: 30 The number of seconds after which a DPD timeout occurs.

        :stability: experimental
        '''
        result = self._values.get("dpd_timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_acceleration(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicate whether to enable acceleration for the VPN connection.

        :stability: experimental
        '''
        result = self._values.get("enable_acceleration")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_logging(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable CloudwatchLogging for the S2S VPN.

        :stability: experimental
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ike_versions(self) -> typing.Optional[typing.List[IkeVersion]]:
        '''(experimental) The IKE versions that are permitted for the VPN tunnel.

        :stability: experimental
        '''
        result = self._values.get("ike_versions")
        return typing.cast(typing.Optional[typing.List[IkeVersion]], result)

    @builtins.property
    def local_ipv4_network_cidr(self) -> typing.Optional[builtins.str]:
        '''
        :default: 0.0.0.0/0 The IPv4 CIDR on the AWS side of the VPN connection.

        :stability: experimental
        '''
        result = self._values.get("local_ipv4_network_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outside_ip_address_type(self) -> typing.Optional[OutsideIpAddressType]:
        '''
        :default: PUBLIC The type of IPv4 address assigned to the outside interface of the customer gateway device.

        :stability: experimental
        '''
        result = self._values.get("outside_ip_address_type")
        return typing.cast(typing.Optional[OutsideIpAddressType], result)

    @builtins.property
    def phase1_dh_group_numbers(
        self,
    ) -> typing.Optional[typing.List[Phase1DHGroupNumbers]]:
        '''(experimental) One or more Diffie-Hellman group numbers that are permitted for the VPN tunnel for phase 1 IKE negotiations.

        :stability: experimental
        '''
        result = self._values.get("phase1_dh_group_numbers")
        return typing.cast(typing.Optional[typing.List[Phase1DHGroupNumbers]], result)

    @builtins.property
    def phase1_encryption_algorithms(
        self,
    ) -> typing.Optional[typing.List[Phase1EncryptionAlgorithms]]:
        '''(experimental) One or more encryption algorithms that are permitted for the VPN tunnel for phase 1 IKE negotiations.

        :stability: experimental
        '''
        result = self._values.get("phase1_encryption_algorithms")
        return typing.cast(typing.Optional[typing.List[Phase1EncryptionAlgorithms]], result)

    @builtins.property
    def phase1_integrity_algorithms(
        self,
    ) -> typing.Optional[typing.List[Phase1IntegrityAlgorithms]]:
        '''(experimental) One or more integrity algorithms that are permitted for the VPN tunnel for phase 1 IKE negotiations.

        :stability: experimental
        '''
        result = self._values.get("phase1_integrity_algorithms")
        return typing.cast(typing.Optional[typing.List[Phase1IntegrityAlgorithms]], result)

    @builtins.property
    def phase1_lifetime_seconds(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The lifetime for phase 1 of the IKE negotiation, in seconds.

        :stability: experimental
        '''
        result = self._values.get("phase1_lifetime_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def phase2_dh_group_numbers(
        self,
    ) -> typing.Optional[typing.List[Phase2DHGroupNumbers]]:
        '''(experimental) One or more Diffie-Hellman group numbers that are permitted for the VPN tunnel for phase 2 IKE negotiations.

        :stability: experimental
        '''
        result = self._values.get("phase2_dh_group_numbers")
        return typing.cast(typing.Optional[typing.List[Phase2DHGroupNumbers]], result)

    @builtins.property
    def phase2_encryption_algorithms(
        self,
    ) -> typing.Optional[typing.List[Phase2EncryptionAlgorithms]]:
        '''(experimental) One or more encryption algorithms that are permitted for the VPN tunnel for phase 2 IKE negotiations.

        :stability: experimental
        '''
        result = self._values.get("phase2_encryption_algorithms")
        return typing.cast(typing.Optional[typing.List[Phase2EncryptionAlgorithms]], result)

    @builtins.property
    def phase2_integrity_algorithms(
        self,
    ) -> typing.Optional[typing.List[Phase2IntegrityAlgorithms]]:
        '''(experimental) One or more integrity algorithms that are permitted for the VPN tunnel for phase 2 IKE negotiations.

        :stability: experimental
        '''
        result = self._values.get("phase2_integrity_algorithms")
        return typing.cast(typing.Optional[typing.List[Phase2IntegrityAlgorithms]], result)

    @builtins.property
    def phase2_life_time_seconds(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The lifetime for phase 2 of the IKE negotiation, in seconds.

        :stability: experimental
        '''
        result = self._values.get("phase2_life_time_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rekey_fuzz_percentage(self) -> typing.Optional[jsii.Number]:
        '''
        :default: 100 The percentage of the rekey window (determined by RekeyMarginTimeSeconds) during which the rekey time is randomly selected.

        :stability: experimental
        '''
        result = self._values.get("rekey_fuzz_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rekey_margin_time_seconds(self) -> typing.Optional[jsii.Number]:
        '''
        :default: 540 The margin time, in seconds, before the phase 2 lifetime expires, during which the AWS side of the VPN connection performs an IKE rekey. The exact time of the rekey is randomly selected based on the value for RekeyFuzzPercentage.

        :stability: experimental
        '''
        result = self._values.get("rekey_margin_time_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def remote_ipv4_network_cidr(self) -> typing.Optional[builtins.str]:
        '''
        :default: 0.0.0.0/0 The IPv4 CIDR on the Remote side of the VPN connection.

        :stability: experimental
        '''
        result = self._values.get("remote_ipv4_network_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replay_window_size(self) -> typing.Optional[jsii.Number]:
        '''
        :default: 1024 The number of packets in an IKE replay window.

        :stability: experimental
        '''
        result = self._values.get("replay_window_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def startup_action(self) -> typing.Optional[StartupAction]:
        '''(experimental) The action to take when the establishing the tunnel for the VPN connection.

        By default, your customer gateway device must initiate the IKE negotiation and bring up the tunnel. Specify start for AWS to initiate the IKE negotiation.

        :stability: experimental
        '''
        result = self._values.get("startup_action")
        return typing.cast(typing.Optional[StartupAction], result)

    @builtins.property
    def static_routes_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.IResolvable]]:
        '''(experimental) Indicate if this will only use Static Routes Only.

        :stability: experimental
        '''
        result = self._values.get("static_routes_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.IResolvable]], result)

    @builtins.property
    def tunnel_inside_ip_version(self) -> typing.Optional[TunnelInsideIpVersion]:
        '''
        :default: IPV4 Indicate whether the VPN tunnels process IPv4 or IPv6 traffic.

        :stability: experimental
        '''
        result = self._values.get("tunnel_inside_ip_version")
        return typing.cast(typing.Optional[TunnelInsideIpVersion], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnSpecProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddCoreRoutesProps",
    "AddR53ZoneProps",
    "AddRoutesProps",
    "ApplianceMode",
    "AssociationMethod",
    "AttachToCloudWanProps",
    "AttachToTransitGatewayProps",
    "AttachmentCondition",
    "AttachmentConditions",
    "AttachmentPolicy",
    "AttachmentPolicyAction",
    "AwsServiceEndPoints",
    "AwsServiceEndPointsProps",
    "CloudWanRoutingProtocolProps",
    "CloudWanTGW",
    "ConditionLogic",
    "CoreNetwork",
    "CoreNetworkProps",
    "CoreNetworkSegment",
    "CoreNetworkShare",
    "DPDTimeoutAction",
    "Destination",
    "EnterpriseVpc",
    "EnterpriseVpcProps",
    "Evpc",
    "EvpcProps",
    "FlowLogProps",
    "GetTunnelAddressPair",
    "GetTunnelAddressPairProps",
    "ICoreNetworkSegmentProps",
    "IkeVersion",
    "IpsecTunnelPool",
    "IpsecTunnelPoolProps",
    "NetworkFirewall",
    "NetworkFirewallProps",
    "Operators",
    "OutboundForwardingRule",
    "OutsideIpAddressType",
    "Phase1DHGroupNumbers",
    "Phase1EncryptionAlgorithms",
    "Phase1IntegrityAlgorithms",
    "Phase2DHGroupNumbers",
    "Phase2EncryptionAlgorithms",
    "Phase2IntegrityAlgorithms",
    "R53Resolverendpoints",
    "R53ResolverendpointsProps",
    "ResolverDirection",
    "SampleConfig",
    "Segment",
    "SegmentAction",
    "SegmentActionMode",
    "SegmentActionType",
    "ShareSubnetGroupProps",
    "SimpleAttachmentPolicyProps",
    "SimpleShareActionProps",
    "StartupAction",
    "TGWOnCloudWanProps",
    "TunnelInsideIpVersion",
    "VpnDeviceType",
    "VpnProps",
    "VpnSpecProps",
]

publication.publish()
