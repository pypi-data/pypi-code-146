'''
# `aws_redshift_security_group`

Refer to the Terraform Registory for docs: [`aws_redshift_security_group`](https://www.terraform.io/docs/providers/aws/r/redshift_security_group).
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


class RedshiftSecurityGroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.redshiftSecurityGroup.RedshiftSecurityGroup",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/redshift_security_group aws_redshift_security_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        ingress: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedshiftSecurityGroupIngress", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/redshift_security_group aws_redshift_security_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param ingress: ingress block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/redshift_security_group#ingress RedshiftSecurityGroup#ingress}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/redshift_security_group#name RedshiftSecurityGroup#name}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/redshift_security_group#description RedshiftSecurityGroup#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/redshift_security_group#id RedshiftSecurityGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c457e612d5ea3fe73ae9ab71a10af77b0d9d0c157cba371bf2a30e9b20ddf72)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RedshiftSecurityGroupConfig(
            ingress=ingress,
            name=name,
            description=description,
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

    @jsii.member(jsii_name="putIngress")
    def put_ingress(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedshiftSecurityGroupIngress", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0376916717c640eaaa0f4a23ff895dd4647131ff02c5a0d4bf2d0ff1ad27c9a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIngress", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

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
    @jsii.member(jsii_name="ingress")
    def ingress(self) -> "RedshiftSecurityGroupIngressList":
        return typing.cast("RedshiftSecurityGroupIngressList", jsii.get(self, "ingress"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressInput")
    def ingress_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftSecurityGroupIngress"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftSecurityGroupIngress"]]], jsii.get(self, "ingressInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__064384eb03f193837e577f692388be76f10e69f5e6487f0f8e2279daffdc5358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0a61ba26dfed49814be56911830a66f08f7cdc6d72305745c3820e4acc37301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__844649932449ce5c3a14c11d62e8b98cb16643c9833f48e16496332ad3b96826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.redshiftSecurityGroup.RedshiftSecurityGroupConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "ingress": "ingress",
        "name": "name",
        "description": "description",
        "id": "id",
    },
)
class RedshiftSecurityGroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        ingress: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedshiftSecurityGroupIngress", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
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
        :param ingress: ingress block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/redshift_security_group#ingress RedshiftSecurityGroup#ingress}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/redshift_security_group#name RedshiftSecurityGroup#name}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/redshift_security_group#description RedshiftSecurityGroup#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/redshift_security_group#id RedshiftSecurityGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d81a433b70c19f748fb4ffc6cdabeb9b62356e3f6003751a234cbf92854555e0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument ingress", value=ingress, expected_type=type_hints["ingress"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ingress": ingress,
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
        if description is not None:
            self._values["description"] = description
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
    def ingress(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftSecurityGroupIngress"]]:
        '''ingress block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/redshift_security_group#ingress RedshiftSecurityGroup#ingress}
        '''
        result = self._values.get("ingress")
        assert result is not None, "Required property 'ingress' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftSecurityGroupIngress"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/redshift_security_group#name RedshiftSecurityGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/redshift_security_group#description RedshiftSecurityGroup#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/redshift_security_group#id RedshiftSecurityGroup#id}.

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
        return "RedshiftSecurityGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.redshiftSecurityGroup.RedshiftSecurityGroupIngress",
    jsii_struct_bases=[],
    name_mapping={
        "cidr": "cidr",
        "security_group_name": "securityGroupName",
        "security_group_owner_id": "securityGroupOwnerId",
    },
)
class RedshiftSecurityGroupIngress:
    def __init__(
        self,
        *,
        cidr: typing.Optional[builtins.str] = None,
        security_group_name: typing.Optional[builtins.str] = None,
        security_group_owner_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cidr: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/redshift_security_group#cidr RedshiftSecurityGroup#cidr}.
        :param security_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/redshift_security_group#security_group_name RedshiftSecurityGroup#security_group_name}.
        :param security_group_owner_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/redshift_security_group#security_group_owner_id RedshiftSecurityGroup#security_group_owner_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef106117c6208fc1fe8b2bd607204a7031831d6adb200f86258326eb195e48f6)
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument security_group_name", value=security_group_name, expected_type=type_hints["security_group_name"])
            check_type(argname="argument security_group_owner_id", value=security_group_owner_id, expected_type=type_hints["security_group_owner_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cidr is not None:
            self._values["cidr"] = cidr
        if security_group_name is not None:
            self._values["security_group_name"] = security_group_name
        if security_group_owner_id is not None:
            self._values["security_group_owner_id"] = security_group_owner_id

    @builtins.property
    def cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/redshift_security_group#cidr RedshiftSecurityGroup#cidr}.'''
        result = self._values.get("cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/redshift_security_group#security_group_name RedshiftSecurityGroup#security_group_name}.'''
        result = self._values.get("security_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_owner_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/redshift_security_group#security_group_owner_id RedshiftSecurityGroup#security_group_owner_id}.'''
        result = self._values.get("security_group_owner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedshiftSecurityGroupIngress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedshiftSecurityGroupIngressList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.redshiftSecurityGroup.RedshiftSecurityGroupIngressList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d03b297f7b5573beee258dce816eaf693c7ca57d330d72100bd3b2bd031ea7d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RedshiftSecurityGroupIngressOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ccc35141575d7195930959bfebcb46a6a23230216502494c7ec54eef6768f3b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedshiftSecurityGroupIngressOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bcd1cbe7c55e5a70f1a4a1d0192b0cfcf9e4cdb7536af34b7563ff9a772005a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8a9b01f66aa47e6dffa84d980bc3a0742b25de79c7865e5c1ed1bb52e97eef7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd3fbc3e8d4ea3c9d38c5e7eb454fc962cf5a399686aec95273d5489f7217366)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftSecurityGroupIngress]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftSecurityGroupIngress]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftSecurityGroupIngress]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__848dde5041cecb910001a9ac8ef55aa6ab22ad38019d87e1b174adc5a8ac6c46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class RedshiftSecurityGroupIngressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.redshiftSecurityGroup.RedshiftSecurityGroupIngressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c99002e3b8413a4e9f5fd57089913bbaaaec956e39f6e4ed31fc3fbedffbdf04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCidr")
    def reset_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCidr", []))

    @jsii.member(jsii_name="resetSecurityGroupName")
    def reset_security_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupName", []))

    @jsii.member(jsii_name="resetSecurityGroupOwnerId")
    def reset_security_group_owner_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupOwnerId", []))

    @builtins.property
    @jsii.member(jsii_name="cidrInput")
    def cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cidrInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupNameInput")
    def security_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupOwnerIdInput")
    def security_group_owner_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityGroupOwnerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cidr"))

    @cidr.setter
    def cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20a8e0a5992ba7d28938679b5e67b14ce59d4bc4c479030d57bb94cff5218363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cidr", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupName")
    def security_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupName"))

    @security_group_name.setter
    def security_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c293b42193463d60465a676f5ef429c11c7d437ea0ccddbbfad4b43ee02af5c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupOwnerId")
    def security_group_owner_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupOwnerId"))

    @security_group_owner_id.setter
    def security_group_owner_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94bc63f085395fa6f9b501a2ef71951c2bc3b3a2f6053a8b2a9964d0772bb853)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupOwnerId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[RedshiftSecurityGroupIngress, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[RedshiftSecurityGroupIngress, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[RedshiftSecurityGroupIngress, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e7800945b0d2980dc50be83444c5605b057ae94c73bdddcb356042a43cf44ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "RedshiftSecurityGroup",
    "RedshiftSecurityGroupConfig",
    "RedshiftSecurityGroupIngress",
    "RedshiftSecurityGroupIngressList",
    "RedshiftSecurityGroupIngressOutputReference",
]

publication.publish()

def _typecheckingstub__7c457e612d5ea3fe73ae9ab71a10af77b0d9d0c157cba371bf2a30e9b20ddf72(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    ingress: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftSecurityGroupIngress, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__0376916717c640eaaa0f4a23ff895dd4647131ff02c5a0d4bf2d0ff1ad27c9a3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftSecurityGroupIngress, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__064384eb03f193837e577f692388be76f10e69f5e6487f0f8e2279daffdc5358(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0a61ba26dfed49814be56911830a66f08f7cdc6d72305745c3820e4acc37301(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844649932449ce5c3a14c11d62e8b98cb16643c9833f48e16496332ad3b96826(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d81a433b70c19f748fb4ffc6cdabeb9b62356e3f6003751a234cbf92854555e0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ingress: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftSecurityGroupIngress, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef106117c6208fc1fe8b2bd607204a7031831d6adb200f86258326eb195e48f6(
    *,
    cidr: typing.Optional[builtins.str] = None,
    security_group_name: typing.Optional[builtins.str] = None,
    security_group_owner_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d03b297f7b5573beee258dce816eaf693c7ca57d330d72100bd3b2bd031ea7d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ccc35141575d7195930959bfebcb46a6a23230216502494c7ec54eef6768f3b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bcd1cbe7c55e5a70f1a4a1d0192b0cfcf9e4cdb7536af34b7563ff9a772005a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a9b01f66aa47e6dffa84d980bc3a0742b25de79c7865e5c1ed1bb52e97eef7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd3fbc3e8d4ea3c9d38c5e7eb454fc962cf5a399686aec95273d5489f7217366(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__848dde5041cecb910001a9ac8ef55aa6ab22ad38019d87e1b174adc5a8ac6c46(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftSecurityGroupIngress]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c99002e3b8413a4e9f5fd57089913bbaaaec956e39f6e4ed31fc3fbedffbdf04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a8e0a5992ba7d28938679b5e67b14ce59d4bc4c479030d57bb94cff5218363(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c293b42193463d60465a676f5ef429c11c7d437ea0ccddbbfad4b43ee02af5c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94bc63f085395fa6f9b501a2ef71951c2bc3b3a2f6053a8b2a9964d0772bb853(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7800945b0d2980dc50be83444c5605b057ae94c73bdddcb356042a43cf44ec(
    value: typing.Optional[typing.Union[RedshiftSecurityGroupIngress, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
