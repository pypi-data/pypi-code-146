'''
# `aws_ssoadmin_customer_managed_policy_attachment`

Refer to the Terraform Registory for docs: [`aws_ssoadmin_customer_managed_policy_attachment`](https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment).
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


class SsoadminCustomerManagedPolicyAttachment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ssoadminCustomerManagedPolicyAttachment.SsoadminCustomerManagedPolicyAttachment",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment aws_ssoadmin_customer_managed_policy_attachment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        customer_managed_policy_reference: typing.Union["SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReference", typing.Dict[builtins.str, typing.Any]],
        instance_arn: builtins.str,
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
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment aws_ssoadmin_customer_managed_policy_attachment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param customer_managed_policy_reference: customer_managed_policy_reference block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment#customer_managed_policy_reference SsoadminCustomerManagedPolicyAttachment#customer_managed_policy_reference}
        :param instance_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment#instance_arn SsoadminCustomerManagedPolicyAttachment#instance_arn}.
        :param permission_set_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment#permission_set_arn SsoadminCustomerManagedPolicyAttachment#permission_set_arn}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment#id SsoadminCustomerManagedPolicyAttachment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__103c15635b620a58aeae6c6e6992f6380ca9be7f1f853c906b1aa1b83ac97cf7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SsoadminCustomerManagedPolicyAttachmentConfig(
            customer_managed_policy_reference=customer_managed_policy_reference,
            instance_arn=instance_arn,
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

    @jsii.member(jsii_name="putCustomerManagedPolicyReference")
    def put_customer_managed_policy_reference(
        self,
        *,
        name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment#name SsoadminCustomerManagedPolicyAttachment#name}.
        :param path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment#path SsoadminCustomerManagedPolicyAttachment#path}.
        '''
        value = SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReference(
            name=name, path=path
        )

        return typing.cast(None, jsii.invoke(self, "putCustomerManagedPolicyReference", [value]))

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
    @jsii.member(jsii_name="customerManagedPolicyReference")
    def customer_managed_policy_reference(
        self,
    ) -> "SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReferenceOutputReference":
        return typing.cast("SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReferenceOutputReference", jsii.get(self, "customerManagedPolicyReference"))

    @builtins.property
    @jsii.member(jsii_name="customerManagedPolicyReferenceInput")
    def customer_managed_policy_reference_input(
        self,
    ) -> typing.Optional["SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReference"]:
        return typing.cast(typing.Optional["SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReference"], jsii.get(self, "customerManagedPolicyReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceArnInput")
    def instance_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceArnInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__12a2b25110f2c5a585e2478ce55f4d7162fd00482dd728bb1e761ba5a74def2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @instance_arn.setter
    def instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2437653be8fbf781f33181604bb263d857a5e0bffdeabeea8a5c8a4b05acf055)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="permissionSetArn")
    def permission_set_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissionSetArn"))

    @permission_set_arn.setter
    def permission_set_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__342da0d3bc77c2355b44352f10718eea3e100271bf9fd46badcfbfc63cd21b77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionSetArn", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ssoadminCustomerManagedPolicyAttachment.SsoadminCustomerManagedPolicyAttachmentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "customer_managed_policy_reference": "customerManagedPolicyReference",
        "instance_arn": "instanceArn",
        "permission_set_arn": "permissionSetArn",
        "id": "id",
    },
)
class SsoadminCustomerManagedPolicyAttachmentConfig(
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
        customer_managed_policy_reference: typing.Union["SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReference", typing.Dict[builtins.str, typing.Any]],
        instance_arn: builtins.str,
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
        :param customer_managed_policy_reference: customer_managed_policy_reference block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment#customer_managed_policy_reference SsoadminCustomerManagedPolicyAttachment#customer_managed_policy_reference}
        :param instance_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment#instance_arn SsoadminCustomerManagedPolicyAttachment#instance_arn}.
        :param permission_set_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment#permission_set_arn SsoadminCustomerManagedPolicyAttachment#permission_set_arn}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment#id SsoadminCustomerManagedPolicyAttachment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(customer_managed_policy_reference, dict):
            customer_managed_policy_reference = SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReference(**customer_managed_policy_reference)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abeb1a2641070670a956a12cb964adee236b562871841b843cbeca5e2d16589a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument customer_managed_policy_reference", value=customer_managed_policy_reference, expected_type=type_hints["customer_managed_policy_reference"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument permission_set_arn", value=permission_set_arn, expected_type=type_hints["permission_set_arn"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "customer_managed_policy_reference": customer_managed_policy_reference,
            "instance_arn": instance_arn,
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
    def customer_managed_policy_reference(
        self,
    ) -> "SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReference":
        '''customer_managed_policy_reference block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment#customer_managed_policy_reference SsoadminCustomerManagedPolicyAttachment#customer_managed_policy_reference}
        '''
        result = self._values.get("customer_managed_policy_reference")
        assert result is not None, "Required property 'customer_managed_policy_reference' is missing"
        return typing.cast("SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReference", result)

    @builtins.property
    def instance_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment#instance_arn SsoadminCustomerManagedPolicyAttachment#instance_arn}.'''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def permission_set_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment#permission_set_arn SsoadminCustomerManagedPolicyAttachment#permission_set_arn}.'''
        result = self._values.get("permission_set_arn")
        assert result is not None, "Required property 'permission_set_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment#id SsoadminCustomerManagedPolicyAttachment#id}.

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
        return "SsoadminCustomerManagedPolicyAttachmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ssoadminCustomerManagedPolicyAttachment.SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReference",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path"},
)
class SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReference:
    def __init__(
        self,
        *,
        name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment#name SsoadminCustomerManagedPolicyAttachment#name}.
        :param path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment#path SsoadminCustomerManagedPolicyAttachment#path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__169b9e92d4a9d97cf84c626b927144360c567a589bc68c5d65d54be4e8d315cd)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment#name SsoadminCustomerManagedPolicyAttachment#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ssoadmin_customer_managed_policy_attachment#path SsoadminCustomerManagedPolicyAttachment#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ssoadminCustomerManagedPolicyAttachment.SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22324524f48e634cfc8ae6388e50d2276f42d9031908718c36f6c875d3dcccaa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1dc3a91e551949cbcc75e62ba5b46e1a6d10533aa150218747a4687d295f61b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5108552d09d7ee0be80145603dad1ed8ea84af3beb27160dad34772d9e957367)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReference]:
        return typing.cast(typing.Optional[SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReference],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f2d6e3767353a2cbd4b7235e462740a9ca4f4ae1c9f53c54347c0151d79a28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "SsoadminCustomerManagedPolicyAttachment",
    "SsoadminCustomerManagedPolicyAttachmentConfig",
    "SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReference",
    "SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReferenceOutputReference",
]

publication.publish()

def _typecheckingstub__103c15635b620a58aeae6c6e6992f6380ca9be7f1f853c906b1aa1b83ac97cf7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    customer_managed_policy_reference: typing.Union[SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReference, typing.Dict[builtins.str, typing.Any]],
    instance_arn: builtins.str,
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

def _typecheckingstub__12a2b25110f2c5a585e2478ce55f4d7162fd00482dd728bb1e761ba5a74def2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2437653be8fbf781f33181604bb263d857a5e0bffdeabeea8a5c8a4b05acf055(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342da0d3bc77c2355b44352f10718eea3e100271bf9fd46badcfbfc63cd21b77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abeb1a2641070670a956a12cb964adee236b562871841b843cbeca5e2d16589a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    customer_managed_policy_reference: typing.Union[SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReference, typing.Dict[builtins.str, typing.Any]],
    instance_arn: builtins.str,
    permission_set_arn: builtins.str,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__169b9e92d4a9d97cf84c626b927144360c567a589bc68c5d65d54be4e8d315cd(
    *,
    name: builtins.str,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22324524f48e634cfc8ae6388e50d2276f42d9031908718c36f6c875d3dcccaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1dc3a91e551949cbcc75e62ba5b46e1a6d10533aa150218747a4687d295f61b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5108552d09d7ee0be80145603dad1ed8ea84af3beb27160dad34772d9e957367(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f2d6e3767353a2cbd4b7235e462740a9ca4f4ae1c9f53c54347c0151d79a28(
    value: typing.Optional[SsoadminCustomerManagedPolicyAttachmentCustomerManagedPolicyReference],
) -> None:
    """Type checking stubs"""
    pass
