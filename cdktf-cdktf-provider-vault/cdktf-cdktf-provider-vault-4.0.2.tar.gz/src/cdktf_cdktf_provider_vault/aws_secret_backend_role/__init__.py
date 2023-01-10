'''
# `vault_aws_secret_backend_role`

Refer to the Terraform Registory for docs: [`vault_aws_secret_backend_role`](https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role).
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


class AwsSecretBackendRole(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.awsSecretBackendRole.AwsSecretBackendRole",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role vault_aws_secret_backend_role}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        backend: builtins.str,
        credential_type: builtins.str,
        name: builtins.str,
        default_sts_ttl: typing.Optional[jsii.Number] = None,
        iam_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        max_sts_ttl: typing.Optional[jsii.Number] = None,
        namespace: typing.Optional[builtins.str] = None,
        permissions_boundary_arn: typing.Optional[builtins.str] = None,
        policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        policy_document: typing.Optional[builtins.str] = None,
        role_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_path: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role vault_aws_secret_backend_role} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param backend: The path of the AWS Secret Backend the role belongs to. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#backend AwsSecretBackendRole#backend}
        :param credential_type: Role credential type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#credential_type AwsSecretBackendRole#credential_type}
        :param name: Unique name for the role. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#name AwsSecretBackendRole#name}
        :param default_sts_ttl: The default TTL in seconds for STS credentials. When a TTL is not specified when STS credentials are requested, and a default TTL is specified on the role, then this default TTL will be used. Valid only when credential_type is one of assumed_role or federation_token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#default_sts_ttl AwsSecretBackendRole#default_sts_ttl}
        :param iam_groups: A list of IAM group names. IAM users generated against this vault role will be added to these IAM Groups. For a credential type of assumed_role or federation_token, the policies sent to the corresponding AWS call (sts:AssumeRole or sts:GetFederation) will be the policies from each group in iam_groups combined with the policy_document and policy_arns parameters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#iam_groups AwsSecretBackendRole#iam_groups}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#id AwsSecretBackendRole#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_sts_ttl: The max allowed TTL in seconds for STS credentials (credentials TTL are capped to max_sts_ttl). Valid only when credential_type is one of assumed_role or federation_token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#max_sts_ttl AwsSecretBackendRole#max_sts_ttl}
        :param namespace: Target namespace. (requires Enterprise). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#namespace AwsSecretBackendRole#namespace}
        :param permissions_boundary_arn: The ARN of the AWS Permissions Boundary to attach to IAM users created in the role. Valid only when credential_type is iam_user. If not specified, then no permissions boundary policy will be attached. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#permissions_boundary_arn AwsSecretBackendRole#permissions_boundary_arn}
        :param policy_arns: ARN for an existing IAM policy the role should use. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#policy_arns AwsSecretBackendRole#policy_arns}
        :param policy_document: IAM policy the role should use in JSON format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#policy_document AwsSecretBackendRole#policy_document}
        :param role_arns: ARNs of AWS roles allowed to be assumed. Only valid when credential_type is 'assumed_role'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#role_arns AwsSecretBackendRole#role_arns}
        :param user_path: The path for the user name. Valid only when credential_type is iam_user. Default is /. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#user_path AwsSecretBackendRole#user_path}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__663a3ea86009355c9c58a6ee0d6e1bdb7dc4885593381f5d5673c88c616c51be)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AwsSecretBackendRoleConfig(
            backend=backend,
            credential_type=credential_type,
            name=name,
            default_sts_ttl=default_sts_ttl,
            iam_groups=iam_groups,
            id=id,
            max_sts_ttl=max_sts_ttl,
            namespace=namespace,
            permissions_boundary_arn=permissions_boundary_arn,
            policy_arns=policy_arns,
            policy_document=policy_document,
            role_arns=role_arns,
            user_path=user_path,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetDefaultStsTtl")
    def reset_default_sts_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultStsTtl", []))

    @jsii.member(jsii_name="resetIamGroups")
    def reset_iam_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIamGroups", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaxStsTtl")
    def reset_max_sts_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxStsTtl", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetPermissionsBoundaryArn")
    def reset_permissions_boundary_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissionsBoundaryArn", []))

    @jsii.member(jsii_name="resetPolicyArns")
    def reset_policy_arns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyArns", []))

    @jsii.member(jsii_name="resetPolicyDocument")
    def reset_policy_document(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyDocument", []))

    @jsii.member(jsii_name="resetRoleArns")
    def reset_role_arns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoleArns", []))

    @jsii.member(jsii_name="resetUserPath")
    def reset_user_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserPath", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="backendInput")
    def backend_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backendInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialTypeInput")
    def credential_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultStsTtlInput")
    def default_sts_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultStsTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="iamGroupsInput")
    def iam_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "iamGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="maxStsTtlInput")
    def max_sts_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxStsTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundaryArnInput")
    def permissions_boundary_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsBoundaryArnInput"))

    @builtins.property
    @jsii.member(jsii_name="policyArnsInput")
    def policy_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "policyArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="policyDocumentInput")
    def policy_document_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyDocumentInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnsInput")
    def role_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "roleArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="userPathInput")
    def user_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPathInput"))

    @builtins.property
    @jsii.member(jsii_name="backend")
    def backend(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backend"))

    @backend.setter
    def backend(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8446b7e7024db391dd5852b45f7ddb55b190d8ad3805bb0c8791eaa775248d11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backend", value)

    @builtins.property
    @jsii.member(jsii_name="credentialType")
    def credential_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentialType"))

    @credential_type.setter
    def credential_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea6b12aa288744d0c63ba2c772fcbd9a315f485ca31a65b3e9536047e46b142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialType", value)

    @builtins.property
    @jsii.member(jsii_name="defaultStsTtl")
    def default_sts_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultStsTtl"))

    @default_sts_ttl.setter
    def default_sts_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98ad7ed45a9d4d1ea52cb4e5aff8dcca28a6bd027de1ae85625fbafded8d2137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultStsTtl", value)

    @builtins.property
    @jsii.member(jsii_name="iamGroups")
    def iam_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "iamGroups"))

    @iam_groups.setter
    def iam_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d20bc2515ece10b3dff0a6ffa582f99fa4117bc847d336f037b925e6461beabb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamGroups", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec631ee33ed1abc4989762bb8f65db28737e7238529cf74e85124f0ac8657817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="maxStsTtl")
    def max_sts_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxStsTtl"))

    @max_sts_ttl.setter
    def max_sts_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c83025ff782d311a6bbee85d4dad4df9d35b6c00c8d092a3b058bd86d81beef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxStsTtl", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d0a6e7d0cf817b65ed5033e5497dbf0288db37ef099a8fbff77d37612c9de62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d2136d094ad30954ae0876aace2c5fe6c60933ea96aa3c9f65c21e8f744489d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value)

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundaryArn")
    def permissions_boundary_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissionsBoundaryArn"))

    @permissions_boundary_arn.setter
    def permissions_boundary_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5040006dd9b1f3ab6c76da027c1320e4210363484c53d69c02ea1da9c4ff8550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionsBoundaryArn", value)

    @builtins.property
    @jsii.member(jsii_name="policyArns")
    def policy_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "policyArns"))

    @policy_arns.setter
    def policy_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5269f9b8625105b04ebdc9ffc01c05112d1cc1bca521e6cdb0ef8ed7e6455937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyArns", value)

    @builtins.property
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyDocument"))

    @policy_document.setter
    def policy_document(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cab822a377c9ad5b0c2b06839cb75f5442f11feb2ba0a918663190eb81c2045)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="roleArns")
    def role_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roleArns"))

    @role_arns.setter
    def role_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf9ef81590bf704c788163c8f1468bb8e5ed5678c522067a4b81f8cd90fa4cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArns", value)

    @builtins.property
    @jsii.member(jsii_name="userPath")
    def user_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPath"))

    @user_path.setter
    def user_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b50460f234bf337eb9887f1c1d9c43154d8a1de05232592e5408b53e0450c619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPath", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.awsSecretBackendRole.AwsSecretBackendRoleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "backend": "backend",
        "credential_type": "credentialType",
        "name": "name",
        "default_sts_ttl": "defaultStsTtl",
        "iam_groups": "iamGroups",
        "id": "id",
        "max_sts_ttl": "maxStsTtl",
        "namespace": "namespace",
        "permissions_boundary_arn": "permissionsBoundaryArn",
        "policy_arns": "policyArns",
        "policy_document": "policyDocument",
        "role_arns": "roleArns",
        "user_path": "userPath",
    },
)
class AwsSecretBackendRoleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        backend: builtins.str,
        credential_type: builtins.str,
        name: builtins.str,
        default_sts_ttl: typing.Optional[jsii.Number] = None,
        iam_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        max_sts_ttl: typing.Optional[jsii.Number] = None,
        namespace: typing.Optional[builtins.str] = None,
        permissions_boundary_arn: typing.Optional[builtins.str] = None,
        policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        policy_document: typing.Optional[builtins.str] = None,
        role_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param backend: The path of the AWS Secret Backend the role belongs to. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#backend AwsSecretBackendRole#backend}
        :param credential_type: Role credential type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#credential_type AwsSecretBackendRole#credential_type}
        :param name: Unique name for the role. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#name AwsSecretBackendRole#name}
        :param default_sts_ttl: The default TTL in seconds for STS credentials. When a TTL is not specified when STS credentials are requested, and a default TTL is specified on the role, then this default TTL will be used. Valid only when credential_type is one of assumed_role or federation_token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#default_sts_ttl AwsSecretBackendRole#default_sts_ttl}
        :param iam_groups: A list of IAM group names. IAM users generated against this vault role will be added to these IAM Groups. For a credential type of assumed_role or federation_token, the policies sent to the corresponding AWS call (sts:AssumeRole or sts:GetFederation) will be the policies from each group in iam_groups combined with the policy_document and policy_arns parameters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#iam_groups AwsSecretBackendRole#iam_groups}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#id AwsSecretBackendRole#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_sts_ttl: The max allowed TTL in seconds for STS credentials (credentials TTL are capped to max_sts_ttl). Valid only when credential_type is one of assumed_role or federation_token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#max_sts_ttl AwsSecretBackendRole#max_sts_ttl}
        :param namespace: Target namespace. (requires Enterprise). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#namespace AwsSecretBackendRole#namespace}
        :param permissions_boundary_arn: The ARN of the AWS Permissions Boundary to attach to IAM users created in the role. Valid only when credential_type is iam_user. If not specified, then no permissions boundary policy will be attached. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#permissions_boundary_arn AwsSecretBackendRole#permissions_boundary_arn}
        :param policy_arns: ARN for an existing IAM policy the role should use. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#policy_arns AwsSecretBackendRole#policy_arns}
        :param policy_document: IAM policy the role should use in JSON format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#policy_document AwsSecretBackendRole#policy_document}
        :param role_arns: ARNs of AWS roles allowed to be assumed. Only valid when credential_type is 'assumed_role'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#role_arns AwsSecretBackendRole#role_arns}
        :param user_path: The path for the user name. Valid only when credential_type is iam_user. Default is /. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#user_path AwsSecretBackendRole#user_path}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8807b740994d46f071152460b10ed5176d10bbb157454d75b22602e9705a9cd9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument backend", value=backend, expected_type=type_hints["backend"])
            check_type(argname="argument credential_type", value=credential_type, expected_type=type_hints["credential_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument default_sts_ttl", value=default_sts_ttl, expected_type=type_hints["default_sts_ttl"])
            check_type(argname="argument iam_groups", value=iam_groups, expected_type=type_hints["iam_groups"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument max_sts_ttl", value=max_sts_ttl, expected_type=type_hints["max_sts_ttl"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument permissions_boundary_arn", value=permissions_boundary_arn, expected_type=type_hints["permissions_boundary_arn"])
            check_type(argname="argument policy_arns", value=policy_arns, expected_type=type_hints["policy_arns"])
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument role_arns", value=role_arns, expected_type=type_hints["role_arns"])
            check_type(argname="argument user_path", value=user_path, expected_type=type_hints["user_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backend": backend,
            "credential_type": credential_type,
            "name": name,
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
        if default_sts_ttl is not None:
            self._values["default_sts_ttl"] = default_sts_ttl
        if iam_groups is not None:
            self._values["iam_groups"] = iam_groups
        if id is not None:
            self._values["id"] = id
        if max_sts_ttl is not None:
            self._values["max_sts_ttl"] = max_sts_ttl
        if namespace is not None:
            self._values["namespace"] = namespace
        if permissions_boundary_arn is not None:
            self._values["permissions_boundary_arn"] = permissions_boundary_arn
        if policy_arns is not None:
            self._values["policy_arns"] = policy_arns
        if policy_document is not None:
            self._values["policy_document"] = policy_document
        if role_arns is not None:
            self._values["role_arns"] = role_arns
        if user_path is not None:
            self._values["user_path"] = user_path

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
    def backend(self) -> builtins.str:
        '''The path of the AWS Secret Backend the role belongs to.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#backend AwsSecretBackendRole#backend}
        '''
        result = self._values.get("backend")
        assert result is not None, "Required property 'backend' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def credential_type(self) -> builtins.str:
        '''Role credential type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#credential_type AwsSecretBackendRole#credential_type}
        '''
        result = self._values.get("credential_type")
        assert result is not None, "Required property 'credential_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Unique name for the role.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#name AwsSecretBackendRole#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_sts_ttl(self) -> typing.Optional[jsii.Number]:
        '''The default TTL in seconds for STS credentials.

        When a TTL is not specified when STS credentials are requested, and a default TTL is specified on the role, then this default TTL will be used. Valid only when credential_type is one of assumed_role or federation_token.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#default_sts_ttl AwsSecretBackendRole#default_sts_ttl}
        '''
        result = self._values.get("default_sts_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def iam_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IAM group names.

        IAM users generated against this vault role will be added to these IAM Groups. For a credential type of assumed_role or federation_token, the policies sent to the corresponding AWS call (sts:AssumeRole or sts:GetFederation) will be the policies from each group in iam_groups combined with the policy_document and policy_arns parameters.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#iam_groups AwsSecretBackendRole#iam_groups}
        '''
        result = self._values.get("iam_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#id AwsSecretBackendRole#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_sts_ttl(self) -> typing.Optional[jsii.Number]:
        '''The max allowed TTL in seconds for STS credentials (credentials TTL are capped to max_sts_ttl).

        Valid only when credential_type is one of assumed_role or federation_token.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#max_sts_ttl AwsSecretBackendRole#max_sts_ttl}
        '''
        result = self._values.get("max_sts_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Target namespace. (requires Enterprise).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#namespace AwsSecretBackendRole#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the AWS Permissions Boundary to attach to IAM users created in the role.

        Valid only when credential_type is iam_user. If not specified, then no permissions boundary policy will be attached.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#permissions_boundary_arn AwsSecretBackendRole#permissions_boundary_arn}
        '''
        result = self._values.get("permissions_boundary_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''ARN for an existing IAM policy the role should use.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#policy_arns AwsSecretBackendRole#policy_arns}
        '''
        result = self._values.get("policy_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def policy_document(self) -> typing.Optional[builtins.str]:
        '''IAM policy the role should use in JSON format.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#policy_document AwsSecretBackendRole#policy_document}
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''ARNs of AWS roles allowed to be assumed. Only valid when credential_type is 'assumed_role'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#role_arns AwsSecretBackendRole#role_arns}
        '''
        result = self._values.get("role_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_path(self) -> typing.Optional[builtins.str]:
        '''The path for the user name. Valid only when credential_type is iam_user. Default is /.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/aws_secret_backend_role#user_path AwsSecretBackendRole#user_path}
        '''
        result = self._values.get("user_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsSecretBackendRoleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsSecretBackendRole",
    "AwsSecretBackendRoleConfig",
]

publication.publish()

def _typecheckingstub__663a3ea86009355c9c58a6ee0d6e1bdb7dc4885593381f5d5673c88c616c51be(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    backend: builtins.str,
    credential_type: builtins.str,
    name: builtins.str,
    default_sts_ttl: typing.Optional[jsii.Number] = None,
    iam_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    max_sts_ttl: typing.Optional[jsii.Number] = None,
    namespace: typing.Optional[builtins.str] = None,
    permissions_boundary_arn: typing.Optional[builtins.str] = None,
    policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    policy_document: typing.Optional[builtins.str] = None,
    role_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_path: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__8446b7e7024db391dd5852b45f7ddb55b190d8ad3805bb0c8791eaa775248d11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea6b12aa288744d0c63ba2c772fcbd9a315f485ca31a65b3e9536047e46b142(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ad7ed45a9d4d1ea52cb4e5aff8dcca28a6bd027de1ae85625fbafded8d2137(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d20bc2515ece10b3dff0a6ffa582f99fa4117bc847d336f037b925e6461beabb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec631ee33ed1abc4989762bb8f65db28737e7238529cf74e85124f0ac8657817(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c83025ff782d311a6bbee85d4dad4df9d35b6c00c8d092a3b058bd86d81beef(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d0a6e7d0cf817b65ed5033e5497dbf0288db37ef099a8fbff77d37612c9de62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d2136d094ad30954ae0876aace2c5fe6c60933ea96aa3c9f65c21e8f744489d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5040006dd9b1f3ab6c76da027c1320e4210363484c53d69c02ea1da9c4ff8550(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5269f9b8625105b04ebdc9ffc01c05112d1cc1bca521e6cdb0ef8ed7e6455937(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cab822a377c9ad5b0c2b06839cb75f5442f11feb2ba0a918663190eb81c2045(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf9ef81590bf704c788163c8f1468bb8e5ed5678c522067a4b81f8cd90fa4cc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50460f234bf337eb9887f1c1d9c43154d8a1de05232592e5408b53e0450c619(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8807b740994d46f071152460b10ed5176d10bbb157454d75b22602e9705a9cd9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    backend: builtins.str,
    credential_type: builtins.str,
    name: builtins.str,
    default_sts_ttl: typing.Optional[jsii.Number] = None,
    iam_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    max_sts_ttl: typing.Optional[jsii.Number] = None,
    namespace: typing.Optional[builtins.str] = None,
    permissions_boundary_arn: typing.Optional[builtins.str] = None,
    policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    policy_document: typing.Optional[builtins.str] = None,
    role_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
