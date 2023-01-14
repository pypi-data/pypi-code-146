'''
# `azurerm_media_asset_filter`

Refer to the Terraform Registory for docs: [`azurerm_media_asset_filter`](https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter).
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


class MediaAssetFilter(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaAssetFilter.MediaAssetFilter",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter azurerm_media_asset_filter}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        asset_id: builtins.str,
        name: builtins.str,
        first_quality_bitrate: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        presentation_time_range: typing.Optional[typing.Union["MediaAssetFilterPresentationTimeRange", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["MediaAssetFilterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        track_selection: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MediaAssetFilterTrackSelection", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter azurerm_media_asset_filter} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param asset_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#asset_id MediaAssetFilter#asset_id}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#name MediaAssetFilter#name}.
        :param first_quality_bitrate: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#first_quality_bitrate MediaAssetFilter#first_quality_bitrate}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#id MediaAssetFilter#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param presentation_time_range: presentation_time_range block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#presentation_time_range MediaAssetFilter#presentation_time_range}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#timeouts MediaAssetFilter#timeouts}
        :param track_selection: track_selection block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#track_selection MediaAssetFilter#track_selection}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0073224a0789fb82e19b587237438a4d7890fa24bbd6a48b3fd8cf397bac1c7f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MediaAssetFilterConfig(
            asset_id=asset_id,
            name=name,
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
        end_in_units: typing.Optional[jsii.Number] = None,
        force_end: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        live_backoff_in_units: typing.Optional[jsii.Number] = None,
        presentation_window_in_units: typing.Optional[jsii.Number] = None,
        start_in_units: typing.Optional[jsii.Number] = None,
        unit_timescale_in_miliseconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param end_in_units: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#end_in_units MediaAssetFilter#end_in_units}.
        :param force_end: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#force_end MediaAssetFilter#force_end}.
        :param live_backoff_in_units: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#live_backoff_in_units MediaAssetFilter#live_backoff_in_units}.
        :param presentation_window_in_units: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#presentation_window_in_units MediaAssetFilter#presentation_window_in_units}.
        :param start_in_units: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#start_in_units MediaAssetFilter#start_in_units}.
        :param unit_timescale_in_miliseconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#unit_timescale_in_miliseconds MediaAssetFilter#unit_timescale_in_miliseconds}.
        '''
        value = MediaAssetFilterPresentationTimeRange(
            end_in_units=end_in_units,
            force_end=force_end,
            live_backoff_in_units=live_backoff_in_units,
            presentation_window_in_units=presentation_window_in_units,
            start_in_units=start_in_units,
            unit_timescale_in_miliseconds=unit_timescale_in_miliseconds,
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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#create MediaAssetFilter#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#delete MediaAssetFilter#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#read MediaAssetFilter#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#update MediaAssetFilter#update}.
        '''
        value = MediaAssetFilterTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTrackSelection")
    def put_track_selection(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MediaAssetFilterTrackSelection", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__581ad25d4725c767a892f47f1b0889a57db97d7bb9a2b30c3c7f6a3c049a6ab3)
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
    ) -> "MediaAssetFilterPresentationTimeRangeOutputReference":
        return typing.cast("MediaAssetFilterPresentationTimeRangeOutputReference", jsii.get(self, "presentationTimeRange"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MediaAssetFilterTimeoutsOutputReference":
        return typing.cast("MediaAssetFilterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="trackSelection")
    def track_selection(self) -> "MediaAssetFilterTrackSelectionList":
        return typing.cast("MediaAssetFilterTrackSelectionList", jsii.get(self, "trackSelection"))

    @builtins.property
    @jsii.member(jsii_name="assetIdInput")
    def asset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="firstQualityBitrateInput")
    def first_quality_bitrate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "firstQualityBitrateInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="presentationTimeRangeInput")
    def presentation_time_range_input(
        self,
    ) -> typing.Optional["MediaAssetFilterPresentationTimeRange"]:
        return typing.cast(typing.Optional["MediaAssetFilterPresentationTimeRange"], jsii.get(self, "presentationTimeRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["MediaAssetFilterTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["MediaAssetFilterTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="trackSelectionInput")
    def track_selection_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaAssetFilterTrackSelection"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaAssetFilterTrackSelection"]]], jsii.get(self, "trackSelectionInput"))

    @builtins.property
    @jsii.member(jsii_name="assetId")
    def asset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assetId"))

    @asset_id.setter
    def asset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e102224d12df3f52f4bf8850cdbabe8d90999aae5c0288fe2d826fa805d7b36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetId", value)

    @builtins.property
    @jsii.member(jsii_name="firstQualityBitrate")
    def first_quality_bitrate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "firstQualityBitrate"))

    @first_quality_bitrate.setter
    def first_quality_bitrate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44dc5adcd6d55b813bf3148dc0441df2ab8ae8ebaa9bd5022d635b4a580d3f5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstQualityBitrate", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c5b3f670e71a2e343413c7f910945a1731aa710ffcc49daf7cfda390bd9974)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55e96fdc358ce518cab0ff50697707fe3c5c375e7241076d19b75fe632a705de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaAssetFilter.MediaAssetFilterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "asset_id": "assetId",
        "name": "name",
        "first_quality_bitrate": "firstQualityBitrate",
        "id": "id",
        "presentation_time_range": "presentationTimeRange",
        "timeouts": "timeouts",
        "track_selection": "trackSelection",
    },
)
class MediaAssetFilterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        asset_id: builtins.str,
        name: builtins.str,
        first_quality_bitrate: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        presentation_time_range: typing.Optional[typing.Union["MediaAssetFilterPresentationTimeRange", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["MediaAssetFilterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        track_selection: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MediaAssetFilterTrackSelection", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param asset_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#asset_id MediaAssetFilter#asset_id}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#name MediaAssetFilter#name}.
        :param first_quality_bitrate: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#first_quality_bitrate MediaAssetFilter#first_quality_bitrate}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#id MediaAssetFilter#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param presentation_time_range: presentation_time_range block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#presentation_time_range MediaAssetFilter#presentation_time_range}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#timeouts MediaAssetFilter#timeouts}
        :param track_selection: track_selection block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#track_selection MediaAssetFilter#track_selection}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(presentation_time_range, dict):
            presentation_time_range = MediaAssetFilterPresentationTimeRange(**presentation_time_range)
        if isinstance(timeouts, dict):
            timeouts = MediaAssetFilterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f4258224f609cb6553d8fa3a6f31559a1ae3c8d4a7b37dc0f464dc7a57339eb)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument asset_id", value=asset_id, expected_type=type_hints["asset_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument first_quality_bitrate", value=first_quality_bitrate, expected_type=type_hints["first_quality_bitrate"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument presentation_time_range", value=presentation_time_range, expected_type=type_hints["presentation_time_range"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument track_selection", value=track_selection, expected_type=type_hints["track_selection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "asset_id": asset_id,
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
    def asset_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#asset_id MediaAssetFilter#asset_id}.'''
        result = self._values.get("asset_id")
        assert result is not None, "Required property 'asset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#name MediaAssetFilter#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def first_quality_bitrate(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#first_quality_bitrate MediaAssetFilter#first_quality_bitrate}.'''
        result = self._values.get("first_quality_bitrate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#id MediaAssetFilter#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def presentation_time_range(
        self,
    ) -> typing.Optional["MediaAssetFilterPresentationTimeRange"]:
        '''presentation_time_range block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#presentation_time_range MediaAssetFilter#presentation_time_range}
        '''
        result = self._values.get("presentation_time_range")
        return typing.cast(typing.Optional["MediaAssetFilterPresentationTimeRange"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MediaAssetFilterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#timeouts MediaAssetFilter#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MediaAssetFilterTimeouts"], result)

    @builtins.property
    def track_selection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaAssetFilterTrackSelection"]]]:
        '''track_selection block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#track_selection MediaAssetFilter#track_selection}
        '''
        result = self._values.get("track_selection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaAssetFilterTrackSelection"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaAssetFilterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaAssetFilter.MediaAssetFilterPresentationTimeRange",
    jsii_struct_bases=[],
    name_mapping={
        "end_in_units": "endInUnits",
        "force_end": "forceEnd",
        "live_backoff_in_units": "liveBackoffInUnits",
        "presentation_window_in_units": "presentationWindowInUnits",
        "start_in_units": "startInUnits",
        "unit_timescale_in_miliseconds": "unitTimescaleInMiliseconds",
    },
)
class MediaAssetFilterPresentationTimeRange:
    def __init__(
        self,
        *,
        end_in_units: typing.Optional[jsii.Number] = None,
        force_end: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        live_backoff_in_units: typing.Optional[jsii.Number] = None,
        presentation_window_in_units: typing.Optional[jsii.Number] = None,
        start_in_units: typing.Optional[jsii.Number] = None,
        unit_timescale_in_miliseconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param end_in_units: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#end_in_units MediaAssetFilter#end_in_units}.
        :param force_end: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#force_end MediaAssetFilter#force_end}.
        :param live_backoff_in_units: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#live_backoff_in_units MediaAssetFilter#live_backoff_in_units}.
        :param presentation_window_in_units: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#presentation_window_in_units MediaAssetFilter#presentation_window_in_units}.
        :param start_in_units: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#start_in_units MediaAssetFilter#start_in_units}.
        :param unit_timescale_in_miliseconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#unit_timescale_in_miliseconds MediaAssetFilter#unit_timescale_in_miliseconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0a5e708cd3a3f9022b47f6ae783ba11175ee7e0797ed842dcdea5f323efee1)
            check_type(argname="argument end_in_units", value=end_in_units, expected_type=type_hints["end_in_units"])
            check_type(argname="argument force_end", value=force_end, expected_type=type_hints["force_end"])
            check_type(argname="argument live_backoff_in_units", value=live_backoff_in_units, expected_type=type_hints["live_backoff_in_units"])
            check_type(argname="argument presentation_window_in_units", value=presentation_window_in_units, expected_type=type_hints["presentation_window_in_units"])
            check_type(argname="argument start_in_units", value=start_in_units, expected_type=type_hints["start_in_units"])
            check_type(argname="argument unit_timescale_in_miliseconds", value=unit_timescale_in_miliseconds, expected_type=type_hints["unit_timescale_in_miliseconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if unit_timescale_in_miliseconds is not None:
            self._values["unit_timescale_in_miliseconds"] = unit_timescale_in_miliseconds

    @builtins.property
    def end_in_units(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#end_in_units MediaAssetFilter#end_in_units}.'''
        result = self._values.get("end_in_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def force_end(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#force_end MediaAssetFilter#force_end}.'''
        result = self._values.get("force_end")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def live_backoff_in_units(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#live_backoff_in_units MediaAssetFilter#live_backoff_in_units}.'''
        result = self._values.get("live_backoff_in_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def presentation_window_in_units(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#presentation_window_in_units MediaAssetFilter#presentation_window_in_units}.'''
        result = self._values.get("presentation_window_in_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_in_units(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#start_in_units MediaAssetFilter#start_in_units}.'''
        result = self._values.get("start_in_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unit_timescale_in_miliseconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#unit_timescale_in_miliseconds MediaAssetFilter#unit_timescale_in_miliseconds}.'''
        result = self._values.get("unit_timescale_in_miliseconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaAssetFilterPresentationTimeRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaAssetFilterPresentationTimeRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaAssetFilter.MediaAssetFilterPresentationTimeRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2ee106f500301ea29cfe90c7cbaf8eec78874f3f648ecc707c1bee83eb1a274)
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

    @jsii.member(jsii_name="resetUnitTimescaleInMiliseconds")
    def reset_unit_timescale_in_miliseconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnitTimescaleInMiliseconds", []))

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
    @jsii.member(jsii_name="unitTimescaleInMilisecondsInput")
    def unit_timescale_in_miliseconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "unitTimescaleInMilisecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="endInUnits")
    def end_in_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "endInUnits"))

    @end_in_units.setter
    def end_in_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c38ee6bf40a4ae356e2f3d4fe9dbd3ad0c5841ff8687335d03580f4cb0d2920)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50856d240d175d3be51923cfacefb42c6e88ee3289b4969696cc9683d9b1dcb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceEnd", value)

    @builtins.property
    @jsii.member(jsii_name="liveBackoffInUnits")
    def live_backoff_in_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "liveBackoffInUnits"))

    @live_backoff_in_units.setter
    def live_backoff_in_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8391c9e737626f87b25b85d22ffc7aaabe7eeae1af44e79b8e1d891a3dfb1133)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "liveBackoffInUnits", value)

    @builtins.property
    @jsii.member(jsii_name="presentationWindowInUnits")
    def presentation_window_in_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "presentationWindowInUnits"))

    @presentation_window_in_units.setter
    def presentation_window_in_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a411401a0b7931996ef1ac08458ece0b79a14cf6c6a9e3d5dfa480cd6a6b91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "presentationWindowInUnits", value)

    @builtins.property
    @jsii.member(jsii_name="startInUnits")
    def start_in_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startInUnits"))

    @start_in_units.setter
    def start_in_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__999a26688345dd7f3f3ca21d00c6eaf94b4541c0239e182754058c564e50b4a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startInUnits", value)

    @builtins.property
    @jsii.member(jsii_name="unitTimescaleInMiliseconds")
    def unit_timescale_in_miliseconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "unitTimescaleInMiliseconds"))

    @unit_timescale_in_miliseconds.setter
    def unit_timescale_in_miliseconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b548b64b1dc0fd439f7aa310be9a048b9e1b4bfd32cd60b8bb40bca75c10568c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unitTimescaleInMiliseconds", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MediaAssetFilterPresentationTimeRange]:
        return typing.cast(typing.Optional[MediaAssetFilterPresentationTimeRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MediaAssetFilterPresentationTimeRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e37c605e9aa06c542d7f42ca09298e9cf4885f38e0eb69686ae4968fbfef358f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaAssetFilter.MediaAssetFilterTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MediaAssetFilterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#create MediaAssetFilter#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#delete MediaAssetFilter#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#read MediaAssetFilter#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#update MediaAssetFilter#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66cd62aa769f525cf7b5b5f2021e3fd03bfc36031ccbf779c6a9f56411d42813)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#create MediaAssetFilter#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#delete MediaAssetFilter#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#read MediaAssetFilter#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#update MediaAssetFilter#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaAssetFilterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaAssetFilterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaAssetFilter.MediaAssetFilterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6d10cb73eafe986f42b231c28a5ac0b3e302e67c9d3d3b21526eed8fca5a4f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef7fdffd510cf81c9e6ed6867db5d581289bb990f197b710bdc500670da2d27a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d5c91ecebecff17c2fa7be7376f14755b8dfb1cdd41580fbaebde3697c4c958)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a8515f0f7a91bd5a9dbba17cb080db0fe03bc2dc14fcdae90375c838b28f2c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b496d039b549fc3ce4f5f6f78a64a72c31b92212bda555d5e776ad9519e7e22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MediaAssetFilterTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MediaAssetFilterTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MediaAssetFilterTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e2b8ae2d2b48cb44564a96d359314b119fec398302d135182c1175c801e8be9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaAssetFilter.MediaAssetFilterTrackSelection",
    jsii_struct_bases=[],
    name_mapping={"condition": "condition"},
)
class MediaAssetFilterTrackSelection:
    def __init__(
        self,
        *,
        condition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MediaAssetFilterTrackSelectionCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param condition: condition block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#condition MediaAssetFilter#condition}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ece9e2630d152fd155d668a06f15b60554fbfd6e1fa31dc6b1539f5d9b573de)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "condition": condition,
        }

    @builtins.property
    def condition(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaAssetFilterTrackSelectionCondition"]]:
        '''condition block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#condition MediaAssetFilter#condition}
        '''
        result = self._values.get("condition")
        assert result is not None, "Required property 'condition' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaAssetFilterTrackSelectionCondition"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaAssetFilterTrackSelection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaAssetFilter.MediaAssetFilterTrackSelectionCondition",
    jsii_struct_bases=[],
    name_mapping={"operation": "operation", "property": "property", "value": "value"},
)
class MediaAssetFilterTrackSelectionCondition:
    def __init__(
        self,
        *,
        operation: typing.Optional[builtins.str] = None,
        property: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operation: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#operation MediaAssetFilter#operation}.
        :param property: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#property MediaAssetFilter#property}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#value MediaAssetFilter#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ef1e753e82d9e9a47e6775dc9e79e793a4d6402a514d25783cc63cb57b6c1d)
            check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
            check_type(argname="argument property", value=property, expected_type=type_hints["property"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if operation is not None:
            self._values["operation"] = operation
        if property is not None:
            self._values["property"] = property
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def operation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#operation MediaAssetFilter#operation}.'''
        result = self._values.get("operation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def property(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#property MediaAssetFilter#property}.'''
        result = self._values.get("property")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_asset_filter#value MediaAssetFilter#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaAssetFilterTrackSelectionCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaAssetFilterTrackSelectionConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaAssetFilter.MediaAssetFilterTrackSelectionConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75f33b05b135f7ed24df34f544600d5fe96e9f1944c69a3a10a78cbb0419b6c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MediaAssetFilterTrackSelectionConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cedc14c00cf4db47e661e4edd176d5078d9ef023261d5787b9d9e7359362fb59)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MediaAssetFilterTrackSelectionConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__937363e41854cf15bac7f4a5a7af2ed244268bb4e6874a087cfbcc924dd84c41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f40745122de68759eed696f64720aea075c4a70429c49f78559b1a8e367881c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c813ab859a56b3ae640fbe90d5f8b18026ca5753be216f1681c8345242b16b1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaAssetFilterTrackSelectionCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaAssetFilterTrackSelectionCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaAssetFilterTrackSelectionCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f62a921774d1f96679b04c74c00013b3f1eb3be2c96107929aa1c2f6fc80c263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MediaAssetFilterTrackSelectionConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaAssetFilter.MediaAssetFilterTrackSelectionConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f14b7aafea8f8371af8640159f2b7287ad61bc1f178b735176e8e0c53ed1ab6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOperation")
    def reset_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperation", []))

    @jsii.member(jsii_name="resetProperty")
    def reset_property(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperty", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3e619b3a66b0531d37293cea164c389f787b7238cf16263741cfb7190cb62e0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operation", value)

    @builtins.property
    @jsii.member(jsii_name="property")
    def property(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "property"))

    @property.setter
    def property(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df8cded7c581b72617bdd11bee8e8646a0d0adf640bf5a8511b5dbdf36949d3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "property", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8274e1a81ee0db01476512bfda872bf6f2660db7e8164a865c13e320b209643)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MediaAssetFilterTrackSelectionCondition, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MediaAssetFilterTrackSelectionCondition, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MediaAssetFilterTrackSelectionCondition, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63cd682c3842e5062779d319abcb55b3a11aaa3ffac51f2ec9d40d6643051fc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MediaAssetFilterTrackSelectionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaAssetFilter.MediaAssetFilterTrackSelectionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42041616e44c08e8fd9fd4a97ee6a45bf50aae75accb9ce743fcbae6dc806c8a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MediaAssetFilterTrackSelectionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0273dd174f4d708930095b1baf19c5d21072817b2a6feeb1730a3a00cdbfc1bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MediaAssetFilterTrackSelectionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac0499c42354eeeacc09593856a068f4c067ec5f756772ce899e7964a015b91b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__601fad747de1edc68117f0b03a633d59697c91744eb3436c2f8e3b0219c6a74d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ef796ce0d681a2be2e8c3a859b8109c8699524369c4744bded5958aee86a428)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaAssetFilterTrackSelection]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaAssetFilterTrackSelection]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaAssetFilterTrackSelection]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ef35b289529c2aa9a1bc065cde26c313819779e802063e278ef97ab7fd3873b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MediaAssetFilterTrackSelectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaAssetFilter.MediaAssetFilterTrackSelectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e31f7835fb5ccd6d5440ead0123e19b02833c0b44b94eaf3bf7eadbe70d32585)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaAssetFilterTrackSelectionCondition, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__442119effb6bc4294860e2a84fe0a54063555b2a846698241c18d58e6e382092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> MediaAssetFilterTrackSelectionConditionList:
        return typing.cast(MediaAssetFilterTrackSelectionConditionList, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaAssetFilterTrackSelectionCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaAssetFilterTrackSelectionCondition]]], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MediaAssetFilterTrackSelection, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MediaAssetFilterTrackSelection, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MediaAssetFilterTrackSelection, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86f4d09aa1dec84dceb9145745c9b0414b62098350b1ef8c2674b3693df1880d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MediaAssetFilter",
    "MediaAssetFilterConfig",
    "MediaAssetFilterPresentationTimeRange",
    "MediaAssetFilterPresentationTimeRangeOutputReference",
    "MediaAssetFilterTimeouts",
    "MediaAssetFilterTimeoutsOutputReference",
    "MediaAssetFilterTrackSelection",
    "MediaAssetFilterTrackSelectionCondition",
    "MediaAssetFilterTrackSelectionConditionList",
    "MediaAssetFilterTrackSelectionConditionOutputReference",
    "MediaAssetFilterTrackSelectionList",
    "MediaAssetFilterTrackSelectionOutputReference",
]

