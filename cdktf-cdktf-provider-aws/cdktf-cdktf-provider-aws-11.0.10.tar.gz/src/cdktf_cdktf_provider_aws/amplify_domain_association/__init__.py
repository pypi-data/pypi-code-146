'''
# `aws_amplify_domain_association`

Refer to the Terraform Registory for docs: [`aws_amplify_domain_association`](https://www.terraform.io/docs/providers/aws/r/amplify_domain_association).
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


class AmplifyDomainAssociation(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.amplifyDomainAssociation.AmplifyDomainAssociation",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association aws_amplify_domain_association}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        app_id: builtins.str,
        domain_name: builtins.str,
        sub_domain: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AmplifyDomainAssociationSubDomain", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        wait_for_verification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association aws_amplify_domain_association} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param app_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association#app_id AmplifyDomainAssociation#app_id}.
        :param domain_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association#domain_name AmplifyDomainAssociation#domain_name}.
        :param sub_domain: sub_domain block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association#sub_domain AmplifyDomainAssociation#sub_domain}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association#id AmplifyDomainAssociation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param wait_for_verification: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association#wait_for_verification AmplifyDomainAssociation#wait_for_verification}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc1bef3caee9441d258c328945cfea1099db8a30563e5dec043d4b656661f740)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AmplifyDomainAssociationConfig(
            app_id=app_id,
            domain_name=domain_name,
            sub_domain=sub_domain,
            id=id,
            wait_for_verification=wait_for_verification,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putSubDomain")
    def put_sub_domain(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AmplifyDomainAssociationSubDomain", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d637100b1c665d7278c13438a9fb32eba3b239df2492b9de83a99c2293c7ce0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSubDomain", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetWaitForVerification")
    def reset_wait_for_verification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWaitForVerification", []))

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
    @jsii.member(jsii_name="certificateVerificationDnsRecord")
    def certificate_verification_dns_record(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateVerificationDnsRecord"))

    @builtins.property
    @jsii.member(jsii_name="subDomain")
    def sub_domain(self) -> "AmplifyDomainAssociationSubDomainList":
        return typing.cast("AmplifyDomainAssociationSubDomainList", jsii.get(self, "subDomain"))

    @builtins.property
    @jsii.member(jsii_name="appIdInput")
    def app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appIdInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="subDomainInput")
    def sub_domain_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AmplifyDomainAssociationSubDomain"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AmplifyDomainAssociationSubDomain"]]], jsii.get(self, "subDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="waitForVerificationInput")
    def wait_for_verification_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "waitForVerificationInput"))

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appId"))

    @app_id.setter
    def app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac63ca8dc38102c7e9902430dbe3743b7e48d6b0fcb0fd413c1b14972c2eaf80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appId", value)

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86bc206cc747a48fcdb8f004fb6b85527017f854fd77471003e13d6cf86a6449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5658bbb4b0f5f47395aeb0845592838ed788df3624b70dcf158424413e82df8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="waitForVerification")
    def wait_for_verification(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "waitForVerification"))

    @wait_for_verification.setter
    def wait_for_verification(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ef2c3a7905ed2a227be7b5518b6e468dd4b696927a099b15e5d02f5b5b7252e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForVerification", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.amplifyDomainAssociation.AmplifyDomainAssociationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "app_id": "appId",
        "domain_name": "domainName",
        "sub_domain": "subDomain",
        "id": "id",
        "wait_for_verification": "waitForVerification",
    },
)
class AmplifyDomainAssociationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        app_id: builtins.str,
        domain_name: builtins.str,
        sub_domain: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AmplifyDomainAssociationSubDomain", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        wait_for_verification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param app_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association#app_id AmplifyDomainAssociation#app_id}.
        :param domain_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association#domain_name AmplifyDomainAssociation#domain_name}.
        :param sub_domain: sub_domain block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association#sub_domain AmplifyDomainAssociation#sub_domain}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association#id AmplifyDomainAssociation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param wait_for_verification: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association#wait_for_verification AmplifyDomainAssociation#wait_for_verification}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c56f14e9bec6f2e0e37c0a7f31c2146373bf2f7d5b9deda5e21dba1b3234dc3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument sub_domain", value=sub_domain, expected_type=type_hints["sub_domain"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument wait_for_verification", value=wait_for_verification, expected_type=type_hints["wait_for_verification"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_id": app_id,
            "domain_name": domain_name,
            "sub_domain": sub_domain,
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
        if wait_for_verification is not None:
            self._values["wait_for_verification"] = wait_for_verification

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
    def app_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association#app_id AmplifyDomainAssociation#app_id}.'''
        result = self._values.get("app_id")
        assert result is not None, "Required property 'app_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association#domain_name AmplifyDomainAssociation#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sub_domain(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AmplifyDomainAssociationSubDomain"]]:
        '''sub_domain block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association#sub_domain AmplifyDomainAssociation#sub_domain}
        '''
        result = self._values.get("sub_domain")
        assert result is not None, "Required property 'sub_domain' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AmplifyDomainAssociationSubDomain"]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association#id AmplifyDomainAssociation#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wait_for_verification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association#wait_for_verification AmplifyDomainAssociation#wait_for_verification}.'''
        result = self._values.get("wait_for_verification")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AmplifyDomainAssociationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.amplifyDomainAssociation.AmplifyDomainAssociationSubDomain",
    jsii_struct_bases=[],
    name_mapping={"branch_name": "branchName", "prefix": "prefix"},
)
class AmplifyDomainAssociationSubDomain:
    def __init__(self, *, branch_name: builtins.str, prefix: builtins.str) -> None:
        '''
        :param branch_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association#branch_name AmplifyDomainAssociation#branch_name}.
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association#prefix AmplifyDomainAssociation#prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3abbc2fbfe5b6baecf822996d8a1a34ad0f1ed5084f3c277dcf5db0b1166600d)
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "branch_name": branch_name,
            "prefix": prefix,
        }

    @builtins.property
    def branch_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association#branch_name AmplifyDomainAssociation#branch_name}.'''
        result = self._values.get("branch_name")
        assert result is not None, "Required property 'branch_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/amplify_domain_association#prefix AmplifyDomainAssociation#prefix}.'''
        result = self._values.get("prefix")
        assert result is not None, "Required property 'prefix' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AmplifyDomainAssociationSubDomain(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AmplifyDomainAssociationSubDomainList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.amplifyDomainAssociation.AmplifyDomainAssociationSubDomainList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51e7851ee7765a44d3a811cb1517dc984e345e1f151eb219457d7814e20b4b3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AmplifyDomainAssociationSubDomainOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f33b0e9e8e647d8931f0beaac80e3219b968fcef8e705df4c2766b40df8caef7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AmplifyDomainAssociationSubDomainOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe54f3b858d036c00153038d2a4469ca2d55bdf4ae845703bf4c1708aca9b07c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57919b544a0333dd7c791658a6dff057411ccab254a9b6e6d4698e65efd0580f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b94f5ae245c88dbfcabda563ba1a1979e2c2cca860c9f299d67fd810ae231adf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AmplifyDomainAssociationSubDomain]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AmplifyDomainAssociationSubDomain]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AmplifyDomainAssociationSubDomain]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9beaabb52b71261ed1f35fed5aee4697a365f36a4d08f40455749f5d619740ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AmplifyDomainAssociationSubDomainOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.amplifyDomainAssociation.AmplifyDomainAssociationSubDomainOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__809333b9d9a0676370f34599cbdd8a83d0b6b99f7238b9568338a1cd424b5eb0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dnsRecord")
    def dns_record(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsRecord"))

    @builtins.property
    @jsii.member(jsii_name="verified")
    def verified(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "verified"))

    @builtins.property
    @jsii.member(jsii_name="branchNameInput")
    def branch_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchNameInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branchName"))

    @branch_name.setter
    def branch_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dfd791eb7be71ce45d848096544d09d0c94902ddae79739e3d631ca62fd9765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branchName", value)

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7c556e3b7526ae1373ead02ec30f58b809a794c41b118b63f1a99eb9d5f2835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AmplifyDomainAssociationSubDomain, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AmplifyDomainAssociationSubDomain, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AmplifyDomainAssociationSubDomain, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c97d8e44d45110a7beff46701d71fa31d6780cf9588211f284d9c8a4f374c18d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "AmplifyDomainAssociation",
    "AmplifyDomainAssociationConfig",
    "AmplifyDomainAssociationSubDomain",
    "AmplifyDomainAssociationSubDomainList",
    "AmplifyDomainAssociationSubDomainOutputReference",
]

