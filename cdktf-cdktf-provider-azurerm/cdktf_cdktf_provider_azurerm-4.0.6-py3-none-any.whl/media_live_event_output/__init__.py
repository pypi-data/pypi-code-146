'''
# `azurerm_media_live_event_output`

Refer to the Terraform Registory for docs: [`azurerm_media_live_event_output`](https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output).
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


class MediaLiveEventOutput(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaLiveEventOutput.MediaLiveEventOutput",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output azurerm_media_live_event_output}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        archive_window_duration: builtins.str,
        asset_name: builtins.str,
        live_event_id: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        hls_fragments_per_ts_segment: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        manifest_name: typing.Optional[builtins.str] = None,
        output_snap_time_in_seconds: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["MediaLiveEventOutputTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output azurerm_media_live_event_output} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param archive_window_duration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#archive_window_duration MediaLiveEventOutput#archive_window_duration}.
        :param asset_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#asset_name MediaLiveEventOutput#asset_name}.
        :param live_event_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#live_event_id MediaLiveEventOutput#live_event_id}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#name MediaLiveEventOutput#name}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#description MediaLiveEventOutput#description}.
        :param hls_fragments_per_ts_segment: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#hls_fragments_per_ts_segment MediaLiveEventOutput#hls_fragments_per_ts_segment}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#id MediaLiveEventOutput#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param manifest_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#manifest_name MediaLiveEventOutput#manifest_name}.
        :param output_snap_time_in_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#output_snap_time_in_seconds MediaLiveEventOutput#output_snap_time_in_seconds}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#timeouts MediaLiveEventOutput#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b964f45882ffebe4acab2a8c55fe21fe915d8aab2ad20e4c5fd761ea0ffc5452)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MediaLiveEventOutputConfig(
            archive_window_duration=archive_window_duration,
            asset_name=asset_name,
            live_event_id=live_event_id,
            name=name,
            description=description,
            hls_fragments_per_ts_segment=hls_fragments_per_ts_segment,
            id=id,
            manifest_name=manifest_name,
            output_snap_time_in_seconds=output_snap_time_in_seconds,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#create MediaLiveEventOutput#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#delete MediaLiveEventOutput#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#read MediaLiveEventOutput#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#update MediaLiveEventOutput#update}.
        '''
        value = MediaLiveEventOutputTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetHlsFragmentsPerTsSegment")
    def reset_hls_fragments_per_ts_segment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHlsFragmentsPerTsSegment", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetManifestName")
    def reset_manifest_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManifestName", []))

    @jsii.member(jsii_name="resetOutputSnapTimeInSeconds")
    def reset_output_snap_time_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputSnapTimeInSeconds", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MediaLiveEventOutputTimeoutsOutputReference":
        return typing.cast("MediaLiveEventOutputTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="archiveWindowDurationInput")
    def archive_window_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "archiveWindowDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="assetNameInput")
    def asset_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="hlsFragmentsPerTsSegmentInput")
    def hls_fragments_per_ts_segment_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hlsFragmentsPerTsSegmentInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="liveEventIdInput")
    def live_event_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "liveEventIdInput"))

    @builtins.property
    @jsii.member(jsii_name="manifestNameInput")
    def manifest_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "manifestNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="outputSnapTimeInSecondsInput")
    def output_snap_time_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "outputSnapTimeInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["MediaLiveEventOutputTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["MediaLiveEventOutputTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="archiveWindowDuration")
    def archive_window_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "archiveWindowDuration"))

    @archive_window_duration.setter
    def archive_window_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4923dff84f4276b2eee8692a8c1041627d24c3bf6cdd29220e9075ff14a13557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveWindowDuration", value)

    @builtins.property
    @jsii.member(jsii_name="assetName")
    def asset_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assetName"))

    @asset_name.setter
    def asset_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8eeb0021eef779f9fd7cfd2c5b6f38823eff8c703e0d439a9cd8ae0f402c14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetName", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2103ff8f262fe4753f4ff2e83c1b039901f15c2bdc87254b25de8d6b2fd11eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="hlsFragmentsPerTsSegment")
    def hls_fragments_per_ts_segment(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hlsFragmentsPerTsSegment"))

    @hls_fragments_per_ts_segment.setter
    def hls_fragments_per_ts_segment(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e2411b45b0aaa39d3b5d6cd9341ed825c035587467662a011898c3875c4364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hlsFragmentsPerTsSegment", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17a7173bfbe6da374ac2a99972b36488a4c96dde4318093e1b2ec9e15d4aa983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="liveEventId")
    def live_event_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "liveEventId"))

    @live_event_id.setter
    def live_event_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80b022cfcc81537808aed3b04ed215c101dc922708a907d61ad8b45d22428c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "liveEventId", value)

    @builtins.property
    @jsii.member(jsii_name="manifestName")
    def manifest_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "manifestName"))

    @manifest_name.setter
    def manifest_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc1bfc261bc47d3f8abb3d29e76040d0b26caa56282d05e87634af37fac58240)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manifestName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd20a6d36268f004f19011707f633406401e3db54d3f5b6c1b66b22563ce398b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="outputSnapTimeInSeconds")
    def output_snap_time_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "outputSnapTimeInSeconds"))

    @output_snap_time_in_seconds.setter
    def output_snap_time_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3e957db3ee12659ffb8c4879fb84c526e1b29ffb7302003c734f5526da7a46c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputSnapTimeInSeconds", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaLiveEventOutput.MediaLiveEventOutputConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "archive_window_duration": "archiveWindowDuration",
        "asset_name": "assetName",
        "live_event_id": "liveEventId",
        "name": "name",
        "description": "description",
        "hls_fragments_per_ts_segment": "hlsFragmentsPerTsSegment",
        "id": "id",
        "manifest_name": "manifestName",
        "output_snap_time_in_seconds": "outputSnapTimeInSeconds",
        "timeouts": "timeouts",
    },
)
class MediaLiveEventOutputConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        archive_window_duration: builtins.str,
        asset_name: builtins.str,
        live_event_id: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        hls_fragments_per_ts_segment: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        manifest_name: typing.Optional[builtins.str] = None,
        output_snap_time_in_seconds: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["MediaLiveEventOutputTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param archive_window_duration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#archive_window_duration MediaLiveEventOutput#archive_window_duration}.
        :param asset_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#asset_name MediaLiveEventOutput#asset_name}.
        :param live_event_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#live_event_id MediaLiveEventOutput#live_event_id}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#name MediaLiveEventOutput#name}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#description MediaLiveEventOutput#description}.
        :param hls_fragments_per_ts_segment: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#hls_fragments_per_ts_segment MediaLiveEventOutput#hls_fragments_per_ts_segment}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#id MediaLiveEventOutput#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param manifest_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#manifest_name MediaLiveEventOutput#manifest_name}.
        :param output_snap_time_in_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#output_snap_time_in_seconds MediaLiveEventOutput#output_snap_time_in_seconds}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#timeouts MediaLiveEventOutput#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = MediaLiveEventOutputTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72973f92ead93800a90b1e15eaa8a8225136a8d6d9742b9bac8971e6ae30c776)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument archive_window_duration", value=archive_window_duration, expected_type=type_hints["archive_window_duration"])
            check_type(argname="argument asset_name", value=asset_name, expected_type=type_hints["asset_name"])
            check_type(argname="argument live_event_id", value=live_event_id, expected_type=type_hints["live_event_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument hls_fragments_per_ts_segment", value=hls_fragments_per_ts_segment, expected_type=type_hints["hls_fragments_per_ts_segment"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument manifest_name", value=manifest_name, expected_type=type_hints["manifest_name"])
            check_type(argname="argument output_snap_time_in_seconds", value=output_snap_time_in_seconds, expected_type=type_hints["output_snap_time_in_seconds"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "archive_window_duration": archive_window_duration,
            "asset_name": asset_name,
            "live_event_id": live_event_id,
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
        if hls_fragments_per_ts_segment is not None:
            self._values["hls_fragments_per_ts_segment"] = hls_fragments_per_ts_segment
        if id is not None:
            self._values["id"] = id
        if manifest_name is not None:
            self._values["manifest_name"] = manifest_name
        if output_snap_time_in_seconds is not None:
            self._values["output_snap_time_in_seconds"] = output_snap_time_in_seconds
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def archive_window_duration(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#archive_window_duration MediaLiveEventOutput#archive_window_duration}.'''
        result = self._values.get("archive_window_duration")
        assert result is not None, "Required property 'archive_window_duration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#asset_name MediaLiveEventOutput#asset_name}.'''
        result = self._values.get("asset_name")
        assert result is not None, "Required property 'asset_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def live_event_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#live_event_id MediaLiveEventOutput#live_event_id}.'''
        result = self._values.get("live_event_id")
        assert result is not None, "Required property 'live_event_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#name MediaLiveEventOutput#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#description MediaLiveEventOutput#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hls_fragments_per_ts_segment(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#hls_fragments_per_ts_segment MediaLiveEventOutput#hls_fragments_per_ts_segment}.'''
        result = self._values.get("hls_fragments_per_ts_segment")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#id MediaLiveEventOutput#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manifest_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#manifest_name MediaLiveEventOutput#manifest_name}.'''
        result = self._values.get("manifest_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_snap_time_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#output_snap_time_in_seconds MediaLiveEventOutput#output_snap_time_in_seconds}.'''
        result = self._values.get("output_snap_time_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MediaLiveEventOutputTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#timeouts MediaLiveEventOutput#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MediaLiveEventOutputTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaLiveEventOutputConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaLiveEventOutput.MediaLiveEventOutputTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MediaLiveEventOutputTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#create MediaLiveEventOutput#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#delete MediaLiveEventOutput#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#read MediaLiveEventOutput#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#update MediaLiveEventOutput#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3af2bd9418a09ae50f005f445f3d020a27700eba11e32fa20376a775c44f8e41)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#create MediaLiveEventOutput#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#delete MediaLiveEventOutput#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#read MediaLiveEventOutput#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event_output#update MediaLiveEventOutput#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaLiveEventOutputTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaLiveEventOutputTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaLiveEventOutput.MediaLiveEventOutputTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3aaf08a98f46a9a9f7f731dcaa0683e49755fc08a675849e81cc9261dec31fd6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e959e4ea68e18393a1fb6ac127401cef08684421210dff3d213248e818c65afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2428df9121e7d08b8ff751b330c182581e228c6873be10afafca9caf6ddc66d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a36420a473ec483b67f9fa7d233109debb5501b03a4dcfe1193b75927d1d487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9327402acedef76f5cd1961bc32c8660dbebd6cbea7ea34841237469f36efa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MediaLiveEventOutputTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MediaLiveEventOutputTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MediaLiveEventOutputTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2d15644382d16cc897f82ee0542e87ad0d29f4e96a60671a83708b1a7d85bc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MediaLiveEventOutput",
    "MediaLiveEventOutputConfig",
    "MediaLiveEventOutputTimeouts",
    "MediaLiveEventOutputTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b964f45882ffebe4acab2a8c55fe21fe915d8aab2ad20e4c5fd761ea0ffc5452(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    archive_window_duration: builtins.str,
    asset_name: builtins.str,
    live_event_id: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    hls_fragments_per_ts_segment: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    manifest_name: typing.Optional[builtins.str] = None,
    output_snap_time_in_seconds: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[MediaLiveEventOutputTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4923dff84f4276b2eee8692a8c1041627d24c3bf6cdd29220e9075ff14a13557(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8eeb0021eef779f9fd7cfd2c5b6f38823eff8c703e0d439a9cd8ae0f402c14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2103ff8f262fe4753f4ff2e83c1b039901f15c2bdc87254b25de8d6b2fd11eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e2411b45b0aaa39d3b5d6cd9341ed825c035587467662a011898c3875c4364(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a7173bfbe6da374ac2a99972b36488a4c96dde4318093e1b2ec9e15d4aa983(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80b022cfcc81537808aed3b04ed215c101dc922708a907d61ad8b45d22428c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1bfc261bc47d3f8abb3d29e76040d0b26caa56282d05e87634af37fac58240(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd20a6d36268f004f19011707f633406401e3db54d3f5b6c1b66b22563ce398b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e957db3ee12659ffb8c4879fb84c526e1b29ffb7302003c734f5526da7a46c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72973f92ead93800a90b1e15eaa8a8225136a8d6d9742b9bac8971e6ae30c776(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    archive_window_duration: builtins.str,
    asset_name: builtins.str,
    live_event_id: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    hls_fragments_per_ts_segment: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    manifest_name: typing.Optional[builtins.str] = None,
    output_snap_time_in_seconds: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[MediaLiveEventOutputTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af2bd9418a09ae50f005f445f3d020a27700eba11e32fa20376a775c44f8e41(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aaf08a98f46a9a9f7f731dcaa0683e49755fc08a675849e81cc9261dec31fd6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e959e4ea68e18393a1fb6ac127401cef08684421210dff3d213248e818c65afa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2428df9121e7d08b8ff751b330c182581e228c6873be10afafca9caf6ddc66d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a36420a473ec483b67f9fa7d233109debb5501b03a4dcfe1193b75927d1d487(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9327402acedef76f5cd1961bc32c8660dbebd6cbea7ea34841237469f36efa5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2d15644382d16cc897f82ee0542e87ad0d29f4e96a60671a83708b1a7d85bc6(
    value: typing.Optional[typing.Union[MediaLiveEventOutputTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
