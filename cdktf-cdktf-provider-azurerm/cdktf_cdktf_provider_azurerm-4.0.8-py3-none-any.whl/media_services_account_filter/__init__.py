'''
# `azurerm_media_services_account_filter`

Refer to the Terraform Registory for docs: [`azurerm_media_services_account_filter`](https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter).
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


class MediaServicesAccountFilter(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaServicesAccountFilter.MediaServicesAccountFilter",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter azurerm_media_services_account_filter}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        media_services_account_name: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        first_quality_bitrate: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        presentation_time_range: typing.Optional[typing.Union["MediaServicesAccountFilterPresentationTimeRange", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["MediaServicesAccountFilterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        track_selection: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MediaServicesAccountFilterTrackSelection", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter azurerm_media_services_account_filter} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param media_services_account_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#media_services_account_name MediaServicesAccountFilter#media_services_account_name}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#name MediaServicesAccountFilter#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#resource_group_name MediaServicesAccountFilter#resource_group_name}.
        :param first_quality_bitrate: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#first_quality_bitrate MediaServicesAccountFilter#first_quality_bitrate}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#id MediaServicesAccountFilter#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param presentation_time_range: presentation_time_range block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#presentation_time_range MediaServicesAccountFilter#presentation_time_range}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#timeouts MediaServicesAccountFilter#timeouts}
        :param track_selection: track_selection block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#track_selection MediaServicesAccountFilter#track_selection}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d96d3f0203feb46c21188ddcb080a12f17357645a59742afeb36484e464ca76)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MediaServicesAccountFilterConfig(
            media_services_account_name=media_services_account_name,
            name=name,
            resource_group_name=resource_group_name,
            first_quality_bitrate=first_quality_bitrate,
            id=id,
            presentation_time_range=presentation_time_range,
            timeouts=timeouts,
            track_selection=track_selection,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putPresentationTimeRange")
    def put_presentation_time_range(
        self,
        *,
        unit_timescale_in_milliseconds: jsii.Number,
        end_in_units: typing.Optional[jsii.Number] = None,
        force_end: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        live_backoff_in_units: typing.Optional[jsii.Number] = None,
        presentation_window_in_units: typing.Optional[jsii.Number] = None,
        start_in_units: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param unit_timescale_in_milliseconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#unit_timescale_in_milliseconds MediaServicesAccountFilter#unit_timescale_in_milliseconds}.
        :param end_in_units: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#end_in_units MediaServicesAccountFilter#end_in_units}.
        :param force_end: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#force_end MediaServicesAccountFilter#force_end}.
        :param live_backoff_in_units: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#live_backoff_in_units MediaServicesAccountFilter#live_backoff_in_units}.
        :param presentation_window_in_units: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#presentation_window_in_units MediaServicesAccountFilter#presentation_window_in_units}.
        :param start_in_units: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#start_in_units MediaServicesAccountFilter#start_in_units}.
        '''
        value = MediaServicesAccountFilterPresentationTimeRange(
            unit_timescale_in_milliseconds=unit_timescale_in_milliseconds,
            end_in_units=end_in_units,
            force_end=force_end,
            live_backoff_in_units=live_backoff_in_units,
            presentation_window_in_units=presentation_window_in_units,
            start_in_units=start_in_units,
        )

        return typing.cast(None, jsii.invoke(self, "putPresentationTimeRange", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#create MediaServicesAccountFilter#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#delete MediaServicesAccountFilter#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#read MediaServicesAccountFilter#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#update MediaServicesAccountFilter#update}.
        '''
        value = MediaServicesAccountFilterTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTrackSelection")
    def put_track_selection(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MediaServicesAccountFilterTrackSelection", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4128cd60d88a136cb8ccbcac93c303a0f8bc5470c80d0c4b85e43957f812d5c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTrackSelection", [value]))

    @jsii.member(jsii_name="resetFirstQualityBitrate")
    def reset_first_quality_bitrate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstQualityBitrate", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPresentationTimeRange")
    def reset_presentation_time_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPresentationTimeRange", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTrackSelection")
    def reset_track_selection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrackSelection", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="presentationTimeRange")
    def presentation_time_range(
        self,
    ) -> "MediaServicesAccountFilterPresentationTimeRangeOutputReference":
        return typing.cast("MediaServicesAccountFilterPresentationTimeRangeOutputReference", jsii.get(self, "presentationTimeRange"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MediaServicesAccountFilterTimeoutsOutputReference":
        return typing.cast("MediaServicesAccountFilterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="trackSelection")
    def track_selection(self) -> "MediaServicesAccountFilterTrackSelectionList":
        return typing.cast("MediaServicesAccountFilterTrackSelectionList", jsii.get(self, "trackSelection"))

    @builtins.property
    @jsii.member(jsii_name="firstQualityBitrateInput")
    def first_quality_bitrate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "firstQualityBitrateInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mediaServicesAccountNameInput")
    def media_services_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mediaServicesAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="presentationTimeRangeInput")
    def presentation_time_range_input(
        self,
    ) -> typing.Optional["MediaServicesAccountFilterPresentationTimeRange"]:
        return typing.cast(typing.Optional["MediaServicesAccountFilterPresentationTimeRange"], jsii.get(self, "presentationTimeRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["MediaServicesAccountFilterTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["MediaServicesAccountFilterTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="trackSelectionInput")
    def track_selection_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaServicesAccountFilterTrackSelection"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaServicesAccountFilterTrackSelection"]]], jsii.get(self, "trackSelectionInput"))

    @builtins.property
    @jsii.member(jsii_name="firstQualityBitrate")
    def first_quality_bitrate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "firstQualityBitrate"))

    @first_quality_bitrate.setter
    def first_quality_bitrate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f1a3836b02cfdd40337e8ee8322855fc74c79eaca382e1a37fbc92ab9286bd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstQualityBitrate", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aac318964617a0e87a031075030ce75bd68faef91e43fd9ab54d08944ff5e8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="mediaServicesAccountName")
    def media_services_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mediaServicesAccountName"))

    @media_services_account_name.setter
    def media_services_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce7efc6808570bba3728fac72d935375033c830d9c55ff1f9cf88d9bdcb81dcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mediaServicesAccountName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1b863157395347997c1b9cdb2c3b6552b9674b39cbdf53c1b7ba07b2980f40c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8532bfbcca4f5be6b4475260d8c1aa2d9965fc7d657ba3496e60671af9f34c7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaServicesAccountFilter.MediaServicesAccountFilterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "media_services_account_name": "mediaServicesAccountName",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "first_quality_bitrate": "firstQualityBitrate",
        "id": "id",
        "presentation_time_range": "presentationTimeRange",
        "timeouts": "timeouts",
        "track_selection": "trackSelection",
    },
)
class MediaServicesAccountFilterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        media_services_account_name: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        first_quality_bitrate: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        presentation_time_range: typing.Optional[typing.Union["MediaServicesAccountFilterPresentationTimeRange", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["MediaServicesAccountFilterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        track_selection: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MediaServicesAccountFilterTrackSelection", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param media_services_account_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#media_services_account_name MediaServicesAccountFilter#media_services_account_name}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#name MediaServicesAccountFilter#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#resource_group_name MediaServicesAccountFilter#resource_group_name}.
        :param first_quality_bitrate: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#first_quality_bitrate MediaServicesAccountFilter#first_quality_bitrate}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#id MediaServicesAccountFilter#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param presentation_time_range: presentation_time_range block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#presentation_time_range MediaServicesAccountFilter#presentation_time_range}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#timeouts MediaServicesAccountFilter#timeouts}
        :param track_selection: track_selection block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#track_selection MediaServicesAccountFilter#track_selection}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(presentation_time_range, dict):
            presentation_time_range = MediaServicesAccountFilterPresentationTimeRange(**presentation_time_range)
        if isinstance(timeouts, dict):
            timeouts = MediaServicesAccountFilterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77920e8b4a71634809ab75c422068898094e922b2f4c5e91017ffc861b090cd9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument media_services_account_name", value=media_services_account_name, expected_type=type_hints["media_services_account_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument first_quality_bitrate", value=first_quality_bitrate, expected_type=type_hints["first_quality_bitrate"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument presentation_time_range", value=presentation_time_range, expected_type=type_hints["presentation_time_range"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument track_selection", value=track_selection, expected_type=type_hints["track_selection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "media_services_account_name": media_services_account_name,
            "name": name,
            "resource_group_name": resource_group_name,
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
        if first_quality_bitrate is not None:
            self._values["first_quality_bitrate"] = first_quality_bitrate
        if id is not None:
            self._values["id"] = id
        if presentation_time_range is not None:
            self._values["presentation_time_range"] = presentation_time_range
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if track_selection is not None:
            self._values["track_selection"] = track_selection

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
    def media_services_account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#media_services_account_name MediaServicesAccountFilter#media_services_account_name}.'''
        result = self._values.get("media_services_account_name")
        assert result is not None, "Required property 'media_services_account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#name MediaServicesAccountFilter#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#resource_group_name MediaServicesAccountFilter#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def first_quality_bitrate(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#first_quality_bitrate MediaServicesAccountFilter#first_quality_bitrate}.'''
        result = self._values.get("first_quality_bitrate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#id MediaServicesAccountFilter#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def presentation_time_range(
        self,
    ) -> typing.Optional["MediaServicesAccountFilterPresentationTimeRange"]:
        '''presentation_time_range block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#presentation_time_range MediaServicesAccountFilter#presentation_time_range}
        '''
        result = self._values.get("presentation_time_range")
        return typing.cast(typing.Optional["MediaServicesAccountFilterPresentationTimeRange"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MediaServicesAccountFilterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#timeouts MediaServicesAccountFilter#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MediaServicesAccountFilterTimeouts"], result)

    @builtins.property
    def track_selection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaServicesAccountFilterTrackSelection"]]]:
        '''track_selection block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#track_selection MediaServicesAccountFilter#track_selection}
        '''
        result = self._values.get("track_selection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaServicesAccountFilterTrackSelection"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaServicesAccountFilterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaServicesAccountFilter.MediaServicesAccountFilterPresentationTimeRange",
    jsii_struct_bases=[],
    name_mapping={
        "unit_timescale_in_milliseconds": "unitTimescaleInMilliseconds",
        "end_in_units": "endInUnits",
        "force_end": "forceEnd",
        "live_backoff_in_units": "liveBackoffInUnits",
        "presentation_window_in_units": "presentationWindowInUnits",
        "start_in_units": "startInUnits",
    },
)
class MediaServicesAccountFilterPresentationTimeRange:
    def __init__(
        self,
        *,
        unit_timescale_in_milliseconds: jsii.Number,
        end_in_units: typing.Optional[jsii.Number] = None,
        force_end: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        live_backoff_in_units: typing.Optional[jsii.Number] = None,
        presentation_window_in_units: typing.Optional[jsii.Number] = None,
        start_in_units: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param unit_timescale_in_milliseconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#unit_timescale_in_milliseconds MediaServicesAccountFilter#unit_timescale_in_milliseconds}.
        :param end_in_units: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#end_in_units MediaServicesAccountFilter#end_in_units}.
        :param force_end: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#force_end MediaServicesAccountFilter#force_end}.
        :param live_backoff_in_units: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#live_backoff_in_units MediaServicesAccountFilter#live_backoff_in_units}.
        :param presentation_window_in_units: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#presentation_window_in_units MediaServicesAccountFilter#presentation_window_in_units}.
        :param start_in_units: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#start_in_units MediaServicesAccountFilter#start_in_units}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ead8acd3dd2dec8174f295824db000402c4059bf3848a965cc4475d2e4f5763)
            check_type(argname="argument unit_timescale_in_milliseconds", value=unit_timescale_in_milliseconds, expected_type=type_hints["unit_timescale_in_milliseconds"])
            check_type(argname="argument end_in_units", value=end_in_units, expected_type=type_hints["end_in_units"])
            check_type(argname="argument force_end", value=force_end, expected_type=type_hints["force_end"])
            check_type(argname="argument live_backoff_in_units", value=live_backoff_in_units, expected_type=type_hints["live_backoff_in_units"])
            check_type(argname="argument presentation_window_in_units", value=presentation_window_in_units, expected_type=type_hints["presentation_window_in_units"])
            check_type(argname="argument start_in_units", value=start_in_units, expected_type=type_hints["start_in_units"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit_timescale_in_milliseconds": unit_timescale_in_milliseconds,
        }
        if end_in_units is not None:
            self._values["end_in_units"] = end_in_units
        if force_end is not None:
            self._values["force_end"] = force_end
        if live_backoff_in_units is not None:
            self._values["live_backoff_in_units"] = live_backoff_in_units
        if presentation_window_in_units is not None:
            self._values["presentation_window_in_units"] = presentation_window_in_units
        if start_in_units is not None:
            self._values["start_in_units"] = start_in_units

    @builtins.property
    def unit_timescale_in_milliseconds(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#unit_timescale_in_milliseconds MediaServicesAccountFilter#unit_timescale_in_milliseconds}.'''
        result = self._values.get("unit_timescale_in_milliseconds")
        assert result is not None, "Required property 'unit_timescale_in_milliseconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def end_in_units(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#end_in_units MediaServicesAccountFilter#end_in_units}.'''
        result = self._values.get("end_in_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def force_end(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#force_end MediaServicesAccountFilter#force_end}.'''
        result = self._values.get("force_end")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def live_backoff_in_units(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#live_backoff_in_units MediaServicesAccountFilter#live_backoff_in_units}.'''
        result = self._values.get("live_backoff_in_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def presentation_window_in_units(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#presentation_window_in_units MediaServicesAccountFilter#presentation_window_in_units}.'''
        result = self._values.get("presentation_window_in_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_in_units(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#start_in_units MediaServicesAccountFilter#start_in_units}.'''
        result = self._values.get("start_in_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaServicesAccountFilterPresentationTimeRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaServicesAccountFilterPresentationTimeRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaServicesAccountFilter.MediaServicesAccountFilterPresentationTimeRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c1768c2e1246762de565adbb27056e250b0082fc72f1c54bf5f268edd9749bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEndInUnits")
    def reset_end_in_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndInUnits", []))

    @jsii.member(jsii_name="resetForceEnd")
    def reset_force_end(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceEnd", []))

    @jsii.member(jsii_name="resetLiveBackoffInUnits")
    def reset_live_backoff_in_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLiveBackoffInUnits", []))

    @jsii.member(jsii_name="resetPresentationWindowInUnits")
    def reset_presentation_window_in_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPresentationWindowInUnits", []))

    @jsii.member(jsii_name="resetStartInUnits")
    def reset_start_in_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartInUnits", []))

    @builtins.property
    @jsii.member(jsii_name="endInUnitsInput")
    def end_in_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "endInUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="forceEndInput")
    def force_end_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceEndInput"))

    @builtins.property
    @jsii.member(jsii_name="liveBackoffInUnitsInput")
    def live_backoff_in_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "liveBackoffInUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="presentationWindowInUnitsInput")
    def presentation_window_in_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "presentationWindowInUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="startInUnitsInput")
    def start_in_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startInUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="unitTimescaleInMillisecondsInput")
    def unit_timescale_in_milliseconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "unitTimescaleInMillisecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="endInUnits")
    def end_in_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "endInUnits"))

    @end_in_units.setter
    def end_in_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98fdc909de0e2fe7efbf8316a2ad2521f58b1705cb996457ff404c7fdab34720)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endInUnits", value)

    @builtins.property
    @jsii.member(jsii_name="forceEnd")
    def force_end(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceEnd"))

    @force_end.setter
    def force_end(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a0286c2f6c1d1ef978c01076dec6392d50120231c329cee352f25677cffb5d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceEnd", value)

    @builtins.property
    @jsii.member(jsii_name="liveBackoffInUnits")
    def live_backoff_in_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "liveBackoffInUnits"))

    @live_backoff_in_units.setter
    def live_backoff_in_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f21f9321e1fdd86c823ee7e4ad2df5498fbc7d6310ca6eb628c0d0fbed7fd73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "liveBackoffInUnits", value)

    @builtins.property
    @jsii.member(jsii_name="presentationWindowInUnits")
    def presentation_window_in_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "presentationWindowInUnits"))

    @presentation_window_in_units.setter
    def presentation_window_in_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0942b86ee918e856676fd9d3084baba611115b4e52217f05c1c2c6bd05270d8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "presentationWindowInUnits", value)

    @builtins.property
    @jsii.member(jsii_name="startInUnits")
    def start_in_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startInUnits"))

    @start_in_units.setter
    def start_in_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a563588a8ef5515f751c45d9b52d9f0b6b0cd27e500de3e7cb858aff42fb3e6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startInUnits", value)

    @builtins.property
    @jsii.member(jsii_name="unitTimescaleInMilliseconds")
    def unit_timescale_in_milliseconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "unitTimescaleInMilliseconds"))

    @unit_timescale_in_milliseconds.setter
    def unit_timescale_in_milliseconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7795341716dc03350b43caeb52f08de20392b0c8c0336fe1f6c71c7f179b02bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unitTimescaleInMilliseconds", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MediaServicesAccountFilterPresentationTimeRange]:
        return typing.cast(typing.Optional[MediaServicesAccountFilterPresentationTimeRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MediaServicesAccountFilterPresentationTimeRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828fe1a248bbc5fc3bec465b2070b42a0a4290fb38bc82cda3c2be4e654df1a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaServicesAccountFilter.MediaServicesAccountFilterTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MediaServicesAccountFilterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#create MediaServicesAccountFilter#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#delete MediaServicesAccountFilter#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#read MediaServicesAccountFilter#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#update MediaServicesAccountFilter#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df3223aa001be9f94e661c59a7a55d6535c8e142ba60499ced08edabada0bc32)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#create MediaServicesAccountFilter#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#delete MediaServicesAccountFilter#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#read MediaServicesAccountFilter#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#update MediaServicesAccountFilter#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaServicesAccountFilterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaServicesAccountFilterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaServicesAccountFilter.MediaServicesAccountFilterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__039c920249f4506f38b184a3ccd493087e7a49377524dc0437bebbf673509c18)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8d51e8959fb223e4e69c956566b331bfcfbf9db917914af582184780a816705a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__698ff40f335b0137c0678a63cd6b46f0b5668a33a18dbade044a78ce1acb4460)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__273dfa23888a3d1b3ab37210ea7e0d3e3b42b1b3901ac5766c5184e6f1ccd076)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__958301c05489fa9d4a8aea58c9bd6247f4e98ee9e87ca40678d4ee463115cd75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MediaServicesAccountFilterTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MediaServicesAccountFilterTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MediaServicesAccountFilterTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b01d5f521dc394f36757c442a3f6d106d8e9cb9b157cd420c48d79b12367caf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaServicesAccountFilter.MediaServicesAccountFilterTrackSelection",
    jsii_struct_bases=[],
    name_mapping={"condition": "condition"},
)
class MediaServicesAccountFilterTrackSelection:
    def __init__(
        self,
        *,
        condition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MediaServicesAccountFilterTrackSelectionCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param condition: condition block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#condition MediaServicesAccountFilter#condition}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85cb3c25b726944dc6a0eec7e9be71af99c74d552ff730668826f38646eef770)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "condition": condition,
        }

    @builtins.property
    def condition(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaServicesAccountFilterTrackSelectionCondition"]]:
        '''condition block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#condition MediaServicesAccountFilter#condition}
        '''
        result = self._values.get("condition")
        assert result is not None, "Required property 'condition' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaServicesAccountFilterTrackSelectionCondition"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaServicesAccountFilterTrackSelection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaServicesAccountFilter.MediaServicesAccountFilterTrackSelectionCondition",
    jsii_struct_bases=[],
    name_mapping={"operation": "operation", "property": "property", "value": "value"},
)
class MediaServicesAccountFilterTrackSelectionCondition:
    def __init__(
        self,
        *,
        operation: builtins.str,
        property: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param operation: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#operation MediaServicesAccountFilter#operation}.
        :param property: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#property MediaServicesAccountFilter#property}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#value MediaServicesAccountFilter#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1500567651162381ba48cfe3c6e345069f7404db135eb6c81dfe95b0a74357f)
            check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
            check_type(argname="argument property", value=property, expected_type=type_hints["property"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operation": operation,
            "property": property,
            "value": value,
        }

    @builtins.property
    def operation(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#operation MediaServicesAccountFilter#operation}.'''
        result = self._values.get("operation")
        assert result is not None, "Required property 'operation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def property(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#property MediaServicesAccountFilter#property}.'''
        result = self._values.get("property")
        assert result is not None, "Required property 'property' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_services_account_filter#value MediaServicesAccountFilter#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaServicesAccountFilterTrackSelectionCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaServicesAccountFilterTrackSelectionConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaServicesAccountFilter.MediaServicesAccountFilterTrackSelectionConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2fb59316a19b3e0f99ecbba00e3314790bee59e620782e264edec0ab98ad3ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MediaServicesAccountFilterTrackSelectionConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80f66527618f91a1e9a858ff2eecf807c2149b5463dea0b3a5f355045b750d92)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MediaServicesAccountFilterTrackSelectionConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb32b93e17aed8eaa3de0ec6b23a33cc2e526a388f9ec140bcbcf95f1308083)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21de57cc5b66816bc42653251086f9099052843b684993518dfe459c78a58bf0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a5e36f8879ede3dc431c9eead7c8661f9c9d9d03fe26d3ff5d86210edecce62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaServicesAccountFilterTrackSelectionCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaServicesAccountFilterTrackSelectionCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaServicesAccountFilterTrackSelectionCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd06f6fa13f988701bd64ef810ed2a1f774b65b761e494495a19a2185d79a8ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MediaServicesAccountFilterTrackSelectionConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaServicesAccountFilter.MediaServicesAccountFilterTrackSelectionConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1d582e893a5c6fdec6cef5da70f578f9a9fd35f45d931f74261b44107de3749)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="operationInput")
    def operation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationInput"))

    @builtins.property
    @jsii.member(jsii_name="propertyInput")
    def property_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "propertyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="operation")
    def operation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operation"))

    @operation.setter
    def operation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0054f6c2192b1a0bbd93f46fb83dae8b0f6ca2c80429e2f79cb60d9e81ae8ae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operation", value)

    @builtins.property
    @jsii.member(jsii_name="property")
    def property(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "property"))

    @property.setter
    def property(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__090bb54f8a6d48621b1a082e72df2ec50cd5df30b98df223217c67efc643601e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "property", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a95fc10534fdca75a8f08a78a8904eeb7753180817b291f03a498bf7c64d770e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MediaServicesAccountFilterTrackSelectionCondition, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MediaServicesAccountFilterTrackSelectionCondition, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MediaServicesAccountFilterTrackSelectionCondition, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd2a9493261cac87d2ed4a79408b6a18622bfd4a2e37445255c766cafb1d6f80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MediaServicesAccountFilterTrackSelectionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaServicesAccountFilter.MediaServicesAccountFilterTrackSelectionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2e601249d8c2f513264f4fcc4885dee18138f170a8bebee23fb3c49a730e055)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MediaServicesAccountFilterTrackSelectionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1d85ca260636b97e355fcdedf9a881e0949e6ab8a2449ef1e42447a14f9fdf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MediaServicesAccountFilterTrackSelectionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7b9881beab5fe68d7094a92ad59d8c2a0cfa702e13708403e2ef8de1373e661)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd32889b2e7cbf98bdd2e0430691a51184181ca9f5c34f225dad80d9d674ab07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__195b0ab91829a2a0dfa6f8875ef6a756584eab6b174798bd9f011bdbda7044d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaServicesAccountFilterTrackSelection]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaServicesAccountFilterTrackSelection]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaServicesAccountFilterTrackSelection]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8072b1772535958a545a659b01ee0658ea3b3ecff0265170c584c58f2a57ab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MediaServicesAccountFilterTrackSelectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaServicesAccountFilter.MediaServicesAccountFilterTrackSelectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68f968cdec84ec5fa03670f0112d229505867980be869fda102a6ff1c1b6f720)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaServicesAccountFilterTrackSelectionCondition, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b250a52fba8fae7bce88844c915346a9d9275a2e6a5859249bf892b64ded7c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> MediaServicesAccountFilterTrackSelectionConditionList:
        return typing.cast(MediaServicesAccountFilterTrackSelectionConditionList, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaServicesAccountFilterTrackSelectionCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaServicesAccountFilterTrackSelectionCondition]]], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MediaServicesAccountFilterTrackSelection, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MediaServicesAccountFilterTrackSelection, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MediaServicesAccountFilterTrackSelection, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e733553b8b36edf736b96e5585a81564230a5fbf06f984bb91e3034a194b7f7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MediaServicesAccountFilter",
    "MediaServicesAccountFilterConfig",
    "MediaServicesAccountFilterPresentationTimeRange",
    "MediaServicesAccountFilterPresentationTimeRangeOutputReference",
    "MediaServicesAccountFilterTimeouts",
    "MediaServicesAccountFilterTimeoutsOutputReference",
    "MediaServicesAccountFilterTrackSelection",
    "MediaServicesAccountFilterTrackSelectionCondition",
    "MediaServicesAccountFilterTrackSelectionConditionList",
    "MediaServicesAccountFilterTrackSelectionConditionOutputReference",
    "MediaServicesAccountFilterTrackSelectionList",
    "MediaServicesAccountFilterTrackSelectionOutputReference",
]