publication.publish()

def _typecheckingstub__cc1bef3caee9441d258c328945cfea1099db8a30563e5dec043d4b656661f740(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    app_id: builtins.str,
    domain_name: builtins.str,
    sub_domain: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AmplifyDomainAssociationSubDomain, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    wait_for_verification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__d637100b1c665d7278c13438a9fb32eba3b239df2492b9de83a99c2293c7ce0a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AmplifyDomainAssociationSubDomain, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac63ca8dc38102c7e9902430dbe3743b7e48d6b0fcb0fd413c1b14972c2eaf80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86bc206cc747a48fcdb8f004fb6b85527017f854fd77471003e13d6cf86a6449(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5658bbb4b0f5f47395aeb0845592838ed788df3624b70dcf158424413e82df8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef2c3a7905ed2a227be7b5518b6e468dd4b696927a099b15e5d02f5b5b7252e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c56f14e9bec6f2e0e37c0a7f31c2146373bf2f7d5b9deda5e21dba1b3234dc3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    app_id: builtins.str,
    domain_name: builtins.str,
    sub_domain: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AmplifyDomainAssociationSubDomain, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    wait_for_verification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3abbc2fbfe5b6baecf822996d8a1a34ad0f1ed5084f3c277dcf5db0b1166600d(
    *,
    branch_name: builtins.str,
    prefix: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e7851ee7765a44d3a811cb1517dc984e345e1f151eb219457d7814e20b4b3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f33b0e9e8e647d8931f0beaac80e3219b968fcef8e705df4c2766b40df8caef7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe54f3b858d036c00153038d2a4469ca2d55bdf4ae845703bf4c1708aca9b07c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57919b544a0333dd7c791658a6dff057411ccab254a9b6e6d4698e65efd0580f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b94f5ae245c88dbfcabda563ba1a1979e2c2cca860c9f299d67fd810ae231adf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9beaabb52b71261ed1f35fed5aee4697a365f36a4d08f40455749f5d619740ec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AmplifyDomainAssociationSubDomain]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809333b9d9a0676370f34599cbdd8a83d0b6b99f7238b9568338a1cd424b5eb0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dfd791eb7be71ce45d848096544d09d0c94902ddae79739e3d631ca62fd9765(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c556e3b7526ae1373ead02ec30f58b809a794c41b118b63f1a99eb9d5f2835(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c97d8e44d45110a7beff46701d71fa31d6780cf9588211f284d9c8a4f374c18d(
    value: typing.Optional[typing.Union[AmplifyDomainAssociationSubDomain, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
