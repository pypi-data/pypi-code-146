'''
# `data_aws_resourcegroupstaggingapi_resources`

Refer to the Terraform Registory for docs: [`data_aws_resourcegroupstaggingapi_resources`](https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources).
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


class DataAwsResourcegroupstaggingapiResources(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsResourcegroupstaggingapiResources.DataAwsResourcegroupstaggingapiResources",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources aws_resourcegroupstaggingapi_resources}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        exclude_compliant_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        include_compliance_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        resource_arn_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_type_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataAwsResourcegroupstaggingapiResourcesTagFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources aws_resourcegroupstaggingapi_resources} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param exclude_compliant_resources: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#exclude_compliant_resources DataAwsResourcegroupstaggingapiResources#exclude_compliant_resources}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#id DataAwsResourcegroupstaggingapiResources#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_compliance_details: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#include_compliance_details DataAwsResourcegroupstaggingapiResources#include_compliance_details}.
        :param resource_arn_list: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#resource_arn_list DataAwsResourcegroupstaggingapiResources#resource_arn_list}.
        :param resource_type_filters: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#resource_type_filters DataAwsResourcegroupstaggingapiResources#resource_type_filters}.
        :param tag_filter: tag_filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#tag_filter DataAwsResourcegroupstaggingapiResources#tag_filter}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__379a0a56e3c395a2c0b10c3907d12e97b93e09cefb56ca213ea912eb2f3f02b0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataAwsResourcegroupstaggingapiResourcesConfig(
            exclude_compliant_resources=exclude_compliant_resources,
            id=id,
            include_compliance_details=include_compliance_details,
            resource_arn_list=resource_arn_list,
            resource_type_filters=resource_type_filters,
            tag_filter=tag_filter,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putTagFilter")
    def put_tag_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataAwsResourcegroupstaggingapiResourcesTagFilter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__459110b412e197ff0de2649b6bcac46a80213d75ce721d1c524c72150766271b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTagFilter", [value]))

    @jsii.member(jsii_name="resetExcludeCompliantResources")
    def reset_exclude_compliant_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeCompliantResources", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIncludeComplianceDetails")
    def reset_include_compliance_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeComplianceDetails", []))

    @jsii.member(jsii_name="resetResourceArnList")
    def reset_resource_arn_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceArnList", []))

    @jsii.member(jsii_name="resetResourceTypeFilters")
    def reset_resource_type_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTypeFilters", []))

    @jsii.member(jsii_name="resetTagFilter")
    def reset_tag_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagFilter", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="resourceTagMappingList")
    def resource_tag_mapping_list(
        self,
    ) -> "DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListList":
        return typing.cast("DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListList", jsii.get(self, "resourceTagMappingList"))

    @builtins.property
    @jsii.member(jsii_name="tagFilter")
    def tag_filter(self) -> "DataAwsResourcegroupstaggingapiResourcesTagFilterList":
        return typing.cast("DataAwsResourcegroupstaggingapiResourcesTagFilterList", jsii.get(self, "tagFilter"))

    @builtins.property
    @jsii.member(jsii_name="excludeCompliantResourcesInput")
    def exclude_compliant_resources_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "excludeCompliantResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includeComplianceDetailsInput")
    def include_compliance_details_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeComplianceDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceArnListInput")
    def resource_arn_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceArnListInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeFiltersInput")
    def resource_type_filters_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceTypeFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="tagFilterInput")
    def tag_filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsResourcegroupstaggingapiResourcesTagFilter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsResourcegroupstaggingapiResourcesTagFilter"]]], jsii.get(self, "tagFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeCompliantResources")
    def exclude_compliant_resources(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "excludeCompliantResources"))

    @exclude_compliant_resources.setter
    def exclude_compliant_resources(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a602e767b6b8c345ad529b4de7804da7fc26fc390a27bbab32b5dd34e0927283)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeCompliantResources", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccb7e6a17937722a8fbf3f8926ff9063dfc8ccea7a4b5185e90c28113b4cde4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="includeComplianceDetails")
    def include_compliance_details(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeComplianceDetails"))

    @include_compliance_details.setter
    def include_compliance_details(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89fce751b5d60d0ad8164b02b7d36f9e244cde4f2c63255278868422efac3693)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeComplianceDetails", value)

    @builtins.property
    @jsii.member(jsii_name="resourceArnList")
    def resource_arn_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceArnList"))

    @resource_arn_list.setter
    def resource_arn_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89692354778d82575b7d2f9708fe56a06d0a625e6ccac1c62d3c2fc8608a4f24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArnList", value)

    @builtins.property
    @jsii.member(jsii_name="resourceTypeFilters")
    def resource_type_filters(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypeFilters"))

    @resource_type_filters.setter
    def resource_type_filters(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__154bc8e387716a6fd93c2229dd31b704e04607ec41e75d1ec72a1fbaefe8108c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypeFilters", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsResourcegroupstaggingapiResources.DataAwsResourcegroupstaggingapiResourcesConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "exclude_compliant_resources": "excludeCompliantResources",
        "id": "id",
        "include_compliance_details": "includeComplianceDetails",
        "resource_arn_list": "resourceArnList",
        "resource_type_filters": "resourceTypeFilters",
        "tag_filter": "tagFilter",
    },
)
class DataAwsResourcegroupstaggingapiResourcesConfig(
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
        exclude_compliant_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        include_compliance_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        resource_arn_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_type_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataAwsResourcegroupstaggingapiResourcesTagFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param exclude_compliant_resources: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#exclude_compliant_resources DataAwsResourcegroupstaggingapiResources#exclude_compliant_resources}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#id DataAwsResourcegroupstaggingapiResources#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_compliance_details: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#include_compliance_details DataAwsResourcegroupstaggingapiResources#include_compliance_details}.
        :param resource_arn_list: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#resource_arn_list DataAwsResourcegroupstaggingapiResources#resource_arn_list}.
        :param resource_type_filters: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#resource_type_filters DataAwsResourcegroupstaggingapiResources#resource_type_filters}.
        :param tag_filter: tag_filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#tag_filter DataAwsResourcegroupstaggingapiResources#tag_filter}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb87dae7972e41450dd18fbb52c3c5922ed174f7092e1ccceea839dea927ce2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument exclude_compliant_resources", value=exclude_compliant_resources, expected_type=type_hints["exclude_compliant_resources"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument include_compliance_details", value=include_compliance_details, expected_type=type_hints["include_compliance_details"])
            check_type(argname="argument resource_arn_list", value=resource_arn_list, expected_type=type_hints["resource_arn_list"])
            check_type(argname="argument resource_type_filters", value=resource_type_filters, expected_type=type_hints["resource_type_filters"])
            check_type(argname="argument tag_filter", value=tag_filter, expected_type=type_hints["tag_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if exclude_compliant_resources is not None:
            self._values["exclude_compliant_resources"] = exclude_compliant_resources
        if id is not None:
            self._values["id"] = id
        if include_compliance_details is not None:
            self._values["include_compliance_details"] = include_compliance_details
        if resource_arn_list is not None:
            self._values["resource_arn_list"] = resource_arn_list
        if resource_type_filters is not None:
            self._values["resource_type_filters"] = resource_type_filters
        if tag_filter is not None:
            self._values["tag_filter"] = tag_filter

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
    def exclude_compliant_resources(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#exclude_compliant_resources DataAwsResourcegroupstaggingapiResources#exclude_compliant_resources}.'''
        result = self._values.get("exclude_compliant_resources")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#id DataAwsResourcegroupstaggingapiResources#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_compliance_details(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#include_compliance_details DataAwsResourcegroupstaggingapiResources#include_compliance_details}.'''
        result = self._values.get("include_compliance_details")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def resource_arn_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#resource_arn_list DataAwsResourcegroupstaggingapiResources#resource_arn_list}.'''
        result = self._values.get("resource_arn_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_type_filters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#resource_type_filters DataAwsResourcegroupstaggingapiResources#resource_type_filters}.'''
        result = self._values.get("resource_type_filters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag_filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsResourcegroupstaggingapiResourcesTagFilter"]]]:
        '''tag_filter block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#tag_filter DataAwsResourcegroupstaggingapiResources#tag_filter}
        '''
        result = self._values.get("tag_filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsResourcegroupstaggingapiResourcesTagFilter"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsResourcegroupstaggingapiResourcesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsResourcegroupstaggingapiResources.DataAwsResourcegroupstaggingapiResourcesResourceTagMappingList",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAwsResourcegroupstaggingapiResourcesResourceTagMappingList:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsResourcegroupstaggingapiResourcesResourceTagMappingList(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsResourcegroupstaggingapiResources.DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListComplianceDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListComplianceDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListComplianceDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListComplianceDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsResourcegroupstaggingapiResources.DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListComplianceDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2ff2d46eaf3e39beca75af28dc7e8641d1ddd188088eb5804bc29e383151eb2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListComplianceDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c68c453d933b70f5dac55b26724dabc7816b972a4956ebce33b70cfcaab4da2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListComplianceDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c12c573b69e4f215907cf070e4775b58071310a10a4751e19473be77880dc2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2f78983fcb35155b9de5797c14b25b6402374ffd84cc03e8fb22cd122d9c83b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6f0a65604710e5e1bdfd79c91ecc12749c197a5c5333d958a99e146a05af6f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListComplianceDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsResourcegroupstaggingapiResources.DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListComplianceDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1b07d6e93339305f3f21b0aeb281cea246942346992fc036227fd532c9d2f82)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="complianceStatus")
    def compliance_status(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "complianceStatus"))

    @builtins.property
    @jsii.member(jsii_name="keysWithNoncompliantValues")
    def keys_with_noncompliant_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "keysWithNoncompliantValues"))

    @builtins.property
    @jsii.member(jsii_name="nonCompliantKeys")
    def non_compliant_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "nonCompliantKeys"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListComplianceDetails]:
        return typing.cast(typing.Optional[DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListComplianceDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListComplianceDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__401276d851b8881cfafe862d3ca6596ad7406461b0ef28adeb6c802cc84cd272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsResourcegroupstaggingapiResources.DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1f43e10e545698bde1451deb89e9e6bb21f94afad5e17f711e7952dd2fc0865)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9da550a493c5622edcc36b8d4faa92373d3120c4acff2f476224c3c96e08c91e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f46e07963a61fe5a25bc134de8f93d035586f8e789e0c9d1f3c7a338e30f8e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60c93ce67bf08735baa196b18d4046181c7162abbc7a48e0a73a90359a592432)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a4584afb90e8b49547780e22e30c7d0e0a12b25338320465a67ae2acc5a904e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsResourcegroupstaggingapiResources.DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2be6ba88e1a38e7a04c90428ccc9d9f6ce5fd7d880e93a9de8304ed9632c05f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="complianceDetails")
    def compliance_details(
        self,
    ) -> DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListComplianceDetailsList:
        return typing.cast(DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListComplianceDetailsList, jsii.get(self, "complianceDetails"))

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAwsResourcegroupstaggingapiResourcesResourceTagMappingList]:
        return typing.cast(typing.Optional[DataAwsResourcegroupstaggingapiResourcesResourceTagMappingList], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAwsResourcegroupstaggingapiResourcesResourceTagMappingList],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bb5af227e98d1943edb5005fb2028235c55d555be4403307a707c63abd9a797)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsResourcegroupstaggingapiResources.DataAwsResourcegroupstaggingapiResourcesTagFilter",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class DataAwsResourcegroupstaggingapiResourcesTagFilter:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#key DataAwsResourcegroupstaggingapiResources#key}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#values DataAwsResourcegroupstaggingapiResources#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36a356d13b83add7263e47e9a3a7bdcd05279ae103507c8ed023cfb5f97ec704)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#key DataAwsResourcegroupstaggingapiResources#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/resourcegroupstaggingapi_resources#values DataAwsResourcegroupstaggingapiResources#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsResourcegroupstaggingapiResourcesTagFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAwsResourcegroupstaggingapiResourcesTagFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsResourcegroupstaggingapiResources.DataAwsResourcegroupstaggingapiResourcesTagFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35e06f138a9c96de7e60ac57a6a5be0f7af3200c68082e25ec06dc9a9b665d10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAwsResourcegroupstaggingapiResourcesTagFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ad19772033c7c2c7ac6dfd117506add90b5abf86a39a1adbcba7fd9f55b9d4f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAwsResourcegroupstaggingapiResourcesTagFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b9069ed6059a40822e7672a8dc973c6bff6e3710cbaa304b43ebc30074f7f5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92ca2cb903211b25b735d0b45fac11cce86bc04530466cf1b04227b280d06691)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe77bd018188e85c0824e12dfe83db97a9d0d3405ebc772c355dc51213a43af7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsResourcegroupstaggingapiResourcesTagFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsResourcegroupstaggingapiResourcesTagFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsResourcegroupstaggingapiResourcesTagFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4b1176d24a821e0ae71f374e9a0cbb28cb4de223e9e4a963979917c3e422659)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataAwsResourcegroupstaggingapiResourcesTagFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsResourcegroupstaggingapiResources.DataAwsResourcegroupstaggingapiResourcesTagFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62df0c240384276754bc6cd4d1b67feb985e447b53309134ea8e3f5899cdb09c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9c77878896d4df08741628699376b97dfd66d36c3d400db7e77af76826afc19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc34727f5569972ca4a6dd2df725013e06a0902f37e2950770d3bf62d6619933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataAwsResourcegroupstaggingapiResourcesTagFilter, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataAwsResourcegroupstaggingapiResourcesTagFilter, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataAwsResourcegroupstaggingapiResourcesTagFilter, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__633acecab0265f265500a5e70d380dc6085b7d8bcc868f5c2b58856b6a6f298f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataAwsResourcegroupstaggingapiResources",
    "DataAwsResourcegroupstaggingapiResourcesConfig",
    "DataAwsResourcegroupstaggingapiResourcesResourceTagMappingList",
    "DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListComplianceDetails",
    "DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListComplianceDetailsList",
    "DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListComplianceDetailsOutputReference",
    "DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListList",
    "DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListOutputReference",
    "DataAwsResourcegroupstaggingapiResourcesTagFilter",
    "DataAwsResourcegroupstaggingapiResourcesTagFilterList",
    "DataAwsResourcegroupstaggingapiResourcesTagFilterOutputReference",
]

