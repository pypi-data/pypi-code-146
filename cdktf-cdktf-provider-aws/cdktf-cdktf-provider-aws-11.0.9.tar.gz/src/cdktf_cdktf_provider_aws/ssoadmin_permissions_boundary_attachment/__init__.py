'''
# `aws_ssoadmin_permissions_boundary_attachment`

Refer to the Terraform Registory for docs: [`aws_ssoadmin_permissions_boundary_attachment`](https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment).
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


class SsoadminPermissionsBoundaryAttachment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ssoadminPermissionsBoundaryAttachment.SsoadminPermissionsBoundaryAttachment",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment aws_ssoadmin_permissions_boundary_attachment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        instance_arn: builtins.str,
        permissions_boundary: typing.Union["SsoadminPermissionsBoundaryAttachmentPermissionsBoundary", typing.Dict[builtins.str, typing.Any]],
        permission_set_arn: builtins.str,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment aws_ssoadmin_permissions_boundary_attachment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param instance_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#instance_arn SsoadminPermissionsBoundaryAttachment#instance_arn}.
        :param permissions_boundary: permissions_boundary block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#permissions_boundary SsoadminPermissionsBoundaryAttachment#permissions_boundary}
        :param permission_set_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#permission_set_arn SsoadminPermissionsBoundaryAttachment#permission_set_arn}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#id SsoadminPermissionsBoundaryAttachment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__691371c5ef88500e127c5cc5a79194f4bdc3e4e1238a10d0160385977b89ab17)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SsoadminPermissionsBoundaryAttachmentConfig(
            instance_arn=instance_arn,
            permissions_boundary=permissions_boundary,
            permission_set_arn=permission_set_arn,
            id=id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putPermissionsBoundary")
    def put_permissions_boundary(
        self,
        *,
        customer_managed_policy_reference: typing.Optional[typing.Union["SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReference", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_policy_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param customer_managed_policy_reference: customer_managed_policy_reference block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#customer_managed_policy_reference SsoadminPermissionsBoundaryAttachment#customer_managed_policy_reference}
        :param managed_policy_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#managed_policy_arn SsoadminPermissionsBoundaryAttachment#managed_policy_arn}.
        '''
        value = SsoadminPermissionsBoundaryAttachmentPermissionsBoundary(
            customer_managed_policy_reference=customer_managed_policy_reference,
            managed_policy_arn=managed_policy_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putPermissionsBoundary", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundary")
    def permissions_boundary(
        self,
    ) -> "SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryOutputReference":
        return typing.cast("SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryOutputReference", jsii.get(self, "permissionsBoundary"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceArnInput")
    def instance_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundaryInput")
    def permissions_boundary_input(
        self,
    ) -> typing.Optional["SsoadminPermissionsBoundaryAttachmentPermissionsBoundary"]:
        return typing.cast(typing.Optional["SsoadminPermissionsBoundaryAttachmentPermissionsBoundary"], jsii.get(self, "permissionsBoundaryInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionSetArnInput")
    def permission_set_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionSetArnInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d331081768be4b60aabc4bd270423fafe010c813fe92252dae114755e1474b4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @instance_arn.setter
    def instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29c9b76d0160c3a98b92ac53a0313ab4b9741a6f596210939235d1e1561cea82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="permissionSetArn")
    def permission_set_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissionSetArn"))

    @permission_set_arn.setter
    def permission_set_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a76b02a09a341f2714a2891f5d8f28995b55eac0416211354a0b3d7e1821dd03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionSetArn", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ssoadminPermissionsBoundaryAttachment.SsoadminPermissionsBoundaryAttachmentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "instance_arn": "instanceArn",
        "permissions_boundary": "permissionsBoundary",
        "permission_set_arn": "permissionSetArn",
        "id": "id",
    },
)
class SsoadminPermissionsBoundaryAttachmentConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        instance_arn: builtins.str,
        permissions_boundary: typing.Union["SsoadminPermissionsBoundaryAttachmentPermissionsBoundary", typing.Dict[builtins.str, typing.Any]],
        permission_set_arn: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param instance_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#instance_arn SsoadminPermissionsBoundaryAttachment#instance_arn}.
        :param permissions_boundary: permissions_boundary block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#permissions_boundary SsoadminPermissionsBoundaryAttachment#permissions_boundary}
        :param permission_set_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#permission_set_arn SsoadminPermissionsBoundaryAttachment#permission_set_arn}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#id SsoadminPermissionsBoundaryAttachment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(permissions_boundary, dict):
            permissions_boundary = SsoadminPermissionsBoundaryAttachmentPermissionsBoundary(**permissions_boundary)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f45ca6307bac5931ff2dd689601d2a1121ac31ca352853b8dbf012750facd7d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument permission_set_arn", value=permission_set_arn, expected_type=type_hints["permission_set_arn"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_arn": instance_arn,
            "permissions_boundary": permissions_boundary,
            "permission_set_arn": permission_set_arn,
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
        if id is not None:
            self._values["id"] = id

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
    def instance_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#instance_arn SsoadminPermissionsBoundaryAttachment#instance_arn}.'''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def permissions_boundary(
        self,
    ) -> "SsoadminPermissionsBoundaryAttachmentPermissionsBoundary":
        '''permissions_boundary block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#permissions_boundary SsoadminPermissionsBoundaryAttachment#permissions_boundary}
        '''
        result = self._values.get("permissions_boundary")
        assert result is not None, "Required property 'permissions_boundary' is missing"
        return typing.cast("SsoadminPermissionsBoundaryAttachmentPermissionsBoundary", result)

    @builtins.property
    def permission_set_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#permission_set_arn SsoadminPermissionsBoundaryAttachment#permission_set_arn}.'''
        result = self._values.get("permission_set_arn")
        assert result is not None, "Required property 'permission_set_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#id SsoadminPermissionsBoundaryAttachment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsoadminPermissionsBoundaryAttachmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ssoadminPermissionsBoundaryAttachment.SsoadminPermissionsBoundaryAttachmentPermissionsBoundary",
    jsii_struct_bases=[],
    name_mapping={
        "customer_managed_policy_reference": "customerManagedPolicyReference",
        "managed_policy_arn": "managedPolicyArn",
    },
)
class SsoadminPermissionsBoundaryAttachmentPermissionsBoundary:
    def __init__(
        self,
        *,
        customer_managed_policy_reference: typing.Optional[typing.Union["SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReference", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_policy_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param customer_managed_policy_reference: customer_managed_policy_reference block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#customer_managed_policy_reference SsoadminPermissionsBoundaryAttachment#customer_managed_policy_reference}
        :param managed_policy_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#managed_policy_arn SsoadminPermissionsBoundaryAttachment#managed_policy_arn}.
        '''
        if isinstance(customer_managed_policy_reference, dict):
            customer_managed_policy_reference = SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReference(**customer_managed_policy_reference)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac00bf3c7c40a77b209943baa9746309cc2ba7ae38121f5f964ef26a46ab832)
            check_type(argname="argument customer_managed_policy_reference", value=customer_managed_policy_reference, expected_type=type_hints["customer_managed_policy_reference"])
            check_type(argname="argument managed_policy_arn", value=managed_policy_arn, expected_type=type_hints["managed_policy_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if customer_managed_policy_reference is not None:
            self._values["customer_managed_policy_reference"] = customer_managed_policy_reference
        if managed_policy_arn is not None:
            self._values["managed_policy_arn"] = managed_policy_arn

    @builtins.property
    def customer_managed_policy_reference(
        self,
    ) -> typing.Optional["SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReference"]:
        '''customer_managed_policy_reference block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#customer_managed_policy_reference SsoadminPermissionsBoundaryAttachment#customer_managed_policy_reference}
        '''
        result = self._values.get("customer_managed_policy_reference")
        return typing.cast(typing.Optional["SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReference"], result)

    @builtins.property
    def managed_policy_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#managed_policy_arn SsoadminPermissionsBoundaryAttachment#managed_policy_arn}.'''
        result = self._values.get("managed_policy_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsoadminPermissionsBoundaryAttachmentPermissionsBoundary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ssoadminPermissionsBoundaryAttachment.SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReference",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path"},
)
class SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReference:
    def __init__(
        self,
        *,
        name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#name SsoadminPermissionsBoundaryAttachment#name}.
        :param path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#path SsoadminPermissionsBoundaryAttachment#path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff299be6fa10b56f16c16ebdf9f8aa6a0b06feb9ae99c0fded7de4eff56894d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#name SsoadminPermissionsBoundaryAttachment#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#path SsoadminPermissionsBoundaryAttachment#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ssoadminPermissionsBoundaryAttachment.SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2a45b311c9df7db8c762467dae7f1bb262227c8b985843d2c94dae0dbfbccae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfab53d8b692ef6615214dc20729e2791f538703f4ef8da72c6257eb2fa657c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a9ed74a6c374f84977271d9aad753f87a7c8a5faa52607b9d4200d6e093e140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReference]:
        return typing.cast(typing.Optional[SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReference],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e8cb13e3cd8734d15e8c64e9c1c82894e6270e770097a3b88b72d4ea60ffa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ssoadminPermissionsBoundaryAttachment.SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c2083c139b58c81e683d6b38d6cdf0ad94f0435e2e8efc511e6a95ca1cd0074)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomerManagedPolicyReference")
    def put_customer_managed_policy_reference(
        self,
        *,
        name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#name SsoadminPermissionsBoundaryAttachment#name}.
        :param path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_permissions_boundary_attachment#path SsoadminPermissionsBoundaryAttachment#path}.
        '''
        value = SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReference(
            name=name, path=path
        )

        return typing.cast(None, jsii.invoke(self, "putCustomerManagedPolicyReference", [value]))

    @jsii.member(jsii_name="resetCustomerManagedPolicyReference")
    def reset_customer_managed_policy_reference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerManagedPolicyReference", []))

    @jsii.member(jsii_name="resetManagedPolicyArn")
    def reset_managed_policy_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedPolicyArn", []))

    @builtins.property
    @jsii.member(jsii_name="customerManagedPolicyReference")
    def customer_managed_policy_reference(
        self,
    ) -> SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReferenceOutputReference:
        return typing.cast(SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReferenceOutputReference, jsii.get(self, "customerManagedPolicyReference"))

    @builtins.property
    @jsii.member(jsii_name="customerManagedPolicyReferenceInput")
    def customer_managed_policy_reference_input(
        self,
    ) -> typing.Optional[SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReference]:
        return typing.cast(typing.Optional[SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReference], jsii.get(self, "customerManagedPolicyReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="managedPolicyArnInput")
    def managed_policy_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedPolicyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="managedPolicyArn")
    def managed_policy_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedPolicyArn"))

    @managed_policy_arn.setter
    def managed_policy_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efa5932e3d1eb5c3f0f9411a0e374b64294db65b07be415b6f82e3cb4bc29204)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedPolicyArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SsoadminPermissionsBoundaryAttachmentPermissionsBoundary]:
        return typing.cast(typing.Optional[SsoadminPermissionsBoundaryAttachmentPermissionsBoundary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SsoadminPermissionsBoundaryAttachmentPermissionsBoundary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b23c10ca7c6721147283bdda36a038ed203ded0b4a1d07bcdcd4cd6ae435e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "SsoadminPermissionsBoundaryAttachment",
    "SsoadminPermissionsBoundaryAttachmentConfig",
    "SsoadminPermissionsBoundaryAttachmentPermissionsBoundary",
    "SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReference",
    "SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReferenceOutputReference",
    "SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryOutputReference",
]

publication.publish()

def _typecheckingstub__691371c5ef88500e127c5cc5a79194f4bdc3e4e1238a10d0160385977b89ab17(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    instance_arn: builtins.str,
    permissions_boundary: typing.Union[SsoadminPermissionsBoundaryAttachmentPermissionsBoundary, typing.Dict[builtins.str, typing.Any]],
    permission_set_arn: builtins.str,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__d331081768be4b60aabc4bd270423fafe010c813fe92252dae114755e1474b4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c9b76d0160c3a98b92ac53a0313ab4b9741a6f596210939235d1e1561cea82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a76b02a09a341f2714a2891f5d8f28995b55eac0416211354a0b3d7e1821dd03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f45ca6307bac5931ff2dd689601d2a1121ac31ca352853b8dbf012750facd7d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_arn: builtins.str,
    permissions_boundary: typing.Union[SsoadminPermissionsBoundaryAttachmentPermissionsBoundary, typing.Dict[builtins.str, typing.Any]],
    permission_set_arn: builtins.str,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac00bf3c7c40a77b209943baa9746309cc2ba7ae38121f5f964ef26a46ab832(
    *,
    customer_managed_policy_reference: typing.Optional[typing.Union[SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReference, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_policy_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff299be6fa10b56f16c16ebdf9f8aa6a0b06feb9ae99c0fded7de4eff56894d(
    *,
    name: builtins.str,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a45b311c9df7db8c762467dae7f1bb262227c8b985843d2c94dae0dbfbccae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfab53d8b692ef6615214dc20729e2791f538703f4ef8da72c6257eb2fa657c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9ed74a6c374f84977271d9aad753f87a7c8a5faa52607b9d4200d6e093e140(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e8cb13e3cd8734d15e8c64e9c1c82894e6270e770097a3b88b72d4ea60ffa6(
    value: typing.Optional[SsoadminPermissionsBoundaryAttachmentPermissionsBoundaryCustomerManagedPolicyReference],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2083c139b58c81e683d6b38d6cdf0ad94f0435e2e8efc511e6a95ca1cd0074(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa5932e3d1eb5c3f0f9411a0e374b64294db65b07be415b6f82e3cb4bc29204(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b23c10ca7c6721147283bdda36a038ed203ded0b4a1d07bcdcd4cd6ae435e5(
    value: typing.Optional[SsoadminPermissionsBoundaryAttachmentPermissionsBoundary],
) -> None:
    """Type checking stubs"""
    pass