publication.publish()

def _typecheckingstub__7d96d3f0203feb46c21188ddcb080a12f17357645a59742afeb36484e464ca76(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    media_services_account_name: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    first_quality_bitrate: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    presentation_time_range: typing.Optional[typing.Union[MediaServicesAccountFilterPresentationTimeRange, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[MediaServicesAccountFilterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    track_selection: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaServicesAccountFilterTrackSelection, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__4128cd60d88a136cb8ccbcac93c303a0f8bc5470c80d0c4b85e43957f812d5c9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaServicesAccountFilterTrackSelection, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f1a3836b02cfdd40337e8ee8322855fc74c79eaca382e1a37fbc92ab9286bd0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aac318964617a0e87a031075030ce75bd68faef91e43fd9ab54d08944ff5e8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7efc6808570bba3728fac72d935375033c830d9c55ff1f9cf88d9bdcb81dcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1b863157395347997c1b9cdb2c3b6552b9674b39cbdf53c1b7ba07b2980f40c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8532bfbcca4f5be6b4475260d8c1aa2d9965fc7d657ba3496e60671af9f34c7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77920e8b4a71634809ab75c422068898094e922b2f4c5e91017ffc861b090cd9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    media_services_account_name: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    first_quality_bitrate: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    presentation_time_range: typing.Optional[typing.Union[MediaServicesAccountFilterPresentationTimeRange, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[MediaServicesAccountFilterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    track_selection: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaServicesAccountFilterTrackSelection, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ead8acd3dd2dec8174f295824db000402c4059bf3848a965cc4475d2e4f5763(
    *,
    unit_timescale_in_milliseconds: jsii.Number,
    end_in_units: typing.Optional[jsii.Number] = None,
    force_end: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    live_backoff_in_units: typing.Optional[jsii.Number] = None,
    presentation_window_in_units: typing.Optional[jsii.Number] = None,
    start_in_units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1768c2e1246762de565adbb27056e250b0082fc72f1c54bf5f268edd9749bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98fdc909de0e2fe7efbf8316a2ad2521f58b1705cb996457ff404c7fdab34720(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a0286c2f6c1d1ef978c01076dec6392d50120231c329cee352f25677cffb5d6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f21f9321e1fdd86c823ee7e4ad2df5498fbc7d6310ca6eb628c0d0fbed7fd73(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0942b86ee918e856676fd9d3084baba611115b4e52217f05c1c2c6bd05270d8f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a563588a8ef5515f751c45d9b52d9f0b6b0cd27e500de3e7cb858aff42fb3e6f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7795341716dc03350b43caeb52f08de20392b0c8c0336fe1f6c71c7f179b02bb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828fe1a248bbc5fc3bec465b2070b42a0a4290fb38bc82cda3c2be4e654df1a1(
    value: typing.Optional[MediaServicesAccountFilterPresentationTimeRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3223aa001be9f94e661c59a7a55d6535c8e142ba60499ced08edabada0bc32(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__039c920249f4506f38b184a3ccd493087e7a49377524dc0437bebbf673509c18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d51e8959fb223e4e69c956566b331bfcfbf9db917914af582184780a816705a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698ff40f335b0137c0678a63cd6b46f0b5668a33a18dbade044a78ce1acb4460(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__273dfa23888a3d1b3ab37210ea7e0d3e3b42b1b3901ac5766c5184e6f1ccd076(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958301c05489fa9d4a8aea58c9bd6247f4e98ee9e87ca40678d4ee463115cd75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01d5f521dc394f36757c442a3f6d106d8e9cb9b157cd420c48d79b12367caf1(
    value: typing.Optional[typing.Union[MediaServicesAccountFilterTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85cb3c25b726944dc6a0eec7e9be71af99c74d552ff730668826f38646eef770(
    *,
    condition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaServicesAccountFilterTrackSelectionCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1500567651162381ba48cfe3c6e345069f7404db135eb6c81dfe95b0a74357f(
    *,
    operation: builtins.str,
    property: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2fb59316a19b3e0f99ecbba00e3314790bee59e620782e264edec0ab98ad3ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f66527618f91a1e9a858ff2eecf807c2149b5463dea0b3a5f355045b750d92(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb32b93e17aed8eaa3de0ec6b23a33cc2e526a388f9ec140bcbcf95f1308083(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21de57cc5b66816bc42653251086f9099052843b684993518dfe459c78a58bf0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5e36f8879ede3dc431c9eead7c8661f9c9d9d03fe26d3ff5d86210edecce62(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd06f6fa13f988701bd64ef810ed2a1f774b65b761e494495a19a2185d79a8ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaServicesAccountFilterTrackSelectionCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d582e893a5c6fdec6cef5da70f578f9a9fd35f45d931f74261b44107de3749(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0054f6c2192b1a0bbd93f46fb83dae8b0f6ca2c80429e2f79cb60d9e81ae8ae5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090bb54f8a6d48621b1a082e72df2ec50cd5df30b98df223217c67efc643601e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a95fc10534fdca75a8f08a78a8904eeb7753180817b291f03a498bf7c64d770e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2a9493261cac87d2ed4a79408b6a18622bfd4a2e37445255c766cafb1d6f80(
    value: typing.Optional[typing.Union[MediaServicesAccountFilterTrackSelectionCondition, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2e601249d8c2f513264f4fcc4885dee18138f170a8bebee23fb3c49a730e055(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1d85ca260636b97e355fcdedf9a881e0949e6ab8a2449ef1e42447a14f9fdf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b9881beab5fe68d7094a92ad59d8c2a0cfa702e13708403e2ef8de1373e661(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd32889b2e7cbf98bdd2e0430691a51184181ca9f5c34f225dad80d9d674ab07(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195b0ab91829a2a0dfa6f8875ef6a756584eab6b174798bd9f011bdbda7044d5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8072b1772535958a545a659b01ee0658ea3b3ecff0265170c584c58f2a57ab5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaServicesAccountFilterTrackSelection]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68f968cdec84ec5fa03670f0112d229505867980be869fda102a6ff1c1b6f720(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b250a52fba8fae7bce88844c915346a9d9275a2e6a5859249bf892b64ded7c3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaServicesAccountFilterTrackSelectionCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e733553b8b36edf736b96e5585a81564230a5fbf06f984bb91e3034a194b7f7b(
    value: typing.Optional[typing.Union[MediaServicesAccountFilterTrackSelection, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
