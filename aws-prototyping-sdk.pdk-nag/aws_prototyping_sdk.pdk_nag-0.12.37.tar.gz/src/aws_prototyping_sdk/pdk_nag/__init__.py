'''
## PDK Nag

PDKNag ships with a helper utility that automatically configures CDKNag within your application.

```python
const app = PDKNag.app();
const stack = new Stack(app, 'MyStack');
...
```

As shown above, this will configure your application to have CDKNag run on synthesis.

By default, CDK will trigger a failure on `synth` if any errors are encountered. To relax these, run the following:

```shell
cdk synth --ignore-errors
```

Conversely, CDK will not fail on synth if warnings are detected. To enforce that all warnings are resolved, run the following command:

```shell
cdk synth --strict
```

### Instrumenting custom NagPacks

By default, when creating a PDKNag application the [AwsSolutions](https://github.com/cdklabs/cdk-nag/blob/main/RULES.md) NagPack is instrumented. In order to specify custom NagPacks to instrument, you can configure the PDKApp as follows:

```python
import { PDKNag, AwsPrototypingChecks } from "@aws-prototyping-sdk/pdk-nag";

const app = PDKNag.app({
    nagPacks: [new AwsPrototypingChecks()]
});
```

In this example, the [AwsPrototypingChecks](https://github.com/aws/aws-prototyping-sdk/blob/mainline/packages/pdk-nag/src/packs/README.md) NagPack has been configured to run instead of the default. Multiple NagPacks can also be instrumented by adding NagPack instances to the `nagPacks` array;
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

import aws_cdk
import aws_cdk.cx_api
import cdk_nag
import constructs


class AwsPrototypingChecks(
    cdk_nag.NagPack,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/pdk-nag.AwsPrototypingChecks",
):
    '''Check best practices for prototypes.'''

    def __init__(
        self,
        *,
        log_ignores: typing.Optional[builtins.bool] = None,
        reports: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param log_ignores: Whether or not to log triggered rules that have been suppressed as informational messages (default: false).
        :param reports: Whether or not to generate CSV compliance reports for applied Stacks in the App's output directory (default: true).
        :param verbose: Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        '''
        props = cdk_nag.NagPackProps(
            log_ignores=log_ignores, reports=reports, verbose=verbose
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: constructs.IConstruct) -> None:
        '''Check if CfnResource and apply rules.

        :param node: -
        '''
        if __debug__:
            def stub(node: constructs.IConstruct) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/pdk-nag.Message",
    jsii_struct_bases=[],
    name_mapping={
        "message_description": "messageDescription",
        "message_type": "messageType",
    },
)
class Message:
    def __init__(
        self,
        *,
        message_description: builtins.str,
        message_type: builtins.str,
    ) -> None:
        '''Message instance.

        :param message_description: Message description.
        :param message_type: Message type as returned from cdk-nag.
        '''
        if __debug__:
            def stub(
                *,
                message_description: builtins.str,
                message_type: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument message_description", value=message_description, expected_type=type_hints["message_description"])
            check_type(argname="argument message_type", value=message_type, expected_type=type_hints["message_type"])
        self._values: typing.Dict[str, typing.Any] = {
            "message_description": message_description,
            "message_type": message_type,
        }

    @builtins.property
    def message_description(self) -> builtins.str:
        '''Message description.'''
        result = self._values.get("message_description")
        assert result is not None, "Required property 'message_description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def message_type(self) -> builtins.str:
        '''Message type as returned from cdk-nag.'''
        result = self._values.get("message_type")
        assert result is not None, "Required property 'message_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Message(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/pdk-nag.NagResult",
    jsii_struct_bases=[],
    name_mapping={"messages": "messages", "resource": "resource"},
)
class NagResult:
    def __init__(
        self,
        *,
        messages: typing.Sequence[typing.Union[Message, typing.Dict[str, typing.Any]]],
        resource: builtins.str,
    ) -> None:
        '''Nag result.

        :param messages: List of messages.
        :param resource: Resource which triggered the message.
        '''
        if __debug__:
            def stub(
                *,
                messages: typing.Sequence[typing.Union[Message, typing.Dict[str, typing.Any]]],
                resource: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument messages", value=messages, expected_type=type_hints["messages"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[str, typing.Any] = {
            "messages": messages,
            "resource": resource,
        }

    @builtins.property
    def messages(self) -> typing.List[Message]:
        '''List of messages.'''
        result = self._values.get("messages")
        assert result is not None, "Required property 'messages' is missing"
        return typing.cast(typing.List[Message], result)

    @builtins.property
    def resource(self) -> builtins.str:
        '''Resource which triggered the message.'''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NagResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PDKNag(metaclass=jsii.JSIIMeta, jsii_type="@aws-prototyping-sdk/pdk-nag.PDKNag"):
    '''Helper for create a Nag Enabled App.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="addResourceSuppressionsByPathNoThrow")
    @builtins.classmethod
    def add_resource_suppressions_by_path_no_throw(
        cls,
        stack: aws_cdk.Stack,
        path: builtins.str,
        suppressions: typing.Sequence[typing.Union[cdk_nag.NagPackSuppression, typing.Dict[str, typing.Any]]],
        apply_to_children: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Wrapper around NagSuppressions which does not throw.

        :param stack: stack instance.
        :param path: resource path.
        :param suppressions: list of suppressions to apply.
        :param apply_to_children: whether to apply to children.
        '''
        if __debug__:
            def stub(
                stack: aws_cdk.Stack,
                path: builtins.str,
                suppressions: typing.Sequence[typing.Union[cdk_nag.NagPackSuppression, typing.Dict[str, typing.Any]]],
                apply_to_children: typing.Optional[builtins.bool] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument suppressions", value=suppressions, expected_type=type_hints["suppressions"])
            check_type(argname="argument apply_to_children", value=apply_to_children, expected_type=type_hints["apply_to_children"])
        return typing.cast(None, jsii.sinvoke(cls, "addResourceSuppressionsByPathNoThrow", [stack, path, suppressions, apply_to_children]))

    @jsii.member(jsii_name="app")
    @builtins.classmethod
    def app(
        cls,
        *,
        fail_on_error: typing.Optional[builtins.bool] = None,
        fail_on_warning: typing.Optional[builtins.bool] = None,
        nag_packs: typing.Optional[typing.Sequence[cdk_nag.NagPack]] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        auto_synth: typing.Optional[builtins.bool] = None,
        context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        outdir: typing.Optional[builtins.str] = None,
        post_cli_context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        stack_traces: typing.Optional[builtins.bool] = None,
        tree_metadata: typing.Optional[builtins.bool] = None,
    ) -> "PDKNagApp":
        '''Returns an instance of an App with Nag enabled.

        :param fail_on_error: Determines whether any errors encountered should trigger a test failure. Default: false
        :param fail_on_warning: Determines whether any warnings encountered should trigger a test failure. Default: false
        :param nag_packs: Custom nag packs to execute. Default: DEFAULT_NAG_PACKS
        :param analytics_reporting: Include runtime versioning information in the Stacks of this app. Default: Value of 'aws:cdk:version-reporting' context key
        :param auto_synth: Automatically call ``synth()`` before the program exits. If you set this, you don't have to call ``synth()`` explicitly. Note that this feature is only available for certain programming languages, and calling ``synth()`` is still recommended. Default: true if running via CDK CLI (``CDK_OUTDIR`` is set), ``false`` otherwise
        :param context: Additional context values for the application. Context set by the CLI or the ``context`` key in ``cdk.json`` has precedence. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param outdir: The output directory into which to emit synthesized artifacts. You should never need to set this value. By default, the value you pass to the CLI's ``--output`` flag will be used, and if you change it to a different directory the CLI will fail to pick up the generated Cloud Assembly. This property is intended for internal and testing use. Default: - If this value is *not* set, considers the environment variable ``CDK_OUTDIR``. If ``CDK_OUTDIR`` is not defined, uses a temp directory.
        :param post_cli_context: Additional context values for the application. Context provided here has precedence over context set by: - The CLI via --context - The ``context`` key in ``cdk.json`` - The {@link AppProps.context} property This property is recommended over the {@link AppProps.context} property since you can make final decision over which context value to take in your app. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param stack_traces: Include construct creation stack trace in the ``aws:cdk:trace`` metadata key of all constructs. Default: true stack traces are included unless ``aws:cdk:disable-stack-trace`` is set in the context.
        :param tree_metadata: Include construct tree metadata as part of the Cloud Assembly. Default: true
        '''
        props = PDKNagAppProps(
            fail_on_error=fail_on_error,
            fail_on_warning=fail_on_warning,
            nag_packs=nag_packs,
            analytics_reporting=analytics_reporting,
            auto_synth=auto_synth,
            context=context,
            outdir=outdir,
            post_cli_context=post_cli_context,
            stack_traces=stack_traces,
            tree_metadata=tree_metadata,
        )

        return typing.cast("PDKNagApp", jsii.sinvoke(cls, "app", [props]))

    @jsii.member(jsii_name="getStackAccountRegex")
    @builtins.classmethod
    def get_stack_account_regex(cls, stack: aws_cdk.Stack) -> builtins.str:
        '''Returns a stack account regex.

        :param stack: stack instance.
        '''
        if __debug__:
            def stub(stack: aws_cdk.Stack) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getStackAccountRegex", [stack]))

    @jsii.member(jsii_name="getStackPartitionRegex")
    @builtins.classmethod
    def get_stack_partition_regex(cls, stack: aws_cdk.Stack) -> builtins.str:
        '''Returns a stack partition regex.

        :param stack: stack instance.
        '''
        if __debug__:
            def stub(stack: aws_cdk.Stack) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getStackPartitionRegex", [stack]))

    @jsii.member(jsii_name="getStackPrefix")
    @builtins.classmethod
    def get_stack_prefix(cls, stack: aws_cdk.Stack) -> builtins.str:
        '''Returns a prefix comprising of a delimited set of Stack Ids.

        For example: StackA/NestedStackB/

        :param stack: stack instance.
        '''
        if __debug__:
            def stub(stack: aws_cdk.Stack) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getStackPrefix", [stack]))

    @jsii.member(jsii_name="getStackRegionRegex")
    @builtins.classmethod
    def get_stack_region_regex(cls, stack: aws_cdk.Stack) -> builtins.str:
        '''Returns a stack region regex.

        :param stack: stack instance.
        '''
        if __debug__:
            def stub(stack: aws_cdk.Stack) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getStackRegionRegex", [stack]))


class PDKNagApp(
    aws_cdk.App,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/pdk-nag.PDKNagApp",
):
    '''
    :inheritDoc: true
    '''

    def __init__(
        self,
        *,
        fail_on_error: typing.Optional[builtins.bool] = None,
        fail_on_warning: typing.Optional[builtins.bool] = None,
        nag_packs: typing.Optional[typing.Sequence[cdk_nag.NagPack]] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        auto_synth: typing.Optional[builtins.bool] = None,
        context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        outdir: typing.Optional[builtins.str] = None,
        post_cli_context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        stack_traces: typing.Optional[builtins.bool] = None,
        tree_metadata: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param fail_on_error: Determines whether any errors encountered should trigger a test failure. Default: false
        :param fail_on_warning: Determines whether any warnings encountered should trigger a test failure. Default: false
        :param nag_packs: Custom nag packs to execute. Default: DEFAULT_NAG_PACKS
        :param analytics_reporting: Include runtime versioning information in the Stacks of this app. Default: Value of 'aws:cdk:version-reporting' context key
        :param auto_synth: Automatically call ``synth()`` before the program exits. If you set this, you don't have to call ``synth()`` explicitly. Note that this feature is only available for certain programming languages, and calling ``synth()`` is still recommended. Default: true if running via CDK CLI (``CDK_OUTDIR`` is set), ``false`` otherwise
        :param context: Additional context values for the application. Context set by the CLI or the ``context`` key in ``cdk.json`` has precedence. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param outdir: The output directory into which to emit synthesized artifacts. You should never need to set this value. By default, the value you pass to the CLI's ``--output`` flag will be used, and if you change it to a different directory the CLI will fail to pick up the generated Cloud Assembly. This property is intended for internal and testing use. Default: - If this value is *not* set, considers the environment variable ``CDK_OUTDIR``. If ``CDK_OUTDIR`` is not defined, uses a temp directory.
        :param post_cli_context: Additional context values for the application. Context provided here has precedence over context set by: - The CLI via --context - The ``context`` key in ``cdk.json`` - The {@link AppProps.context} property This property is recommended over the {@link AppProps.context} property since you can make final decision over which context value to take in your app. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param stack_traces: Include construct creation stack trace in the ``aws:cdk:trace`` metadata key of all constructs. Default: true stack traces are included unless ``aws:cdk:disable-stack-trace`` is set in the context.
        :param tree_metadata: Include construct tree metadata as part of the Cloud Assembly. Default: true
        '''
        props = PDKNagAppProps(
            fail_on_error=fail_on_error,
            fail_on_warning=fail_on_warning,
            nag_packs=nag_packs,
            analytics_reporting=analytics_reporting,
            auto_synth=auto_synth,
            context=context,
            outdir=outdir,
            post_cli_context=post_cli_context,
            stack_traces=stack_traces,
            tree_metadata=tree_metadata,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addNagResult")
    def add_nag_result(
        self,
        *,
        messages: typing.Sequence[typing.Union[Message, typing.Dict[str, typing.Any]]],
        resource: builtins.str,
    ) -> None:
        '''
        :param messages: List of messages.
        :param resource: Resource which triggered the message.
        '''
        result = NagResult(messages=messages, resource=resource)

        return typing.cast(None, jsii.invoke(self, "addNagResult", [result]))

    @jsii.member(jsii_name="nagResults")
    def nag_results(self) -> typing.List[NagResult]:
        '''Returns a list of NagResult.

        Note: app.synth() must be called before this to retrieve results.
        '''
        return typing.cast(typing.List[NagResult], jsii.invoke(self, "nagResults", []))

    @jsii.member(jsii_name="synth")
    def synth(
        self,
        *,
        force: typing.Optional[builtins.bool] = None,
        skip_validation: typing.Optional[builtins.bool] = None,
        validate_on_synthesis: typing.Optional[builtins.bool] = None,
    ) -> aws_cdk.cx_api.CloudAssembly:
        '''Synthesize this stage into a cloud assembly.

        Once an assembly has been synthesized, it cannot be modified. Subsequent
        calls will return the same assembly.

        :param force: Force a re-synth, even if the stage has already been synthesized. This is used by tests to allow for incremental verification of the output. Do not use in production. Default: false
        :param skip_validation: Should we skip construct validation. Default: - false
        :param validate_on_synthesis: Whether the stack should be validated after synthesis to check for error metadata. Default: - false
        '''
        options = aws_cdk.StageSynthesisOptions(
            force=force,
            skip_validation=skip_validation,
            validate_on_synthesis=validate_on_synthesis,
        )

        return typing.cast(aws_cdk.cx_api.CloudAssembly, jsii.invoke(self, "synth", [options]))

    @builtins.property
    @jsii.member(jsii_name="nagPacks")
    def nag_packs(self) -> typing.List[cdk_nag.NagPack]:
        return typing.cast(typing.List[cdk_nag.NagPack], jsii.get(self, "nagPacks"))


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/pdk-nag.PDKNagAppProps",
    jsii_struct_bases=[aws_cdk.AppProps],
    name_mapping={
        "analytics_reporting": "analyticsReporting",
        "auto_synth": "autoSynth",
        "context": "context",
        "outdir": "outdir",
        "post_cli_context": "postCliContext",
        "stack_traces": "stackTraces",
        "tree_metadata": "treeMetadata",
        "fail_on_error": "failOnError",
        "fail_on_warning": "failOnWarning",
        "nag_packs": "nagPacks",
    },
)
class PDKNagAppProps(aws_cdk.AppProps):
    def __init__(
        self,
        *,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        auto_synth: typing.Optional[builtins.bool] = None,
        context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        outdir: typing.Optional[builtins.str] = None,
        post_cli_context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        stack_traces: typing.Optional[builtins.bool] = None,
        tree_metadata: typing.Optional[builtins.bool] = None,
        fail_on_error: typing.Optional[builtins.bool] = None,
        fail_on_warning: typing.Optional[builtins.bool] = None,
        nag_packs: typing.Optional[typing.Sequence[cdk_nag.NagPack]] = None,
    ) -> None:
        '''
        :param analytics_reporting: Include runtime versioning information in the Stacks of this app. Default: Value of 'aws:cdk:version-reporting' context key
        :param auto_synth: Automatically call ``synth()`` before the program exits. If you set this, you don't have to call ``synth()`` explicitly. Note that this feature is only available for certain programming languages, and calling ``synth()`` is still recommended. Default: true if running via CDK CLI (``CDK_OUTDIR`` is set), ``false`` otherwise
        :param context: Additional context values for the application. Context set by the CLI or the ``context`` key in ``cdk.json`` has precedence. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param outdir: The output directory into which to emit synthesized artifacts. You should never need to set this value. By default, the value you pass to the CLI's ``--output`` flag will be used, and if you change it to a different directory the CLI will fail to pick up the generated Cloud Assembly. This property is intended for internal and testing use. Default: - If this value is *not* set, considers the environment variable ``CDK_OUTDIR``. If ``CDK_OUTDIR`` is not defined, uses a temp directory.
        :param post_cli_context: Additional context values for the application. Context provided here has precedence over context set by: - The CLI via --context - The ``context`` key in ``cdk.json`` - The {@link AppProps.context} property This property is recommended over the {@link AppProps.context} property since you can make final decision over which context value to take in your app. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param stack_traces: Include construct creation stack trace in the ``aws:cdk:trace`` metadata key of all constructs. Default: true stack traces are included unless ``aws:cdk:disable-stack-trace`` is set in the context.
        :param tree_metadata: Include construct tree metadata as part of the Cloud Assembly. Default: true
        :param fail_on_error: Determines whether any errors encountered should trigger a test failure. Default: false
        :param fail_on_warning: Determines whether any warnings encountered should trigger a test failure. Default: false
        :param nag_packs: Custom nag packs to execute. Default: DEFAULT_NAG_PACKS

        :inheritDoc: true
        '''
        if __debug__:
            def stub(
                *,
                analytics_reporting: typing.Optional[builtins.bool] = None,
                auto_synth: typing.Optional[builtins.bool] = None,
                context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
                outdir: typing.Optional[builtins.str] = None,
                post_cli_context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
                stack_traces: typing.Optional[builtins.bool] = None,
                tree_metadata: typing.Optional[builtins.bool] = None,
                fail_on_error: typing.Optional[builtins.bool] = None,
                fail_on_warning: typing.Optional[builtins.bool] = None,
                nag_packs: typing.Optional[typing.Sequence[cdk_nag.NagPack]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument analytics_reporting", value=analytics_reporting, expected_type=type_hints["analytics_reporting"])
            check_type(argname="argument auto_synth", value=auto_synth, expected_type=type_hints["auto_synth"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument post_cli_context", value=post_cli_context, expected_type=type_hints["post_cli_context"])
            check_type(argname="argument stack_traces", value=stack_traces, expected_type=type_hints["stack_traces"])
            check_type(argname="argument tree_metadata", value=tree_metadata, expected_type=type_hints["tree_metadata"])
            check_type(argname="argument fail_on_error", value=fail_on_error, expected_type=type_hints["fail_on_error"])
            check_type(argname="argument fail_on_warning", value=fail_on_warning, expected_type=type_hints["fail_on_warning"])
            check_type(argname="argument nag_packs", value=nag_packs, expected_type=type_hints["nag_packs"])
        self._values: typing.Dict[str, typing.Any] = {}
        if analytics_reporting is not None:
            self._values["analytics_reporting"] = analytics_reporting
        if auto_synth is not None:
            self._values["auto_synth"] = auto_synth
        if context is not None:
            self._values["context"] = context
        if outdir is not None:
            self._values["outdir"] = outdir
        if post_cli_context is not None:
            self._values["post_cli_context"] = post_cli_context
        if stack_traces is not None:
            self._values["stack_traces"] = stack_traces
        if tree_metadata is not None:
            self._values["tree_metadata"] = tree_metadata
        if fail_on_error is not None:
            self._values["fail_on_error"] = fail_on_error
        if fail_on_warning is not None:
            self._values["fail_on_warning"] = fail_on_warning
        if nag_packs is not None:
            self._values["nag_packs"] = nag_packs

    @builtins.property
    def analytics_reporting(self) -> typing.Optional[builtins.bool]:
        '''Include runtime versioning information in the Stacks of this app.

        :default: Value of 'aws:cdk:version-reporting' context key
        '''
        result = self._values.get("analytics_reporting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_synth(self) -> typing.Optional[builtins.bool]:
        '''Automatically call ``synth()`` before the program exits.

        If you set this, you don't have to call ``synth()`` explicitly. Note that
        this feature is only available for certain programming languages, and
        calling ``synth()`` is still recommended.

        :default:

        true if running via CDK CLI (``CDK_OUTDIR`` is set), ``false``
        otherwise
        '''
        result = self._values.get("auto_synth")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Additional context values for the application.

        Context set by the CLI or the ``context`` key in ``cdk.json`` has precedence.

        Context can be read from any construct using ``node.getContext(key)``.

        :default: - no additional context
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''The output directory into which to emit synthesized artifacts.

        You should never need to set this value. By default, the value you pass to
        the CLI's ``--output`` flag will be used, and if you change it to a different
        directory the CLI will fail to pick up the generated Cloud Assembly.

        This property is intended for internal and testing use.

        :default:

        - If this value is *not* set, considers the environment variable ``CDK_OUTDIR``.
        If ``CDK_OUTDIR`` is not defined, uses a temp directory.
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_cli_context(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Additional context values for the application.

        Context provided here has precedence over context set by:

        - The CLI via --context
        - The ``context`` key in ``cdk.json``
        - The {@link AppProps.context} property

        This property is recommended over the {@link AppProps.context} property since you
        can make final decision over which context value to take in your app.

        Context can be read from any construct using ``node.getContext(key)``.

        :default: - no additional context

        Example::

            // context from the CLI and from `cdk.json` are stored in the
            // CDK_CONTEXT env variable
            const cliContext = JSON.parse(process.env.CDK_CONTEXT!);
            
            // determine whether to take the context passed in the CLI or not
            const determineValue = process.env.PROD ? cliContext.SOMEKEY : 'my-prod-value';
            new App({
              postCliContext: {
                SOMEKEY: determineValue,
              },
            });
        '''
        result = self._values.get("post_cli_context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def stack_traces(self) -> typing.Optional[builtins.bool]:
        '''Include construct creation stack trace in the ``aws:cdk:trace`` metadata key of all constructs.

        :default: true stack traces are included unless ``aws:cdk:disable-stack-trace`` is set in the context.
        '''
        result = self._values.get("stack_traces")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tree_metadata(self) -> typing.Optional[builtins.bool]:
        '''Include construct tree metadata as part of the Cloud Assembly.

        :default: true
        '''
        result = self._values.get("tree_metadata")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def fail_on_error(self) -> typing.Optional[builtins.bool]:
        '''Determines whether any errors encountered should trigger a test failure.

        :default: false
        '''
        result = self._values.get("fail_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def fail_on_warning(self) -> typing.Optional[builtins.bool]:
        '''Determines whether any warnings encountered should trigger a test failure.

        :default: false
        '''
        result = self._values.get("fail_on_warning")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def nag_packs(self) -> typing.Optional[typing.List[cdk_nag.NagPack]]:
        '''Custom nag packs to execute.

        :default: DEFAULT_NAG_PACKS
        '''
        result = self._values.get("nag_packs")
        return typing.cast(typing.Optional[typing.List[cdk_nag.NagPack]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PDKNagAppProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsPrototypingChecks",
    "Message",
    "NagResult",
    "PDKNag",
    "PDKNagApp",
    "PDKNagAppProps",
]

publication.publish()
