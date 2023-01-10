'''
# `aws_eks_cluster`

Refer to the Terraform Registory for docs: [`aws_eks_cluster`](https://www.terraform.io/docs/providers/aws/r/eks_cluster).
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

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class EksCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.eksCluster.EksCluster",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster aws_eks_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        role_arn: builtins.str,
        vpc_config: typing.Union["EksClusterVpcConfig", typing.Dict[builtins.str, typing.Any]],
        enabled_cluster_log_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        encryption_config: typing.Optional[typing.Union["EksClusterEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kubernetes_network_config: typing.Optional[typing.Union["EksClusterKubernetesNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        outpost_config: typing.Optional[typing.Union["EksClusterOutpostConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["EksClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster aws_eks_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#name EksCluster#name}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#role_arn EksCluster#role_arn}.
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#vpc_config EksCluster#vpc_config}
        :param enabled_cluster_log_types: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#enabled_cluster_log_types EksCluster#enabled_cluster_log_types}.
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#encryption_config EksCluster#encryption_config}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#id EksCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kubernetes_network_config: kubernetes_network_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#kubernetes_network_config EksCluster#kubernetes_network_config}
        :param outpost_config: outpost_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#outpost_config EksCluster#outpost_config}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#tags EksCluster#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#tags_all EksCluster#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#timeouts EksCluster#timeouts}
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#version EksCluster#version}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4aebfdf6ed797ed560522d06d31ecf6bcd525a488b66bc53cf1b542b89c9cd0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EksClusterConfig(
            name=name,
            role_arn=role_arn,
            vpc_config=vpc_config,
            enabled_cluster_log_types=enabled_cluster_log_types,
            encryption_config=encryption_config,
            id=id,
            kubernetes_network_config=kubernetes_network_config,
            outpost_config=outpost_config,
            tags=tags,
            tags_all=tags_all,
            timeouts=timeouts,
            version=version,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putEncryptionConfig")
    def put_encryption_config(
        self,
        *,
        provider: typing.Union["EksClusterEncryptionConfigProvider", typing.Dict[builtins.str, typing.Any]],
        resources: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param provider: provider block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#provider EksCluster#provider}
        :param resources: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#resources EksCluster#resources}.
        '''
        value = EksClusterEncryptionConfig(provider=provider, resources=resources)

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfig", [value]))

    @jsii.member(jsii_name="putKubernetesNetworkConfig")
    def put_kubernetes_network_config(
        self,
        *,
        ip_family: typing.Optional[builtins.str] = None,
        service_ipv4_cidr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip_family: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#ip_family EksCluster#ip_family}.
        :param service_ipv4_cidr: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#service_ipv4_cidr EksCluster#service_ipv4_cidr}.
        '''
        value = EksClusterKubernetesNetworkConfig(
            ip_family=ip_family, service_ipv4_cidr=service_ipv4_cidr
        )

        return typing.cast(None, jsii.invoke(self, "putKubernetesNetworkConfig", [value]))

    @jsii.member(jsii_name="putOutpostConfig")
    def put_outpost_config(
        self,
        *,
        control_plane_instance_type: builtins.str,
        outpost_arns: typing.Sequence[builtins.str],
        control_plane_placement: typing.Optional[typing.Union["EksClusterOutpostConfigControlPlanePlacement", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param control_plane_instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#control_plane_instance_type EksCluster#control_plane_instance_type}.
        :param outpost_arns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#outpost_arns EksCluster#outpost_arns}.
        :param control_plane_placement: control_plane_placement block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#control_plane_placement EksCluster#control_plane_placement}
        '''
        value = EksClusterOutpostConfig(
            control_plane_instance_type=control_plane_instance_type,
            outpost_arns=outpost_arns,
            control_plane_placement=control_plane_placement,
        )

        return typing.cast(None, jsii.invoke(self, "putOutpostConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#create EksCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#delete EksCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#update EksCluster#update}.
        '''
        value = EksClusterTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVpcConfig")
    def put_vpc_config(
        self,
        *,
        subnet_ids: typing.Sequence[builtins.str],
        endpoint_private_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        endpoint_public_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_access_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param subnet_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#subnet_ids EksCluster#subnet_ids}.
        :param endpoint_private_access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#endpoint_private_access EksCluster#endpoint_private_access}.
        :param endpoint_public_access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#endpoint_public_access EksCluster#endpoint_public_access}.
        :param public_access_cidrs: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#public_access_cidrs EksCluster#public_access_cidrs}.
        :param security_group_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#security_group_ids EksCluster#security_group_ids}.
        '''
        value = EksClusterVpcConfig(
            subnet_ids=subnet_ids,
            endpoint_private_access=endpoint_private_access,
            endpoint_public_access=endpoint_public_access,
            public_access_cidrs=public_access_cidrs,
            security_group_ids=security_group_ids,
        )

        return typing.cast(None, jsii.invoke(self, "putVpcConfig", [value]))

    @jsii.member(jsii_name="resetEnabledClusterLogTypes")
    def reset_enabled_cluster_log_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabledClusterLogTypes", []))

    @jsii.member(jsii_name="resetEncryptionConfig")
    def reset_encryption_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKubernetesNetworkConfig")
    def reset_kubernetes_network_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubernetesNetworkConfig", []))

    @jsii.member(jsii_name="resetOutpostConfig")
    def reset_outpost_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutpostConfig", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthority")
    def certificate_authority(self) -> "EksClusterCertificateAuthorityList":
        return typing.cast("EksClusterCertificateAuthorityList", jsii.get(self, "certificateAuthority"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(self) -> "EksClusterEncryptionConfigOutputReference":
        return typing.cast("EksClusterEncryptionConfigOutputReference", jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "EksClusterIdentityList":
        return typing.cast("EksClusterIdentityList", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesNetworkConfig")
    def kubernetes_network_config(
        self,
    ) -> "EksClusterKubernetesNetworkConfigOutputReference":
        return typing.cast("EksClusterKubernetesNetworkConfigOutputReference", jsii.get(self, "kubernetesNetworkConfig"))

    @builtins.property
    @jsii.member(jsii_name="outpostConfig")
    def outpost_config(self) -> "EksClusterOutpostConfigOutputReference":
        return typing.cast("EksClusterOutpostConfigOutputReference", jsii.get(self, "outpostConfig"))

    @builtins.property
    @jsii.member(jsii_name="platformVersion")
    def platform_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platformVersion"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "EksClusterTimeoutsOutputReference":
        return typing.cast("EksClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(self) -> "EksClusterVpcConfigOutputReference":
        return typing.cast("EksClusterVpcConfigOutputReference", jsii.get(self, "vpcConfig"))

    @builtins.property
    @jsii.member(jsii_name="enabledClusterLogTypesInput")
    def enabled_cluster_log_types_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "enabledClusterLogTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigInput")
    def encryption_config_input(self) -> typing.Optional["EksClusterEncryptionConfig"]:
        return typing.cast(typing.Optional["EksClusterEncryptionConfig"], jsii.get(self, "encryptionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesNetworkConfigInput")
    def kubernetes_network_config_input(
        self,
    ) -> typing.Optional["EksClusterKubernetesNetworkConfig"]:
        return typing.cast(typing.Optional["EksClusterKubernetesNetworkConfig"], jsii.get(self, "kubernetesNetworkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="outpostConfigInput")
    def outpost_config_input(self) -> typing.Optional["EksClusterOutpostConfig"]:
        return typing.cast(typing.Optional["EksClusterOutpostConfig"], jsii.get(self, "outpostConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["EksClusterTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["EksClusterTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcConfigInput")
    def vpc_config_input(self) -> typing.Optional["EksClusterVpcConfig"]:
        return typing.cast(typing.Optional["EksClusterVpcConfig"], jsii.get(self, "vpcConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledClusterLogTypes")
    def enabled_cluster_log_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "enabledClusterLogTypes"))

    @enabled_cluster_log_types.setter
    def enabled_cluster_log_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b12d4b59840b7e14b1afb4c4ce9594818646b67a33a51b849426ad0956790c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabledClusterLogTypes", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bd4770700448754bff7fa0518f94812124e848204a0a1374e2f0e5e021450a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b4c307ee26087778b59fd9cd8882f8b5214373439561fc944b9799b66e4a30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9870a5e95e5be0f0fa0187ddd42975b5544559b3e5f7af6358d6ee2308f249ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e01330623a7de89553fbbb1ed8c756792f6b08c3208bd7e68e233677e0f72f8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__907375254a2361c9926041e0010e1561a334781dbeba6b0ce02a3134cf7de34b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fc4e7a6ea7cf361b770e6d239e1be6bdbb53bafc1602a649e94d80035ab6e61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterCertificateAuthority",
    jsii_struct_bases=[],
    name_mapping={},
)
class EksClusterCertificateAuthority:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterCertificateAuthority(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterCertificateAuthorityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterCertificateAuthorityList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3116ec0f5b581d8c0ea2868f8d171f6feeb9d68666d7c8bf6a8a81f43821b8f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EksClusterCertificateAuthorityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__403877ea60d63a309b50b096a7070042057c0a735709d7f04dfda0afa8c0ecd9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EksClusterCertificateAuthorityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ecdfdb6e8d5b0fd3076d26c380a20fac1acda665dedfc0dc2ffffdb27364032)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eacff12b7b85bc06d312636f1a43ea5d0e150ca98e60d30eecf1e2a89837392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a58d915541bf7f3a090019f2b88460186a83913260393409e0c9d4f024301976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class EksClusterCertificateAuthorityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterCertificateAuthorityOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40a3d7a8a8e341c56c7565788e789566456a7116b6d71d514660a11502b1d24d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "data"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterCertificateAuthority]:
        return typing.cast(typing.Optional[EksClusterCertificateAuthority], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EksClusterCertificateAuthority],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe4f0432b0092e2df18db8e3c5e79f475c10e9e3a2b8a38096f3e9f58b0a205)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "role_arn": "roleArn",
        "vpc_config": "vpcConfig",
        "enabled_cluster_log_types": "enabledClusterLogTypes",
        "encryption_config": "encryptionConfig",
        "id": "id",
        "kubernetes_network_config": "kubernetesNetworkConfig",
        "outpost_config": "outpostConfig",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
        "version": "version",
    },
)
class EksClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: builtins.str,
        role_arn: builtins.str,
        vpc_config: typing.Union["EksClusterVpcConfig", typing.Dict[builtins.str, typing.Any]],
        enabled_cluster_log_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        encryption_config: typing.Optional[typing.Union["EksClusterEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kubernetes_network_config: typing.Optional[typing.Union["EksClusterKubernetesNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        outpost_config: typing.Optional[typing.Union["EksClusterOutpostConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["EksClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#name EksCluster#name}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#role_arn EksCluster#role_arn}.
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#vpc_config EksCluster#vpc_config}
        :param enabled_cluster_log_types: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#enabled_cluster_log_types EksCluster#enabled_cluster_log_types}.
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#encryption_config EksCluster#encryption_config}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#id EksCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kubernetes_network_config: kubernetes_network_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#kubernetes_network_config EksCluster#kubernetes_network_config}
        :param outpost_config: outpost_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#outpost_config EksCluster#outpost_config}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#tags EksCluster#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#tags_all EksCluster#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#timeouts EksCluster#timeouts}
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#version EksCluster#version}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(vpc_config, dict):
            vpc_config = EksClusterVpcConfig(**vpc_config)
        if isinstance(encryption_config, dict):
            encryption_config = EksClusterEncryptionConfig(**encryption_config)
        if isinstance(kubernetes_network_config, dict):
            kubernetes_network_config = EksClusterKubernetesNetworkConfig(**kubernetes_network_config)
        if isinstance(outpost_config, dict):
            outpost_config = EksClusterOutpostConfig(**outpost_config)
        if isinstance(timeouts, dict):
            timeouts = EksClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b72ef05616023323f5910901a44a9f66a350a3a0e386893813dd5f1f61348cf)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
            check_type(argname="argument enabled_cluster_log_types", value=enabled_cluster_log_types, expected_type=type_hints["enabled_cluster_log_types"])
            check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kubernetes_network_config", value=kubernetes_network_config, expected_type=type_hints["kubernetes_network_config"])
            check_type(argname="argument outpost_config", value=outpost_config, expected_type=type_hints["outpost_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "role_arn": role_arn,
            "vpc_config": vpc_config,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if enabled_cluster_log_types is not None:
            self._values["enabled_cluster_log_types"] = enabled_cluster_log_types
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if id is not None:
            self._values["id"] = id
        if kubernetes_network_config is not None:
            self._values["kubernetes_network_config"] = kubernetes_network_config
        if outpost_config is not None:
            self._values["outpost_config"] = outpost_config
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#name EksCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#role_arn EksCluster#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_config(self) -> "EksClusterVpcConfig":
        '''vpc_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#vpc_config EksCluster#vpc_config}
        '''
        result = self._values.get("vpc_config")
        assert result is not None, "Required property 'vpc_config' is missing"
        return typing.cast("EksClusterVpcConfig", result)

    @builtins.property
    def enabled_cluster_log_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#enabled_cluster_log_types EksCluster#enabled_cluster_log_types}.'''
        result = self._values.get("enabled_cluster_log_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def encryption_config(self) -> typing.Optional["EksClusterEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#encryption_config EksCluster#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["EksClusterEncryptionConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#id EksCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kubernetes_network_config(
        self,
    ) -> typing.Optional["EksClusterKubernetesNetworkConfig"]:
        '''kubernetes_network_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#kubernetes_network_config EksCluster#kubernetes_network_config}
        '''
        result = self._values.get("kubernetes_network_config")
        return typing.cast(typing.Optional["EksClusterKubernetesNetworkConfig"], result)

    @builtins.property
    def outpost_config(self) -> typing.Optional["EksClusterOutpostConfig"]:
        '''outpost_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#outpost_config EksCluster#outpost_config}
        '''
        result = self._values.get("outpost_config")
        return typing.cast(typing.Optional["EksClusterOutpostConfig"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#tags EksCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#tags_all EksCluster#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["EksClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#timeouts EksCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["EksClusterTimeouts"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#version EksCluster#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"provider": "provider", "resources": "resources"},
)
class EksClusterEncryptionConfig:
    def __init__(
        self,
        *,
        provider: typing.Union["EksClusterEncryptionConfigProvider", typing.Dict[builtins.str, typing.Any]],
        resources: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param provider: provider block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#provider EksCluster#provider}
        :param resources: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#resources EksCluster#resources}.
        '''
        if isinstance(provider, dict):
            provider = EksClusterEncryptionConfigProvider(**provider)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eaa47b989c363b78192275f6c7390682374e3a59e69280828c3bd69eaeae0c9)
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "provider": provider,
            "resources": resources,
        }

    @builtins.property
    def provider(self) -> "EksClusterEncryptionConfigProvider":
        '''provider block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#provider EksCluster#provider}
        '''
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return typing.cast("EksClusterEncryptionConfigProvider", result)

    @builtins.property
    def resources(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#resources EksCluster#resources}.'''
        result = self._values.get("resources")
        assert result is not None, "Required property 'resources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterEncryptionConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__262c1bd90efd76a98f242ebc7c9c96af725dd07f15110dc5e17a251b01ecd4fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProvider")
    def put_provider(self, *, key_arn: builtins.str) -> None:
        '''
        :param key_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#key_arn EksCluster#key_arn}.
        '''
        value = EksClusterEncryptionConfigProvider(key_arn=key_arn)

        return typing.cast(None, jsii.invoke(self, "putProvider", [value]))

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> "EksClusterEncryptionConfigProviderOutputReference":
        return typing.cast("EksClusterEncryptionConfigProviderOutputReference", jsii.get(self, "provider"))

    @builtins.property
    @jsii.member(jsii_name="providerInput")
    def provider_input(self) -> typing.Optional["EksClusterEncryptionConfigProvider"]:
        return typing.cast(typing.Optional["EksClusterEncryptionConfigProvider"], jsii.get(self, "providerInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ab9968a167187ecf3b5b44b1b19b62a8a5461cc489a4192b1cf4594a936c592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterEncryptionConfig]:
        return typing.cast(typing.Optional[EksClusterEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EksClusterEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f49ccc2e503e3f59438cb7acfbd97183908df96c81c0db5fc559870e7e30029f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterEncryptionConfigProvider",
    jsii_struct_bases=[],
    name_mapping={"key_arn": "keyArn"},
)
class EksClusterEncryptionConfigProvider:
    def __init__(self, *, key_arn: builtins.str) -> None:
        '''
        :param key_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#key_arn EksCluster#key_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67b1c05361d05a3612505068c88af51f4e89a6ddf234ac08a9ee495a17a9d823)
            check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_arn": key_arn,
        }

    @builtins.property
    def key_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#key_arn EksCluster#key_arn}.'''
        result = self._values.get("key_arn")
        assert result is not None, "Required property 'key_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterEncryptionConfigProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterEncryptionConfigProviderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterEncryptionConfigProviderOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1bf33f8db8b7c5b0e0754f4af5797a0c4148e4d88638612869f2c666b8819c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyArnInput")
    def key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyArn"))

    @key_arn.setter
    def key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b57ba56894798567fd7aa87f5a02a82a2d4dc0186e63e7fe9d58563d1d899d2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterEncryptionConfigProvider]:
        return typing.cast(typing.Optional[EksClusterEncryptionConfigProvider], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EksClusterEncryptionConfigProvider],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__996f4ae28f15bf379cd95b22d6b8c3929b5d8cb614bffbbacf790fb6a8dc834a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterIdentity",
    jsii_struct_bases=[],
    name_mapping={},
)
class EksClusterIdentity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterIdentityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterIdentityList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5443c1be102da8fa32bfab7d2ef093b2cdf20bbd515aa749847944d6ede74d1f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EksClusterIdentityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60413445bfb8ec116a8fa70add093de1cb7c1f5d00b803090a66cbc99e693c9b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EksClusterIdentityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__984121d0973d2fcd63068156dcfc8c732fe3ace507f1c675e57a929c77daaec8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00f923ba5ddcadf126bcab8a24c58e72a035e6b42d06725bb142b3079825a380)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f502d2ae5906759f0158c9e37d7a299f9a5d3e184f87351a1090ebebf7923d25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterIdentityOidc",
    jsii_struct_bases=[],
    name_mapping={},
)
class EksClusterIdentityOidc:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterIdentityOidc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterIdentityOidcList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterIdentityOidcList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd65a317dc0afe06e68d58ec1870e589354a27f116df05c93e73563dedce2ed9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EksClusterIdentityOidcOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91fac3a8daa6bdb0d7f0d98d55fe04f16b8cc94ffcd81258f6666c1d42084503)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EksClusterIdentityOidcOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24fcef3487d855a74f6c8115411f97cd42f00b1f7d360d43b3429f349319b9e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c76c66e0cc89a57148f3b9bef4fe126b37da35a13684356308088bc8fdf5578f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1b5ff5016807589352ecb6b3fefc60b39b70cbfd9533a79e8d201840ff92043)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class EksClusterIdentityOidcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterIdentityOidcOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8676f271ee445e085e8f0a825d99c3ab4c4d28a0f21d5a3d6234c5ffcd170731)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterIdentityOidc]:
        return typing.cast(typing.Optional[EksClusterIdentityOidc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EksClusterIdentityOidc]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1585ab14122ccda1fa86e06f2c99992ef72fe88f607931d51a94f7bc75c20efa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class EksClusterIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterIdentityOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5529e82bc64ea3c9cffffe6b9da699c85ec004ee53f27e4c03635add30cedbd8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="oidc")
    def oidc(self) -> EksClusterIdentityOidcList:
        return typing.cast(EksClusterIdentityOidcList, jsii.get(self, "oidc"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterIdentity]:
        return typing.cast(typing.Optional[EksClusterIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EksClusterIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca13334d1c4a4e24ebaad77b1db2922992938ca8f13008c350a5bfc55690172a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterKubernetesNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={"ip_family": "ipFamily", "service_ipv4_cidr": "serviceIpv4Cidr"},
)
class EksClusterKubernetesNetworkConfig:
    def __init__(
        self,
        *,
        ip_family: typing.Optional[builtins.str] = None,
        service_ipv4_cidr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip_family: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#ip_family EksCluster#ip_family}.
        :param service_ipv4_cidr: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#service_ipv4_cidr EksCluster#service_ipv4_cidr}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__267bc8070eb9736000bfec7f91a7fc24a6abcb1431b83260db604e3009d39a7c)
            check_type(argname="argument ip_family", value=ip_family, expected_type=type_hints["ip_family"])
            check_type(argname="argument service_ipv4_cidr", value=service_ipv4_cidr, expected_type=type_hints["service_ipv4_cidr"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ip_family is not None:
            self._values["ip_family"] = ip_family
        if service_ipv4_cidr is not None:
            self._values["service_ipv4_cidr"] = service_ipv4_cidr

    @builtins.property
    def ip_family(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#ip_family EksCluster#ip_family}.'''
        result = self._values.get("ip_family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_ipv4_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#service_ipv4_cidr EksCluster#service_ipv4_cidr}.'''
        result = self._values.get("service_ipv4_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterKubernetesNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterKubernetesNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterKubernetesNetworkConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4e6b30eff24c12bbb197d288a2a52393ca795c8682f442cd0627cb899ad18b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIpFamily")
    def reset_ip_family(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpFamily", []))

    @jsii.member(jsii_name="resetServiceIpv4Cidr")
    def reset_service_ipv4_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceIpv4Cidr", []))

    @builtins.property
    @jsii.member(jsii_name="serviceIpv6Cidr")
    def service_ipv6_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceIpv6Cidr"))

    @builtins.property
    @jsii.member(jsii_name="ipFamilyInput")
    def ip_family_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipFamilyInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceIpv4CidrInput")
    def service_ipv4_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceIpv4CidrInput"))

    @builtins.property
    @jsii.member(jsii_name="ipFamily")
    def ip_family(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipFamily"))

    @ip_family.setter
    def ip_family(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__014b383b3fb5313c2620ad8c0783ed0397bd311d07b611af5113a7bf0cd73705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipFamily", value)

    @builtins.property
    @jsii.member(jsii_name="serviceIpv4Cidr")
    def service_ipv4_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceIpv4Cidr"))

    @service_ipv4_cidr.setter
    def service_ipv4_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5b1cec684baac2a3115a758d4440646e98f78e18afc9428478c2d6feaeaffbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceIpv4Cidr", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterKubernetesNetworkConfig]:
        return typing.cast(typing.Optional[EksClusterKubernetesNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EksClusterKubernetesNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddc35a11e62ff28813239eb2f19197d614da0feca2cc5ebbd86ea4bc84f2a0aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterOutpostConfig",
    jsii_struct_bases=[],
    name_mapping={
        "control_plane_instance_type": "controlPlaneInstanceType",
        "outpost_arns": "outpostArns",
        "control_plane_placement": "controlPlanePlacement",
    },
)
class EksClusterOutpostConfig:
    def __init__(
        self,
        *,
        control_plane_instance_type: builtins.str,
        outpost_arns: typing.Sequence[builtins.str],
        control_plane_placement: typing.Optional[typing.Union["EksClusterOutpostConfigControlPlanePlacement", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param control_plane_instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#control_plane_instance_type EksCluster#control_plane_instance_type}.
        :param outpost_arns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#outpost_arns EksCluster#outpost_arns}.
        :param control_plane_placement: control_plane_placement block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#control_plane_placement EksCluster#control_plane_placement}
        '''
        if isinstance(control_plane_placement, dict):
            control_plane_placement = EksClusterOutpostConfigControlPlanePlacement(**control_plane_placement)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8b2c3ce50adfa81d56904e8f25df9f4a168e00ca5c77fc7c01e7373559feb5)
            check_type(argname="argument control_plane_instance_type", value=control_plane_instance_type, expected_type=type_hints["control_plane_instance_type"])
            check_type(argname="argument outpost_arns", value=outpost_arns, expected_type=type_hints["outpost_arns"])
            check_type(argname="argument control_plane_placement", value=control_plane_placement, expected_type=type_hints["control_plane_placement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "control_plane_instance_type": control_plane_instance_type,
            "outpost_arns": outpost_arns,
        }
        if control_plane_placement is not None:
            self._values["control_plane_placement"] = control_plane_placement

    @builtins.property
    def control_plane_instance_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#control_plane_instance_type EksCluster#control_plane_instance_type}.'''
        result = self._values.get("control_plane_instance_type")
        assert result is not None, "Required property 'control_plane_instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def outpost_arns(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#outpost_arns EksCluster#outpost_arns}.'''
        result = self._values.get("outpost_arns")
        assert result is not None, "Required property 'outpost_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def control_plane_placement(
        self,
    ) -> typing.Optional["EksClusterOutpostConfigControlPlanePlacement"]:
        '''control_plane_placement block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#control_plane_placement EksCluster#control_plane_placement}
        '''
        result = self._values.get("control_plane_placement")
        return typing.cast(typing.Optional["EksClusterOutpostConfigControlPlanePlacement"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterOutpostConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterOutpostConfigControlPlanePlacement",
    jsii_struct_bases=[],
    name_mapping={"group_name": "groupName"},
)
class EksClusterOutpostConfigControlPlanePlacement:
    def __init__(self, *, group_name: builtins.str) -> None:
        '''
        :param group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#group_name EksCluster#group_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__591ce7e7b64e69b806d4a5907ee9a6bdbe9da8ac485cf6aad89676b7fe88e8b6)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_name": group_name,
        }

    @builtins.property
    def group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#group_name EksCluster#group_name}.'''
        result = self._values.get("group_name")
        assert result is not None, "Required property 'group_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterOutpostConfigControlPlanePlacement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterOutpostConfigControlPlanePlacementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterOutpostConfigControlPlanePlacementOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff57cc9109f512b8c7cebdaafe3bfe024d4f5492bcd17ff192da8c2e059320c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="groupNameInput")
    def group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupName"))

    @group_name.setter
    def group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b24d53896d116a4da3853f7e2e22a8de158afa9d2423ff52748e0aee8c68ccc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EksClusterOutpostConfigControlPlanePlacement]:
        return typing.cast(typing.Optional[EksClusterOutpostConfigControlPlanePlacement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EksClusterOutpostConfigControlPlanePlacement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b777e305fac7646459aad01f42bf9e5b4e69ce0e17a20760e1127340b925b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class EksClusterOutpostConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterOutpostConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a813370b2ae535e10c1b268ea611eaa88a794dca37d4a167971000b78a25e4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putControlPlanePlacement")
    def put_control_plane_placement(self, *, group_name: builtins.str) -> None:
        '''
        :param group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#group_name EksCluster#group_name}.
        '''
        value = EksClusterOutpostConfigControlPlanePlacement(group_name=group_name)

        return typing.cast(None, jsii.invoke(self, "putControlPlanePlacement", [value]))

    @jsii.member(jsii_name="resetControlPlanePlacement")
    def reset_control_plane_placement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlPlanePlacement", []))

    @builtins.property
    @jsii.member(jsii_name="controlPlanePlacement")
    def control_plane_placement(
        self,
    ) -> EksClusterOutpostConfigControlPlanePlacementOutputReference:
        return typing.cast(EksClusterOutpostConfigControlPlanePlacementOutputReference, jsii.get(self, "controlPlanePlacement"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneInstanceTypeInput")
    def control_plane_instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "controlPlaneInstanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlanePlacementInput")
    def control_plane_placement_input(
        self,
    ) -> typing.Optional[EksClusterOutpostConfigControlPlanePlacement]:
        return typing.cast(typing.Optional[EksClusterOutpostConfigControlPlanePlacement], jsii.get(self, "controlPlanePlacementInput"))

    @builtins.property
    @jsii.member(jsii_name="outpostArnsInput")
    def outpost_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "outpostArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneInstanceType")
    def control_plane_instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "controlPlaneInstanceType"))

    @control_plane_instance_type.setter
    def control_plane_instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96a0a68c3315e2bb27ab44b50234adb65618ddccda8151f28ea941dc539ca719)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneInstanceType", value)

    @builtins.property
    @jsii.member(jsii_name="outpostArns")
    def outpost_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "outpostArns"))

    @outpost_arns.setter
    def outpost_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c3b4503bf89102b473048255dca3761d7af5eca45eb86cc4e576568c226282)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outpostArns", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterOutpostConfig]:
        return typing.cast(typing.Optional[EksClusterOutpostConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EksClusterOutpostConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa4a2296c57406de692e73bc4e7ca0a0961014d367c926b141c354269e9476b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class EksClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#create EksCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#delete EksCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#update EksCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aea8c89f89d9d6d9d98349aa2b98d286f6fe0be0689a191e69b8a9a2154c7cd)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#create EksCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#delete EksCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#update EksCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e45645907d46b199aadb64c44f5d1f4f6e3bd55bb26c21493403475b004c293)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d6e25dd7f6fc551b91053f8d9fb22ffe8dd5a83388a278ee3821b9b5b56dde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7585ecc7bffda7c2a226abfa3c3c4354ad9e1d4c5ae151726e8491e2413758fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607459d309d15f9c3e63fc5701ba1d9f5f53d2203fd1a99e8c49d3559db16e6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[EksClusterTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[EksClusterTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[EksClusterTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c12ae59339cd92035ccee14c840c21d43838666fbb54b55e963e47aaa5a07889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterVpcConfig",
    jsii_struct_bases=[],
    name_mapping={
        "subnet_ids": "subnetIds",
        "endpoint_private_access": "endpointPrivateAccess",
        "endpoint_public_access": "endpointPublicAccess",
        "public_access_cidrs": "publicAccessCidrs",
        "security_group_ids": "securityGroupIds",
    },
)
class EksClusterVpcConfig:
    def __init__(
        self,
        *,
        subnet_ids: typing.Sequence[builtins.str],
        endpoint_private_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        endpoint_public_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_access_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param subnet_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#subnet_ids EksCluster#subnet_ids}.
        :param endpoint_private_access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#endpoint_private_access EksCluster#endpoint_private_access}.
        :param endpoint_public_access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#endpoint_public_access EksCluster#endpoint_public_access}.
        :param public_access_cidrs: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#public_access_cidrs EksCluster#public_access_cidrs}.
        :param security_group_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#security_group_ids EksCluster#security_group_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58b4fb9db7c16fb1bfe30835f60574d3f94f4b1ce5871471c55ee206e0092a1)
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument endpoint_private_access", value=endpoint_private_access, expected_type=type_hints["endpoint_private_access"])
            check_type(argname="argument endpoint_public_access", value=endpoint_public_access, expected_type=type_hints["endpoint_public_access"])
            check_type(argname="argument public_access_cidrs", value=public_access_cidrs, expected_type=type_hints["public_access_cidrs"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet_ids": subnet_ids,
        }
        if endpoint_private_access is not None:
            self._values["endpoint_private_access"] = endpoint_private_access
        if endpoint_public_access is not None:
            self._values["endpoint_public_access"] = endpoint_public_access
        if public_access_cidrs is not None:
            self._values["public_access_cidrs"] = public_access_cidrs
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#subnet_ids EksCluster#subnet_ids}.'''
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def endpoint_private_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#endpoint_private_access EksCluster#endpoint_private_access}.'''
        result = self._values.get("endpoint_private_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def endpoint_public_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#endpoint_public_access EksCluster#endpoint_public_access}.'''
        result = self._values.get("endpoint_public_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def public_access_cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#public_access_cidrs EksCluster#public_access_cidrs}.'''
        result = self._values.get("public_access_cidrs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/eks_cluster#security_group_ids EksCluster#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterVpcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterVpcConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.eksCluster.EksClusterVpcConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31fc31961433ba1b1dae71eb72142a7f09e1d9363a56a4abfb2e6783081c1a10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEndpointPrivateAccess")
    def reset_endpoint_private_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointPrivateAccess", []))

    @jsii.member(jsii_name="resetEndpointPublicAccess")
    def reset_endpoint_public_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointPublicAccess", []))

    @jsii.member(jsii_name="resetPublicAccessCidrs")
    def reset_public_access_cidrs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicAccessCidrs", []))

    @jsii.member(jsii_name="resetSecurityGroupIds")
    def reset_security_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupIds", []))

    @builtins.property
    @jsii.member(jsii_name="clusterSecurityGroupId")
    def cluster_security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterSecurityGroupId"))

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @builtins.property
    @jsii.member(jsii_name="endpointPrivateAccessInput")
    def endpoint_private_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "endpointPrivateAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointPublicAccessInput")
    def endpoint_public_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "endpointPublicAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="publicAccessCidrsInput")
    def public_access_cidrs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "publicAccessCidrsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdsInput")
    def subnet_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointPrivateAccess")
    def endpoint_private_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "endpointPrivateAccess"))

    @endpoint_private_access.setter
    def endpoint_private_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__309e56bfba6c637539a0af5959a2f21a3777d16416d0116cdc74084a7ed43047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointPrivateAccess", value)

    @builtins.property
    @jsii.member(jsii_name="endpointPublicAccess")
    def endpoint_public_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "endpointPublicAccess"))

    @endpoint_public_access.setter
    def endpoint_public_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__819b34c75dad5169d14e36d62b6f32636929c1287b7badb80b201ba08aa3b3df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointPublicAccess", value)

    @builtins.property
    @jsii.member(jsii_name="publicAccessCidrs")
    def public_access_cidrs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "publicAccessCidrs"))

    @public_access_cidrs.setter
    def public_access_cidrs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__885bee2af2c1e2f4af6f58bd200e3a59e6c196f8b3eb99fc0f2a41b81293165a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicAccessCidrs", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12273f83050fc167620c9562aa4e4bc915b45760d259fa75d0c5dcb01a5b0780)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c484b1ca505f9e4e81eba8dc2ab67767cbf795ebb0524cf105dd5e98a514ae5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterVpcConfig]:
        return typing.cast(typing.Optional[EksClusterVpcConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EksClusterVpcConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44e3c456e290ecf65a7338c295c5bef2d254cee54ca61275f35160f975e49d50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "EksCluster",
    "EksClusterCertificateAuthority",
    "EksClusterCertificateAuthorityList",
    "EksClusterCertificateAuthorityOutputReference",
    "EksClusterConfig",
    "EksClusterEncryptionConfig",
    "EksClusterEncryptionConfigOutputReference",
    "EksClusterEncryptionConfigProvider",
    "EksClusterEncryptionConfigProviderOutputReference",
    "EksClusterIdentity",
    "EksClusterIdentityList",
    "EksClusterIdentityOidc",
    "EksClusterIdentityOidcList",
    "EksClusterIdentityOidcOutputReference",
    "EksClusterIdentityOutputReference",
    "EksClusterKubernetesNetworkConfig",
    "EksClusterKubernetesNetworkConfigOutputReference",
    "EksClusterOutpostConfig",
    "EksClusterOutpostConfigControlPlanePlacement",
    "EksClusterOutpostConfigControlPlanePlacementOutputReference",
    "EksClusterOutpostConfigOutputReference",
    "EksClusterTimeouts",
    "EksClusterTimeoutsOutputReference",
    "EksClusterVpcConfig",
    "EksClusterVpcConfigOutputReference",
]

publication.publish()

def _typecheckingstub__b4aebfdf6ed797ed560522d06d31ecf6bcd525a488b66bc53cf1b542b89c9cd0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    role_arn: builtins.str,
    vpc_config: typing.Union[EksClusterVpcConfig, typing.Dict[builtins.str, typing.Any]],
    enabled_cluster_log_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    encryption_config: typing.Optional[typing.Union[EksClusterEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kubernetes_network_config: typing.Optional[typing.Union[EksClusterKubernetesNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    outpost_config: typing.Optional[typing.Union[EksClusterOutpostConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[EksClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12d4b59840b7e14b1afb4c4ce9594818646b67a33a51b849426ad0956790c83(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd4770700448754bff7fa0518f94812124e848204a0a1374e2f0e5e021450a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b4c307ee26087778b59fd9cd8882f8b5214373439561fc944b9799b66e4a30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9870a5e95e5be0f0fa0187ddd42975b5544559b3e5f7af6358d6ee2308f249ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e01330623a7de89553fbbb1ed8c756792f6b08c3208bd7e68e233677e0f72f8a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__907375254a2361c9926041e0010e1561a334781dbeba6b0ce02a3134cf7de34b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc4e7a6ea7cf361b770e6d239e1be6bdbb53bafc1602a649e94d80035ab6e61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3116ec0f5b581d8c0ea2868f8d171f6feeb9d68666d7c8bf6a8a81f43821b8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__403877ea60d63a309b50b096a7070042057c0a735709d7f04dfda0afa8c0ecd9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ecdfdb6e8d5b0fd3076d26c380a20fac1acda665dedfc0dc2ffffdb27364032(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eacff12b7b85bc06d312636f1a43ea5d0e150ca98e60d30eecf1e2a89837392(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58d915541bf7f3a090019f2b88460186a83913260393409e0c9d4f024301976(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a3d7a8a8e341c56c7565788e789566456a7116b6d71d514660a11502b1d24d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe4f0432b0092e2df18db8e3c5e79f475c10e9e3a2b8a38096f3e9f58b0a205(
    value: typing.Optional[EksClusterCertificateAuthority],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b72ef05616023323f5910901a44a9f66a350a3a0e386893813dd5f1f61348cf(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    role_arn: builtins.str,
    vpc_config: typing.Union[EksClusterVpcConfig, typing.Dict[builtins.str, typing.Any]],
    enabled_cluster_log_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    encryption_config: typing.Optional[typing.Union[EksClusterEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kubernetes_network_config: typing.Optional[typing.Union[EksClusterKubernetesNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    outpost_config: typing.Optional[typing.Union[EksClusterOutpostConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[EksClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eaa47b989c363b78192275f6c7390682374e3a59e69280828c3bd69eaeae0c9(
    *,
    provider: typing.Union[EksClusterEncryptionConfigProvider, typing.Dict[builtins.str, typing.Any]],
    resources: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262c1bd90efd76a98f242ebc7c9c96af725dd07f15110dc5e17a251b01ecd4fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ab9968a167187ecf3b5b44b1b19b62a8a5461cc489a4192b1cf4594a936c592(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f49ccc2e503e3f59438cb7acfbd97183908df96c81c0db5fc559870e7e30029f(
    value: typing.Optional[EksClusterEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b1c05361d05a3612505068c88af51f4e89a6ddf234ac08a9ee495a17a9d823(
    *,
    key_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1bf33f8db8b7c5b0e0754f4af5797a0c4148e4d88638612869f2c666b8819c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b57ba56894798567fd7aa87f5a02a82a2d4dc0186e63e7fe9d58563d1d899d2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__996f4ae28f15bf379cd95b22d6b8c3929b5d8cb614bffbbacf790fb6a8dc834a(
    value: typing.Optional[EksClusterEncryptionConfigProvider],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5443c1be102da8fa32bfab7d2ef093b2cdf20bbd515aa749847944d6ede74d1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60413445bfb8ec116a8fa70add093de1cb7c1f5d00b803090a66cbc99e693c9b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__984121d0973d2fcd63068156dcfc8c732fe3ace507f1c675e57a929c77daaec8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00f923ba5ddcadf126bcab8a24c58e72a035e6b42d06725bb142b3079825a380(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f502d2ae5906759f0158c9e37d7a299f9a5d3e184f87351a1090ebebf7923d25(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd65a317dc0afe06e68d58ec1870e589354a27f116df05c93e73563dedce2ed9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91fac3a8daa6bdb0d7f0d98d55fe04f16b8cc94ffcd81258f6666c1d42084503(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24fcef3487d855a74f6c8115411f97cd42f00b1f7d360d43b3429f349319b9e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c76c66e0cc89a57148f3b9bef4fe126b37da35a13684356308088bc8fdf5578f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1b5ff5016807589352ecb6b3fefc60b39b70cbfd9533a79e8d201840ff92043(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8676f271ee445e085e8f0a825d99c3ab4c4d28a0f21d5a3d6234c5ffcd170731(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1585ab14122ccda1fa86e06f2c99992ef72fe88f607931d51a94f7bc75c20efa(
    value: typing.Optional[EksClusterIdentityOidc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5529e82bc64ea3c9cffffe6b9da699c85ec004ee53f27e4c03635add30cedbd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca13334d1c4a4e24ebaad77b1db2922992938ca8f13008c350a5bfc55690172a(
    value: typing.Optional[EksClusterIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267bc8070eb9736000bfec7f91a7fc24a6abcb1431b83260db604e3009d39a7c(
    *,
    ip_family: typing.Optional[builtins.str] = None,
    service_ipv4_cidr: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e6b30eff24c12bbb197d288a2a52393ca795c8682f442cd0627cb899ad18b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014b383b3fb5313c2620ad8c0783ed0397bd311d07b611af5113a7bf0cd73705(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b1cec684baac2a3115a758d4440646e98f78e18afc9428478c2d6feaeaffbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddc35a11e62ff28813239eb2f19197d614da0feca2cc5ebbd86ea4bc84f2a0aa(
    value: typing.Optional[EksClusterKubernetesNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8b2c3ce50adfa81d56904e8f25df9f4a168e00ca5c77fc7c01e7373559feb5(
    *,
    control_plane_instance_type: builtins.str,
    outpost_arns: typing.Sequence[builtins.str],
    control_plane_placement: typing.Optional[typing.Union[EksClusterOutpostConfigControlPlanePlacement, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591ce7e7b64e69b806d4a5907ee9a6bdbe9da8ac485cf6aad89676b7fe88e8b6(
    *,
    group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff57cc9109f512b8c7cebdaafe3bfe024d4f5492bcd17ff192da8c2e059320c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b24d53896d116a4da3853f7e2e22a8de158afa9d2423ff52748e0aee8c68ccc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b777e305fac7646459aad01f42bf9e5b4e69ce0e17a20760e1127340b925b4(
    value: typing.Optional[EksClusterOutpostConfigControlPlanePlacement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a813370b2ae535e10c1b268ea611eaa88a794dca37d4a167971000b78a25e4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96a0a68c3315e2bb27ab44b50234adb65618ddccda8151f28ea941dc539ca719(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c3b4503bf89102b473048255dca3761d7af5eca45eb86cc4e576568c226282(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa4a2296c57406de692e73bc4e7ca0a0961014d367c926b141c354269e9476b6(
    value: typing.Optional[EksClusterOutpostConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aea8c89f89d9d6d9d98349aa2b98d286f6fe0be0689a191e69b8a9a2154c7cd(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e45645907d46b199aadb64c44f5d1f4f6e3bd55bb26c21493403475b004c293(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d6e25dd7f6fc551b91053f8d9fb22ffe8dd5a83388a278ee3821b9b5b56dde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7585ecc7bffda7c2a226abfa3c3c4354ad9e1d4c5ae151726e8491e2413758fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607459d309d15f9c3e63fc5701ba1d9f5f53d2203fd1a99e8c49d3559db16e6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c12ae59339cd92035ccee14c840c21d43838666fbb54b55e963e47aaa5a07889(
    value: typing.Optional[typing.Union[EksClusterTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58b4fb9db7c16fb1bfe30835f60574d3f94f4b1ce5871471c55ee206e0092a1(
    *,
    subnet_ids: typing.Sequence[builtins.str],
    endpoint_private_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    endpoint_public_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_access_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31fc31961433ba1b1dae71eb72142a7f09e1d9363a56a4abfb2e6783081c1a10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__309e56bfba6c637539a0af5959a2f21a3777d16416d0116cdc74084a7ed43047(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819b34c75dad5169d14e36d62b6f32636929c1287b7badb80b201ba08aa3b3df(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__885bee2af2c1e2f4af6f58bd200e3a59e6c196f8b3eb99fc0f2a41b81293165a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12273f83050fc167620c9562aa4e4bc915b45760d259fa75d0c5dcb01a5b0780(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c484b1ca505f9e4e81eba8dc2ab67767cbf795ebb0524cf105dd5e98a514ae5a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e3c456e290ecf65a7338c295c5bef2d254cee54ca61275f35160f975e49d50(
    value: typing.Optional[EksClusterVpcConfig],
) -> None:
    """Type checking stubs"""
    pass
