'''
# @dontirun/state-machine-semaphore

[![npm version](https://img.shields.io/npm/v/@dontirun/state-machine-semaphore.svg)](https://img.shields.io/npm/v/@dontirun/state-machine-semaphore)
[![PyPI version](https://img.shields.io/pypi/v/state-machine-semaphore.svg)](https://pypi.org/project/state-machine-semaphore)
[![NuGet version](https://img.shields.io/nuget/v/Dontirun.StateMachineSemaphore)](https://www.nuget.org/packages/Dontirun.StateMachineSemaphore)
[![Maven version](https://img.shields.io/maven-central/v/io.github.dontirun/statemachinesemaphore)](https://search.maven.org/artifact/io.github.dontirun/statemachinesemaphore)
[![Go version](https://img.shields.io/github/go-mod/go-version/dontirun/state-machine-semaphore-go?color=orange&filename=dontirunstatemachinesemaphore%2Fgo.mod)](https://github.com/dontirun/state-machine-semaphore-go)

[![View on Construct Hub](https://constructs.dev/badge?package=%40dontirun%2Fstate-machine-semaphore)](https://constructs.dev/packages/@dontirun/state-machine-semaphore)

An [aws-cdk](https://github.com/aws/aws-cdk) construct that enables you to use AWS Step Functions to control concurrency in your distributed system. You can use this construct to distributed state machine semaphores to control concurrent invocations of contentious work.

This construct is based off of [Justin Callison's](https://github.com/JustinCallison) example [code](https://github.com/aws-samples/aws-stepfunctions-examples/blob/main/sam/app-control-concurrency-with-dynamodb/statemachines/dynamodb-semaphore.asl.json). Make sure to check out Justin's [blogpost](https://aws.amazon.com/blogs/compute/controlling-concurrency-in-distributed-systems-using-aws-step-functions/) to learn about how the system works.

## Examples

### Example 1) A state machine with a controlled job

<details><summary>Click to see code</summary>

```python
import { Function } from 'aws-cdk-lib/aws-lambda';
import { Duration, Stack, StackProps } from 'aws-cdk-lib';
import { StateMachine, Succeed, Wait, WaitTime } from 'aws-cdk-lib/aws-stepfunctions';
import { LambdaInvoke } from 'aws-cdk-lib/aws-stepfunctions-tasks';
import { Construct } from 'constructs';
import { Semaphore } from '@dontirun/state-machine-semaphore';


export class CdkTestStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const contestedJob = new LambdaInvoke(this, 'ContestedJobPart1', {
      lambdaFunction: Function.fromFunctionName(this, 'JobFunctionPart1', 'cool-function'),
    }).next(new Wait(this, 'Wait', { time: WaitTime.duration(Duration.seconds(7)) }))
      .next(new Wait(this, 'AnotherWait', { time: WaitTime.duration(Duration.seconds(7)) }))
      .next(new Wait(this, 'YetAnotherWait', { time: WaitTime.duration(Duration.seconds(7)) }));

    const afterContestedJob = new Succeed(this, 'Succeed');

    const stateMachineFragment = new Semaphore(stack, 'Semaphore', { lockName: 'life', limit: 42, job: contestedJob, nextState: afterContestedJob });

    new StateMachine(this, 'StateMachine', {
      definition: stateMachineFragment,
    });
  }
}
```

</details><details><summary>Click to see the state machine definition</summary>

![Example 1 Definition](./images/Example1_Graph_Edit.png)

</details>

### Example 2) A state machine with multiple semaphores

<details><summary>Click to see code</summary>

```python
import { Function } from 'aws-cdk-lib/aws-lambda';
import { Duration, Stack, StackProps } from 'aws-cdk-lib';
import { StateMachine, Succeed, Wait, WaitTime } from 'aws-cdk-lib/aws-stepfunctions';
import { LambdaInvoke } from 'aws-cdk-lib/aws-stepfunctions-tasks';
import { Construct } from 'constructs';
import { Semaphore } from '@dontirun/state-machine-semaphore';


export class CdkTestStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const contestedJob = new LambdaInvoke(this, 'ContestedJobPart1', {
      lambdaFunction: Function.fromFunctionName(this, 'JobFunctionPart1', 'cool-function'),
    })
    const notContestedJob = new LambdaInvoke(this, 'NotContestedJob', {
      lambdaFunction: Function.fromFunctionName(this, 'NotContestedJobFunction', 'cooler-function'),
    })
    const contestedJob2 = new LambdaInvoke(this, 'ContestedJobPart2', {
      lambdaFunction: Function.fromFunctionName(this, 'JobFunctionPart2', 'coolest-function'),
    })
    const afterContestedJob2 = new Succeed(this, 'Succeed');

    const definition = new Semaphore(stack, 'Semaphore', { lockName: 'life', limit: 42, job: contestedJob, nextState: notContestedJob })
      .next(new Semaphore(stack, 'Semaphore2', { lockName: 'liberty', limit: 7, job: contestedJob2, nextState: afterContestedJob2 }));

    new StateMachine(this, 'StateMachine', {
      definition: definition,
    });
  }
}
```

</details><details><summary>Click to see the state machine definition</summary>

![Example 2 Definition](./images/Example2_Graph_Edit.png)

</details>

## API Reference

See [API.md](./API.md).

## License

This project is licensed under the Apache-2.0 License.
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

from ._jsii import *

import aws_cdk.aws_stepfunctions as _aws_cdk_aws_stepfunctions_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.interface(jsii_type="@dontirun/state-machine-semaphore.IChainNextable")
class IChainNextable(
    _aws_cdk_aws_stepfunctions_ceddda9d.IChainable,
    _aws_cdk_aws_stepfunctions_ceddda9d.INextable,
    typing_extensions.Protocol,
):
    pass


class _IChainNextableProxy(
    jsii.proxy_for(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable), # type: ignore[misc]
    jsii.proxy_for(_aws_cdk_aws_stepfunctions_ceddda9d.INextable), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@dontirun/state-machine-semaphore.IChainNextable"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IChainNextable).__jsii_proxy_class__ = lambda : _IChainNextableProxy


class Semaphore(
    _aws_cdk_aws_stepfunctions_ceddda9d.StateMachineFragment,
    metaclass=jsii.JSIIMeta,
    jsii_type="@dontirun/state-machine-semaphore.Semaphore",
):
    '''Generates a semaphore for a StepFunction job (or chained set of jobs) to limit parallelism across executions.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        job: IChainNextable,
        limit: jsii.Number,
        lock_name: builtins.str,
        next_state: _aws_cdk_aws_stepfunctions_ceddda9d.State,
        comments: typing.Optional[builtins.bool] = None,
        reuse_lock: typing.Optional[builtins.bool] = None,
        table_read_write_capacity: typing.Optional[typing.Union["TableReadWriteCapacity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param job: The job (or chained jobs) to be semaphored.
        :param limit: The maximum number of concurrent executions for the given lock.
        :param lock_name: The name of the semaphore.
        :param next_state: The State to go to after the semaphored job completes.
        :param comments: Add detailed comments to lock related states. Significantly increases CloudFormation template size. Default: false.
        :param reuse_lock: Explicility allow the reuse of a named lock from a previously generated job. Throws an error if a different ``limit`` is specified. Default: false.
        :param table_read_write_capacity: Optionally set the DynamoDB table to have a specific read/write capacity with PROVISIONED billing. Note: This property can only be set on the first instantiation of a ``Semaphore`` per stack Default: PAY_PER_REQUEST
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ca016e78c06471897f94d1abe25cb73671af597e2e20eda476d7afe2fe8b547)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SemaphoreProps(
            job=job,
            limit=limit,
            lock_name=lock_name,
            next_state=next_state,
            comments=comments,
            reuse_lock=reuse_lock,
            table_read_write_capacity=table_read_write_capacity,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List[_aws_cdk_aws_stepfunctions_ceddda9d.INextable]:
        '''The states to chain onto if this fragment is used.'''
        return typing.cast(typing.List[_aws_cdk_aws_stepfunctions_ceddda9d.INextable], jsii.get(self, "endStates"))

    @builtins.property
    @jsii.member(jsii_name="startState")
    def start_state(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.State:
        '''The start state of this state machine fragment.'''
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.State, jsii.get(self, "startState"))


@jsii.data_type(
    jsii_type="@dontirun/state-machine-semaphore.SemaphoreProps",
    jsii_struct_bases=[],
    name_mapping={
        "job": "job",
        "limit": "limit",
        "lock_name": "lockName",
        "next_state": "nextState",
        "comments": "comments",
        "reuse_lock": "reuseLock",
        "table_read_write_capacity": "tableReadWriteCapacity",
    },
)
class SemaphoreProps:
    def __init__(
        self,
        *,
        job: IChainNextable,
        limit: jsii.Number,
        lock_name: builtins.str,
        next_state: _aws_cdk_aws_stepfunctions_ceddda9d.State,
        comments: typing.Optional[builtins.bool] = None,
        reuse_lock: typing.Optional[builtins.bool] = None,
        table_read_write_capacity: typing.Optional[typing.Union["TableReadWriteCapacity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Interface for creating a Semaphore.

        :param job: The job (or chained jobs) to be semaphored.
        :param limit: The maximum number of concurrent executions for the given lock.
        :param lock_name: The name of the semaphore.
        :param next_state: The State to go to after the semaphored job completes.
        :param comments: Add detailed comments to lock related states. Significantly increases CloudFormation template size. Default: false.
        :param reuse_lock: Explicility allow the reuse of a named lock from a previously generated job. Throws an error if a different ``limit`` is specified. Default: false.
        :param table_read_write_capacity: Optionally set the DynamoDB table to have a specific read/write capacity with PROVISIONED billing. Note: This property can only be set on the first instantiation of a ``Semaphore`` per stack Default: PAY_PER_REQUEST
        '''
        if isinstance(table_read_write_capacity, dict):
            table_read_write_capacity = TableReadWriteCapacity(**table_read_write_capacity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d2f3ae3c8824281d16f1458e27897f16c6c26c278e4f199e1b9074cc3c6e9ed)
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument lock_name", value=lock_name, expected_type=type_hints["lock_name"])
            check_type(argname="argument next_state", value=next_state, expected_type=type_hints["next_state"])
            check_type(argname="argument comments", value=comments, expected_type=type_hints["comments"])
            check_type(argname="argument reuse_lock", value=reuse_lock, expected_type=type_hints["reuse_lock"])
            check_type(argname="argument table_read_write_capacity", value=table_read_write_capacity, expected_type=type_hints["table_read_write_capacity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "job": job,
            "limit": limit,
            "lock_name": lock_name,
            "next_state": next_state,
        }
        if comments is not None:
            self._values["comments"] = comments
        if reuse_lock is not None:
            self._values["reuse_lock"] = reuse_lock
        if table_read_write_capacity is not None:
            self._values["table_read_write_capacity"] = table_read_write_capacity

    @builtins.property
    def job(self) -> IChainNextable:
        '''The job (or chained jobs) to be semaphored.'''
        result = self._values.get("job")
        assert result is not None, "Required property 'job' is missing"
        return typing.cast(IChainNextable, result)

    @builtins.property
    def limit(self) -> jsii.Number:
        '''The maximum number of concurrent executions for the given lock.'''
        result = self._values.get("limit")
        assert result is not None, "Required property 'limit' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def lock_name(self) -> builtins.str:
        '''The name of the semaphore.'''
        result = self._values.get("lock_name")
        assert result is not None, "Required property 'lock_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def next_state(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.State:
        '''The State to go to after the semaphored job completes.'''
        result = self._values.get("next_state")
        assert result is not None, "Required property 'next_state' is missing"
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.State, result)

    @builtins.property
    def comments(self) -> typing.Optional[builtins.bool]:
        '''Add detailed comments to lock related states.

        Significantly increases CloudFormation template size. Default: false.
        '''
        result = self._values.get("comments")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def reuse_lock(self) -> typing.Optional[builtins.bool]:
        '''Explicility allow the reuse of a named lock from a previously generated job.

        Throws an error if a different ``limit`` is specified. Default: false.
        '''
        result = self._values.get("reuse_lock")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def table_read_write_capacity(self) -> typing.Optional["TableReadWriteCapacity"]:
        '''Optionally set the DynamoDB table to have a specific read/write capacity with PROVISIONED billing.

        Note: This property can only be set on the first instantiation of a ``Semaphore`` per stack

        :default: PAY_PER_REQUEST
        '''
        result = self._values.get("table_read_write_capacity")
        return typing.cast(typing.Optional["TableReadWriteCapacity"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SemaphoreProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@dontirun/state-machine-semaphore.TableReadWriteCapacity",
    jsii_struct_bases=[],
    name_mapping={"read_capacity": "readCapacity", "write_capacity": "writeCapacity"},
)
class TableReadWriteCapacity:
    def __init__(
        self,
        *,
        read_capacity: jsii.Number,
        write_capacity: jsii.Number,
    ) -> None:
        '''Read and write capacity for a PROVISIONED billing DynamoDB table.

        :param read_capacity: 
        :param write_capacity: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41776ce502c4c07b0e8f4089e3749a4a09d5b71f2709854181ab4bbe4dcfffef)
            check_type(argname="argument read_capacity", value=read_capacity, expected_type=type_hints["read_capacity"])
            check_type(argname="argument write_capacity", value=write_capacity, expected_type=type_hints["write_capacity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "read_capacity": read_capacity,
            "write_capacity": write_capacity,
        }

    @builtins.property
    def read_capacity(self) -> jsii.Number:
        result = self._values.get("read_capacity")
        assert result is not None, "Required property 'read_capacity' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def write_capacity(self) -> jsii.Number:
        result = self._values.get("write_capacity")
        assert result is not None, "Required property 'write_capacity' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableReadWriteCapacity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IChainNextable",
    "Semaphore",
    "SemaphoreProps",
    "TableReadWriteCapacity",
]

publication.publish()

def _typecheckingstub__6ca016e78c06471897f94d1abe25cb73671af597e2e20eda476d7afe2fe8b547(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    job: IChainNextable,
    limit: jsii.Number,
    lock_name: builtins.str,
    next_state: _aws_cdk_aws_stepfunctions_ceddda9d.State,
    comments: typing.Optional[builtins.bool] = None,
    reuse_lock: typing.Optional[builtins.bool] = None,
    table_read_write_capacity: typing.Optional[typing.Union[TableReadWriteCapacity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2f3ae3c8824281d16f1458e27897f16c6c26c278e4f199e1b9074cc3c6e9ed(
    *,
    job: IChainNextable,
    limit: jsii.Number,
    lock_name: builtins.str,
    next_state: _aws_cdk_aws_stepfunctions_ceddda9d.State,
    comments: typing.Optional[builtins.bool] = None,
    reuse_lock: typing.Optional[builtins.bool] = None,
    table_read_write_capacity: typing.Optional[typing.Union[TableReadWriteCapacity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41776ce502c4c07b0e8f4089e3749a4a09d5b71f2709854181ab4bbe4dcfffef(
    *,
    read_capacity: jsii.Number,
    write_capacity: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass
