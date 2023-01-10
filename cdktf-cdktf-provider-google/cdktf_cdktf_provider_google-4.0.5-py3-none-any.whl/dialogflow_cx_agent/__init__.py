'''
# `google_dialogflow_cx_agent`

Refer to the Terraform Registory for docs: [`google_dialogflow_cx_agent`](https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent).
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


class DialogflowCxAgent(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgent",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent google_dialogflow_cx_agent}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_language_code: builtins.str,
        display_name: builtins.str,
        location: builtins.str,
        time_zone: builtins.str,
        avatar_uri: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_spell_correction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        security_settings: typing.Optional[builtins.str] = None,
        speech_to_text_settings: typing.Optional[typing.Union["DialogflowCxAgentSpeechToTextSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        supported_language_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DialogflowCxAgentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent google_dialogflow_cx_agent} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_language_code: The default language of the agent as a language tag. `See Language Support <https://cloud.google.com/dialogflow/cx/docs/reference/language>`_ for a list of the currently supported language codes. This field cannot be updated after creation. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#default_language_code DialogflowCxAgent#default_language_code}
        :param display_name: The human-readable name of the agent, unique within the location. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#display_name DialogflowCxAgent#display_name}
        :param location: The name of the location this agent is located in. ~> **Note:** The first time you are deploying an Agent in your project you must configure location settings. This is a one time step but at the moment you can only `configure location settings <https://cloud.google.com/dialogflow/cx/docs/concept/region#location-settings>`_ via the Dialogflow CX console. Another options is to use global location so you don't need to manually configure location settings. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#location DialogflowCxAgent#location}
        :param time_zone: The time zone of this agent from the `time zone database <https://www.iana.org/time-zones>`_, e.g., America/New_York, Europe/Paris. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#time_zone DialogflowCxAgent#time_zone}
        :param avatar_uri: The URI of the agent's avatar. Avatars are used throughout the Dialogflow console and in the self-hosted Web Demo integration. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#avatar_uri DialogflowCxAgent#avatar_uri}
        :param description: The description of this agent. The maximum length is 500 characters. If exceeded, the request is rejected. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#description DialogflowCxAgent#description}
        :param enable_spell_correction: Indicates if automatic spell correction is enabled in detect intent requests. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#enable_spell_correction DialogflowCxAgent#enable_spell_correction}
        :param enable_stackdriver_logging: Determines whether this agent should log conversation queries. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#enable_stackdriver_logging DialogflowCxAgent#enable_stackdriver_logging}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#id DialogflowCxAgent#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#project DialogflowCxAgent#project}.
        :param security_settings: Name of the SecuritySettings reference for the agent. Format: projects//locations//securitySettings/. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#security_settings DialogflowCxAgent#security_settings}
        :param speech_to_text_settings: speech_to_text_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#speech_to_text_settings DialogflowCxAgent#speech_to_text_settings}
        :param supported_language_codes: The list of all languages supported by this agent (except for the default_language_code). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#supported_language_codes DialogflowCxAgent#supported_language_codes}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#timeouts DialogflowCxAgent#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61bc8ebf23753dd057cb6e8d4f9cd853d22b0db49b9c2922bb276b018421e905)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DialogflowCxAgentConfig(
            default_language_code=default_language_code,
            display_name=display_name,
            location=location,
            time_zone=time_zone,
            avatar_uri=avatar_uri,
            description=description,
            enable_spell_correction=enable_spell_correction,
            enable_stackdriver_logging=enable_stackdriver_logging,
            id=id,
            project=project,
            security_settings=security_settings,
            speech_to_text_settings=speech_to_text_settings,
            supported_language_codes=supported_language_codes,
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

    @jsii.member(jsii_name="putSpeechToTextSettings")
    def put_speech_to_text_settings(
        self,
        *,
        enable_speech_adaptation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_speech_adaptation: Whether to use speech adaptation for speech recognition. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#enable_speech_adaptation DialogflowCxAgent#enable_speech_adaptation}
        '''
        value = DialogflowCxAgentSpeechToTextSettings(
            enable_speech_adaptation=enable_speech_adaptation
        )

        return typing.cast(None, jsii.invoke(self, "putSpeechToTextSettings", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#create DialogflowCxAgent#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#delete DialogflowCxAgent#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#update DialogflowCxAgent#update}.
        '''
        value = DialogflowCxAgentTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAvatarUri")
    def reset_avatar_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvatarUri", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnableSpellCorrection")
    def reset_enable_spell_correction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSpellCorrection", []))

    @jsii.member(jsii_name="resetEnableStackdriverLogging")
    def reset_enable_stackdriver_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableStackdriverLogging", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSecuritySettings")
    def reset_security_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecuritySettings", []))

    @jsii.member(jsii_name="resetSpeechToTextSettings")
    def reset_speech_to_text_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpeechToTextSettings", []))

    @jsii.member(jsii_name="resetSupportedLanguageCodes")
    def reset_supported_language_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportedLanguageCodes", []))

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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="speechToTextSettings")
    def speech_to_text_settings(
        self,
    ) -> "DialogflowCxAgentSpeechToTextSettingsOutputReference":
        return typing.cast("DialogflowCxAgentSpeechToTextSettingsOutputReference", jsii.get(self, "speechToTextSettings"))

    @builtins.property
    @jsii.member(jsii_name="startFlow")
    def start_flow(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startFlow"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DialogflowCxAgentTimeoutsOutputReference":
        return typing.cast("DialogflowCxAgentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="avatarUriInput")
    def avatar_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "avatarUriInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultLanguageCodeInput")
    def default_language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultLanguageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSpellCorrectionInput")
    def enable_spell_correction_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSpellCorrectionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableStackdriverLoggingInput")
    def enable_stackdriver_logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableStackdriverLoggingInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="securitySettingsInput")
    def security_settings_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securitySettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="speechToTextSettingsInput")
    def speech_to_text_settings_input(
        self,
    ) -> typing.Optional["DialogflowCxAgentSpeechToTextSettings"]:
        return typing.cast(typing.Optional["DialogflowCxAgentSpeechToTextSettings"], jsii.get(self, "speechToTextSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="supportedLanguageCodesInput")
    def supported_language_codes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "supportedLanguageCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["DialogflowCxAgentTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["DialogflowCxAgentTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="avatarUri")
    def avatar_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "avatarUri"))

    @avatar_uri.setter
    def avatar_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f8342ecdcceb1cabba42fe56e31dbc4a14507bfaef9856c10796f591d512b1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "avatarUri", value)

    @builtins.property
    @jsii.member(jsii_name="defaultLanguageCode")
    def default_language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultLanguageCode"))

    @default_language_code.setter
    def default_language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bc0b4ccf9181d2f9f6f678eeef3eeb36a64dc0fcc331c10be266fd624efb683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLanguageCode", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40be0b053fa106e7cd28a68719bed0f75eb5e745376e20a1cce3dbf10d3d3ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76cde625c357c697363055d9778903f7556f2ff4429366505dec0397319438e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="enableSpellCorrection")
    def enable_spell_correction(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSpellCorrection"))

    @enable_spell_correction.setter
    def enable_spell_correction(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__852f9a4bbdb359fce82d94e4ec9e1c19a2a3ce9055173ebf9741fb32ad338082)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSpellCorrection", value)

    @builtins.property
    @jsii.member(jsii_name="enableStackdriverLogging")
    def enable_stackdriver_logging(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableStackdriverLogging"))

    @enable_stackdriver_logging.setter
    def enable_stackdriver_logging(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9076bdd2a578519759a083b967238a1fe8a7f22236ea2c5546cb7be1b4f5ab77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableStackdriverLogging", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af559d9afdf65e776615de7bfe4984ce199773f4928c7767ebaa0b61d6755470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6144bab910f257b0b948dc47375128bd670cae3fe3c17b8ecd25584c51b849e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1cc79a9c1491ecf859c84adc5762c52f705c16b40203907edf7ffb4320f9bb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="securitySettings")
    def security_settings(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securitySettings"))

    @security_settings.setter
    def security_settings(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65c7b967aea01cb6fb2707be603fb0bbf07ed6b9f53a43f099002cd5e7c81ff8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securitySettings", value)

    @builtins.property
    @jsii.member(jsii_name="supportedLanguageCodes")
    def supported_language_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedLanguageCodes"))

    @supported_language_codes.setter
    def supported_language_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa74fce4e5b331de1ab843d0f0fae51e53e2a011f0120f4c26638e8b9736b9ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportedLanguageCodes", value)

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a60a74ebc2d61e20780b51fd6e21558a214487625a399fb079862df69f84431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "default_language_code": "defaultLanguageCode",
        "display_name": "displayName",
        "location": "location",
        "time_zone": "timeZone",
        "avatar_uri": "avatarUri",
        "description": "description",
        "enable_spell_correction": "enableSpellCorrection",
        "enable_stackdriver_logging": "enableStackdriverLogging",
        "id": "id",
        "project": "project",
        "security_settings": "securitySettings",
        "speech_to_text_settings": "speechToTextSettings",
        "supported_language_codes": "supportedLanguageCodes",
        "timeouts": "timeouts",
    },
)
class DialogflowCxAgentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        default_language_code: builtins.str,
        display_name: builtins.str,
        location: builtins.str,
        time_zone: builtins.str,
        avatar_uri: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_spell_correction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        security_settings: typing.Optional[builtins.str] = None,
        speech_to_text_settings: typing.Optional[typing.Union["DialogflowCxAgentSpeechToTextSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        supported_language_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DialogflowCxAgentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param default_language_code: The default language of the agent as a language tag. `See Language Support <https://cloud.google.com/dialogflow/cx/docs/reference/language>`_ for a list of the currently supported language codes. This field cannot be updated after creation. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#default_language_code DialogflowCxAgent#default_language_code}
        :param display_name: The human-readable name of the agent, unique within the location. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#display_name DialogflowCxAgent#display_name}
        :param location: The name of the location this agent is located in. ~> **Note:** The first time you are deploying an Agent in your project you must configure location settings. This is a one time step but at the moment you can only `configure location settings <https://cloud.google.com/dialogflow/cx/docs/concept/region#location-settings>`_ via the Dialogflow CX console. Another options is to use global location so you don't need to manually configure location settings. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#location DialogflowCxAgent#location}
        :param time_zone: The time zone of this agent from the `time zone database <https://www.iana.org/time-zones>`_, e.g., America/New_York, Europe/Paris. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#time_zone DialogflowCxAgent#time_zone}
        :param avatar_uri: The URI of the agent's avatar. Avatars are used throughout the Dialogflow console and in the self-hosted Web Demo integration. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#avatar_uri DialogflowCxAgent#avatar_uri}
        :param description: The description of this agent. The maximum length is 500 characters. If exceeded, the request is rejected. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#description DialogflowCxAgent#description}
        :param enable_spell_correction: Indicates if automatic spell correction is enabled in detect intent requests. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#enable_spell_correction DialogflowCxAgent#enable_spell_correction}
        :param enable_stackdriver_logging: Determines whether this agent should log conversation queries. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#enable_stackdriver_logging DialogflowCxAgent#enable_stackdriver_logging}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#id DialogflowCxAgent#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#project DialogflowCxAgent#project}.
        :param security_settings: Name of the SecuritySettings reference for the agent. Format: projects//locations//securitySettings/. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#security_settings DialogflowCxAgent#security_settings}
        :param speech_to_text_settings: speech_to_text_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#speech_to_text_settings DialogflowCxAgent#speech_to_text_settings}
        :param supported_language_codes: The list of all languages supported by this agent (except for the default_language_code). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#supported_language_codes DialogflowCxAgent#supported_language_codes}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#timeouts DialogflowCxAgent#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(speech_to_text_settings, dict):
            speech_to_text_settings = DialogflowCxAgentSpeechToTextSettings(**speech_to_text_settings)
        if isinstance(timeouts, dict):
            timeouts = DialogflowCxAgentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1cdc3ec5885cae236dbed1fab750af37905b761eb071a01995f6899822650c1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument default_language_code", value=default_language_code, expected_type=type_hints["default_language_code"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument avatar_uri", value=avatar_uri, expected_type=type_hints["avatar_uri"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_spell_correction", value=enable_spell_correction, expected_type=type_hints["enable_spell_correction"])
            check_type(argname="argument enable_stackdriver_logging", value=enable_stackdriver_logging, expected_type=type_hints["enable_stackdriver_logging"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument security_settings", value=security_settings, expected_type=type_hints["security_settings"])
            check_type(argname="argument speech_to_text_settings", value=speech_to_text_settings, expected_type=type_hints["speech_to_text_settings"])
            check_type(argname="argument supported_language_codes", value=supported_language_codes, expected_type=type_hints["supported_language_codes"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_language_code": default_language_code,
            "display_name": display_name,
            "location": location,
            "time_zone": time_zone,
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
        if avatar_uri is not None:
            self._values["avatar_uri"] = avatar_uri
        if description is not None:
            self._values["description"] = description
        if enable_spell_correction is not None:
            self._values["enable_spell_correction"] = enable_spell_correction
        if enable_stackdriver_logging is not None:
            self._values["enable_stackdriver_logging"] = enable_stackdriver_logging
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if security_settings is not None:
            self._values["security_settings"] = security_settings
        if speech_to_text_settings is not None:
            self._values["speech_to_text_settings"] = speech_to_text_settings
        if supported_language_codes is not None:
            self._values["supported_language_codes"] = supported_language_codes
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
    def default_language_code(self) -> builtins.str:
        '''The default language of the agent as a language tag.

        `See Language Support <https://cloud.google.com/dialogflow/cx/docs/reference/language>`_
        for a list of the currently supported language codes. This field cannot be updated after creation.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#default_language_code DialogflowCxAgent#default_language_code}
        '''
        result = self._values.get("default_language_code")
        assert result is not None, "Required property 'default_language_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The human-readable name of the agent, unique within the location.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#display_name DialogflowCxAgent#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The name of the location this agent is located in.

        ~> **Note:** The first time you are deploying an Agent in your project you must configure location settings.
        This is a one time step but at the moment you can only `configure location settings <https://cloud.google.com/dialogflow/cx/docs/concept/region#location-settings>`_ via the Dialogflow CX console.
        Another options is to use global location so you don't need to manually configure location settings.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#location DialogflowCxAgent#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''The time zone of this agent from the `time zone database <https://www.iana.org/time-zones>`_, e.g., America/New_York, Europe/Paris.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#time_zone DialogflowCxAgent#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def avatar_uri(self) -> typing.Optional[builtins.str]:
        '''The URI of the agent's avatar.

        Avatars are used throughout the Dialogflow console and in the self-hosted Web Demo integration.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#avatar_uri DialogflowCxAgent#avatar_uri}
        '''
        result = self._values.get("avatar_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of this agent. The maximum length is 500 characters. If exceeded, the request is rejected.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#description DialogflowCxAgent#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_spell_correction(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if automatic spell correction is enabled in detect intent requests.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#enable_spell_correction DialogflowCxAgent#enable_spell_correction}
        '''
        result = self._values.get("enable_spell_correction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_stackdriver_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether this agent should log conversation queries.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#enable_stackdriver_logging DialogflowCxAgent#enable_stackdriver_logging}
        '''
        result = self._values.get("enable_stackdriver_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#id DialogflowCxAgent#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#project DialogflowCxAgent#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_settings(self) -> typing.Optional[builtins.str]:
        '''Name of the SecuritySettings reference for the agent. Format: projects//locations//securitySettings/.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#security_settings DialogflowCxAgent#security_settings}
        '''
        result = self._values.get("security_settings")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def speech_to_text_settings(
        self,
    ) -> typing.Optional["DialogflowCxAgentSpeechToTextSettings"]:
        '''speech_to_text_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#speech_to_text_settings DialogflowCxAgent#speech_to_text_settings}
        '''
        result = self._values.get("speech_to_text_settings")
        return typing.cast(typing.Optional["DialogflowCxAgentSpeechToTextSettings"], result)

    @builtins.property
    def supported_language_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of all languages supported by this agent (except for the default_language_code).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#supported_language_codes DialogflowCxAgent#supported_language_codes}
        '''
        result = self._values.get("supported_language_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DialogflowCxAgentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#timeouts DialogflowCxAgent#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DialogflowCxAgentTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxAgentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentSpeechToTextSettings",
    jsii_struct_bases=[],
    name_mapping={"enable_speech_adaptation": "enableSpeechAdaptation"},
)
class DialogflowCxAgentSpeechToTextSettings:
    def __init__(
        self,
        *,
        enable_speech_adaptation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_speech_adaptation: Whether to use speech adaptation for speech recognition. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#enable_speech_adaptation DialogflowCxAgent#enable_speech_adaptation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__926b122006c1e9e79ed70f35af2ca75f677a1b35d30fb4abc783d008593f0235)
            check_type(argname="argument enable_speech_adaptation", value=enable_speech_adaptation, expected_type=type_hints["enable_speech_adaptation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_speech_adaptation is not None:
            self._values["enable_speech_adaptation"] = enable_speech_adaptation

    @builtins.property
    def enable_speech_adaptation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to use speech adaptation for speech recognition.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#enable_speech_adaptation DialogflowCxAgent#enable_speech_adaptation}
        '''
        result = self._values.get("enable_speech_adaptation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxAgentSpeechToTextSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxAgentSpeechToTextSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentSpeechToTextSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb2ecd0f6bbafc8dc303cdd31134cfec04fabc59ecaa036749a0d95d691e902a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableSpeechAdaptation")
    def reset_enable_speech_adaptation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSpeechAdaptation", []))

    @builtins.property
    @jsii.member(jsii_name="enableSpeechAdaptationInput")
    def enable_speech_adaptation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSpeechAdaptationInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSpeechAdaptation")
    def enable_speech_adaptation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSpeechAdaptation"))

    @enable_speech_adaptation.setter
    def enable_speech_adaptation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__816e3fee077b167014c315711d9aff35c88055a32c3086a5d283e895271388d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSpeechAdaptation", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DialogflowCxAgentSpeechToTextSettings]:
        return typing.cast(typing.Optional[DialogflowCxAgentSpeechToTextSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxAgentSpeechToTextSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b19c56ebbd32d78350855cfefdcdbdc1251faf121f20d99f72c2c69480b359a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DialogflowCxAgentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#create DialogflowCxAgent#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#delete DialogflowCxAgent#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#update DialogflowCxAgent#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__834b92cd0c3b54b3a5968d7f7e2f1ac5dbe76dd39697e902d2da8a83550223ce)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#create DialogflowCxAgent#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#delete DialogflowCxAgent#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dialogflow_cx_agent#update DialogflowCxAgent#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxAgentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxAgentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dbd1125069a82588014a0569e709f5ee3fe4249fd3d64197c306052f14b2c7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb40cfb7e89d43f5409927bfe09b5942fa74f192bf8388d8f962ef92f85f1d21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce7d6e4255f0c54e113ce3664351548279d771836fffee79c1f849e5b803c6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56fea1942b835f8ccb7fd81cb2425d18583bb4c543407a018555292414c58194)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DialogflowCxAgentTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DialogflowCxAgentTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DialogflowCxAgentTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b363813d9730e14a97601d4d9dec551302278221e30803ee54b291d9d6c86e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DialogflowCxAgent",
    "DialogflowCxAgentConfig",
    "DialogflowCxAgentSpeechToTextSettings",
    "DialogflowCxAgentSpeechToTextSettingsOutputReference",
    "DialogflowCxAgentTimeouts",
    "DialogflowCxAgentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__61bc8ebf23753dd057cb6e8d4f9cd853d22b0db49b9c2922bb276b018421e905(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_language_code: builtins.str,
    display_name: builtins.str,
    location: builtins.str,
    time_zone: builtins.str,
    avatar_uri: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_spell_correction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    security_settings: typing.Optional[builtins.str] = None,
    speech_to_text_settings: typing.Optional[typing.Union[DialogflowCxAgentSpeechToTextSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    supported_language_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DialogflowCxAgentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3f8342ecdcceb1cabba42fe56e31dbc4a14507bfaef9856c10796f591d512b1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bc0b4ccf9181d2f9f6f678eeef3eeb36a64dc0fcc331c10be266fd624efb683(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40be0b053fa106e7cd28a68719bed0f75eb5e745376e20a1cce3dbf10d3d3ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76cde625c357c697363055d9778903f7556f2ff4429366505dec0397319438e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__852f9a4bbdb359fce82d94e4ec9e1c19a2a3ce9055173ebf9741fb32ad338082(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9076bdd2a578519759a083b967238a1fe8a7f22236ea2c5546cb7be1b4f5ab77(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af559d9afdf65e776615de7bfe4984ce199773f4928c7767ebaa0b61d6755470(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6144bab910f257b0b948dc47375128bd670cae3fe3c17b8ecd25584c51b849e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1cc79a9c1491ecf859c84adc5762c52f705c16b40203907edf7ffb4320f9bb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c7b967aea01cb6fb2707be603fb0bbf07ed6b9f53a43f099002cd5e7c81ff8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa74fce4e5b331de1ab843d0f0fae51e53e2a011f0120f4c26638e8b9736b9ca(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a60a74ebc2d61e20780b51fd6e21558a214487625a399fb079862df69f84431(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1cdc3ec5885cae236dbed1fab750af37905b761eb071a01995f6899822650c1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_language_code: builtins.str,
    display_name: builtins.str,
    location: builtins.str,
    time_zone: builtins.str,
    avatar_uri: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_spell_correction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    security_settings: typing.Optional[builtins.str] = None,
    speech_to_text_settings: typing.Optional[typing.Union[DialogflowCxAgentSpeechToTextSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    supported_language_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DialogflowCxAgentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__926b122006c1e9e79ed70f35af2ca75f677a1b35d30fb4abc783d008593f0235(
    *,
    enable_speech_adaptation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb2ecd0f6bbafc8dc303cdd31134cfec04fabc59ecaa036749a0d95d691e902a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816e3fee077b167014c315711d9aff35c88055a32c3086a5d283e895271388d7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b19c56ebbd32d78350855cfefdcdbdc1251faf121f20d99f72c2c69480b359a(
    value: typing.Optional[DialogflowCxAgentSpeechToTextSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__834b92cd0c3b54b3a5968d7f7e2f1ac5dbe76dd39697e902d2da8a83550223ce(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dbd1125069a82588014a0569e709f5ee3fe4249fd3d64197c306052f14b2c7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb40cfb7e89d43f5409927bfe09b5942fa74f192bf8388d8f962ef92f85f1d21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce7d6e4255f0c54e113ce3664351548279d771836fffee79c1f849e5b803c6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56fea1942b835f8ccb7fd81cb2425d18583bb4c543407a018555292414c58194(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b363813d9730e14a97601d4d9dec551302278221e30803ee54b291d9d6c86e1(
    value: typing.Optional[typing.Union[DialogflowCxAgentTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