publication.publish()

def _typecheckingstub__379a0a56e3c395a2c0b10c3907d12e97b93e09cefb56ca213ea912eb2f3f02b0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    exclude_compliant_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    include_compliance_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    resource_arn_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_type_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsResourcegroupstaggingapiResourcesTagFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__459110b412e197ff0de2649b6bcac46a80213d75ce721d1c524c72150766271b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsResourcegroupstaggingapiResourcesTagFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a602e767b6b8c345ad529b4de7804da7fc26fc390a27bbab32b5dd34e0927283(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb7e6a17937722a8fbf3f8926ff9063dfc8ccea7a4b5185e90c28113b4cde4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89fce751b5d60d0ad8164b02b7d36f9e244cde4f2c63255278868422efac3693(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89692354778d82575b7d2f9708fe56a06d0a625e6ccac1c62d3c2fc8608a4f24(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__154bc8e387716a6fd93c2229dd31b704e04607ec41e75d1ec72a1fbaefe8108c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb87dae7972e41450dd18fbb52c3c5922ed174f7092e1ccceea839dea927ce2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    exclude_compliant_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    include_compliance_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    resource_arn_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_type_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsResourcegroupstaggingapiResourcesTagFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ff2d46eaf3e39beca75af28dc7e8641d1ddd188088eb5804bc29e383151eb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c68c453d933b70f5dac55b26724dabc7816b972a4956ebce33b70cfcaab4da2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c12c573b69e4f215907cf070e4775b58071310a10a4751e19473be77880dc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2f78983fcb35155b9de5797c14b25b6402374ffd84cc03e8fb22cd122d9c83b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f0a65604710e5e1bdfd79c91ecc12749c197a5c5333d958a99e146a05af6f1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b07d6e93339305f3f21b0aeb281cea246942346992fc036227fd532c9d2f82(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__401276d851b8881cfafe862d3ca6596ad7406461b0ef28adeb6c802cc84cd272(
    value: typing.Optional[DataAwsResourcegroupstaggingapiResourcesResourceTagMappingListComplianceDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1f43e10e545698bde1451deb89e9e6bb21f94afad5e17f711e7952dd2fc0865(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9da550a493c5622edcc36b8d4faa92373d3120c4acff2f476224c3c96e08c91e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f46e07963a61fe5a25bc134de8f93d035586f8e789e0c9d1f3c7a338e30f8e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c93ce67bf08735baa196b18d4046181c7162abbc7a48e0a73a90359a592432(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4584afb90e8b49547780e22e30c7d0e0a12b25338320465a67ae2acc5a904e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2be6ba88e1a38e7a04c90428ccc9d9f6ce5fd7d880e93a9de8304ed9632c05f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb5af227e98d1943edb5005fb2028235c55d555be4403307a707c63abd9a797(
    value: typing.Optional[DataAwsResourcegroupstaggingapiResourcesResourceTagMappingList],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a356d13b83add7263e47e9a3a7bdcd05279ae103507c8ed023cfb5f97ec704(
    *,
    key: builtins.str,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35e06f138a9c96de7e60ac57a6a5be0f7af3200c68082e25ec06dc9a9b665d10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad19772033c7c2c7ac6dfd117506add90b5abf86a39a1adbcba7fd9f55b9d4f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9069ed6059a40822e7672a8dc973c6bff6e3710cbaa304b43ebc30074f7f5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ca2cb903211b25b735d0b45fac11cce86bc04530466cf1b04227b280d06691(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe77bd018188e85c0824e12dfe83db97a9d0d3405ebc772c355dc51213a43af7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b1176d24a821e0ae71f374e9a0cbb28cb4de223e9e4a963979917c3e422659(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsResourcegroupstaggingapiResourcesTagFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62df0c240384276754bc6cd4d1b67feb985e447b53309134ea8e3f5899cdb09c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c77878896d4df08741628699376b97dfd66d36c3d400db7e77af76826afc19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc34727f5569972ca4a6dd2df725013e06a0902f37e2950770d3bf62d6619933(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633acecab0265f265500a5e70d380dc6085b7d8bcc868f5c2b58856b6a6f298f(
    value: typing.Optional[typing.Union[DataAwsResourcegroupstaggingapiResourcesTagFilter, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
