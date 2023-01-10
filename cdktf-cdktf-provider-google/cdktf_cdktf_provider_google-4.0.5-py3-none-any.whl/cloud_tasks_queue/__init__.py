'''
# `google_cloud_tasks_queue`

Refer to the Terraform Registory for docs: [`google_cloud_tasks_queue`](https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue).
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


class CloudTasksQueue(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueue",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue google_cloud_tasks_queue}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        app_engine_routing_override: typing.Optional[typing.Union["CloudTasksQueueAppEngineRoutingOverride", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        rate_limits: typing.Optional[typing.Union["CloudTasksQueueRateLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_config: typing.Optional[typing.Union["CloudTasksQueueRetryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        stackdriver_logging_config: typing.Optional[typing.Union["CloudTasksQueueStackdriverLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["CloudTasksQueueTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue google_cloud_tasks_queue} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the queue. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#location CloudTasksQueue#location}
        :param app_engine_routing_override: app_engine_routing_override block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#app_engine_routing_override CloudTasksQueue#app_engine_routing_override}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#id CloudTasksQueue#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: The queue name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#name CloudTasksQueue#name}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#project CloudTasksQueue#project}.
        :param rate_limits: rate_limits block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#rate_limits CloudTasksQueue#rate_limits}
        :param retry_config: retry_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#retry_config CloudTasksQueue#retry_config}
        :param stackdriver_logging_config: stackdriver_logging_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#stackdriver_logging_config CloudTasksQueue#stackdriver_logging_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#timeouts CloudTasksQueue#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af4b65c7c98de529a56114659ee7eea05c423eb2573bf13ef256640ec5537628)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudTasksQueueConfig(
            location=location,
            app_engine_routing_override=app_engine_routing_override,
            id=id,
            name=name,
            project=project,
            rate_limits=rate_limits,
            retry_config=retry_config,
            stackdriver_logging_config=stackdriver_logging_config,
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

    @jsii.member(jsii_name="putAppEngineRoutingOverride")
    def put_app_engine_routing_override(
        self,
        *,
        instance: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance: App instance. By default, the task is sent to an instance which is available when the task is attempted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#instance CloudTasksQueue#instance}
        :param service: App service. By default, the task is sent to the service which is the default service when the task is attempted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#service CloudTasksQueue#service}
        :param version: App version. By default, the task is sent to the version which is the default version when the task is attempted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#version CloudTasksQueue#version}
        '''
        value = CloudTasksQueueAppEngineRoutingOverride(
            instance=instance, service=service, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putAppEngineRoutingOverride", [value]))

    @jsii.member(jsii_name="putRateLimits")
    def put_rate_limits(
        self,
        *,
        max_concurrent_dispatches: typing.Optional[jsii.Number] = None,
        max_dispatches_per_second: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrent_dispatches: The maximum number of concurrent tasks that Cloud Tasks allows to be dispatched for this queue. After this threshold has been reached, Cloud Tasks stops dispatching tasks until the number of concurrent requests decreases. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#max_concurrent_dispatches CloudTasksQueue#max_concurrent_dispatches}
        :param max_dispatches_per_second: The maximum rate at which tasks are dispatched from this queue. If unspecified when the queue is created, Cloud Tasks will pick the default. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#max_dispatches_per_second CloudTasksQueue#max_dispatches_per_second}
        '''
        value = CloudTasksQueueRateLimits(
            max_concurrent_dispatches=max_concurrent_dispatches,
            max_dispatches_per_second=max_dispatches_per_second,
        )

        return typing.cast(None, jsii.invoke(self, "putRateLimits", [value]))

    @jsii.member(jsii_name="putRetryConfig")
    def put_retry_config(
        self,
        *,
        max_attempts: typing.Optional[jsii.Number] = None,
        max_backoff: typing.Optional[builtins.str] = None,
        max_doublings: typing.Optional[jsii.Number] = None,
        max_retry_duration: typing.Optional[builtins.str] = None,
        min_backoff: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_attempts: Number of attempts per task. Cloud Tasks will attempt the task maxAttempts times (that is, if the first attempt fails, then there will be maxAttempts - 1 retries). Must be >= -1. If unspecified when the queue is created, Cloud Tasks will pick the default. -1 indicates unlimited attempts. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#max_attempts CloudTasksQueue#max_attempts}
        :param max_backoff: A task will be scheduled for retry between minBackoff and maxBackoff duration after it fails, if the queue's RetryConfig specifies that the task should be retried. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#max_backoff CloudTasksQueue#max_backoff}
        :param max_doublings: The time between retries will double maxDoublings times. A task's retry interval starts at minBackoff, then doubles maxDoublings times, then increases linearly, and finally retries retries at intervals of maxBackoff up to maxAttempts times. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#max_doublings CloudTasksQueue#max_doublings}
        :param max_retry_duration: If positive, maxRetryDuration specifies the time limit for retrying a failed task, measured from when the task was first attempted. Once maxRetryDuration time has passed and the task has been attempted maxAttempts times, no further attempts will be made and the task will be deleted. If zero, then the task age is unlimited. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#max_retry_duration CloudTasksQueue#max_retry_duration}
        :param min_backoff: A task will be scheduled for retry between minBackoff and maxBackoff duration after it fails, if the queue's RetryConfig specifies that the task should be retried. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#min_backoff CloudTasksQueue#min_backoff}
        '''
        value = CloudTasksQueueRetryConfig(
            max_attempts=max_attempts,
            max_backoff=max_backoff,
            max_doublings=max_doublings,
            max_retry_duration=max_retry_duration,
            min_backoff=min_backoff,
        )

        return typing.cast(None, jsii.invoke(self, "putRetryConfig", [value]))

    @jsii.member(jsii_name="putStackdriverLoggingConfig")
    def put_stackdriver_logging_config(self, *, sampling_ratio: jsii.Number) -> None:
        '''
        :param sampling_ratio: Specifies the fraction of operations to write to Stackdriver Logging. This field may contain any value between 0.0 and 1.0, inclusive. 0.0 is the default and means that no operations are logged. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#sampling_ratio CloudTasksQueue#sampling_ratio}
        '''
        value = CloudTasksQueueStackdriverLoggingConfig(sampling_ratio=sampling_ratio)

        return typing.cast(None, jsii.invoke(self, "putStackdriverLoggingConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#create CloudTasksQueue#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#delete CloudTasksQueue#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#update CloudTasksQueue#update}.
        '''
        value = CloudTasksQueueTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAppEngineRoutingOverride")
    def reset_app_engine_routing_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppEngineRoutingOverride", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRateLimits")
    def reset_rate_limits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRateLimits", []))

    @jsii.member(jsii_name="resetRetryConfig")
    def reset_retry_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryConfig", []))

    @jsii.member(jsii_name="resetStackdriverLoggingConfig")
    def reset_stackdriver_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStackdriverLoggingConfig", []))

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
    @jsii.member(jsii_name="appEngineRoutingOverride")
    def app_engine_routing_override(
        self,
    ) -> "CloudTasksQueueAppEngineRoutingOverrideOutputReference":
        return typing.cast("CloudTasksQueueAppEngineRoutingOverrideOutputReference", jsii.get(self, "appEngineRoutingOverride"))

    @builtins.property
    @jsii.member(jsii_name="rateLimits")
    def rate_limits(self) -> "CloudTasksQueueRateLimitsOutputReference":
        return typing.cast("CloudTasksQueueRateLimitsOutputReference", jsii.get(self, "rateLimits"))

    @builtins.property
    @jsii.member(jsii_name="retryConfig")
    def retry_config(self) -> "CloudTasksQueueRetryConfigOutputReference":
        return typing.cast("CloudTasksQueueRetryConfigOutputReference", jsii.get(self, "retryConfig"))

    @builtins.property
    @jsii.member(jsii_name="stackdriverLoggingConfig")
    def stackdriver_logging_config(
        self,
    ) -> "CloudTasksQueueStackdriverLoggingConfigOutputReference":
        return typing.cast("CloudTasksQueueStackdriverLoggingConfigOutputReference", jsii.get(self, "stackdriverLoggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CloudTasksQueueTimeoutsOutputReference":
        return typing.cast("CloudTasksQueueTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="appEngineRoutingOverrideInput")
    def app_engine_routing_override_input(
        self,
    ) -> typing.Optional["CloudTasksQueueAppEngineRoutingOverride"]:
        return typing.cast(typing.Optional["CloudTasksQueueAppEngineRoutingOverride"], jsii.get(self, "appEngineRoutingOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitsInput")
    def rate_limits_input(self) -> typing.Optional["CloudTasksQueueRateLimits"]:
        return typing.cast(typing.Optional["CloudTasksQueueRateLimits"], jsii.get(self, "rateLimitsInput"))

    @builtins.property
    @jsii.member(jsii_name="retryConfigInput")
    def retry_config_input(self) -> typing.Optional["CloudTasksQueueRetryConfig"]:
        return typing.cast(typing.Optional["CloudTasksQueueRetryConfig"], jsii.get(self, "retryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="stackdriverLoggingConfigInput")
    def stackdriver_logging_config_input(
        self,
    ) -> typing.Optional["CloudTasksQueueStackdriverLoggingConfig"]:
        return typing.cast(typing.Optional["CloudTasksQueueStackdriverLoggingConfig"], jsii.get(self, "stackdriverLoggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["CloudTasksQueueTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["CloudTasksQueueTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bb26345cf52f11dcd4ef850ccfa20133568374589e76ce84de78fe88a2f9ed6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba7f4ba3031fd0ec8200ea71bf27105a44f16b2568c2335ecf54309d6b53b2bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de8c1aedb20aa05e746efc16a9873fc595c872b96889616a6c0348d8866d74be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db7b2a24d68b223fa27dcd372bce4798813f55128834c98a42d2451d52c50d3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueAppEngineRoutingOverride",
    jsii_struct_bases=[],
    name_mapping={"instance": "instance", "service": "service", "version": "version"},
)
class CloudTasksQueueAppEngineRoutingOverride:
    def __init__(
        self,
        *,
        instance: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance: App instance. By default, the task is sent to an instance which is available when the task is attempted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#instance CloudTasksQueue#instance}
        :param service: App service. By default, the task is sent to the service which is the default service when the task is attempted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#service CloudTasksQueue#service}
        :param version: App version. By default, the task is sent to the version which is the default version when the task is attempted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#version CloudTasksQueue#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef1c48bc18dd9d5d3d3bad0ae065a1068d71e9d3ba9cccd7e5b48ecee7e3a55f)
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance is not None:
            self._values["instance"] = instance
        if service is not None:
            self._values["service"] = service
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def instance(self) -> typing.Optional[builtins.str]:
        '''App instance.

        By default, the task is sent to an instance which is available when the task is attempted.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#instance CloudTasksQueue#instance}
        '''
        result = self._values.get("instance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''App service.

        By default, the task is sent to the service which is the default service when the task is attempted.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#service CloudTasksQueue#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''App version.

        By default, the task is sent to the version which is the default version when the task is attempted.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#version CloudTasksQueue#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudTasksQueueAppEngineRoutingOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudTasksQueueAppEngineRoutingOverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueAppEngineRoutingOverrideOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5294b28a75106c79c8d69f7d9c4052e0ef459a31fc71dbc1d983fb0ef4f44cb1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstance")
    def reset_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstance", []))

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @builtins.property
    @jsii.member(jsii_name="instanceInput")
    def instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instance"))

    @instance.setter
    def instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54f86b4a0660cdc8001b91f44bbc48bfd94884ad95c3feb2deea31b8af2d02e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value)

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f739c7806538573b239c8b622b0915e8f2911bdabc9398fc3d27bf81cbb3486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__891dc54305d15ea2ed9d7f476f32398dc7fb4f82edab0cbe988df848ade8b745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudTasksQueueAppEngineRoutingOverride]:
        return typing.cast(typing.Optional[CloudTasksQueueAppEngineRoutingOverride], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudTasksQueueAppEngineRoutingOverride],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e47552dc050adf038e62f281feabaef42512ed8a384293aafed1e0ae3023a74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "app_engine_routing_override": "appEngineRoutingOverride",
        "id": "id",
        "name": "name",
        "project": "project",
        "rate_limits": "rateLimits",
        "retry_config": "retryConfig",
        "stackdriver_logging_config": "stackdriverLoggingConfig",
        "timeouts": "timeouts",
    },
)
class CloudTasksQueueConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        app_engine_routing_override: typing.Optional[typing.Union[CloudTasksQueueAppEngineRoutingOverride, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        rate_limits: typing.Optional[typing.Union["CloudTasksQueueRateLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_config: typing.Optional[typing.Union["CloudTasksQueueRetryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        stackdriver_logging_config: typing.Optional[typing.Union["CloudTasksQueueStackdriverLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["CloudTasksQueueTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the queue. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#location CloudTasksQueue#location}
        :param app_engine_routing_override: app_engine_routing_override block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#app_engine_routing_override CloudTasksQueue#app_engine_routing_override}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#id CloudTasksQueue#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: The queue name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#name CloudTasksQueue#name}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#project CloudTasksQueue#project}.
        :param rate_limits: rate_limits block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#rate_limits CloudTasksQueue#rate_limits}
        :param retry_config: retry_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#retry_config CloudTasksQueue#retry_config}
        :param stackdriver_logging_config: stackdriver_logging_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#stackdriver_logging_config CloudTasksQueue#stackdriver_logging_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#timeouts CloudTasksQueue#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(app_engine_routing_override, dict):
            app_engine_routing_override = CloudTasksQueueAppEngineRoutingOverride(**app_engine_routing_override)
        if isinstance(rate_limits, dict):
            rate_limits = CloudTasksQueueRateLimits(**rate_limits)
        if isinstance(retry_config, dict):
            retry_config = CloudTasksQueueRetryConfig(**retry_config)
        if isinstance(stackdriver_logging_config, dict):
            stackdriver_logging_config = CloudTasksQueueStackdriverLoggingConfig(**stackdriver_logging_config)
        if isinstance(timeouts, dict):
            timeouts = CloudTasksQueueTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d72ca0923f5716abfb32b718c95c8c961a7d2deae111cd2080cabb7dfe70971f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument app_engine_routing_override", value=app_engine_routing_override, expected_type=type_hints["app_engine_routing_override"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument rate_limits", value=rate_limits, expected_type=type_hints["rate_limits"])
            check_type(argname="argument retry_config", value=retry_config, expected_type=type_hints["retry_config"])
            check_type(argname="argument stackdriver_logging_config", value=stackdriver_logging_config, expected_type=type_hints["stackdriver_logging_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
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
        if app_engine_routing_override is not None:
            self._values["app_engine_routing_override"] = app_engine_routing_override
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
        if project is not None:
            self._values["project"] = project
        if rate_limits is not None:
            self._values["rate_limits"] = rate_limits
        if retry_config is not None:
            self._values["retry_config"] = retry_config
        if stackdriver_logging_config is not None:
            self._values["stackdriver_logging_config"] = stackdriver_logging_config
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
    def location(self) -> builtins.str:
        '''The location of the queue.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#location CloudTasksQueue#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_engine_routing_override(
        self,
    ) -> typing.Optional[CloudTasksQueueAppEngineRoutingOverride]:
        '''app_engine_routing_override block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#app_engine_routing_override CloudTasksQueue#app_engine_routing_override}
        '''
        result = self._values.get("app_engine_routing_override")
        return typing.cast(typing.Optional[CloudTasksQueueAppEngineRoutingOverride], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#id CloudTasksQueue#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The queue name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#name CloudTasksQueue#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#project CloudTasksQueue#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rate_limits(self) -> typing.Optional["CloudTasksQueueRateLimits"]:
        '''rate_limits block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#rate_limits CloudTasksQueue#rate_limits}
        '''
        result = self._values.get("rate_limits")
        return typing.cast(typing.Optional["CloudTasksQueueRateLimits"], result)

    @builtins.property
    def retry_config(self) -> typing.Optional["CloudTasksQueueRetryConfig"]:
        '''retry_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#retry_config CloudTasksQueue#retry_config}
        '''
        result = self._values.get("retry_config")
        return typing.cast(typing.Optional["CloudTasksQueueRetryConfig"], result)

    @builtins.property
    def stackdriver_logging_config(
        self,
    ) -> typing.Optional["CloudTasksQueueStackdriverLoggingConfig"]:
        '''stackdriver_logging_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#stackdriver_logging_config CloudTasksQueue#stackdriver_logging_config}
        '''
        result = self._values.get("stackdriver_logging_config")
        return typing.cast(typing.Optional["CloudTasksQueueStackdriverLoggingConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CloudTasksQueueTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#timeouts CloudTasksQueue#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CloudTasksQueueTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudTasksQueueConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueRateLimits",
    jsii_struct_bases=[],
    name_mapping={
        "max_concurrent_dispatches": "maxConcurrentDispatches",
        "max_dispatches_per_second": "maxDispatchesPerSecond",
    },
)
class CloudTasksQueueRateLimits:
    def __init__(
        self,
        *,
        max_concurrent_dispatches: typing.Optional[jsii.Number] = None,
        max_dispatches_per_second: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrent_dispatches: The maximum number of concurrent tasks that Cloud Tasks allows to be dispatched for this queue. After this threshold has been reached, Cloud Tasks stops dispatching tasks until the number of concurrent requests decreases. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#max_concurrent_dispatches CloudTasksQueue#max_concurrent_dispatches}
        :param max_dispatches_per_second: The maximum rate at which tasks are dispatched from this queue. If unspecified when the queue is created, Cloud Tasks will pick the default. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#max_dispatches_per_second CloudTasksQueue#max_dispatches_per_second}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c188f34f89da88a0f1a401dcfb01acad45dd07cac777bbee3626637963d04d72)
            check_type(argname="argument max_concurrent_dispatches", value=max_concurrent_dispatches, expected_type=type_hints["max_concurrent_dispatches"])
            check_type(argname="argument max_dispatches_per_second", value=max_dispatches_per_second, expected_type=type_hints["max_dispatches_per_second"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_concurrent_dispatches is not None:
            self._values["max_concurrent_dispatches"] = max_concurrent_dispatches
        if max_dispatches_per_second is not None:
            self._values["max_dispatches_per_second"] = max_dispatches_per_second

    @builtins.property
    def max_concurrent_dispatches(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of concurrent tasks that Cloud Tasks allows to be dispatched for this queue.

        After this threshold has been
        reached, Cloud Tasks stops dispatching tasks until the number of
        concurrent requests decreases.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#max_concurrent_dispatches CloudTasksQueue#max_concurrent_dispatches}
        '''
        result = self._values.get("max_concurrent_dispatches")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_dispatches_per_second(self) -> typing.Optional[jsii.Number]:
        '''The maximum rate at which tasks are dispatched from this queue.

        If unspecified when the queue is created, Cloud Tasks will pick the default.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#max_dispatches_per_second CloudTasksQueue#max_dispatches_per_second}
        '''
        result = self._values.get("max_dispatches_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudTasksQueueRateLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudTasksQueueRateLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueRateLimitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32b9b9c0a63f7c1300a6d9b95d833e89cfd07446214c212450da5bd73ce130a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxConcurrentDispatches")
    def reset_max_concurrent_dispatches(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConcurrentDispatches", []))

    @jsii.member(jsii_name="resetMaxDispatchesPerSecond")
    def reset_max_dispatches_per_second(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDispatchesPerSecond", []))

    @builtins.property
    @jsii.member(jsii_name="maxBurstSize")
    def max_burst_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxBurstSize"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentDispatchesInput")
    def max_concurrent_dispatches_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrentDispatchesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDispatchesPerSecondInput")
    def max_dispatches_per_second_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDispatchesPerSecondInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentDispatches")
    def max_concurrent_dispatches(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrentDispatches"))

    @max_concurrent_dispatches.setter
    def max_concurrent_dispatches(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f70401ebb152ad8f5e511bb20a64ca5a1af9335808a2f0c466d40c892c0fab41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentDispatches", value)

    @builtins.property
    @jsii.member(jsii_name="maxDispatchesPerSecond")
    def max_dispatches_per_second(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDispatchesPerSecond"))

    @max_dispatches_per_second.setter
    def max_dispatches_per_second(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b24d2cab6ed38792ad89060d723cc98409736d473f91f76f959f98876d5fa54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDispatchesPerSecond", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudTasksQueueRateLimits]:
        return typing.cast(typing.Optional[CloudTasksQueueRateLimits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudTasksQueueRateLimits]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47338008cc06af963e81e997617433c18d45a89e93f9da7c090a6fabc4209f84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueRetryConfig",
    jsii_struct_bases=[],
    name_mapping={
        "max_attempts": "maxAttempts",
        "max_backoff": "maxBackoff",
        "max_doublings": "maxDoublings",
        "max_retry_duration": "maxRetryDuration",
        "min_backoff": "minBackoff",
    },
)
class CloudTasksQueueRetryConfig:
    def __init__(
        self,
        *,
        max_attempts: typing.Optional[jsii.Number] = None,
        max_backoff: typing.Optional[builtins.str] = None,
        max_doublings: typing.Optional[jsii.Number] = None,
        max_retry_duration: typing.Optional[builtins.str] = None,
        min_backoff: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_attempts: Number of attempts per task. Cloud Tasks will attempt the task maxAttempts times (that is, if the first attempt fails, then there will be maxAttempts - 1 retries). Must be >= -1. If unspecified when the queue is created, Cloud Tasks will pick the default. -1 indicates unlimited attempts. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#max_attempts CloudTasksQueue#max_attempts}
        :param max_backoff: A task will be scheduled for retry between minBackoff and maxBackoff duration after it fails, if the queue's RetryConfig specifies that the task should be retried. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#max_backoff CloudTasksQueue#max_backoff}
        :param max_doublings: The time between retries will double maxDoublings times. A task's retry interval starts at minBackoff, then doubles maxDoublings times, then increases linearly, and finally retries retries at intervals of maxBackoff up to maxAttempts times. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#max_doublings CloudTasksQueue#max_doublings}
        :param max_retry_duration: If positive, maxRetryDuration specifies the time limit for retrying a failed task, measured from when the task was first attempted. Once maxRetryDuration time has passed and the task has been attempted maxAttempts times, no further attempts will be made and the task will be deleted. If zero, then the task age is unlimited. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#max_retry_duration CloudTasksQueue#max_retry_duration}
        :param min_backoff: A task will be scheduled for retry between minBackoff and maxBackoff duration after it fails, if the queue's RetryConfig specifies that the task should be retried. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#min_backoff CloudTasksQueue#min_backoff}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0f2811ac0e591ed79fd26183a9b7c287b8df661459bf427d5e205e59a753522)
            check_type(argname="argument max_attempts", value=max_attempts, expected_type=type_hints["max_attempts"])
            check_type(argname="argument max_backoff", value=max_backoff, expected_type=type_hints["max_backoff"])
            check_type(argname="argument max_doublings", value=max_doublings, expected_type=type_hints["max_doublings"])
            check_type(argname="argument max_retry_duration", value=max_retry_duration, expected_type=type_hints["max_retry_duration"])
            check_type(argname="argument min_backoff", value=min_backoff, expected_type=type_hints["min_backoff"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_attempts is not None:
            self._values["max_attempts"] = max_attempts
        if max_backoff is not None:
            self._values["max_backoff"] = max_backoff
        if max_doublings is not None:
            self._values["max_doublings"] = max_doublings
        if max_retry_duration is not None:
            self._values["max_retry_duration"] = max_retry_duration
        if min_backoff is not None:
            self._values["min_backoff"] = min_backoff

    @builtins.property
    def max_attempts(self) -> typing.Optional[jsii.Number]:
        '''Number of attempts per task.

        Cloud Tasks will attempt the task maxAttempts times (that is, if
        the first attempt fails, then there will be maxAttempts - 1
        retries). Must be >= -1.

        If unspecified when the queue is created, Cloud Tasks will pick
        the default.

        -1 indicates unlimited attempts.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#max_attempts CloudTasksQueue#max_attempts}
        '''
        result = self._values.get("max_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_backoff(self) -> typing.Optional[builtins.str]:
        '''A task will be scheduled for retry between minBackoff and maxBackoff duration after it fails, if the queue's RetryConfig specifies that the task should be retried.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#max_backoff CloudTasksQueue#max_backoff}
        '''
        result = self._values.get("max_backoff")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_doublings(self) -> typing.Optional[jsii.Number]:
        '''The time between retries will double maxDoublings times.

        A task's retry interval starts at minBackoff, then doubles maxDoublings times,
        then increases linearly, and finally retries retries at intervals of maxBackoff
        up to maxAttempts times.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#max_doublings CloudTasksQueue#max_doublings}
        '''
        result = self._values.get("max_doublings")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retry_duration(self) -> typing.Optional[builtins.str]:
        '''If positive, maxRetryDuration specifies the time limit for retrying a failed task, measured from when the task was first attempted.

        Once maxRetryDuration time has passed and the task has
        been attempted maxAttempts times, no further attempts will be
        made and the task will be deleted.

        If zero, then the task age is unlimited.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#max_retry_duration CloudTasksQueue#max_retry_duration}
        '''
        result = self._values.get("max_retry_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_backoff(self) -> typing.Optional[builtins.str]:
        '''A task will be scheduled for retry between minBackoff and maxBackoff duration after it fails, if the queue's RetryConfig specifies that the task should be retried.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#min_backoff CloudTasksQueue#min_backoff}
        '''
        result = self._values.get("min_backoff")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudTasksQueueRetryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudTasksQueueRetryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueRetryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfa44eedd10a27db6641e71f03076ee78294bac56e68638fc7cc339491a6ca13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxAttempts")
    def reset_max_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAttempts", []))

    @jsii.member(jsii_name="resetMaxBackoff")
    def reset_max_backoff(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxBackoff", []))

    @jsii.member(jsii_name="resetMaxDoublings")
    def reset_max_doublings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDoublings", []))

    @jsii.member(jsii_name="resetMaxRetryDuration")
    def reset_max_retry_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRetryDuration", []))

    @jsii.member(jsii_name="resetMinBackoff")
    def reset_min_backoff(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinBackoff", []))

    @builtins.property
    @jsii.member(jsii_name="maxAttemptsInput")
    def max_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxBackoffInput")
    def max_backoff_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxBackoffInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDoublingsInput")
    def max_doublings_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDoublingsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetryDurationInput")
    def max_retry_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxRetryDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="minBackoffInput")
    def min_backoff_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minBackoffInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAttempts")
    def max_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAttempts"))

    @max_attempts.setter
    def max_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96cdb24212b9a4b09c0b8cf9dcbe159faf5e54a7b4ec17308d9fd7691d39d10f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAttempts", value)

    @builtins.property
    @jsii.member(jsii_name="maxBackoff")
    def max_backoff(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxBackoff"))

    @max_backoff.setter
    def max_backoff(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02dc0fdc017d4104ab34380472563fbe905d6b0f1f8b082626ba7ec42fbeb8b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBackoff", value)

    @builtins.property
    @jsii.member(jsii_name="maxDoublings")
    def max_doublings(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDoublings"))

    @max_doublings.setter
    def max_doublings(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a45a466758e50c756c397e3a387720a5d04a1367c8f7bb3d362af471b77c6cc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDoublings", value)

    @builtins.property
    @jsii.member(jsii_name="maxRetryDuration")
    def max_retry_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxRetryDuration"))

    @max_retry_duration.setter
    def max_retry_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22b6e6681febdefe45da0fccded2ad178f9a0a89ceb02f4e32d000bf2115cc34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetryDuration", value)

    @builtins.property
    @jsii.member(jsii_name="minBackoff")
    def min_backoff(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minBackoff"))

    @min_backoff.setter
    def min_backoff(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b848bed0eefda95625ae4333bd791b6938d70df8d1d5d766a74b1c822420774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minBackoff", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudTasksQueueRetryConfig]:
        return typing.cast(typing.Optional[CloudTasksQueueRetryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudTasksQueueRetryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b18b57fa721c854a7077b094515ec33791a71ef45bbf13aa1d60154236183c00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueStackdriverLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"sampling_ratio": "samplingRatio"},
)
class CloudTasksQueueStackdriverLoggingConfig:
    def __init__(self, *, sampling_ratio: jsii.Number) -> None:
        '''
        :param sampling_ratio: Specifies the fraction of operations to write to Stackdriver Logging. This field may contain any value between 0.0 and 1.0, inclusive. 0.0 is the default and means that no operations are logged. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#sampling_ratio CloudTasksQueue#sampling_ratio}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f818077b4fe25b36b9ab62ed7caf6608ede7d537fbff8993809ebde31290f4)
            check_type(argname="argument sampling_ratio", value=sampling_ratio, expected_type=type_hints["sampling_ratio"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sampling_ratio": sampling_ratio,
        }

    @builtins.property
    def sampling_ratio(self) -> jsii.Number:
        '''Specifies the fraction of operations to write to Stackdriver Logging.

        This field may contain any value between 0.0 and 1.0, inclusive. 0.0 is the
        default and means that no operations are logged.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#sampling_ratio CloudTasksQueue#sampling_ratio}
        '''
        result = self._values.get("sampling_ratio")
        assert result is not None, "Required property 'sampling_ratio' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudTasksQueueStackdriverLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudTasksQueueStackdriverLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueStackdriverLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e1151b61c2a33795681934d7e5e51e7ae95bbede9819a27ee4475f77ed2dbc5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="samplingRatioInput")
    def sampling_ratio_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "samplingRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="samplingRatio")
    def sampling_ratio(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "samplingRatio"))

    @sampling_ratio.setter
    def sampling_ratio(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e68cc0d654a74ad7fcbe798d7bd4a60366080def91cfce8a8adae4c04af3eeba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samplingRatio", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudTasksQueueStackdriverLoggingConfig]:
        return typing.cast(typing.Optional[CloudTasksQueueStackdriverLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudTasksQueueStackdriverLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a149839d90144a82e856636ea407526726265a8a75c8a80c8bff50199a427ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CloudTasksQueueTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#create CloudTasksQueue#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#delete CloudTasksQueue#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#update CloudTasksQueue#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bdb91fbc81ec2def08756553d5d01255a5e8a182081c7c355580e6f1a8765f3)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#create CloudTasksQueue#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#delete CloudTasksQueue#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_tasks_queue#update CloudTasksQueue#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudTasksQueueTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudTasksQueueTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f83bd6954e7b28b58bf1554324a87ef5f285d96f0c604a35e6134cc70efc3d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a56bb4e3d211f674a78b0e3079ae2dbb5dbd1282856f43ea842db47142642d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b624e509eda58d258ef887cb86d0a12d230c1da9412a145b81566340647704d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09c0e53b53fe4357eb078fdae7c50d49e88107a617726ccf557503577574d35b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CloudTasksQueueTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CloudTasksQueueTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CloudTasksQueueTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__653fa230e7363c42e111946e56a3f9ff66b69a4c2431ebc9101994af211a8734)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "CloudTasksQueue",
    "CloudTasksQueueAppEngineRoutingOverride",
    "CloudTasksQueueAppEngineRoutingOverrideOutputReference",
    "CloudTasksQueueConfig",
    "CloudTasksQueueRateLimits",
    "CloudTasksQueueRateLimitsOutputReference",
    "CloudTasksQueueRetryConfig",
    "CloudTasksQueueRetryConfigOutputReference",
    "CloudTasksQueueStackdriverLoggingConfig",
    "CloudTasksQueueStackdriverLoggingConfigOutputReference",
    "CloudTasksQueueTimeouts",
    "CloudTasksQueueTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__af4b65c7c98de529a56114659ee7eea05c423eb2573bf13ef256640ec5537628(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    app_engine_routing_override: typing.Optional[typing.Union[CloudTasksQueueAppEngineRoutingOverride, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    rate_limits: typing.Optional[typing.Union[CloudTasksQueueRateLimits, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_config: typing.Optional[typing.Union[CloudTasksQueueRetryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    stackdriver_logging_config: typing.Optional[typing.Union[CloudTasksQueueStackdriverLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[CloudTasksQueueTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5bb26345cf52f11dcd4ef850ccfa20133568374589e76ce84de78fe88a2f9ed6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba7f4ba3031fd0ec8200ea71bf27105a44f16b2568c2335ecf54309d6b53b2bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8c1aedb20aa05e746efc16a9873fc595c872b96889616a6c0348d8866d74be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db7b2a24d68b223fa27dcd372bce4798813f55128834c98a42d2451d52c50d3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef1c48bc18dd9d5d3d3bad0ae065a1068d71e9d3ba9cccd7e5b48ecee7e3a55f(
    *,
    instance: typing.Optional[builtins.str] = None,
    service: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5294b28a75106c79c8d69f7d9c4052e0ef459a31fc71dbc1d983fb0ef4f44cb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f86b4a0660cdc8001b91f44bbc48bfd94884ad95c3feb2deea31b8af2d02e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f739c7806538573b239c8b622b0915e8f2911bdabc9398fc3d27bf81cbb3486(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891dc54305d15ea2ed9d7f476f32398dc7fb4f82edab0cbe988df848ade8b745(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e47552dc050adf038e62f281feabaef42512ed8a384293aafed1e0ae3023a74(
    value: typing.Optional[CloudTasksQueueAppEngineRoutingOverride],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d72ca0923f5716abfb32b718c95c8c961a7d2deae111cd2080cabb7dfe70971f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    app_engine_routing_override: typing.Optional[typing.Union[CloudTasksQueueAppEngineRoutingOverride, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    rate_limits: typing.Optional[typing.Union[CloudTasksQueueRateLimits, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_config: typing.Optional[typing.Union[CloudTasksQueueRetryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    stackdriver_logging_config: typing.Optional[typing.Union[CloudTasksQueueStackdriverLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[CloudTasksQueueTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c188f34f89da88a0f1a401dcfb01acad45dd07cac777bbee3626637963d04d72(
    *,
    max_concurrent_dispatches: typing.Optional[jsii.Number] = None,
    max_dispatches_per_second: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b9b9c0a63f7c1300a6d9b95d833e89cfd07446214c212450da5bd73ce130a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f70401ebb152ad8f5e511bb20a64ca5a1af9335808a2f0c466d40c892c0fab41(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b24d2cab6ed38792ad89060d723cc98409736d473f91f76f959f98876d5fa54(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47338008cc06af963e81e997617433c18d45a89e93f9da7c090a6fabc4209f84(
    value: typing.Optional[CloudTasksQueueRateLimits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f2811ac0e591ed79fd26183a9b7c287b8df661459bf427d5e205e59a753522(
    *,
    max_attempts: typing.Optional[jsii.Number] = None,
    max_backoff: typing.Optional[builtins.str] = None,
    max_doublings: typing.Optional[jsii.Number] = None,
    max_retry_duration: typing.Optional[builtins.str] = None,
    min_backoff: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa44eedd10a27db6641e71f03076ee78294bac56e68638fc7cc339491a6ca13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96cdb24212b9a4b09c0b8cf9dcbe159faf5e54a7b4ec17308d9fd7691d39d10f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02dc0fdc017d4104ab34380472563fbe905d6b0f1f8b082626ba7ec42fbeb8b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a45a466758e50c756c397e3a387720a5d04a1367c8f7bb3d362af471b77c6cc9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22b6e6681febdefe45da0fccded2ad178f9a0a89ceb02f4e32d000bf2115cc34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b848bed0eefda95625ae4333bd791b6938d70df8d1d5d766a74b1c822420774(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18b57fa721c854a7077b094515ec33791a71ef45bbf13aa1d60154236183c00(
    value: typing.Optional[CloudTasksQueueRetryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f818077b4fe25b36b9ab62ed7caf6608ede7d537fbff8993809ebde31290f4(
    *,
    sampling_ratio: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1151b61c2a33795681934d7e5e51e7ae95bbede9819a27ee4475f77ed2dbc5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e68cc0d654a74ad7fcbe798d7bd4a60366080def91cfce8a8adae4c04af3eeba(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a149839d90144a82e856636ea407526726265a8a75c8a80c8bff50199a427ab(
    value: typing.Optional[CloudTasksQueueStackdriverLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bdb91fbc81ec2def08756553d5d01255a5e8a182081c7c355580e6f1a8765f3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f83bd6954e7b28b58bf1554324a87ef5f285d96f0c604a35e6134cc70efc3d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a56bb4e3d211f674a78b0e3079ae2dbb5dbd1282856f43ea842db47142642d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b624e509eda58d258ef887cb86d0a12d230c1da9412a145b81566340647704d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c0e53b53fe4357eb078fdae7c50d49e88107a617726ccf557503577574d35b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653fa230e7363c42e111946e56a3f9ff66b69a4c2431ebc9101994af211a8734(
    value: typing.Optional[typing.Union[CloudTasksQueueTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
