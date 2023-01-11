'''
# `cloudflare_record`

Refer to the Terraform Registory for docs: [`cloudflare_record`](https://www.terraform.io/docs/providers/cloudflare/r/record).
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


class Record(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.record.Record",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/record cloudflare_record}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        type: builtins.str,
        zone_id: builtins.str,
        allow_overwrite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        comment: typing.Optional[builtins.str] = None,
        data: typing.Optional[typing.Union["RecordData", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        proxied: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["RecordTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        ttl: typing.Optional[jsii.Number] = None,
        value: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/record cloudflare_record} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the record. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#name Record#name}
        :param type: The type of the record. Available values: ``A``, ``AAAA``, ``CAA``, ``CNAME``, ``TXT``, ``SRV``, ``LOC``, ``MX``, ``NS``, ``SPF``, ``CERT``, ``DNSKEY``, ``DS``, ``NAPTR``, ``SMIMEA``, ``SSHFP``, ``TLSA``, ``URI``, ``PTR``, ``HTTPS``. **Modifying this attribute will force creation of a new resource.** Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#type Record#type}
        :param zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#zone_id Record#zone_id}
        :param allow_overwrite: Allow creation of this record in Terraform to overwrite an existing record, if any. This does not affect the ability to update the record in Terraform and does not prevent other resources within Terraform or manual changes outside Terraform from overwriting this record. **This configuration is not recommended for most environments**. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#allow_overwrite Record#allow_overwrite}
        :param comment: Comments or notes about the DNS record. This field has no effect on DNS responses. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#comment Record#comment}
        :param data: data block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#data Record#data}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#id Record#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param priority: The priority of the record. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#priority Record#priority}
        :param proxied: Whether the record gets Cloudflare's origin protection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#proxied Record#proxied}
        :param tags: Custom tags for the DNS record. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#tags Record#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#timeouts Record#timeouts}
        :param ttl: The TTL of the record. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#ttl Record#ttl}
        :param value: The value of the record. Conflicts with ``data``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#value Record#value}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e30bb816a443df7011bc7b7cf7799d5a300ac18fa931a88b3f3510637015e14)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RecordConfig(
            name=name,
            type=type,
            zone_id=zone_id,
            allow_overwrite=allow_overwrite,
            comment=comment,
            data=data,
            id=id,
            priority=priority,
            proxied=proxied,
            tags=tags,
            timeouts=timeouts,
            ttl=ttl,
            value=value,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putData")
    def put_data(
        self,
        *,
        algorithm: typing.Optional[jsii.Number] = None,
        altitude: typing.Optional[jsii.Number] = None,
        certificate: typing.Optional[builtins.str] = None,
        content: typing.Optional[builtins.str] = None,
        digest: typing.Optional[builtins.str] = None,
        digest_type: typing.Optional[jsii.Number] = None,
        fingerprint: typing.Optional[builtins.str] = None,
        flags: typing.Optional[builtins.str] = None,
        key_tag: typing.Optional[jsii.Number] = None,
        lat_degrees: typing.Optional[jsii.Number] = None,
        lat_direction: typing.Optional[builtins.str] = None,
        lat_minutes: typing.Optional[jsii.Number] = None,
        lat_seconds: typing.Optional[jsii.Number] = None,
        long_degrees: typing.Optional[jsii.Number] = None,
        long_direction: typing.Optional[builtins.str] = None,
        long_minutes: typing.Optional[jsii.Number] = None,
        long_seconds: typing.Optional[jsii.Number] = None,
        matching_type: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        order: typing.Optional[jsii.Number] = None,
        port: typing.Optional[jsii.Number] = None,
        precision_horz: typing.Optional[jsii.Number] = None,
        precision_vert: typing.Optional[jsii.Number] = None,
        preference: typing.Optional[jsii.Number] = None,
        priority: typing.Optional[jsii.Number] = None,
        proto: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[jsii.Number] = None,
        public_key: typing.Optional[builtins.str] = None,
        regex: typing.Optional[builtins.str] = None,
        replacement: typing.Optional[builtins.str] = None,
        selector: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
        size: typing.Optional[jsii.Number] = None,
        tag: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        type: typing.Optional[jsii.Number] = None,
        usage: typing.Optional[jsii.Number] = None,
        value: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param algorithm: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#algorithm Record#algorithm}.
        :param altitude: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#altitude Record#altitude}.
        :param certificate: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#certificate Record#certificate}.
        :param content: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#content Record#content}.
        :param digest: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#digest Record#digest}.
        :param digest_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#digest_type Record#digest_type}.
        :param fingerprint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#fingerprint Record#fingerprint}.
        :param flags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#flags Record#flags}.
        :param key_tag: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#key_tag Record#key_tag}.
        :param lat_degrees: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#lat_degrees Record#lat_degrees}.
        :param lat_direction: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#lat_direction Record#lat_direction}.
        :param lat_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#lat_minutes Record#lat_minutes}.
        :param lat_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#lat_seconds Record#lat_seconds}.
        :param long_degrees: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#long_degrees Record#long_degrees}.
        :param long_direction: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#long_direction Record#long_direction}.
        :param long_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#long_minutes Record#long_minutes}.
        :param long_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#long_seconds Record#long_seconds}.
        :param matching_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#matching_type Record#matching_type}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#name Record#name}.
        :param order: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#order Record#order}.
        :param port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#port Record#port}.
        :param precision_horz: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#precision_horz Record#precision_horz}.
        :param precision_vert: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#precision_vert Record#precision_vert}.
        :param preference: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#preference Record#preference}.
        :param priority: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#priority Record#priority}.
        :param proto: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#proto Record#proto}.
        :param protocol: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#protocol Record#protocol}.
        :param public_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#public_key Record#public_key}.
        :param regex: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#regex Record#regex}.
        :param replacement: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#replacement Record#replacement}.
        :param selector: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#selector Record#selector}.
        :param service: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#service Record#service}.
        :param size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#size Record#size}.
        :param tag: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#tag Record#tag}.
        :param target: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#target Record#target}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#type Record#type}.
        :param usage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#usage Record#usage}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#value Record#value}.
        :param weight: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#weight Record#weight}.
        '''
        value_ = RecordData(
            algorithm=algorithm,
            altitude=altitude,
            certificate=certificate,
            content=content,
            digest=digest,
            digest_type=digest_type,
            fingerprint=fingerprint,
            flags=flags,
            key_tag=key_tag,
            lat_degrees=lat_degrees,
            lat_direction=lat_direction,
            lat_minutes=lat_minutes,
            lat_seconds=lat_seconds,
            long_degrees=long_degrees,
            long_direction=long_direction,
            long_minutes=long_minutes,
            long_seconds=long_seconds,
            matching_type=matching_type,
            name=name,
            order=order,
            port=port,
            precision_horz=precision_horz,
            precision_vert=precision_vert,
            preference=preference,
            priority=priority,
            proto=proto,
            protocol=protocol,
            public_key=public_key,
            regex=regex,
            replacement=replacement,
            selector=selector,
            service=service,
            size=size,
            tag=tag,
            target=target,
            type=type,
            usage=usage,
            value=value,
            weight=weight,
        )

        return typing.cast(None, jsii.invoke(self, "putData", [value_]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#create Record#create}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#update Record#update}.
        '''
        value = RecordTimeouts(create=create, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAllowOverwrite")
    def reset_allow_overwrite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowOverwrite", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetProxied")
    def reset_proxied(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxied", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTtl")
    def reset_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtl", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> "RecordDataOutputReference":
        return typing.cast("RecordDataOutputReference", jsii.get(self, "data"))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="modifiedOn")
    def modified_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modifiedOn"))

    @builtins.property
    @jsii.member(jsii_name="proxiable")
    def proxiable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "proxiable"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "RecordTimeoutsOutputReference":
        return typing.cast("RecordTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="allowOverwriteInput")
    def allow_overwrite_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowOverwriteInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional["RecordData"]:
        return typing.cast(typing.Optional["RecordData"], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="proxiedInput")
    def proxied_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "proxiedInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["RecordTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["RecordTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="allowOverwrite")
    def allow_overwrite(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowOverwrite"))

    @allow_overwrite.setter
    def allow_overwrite(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e16e22f768dff59cb0d815e13c1b52daf07cc3b4260aa8b2ab0fc1ea8f3b817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowOverwrite", value)

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fecf0799eaea1f1dbc69a1b2df4de7f1e603cf2ed85bdb280ac568306c9f21b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e05967b3b54e63e1357ca3f260b08fab790301ec575f21356f1655ae9b2708b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29851d13f2e57a35ef0bebdcf95ac9f43f6037c84dd9c74e00df9ad3e557b08d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4bf08c1145f96cbfbab333cd21402cce850b6e611b9a7a106af6d9802a0fbfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="proxied")
    def proxied(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "proxied"))

    @proxied.setter
    def proxied(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95a218c857c838b2458c83373bdcbb20fe6d414da58d3f1426f7d5baad02b784)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxied", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d024deeda8b7d24f9e750b58489879aabd62f7b02262ee136d4e76cc942f3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9db7ff37d93ae322489ac4311d5a0200f2af87e146964b577741eccf4acacc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c71ff9a4310514389161510e3654d8f20352156a40b2ec8fb10b8f0104a7bed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1acb7eeaed5715a2226c171bf69bef6c9e0733efbca90d84cf32092634b39c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7a585b540ed022806d9086c042f67de1b1e119de17840462b36f558334798b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.record.RecordConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "type": "type",
        "zone_id": "zoneId",
        "allow_overwrite": "allowOverwrite",
        "comment": "comment",
        "data": "data",
        "id": "id",
        "priority": "priority",
        "proxied": "proxied",
        "tags": "tags",
        "timeouts": "timeouts",
        "ttl": "ttl",
        "value": "value",
    },
)
class RecordConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        type: builtins.str,
        zone_id: builtins.str,
        allow_overwrite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        comment: typing.Optional[builtins.str] = None,
        data: typing.Optional[typing.Union["RecordData", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        proxied: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["RecordTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        ttl: typing.Optional[jsii.Number] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the record. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#name Record#name}
        :param type: The type of the record. Available values: ``A``, ``AAAA``, ``CAA``, ``CNAME``, ``TXT``, ``SRV``, ``LOC``, ``MX``, ``NS``, ``SPF``, ``CERT``, ``DNSKEY``, ``DS``, ``NAPTR``, ``SMIMEA``, ``SSHFP``, ``TLSA``, ``URI``, ``PTR``, ``HTTPS``. **Modifying this attribute will force creation of a new resource.** Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#type Record#type}
        :param zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#zone_id Record#zone_id}
        :param allow_overwrite: Allow creation of this record in Terraform to overwrite an existing record, if any. This does not affect the ability to update the record in Terraform and does not prevent other resources within Terraform or manual changes outside Terraform from overwriting this record. **This configuration is not recommended for most environments**. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#allow_overwrite Record#allow_overwrite}
        :param comment: Comments or notes about the DNS record. This field has no effect on DNS responses. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#comment Record#comment}
        :param data: data block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#data Record#data}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#id Record#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param priority: The priority of the record. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#priority Record#priority}
        :param proxied: Whether the record gets Cloudflare's origin protection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#proxied Record#proxied}
        :param tags: Custom tags for the DNS record. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#tags Record#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#timeouts Record#timeouts}
        :param ttl: The TTL of the record. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#ttl Record#ttl}
        :param value: The value of the record. Conflicts with ``data``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#value Record#value}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(data, dict):
            data = RecordData(**data)
        if isinstance(timeouts, dict):
            timeouts = RecordTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d9fa4b37954cdc103d1674eb12249e97339db9078ca2576accf379f0f3005bf)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
            check_type(argname="argument allow_overwrite", value=allow_overwrite, expected_type=type_hints["allow_overwrite"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument proxied", value=proxied, expected_type=type_hints["proxied"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
            "zone_id": zone_id,
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
        if allow_overwrite is not None:
            self._values["allow_overwrite"] = allow_overwrite
        if comment is not None:
            self._values["comment"] = comment
        if data is not None:
            self._values["data"] = data
        if id is not None:
            self._values["id"] = id
        if priority is not None:
            self._values["priority"] = priority
        if proxied is not None:
            self._values["proxied"] = proxied
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if ttl is not None:
            self._values["ttl"] = ttl
        if value is not None:
            self._values["value"] = value

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
    def name(self) -> builtins.str:
        '''The name of the record. **Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#name Record#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of the record.

        Available values: ``A``, ``AAAA``, ``CAA``, ``CNAME``, ``TXT``, ``SRV``, ``LOC``, ``MX``, ``NS``, ``SPF``, ``CERT``, ``DNSKEY``, ``DS``, ``NAPTR``, ``SMIMEA``, ``SSHFP``, ``TLSA``, ``URI``, ``PTR``, ``HTTPS``. **Modifying this attribute will force creation of a new resource.**

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#type Record#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def zone_id(self) -> builtins.str:
        '''The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#zone_id Record#zone_id}
        '''
        result = self._values.get("zone_id")
        assert result is not None, "Required property 'zone_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_overwrite(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow creation of this record in Terraform to overwrite an existing record, if any.

        This does not affect the ability to update the record in Terraform and does not prevent other resources within Terraform or manual changes outside Terraform from overwriting this record. **This configuration is not recommended for most environments**. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#allow_overwrite Record#allow_overwrite}
        '''
        result = self._values.get("allow_overwrite")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Comments or notes about the DNS record. This field has no effect on DNS responses.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#comment Record#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional["RecordData"]:
        '''data block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#data Record#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional["RecordData"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#id Record#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''The priority of the record.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#priority Record#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def proxied(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the record gets Cloudflare's origin protection.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#proxied Record#proxied}
        '''
        result = self._values.get("proxied")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Custom tags for the DNS record.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#tags Record#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["RecordTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#timeouts Record#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["RecordTimeouts"], result)

    @builtins.property
    def ttl(self) -> typing.Optional[jsii.Number]:
        '''The TTL of the record.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#ttl Record#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The value of the record. Conflicts with ``data``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#value Record#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RecordConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.record.RecordData",
    jsii_struct_bases=[],
    name_mapping={
        "algorithm": "algorithm",
        "altitude": "altitude",
        "certificate": "certificate",
        "content": "content",
        "digest": "digest",
        "digest_type": "digestType",
        "fingerprint": "fingerprint",
        "flags": "flags",
        "key_tag": "keyTag",
        "lat_degrees": "latDegrees",
        "lat_direction": "latDirection",
        "lat_minutes": "latMinutes",
        "lat_seconds": "latSeconds",
        "long_degrees": "longDegrees",
        "long_direction": "longDirection",
        "long_minutes": "longMinutes",
        "long_seconds": "longSeconds",
        "matching_type": "matchingType",
        "name": "name",
        "order": "order",
        "port": "port",
        "precision_horz": "precisionHorz",
        "precision_vert": "precisionVert",
        "preference": "preference",
        "priority": "priority",
        "proto": "proto",
        "protocol": "protocol",
        "public_key": "publicKey",
        "regex": "regex",
        "replacement": "replacement",
        "selector": "selector",
        "service": "service",
        "size": "size",
        "tag": "tag",
        "target": "target",
        "type": "type",
        "usage": "usage",
        "value": "value",
        "weight": "weight",
    },
)
class RecordData:
    def __init__(
        self,
        *,
        algorithm: typing.Optional[jsii.Number] = None,
        altitude: typing.Optional[jsii.Number] = None,
        certificate: typing.Optional[builtins.str] = None,
        content: typing.Optional[builtins.str] = None,
        digest: typing.Optional[builtins.str] = None,
        digest_type: typing.Optional[jsii.Number] = None,
        fingerprint: typing.Optional[builtins.str] = None,
        flags: typing.Optional[builtins.str] = None,
        key_tag: typing.Optional[jsii.Number] = None,
        lat_degrees: typing.Optional[jsii.Number] = None,
        lat_direction: typing.Optional[builtins.str] = None,
        lat_minutes: typing.Optional[jsii.Number] = None,
        lat_seconds: typing.Optional[jsii.Number] = None,
        long_degrees: typing.Optional[jsii.Number] = None,
        long_direction: typing.Optional[builtins.str] = None,
        long_minutes: typing.Optional[jsii.Number] = None,
        long_seconds: typing.Optional[jsii.Number] = None,
        matching_type: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        order: typing.Optional[jsii.Number] = None,
        port: typing.Optional[jsii.Number] = None,
        precision_horz: typing.Optional[jsii.Number] = None,
        precision_vert: typing.Optional[jsii.Number] = None,
        preference: typing.Optional[jsii.Number] = None,
        priority: typing.Optional[jsii.Number] = None,
        proto: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[jsii.Number] = None,
        public_key: typing.Optional[builtins.str] = None,
        regex: typing.Optional[builtins.str] = None,
        replacement: typing.Optional[builtins.str] = None,
        selector: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
        size: typing.Optional[jsii.Number] = None,
        tag: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        type: typing.Optional[jsii.Number] = None,
        usage: typing.Optional[jsii.Number] = None,
        value: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param algorithm: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#algorithm Record#algorithm}.
        :param altitude: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#altitude Record#altitude}.
        :param certificate: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#certificate Record#certificate}.
        :param content: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#content Record#content}.
        :param digest: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#digest Record#digest}.
        :param digest_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#digest_type Record#digest_type}.
        :param fingerprint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#fingerprint Record#fingerprint}.
        :param flags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#flags Record#flags}.
        :param key_tag: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#key_tag Record#key_tag}.
        :param lat_degrees: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#lat_degrees Record#lat_degrees}.
        :param lat_direction: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#lat_direction Record#lat_direction}.
        :param lat_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#lat_minutes Record#lat_minutes}.
        :param lat_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#lat_seconds Record#lat_seconds}.
        :param long_degrees: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#long_degrees Record#long_degrees}.
        :param long_direction: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#long_direction Record#long_direction}.
        :param long_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#long_minutes Record#long_minutes}.
        :param long_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#long_seconds Record#long_seconds}.
        :param matching_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#matching_type Record#matching_type}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#name Record#name}.
        :param order: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#order Record#order}.
        :param port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#port Record#port}.
        :param precision_horz: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#precision_horz Record#precision_horz}.
        :param precision_vert: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#precision_vert Record#precision_vert}.
        :param preference: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#preference Record#preference}.
        :param priority: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#priority Record#priority}.
        :param proto: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#proto Record#proto}.
        :param protocol: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#protocol Record#protocol}.
        :param public_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#public_key Record#public_key}.
        :param regex: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#regex Record#regex}.
        :param replacement: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#replacement Record#replacement}.
        :param selector: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#selector Record#selector}.
        :param service: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#service Record#service}.
        :param size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#size Record#size}.
        :param tag: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#tag Record#tag}.
        :param target: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#target Record#target}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#type Record#type}.
        :param usage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#usage Record#usage}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#value Record#value}.
        :param weight: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#weight Record#weight}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c216bfe8b351eb45e7e0937bdc7b9801083b3c5d28a8d836e8c7ff09f0020a0)
            check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
            check_type(argname="argument altitude", value=altitude, expected_type=type_hints["altitude"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument digest", value=digest, expected_type=type_hints["digest"])
            check_type(argname="argument digest_type", value=digest_type, expected_type=type_hints["digest_type"])
            check_type(argname="argument fingerprint", value=fingerprint, expected_type=type_hints["fingerprint"])
            check_type(argname="argument flags", value=flags, expected_type=type_hints["flags"])
            check_type(argname="argument key_tag", value=key_tag, expected_type=type_hints["key_tag"])
            check_type(argname="argument lat_degrees", value=lat_degrees, expected_type=type_hints["lat_degrees"])
            check_type(argname="argument lat_direction", value=lat_direction, expected_type=type_hints["lat_direction"])
            check_type(argname="argument lat_minutes", value=lat_minutes, expected_type=type_hints["lat_minutes"])
            check_type(argname="argument lat_seconds", value=lat_seconds, expected_type=type_hints["lat_seconds"])
            check_type(argname="argument long_degrees", value=long_degrees, expected_type=type_hints["long_degrees"])
            check_type(argname="argument long_direction", value=long_direction, expected_type=type_hints["long_direction"])
            check_type(argname="argument long_minutes", value=long_minutes, expected_type=type_hints["long_minutes"])
            check_type(argname="argument long_seconds", value=long_seconds, expected_type=type_hints["long_seconds"])
            check_type(argname="argument matching_type", value=matching_type, expected_type=type_hints["matching_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument precision_horz", value=precision_horz, expected_type=type_hints["precision_horz"])
            check_type(argname="argument precision_vert", value=precision_vert, expected_type=type_hints["precision_vert"])
            check_type(argname="argument preference", value=preference, expected_type=type_hints["preference"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument proto", value=proto, expected_type=type_hints["proto"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument public_key", value=public_key, expected_type=type_hints["public_key"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument replacement", value=replacement, expected_type=type_hints["replacement"])
            check_type(argname="argument selector", value=selector, expected_type=type_hints["selector"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument usage", value=usage, expected_type=type_hints["usage"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if algorithm is not None:
            self._values["algorithm"] = algorithm
        if altitude is not None:
            self._values["altitude"] = altitude
        if certificate is not None:
            self._values["certificate"] = certificate
        if content is not None:
            self._values["content"] = content
        if digest is not None:
            self._values["digest"] = digest
        if digest_type is not None:
            self._values["digest_type"] = digest_type
        if fingerprint is not None:
            self._values["fingerprint"] = fingerprint
        if flags is not None:
            self._values["flags"] = flags
        if key_tag is not None:
            self._values["key_tag"] = key_tag
        if lat_degrees is not None:
            self._values["lat_degrees"] = lat_degrees
        if lat_direction is not None:
            self._values["lat_direction"] = lat_direction
        if lat_minutes is not None:
            self._values["lat_minutes"] = lat_minutes
        if lat_seconds is not None:
            self._values["lat_seconds"] = lat_seconds
        if long_degrees is not None:
            self._values["long_degrees"] = long_degrees
        if long_direction is not None:
            self._values["long_direction"] = long_direction
        if long_minutes is not None:
            self._values["long_minutes"] = long_minutes
        if long_seconds is not None:
            self._values["long_seconds"] = long_seconds
        if matching_type is not None:
            self._values["matching_type"] = matching_type
        if name is not None:
            self._values["name"] = name
        if order is not None:
            self._values["order"] = order
        if port is not None:
            self._values["port"] = port
        if precision_horz is not None:
            self._values["precision_horz"] = precision_horz
        if precision_vert is not None:
            self._values["precision_vert"] = precision_vert
        if preference is not None:
            self._values["preference"] = preference
        if priority is not None:
            self._values["priority"] = priority
        if proto is not None:
            self._values["proto"] = proto
        if protocol is not None:
            self._values["protocol"] = protocol
        if public_key is not None:
            self._values["public_key"] = public_key
        if regex is not None:
            self._values["regex"] = regex
        if replacement is not None:
            self._values["replacement"] = replacement
        if selector is not None:
            self._values["selector"] = selector
        if service is not None:
            self._values["service"] = service
        if size is not None:
            self._values["size"] = size
        if tag is not None:
            self._values["tag"] = tag
        if target is not None:
            self._values["target"] = target
        if type is not None:
            self._values["type"] = type
        if usage is not None:
            self._values["usage"] = usage
        if value is not None:
            self._values["value"] = value
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def algorithm(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#algorithm Record#algorithm}.'''
        result = self._values.get("algorithm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def altitude(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#altitude Record#altitude}.'''
        result = self._values.get("altitude")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#certificate Record#certificate}.'''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#content Record#content}.'''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def digest(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#digest Record#digest}.'''
        result = self._values.get("digest")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def digest_type(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#digest_type Record#digest_type}.'''
        result = self._values.get("digest_type")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fingerprint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#fingerprint Record#fingerprint}.'''
        result = self._values.get("fingerprint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flags(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#flags Record#flags}.'''
        result = self._values.get("flags")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_tag(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#key_tag Record#key_tag}.'''
        result = self._values.get("key_tag")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lat_degrees(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#lat_degrees Record#lat_degrees}.'''
        result = self._values.get("lat_degrees")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lat_direction(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#lat_direction Record#lat_direction}.'''
        result = self._values.get("lat_direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lat_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#lat_minutes Record#lat_minutes}.'''
        result = self._values.get("lat_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lat_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#lat_seconds Record#lat_seconds}.'''
        result = self._values.get("lat_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def long_degrees(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#long_degrees Record#long_degrees}.'''
        result = self._values.get("long_degrees")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def long_direction(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#long_direction Record#long_direction}.'''
        result = self._values.get("long_direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def long_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#long_minutes Record#long_minutes}.'''
        result = self._values.get("long_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def long_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#long_seconds Record#long_seconds}.'''
        result = self._values.get("long_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def matching_type(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#matching_type Record#matching_type}.'''
        result = self._values.get("matching_type")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#name Record#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def order(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#order Record#order}.'''
        result = self._values.get("order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#port Record#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def precision_horz(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#precision_horz Record#precision_horz}.'''
        result = self._values.get("precision_horz")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def precision_vert(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#precision_vert Record#precision_vert}.'''
        result = self._values.get("precision_vert")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preference(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#preference Record#preference}.'''
        result = self._values.get("preference")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#priority Record#priority}.'''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def proto(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#proto Record#proto}.'''
        result = self._values.get("proto")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#protocol Record#protocol}.'''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def public_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#public_key Record#public_key}.'''
        result = self._values.get("public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#regex Record#regex}.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replacement(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#replacement Record#replacement}.'''
        result = self._values.get("replacement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def selector(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#selector Record#selector}.'''
        result = self._values.get("selector")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#service Record#service}.'''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#size Record#size}.'''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#tag Record#tag}.'''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#target Record#target}.'''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#type Record#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def usage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#usage Record#usage}.'''
        result = self._values.get("usage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#value Record#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#weight Record#weight}.'''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RecordData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RecordDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.record.RecordDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e81b2c17e556ec3fb61107d3816647e274f5123ceb81da830a5dbf376930f354)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAlgorithm")
    def reset_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlgorithm", []))

    @jsii.member(jsii_name="resetAltitude")
    def reset_altitude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAltitude", []))

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetContent")
    def reset_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContent", []))

    @jsii.member(jsii_name="resetDigest")
    def reset_digest(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDigest", []))

    @jsii.member(jsii_name="resetDigestType")
    def reset_digest_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDigestType", []))

    @jsii.member(jsii_name="resetFingerprint")
    def reset_fingerprint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFingerprint", []))

    @jsii.member(jsii_name="resetFlags")
    def reset_flags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlags", []))

    @jsii.member(jsii_name="resetKeyTag")
    def reset_key_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyTag", []))

    @jsii.member(jsii_name="resetLatDegrees")
    def reset_lat_degrees(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLatDegrees", []))

    @jsii.member(jsii_name="resetLatDirection")
    def reset_lat_direction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLatDirection", []))

    @jsii.member(jsii_name="resetLatMinutes")
    def reset_lat_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLatMinutes", []))

    @jsii.member(jsii_name="resetLatSeconds")
    def reset_lat_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLatSeconds", []))

    @jsii.member(jsii_name="resetLongDegrees")
    def reset_long_degrees(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongDegrees", []))

    @jsii.member(jsii_name="resetLongDirection")
    def reset_long_direction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongDirection", []))

    @jsii.member(jsii_name="resetLongMinutes")
    def reset_long_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongMinutes", []))

    @jsii.member(jsii_name="resetLongSeconds")
    def reset_long_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongSeconds", []))

    @jsii.member(jsii_name="resetMatchingType")
    def reset_matching_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchingType", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOrder")
    def reset_order(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrder", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetPrecisionHorz")
    def reset_precision_horz(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrecisionHorz", []))

    @jsii.member(jsii_name="resetPrecisionVert")
    def reset_precision_vert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrecisionVert", []))

    @jsii.member(jsii_name="resetPreference")
    def reset_preference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreference", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetProto")
    def reset_proto(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProto", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetPublicKey")
    def reset_public_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicKey", []))

    @jsii.member(jsii_name="resetRegex")
    def reset_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegex", []))

    @jsii.member(jsii_name="resetReplacement")
    def reset_replacement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplacement", []))

    @jsii.member(jsii_name="resetSelector")
    def reset_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelector", []))

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

    @jsii.member(jsii_name="resetSize")
    def reset_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSize", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUsage")
    def reset_usage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsage", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

    @builtins.property
    @jsii.member(jsii_name="algorithmInput")
    def algorithm_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "algorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="altitudeInput")
    def altitude_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "altitudeInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="digestInput")
    def digest_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "digestInput"))

    @builtins.property
    @jsii.member(jsii_name="digestTypeInput")
    def digest_type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "digestTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="fingerprintInput")
    def fingerprint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fingerprintInput"))

    @builtins.property
    @jsii.member(jsii_name="flagsInput")
    def flags_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flagsInput"))

    @builtins.property
    @jsii.member(jsii_name="keyTagInput")
    def key_tag_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keyTagInput"))

    @builtins.property
    @jsii.member(jsii_name="latDegreesInput")
    def lat_degrees_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "latDegreesInput"))

    @builtins.property
    @jsii.member(jsii_name="latDirectionInput")
    def lat_direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "latDirectionInput"))

    @builtins.property
    @jsii.member(jsii_name="latMinutesInput")
    def lat_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "latMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="latSecondsInput")
    def lat_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "latSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="longDegreesInput")
    def long_degrees_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "longDegreesInput"))

    @builtins.property
    @jsii.member(jsii_name="longDirectionInput")
    def long_direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "longDirectionInput"))

    @builtins.property
    @jsii.member(jsii_name="longMinutesInput")
    def long_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "longMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="longSecondsInput")
    def long_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "longSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchingTypeInput")
    def matching_type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "matchingTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orderInput")
    def order_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "orderInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="precisionHorzInput")
    def precision_horz_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "precisionHorzInput"))

    @builtins.property
    @jsii.member(jsii_name="precisionVertInput")
    def precision_vert_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "precisionVertInput"))

    @builtins.property
    @jsii.member(jsii_name="preferenceInput")
    def preference_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "preferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="protoInput")
    def proto_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protoInput"))

    @builtins.property
    @jsii.member(jsii_name="publicKeyInput")
    def public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="replacementInput")
    def replacement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replacementInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="usageInput")
    def usage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "usageInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="algorithm")
    def algorithm(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "algorithm"))

    @algorithm.setter
    def algorithm(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07f529e632b1d7b193264e19c46314133aeaa0d06a67dfab6d9991677ab8f4a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "algorithm", value)

    @builtins.property
    @jsii.member(jsii_name="altitude")
    def altitude(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "altitude"))

    @altitude.setter
    def altitude(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2afcb66a1894d8079b42470eb1f9d6bab4c344a6986c9d20709c14059bd70cba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "altitude", value)

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb33a0230f649b279cafc6cc26e6776302368dfc7463684862b386103c45393d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37b1d8b971b8eb7f54f7c83745359665007e185e877de3ec9f4f0e56baa566f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="digest")
    def digest(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "digest"))

    @digest.setter
    def digest(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fdc275cfff99472462561a26ae7cae17758f7dc0e90c23b1e39986a64baeade)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "digest", value)

    @builtins.property
    @jsii.member(jsii_name="digestType")
    def digest_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "digestType"))

    @digest_type.setter
    def digest_type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe37bf73a5ce67c87588d9777239c4bc50a0e83580cbfae32771d11cb155d351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "digestType", value)

    @builtins.property
    @jsii.member(jsii_name="fingerprint")
    def fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fingerprint"))

    @fingerprint.setter
    def fingerprint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dccb9bce604cb815aa63062812e0f1729415a52bffac5bd88fd559a6e4a84209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fingerprint", value)

    @builtins.property
    @jsii.member(jsii_name="flags")
    def flags(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flags"))

    @flags.setter
    def flags(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03442163938a70abceb0a66feff83aa7993d78549a0785aafb08c6da8704a6fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flags", value)

    @builtins.property
    @jsii.member(jsii_name="keyTag")
    def key_tag(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keyTag"))

    @key_tag.setter
    def key_tag(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4df5ad5813e63fdd24debc542b43e30a1c2cbca377214658d2f03bcfec8bc5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyTag", value)

    @builtins.property
    @jsii.member(jsii_name="latDegrees")
    def lat_degrees(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "latDegrees"))

    @lat_degrees.setter
    def lat_degrees(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22dc8d33b4f8442d0246058d58b783dd184e6ad4f721365a79e4d725e2050ce5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "latDegrees", value)

    @builtins.property
    @jsii.member(jsii_name="latDirection")
    def lat_direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "latDirection"))

    @lat_direction.setter
    def lat_direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab64c2efce67a890a16377962cffc7b0749a7e17ea32b02ecff4f33064d702b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "latDirection", value)

    @builtins.property
    @jsii.member(jsii_name="latMinutes")
    def lat_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "latMinutes"))

    @lat_minutes.setter
    def lat_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c98bb8a3063fb9c4d67fcdb29c16adcee282b21e8bac1a52cb2a9bb5940ccc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "latMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="latSeconds")
    def lat_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "latSeconds"))

    @lat_seconds.setter
    def lat_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43369ded08b3b44cd437fd1299b1587b43a9176b32149e25f3cb7bec9cdec3b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "latSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="longDegrees")
    def long_degrees(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "longDegrees"))

    @long_degrees.setter
    def long_degrees(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1106b653686e263bbe365fd90086013a7056c229c6f91546b3c66f77f5ae4cfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longDegrees", value)

    @builtins.property
    @jsii.member(jsii_name="longDirection")
    def long_direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "longDirection"))

    @long_direction.setter
    def long_direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99f75c62c3833f57bddc5255a149376b19e695f4d9831e10f53619140872ad59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longDirection", value)

    @builtins.property
    @jsii.member(jsii_name="longMinutes")
    def long_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "longMinutes"))

    @long_minutes.setter
    def long_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf6eb2e9645da2834188fae33f3229749b07c6014f7300b8abf20f21b4339a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="longSeconds")
    def long_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "longSeconds"))

    @long_seconds.setter
    def long_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__597eeb43ebe6b7f2b1bedf9075d15e169e2b38ec60d36b5925db97b0a93e41e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="matchingType")
    def matching_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "matchingType"))

    @matching_type.setter
    def matching_type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cc484c7ea369cda2f71e5a60bf44f63e5dd2e0c4a2c4031e13c0fe607b6002d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchingType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b6a83b9abfdc41f7e41108160c33c1e589d171a9ddb4911cea9071333421301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "order"))

    @order.setter
    def order(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50596f91cf70d0e3f3742a2ccd371f76dc34e4b1fda3bffc4c02bf6913becfe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e680b42879dcfba6612170a686d688c0da6e08d6f9cea2dee726b39b405abe38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="precisionHorz")
    def precision_horz(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "precisionHorz"))

    @precision_horz.setter
    def precision_horz(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1425145cf802ed6960adac0e31d3786e1c2da6702292f45efc50abfde2912934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "precisionHorz", value)

    @builtins.property
    @jsii.member(jsii_name="precisionVert")
    def precision_vert(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "precisionVert"))

    @precision_vert.setter
    def precision_vert(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1bdded07a30380d97fbd66e2767b69ebdd091ec5b392a1a32a89ec778be8180)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "precisionVert", value)

    @builtins.property
    @jsii.member(jsii_name="preference")
    def preference(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "preference"))

    @preference.setter
    def preference(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d27a60ba7f7222e276e2c138a3fc433bd84f065488bc7366962b77392ea2072)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preference", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cdbfac05fa02be8c3dfad8f7cc16d2c9a8c205b74094311c2dde02afe184635)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="proto")
    def proto(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proto"))

    @proto.setter
    def proto(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f69aa606a38fc6b55dcee3b319a83b01d9ec542c0c45c10309b624baf9b7bb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proto", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34c96473f06443cc1faf1200d18cad481175bcda45162c2c911ecc76463450b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="publicKey")
    def public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicKey"))

    @public_key.setter
    def public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6daaa25565128736d8a9c7b54e4e2f2cf52aedd93aa948ba5311eb9944bcd982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicKey", value)

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regex"))

    @regex.setter
    def regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f7050cbfa00aaa95bcccac73afe1c233edcda1351d6e6f86882e57bad0c6359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value)

    @builtins.property
    @jsii.member(jsii_name="replacement")
    def replacement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replacement"))

    @replacement.setter
    def replacement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd27b0f51039217530fe46811ae2485220e4939bc6b3f00afd1b9b5fb14dcbb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replacement", value)

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "selector"))

    @selector.setter
    def selector(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1cc219dd2bb64ff9b76cd05ba39ab1911a62ca5c3c4b89b81afef10c5872836)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selector", value)

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05fd4c858cb0d09dd26b9003bbe8b36b1fd82b878b8311d05a75fd1f26b95210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value)

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1dc7d3853e92f102ea25e26ba41a63c904f8417b0d5d4dec46d393f696cef23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value)

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbff154b0ffae7300e88acb08be86fc511abd10facc3745434ae5af1f146d927)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value)

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2a9e45760fbf4a3626171b3915ea2f2fc34e6f5a65ae307a504a515711a27a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "type"))

    @type.setter
    def type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05ded194fa0877d8896cc4f5c6c1d0294e96b7478bac7fe1ac8711bc217c0d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="usage")
    def usage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "usage"))

    @usage.setter
    def usage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd2b7208738e5d7f350ed1722701558847571c5ea6f4eaba6c2e37aefd901a12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usage", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42c8411aa6fb6e7f0c0a160fc52a9da01851c715e495458b8ee9da7feed3384d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2418605ae005e50a275c6fb9c5b02488026cab50e90068f20f75b31e5815a5e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RecordData]:
        return typing.cast(typing.Optional[RecordData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RecordData]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ff20c0957275dbe6df5b4031dd9b755b78dc8ea3239f35512ccfe4575645da1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.record.RecordTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "update": "update"},
)
class RecordTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#create Record#create}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#update Record#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d96b6138a969fd43081670fd4383628bfd1217e975b19e4ff120a01aa1d33e)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#create Record#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/record#update Record#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RecordTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RecordTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.record.RecordTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bb994e84bd3c03a8747e982c7ecda35fac7935f49421efd3fc4491d2e617c2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__60fafe573e0a650b4f63f38cb8b6cb16b5cef00b825e5607090bbc06ed6b6dd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13401dc1aa0946fce187bf66bbee213a0697815de74fa0c93aa64320b82d3784)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[RecordTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[RecordTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[RecordTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d9840841202379ff4ba9c8455587e1a8b9fa0b6b3f193522f09ef878a04709f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "Record",
    "RecordConfig",
    "RecordData",
    "RecordDataOutputReference",
    "RecordTimeouts",
    "RecordTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7e30bb816a443df7011bc7b7cf7799d5a300ac18fa931a88b3f3510637015e14(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    type: builtins.str,
    zone_id: builtins.str,
    allow_overwrite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    comment: typing.Optional[builtins.str] = None,
    data: typing.Optional[typing.Union[RecordData, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    proxied: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[RecordTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    ttl: typing.Optional[jsii.Number] = None,
    value: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__1e16e22f768dff59cb0d815e13c1b52daf07cc3b4260aa8b2ab0fc1ea8f3b817(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fecf0799eaea1f1dbc69a1b2df4de7f1e603cf2ed85bdb280ac568306c9f21b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e05967b3b54e63e1357ca3f260b08fab790301ec575f21356f1655ae9b2708b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29851d13f2e57a35ef0bebdcf95ac9f43f6037c84dd9c74e00df9ad3e557b08d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4bf08c1145f96cbfbab333cd21402cce850b6e611b9a7a106af6d9802a0fbfe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95a218c857c838b2458c83373bdcbb20fe6d414da58d3f1426f7d5baad02b784(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d024deeda8b7d24f9e750b58489879aabd62f7b02262ee136d4e76cc942f3c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9db7ff37d93ae322489ac4311d5a0200f2af87e146964b577741eccf4acacc0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c71ff9a4310514389161510e3654d8f20352156a40b2ec8fb10b8f0104a7bed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1acb7eeaed5715a2226c171bf69bef6c9e0733efbca90d84cf32092634b39c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a585b540ed022806d9086c042f67de1b1e119de17840462b36f558334798b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d9fa4b37954cdc103d1674eb12249e97339db9078ca2576accf379f0f3005bf(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    type: builtins.str,
    zone_id: builtins.str,
    allow_overwrite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    comment: typing.Optional[builtins.str] = None,
    data: typing.Optional[typing.Union[RecordData, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    proxied: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[RecordTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    ttl: typing.Optional[jsii.Number] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c216bfe8b351eb45e7e0937bdc7b9801083b3c5d28a8d836e8c7ff09f0020a0(
    *,
    algorithm: typing.Optional[jsii.Number] = None,
    altitude: typing.Optional[jsii.Number] = None,
    certificate: typing.Optional[builtins.str] = None,
    content: typing.Optional[builtins.str] = None,
    digest: typing.Optional[builtins.str] = None,
    digest_type: typing.Optional[jsii.Number] = None,
    fingerprint: typing.Optional[builtins.str] = None,
    flags: typing.Optional[builtins.str] = None,
    key_tag: typing.Optional[jsii.Number] = None,
    lat_degrees: typing.Optional[jsii.Number] = None,
    lat_direction: typing.Optional[builtins.str] = None,
    lat_minutes: typing.Optional[jsii.Number] = None,
    lat_seconds: typing.Optional[jsii.Number] = None,
    long_degrees: typing.Optional[jsii.Number] = None,
    long_direction: typing.Optional[builtins.str] = None,
    long_minutes: typing.Optional[jsii.Number] = None,
    long_seconds: typing.Optional[jsii.Number] = None,
    matching_type: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    order: typing.Optional[jsii.Number] = None,
    port: typing.Optional[jsii.Number] = None,
    precision_horz: typing.Optional[jsii.Number] = None,
    precision_vert: typing.Optional[jsii.Number] = None,
    preference: typing.Optional[jsii.Number] = None,
    priority: typing.Optional[jsii.Number] = None,
    proto: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[jsii.Number] = None,
    public_key: typing.Optional[builtins.str] = None,
    regex: typing.Optional[builtins.str] = None,
    replacement: typing.Optional[builtins.str] = None,
    selector: typing.Optional[jsii.Number] = None,
    service: typing.Optional[builtins.str] = None,
    size: typing.Optional[jsii.Number] = None,
    tag: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    type: typing.Optional[jsii.Number] = None,
    usage: typing.Optional[jsii.Number] = None,
    value: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e81b2c17e556ec3fb61107d3816647e274f5123ceb81da830a5dbf376930f354(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f529e632b1d7b193264e19c46314133aeaa0d06a67dfab6d9991677ab8f4a1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2afcb66a1894d8079b42470eb1f9d6bab4c344a6986c9d20709c14059bd70cba(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb33a0230f649b279cafc6cc26e6776302368dfc7463684862b386103c45393d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b1d8b971b8eb7f54f7c83745359665007e185e877de3ec9f4f0e56baa566f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fdc275cfff99472462561a26ae7cae17758f7dc0e90c23b1e39986a64baeade(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe37bf73a5ce67c87588d9777239c4bc50a0e83580cbfae32771d11cb155d351(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dccb9bce604cb815aa63062812e0f1729415a52bffac5bd88fd559a6e4a84209(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03442163938a70abceb0a66feff83aa7993d78549a0785aafb08c6da8704a6fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4df5ad5813e63fdd24debc542b43e30a1c2cbca377214658d2f03bcfec8bc5a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22dc8d33b4f8442d0246058d58b783dd184e6ad4f721365a79e4d725e2050ce5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab64c2efce67a890a16377962cffc7b0749a7e17ea32b02ecff4f33064d702b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c98bb8a3063fb9c4d67fcdb29c16adcee282b21e8bac1a52cb2a9bb5940ccc2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43369ded08b3b44cd437fd1299b1587b43a9176b32149e25f3cb7bec9cdec3b4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1106b653686e263bbe365fd90086013a7056c229c6f91546b3c66f77f5ae4cfd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99f75c62c3833f57bddc5255a149376b19e695f4d9831e10f53619140872ad59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf6eb2e9645da2834188fae33f3229749b07c6014f7300b8abf20f21b4339a6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__597eeb43ebe6b7f2b1bedf9075d15e169e2b38ec60d36b5925db97b0a93e41e6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cc484c7ea369cda2f71e5a60bf44f63e5dd2e0c4a2c4031e13c0fe607b6002d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6a83b9abfdc41f7e41108160c33c1e589d171a9ddb4911cea9071333421301(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50596f91cf70d0e3f3742a2ccd371f76dc34e4b1fda3bffc4c02bf6913becfe3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e680b42879dcfba6612170a686d688c0da6e08d6f9cea2dee726b39b405abe38(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1425145cf802ed6960adac0e31d3786e1c2da6702292f45efc50abfde2912934(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1bdded07a30380d97fbd66e2767b69ebdd091ec5b392a1a32a89ec778be8180(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d27a60ba7f7222e276e2c138a3fc433bd84f065488bc7366962b77392ea2072(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cdbfac05fa02be8c3dfad8f7cc16d2c9a8c205b74094311c2dde02afe184635(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f69aa606a38fc6b55dcee3b319a83b01d9ec542c0c45c10309b624baf9b7bb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c96473f06443cc1faf1200d18cad481175bcda45162c2c911ecc76463450b9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6daaa25565128736d8a9c7b54e4e2f2cf52aedd93aa948ba5311eb9944bcd982(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7050cbfa00aaa95bcccac73afe1c233edcda1351d6e6f86882e57bad0c6359(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd27b0f51039217530fe46811ae2485220e4939bc6b3f00afd1b9b5fb14dcbb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1cc219dd2bb64ff9b76cd05ba39ab1911a62ca5c3c4b89b81afef10c5872836(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05fd4c858cb0d09dd26b9003bbe8b36b1fd82b878b8311d05a75fd1f26b95210(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1dc7d3853e92f102ea25e26ba41a63c904f8417b0d5d4dec46d393f696cef23(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbff154b0ffae7300e88acb08be86fc511abd10facc3745434ae5af1f146d927(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2a9e45760fbf4a3626171b3915ea2f2fc34e6f5a65ae307a504a515711a27a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05ded194fa0877d8896cc4f5c6c1d0294e96b7478bac7fe1ac8711bc217c0d5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd2b7208738e5d7f350ed1722701558847571c5ea6f4eaba6c2e37aefd901a12(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42c8411aa6fb6e7f0c0a160fc52a9da01851c715e495458b8ee9da7feed3384d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2418605ae005e50a275c6fb9c5b02488026cab50e90068f20f75b31e5815a5e6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff20c0957275dbe6df5b4031dd9b755b78dc8ea3239f35512ccfe4575645da1(
    value: typing.Optional[RecordData],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d96b6138a969fd43081670fd4383628bfd1217e975b19e4ff120a01aa1d33e(
    *,
    create: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bb994e84bd3c03a8747e982c7ecda35fac7935f49421efd3fc4491d2e617c2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60fafe573e0a650b4f63f38cb8b6cb16b5cef00b825e5607090bbc06ed6b6dd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13401dc1aa0946fce187bf66bbee213a0697815de74fa0c93aa64320b82d3784(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d9840841202379ff4ba9c8455587e1a8b9fa0b6b3f193522f09ef878a04709f(
    value: typing.Optional[typing.Union[RecordTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