publication.publish()

def _typecheckingstub__0073224a0789fb82e19b587237438a4d7890fa24bbd6a48b3fd8cf397bac1c7f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    asset_id: builtins.str,
    name: builtins.str,
    first_quality_bitrate: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    presentation_time_range: typing.Optional[typing.Union[MediaAssetFilterPresentationTimeRange, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[MediaAssetFilterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    track_selection: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaAssetFilterTrackSelection, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__581ad25d4725c767a892f47f1b0889a57db97d7bb9a2b30c3c7f6a3c049a6ab3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaAssetFilterTrackSelection, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e102224d12df3f52f4bf8850cdbabe8d90999aae5c0288fe2d826fa805d7b36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44dc5adcd6d55b813bf3148dc0441df2ab8ae8ebaa9bd5022d635b4a580d3f5a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c5b3f670e71a2e343413c7f910945a1731aa710ffcc49daf7cfda390bd9974(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e96fdc358ce518cab0ff50697707fe3c5c375e7241076d19b75fe632a705de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4258224f609cb6553d8fa3a6f31559a1ae3c8d4a7b37dc0f464dc7a57339eb(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    asset_id: builtins.str,
    name: builtins.str,
    first_quality_bitrate: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    presentation_time_range: typing.Optional[typing.Union[MediaAssetFilterPresentationTimeRange, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[MediaAssetFilterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    track_selection: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaAssetFilterTrackSelection, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0a5e708cd3a3f9022b47f6ae783ba11175ee7e0797ed842dcdea5f323efee1(
    *,
    end_in_units: typing.Optional[jsii.Number] = None,
    force_end: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    live_backoff_in_units: typing.Optional[jsii.Number] = None,
    presentation_window_in_units: typing.Optional[jsii.Number] = None,
    start_in_units: typing.Optional[jsii.Number] = None,
    unit_timescale_in_miliseconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ee106f500301ea29cfe90c7cbaf8eec78874f3f648ecc707c1bee83eb1a274(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c38ee6bf40a4ae356e2f3d4fe9dbd3ad0c5841ff8687335d03580f4cb0d2920(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50856d240d175d3be51923cfacefb42c6e88ee3289b4969696cc9683d9b1dcb1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8391c9e737626f87b25b85d22ffc7aaabe7eeae1af44e79b8e1d891a3dfb1133(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a411401a0b7931996ef1ac08458ece0b79a14cf6c6a9e3d5dfa480cd6a6b91(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__999a26688345dd7f3f3ca21d00c6eaf94b4541c0239e182754058c564e50b4a5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b548b64b1dc0fd439f7aa310be9a048b9e1b4bfd32cd60b8bb40bca75c10568c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37c605e9aa06c542d7f42ca09298e9cf4885f38e0eb69686ae4968fbfef358f(
    value: typing.Optional[MediaAssetFilterPresentationTimeRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66cd62aa769f525cf7b5b5f2021e3fd03bfc36031ccbf779c6a9f56411d42813(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d10cb73eafe986f42b231c28a5ac0b3e302e67c9d3d3b21526eed8fca5a4f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef7fdffd510cf81c9e6ed6867db5d581289bb990f197b710bdc500670da2d27a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d5c91ecebecff17c2fa7be7376f14755b8dfb1cdd41580fbaebde3697c4c958(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a8515f0f7a91bd5a9dbba17cb080db0fe03bc2dc14fcdae90375c838b28f2c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b496d039b549fc3ce4f5f6f78a64a72c31b92212bda555d5e776ad9519e7e22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e2b8ae2d2b48cb44564a96d359314b119fec398302d135182c1175c801e8be9(
    value: typing.Optional[typing.Union[MediaAssetFilterTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ece9e2630d152fd155d668a06f15b60554fbfd6e1fa31dc6b1539f5d9b573de(
    *,
    condition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaAssetFilterTrackSelectionCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ef1e753e82d9e9a47e6775dc9e79e793a4d6402a514d25783cc63cb57b6c1d(
    *,
    operation: typing.Optional[builtins.str] = None,
    property: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75f33b05b135f7ed24df34f544600d5fe96e9f1944c69a3a10a78cbb0419b6c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cedc14c00cf4db47e661e4edd176d5078d9ef023261d5787b9d9e7359362fb59(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937363e41854cf15bac7f4a5a7af2ed244268bb4e6874a087cfbcc924dd84c41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f40745122de68759eed696f64720aea075c4a70429c49f78559b1a8e367881c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c813ab859a56b3ae640fbe90d5f8b18026ca5753be216f1681c8345242b16b1f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62a921774d1f96679b04c74c00013b3f1eb3be2c96107929aa1c2f6fc80c263(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaAssetFilterTrackSelectionCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f14b7aafea8f8371af8640159f2b7287ad61bc1f178b735176e8e0c53ed1ab6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e619b3a66b0531d37293cea164c389f787b7238cf16263741cfb7190cb62e0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df8cded7c581b72617bdd11bee8e8646a0d0adf640bf5a8511b5dbdf36949d3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8274e1a81ee0db01476512bfda872bf6f2660db7e8164a865c13e320b209643(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63cd682c3842e5062779d319abcb55b3a11aaa3ffac51f2ec9d40d6643051fc1(
    value: typing.Optional[typing.Union[MediaAssetFilterTrackSelectionCondition, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42041616e44c08e8fd9fd4a97ee6a45bf50aae75accb9ce743fcbae6dc806c8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0273dd174f4d708930095b1baf19c5d21072817b2a6feeb1730a3a00cdbfc1bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac0499c42354eeeacc09593856a068f4c067ec5f756772ce899e7964a015b91b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__601fad747de1edc68117f0b03a633d59697c91744eb3436c2f8e3b0219c6a74d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef796ce0d681a2be2e8c3a859b8109c8699524369c4744bded5958aee86a428(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef35b289529c2aa9a1bc065cde26c313819779e802063e278ef97ab7fd3873b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaAssetFilterTrackSelection]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31f7835fb5ccd6d5440ead0123e19b02833c0b44b94eaf3bf7eadbe70d32585(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__442119effb6bc4294860e2a84fe0a54063555b2a846698241c18d58e6e382092(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaAssetFilterTrackSelectionCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86f4d09aa1dec84dceb9145745c9b0414b62098350b1ef8c2674b3693df1880d(
    value: typing.Optional[typing.Union[MediaAssetFilterTrackSelection, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
