'''
# `docker_registry_image`

Refer to the Terraform Registory for docs: [`docker_registry_image`](https://www.terraform.io/docs/providers/docker/r/registry_image).
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


class RegistryImage(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.registryImage.RegistryImage",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/docker/r/registry_image docker_registry_image}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        build_attribute: typing.Optional[typing.Union["RegistryImageBuild", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        insecure_skip_verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        keep_remotely: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/docker/r/registry_image docker_registry_image} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the Docker image. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#name RegistryImage#name}
        :param build_attribute: build block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#build RegistryImage#build}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#id RegistryImage#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param insecure_skip_verify: If ``true``, the verification of TLS certificates of the server/registry is disabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#insecure_skip_verify RegistryImage#insecure_skip_verify}
        :param keep_remotely: If true, then the Docker image won't be deleted on destroy operation. If this is false, it will delete the image from the docker registry on destroy operation. Defaults to ``false`` Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#keep_remotely RegistryImage#keep_remotely}
        :param triggers: A map of arbitrary strings that, when changed, will force the ``docker_registry_image`` resource to be replaced. This can be used to repush a local image Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#triggers RegistryImage#triggers}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8c118a8ddb426cbfaee36e222bbe15cafa13cc4fbc6f1cf1024ed1432f538bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RegistryImageConfig(
            name=name,
            build_attribute=build_attribute,
            id=id,
            insecure_skip_verify=insecure_skip_verify,
            keep_remotely=keep_remotely,
            triggers=triggers,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putBuildAttribute")
    def put_build_attribute(
        self,
        *,
        context: builtins.str,
        auth_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RegistryImageBuildAuthConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        build_id: typing.Optional[builtins.str] = None,
        cache_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        cgroup_parent: typing.Optional[builtins.str] = None,
        cpu_period: typing.Optional[jsii.Number] = None,
        cpu_quota: typing.Optional[jsii.Number] = None,
        cpu_set_cpus: typing.Optional[builtins.str] = None,
        cpu_set_mems: typing.Optional[builtins.str] = None,
        cpu_shares: typing.Optional[jsii.Number] = None,
        dockerfile: typing.Optional[builtins.str] = None,
        extra_hosts: typing.Optional[typing.Sequence[builtins.str]] = None,
        force_remove: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        isolation: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        memory: typing.Optional[jsii.Number] = None,
        memory_swap: typing.Optional[jsii.Number] = None,
        network_mode: typing.Optional[builtins.str] = None,
        no_cache: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        platform: typing.Optional[builtins.str] = None,
        pull_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remote_context: typing.Optional[builtins.str] = None,
        remove: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_opt: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_id: typing.Optional[builtins.str] = None,
        shm_size: typing.Optional[jsii.Number] = None,
        squash: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suppress_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        target: typing.Optional[builtins.str] = None,
        ulimit: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RegistryImageBuildUlimit", typing.Dict[builtins.str, typing.Any]]]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param context: The absolute path to the context folder. You can use the helper function '${path.cwd}/context-dir'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#context RegistryImage#context}
        :param auth_config: auth_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#auth_config RegistryImage#auth_config}
        :param build_args: Pairs for build-time variables in the form TODO. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#build_args RegistryImage#build_args}
        :param build_id: BuildID is an optional identifier that can be passed together with the build request. The same identifier can be used to gracefully cancel the build with the cancel request. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#build_id RegistryImage#build_id}
        :param cache_from: Images to consider as cache sources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cache_from RegistryImage#cache_from}
        :param cgroup_parent: Optional parent cgroup for the container. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cgroup_parent RegistryImage#cgroup_parent}
        :param cpu_period: The length of a CPU period in microseconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cpu_period RegistryImage#cpu_period}
        :param cpu_quota: Microseconds of CPU time that the container can get in a CPU period. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cpu_quota RegistryImage#cpu_quota}
        :param cpu_set_cpus: CPUs in which to allow execution (e.g., ``0-3``, ``0``, ``1``). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cpu_set_cpus RegistryImage#cpu_set_cpus}
        :param cpu_set_mems: MEMs in which to allow execution (``0-3``, ``0``, ``1``). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cpu_set_mems RegistryImage#cpu_set_mems}
        :param cpu_shares: CPU shares (relative weight). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cpu_shares RegistryImage#cpu_shares}
        :param dockerfile: Dockerfile file. Defaults to ``Dockerfile``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#dockerfile RegistryImage#dockerfile}
        :param extra_hosts: A list of hostnames/IP mappings to add to the container’s /etc/hosts file. Specified in the form ["hostname:IP"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#extra_hosts RegistryImage#extra_hosts}
        :param force_remove: Always remove intermediate containers. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#force_remove RegistryImage#force_remove}
        :param isolation: Isolation represents the isolation technology of a container. The supported values are. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#isolation RegistryImage#isolation}
        :param labels: User-defined key/value metadata. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#labels RegistryImage#labels}
        :param memory: Set memory limit for build. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#memory RegistryImage#memory}
        :param memory_swap: Total memory (memory + swap), -1 to enable unlimited swap. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#memory_swap RegistryImage#memory_swap}
        :param network_mode: Set the networking mode for the RUN instructions during build. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#network_mode RegistryImage#network_mode}
        :param no_cache: Do not use the cache when building the image. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#no_cache RegistryImage#no_cache}
        :param platform: Set platform if server is multi-platform capable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#platform RegistryImage#platform}
        :param pull_parent: Attempt to pull the image even if an older image exists locally. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#pull_parent RegistryImage#pull_parent}
        :param remote_context: A Git repository URI or HTTP/HTTPS context URI. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#remote_context RegistryImage#remote_context}
        :param remove: Remove intermediate containers after a successful build (default behavior). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#remove RegistryImage#remove}
        :param security_opt: The security options. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#security_opt RegistryImage#security_opt}
        :param session_id: Set an ID for the build session. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#session_id RegistryImage#session_id}
        :param shm_size: Size of /dev/shm in bytes. The size must be greater than 0. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#shm_size RegistryImage#shm_size}
        :param squash: If true the new layers are squashed into a new image with a single new layer. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#squash RegistryImage#squash}
        :param suppress_output: Suppress the build output and print image ID on success. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#suppress_output RegistryImage#suppress_output}
        :param target: Set the target build stage to build. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#target RegistryImage#target}
        :param ulimit: ulimit block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#ulimit RegistryImage#ulimit}
        :param version: Version of the underlying builder to use. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#version RegistryImage#version}
        '''
        value = RegistryImageBuild(
            context=context,
            auth_config=auth_config,
            build_args=build_args,
            build_id=build_id,
            cache_from=cache_from,
            cgroup_parent=cgroup_parent,
            cpu_period=cpu_period,
            cpu_quota=cpu_quota,
            cpu_set_cpus=cpu_set_cpus,
            cpu_set_mems=cpu_set_mems,
            cpu_shares=cpu_shares,
            dockerfile=dockerfile,
            extra_hosts=extra_hosts,
            force_remove=force_remove,
            isolation=isolation,
            labels=labels,
            memory=memory,
            memory_swap=memory_swap,
            network_mode=network_mode,
            no_cache=no_cache,
            platform=platform,
            pull_parent=pull_parent,
            remote_context=remote_context,
            remove=remove,
            security_opt=security_opt,
            session_id=session_id,
            shm_size=shm_size,
            squash=squash,
            suppress_output=suppress_output,
            target=target,
            ulimit=ulimit,
            version=version,
        )

        return typing.cast(None, jsii.invoke(self, "putBuildAttribute", [value]))

    @jsii.member(jsii_name="resetBuildAttribute")
    def reset_build_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildAttribute", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInsecureSkipVerify")
    def reset_insecure_skip_verify(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecureSkipVerify", []))

    @jsii.member(jsii_name="resetKeepRemotely")
    def reset_keep_remotely(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepRemotely", []))

    @jsii.member(jsii_name="resetTriggers")
    def reset_triggers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggers", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="buildAttribute")
    def build_attribute(self) -> "RegistryImageBuildOutputReference":
        return typing.cast("RegistryImageBuildOutputReference", jsii.get(self, "buildAttribute"))

    @builtins.property
    @jsii.member(jsii_name="sha256Digest")
    def sha256_digest(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha256Digest"))

    @builtins.property
    @jsii.member(jsii_name="buildAttributeInput")
    def build_attribute_input(self) -> typing.Optional["RegistryImageBuild"]:
        return typing.cast(typing.Optional["RegistryImageBuild"], jsii.get(self, "buildAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureSkipVerifyInput")
    def insecure_skip_verify_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureSkipVerifyInput"))

    @builtins.property
    @jsii.member(jsii_name="keepRemotelyInput")
    def keep_remotely_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "keepRemotelyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="triggersInput")
    def triggers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "triggersInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ff8ed25cb9671772005d9fb3a69e11711118a3346a388258a936372e3b049e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="insecureSkipVerify")
    def insecure_skip_verify(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "insecureSkipVerify"))

    @insecure_skip_verify.setter
    def insecure_skip_verify(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__165a965a38202187f7bf254ea0a0cfdacbdcfbb38452e0d8a7ab9add712798d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecureSkipVerify", value)

    @builtins.property
    @jsii.member(jsii_name="keepRemotely")
    def keep_remotely(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "keepRemotely"))

    @keep_remotely.setter
    def keep_remotely(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38295d51248cd1a5cc405dfe316f41c7af33e06a2fa3c287f2b065e3707f37e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepRemotely", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11694d42b6e4bf573a26db19b8a8d8dabbf142e3527087877358cda2ed80434b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="triggers")
    def triggers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "triggers"))

    @triggers.setter
    def triggers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4b2638177ed35a01cf68e6834031c8e490d8a119d0333d25dfe1e70d3da68d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggers", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.registryImage.RegistryImageBuild",
    jsii_struct_bases=[],
    name_mapping={
        "context": "context",
        "auth_config": "authConfig",
        "build_args": "buildArgs",
        "build_id": "buildId",
        "cache_from": "cacheFrom",
        "cgroup_parent": "cgroupParent",
        "cpu_period": "cpuPeriod",
        "cpu_quota": "cpuQuota",
        "cpu_set_cpus": "cpuSetCpus",
        "cpu_set_mems": "cpuSetMems",
        "cpu_shares": "cpuShares",
        "dockerfile": "dockerfile",
        "extra_hosts": "extraHosts",
        "force_remove": "forceRemove",
        "isolation": "isolation",
        "labels": "labels",
        "memory": "memory",
        "memory_swap": "memorySwap",
        "network_mode": "networkMode",
        "no_cache": "noCache",
        "platform": "platform",
        "pull_parent": "pullParent",
        "remote_context": "remoteContext",
        "remove": "remove",
        "security_opt": "securityOpt",
        "session_id": "sessionId",
        "shm_size": "shmSize",
        "squash": "squash",
        "suppress_output": "suppressOutput",
        "target": "target",
        "ulimit": "ulimit",
        "version": "version",
    },
)
class RegistryImageBuild:
    def __init__(
        self,
        *,
        context: builtins.str,
        auth_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RegistryImageBuildAuthConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        build_id: typing.Optional[builtins.str] = None,
        cache_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        cgroup_parent: typing.Optional[builtins.str] = None,
        cpu_period: typing.Optional[jsii.Number] = None,
        cpu_quota: typing.Optional[jsii.Number] = None,
        cpu_set_cpus: typing.Optional[builtins.str] = None,
        cpu_set_mems: typing.Optional[builtins.str] = None,
        cpu_shares: typing.Optional[jsii.Number] = None,
        dockerfile: typing.Optional[builtins.str] = None,
        extra_hosts: typing.Optional[typing.Sequence[builtins.str]] = None,
        force_remove: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        isolation: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        memory: typing.Optional[jsii.Number] = None,
        memory_swap: typing.Optional[jsii.Number] = None,
        network_mode: typing.Optional[builtins.str] = None,
        no_cache: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        platform: typing.Optional[builtins.str] = None,
        pull_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remote_context: typing.Optional[builtins.str] = None,
        remove: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_opt: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_id: typing.Optional[builtins.str] = None,
        shm_size: typing.Optional[jsii.Number] = None,
        squash: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suppress_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        target: typing.Optional[builtins.str] = None,
        ulimit: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RegistryImageBuildUlimit", typing.Dict[builtins.str, typing.Any]]]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param context: The absolute path to the context folder. You can use the helper function '${path.cwd}/context-dir'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#context RegistryImage#context}
        :param auth_config: auth_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#auth_config RegistryImage#auth_config}
        :param build_args: Pairs for build-time variables in the form TODO. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#build_args RegistryImage#build_args}
        :param build_id: BuildID is an optional identifier that can be passed together with the build request. The same identifier can be used to gracefully cancel the build with the cancel request. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#build_id RegistryImage#build_id}
        :param cache_from: Images to consider as cache sources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cache_from RegistryImage#cache_from}
        :param cgroup_parent: Optional parent cgroup for the container. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cgroup_parent RegistryImage#cgroup_parent}
        :param cpu_period: The length of a CPU period in microseconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cpu_period RegistryImage#cpu_period}
        :param cpu_quota: Microseconds of CPU time that the container can get in a CPU period. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cpu_quota RegistryImage#cpu_quota}
        :param cpu_set_cpus: CPUs in which to allow execution (e.g., ``0-3``, ``0``, ``1``). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cpu_set_cpus RegistryImage#cpu_set_cpus}
        :param cpu_set_mems: MEMs in which to allow execution (``0-3``, ``0``, ``1``). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cpu_set_mems RegistryImage#cpu_set_mems}
        :param cpu_shares: CPU shares (relative weight). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cpu_shares RegistryImage#cpu_shares}
        :param dockerfile: Dockerfile file. Defaults to ``Dockerfile``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#dockerfile RegistryImage#dockerfile}
        :param extra_hosts: A list of hostnames/IP mappings to add to the container’s /etc/hosts file. Specified in the form ["hostname:IP"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#extra_hosts RegistryImage#extra_hosts}
        :param force_remove: Always remove intermediate containers. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#force_remove RegistryImage#force_remove}
        :param isolation: Isolation represents the isolation technology of a container. The supported values are. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#isolation RegistryImage#isolation}
        :param labels: User-defined key/value metadata. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#labels RegistryImage#labels}
        :param memory: Set memory limit for build. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#memory RegistryImage#memory}
        :param memory_swap: Total memory (memory + swap), -1 to enable unlimited swap. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#memory_swap RegistryImage#memory_swap}
        :param network_mode: Set the networking mode for the RUN instructions during build. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#network_mode RegistryImage#network_mode}
        :param no_cache: Do not use the cache when building the image. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#no_cache RegistryImage#no_cache}
        :param platform: Set platform if server is multi-platform capable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#platform RegistryImage#platform}
        :param pull_parent: Attempt to pull the image even if an older image exists locally. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#pull_parent RegistryImage#pull_parent}
        :param remote_context: A Git repository URI or HTTP/HTTPS context URI. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#remote_context RegistryImage#remote_context}
        :param remove: Remove intermediate containers after a successful build (default behavior). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#remove RegistryImage#remove}
        :param security_opt: The security options. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#security_opt RegistryImage#security_opt}
        :param session_id: Set an ID for the build session. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#session_id RegistryImage#session_id}
        :param shm_size: Size of /dev/shm in bytes. The size must be greater than 0. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#shm_size RegistryImage#shm_size}
        :param squash: If true the new layers are squashed into a new image with a single new layer. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#squash RegistryImage#squash}
        :param suppress_output: Suppress the build output and print image ID on success. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#suppress_output RegistryImage#suppress_output}
        :param target: Set the target build stage to build. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#target RegistryImage#target}
        :param ulimit: ulimit block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#ulimit RegistryImage#ulimit}
        :param version: Version of the underlying builder to use. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#version RegistryImage#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3d7734d97b43ee88ad0ad921e83d1057e21b9f33f6e3e3a6d31496c78e4ec46)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument auth_config", value=auth_config, expected_type=type_hints["auth_config"])
            check_type(argname="argument build_args", value=build_args, expected_type=type_hints["build_args"])
            check_type(argname="argument build_id", value=build_id, expected_type=type_hints["build_id"])
            check_type(argname="argument cache_from", value=cache_from, expected_type=type_hints["cache_from"])
            check_type(argname="argument cgroup_parent", value=cgroup_parent, expected_type=type_hints["cgroup_parent"])
            check_type(argname="argument cpu_period", value=cpu_period, expected_type=type_hints["cpu_period"])
            check_type(argname="argument cpu_quota", value=cpu_quota, expected_type=type_hints["cpu_quota"])
            check_type(argname="argument cpu_set_cpus", value=cpu_set_cpus, expected_type=type_hints["cpu_set_cpus"])
            check_type(argname="argument cpu_set_mems", value=cpu_set_mems, expected_type=type_hints["cpu_set_mems"])
            check_type(argname="argument cpu_shares", value=cpu_shares, expected_type=type_hints["cpu_shares"])
            check_type(argname="argument dockerfile", value=dockerfile, expected_type=type_hints["dockerfile"])
            check_type(argname="argument extra_hosts", value=extra_hosts, expected_type=type_hints["extra_hosts"])
            check_type(argname="argument force_remove", value=force_remove, expected_type=type_hints["force_remove"])
            check_type(argname="argument isolation", value=isolation, expected_type=type_hints["isolation"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument memory_swap", value=memory_swap, expected_type=type_hints["memory_swap"])
            check_type(argname="argument network_mode", value=network_mode, expected_type=type_hints["network_mode"])
            check_type(argname="argument no_cache", value=no_cache, expected_type=type_hints["no_cache"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument pull_parent", value=pull_parent, expected_type=type_hints["pull_parent"])
            check_type(argname="argument remote_context", value=remote_context, expected_type=type_hints["remote_context"])
            check_type(argname="argument remove", value=remove, expected_type=type_hints["remove"])
            check_type(argname="argument security_opt", value=security_opt, expected_type=type_hints["security_opt"])
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument shm_size", value=shm_size, expected_type=type_hints["shm_size"])
            check_type(argname="argument squash", value=squash, expected_type=type_hints["squash"])
            check_type(argname="argument suppress_output", value=suppress_output, expected_type=type_hints["suppress_output"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument ulimit", value=ulimit, expected_type=type_hints["ulimit"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "context": context,
        }
        if auth_config is not None:
            self._values["auth_config"] = auth_config
        if build_args is not None:
            self._values["build_args"] = build_args
        if build_id is not None:
            self._values["build_id"] = build_id
        if cache_from is not None:
            self._values["cache_from"] = cache_from
        if cgroup_parent is not None:
            self._values["cgroup_parent"] = cgroup_parent
        if cpu_period is not None:
            self._values["cpu_period"] = cpu_period
        if cpu_quota is not None:
            self._values["cpu_quota"] = cpu_quota
        if cpu_set_cpus is not None:
            self._values["cpu_set_cpus"] = cpu_set_cpus
        if cpu_set_mems is not None:
            self._values["cpu_set_mems"] = cpu_set_mems
        if cpu_shares is not None:
            self._values["cpu_shares"] = cpu_shares
        if dockerfile is not None:
            self._values["dockerfile"] = dockerfile
        if extra_hosts is not None:
            self._values["extra_hosts"] = extra_hosts
        if force_remove is not None:
            self._values["force_remove"] = force_remove
        if isolation is not None:
            self._values["isolation"] = isolation
        if labels is not None:
            self._values["labels"] = labels
        if memory is not None:
            self._values["memory"] = memory
        if memory_swap is not None:
            self._values["memory_swap"] = memory_swap
        if network_mode is not None:
            self._values["network_mode"] = network_mode
        if no_cache is not None:
            self._values["no_cache"] = no_cache
        if platform is not None:
            self._values["platform"] = platform
        if pull_parent is not None:
            self._values["pull_parent"] = pull_parent
        if remote_context is not None:
            self._values["remote_context"] = remote_context
        if remove is not None:
            self._values["remove"] = remove
        if security_opt is not None:
            self._values["security_opt"] = security_opt
        if session_id is not None:
            self._values["session_id"] = session_id
        if shm_size is not None:
            self._values["shm_size"] = shm_size
        if squash is not None:
            self._values["squash"] = squash
        if suppress_output is not None:
            self._values["suppress_output"] = suppress_output
        if target is not None:
            self._values["target"] = target
        if ulimit is not None:
            self._values["ulimit"] = ulimit
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def context(self) -> builtins.str:
        '''The absolute path to the context folder. You can use the helper function '${path.cwd}/context-dir'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#context RegistryImage#context}
        '''
        result = self._values.get("context")
        assert result is not None, "Required property 'context' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RegistryImageBuildAuthConfig"]]]:
        '''auth_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#auth_config RegistryImage#auth_config}
        '''
        result = self._values.get("auth_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RegistryImageBuildAuthConfig"]]], result)

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Pairs for build-time variables in the form TODO.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#build_args RegistryImage#build_args}
        '''
        result = self._values.get("build_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def build_id(self) -> typing.Optional[builtins.str]:
        '''BuildID is an optional identifier that can be passed together with the build request.

        The same identifier can be used to gracefully cancel the build with the cancel request.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#build_id RegistryImage#build_id}
        '''
        result = self._values.get("build_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_from(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Images to consider as cache sources.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cache_from RegistryImage#cache_from}
        '''
        result = self._values.get("cache_from")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cgroup_parent(self) -> typing.Optional[builtins.str]:
        '''Optional parent cgroup for the container.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cgroup_parent RegistryImage#cgroup_parent}
        '''
        result = self._values.get("cgroup_parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_period(self) -> typing.Optional[jsii.Number]:
        '''The length of a CPU period in microseconds.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cpu_period RegistryImage#cpu_period}
        '''
        result = self._values.get("cpu_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_quota(self) -> typing.Optional[jsii.Number]:
        '''Microseconds of CPU time that the container can get in a CPU period.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cpu_quota RegistryImage#cpu_quota}
        '''
        result = self._values.get("cpu_quota")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_set_cpus(self) -> typing.Optional[builtins.str]:
        '''CPUs in which to allow execution (e.g., ``0-3``, ``0``, ``1``).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cpu_set_cpus RegistryImage#cpu_set_cpus}
        '''
        result = self._values.get("cpu_set_cpus")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_set_mems(self) -> typing.Optional[builtins.str]:
        '''MEMs in which to allow execution (``0-3``, ``0``, ``1``).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cpu_set_mems RegistryImage#cpu_set_mems}
        '''
        result = self._values.get("cpu_set_mems")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_shares(self) -> typing.Optional[jsii.Number]:
        '''CPU shares (relative weight).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#cpu_shares RegistryImage#cpu_shares}
        '''
        result = self._values.get("cpu_shares")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dockerfile(self) -> typing.Optional[builtins.str]:
        '''Dockerfile file. Defaults to ``Dockerfile``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#dockerfile RegistryImage#dockerfile}
        '''
        result = self._values.get("dockerfile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extra_hosts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of hostnames/IP mappings to add to the container’s /etc/hosts file. Specified in the form ["hostname:IP"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#extra_hosts RegistryImage#extra_hosts}
        '''
        result = self._values.get("extra_hosts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def force_remove(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Always remove intermediate containers.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#force_remove RegistryImage#force_remove}
        '''
        result = self._values.get("force_remove")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def isolation(self) -> typing.Optional[builtins.str]:
        '''Isolation represents the isolation technology of a container. The supported values are.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#isolation RegistryImage#isolation}
        '''
        result = self._values.get("isolation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined key/value metadata.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#labels RegistryImage#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def memory(self) -> typing.Optional[jsii.Number]:
        '''Set memory limit for build.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#memory RegistryImage#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_swap(self) -> typing.Optional[jsii.Number]:
        '''Total memory (memory + swap), -1 to enable unlimited swap.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#memory_swap RegistryImage#memory_swap}
        '''
        result = self._values.get("memory_swap")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def network_mode(self) -> typing.Optional[builtins.str]:
        '''Set the networking mode for the RUN instructions during build.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#network_mode RegistryImage#network_mode}
        '''
        result = self._values.get("network_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_cache(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not use the cache when building the image.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#no_cache RegistryImage#no_cache}
        '''
        result = self._values.get("no_cache")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''Set platform if server is multi-platform capable.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#platform RegistryImage#platform}
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_parent(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Attempt to pull the image even if an older image exists locally.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#pull_parent RegistryImage#pull_parent}
        '''
        result = self._values.get("pull_parent")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def remote_context(self) -> typing.Optional[builtins.str]:
        '''A Git repository URI or HTTP/HTTPS context URI.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#remote_context RegistryImage#remote_context}
        '''
        result = self._values.get("remote_context")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remove(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Remove intermediate containers after a successful build (default behavior).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#remove RegistryImage#remove}
        '''
        result = self._values.get("remove")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def security_opt(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The security options.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#security_opt RegistryImage#security_opt}
        '''
        result = self._values.get("security_opt")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def session_id(self) -> typing.Optional[builtins.str]:
        '''Set an ID for the build session.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#session_id RegistryImage#session_id}
        '''
        result = self._values.get("session_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shm_size(self) -> typing.Optional[jsii.Number]:
        '''Size of /dev/shm in bytes. The size must be greater than 0.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#shm_size RegistryImage#shm_size}
        '''
        result = self._values.get("shm_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def squash(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true the new layers are squashed into a new image with a single new layer.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#squash RegistryImage#squash}
        '''
        result = self._values.get("squash")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def suppress_output(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Suppress the build output and print image ID on success.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#suppress_output RegistryImage#suppress_output}
        '''
        result = self._values.get("suppress_output")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Set the target build stage to build.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#target RegistryImage#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ulimit(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RegistryImageBuildUlimit"]]]:
        '''ulimit block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#ulimit RegistryImage#ulimit}
        '''
        result = self._values.get("ulimit")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RegistryImageBuildUlimit"]]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the underlying builder to use.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#version RegistryImage#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RegistryImageBuild(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.registryImage.RegistryImageBuildAuthConfig",
    jsii_struct_bases=[],
    name_mapping={
        "host_name": "hostName",
        "auth": "auth",
        "email": "email",
        "identity_token": "identityToken",
        "password": "password",
        "registry_token": "registryToken",
        "server_address": "serverAddress",
        "user_name": "userName",
    },
)
class RegistryImageBuildAuthConfig:
    def __init__(
        self,
        *,
        host_name: builtins.str,
        auth: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        identity_token: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        registry_token: typing.Optional[builtins.str] = None,
        server_address: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_name: hostname of the registry. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#host_name RegistryImage#host_name}
        :param auth: the auth token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#auth RegistryImage#auth}
        :param email: the user emal. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#email RegistryImage#email}
        :param identity_token: the identity token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#identity_token RegistryImage#identity_token}
        :param password: the registry password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#password RegistryImage#password}
        :param registry_token: the registry token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#registry_token RegistryImage#registry_token}
        :param server_address: the server address. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#server_address RegistryImage#server_address}
        :param user_name: the registry user name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#user_name RegistryImage#user_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c76a5a4cdc30752c7e981e360ba52ffeffe4face38d45ee64d60e092e07aeff)
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument identity_token", value=identity_token, expected_type=type_hints["identity_token"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument registry_token", value=registry_token, expected_type=type_hints["registry_token"])
            check_type(argname="argument server_address", value=server_address, expected_type=type_hints["server_address"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_name": host_name,
        }
        if auth is not None:
            self._values["auth"] = auth
        if email is not None:
            self._values["email"] = email
        if identity_token is not None:
            self._values["identity_token"] = identity_token
        if password is not None:
            self._values["password"] = password
        if registry_token is not None:
            self._values["registry_token"] = registry_token
        if server_address is not None:
            self._values["server_address"] = server_address
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def host_name(self) -> builtins.str:
        '''hostname of the registry.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#host_name RegistryImage#host_name}
        '''
        result = self._values.get("host_name")
        assert result is not None, "Required property 'host_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth(self) -> typing.Optional[builtins.str]:
        '''the auth token.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#auth RegistryImage#auth}
        '''
        result = self._values.get("auth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''the user emal.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#email RegistryImage#email}
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_token(self) -> typing.Optional[builtins.str]:
        '''the identity token.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#identity_token RegistryImage#identity_token}
        '''
        result = self._values.get("identity_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''the registry password.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#password RegistryImage#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry_token(self) -> typing.Optional[builtins.str]:
        '''the registry token.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#registry_token RegistryImage#registry_token}
        '''
        result = self._values.get("registry_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_address(self) -> typing.Optional[builtins.str]:
        '''the server address.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#server_address RegistryImage#server_address}
        '''
        result = self._values.get("server_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''the registry user name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#user_name RegistryImage#user_name}
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RegistryImageBuildAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RegistryImageBuildAuthConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.registryImage.RegistryImageBuildAuthConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff5fd6f8ff88631cf6e99cf5d680d24fad2f7ef14395146a236eedfff61b2442)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RegistryImageBuildAuthConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2737d6df10e2517f2b9e928ce81f21055ab53fd44a87cd34f966fd174de9836)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RegistryImageBuildAuthConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbe98f44dd75a16963737f79ac7f46b016ff1329d46fa2cea0de359bf4c63229)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79bceb34a0fb91e0ae8a5802365ae326156a1b5899afb6521308f2b80be4c784)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65a121422dd647d77ccea4bd9560ac6c238222a5c8c4997effcf1be4646e3e5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RegistryImageBuildAuthConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RegistryImageBuildAuthConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RegistryImageBuildAuthConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb45a5940e2ab1a5920723e7142c74afc7ef32af26f9d54443391684ba28816)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class RegistryImageBuildAuthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.registryImage.RegistryImageBuildAuthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1be73ea269fcf682f1d1ae6e036cdbefdf06edc7fdf0aaf3def052ae7e6ef91e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAuth")
    def reset_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuth", []))

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetIdentityToken")
    def reset_identity_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityToken", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetRegistryToken")
    def reset_registry_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistryToken", []))

    @jsii.member(jsii_name="resetServerAddress")
    def reset_server_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerAddress", []))

    @jsii.member(jsii_name="resetUserName")
    def reset_user_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserName", []))

    @builtins.property
    @jsii.member(jsii_name="authInput")
    def auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="identityTokenInput")
    def identity_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="registryTokenInput")
    def registry_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "registryTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="serverAddressInput")
    def server_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameInput")
    def user_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameInput"))

    @builtins.property
    @jsii.member(jsii_name="auth")
    def auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "auth"))

    @auth.setter
    def auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efcefb0382068646bc08ffaa682c84853af3621bb01132c9522a542725b82013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auth", value)

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dad0e84522d5e2971f61a8659e5e08a3e7efe7f4142823836f90176d7f91a5ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value)

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__352f14d66c168ef9748ddc5add4bd101297f6b2050967a3c5d6e04551dbff947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value)

    @builtins.property
    @jsii.member(jsii_name="identityToken")
    def identity_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityToken"))

    @identity_token.setter
    def identity_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee199f5e63b63c2cc5644116ee564e33077cad88d2cdfe83ea22a2eb8594a2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityToken", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__847f3dc961ebbdeec89039cf88e9b7f55db1cc272b4b945ceba541336d4ab4e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="registryToken")
    def registry_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registryToken"))

    @registry_token.setter
    def registry_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eebc50be77691df2c20945173ec87353f7da48f86f601e9261f8040156129c26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryToken", value)

    @builtins.property
    @jsii.member(jsii_name="serverAddress")
    def server_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverAddress"))

    @server_address.setter
    def server_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91216d45e3205b950df1cf526b22bb39958fd46d1303fd6cf0b8bce168c0070e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverAddress", value)

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3987b0cb1029e3ed4f82b547dfb53fa8a02267b886bceb28e61e06064ef5a5b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[RegistryImageBuildAuthConfig, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[RegistryImageBuildAuthConfig, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[RegistryImageBuildAuthConfig, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__827a7e6d6006ecf4342ce1b505624dce23f9632cc19a5441049541537af55ae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class RegistryImageBuildOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.registryImage.RegistryImageBuildOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9c2224f07239710be5582e9b11faa2448fdfdb6d5aa8281841c952746f4ffe9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthConfig")
    def put_auth_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RegistryImageBuildAuthConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ba22307fe29dc7ce77a5e3463d224e40dd32f2c7759253922b0088540462ef3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuthConfig", [value]))

    @jsii.member(jsii_name="putUlimit")
    def put_ulimit(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RegistryImageBuildUlimit", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aadc7511fe3b35cc3c109d3b035c731c418ea1ff2f2d8e84a0b96be86c01acf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUlimit", [value]))

    @jsii.member(jsii_name="resetAuthConfig")
    def reset_auth_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthConfig", []))

    @jsii.member(jsii_name="resetBuildArgs")
    def reset_build_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildArgs", []))

    @jsii.member(jsii_name="resetBuildId")
    def reset_build_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildId", []))

    @jsii.member(jsii_name="resetCacheFrom")
    def reset_cache_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheFrom", []))

    @jsii.member(jsii_name="resetCgroupParent")
    def reset_cgroup_parent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCgroupParent", []))

    @jsii.member(jsii_name="resetCpuPeriod")
    def reset_cpu_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuPeriod", []))

    @jsii.member(jsii_name="resetCpuQuota")
    def reset_cpu_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuQuota", []))

    @jsii.member(jsii_name="resetCpuSetCpus")
    def reset_cpu_set_cpus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuSetCpus", []))

    @jsii.member(jsii_name="resetCpuSetMems")
    def reset_cpu_set_mems(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuSetMems", []))

    @jsii.member(jsii_name="resetCpuShares")
    def reset_cpu_shares(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuShares", []))

    @jsii.member(jsii_name="resetDockerfile")
    def reset_dockerfile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerfile", []))

    @jsii.member(jsii_name="resetExtraHosts")
    def reset_extra_hosts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtraHosts", []))

    @jsii.member(jsii_name="resetForceRemove")
    def reset_force_remove(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceRemove", []))

    @jsii.member(jsii_name="resetIsolation")
    def reset_isolation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsolation", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @jsii.member(jsii_name="resetMemorySwap")
    def reset_memory_swap(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemorySwap", []))

    @jsii.member(jsii_name="resetNetworkMode")
    def reset_network_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkMode", []))

    @jsii.member(jsii_name="resetNoCache")
    def reset_no_cache(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoCache", []))

    @jsii.member(jsii_name="resetPlatform")
    def reset_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatform", []))

    @jsii.member(jsii_name="resetPullParent")
    def reset_pull_parent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPullParent", []))

    @jsii.member(jsii_name="resetRemoteContext")
    def reset_remote_context(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteContext", []))

    @jsii.member(jsii_name="resetRemove")
    def reset_remove(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemove", []))

    @jsii.member(jsii_name="resetSecurityOpt")
    def reset_security_opt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityOpt", []))

    @jsii.member(jsii_name="resetSessionId")
    def reset_session_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionId", []))

    @jsii.member(jsii_name="resetShmSize")
    def reset_shm_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShmSize", []))

    @jsii.member(jsii_name="resetSquash")
    def reset_squash(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSquash", []))

    @jsii.member(jsii_name="resetSuppressOutput")
    def reset_suppress_output(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuppressOutput", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @jsii.member(jsii_name="resetUlimit")
    def reset_ulimit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUlimit", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="authConfig")
    def auth_config(self) -> RegistryImageBuildAuthConfigList:
        return typing.cast(RegistryImageBuildAuthConfigList, jsii.get(self, "authConfig"))

    @builtins.property
    @jsii.member(jsii_name="ulimit")
    def ulimit(self) -> "RegistryImageBuildUlimitList":
        return typing.cast("RegistryImageBuildUlimitList", jsii.get(self, "ulimit"))

    @builtins.property
    @jsii.member(jsii_name="authConfigInput")
    def auth_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RegistryImageBuildAuthConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RegistryImageBuildAuthConfig]]], jsii.get(self, "authConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="buildArgsInput")
    def build_args_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "buildArgsInput"))

    @builtins.property
    @jsii.member(jsii_name="buildIdInput")
    def build_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheFromInput")
    def cache_from_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cacheFromInput"))

    @builtins.property
    @jsii.member(jsii_name="cgroupParentInput")
    def cgroup_parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cgroupParentInput"))

    @builtins.property
    @jsii.member(jsii_name="contextInput")
    def context_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuPeriodInput")
    def cpu_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuQuotaInput")
    def cpu_quota_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuSetCpusInput")
    def cpu_set_cpus_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuSetCpusInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuSetMemsInput")
    def cpu_set_mems_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuSetMemsInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuSharesInput")
    def cpu_shares_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuSharesInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerfileInput")
    def dockerfile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerfileInput"))

    @builtins.property
    @jsii.member(jsii_name="extraHostsInput")
    def extra_hosts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "extraHostsInput"))

    @builtins.property
    @jsii.member(jsii_name="forceRemoveInput")
    def force_remove_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceRemoveInput"))

    @builtins.property
    @jsii.member(jsii_name="isolationInput")
    def isolation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "isolationInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="memorySwapInput")
    def memory_swap_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memorySwapInput"))

    @builtins.property
    @jsii.member(jsii_name="networkModeInput")
    def network_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkModeInput"))

    @builtins.property
    @jsii.member(jsii_name="noCacheInput")
    def no_cache_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noCacheInput"))

    @builtins.property
    @jsii.member(jsii_name="platformInput")
    def platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platformInput"))

    @builtins.property
    @jsii.member(jsii_name="pullParentInput")
    def pull_parent_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pullParentInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteContextInput")
    def remote_context_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteContextInput"))

    @builtins.property
    @jsii.member(jsii_name="removeInput")
    def remove_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "removeInput"))

    @builtins.property
    @jsii.member(jsii_name="securityOptInput")
    def security_opt_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityOptInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionIdInput")
    def session_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="shmSizeInput")
    def shm_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "shmSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="squashInput")
    def squash_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "squashInput"))

    @builtins.property
    @jsii.member(jsii_name="suppressOutputInput")
    def suppress_output_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "suppressOutputInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="ulimitInput")
    def ulimit_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RegistryImageBuildUlimit"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RegistryImageBuildUlimit"]]], jsii.get(self, "ulimitInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="buildArgs")
    def build_args(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "buildArgs"))

    @build_args.setter
    def build_args(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12f4e6371a193d3940adb267660083b5a529eb0cf35ee53b6ffcc117ee3c4a79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildArgs", value)

    @builtins.property
    @jsii.member(jsii_name="buildId")
    def build_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildId"))

    @build_id.setter
    def build_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50988c08337c7c1c56fa6c22c01e768c1f6de3dec1fba5a88eeb658f78fc84e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildId", value)

    @builtins.property
    @jsii.member(jsii_name="cacheFrom")
    def cache_from(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cacheFrom"))

    @cache_from.setter
    def cache_from(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c671b3debce2786f3ae75f3fd9053822587bfd8fe01a044b5780b6a2c172a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheFrom", value)

    @builtins.property
    @jsii.member(jsii_name="cgroupParent")
    def cgroup_parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cgroupParent"))

    @cgroup_parent.setter
    def cgroup_parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d40b62b1dc64cf325037fd3ea6cb6cba15d71685b757ffcc403311f72f22dc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cgroupParent", value)

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "context"))

    @context.setter
    def context(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__781b5fbda732f4fbe73d117ea516393f412c9d061e3c2e599e252983c549486c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value)

    @builtins.property
    @jsii.member(jsii_name="cpuPeriod")
    def cpu_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuPeriod"))

    @cpu_period.setter
    def cpu_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__896645c01ad9689cf83b535698db00f0d67de36b0f673aac838d4997e190b2bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="cpuQuota")
    def cpu_quota(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuQuota"))

    @cpu_quota.setter
    def cpu_quota(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d3038ed8954c51a177def9cddef5bb3315dbbd0d057ee886d8d07c002bdbff9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuQuota", value)

    @builtins.property
    @jsii.member(jsii_name="cpuSetCpus")
    def cpu_set_cpus(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuSetCpus"))

    @cpu_set_cpus.setter
    def cpu_set_cpus(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9106875216678bf92e8406d39f6659984c13f21f4aa9165ef44b8b21501e61f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuSetCpus", value)

    @builtins.property
    @jsii.member(jsii_name="cpuSetMems")
    def cpu_set_mems(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuSetMems"))

    @cpu_set_mems.setter
    def cpu_set_mems(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f730b896da6bf0f9884247c577f6c4c8b274176c8342eb136be2e2cdda0ba7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuSetMems", value)

    @builtins.property
    @jsii.member(jsii_name="cpuShares")
    def cpu_shares(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuShares"))

    @cpu_shares.setter
    def cpu_shares(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf70c5d99a674c32cd8fee2ee01b70fde265221f83cc023a2f769ca8fc49c1e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuShares", value)

    @builtins.property
    @jsii.member(jsii_name="dockerfile")
    def dockerfile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dockerfile"))

    @dockerfile.setter
    def dockerfile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e989ba0949fc93d6c1efdd0f125f72c3a09ec0fe7cef5ff8c5b76f9b0063db7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerfile", value)

    @builtins.property
    @jsii.member(jsii_name="extraHosts")
    def extra_hosts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "extraHosts"))

    @extra_hosts.setter
    def extra_hosts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__700dfc8589f6c3027e151a81b03374ce548c9b0379362c6dabd71900175f9140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extraHosts", value)

    @builtins.property
    @jsii.member(jsii_name="forceRemove")
    def force_remove(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceRemove"))

    @force_remove.setter
    def force_remove(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3321815637fb34460e9ebfcb63076d7bf9d24aa81f651eecf87680cbbcfef118)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceRemove", value)

    @builtins.property
    @jsii.member(jsii_name="isolation")
    def isolation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isolation"))

    @isolation.setter
    def isolation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e20afe5aff8cf4beb8280c86b0b02e7ca553f90fe69421a18e18255c8ca17029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isolation", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccf5fd911bd71b1c93c8cfd16a9f803a6c2e00cac6454f8729374542764cca77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d654fb8f581ae1ac867b9a9b1deda4380715a8755501375e1ceb6150ad79cda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value)

    @builtins.property
    @jsii.member(jsii_name="memorySwap")
    def memory_swap(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySwap"))

    @memory_swap.setter
    def memory_swap(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7840fa0ee2d8b16d95b4c7869cc9c96cf461bdc2c594a10329e889a0a847745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memorySwap", value)

    @builtins.property
    @jsii.member(jsii_name="networkMode")
    def network_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkMode"))

    @network_mode.setter
    def network_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45bef4d80c3ea0a93fff4f2ab8488d237e9c417f3d595d20d64c6551a03acf52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkMode", value)

    @builtins.property
    @jsii.member(jsii_name="noCache")
    def no_cache(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noCache"))

    @no_cache.setter
    def no_cache(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23375eb7cd5e57ca73315df73a8e3d20dfb301f176892ccc92bb4968442dbe46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noCache", value)

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platform"))

    @platform.setter
    def platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd1d6c1e78f158de4bb570998e175157ea3366e8fd91d15ec8b86f922eae0b3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platform", value)

    @builtins.property
    @jsii.member(jsii_name="pullParent")
    def pull_parent(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pullParent"))

    @pull_parent.setter
    def pull_parent(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ea9f8d056ef631094ec5cc8fcb17f4bf61c09c5bbd96aa9d99a5b54f405d64a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pullParent", value)

    @builtins.property
    @jsii.member(jsii_name="remoteContext")
    def remote_context(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteContext"))

    @remote_context.setter
    def remote_context(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__179f336ab57de28bb15f3e5c76af7ad1404f507cfff79757db495c3d56390163)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteContext", value)

    @builtins.property
    @jsii.member(jsii_name="remove")
    def remove(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "remove"))

    @remove.setter
    def remove(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a417a9cc222bf57e3c9c82c929f1ec7d25db643050aad178c5a6396feab3c0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remove", value)

    @builtins.property
    @jsii.member(jsii_name="securityOpt")
    def security_opt(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityOpt"))

    @security_opt.setter
    def security_opt(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40844e1f3c2e902bd9172b1144840c9117cbd8e72072de31a8e4b4a4658ce850)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityOpt", value)

    @builtins.property
    @jsii.member(jsii_name="sessionId")
    def session_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionId"))

    @session_id.setter
    def session_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b5bd53bb08c6839c537e5aca62a47aa52bdb854411bcf58732af5ccdf3aa2f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionId", value)

    @builtins.property
    @jsii.member(jsii_name="shmSize")
    def shm_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "shmSize"))

    @shm_size.setter
    def shm_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c098c724dc2a8f86b7aa0830780061c4bc6c25d829ecacf99be802712aca42b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shmSize", value)

    @builtins.property
    @jsii.member(jsii_name="squash")
    def squash(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "squash"))

    @squash.setter
    def squash(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0452f6887bab8464b55998fc5772e8bc81baf01f63dae64d58664330af1af6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "squash", value)

    @builtins.property
    @jsii.member(jsii_name="suppressOutput")
    def suppress_output(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "suppressOutput"))

    @suppress_output.setter
    def suppress_output(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03eeb850b4a7c0f8f0e90bae72fd619ce67bdda983bd5d8cfa3fab5523f02ac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suppressOutput", value)

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27a7a036802ef069e24def60666d725ce79e36ff6100c5d5075efdc8b2f0e994)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7a0e7710f178b3cad180777f81833d347f6e9b33a0a9289e522a0d200380140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RegistryImageBuild]:
        return typing.cast(typing.Optional[RegistryImageBuild], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RegistryImageBuild]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8950f81025c8d1106bbc5a0959cb7b474def122ad6a98c318388ba4592aa282)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.registryImage.RegistryImageBuildUlimit",
    jsii_struct_bases=[],
    name_mapping={"hard": "hard", "name": "name", "soft": "soft"},
)
class RegistryImageBuildUlimit:
    def __init__(
        self,
        *,
        hard: jsii.Number,
        name: builtins.str,
        soft: jsii.Number,
    ) -> None:
        '''
        :param hard: soft limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#hard RegistryImage#hard}
        :param name: type of ulimit, e.g. ``nofile``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#name RegistryImage#name}
        :param soft: hard limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#soft RegistryImage#soft}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1dbb8cb3af5f77f82d16bd279a1bc37041eb117c61d9d8226c8534ab3c785d1)
            check_type(argname="argument hard", value=hard, expected_type=type_hints["hard"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument soft", value=soft, expected_type=type_hints["soft"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hard": hard,
            "name": name,
            "soft": soft,
        }

    @builtins.property
    def hard(self) -> jsii.Number:
        '''soft limit.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#hard RegistryImage#hard}
        '''
        result = self._values.get("hard")
        assert result is not None, "Required property 'hard' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''type of ulimit, e.g. ``nofile``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#name RegistryImage#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def soft(self) -> jsii.Number:
        '''hard limit.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#soft RegistryImage#soft}
        '''
        result = self._values.get("soft")
        assert result is not None, "Required property 'soft' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RegistryImageBuildUlimit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RegistryImageBuildUlimitList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.registryImage.RegistryImageBuildUlimitList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea98e0c7b5c889af5baf478925143c7f8735af2362b2077f58ce8760cfd33cf6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RegistryImageBuildUlimitOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e9e75e76b9913447b92920b07be21b031967a069e67a30e122abc1bc591a3b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RegistryImageBuildUlimitOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e1a5fc981edfad572cfadb3e2dc2e87abbd6ca986a4d2ecbf0e54eaaf9e0298)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b434876717380afb8c3496ee1c7e30a4ac3410246ee43c21c20551f3add0fbd3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f3198de00a6597f1623bdd6a167e9070bc5c00ec50f08fcc85d17300def47bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RegistryImageBuildUlimit]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RegistryImageBuildUlimit]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RegistryImageBuildUlimit]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1f1989cdcf06c945d106c0470d570d3700943d7253f2a5e646c1ee6ae400481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class RegistryImageBuildUlimitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.registryImage.RegistryImageBuildUlimitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5675d678d39c4943d6da6997bb5467ea933a6bc7b42ab63ccf399d568949c08d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hardInput")
    def hard_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hardInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="softInput")
    def soft_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "softInput"))

    @builtins.property
    @jsii.member(jsii_name="hard")
    def hard(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hard"))

    @hard.setter
    def hard(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8246834a5ec58f161c99d9d6a3547e528019070691d1245a9902a99e196bdeea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hard", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c854584017fead7a08739bc4d6160fac7be54e1eb3aea807016de65c265f659)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="soft")
    def soft(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "soft"))

    @soft.setter
    def soft(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6e1b18e7607f47438bd96ca1fefbc925c7bace3871d61d48d4ea35ba4d1d68d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "soft", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[RegistryImageBuildUlimit, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[RegistryImageBuildUlimit, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[RegistryImageBuildUlimit, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebc6e096b015680aca2bca1323853cfc9677f57f8eb3f7ca5032642d7a334788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.registryImage.RegistryImageConfig",
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
        "build_attribute": "buildAttribute",
        "id": "id",
        "insecure_skip_verify": "insecureSkipVerify",
        "keep_remotely": "keepRemotely",
        "triggers": "triggers",
    },
)
class RegistryImageConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        build_attribute: typing.Optional[typing.Union[RegistryImageBuild, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        insecure_skip_verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        keep_remotely: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the Docker image. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#name RegistryImage#name}
        :param build_attribute: build block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#build RegistryImage#build}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#id RegistryImage#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param insecure_skip_verify: If ``true``, the verification of TLS certificates of the server/registry is disabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#insecure_skip_verify RegistryImage#insecure_skip_verify}
        :param keep_remotely: If true, then the Docker image won't be deleted on destroy operation. If this is false, it will delete the image from the docker registry on destroy operation. Defaults to ``false`` Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#keep_remotely RegistryImage#keep_remotely}
        :param triggers: A map of arbitrary strings that, when changed, will force the ``docker_registry_image`` resource to be replaced. This can be used to repush a local image Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#triggers RegistryImage#triggers}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(build_attribute, dict):
            build_attribute = RegistryImageBuild(**build_attribute)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec663aa526a906dbef76621152243db269183685f575c99b03c59a76cc4f5e5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument build_attribute", value=build_attribute, expected_type=type_hints["build_attribute"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument insecure_skip_verify", value=insecure_skip_verify, expected_type=type_hints["insecure_skip_verify"])
            check_type(argname="argument keep_remotely", value=keep_remotely, expected_type=type_hints["keep_remotely"])
            check_type(argname="argument triggers", value=triggers, expected_type=type_hints["triggers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if build_attribute is not None:
            self._values["build_attribute"] = build_attribute
        if id is not None:
            self._values["id"] = id
        if insecure_skip_verify is not None:
            self._values["insecure_skip_verify"] = insecure_skip_verify
        if keep_remotely is not None:
            self._values["keep_remotely"] = keep_remotely
        if triggers is not None:
            self._values["triggers"] = triggers

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
        '''The name of the Docker image.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#name RegistryImage#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_attribute(self) -> typing.Optional[RegistryImageBuild]:
        '''build block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#build RegistryImage#build}
        '''
        result = self._values.get("build_attribute")
        return typing.cast(typing.Optional[RegistryImageBuild], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#id RegistryImage#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure_skip_verify(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If ``true``, the verification of TLS certificates of the server/registry is disabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#insecure_skip_verify RegistryImage#insecure_skip_verify}
        '''
        result = self._values.get("insecure_skip_verify")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def keep_remotely(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, then the Docker image won't be deleted on destroy operation.

        If this is false, it will delete the image from the docker registry on destroy operation. Defaults to ``false``

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#keep_remotely RegistryImage#keep_remotely}
        '''
        result = self._values.get("keep_remotely")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def triggers(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of arbitrary strings that, when changed, will force the ``docker_registry_image`` resource to be replaced.

        This can be used to repush a local image

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/docker/r/registry_image#triggers RegistryImage#triggers}
        '''
        result = self._values.get("triggers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RegistryImageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "RegistryImage",
    "RegistryImageBuild",
    "RegistryImageBuildAuthConfig",
    "RegistryImageBuildAuthConfigList",
    "RegistryImageBuildAuthConfigOutputReference",
    "RegistryImageBuildOutputReference",
    "RegistryImageBuildUlimit",
    "RegistryImageBuildUlimitList",
    "RegistryImageBuildUlimitOutputReference",
    "RegistryImageConfig",
]

publication.publish()

def _typecheckingstub__a8c118a8ddb426cbfaee36e222bbe15cafa13cc4fbc6f1cf1024ed1432f538bb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    build_attribute: typing.Optional[typing.Union[RegistryImageBuild, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    insecure_skip_verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    keep_remotely: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__92ff8ed25cb9671772005d9fb3a69e11711118a3346a388258a936372e3b049e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__165a965a38202187f7bf254ea0a0cfdacbdcfbb38452e0d8a7ab9add712798d9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38295d51248cd1a5cc405dfe316f41c7af33e06a2fa3c287f2b065e3707f37e1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11694d42b6e4bf573a26db19b8a8d8dabbf142e3527087877358cda2ed80434b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b2638177ed35a01cf68e6834031c8e490d8a119d0333d25dfe1e70d3da68d0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3d7734d97b43ee88ad0ad921e83d1057e21b9f33f6e3e3a6d31496c78e4ec46(
    *,
    context: builtins.str,
    auth_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RegistryImageBuildAuthConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    build_id: typing.Optional[builtins.str] = None,
    cache_from: typing.Optional[typing.Sequence[builtins.str]] = None,
    cgroup_parent: typing.Optional[builtins.str] = None,
    cpu_period: typing.Optional[jsii.Number] = None,
    cpu_quota: typing.Optional[jsii.Number] = None,
    cpu_set_cpus: typing.Optional[builtins.str] = None,
    cpu_set_mems: typing.Optional[builtins.str] = None,
    cpu_shares: typing.Optional[jsii.Number] = None,
    dockerfile: typing.Optional[builtins.str] = None,
    extra_hosts: typing.Optional[typing.Sequence[builtins.str]] = None,
    force_remove: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    isolation: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    memory: typing.Optional[jsii.Number] = None,
    memory_swap: typing.Optional[jsii.Number] = None,
    network_mode: typing.Optional[builtins.str] = None,
    no_cache: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    platform: typing.Optional[builtins.str] = None,
    pull_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    remote_context: typing.Optional[builtins.str] = None,
    remove: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security_opt: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_id: typing.Optional[builtins.str] = None,
    shm_size: typing.Optional[jsii.Number] = None,
    squash: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    suppress_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    target: typing.Optional[builtins.str] = None,
    ulimit: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RegistryImageBuildUlimit, typing.Dict[builtins.str, typing.Any]]]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c76a5a4cdc30752c7e981e360ba52ffeffe4face38d45ee64d60e092e07aeff(
    *,
    host_name: builtins.str,
    auth: typing.Optional[builtins.str] = None,
    email: typing.Optional[builtins.str] = None,
    identity_token: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    registry_token: typing.Optional[builtins.str] = None,
    server_address: typing.Optional[builtins.str] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff5fd6f8ff88631cf6e99cf5d680d24fad2f7ef14395146a236eedfff61b2442(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2737d6df10e2517f2b9e928ce81f21055ab53fd44a87cd34f966fd174de9836(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe98f44dd75a16963737f79ac7f46b016ff1329d46fa2cea0de359bf4c63229(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79bceb34a0fb91e0ae8a5802365ae326156a1b5899afb6521308f2b80be4c784(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a121422dd647d77ccea4bd9560ac6c238222a5c8c4997effcf1be4646e3e5d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb45a5940e2ab1a5920723e7142c74afc7ef32af26f9d54443391684ba28816(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RegistryImageBuildAuthConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1be73ea269fcf682f1d1ae6e036cdbefdf06edc7fdf0aaf3def052ae7e6ef91e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efcefb0382068646bc08ffaa682c84853af3621bb01132c9522a542725b82013(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad0e84522d5e2971f61a8659e5e08a3e7efe7f4142823836f90176d7f91a5ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__352f14d66c168ef9748ddc5add4bd101297f6b2050967a3c5d6e04551dbff947(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee199f5e63b63c2cc5644116ee564e33077cad88d2cdfe83ea22a2eb8594a2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__847f3dc961ebbdeec89039cf88e9b7f55db1cc272b4b945ceba541336d4ab4e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eebc50be77691df2c20945173ec87353f7da48f86f601e9261f8040156129c26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91216d45e3205b950df1cf526b22bb39958fd46d1303fd6cf0b8bce168c0070e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3987b0cb1029e3ed4f82b547dfb53fa8a02267b886bceb28e61e06064ef5a5b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827a7e6d6006ecf4342ce1b505624dce23f9632cc19a5441049541537af55ae4(
    value: typing.Optional[typing.Union[RegistryImageBuildAuthConfig, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9c2224f07239710be5582e9b11faa2448fdfdb6d5aa8281841c952746f4ffe9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba22307fe29dc7ce77a5e3463d224e40dd32f2c7759253922b0088540462ef3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RegistryImageBuildAuthConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aadc7511fe3b35cc3c109d3b035c731c418ea1ff2f2d8e84a0b96be86c01acf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RegistryImageBuildUlimit, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12f4e6371a193d3940adb267660083b5a529eb0cf35ee53b6ffcc117ee3c4a79(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50988c08337c7c1c56fa6c22c01e768c1f6de3dec1fba5a88eeb658f78fc84e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c671b3debce2786f3ae75f3fd9053822587bfd8fe01a044b5780b6a2c172a5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d40b62b1dc64cf325037fd3ea6cb6cba15d71685b757ffcc403311f72f22dc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__781b5fbda732f4fbe73d117ea516393f412c9d061e3c2e599e252983c549486c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__896645c01ad9689cf83b535698db00f0d67de36b0f673aac838d4997e190b2bf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d3038ed8954c51a177def9cddef5bb3315dbbd0d057ee886d8d07c002bdbff9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9106875216678bf92e8406d39f6659984c13f21f4aa9165ef44b8b21501e61f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f730b896da6bf0f9884247c577f6c4c8b274176c8342eb136be2e2cdda0ba7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf70c5d99a674c32cd8fee2ee01b70fde265221f83cc023a2f769ca8fc49c1e6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e989ba0949fc93d6c1efdd0f125f72c3a09ec0fe7cef5ff8c5b76f9b0063db7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__700dfc8589f6c3027e151a81b03374ce548c9b0379362c6dabd71900175f9140(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3321815637fb34460e9ebfcb63076d7bf9d24aa81f651eecf87680cbbcfef118(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e20afe5aff8cf4beb8280c86b0b02e7ca553f90fe69421a18e18255c8ca17029(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf5fd911bd71b1c93c8cfd16a9f803a6c2e00cac6454f8729374542764cca77(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d654fb8f581ae1ac867b9a9b1deda4380715a8755501375e1ceb6150ad79cda(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7840fa0ee2d8b16d95b4c7869cc9c96cf461bdc2c594a10329e889a0a847745(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45bef4d80c3ea0a93fff4f2ab8488d237e9c417f3d595d20d64c6551a03acf52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23375eb7cd5e57ca73315df73a8e3d20dfb301f176892ccc92bb4968442dbe46(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd1d6c1e78f158de4bb570998e175157ea3366e8fd91d15ec8b86f922eae0b3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea9f8d056ef631094ec5cc8fcb17f4bf61c09c5bbd96aa9d99a5b54f405d64a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__179f336ab57de28bb15f3e5c76af7ad1404f507cfff79757db495c3d56390163(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a417a9cc222bf57e3c9c82c929f1ec7d25db643050aad178c5a6396feab3c0c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40844e1f3c2e902bd9172b1144840c9117cbd8e72072de31a8e4b4a4658ce850(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b5bd53bb08c6839c537e5aca62a47aa52bdb854411bcf58732af5ccdf3aa2f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c098c724dc2a8f86b7aa0830780061c4bc6c25d829ecacf99be802712aca42b3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0452f6887bab8464b55998fc5772e8bc81baf01f63dae64d58664330af1af6c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03eeb850b4a7c0f8f0e90bae72fd619ce67bdda983bd5d8cfa3fab5523f02ac6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27a7a036802ef069e24def60666d725ce79e36ff6100c5d5075efdc8b2f0e994(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7a0e7710f178b3cad180777f81833d347f6e9b33a0a9289e522a0d200380140(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8950f81025c8d1106bbc5a0959cb7b474def122ad6a98c318388ba4592aa282(
    value: typing.Optional[RegistryImageBuild],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1dbb8cb3af5f77f82d16bd279a1bc37041eb117c61d9d8226c8534ab3c785d1(
    *,
    hard: jsii.Number,
    name: builtins.str,
    soft: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea98e0c7b5c889af5baf478925143c7f8735af2362b2077f58ce8760cfd33cf6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e9e75e76b9913447b92920b07be21b031967a069e67a30e122abc1bc591a3b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1a5fc981edfad572cfadb3e2dc2e87abbd6ca986a4d2ecbf0e54eaaf9e0298(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b434876717380afb8c3496ee1c7e30a4ac3410246ee43c21c20551f3add0fbd3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3198de00a6597f1623bdd6a167e9070bc5c00ec50f08fcc85d17300def47bb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1f1989cdcf06c945d106c0470d570d3700943d7253f2a5e646c1ee6ae400481(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RegistryImageBuildUlimit]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5675d678d39c4943d6da6997bb5467ea933a6bc7b42ab63ccf399d568949c08d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8246834a5ec58f161c99d9d6a3547e528019070691d1245a9902a99e196bdeea(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c854584017fead7a08739bc4d6160fac7be54e1eb3aea807016de65c265f659(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6e1b18e7607f47438bd96ca1fefbc925c7bace3871d61d48d4ea35ba4d1d68d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebc6e096b015680aca2bca1323853cfc9677f57f8eb3f7ca5032642d7a334788(
    value: typing.Optional[typing.Union[RegistryImageBuildUlimit, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec663aa526a906dbef76621152243db269183685f575c99b03c59a76cc4f5e5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    build_attribute: typing.Optional[typing.Union[RegistryImageBuild, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    insecure_skip_verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    keep_remotely: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
