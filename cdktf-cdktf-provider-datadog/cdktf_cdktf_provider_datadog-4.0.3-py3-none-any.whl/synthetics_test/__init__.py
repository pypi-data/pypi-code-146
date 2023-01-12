'''
# `datadog_synthetics_test`

Refer to the Terraform Registory for docs: [`datadog_synthetics_test`](https://www.terraform.io/docs/providers/datadog/r/synthetics_test).
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


class SyntheticsTest(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTest",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test datadog_synthetics_test}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        locations: typing.Sequence[builtins.str],
        name: builtins.str,
        status: builtins.str,
        type: builtins.str,
        api_step: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsTestApiStep", typing.Dict[builtins.str, typing.Any]]]]] = None,
        assertion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsTestAssertion", typing.Dict[builtins.str, typing.Any]]]]] = None,
        browser_step: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsTestBrowserStep", typing.Dict[builtins.str, typing.Any]]]]] = None,
        browser_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsTestBrowserVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        config_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsTestConfigVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        device_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        message: typing.Optional[builtins.str] = None,
        options_list: typing.Optional[typing.Union["SyntheticsTestOptionsList", typing.Dict[builtins.str, typing.Any]]] = None,
        request_basicauth: typing.Optional[typing.Union["SyntheticsTestRequestBasicauth", typing.Dict[builtins.str, typing.Any]]] = None,
        request_client_certificate: typing.Optional[typing.Union["SyntheticsTestRequestClientCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        request_definition: typing.Optional[typing.Union["SyntheticsTestRequestDefinition", typing.Dict[builtins.str, typing.Any]]] = None,
        request_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        request_proxy: typing.Optional[typing.Union["SyntheticsTestRequestProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        request_query: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        set_cookie: typing.Optional[builtins.str] = None,
        subtype: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test datadog_synthetics_test} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param locations: Array of locations used to run the test. Refer to `the Datadog Synthetics location data source <https://registry.terraform.io/providers/DataDog/datadog/latest/docs/data-sources/synthetics_locations>`_ to retrieve the list of locations. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#locations SyntheticsTest#locations}
        :param name: Name of Datadog synthetics test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#name SyntheticsTest#name}
        :param status: Define whether you want to start (``live``) or pause (``paused``) a Synthetic test. Valid values are ``live``, ``paused``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#status SyntheticsTest#status}
        :param type: Synthetics test type. Valid values are ``api``, ``browser``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        :param api_step: api_step block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#api_step SyntheticsTest#api_step}
        :param assertion: assertion block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#assertion SyntheticsTest#assertion}
        :param browser_step: browser_step block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#browser_step SyntheticsTest#browser_step}
        :param browser_variable: browser_variable block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#browser_variable SyntheticsTest#browser_variable}
        :param config_variable: config_variable block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#config_variable SyntheticsTest#config_variable}
        :param device_ids: Required if ``type = "browser"``. Array with the different device IDs used to run the test. Valid values are ``laptop_large``, ``tablet``, ``mobile_small``, ``chrome.laptop_large``, ``chrome.tablet``, ``chrome.mobile_small``, ``firefox.laptop_large``, ``firefox.tablet``, ``firefox.mobile_small``, ``edge.laptop_large``, ``edge.tablet``, ``edge.mobile_small``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#device_ids SyntheticsTest#device_ids}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#id SyntheticsTest#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param message: A message to include with notifications for this synthetics test. Email notifications can be sent to specific users by using the same ``@username`` notation as events. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#message SyntheticsTest#message}
        :param options_list: options_list block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#options_list SyntheticsTest#options_list}
        :param request_basicauth: request_basicauth block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_basicauth SyntheticsTest#request_basicauth}
        :param request_client_certificate: request_client_certificate block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_client_certificate SyntheticsTest#request_client_certificate}
        :param request_definition: request_definition block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_definition SyntheticsTest#request_definition}
        :param request_headers: Header name and value map. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_headers SyntheticsTest#request_headers}
        :param request_proxy: request_proxy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_proxy SyntheticsTest#request_proxy}
        :param request_query: Query arguments name and value map. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_query SyntheticsTest#request_query}
        :param set_cookie: Cookies to be used for a browser test request, using the `Set-Cookie <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie>`_ syntax. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#set_cookie SyntheticsTest#set_cookie}
        :param subtype: The subtype of the Synthetic API test. Defaults to ``http``. Valid values are ``http``, ``ssl``, ``tcp``, ``dns``, ``multi``, ``icmp``, ``udp``, ``websocket``, ``grpc``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#subtype SyntheticsTest#subtype}
        :param tags: A list of tags to associate with your synthetics test. This can help you categorize and filter tests in the manage synthetics page of the UI. Default is an empty list (``[]``). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#tags SyntheticsTest#tags}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b89cc4269f63e8bc3807556eba7178a1b9be7920bf505519de4dc5256f1af23)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SyntheticsTestConfig(
            locations=locations,
            name=name,
            status=status,
            type=type,
            api_step=api_step,
            assertion=assertion,
            browser_step=browser_step,
            browser_variable=browser_variable,
            config_variable=config_variable,
            device_ids=device_ids,
            id=id,
            message=message,
            options_list=options_list,
            request_basicauth=request_basicauth,
            request_client_certificate=request_client_certificate,
            request_definition=request_definition,
            request_headers=request_headers,
            request_proxy=request_proxy,
            request_query=request_query,
            set_cookie=set_cookie,
            subtype=subtype,
            tags=tags,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putApiStep")
    def put_api_step(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsTestApiStep", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__714fa4824f501a9e78f16c1c225a170563d35d7c401c2228564a2614c9e6ee69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putApiStep", [value]))

    @jsii.member(jsii_name="putAssertion")
    def put_assertion(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsTestAssertion", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1152431a587efd5665b5172fa29182f0ead17aa572b7a7c410f965ca3e3770b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAssertion", [value]))

    @jsii.member(jsii_name="putBrowserStep")
    def put_browser_step(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsTestBrowserStep", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0352caac120771a2ae9347ed37d0f13b0ab4ac90e9fed5eedd8afe187cdeb06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBrowserStep", [value]))

    @jsii.member(jsii_name="putBrowserVariable")
    def put_browser_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsTestBrowserVariable", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e00aef3187dd8efbf31c3893fc337f05695c973d91b075ddb7ea129fc2b10b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBrowserVariable", [value]))

    @jsii.member(jsii_name="putConfigVariable")
    def put_config_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsTestConfigVariable", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a343543ea8eca942656fc8b4fcb5c44e430fd889f34586dcdd24c85b446619c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConfigVariable", [value]))

    @jsii.member(jsii_name="putOptionsList")
    def put_options_list(
        self,
        *,
        tick_every: jsii.Number,
        accept_self_signed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        check_certificate_revocation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ci: typing.Optional[typing.Union["SyntheticsTestOptionsListCi", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_cors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_csp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        follow_redirects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ignore_server_certificate_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        initial_navigation_timeout: typing.Optional[jsii.Number] = None,
        min_failure_duration: typing.Optional[jsii.Number] = None,
        min_location_failed: typing.Optional[jsii.Number] = None,
        monitor_name: typing.Optional[builtins.str] = None,
        monitor_options: typing.Optional[typing.Union["SyntheticsTestOptionsListMonitorOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor_priority: typing.Optional[jsii.Number] = None,
        no_screenshot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restricted_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        retry: typing.Optional[typing.Union["SyntheticsTestOptionsListRetry", typing.Dict[builtins.str, typing.Any]]] = None,
        rum_settings: typing.Optional[typing.Union["SyntheticsTestOptionsListRumSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param tick_every: How often the test should run (in seconds). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#tick_every SyntheticsTest#tick_every}
        :param accept_self_signed: For SSL test, whether or not the test should allow self signed certificates. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#accept_self_signed SyntheticsTest#accept_self_signed}
        :param allow_insecure: Allows loading insecure content for an HTTP test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#allow_insecure SyntheticsTest#allow_insecure}
        :param check_certificate_revocation: For SSL test, whether or not the test should fail on revoked certificate in stapled OCSP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#check_certificate_revocation SyntheticsTest#check_certificate_revocation}
        :param ci: ci block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#ci SyntheticsTest#ci}
        :param disable_cors: Disable Cross-Origin Resource Sharing for browser tests. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#disable_cors SyntheticsTest#disable_cors}
        :param disable_csp: Disable Content Security Policy for browser tests. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#disable_csp SyntheticsTest#disable_csp}
        :param follow_redirects: Determines whether or not the API HTTP test should follow redirects. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#follow_redirects SyntheticsTest#follow_redirects}
        :param ignore_server_certificate_error: Ignore server certificate error. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#ignore_server_certificate_error SyntheticsTest#ignore_server_certificate_error}
        :param initial_navigation_timeout: Timeout before declaring the initial step as failed (in seconds) for browser tests. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#initial_navigation_timeout SyntheticsTest#initial_navigation_timeout}
        :param min_failure_duration: Minimum amount of time in failure required to trigger an alert. Default is ``0``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#min_failure_duration SyntheticsTest#min_failure_duration}
        :param min_location_failed: Minimum number of locations in failure required to trigger an alert. Default is ``1``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#min_location_failed SyntheticsTest#min_location_failed}
        :param monitor_name: The monitor name is used for the alert title as well as for all monitor dashboard widgets and SLOs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#monitor_name SyntheticsTest#monitor_name}
        :param monitor_options: monitor_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#monitor_options SyntheticsTest#monitor_options}
        :param monitor_priority: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#monitor_priority SyntheticsTest#monitor_priority}.
        :param no_screenshot: Prevents saving screenshots of the steps. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#no_screenshot SyntheticsTest#no_screenshot}
        :param restricted_roles: A list of role identifiers pulled from the Roles API to restrict read and write access. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#restricted_roles SyntheticsTest#restricted_roles}
        :param retry: retry block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#retry SyntheticsTest#retry}
        :param rum_settings: rum_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#rum_settings SyntheticsTest#rum_settings}
        '''
        value = SyntheticsTestOptionsList(
            tick_every=tick_every,
            accept_self_signed=accept_self_signed,
            allow_insecure=allow_insecure,
            check_certificate_revocation=check_certificate_revocation,
            ci=ci,
            disable_cors=disable_cors,
            disable_csp=disable_csp,
            follow_redirects=follow_redirects,
            ignore_server_certificate_error=ignore_server_certificate_error,
            initial_navigation_timeout=initial_navigation_timeout,
            min_failure_duration=min_failure_duration,
            min_location_failed=min_location_failed,
            monitor_name=monitor_name,
            monitor_options=monitor_options,
            monitor_priority=monitor_priority,
            no_screenshot=no_screenshot,
            restricted_roles=restricted_roles,
            retry=retry,
            rum_settings=rum_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putOptionsList", [value]))

    @jsii.member(jsii_name="putRequestBasicauth")
    def put_request_basicauth(
        self,
        *,
        access_key: typing.Optional[builtins.str] = None,
        access_token_url: typing.Optional[builtins.str] = None,
        audience: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        domain: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        service_name: typing.Optional[builtins.str] = None,
        session_token: typing.Optional[builtins.str] = None,
        token_api_authentication: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
        workstation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_key: Access key for ``SIGV4`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#access_key SyntheticsTest#access_key}
        :param access_token_url: Access token url for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#access_token_url SyntheticsTest#access_token_url}
        :param audience: Audience for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#audience SyntheticsTest#audience}
        :param client_id: Client ID for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#client_id SyntheticsTest#client_id}
        :param client_secret: Client secret for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#client_secret SyntheticsTest#client_secret}
        :param domain: Domain for ``ntlm`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#domain SyntheticsTest#domain}
        :param password: Password for authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#password SyntheticsTest#password}
        :param region: Region for ``SIGV4`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#region SyntheticsTest#region}
        :param resource: Resource for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#resource SyntheticsTest#resource}
        :param scope: Scope for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#scope SyntheticsTest#scope}
        :param secret_key: Secret key for ``SIGV4`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#secret_key SyntheticsTest#secret_key}
        :param service_name: Service name for ``SIGV4`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#service_name SyntheticsTest#service_name}
        :param session_token: Session token for ``SIGV4`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#session_token SyntheticsTest#session_token}
        :param token_api_authentication: Token API Authentication for ``oauth-client`` or ``oauth-rop`` authentication. Valid values are ``header``, ``body``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#token_api_authentication SyntheticsTest#token_api_authentication}
        :param type: Type of basic authentication to use when performing the test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        :param username: Username for authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#username SyntheticsTest#username}
        :param workstation: Workstation for ``ntlm`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#workstation SyntheticsTest#workstation}
        '''
        value = SyntheticsTestRequestBasicauth(
            access_key=access_key,
            access_token_url=access_token_url,
            audience=audience,
            client_id=client_id,
            client_secret=client_secret,
            domain=domain,
            password=password,
            region=region,
            resource=resource,
            scope=scope,
            secret_key=secret_key,
            service_name=service_name,
            session_token=session_token,
            token_api_authentication=token_api_authentication,
            type=type,
            username=username,
            workstation=workstation,
        )

        return typing.cast(None, jsii.invoke(self, "putRequestBasicauth", [value]))

    @jsii.member(jsii_name="putRequestClientCertificate")
    def put_request_client_certificate(
        self,
        *,
        cert: typing.Union["SyntheticsTestRequestClientCertificateCert", typing.Dict[builtins.str, typing.Any]],
        key: typing.Union["SyntheticsTestRequestClientCertificateKey", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param cert: cert block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#cert SyntheticsTest#cert}
        :param key: key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#key SyntheticsTest#key}
        '''
        value = SyntheticsTestRequestClientCertificate(cert=cert, key=key)

        return typing.cast(None, jsii.invoke(self, "putRequestClientCertificate", [value]))

    @jsii.member(jsii_name="putRequestDefinition")
    def put_request_definition(
        self,
        *,
        body: typing.Optional[builtins.str] = None,
        body_type: typing.Optional[builtins.str] = None,
        call_type: typing.Optional[builtins.str] = None,
        certificate_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        dns_server: typing.Optional[builtins.str] = None,
        dns_server_port: typing.Optional[jsii.Number] = None,
        host: typing.Optional[builtins.str] = None,
        message: typing.Optional[builtins.str] = None,
        method: typing.Optional[builtins.str] = None,
        no_saving_response_body: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        number_of_packets: typing.Optional[jsii.Number] = None,
        port: typing.Optional[jsii.Number] = None,
        servername: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
        should_track_hops: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param body: The request body. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#body SyntheticsTest#body}
        :param body_type: Type of the request body. Valid values are ``text/plain``, ``application/json``, ``text/xml``, ``text/html``, ``application/x-www-form-urlencoded``, ``graphql``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#body_type SyntheticsTest#body_type}
        :param call_type: The type of gRPC call to perform. Valid values are ``healthcheck``, ``unary``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#call_type SyntheticsTest#call_type}
        :param certificate_domains: By default, the client certificate is applied on the domain of the starting URL for browser tests. If you want your client certificate to be applied on other domains instead, add them in ``certificate_domains``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#certificate_domains SyntheticsTest#certificate_domains}
        :param dns_server: DNS server to use for DNS tests (``subtype = "dns"``). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#dns_server SyntheticsTest#dns_server}
        :param dns_server_port: DNS server port to use for DNS tests. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#dns_server_port SyntheticsTest#dns_server_port}
        :param host: Host name to perform the test with. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#host SyntheticsTest#host}
        :param message: For UDP and websocket tests, message to send with the request. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#message SyntheticsTest#message}
        :param method: Either the HTTP method/verb to use or a gRPC method available on the service set in the ``service`` field. Required if ``subtype`` is ``HTTP`` or if ``subtype`` is ``grpc`` and ``callType`` is ``unary``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#method SyntheticsTest#method}
        :param no_saving_response_body: Determines whether or not to save the response body. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#no_saving_response_body SyntheticsTest#no_saving_response_body}
        :param number_of_packets: Number of pings to use per test for ICMP tests (``subtype = "icmp"``) between 0 and 10. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#number_of_packets SyntheticsTest#number_of_packets}
        :param port: Port to use when performing the test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#port SyntheticsTest#port}
        :param servername: For SSL tests, it specifies on which server you want to initiate the TLS handshake, allowing the server to present one of multiple possible certificates on the same IP address and TCP port number. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#servername SyntheticsTest#servername}
        :param service: The gRPC service on which you want to perform the gRPC call. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#service SyntheticsTest#service}
        :param should_track_hops: This will turn on a traceroute probe to discover all gateways along the path to the host destination. For ICMP tests (``subtype = "icmp"``). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#should_track_hops SyntheticsTest#should_track_hops}
        :param timeout: Timeout in seconds for the test. Defaults to ``60``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#timeout SyntheticsTest#timeout}
        :param url: The URL to send the request to. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#url SyntheticsTest#url}
        '''
        value = SyntheticsTestRequestDefinition(
            body=body,
            body_type=body_type,
            call_type=call_type,
            certificate_domains=certificate_domains,
            dns_server=dns_server,
            dns_server_port=dns_server_port,
            host=host,
            message=message,
            method=method,
            no_saving_response_body=no_saving_response_body,
            number_of_packets=number_of_packets,
            port=port,
            servername=servername,
            service=service,
            should_track_hops=should_track_hops,
            timeout=timeout,
            url=url,
        )

        return typing.cast(None, jsii.invoke(self, "putRequestDefinition", [value]))

    @jsii.member(jsii_name="putRequestProxy")
    def put_request_proxy(
        self,
        *,
        url: builtins.str,
        headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param url: URL of the proxy to perform the test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#url SyntheticsTest#url}
        :param headers: Header name and value map. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#headers SyntheticsTest#headers}
        '''
        value = SyntheticsTestRequestProxy(url=url, headers=headers)

        return typing.cast(None, jsii.invoke(self, "putRequestProxy", [value]))

    @jsii.member(jsii_name="resetApiStep")
    def reset_api_step(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiStep", []))

    @jsii.member(jsii_name="resetAssertion")
    def reset_assertion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssertion", []))

    @jsii.member(jsii_name="resetBrowserStep")
    def reset_browser_step(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBrowserStep", []))

    @jsii.member(jsii_name="resetBrowserVariable")
    def reset_browser_variable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBrowserVariable", []))

    @jsii.member(jsii_name="resetConfigVariable")
    def reset_config_variable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigVariable", []))

    @jsii.member(jsii_name="resetDeviceIds")
    def reset_device_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceIds", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMessage")
    def reset_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessage", []))

    @jsii.member(jsii_name="resetOptionsList")
    def reset_options_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptionsList", []))

    @jsii.member(jsii_name="resetRequestBasicauth")
    def reset_request_basicauth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestBasicauth", []))

    @jsii.member(jsii_name="resetRequestClientCertificate")
    def reset_request_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestClientCertificate", []))

    @jsii.member(jsii_name="resetRequestDefinition")
    def reset_request_definition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestDefinition", []))

    @jsii.member(jsii_name="resetRequestHeaders")
    def reset_request_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestHeaders", []))

    @jsii.member(jsii_name="resetRequestProxy")
    def reset_request_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestProxy", []))

    @jsii.member(jsii_name="resetRequestQuery")
    def reset_request_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestQuery", []))

    @jsii.member(jsii_name="resetSetCookie")
    def reset_set_cookie(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSetCookie", []))

    @jsii.member(jsii_name="resetSubtype")
    def reset_subtype(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubtype", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="apiStep")
    def api_step(self) -> "SyntheticsTestApiStepList":
        return typing.cast("SyntheticsTestApiStepList", jsii.get(self, "apiStep"))

    @builtins.property
    @jsii.member(jsii_name="assertion")
    def assertion(self) -> "SyntheticsTestAssertionList":
        return typing.cast("SyntheticsTestAssertionList", jsii.get(self, "assertion"))

    @builtins.property
    @jsii.member(jsii_name="browserStep")
    def browser_step(self) -> "SyntheticsTestBrowserStepList":
        return typing.cast("SyntheticsTestBrowserStepList", jsii.get(self, "browserStep"))

    @builtins.property
    @jsii.member(jsii_name="browserVariable")
    def browser_variable(self) -> "SyntheticsTestBrowserVariableList":
        return typing.cast("SyntheticsTestBrowserVariableList", jsii.get(self, "browserVariable"))

    @builtins.property
    @jsii.member(jsii_name="configVariable")
    def config_variable(self) -> "SyntheticsTestConfigVariableList":
        return typing.cast("SyntheticsTestConfigVariableList", jsii.get(self, "configVariable"))

    @builtins.property
    @jsii.member(jsii_name="monitorId")
    def monitor_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "monitorId"))

    @builtins.property
    @jsii.member(jsii_name="optionsList")
    def options_list(self) -> "SyntheticsTestOptionsListOutputReference":
        return typing.cast("SyntheticsTestOptionsListOutputReference", jsii.get(self, "optionsList"))

    @builtins.property
    @jsii.member(jsii_name="requestBasicauth")
    def request_basicauth(self) -> "SyntheticsTestRequestBasicauthOutputReference":
        return typing.cast("SyntheticsTestRequestBasicauthOutputReference", jsii.get(self, "requestBasicauth"))

    @builtins.property
    @jsii.member(jsii_name="requestClientCertificate")
    def request_client_certificate(
        self,
    ) -> "SyntheticsTestRequestClientCertificateOutputReference":
        return typing.cast("SyntheticsTestRequestClientCertificateOutputReference", jsii.get(self, "requestClientCertificate"))

    @builtins.property
    @jsii.member(jsii_name="requestDefinition")
    def request_definition(self) -> "SyntheticsTestRequestDefinitionOutputReference":
        return typing.cast("SyntheticsTestRequestDefinitionOutputReference", jsii.get(self, "requestDefinition"))

    @builtins.property
    @jsii.member(jsii_name="requestProxy")
    def request_proxy(self) -> "SyntheticsTestRequestProxyOutputReference":
        return typing.cast("SyntheticsTestRequestProxyOutputReference", jsii.get(self, "requestProxy"))

    @builtins.property
    @jsii.member(jsii_name="apiStepInput")
    def api_step_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsTestApiStep"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsTestApiStep"]]], jsii.get(self, "apiStepInput"))

    @builtins.property
    @jsii.member(jsii_name="assertionInput")
    def assertion_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsTestAssertion"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsTestAssertion"]]], jsii.get(self, "assertionInput"))

    @builtins.property
    @jsii.member(jsii_name="browserStepInput")
    def browser_step_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsTestBrowserStep"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsTestBrowserStep"]]], jsii.get(self, "browserStepInput"))

    @builtins.property
    @jsii.member(jsii_name="browserVariableInput")
    def browser_variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsTestBrowserVariable"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsTestBrowserVariable"]]], jsii.get(self, "browserVariableInput"))

    @builtins.property
    @jsii.member(jsii_name="configVariableInput")
    def config_variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsTestConfigVariable"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsTestConfigVariable"]]], jsii.get(self, "configVariableInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceIdsInput")
    def device_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "deviceIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationsInput")
    def locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "locationsInput"))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="optionsListInput")
    def options_list_input(self) -> typing.Optional["SyntheticsTestOptionsList"]:
        return typing.cast(typing.Optional["SyntheticsTestOptionsList"], jsii.get(self, "optionsListInput"))

    @builtins.property
    @jsii.member(jsii_name="requestBasicauthInput")
    def request_basicauth_input(
        self,
    ) -> typing.Optional["SyntheticsTestRequestBasicauth"]:
        return typing.cast(typing.Optional["SyntheticsTestRequestBasicauth"], jsii.get(self, "requestBasicauthInput"))

    @builtins.property
    @jsii.member(jsii_name="requestClientCertificateInput")
    def request_client_certificate_input(
        self,
    ) -> typing.Optional["SyntheticsTestRequestClientCertificate"]:
        return typing.cast(typing.Optional["SyntheticsTestRequestClientCertificate"], jsii.get(self, "requestClientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="requestDefinitionInput")
    def request_definition_input(
        self,
    ) -> typing.Optional["SyntheticsTestRequestDefinition"]:
        return typing.cast(typing.Optional["SyntheticsTestRequestDefinition"], jsii.get(self, "requestDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeadersInput")
    def request_headers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "requestHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="requestProxyInput")
    def request_proxy_input(self) -> typing.Optional["SyntheticsTestRequestProxy"]:
        return typing.cast(typing.Optional["SyntheticsTestRequestProxy"], jsii.get(self, "requestProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="requestQueryInput")
    def request_query_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "requestQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="setCookieInput")
    def set_cookie_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "setCookieInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="subtypeInput")
    def subtype_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subtypeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceIds")
    def device_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "deviceIds"))

    @device_ids.setter
    def device_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21e72b0d783535e75b1149bb24b6154e9942a4036100bb34641e696ef94c5515)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceIds", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73225d0602a79ccaf9a581d4e1ad0188a66d4fd21c6ccaf84f01218e8bf8be90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="locations")
    def locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "locations"))

    @locations.setter
    def locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0338904ab0eab2a8e34960cc132109d19549cf3e264f9395b04f57c1a65483d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value)

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @message.setter
    def message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f6359dc1a5c20ea2fcd22fdba30ffdc0b857740eb54291ff038c5b92c28e779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbdf5872c6500ea5002e9a1093c2a11e3a9a5b378b2ae980d010cff34938a002)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="requestHeaders")
    def request_headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "requestHeaders"))

    @request_headers.setter
    def request_headers(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b755f999797f910b20e2585b3cbf00b83516f3925175c2ad1d5d5d5d89c1e392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestHeaders", value)

    @builtins.property
    @jsii.member(jsii_name="requestQuery")
    def request_query(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "requestQuery"))

    @request_query.setter
    def request_query(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35cec634470ee9480807a84a948b9a8afd673eab1cb11e4bada87cf35c4b8f13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestQuery", value)

    @builtins.property
    @jsii.member(jsii_name="setCookie")
    def set_cookie(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "setCookie"))

    @set_cookie.setter
    def set_cookie(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76cda7beaf463e1f3b43cc4d9d031f93bbee4be1f9711e95b7553da07535cece)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "setCookie", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f8fd678b604b907b82b5ce637905f501dc0e919b6b237dcdb293288aa76a04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="subtype")
    def subtype(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subtype"))

    @subtype.setter
    def subtype(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67fd2426599fed35a7500d6208da818fd80978ad848d9e02629e117d4ec18dc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subtype", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f6088555e47ca20d3b571c37e39653d0bca80d7e788a555c9f179000747173e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63cde1b2d68674b5d959a7bd828c3acecd6b72eb5ab53e8a529d8a8ba6d4144a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStep",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allow_failure": "allowFailure",
        "assertion": "assertion",
        "extracted_value": "extractedValue",
        "is_critical": "isCritical",
        "request_basicauth": "requestBasicauth",
        "request_client_certificate": "requestClientCertificate",
        "request_definition": "requestDefinition",
        "request_headers": "requestHeaders",
        "request_proxy": "requestProxy",
        "request_query": "requestQuery",
        "retry": "retry",
        "subtype": "subtype",
    },
)
class SyntheticsTestApiStep:
    def __init__(
        self,
        *,
        name: builtins.str,
        allow_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        assertion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsTestApiStepAssertion", typing.Dict[builtins.str, typing.Any]]]]] = None,
        extracted_value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsTestApiStepExtractedValue", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_critical: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        request_basicauth: typing.Optional[typing.Union["SyntheticsTestApiStepRequestBasicauth", typing.Dict[builtins.str, typing.Any]]] = None,
        request_client_certificate: typing.Optional[typing.Union["SyntheticsTestApiStepRequestClientCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        request_definition: typing.Optional[typing.Union["SyntheticsTestApiStepRequestDefinition", typing.Dict[builtins.str, typing.Any]]] = None,
        request_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        request_proxy: typing.Optional[typing.Union["SyntheticsTestApiStepRequestProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        request_query: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        retry: typing.Optional[typing.Union["SyntheticsTestApiStepRetry", typing.Dict[builtins.str, typing.Any]]] = None,
        subtype: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#name SyntheticsTest#name}
        :param allow_failure: Determines whether or not to continue with test if this step fails. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#allow_failure SyntheticsTest#allow_failure}
        :param assertion: assertion block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#assertion SyntheticsTest#assertion}
        :param extracted_value: extracted_value block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#extracted_value SyntheticsTest#extracted_value}
        :param is_critical: Determines whether or not to consider the entire test as failed if this step fails. Can be used only if ``allow_failure`` is ``true``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#is_critical SyntheticsTest#is_critical}
        :param request_basicauth: request_basicauth block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_basicauth SyntheticsTest#request_basicauth}
        :param request_client_certificate: request_client_certificate block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_client_certificate SyntheticsTest#request_client_certificate}
        :param request_definition: request_definition block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_definition SyntheticsTest#request_definition}
        :param request_headers: Header name and value map. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_headers SyntheticsTest#request_headers}
        :param request_proxy: request_proxy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_proxy SyntheticsTest#request_proxy}
        :param request_query: Query arguments name and value map. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_query SyntheticsTest#request_query}
        :param retry: retry block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#retry SyntheticsTest#retry}
        :param subtype: The subtype of the Synthetic multistep API test step. Valid values are ``http``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#subtype SyntheticsTest#subtype}
        '''
        if isinstance(request_basicauth, dict):
            request_basicauth = SyntheticsTestApiStepRequestBasicauth(**request_basicauth)
        if isinstance(request_client_certificate, dict):
            request_client_certificate = SyntheticsTestApiStepRequestClientCertificate(**request_client_certificate)
        if isinstance(request_definition, dict):
            request_definition = SyntheticsTestApiStepRequestDefinition(**request_definition)
        if isinstance(request_proxy, dict):
            request_proxy = SyntheticsTestApiStepRequestProxy(**request_proxy)
        if isinstance(retry, dict):
            retry = SyntheticsTestApiStepRetry(**retry)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__702cd51f3b0abb5ca3b5b9ca05bc1a1dce4a0837424e2b161aa3799d16972cc7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allow_failure", value=allow_failure, expected_type=type_hints["allow_failure"])
            check_type(argname="argument assertion", value=assertion, expected_type=type_hints["assertion"])
            check_type(argname="argument extracted_value", value=extracted_value, expected_type=type_hints["extracted_value"])
            check_type(argname="argument is_critical", value=is_critical, expected_type=type_hints["is_critical"])
            check_type(argname="argument request_basicauth", value=request_basicauth, expected_type=type_hints["request_basicauth"])
            check_type(argname="argument request_client_certificate", value=request_client_certificate, expected_type=type_hints["request_client_certificate"])
            check_type(argname="argument request_definition", value=request_definition, expected_type=type_hints["request_definition"])
            check_type(argname="argument request_headers", value=request_headers, expected_type=type_hints["request_headers"])
            check_type(argname="argument request_proxy", value=request_proxy, expected_type=type_hints["request_proxy"])
            check_type(argname="argument request_query", value=request_query, expected_type=type_hints["request_query"])
            check_type(argname="argument retry", value=retry, expected_type=type_hints["retry"])
            check_type(argname="argument subtype", value=subtype, expected_type=type_hints["subtype"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allow_failure is not None:
            self._values["allow_failure"] = allow_failure
        if assertion is not None:
            self._values["assertion"] = assertion
        if extracted_value is not None:
            self._values["extracted_value"] = extracted_value
        if is_critical is not None:
            self._values["is_critical"] = is_critical
        if request_basicauth is not None:
            self._values["request_basicauth"] = request_basicauth
        if request_client_certificate is not None:
            self._values["request_client_certificate"] = request_client_certificate
        if request_definition is not None:
            self._values["request_definition"] = request_definition
        if request_headers is not None:
            self._values["request_headers"] = request_headers
        if request_proxy is not None:
            self._values["request_proxy"] = request_proxy
        if request_query is not None:
            self._values["request_query"] = request_query
        if retry is not None:
            self._values["retry"] = retry
        if subtype is not None:
            self._values["subtype"] = subtype

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the step.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#name SyntheticsTest#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_failure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether or not to continue with test if this step fails.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#allow_failure SyntheticsTest#allow_failure}
        '''
        result = self._values.get("allow_failure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def assertion(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsTestApiStepAssertion"]]]:
        '''assertion block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#assertion SyntheticsTest#assertion}
        '''
        result = self._values.get("assertion")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsTestApiStepAssertion"]]], result)

    @builtins.property
    def extracted_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsTestApiStepExtractedValue"]]]:
        '''extracted_value block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#extracted_value SyntheticsTest#extracted_value}
        '''
        result = self._values.get("extracted_value")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsTestApiStepExtractedValue"]]], result)

    @builtins.property
    def is_critical(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether or not to consider the entire test as failed if this step fails.

        Can be used only if ``allow_failure`` is ``true``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#is_critical SyntheticsTest#is_critical}
        '''
        result = self._values.get("is_critical")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def request_basicauth(
        self,
    ) -> typing.Optional["SyntheticsTestApiStepRequestBasicauth"]:
        '''request_basicauth block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_basicauth SyntheticsTest#request_basicauth}
        '''
        result = self._values.get("request_basicauth")
        return typing.cast(typing.Optional["SyntheticsTestApiStepRequestBasicauth"], result)

    @builtins.property
    def request_client_certificate(
        self,
    ) -> typing.Optional["SyntheticsTestApiStepRequestClientCertificate"]:
        '''request_client_certificate block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_client_certificate SyntheticsTest#request_client_certificate}
        '''
        result = self._values.get("request_client_certificate")
        return typing.cast(typing.Optional["SyntheticsTestApiStepRequestClientCertificate"], result)

    @builtins.property
    def request_definition(
        self,
    ) -> typing.Optional["SyntheticsTestApiStepRequestDefinition"]:
        '''request_definition block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_definition SyntheticsTest#request_definition}
        '''
        result = self._values.get("request_definition")
        return typing.cast(typing.Optional["SyntheticsTestApiStepRequestDefinition"], result)

    @builtins.property
    def request_headers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Header name and value map.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_headers SyntheticsTest#request_headers}
        '''
        result = self._values.get("request_headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def request_proxy(self) -> typing.Optional["SyntheticsTestApiStepRequestProxy"]:
        '''request_proxy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_proxy SyntheticsTest#request_proxy}
        '''
        result = self._values.get("request_proxy")
        return typing.cast(typing.Optional["SyntheticsTestApiStepRequestProxy"], result)

    @builtins.property
    def request_query(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Query arguments name and value map.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_query SyntheticsTest#request_query}
        '''
        result = self._values.get("request_query")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def retry(self) -> typing.Optional["SyntheticsTestApiStepRetry"]:
        '''retry block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#retry SyntheticsTest#retry}
        '''
        result = self._values.get("retry")
        return typing.cast(typing.Optional["SyntheticsTestApiStepRetry"], result)

    @builtins.property
    def subtype(self) -> typing.Optional[builtins.str]:
        '''The subtype of the Synthetic multistep API test step. Valid values are ``http``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#subtype SyntheticsTest#subtype}
        '''
        result = self._values.get("subtype")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestApiStep(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepAssertion",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "type": "type",
        "property": "property",
        "target": "target",
        "targetjsonpath": "targetjsonpath",
        "targetxpath": "targetxpath",
    },
)
class SyntheticsTestApiStepAssertion:
    def __init__(
        self,
        *,
        operator: builtins.str,
        type: builtins.str,
        property: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        targetjsonpath: typing.Optional[typing.Union["SyntheticsTestApiStepAssertionTargetjsonpath", typing.Dict[builtins.str, typing.Any]]] = None,
        targetxpath: typing.Optional[typing.Union["SyntheticsTestApiStepAssertionTargetxpath", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param operator: Assertion operator. **Note** Only some combinations of ``type`` and ``operator`` are valid (please refer to `Datadog documentation <https://docs.datadoghq.com/api/latest/synthetics/#create-a-test>`_). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#operator SyntheticsTest#operator}
        :param type: Type of assertion. **Note** Only some combinations of ``type`` and ``operator`` are valid (please refer to `Datadog documentation <https://docs.datadoghq.com/api/latest/synthetics/#create-a-test>`_). Valid values are ``body``, ``header``, ``statusCode``, ``certificate``, ``responseTime``, ``property``, ``recordEvery``, ``recordSome``, ``tlsVersion``, ``minTlsVersion``, ``latency``, ``packetLossPercentage``, ``packetsReceived``, ``networkHop``, ``receivedMessage``, ``grpcHealthcheckStatus``, ``connection``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        :param property: If assertion type is ``header``, this is the header name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#property SyntheticsTest#property}
        :param target: Expected value. Depends on the assertion type, refer to `Datadog documentation <https://docs.datadoghq.com/api/latest/synthetics/#create-a-test>`_ for details. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#target SyntheticsTest#target}
        :param targetjsonpath: targetjsonpath block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#targetjsonpath SyntheticsTest#targetjsonpath}
        :param targetxpath: targetxpath block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#targetxpath SyntheticsTest#targetxpath}
        '''
        if isinstance(targetjsonpath, dict):
            targetjsonpath = SyntheticsTestApiStepAssertionTargetjsonpath(**targetjsonpath)
        if isinstance(targetxpath, dict):
            targetxpath = SyntheticsTestApiStepAssertionTargetxpath(**targetxpath)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c4da265a3569b7eb4f2ae85853e757e4297a4fa3c5d515ee9324c83ea3d9b8a)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument property", value=property, expected_type=type_hints["property"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument targetjsonpath", value=targetjsonpath, expected_type=type_hints["targetjsonpath"])
            check_type(argname="argument targetxpath", value=targetxpath, expected_type=type_hints["targetxpath"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "type": type,
        }
        if property is not None:
            self._values["property"] = property
        if target is not None:
            self._values["target"] = target
        if targetjsonpath is not None:
            self._values["targetjsonpath"] = targetjsonpath
        if targetxpath is not None:
            self._values["targetxpath"] = targetxpath

    @builtins.property
    def operator(self) -> builtins.str:
        '''Assertion operator. **Note** Only some combinations of ``type`` and ``operator`` are valid (please refer to `Datadog documentation <https://docs.datadoghq.com/api/latest/synthetics/#create-a-test>`_).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#operator SyntheticsTest#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of assertion.

        **Note** Only some combinations of ``type`` and ``operator`` are valid (please refer to `Datadog documentation <https://docs.datadoghq.com/api/latest/synthetics/#create-a-test>`_). Valid values are ``body``, ``header``, ``statusCode``, ``certificate``, ``responseTime``, ``property``, ``recordEvery``, ``recordSome``, ``tlsVersion``, ``minTlsVersion``, ``latency``, ``packetLossPercentage``, ``packetsReceived``, ``networkHop``, ``receivedMessage``, ``grpcHealthcheckStatus``, ``connection``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def property(self) -> typing.Optional[builtins.str]:
        '''If assertion type is ``header``, this is the header name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#property SyntheticsTest#property}
        '''
        result = self._values.get("property")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Expected value. Depends on the assertion type, refer to `Datadog documentation <https://docs.datadoghq.com/api/latest/synthetics/#create-a-test>`_ for details.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#target SyntheticsTest#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def targetjsonpath(
        self,
    ) -> typing.Optional["SyntheticsTestApiStepAssertionTargetjsonpath"]:
        '''targetjsonpath block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#targetjsonpath SyntheticsTest#targetjsonpath}
        '''
        result = self._values.get("targetjsonpath")
        return typing.cast(typing.Optional["SyntheticsTestApiStepAssertionTargetjsonpath"], result)

    @builtins.property
    def targetxpath(
        self,
    ) -> typing.Optional["SyntheticsTestApiStepAssertionTargetxpath"]:
        '''targetxpath block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#targetxpath SyntheticsTest#targetxpath}
        '''
        result = self._values.get("targetxpath")
        return typing.cast(typing.Optional["SyntheticsTestApiStepAssertionTargetxpath"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestApiStepAssertion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestApiStepAssertionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepAssertionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f67d7bff63235752cffdcac578cd1327d2f8e2db90b1ddc9f596e884bcc032b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SyntheticsTestApiStepAssertionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d71161a87f6de471c2862d15d82a159ac7e2eaba7c1f0c2f0f51081942a1f4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SyntheticsTestApiStepAssertionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdb90de66cfa2997e19b6cd7900f21d724b60e8d93a1c45478ba10046c90c55e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f0eac7ad47fc90c6c6792f54a2e2514478f696786025591381febd1fd64086c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f7a4a8f25f93d4aedec9c438d57a894a38a6af30fff397d8abc1e8e2911ba58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestApiStepAssertion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestApiStepAssertion]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestApiStepAssertion]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c876298ab44b3aad8bdc85080bc97f9d6bce30caef165d11e97e553122af0cbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SyntheticsTestApiStepAssertionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepAssertionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9edf1952456d7b35f5c2347ca13b1eed33dbec4c605901f5e4036c42ea4379e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTargetjsonpath")
    def put_targetjsonpath(
        self,
        *,
        jsonpath: builtins.str,
        operator: builtins.str,
        targetvalue: builtins.str,
    ) -> None:
        '''
        :param jsonpath: The JSON path to assert. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#jsonpath SyntheticsTest#jsonpath}
        :param operator: The specific operator to use on the path. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#operator SyntheticsTest#operator}
        :param targetvalue: Expected matching value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#targetvalue SyntheticsTest#targetvalue}
        '''
        value = SyntheticsTestApiStepAssertionTargetjsonpath(
            jsonpath=jsonpath, operator=operator, targetvalue=targetvalue
        )

        return typing.cast(None, jsii.invoke(self, "putTargetjsonpath", [value]))

    @jsii.member(jsii_name="putTargetxpath")
    def put_targetxpath(
        self,
        *,
        operator: builtins.str,
        targetvalue: builtins.str,
        xpath: builtins.str,
    ) -> None:
        '''
        :param operator: The specific operator to use on the path. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#operator SyntheticsTest#operator}
        :param targetvalue: Expected matching value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#targetvalue SyntheticsTest#targetvalue}
        :param xpath: The xpath to assert. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#xpath SyntheticsTest#xpath}
        '''
        value = SyntheticsTestApiStepAssertionTargetxpath(
            operator=operator, targetvalue=targetvalue, xpath=xpath
        )

        return typing.cast(None, jsii.invoke(self, "putTargetxpath", [value]))

    @jsii.member(jsii_name="resetProperty")
    def reset_property(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperty", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @jsii.member(jsii_name="resetTargetjsonpath")
    def reset_targetjsonpath(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetjsonpath", []))

    @jsii.member(jsii_name="resetTargetxpath")
    def reset_targetxpath(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetxpath", []))

    @builtins.property
    @jsii.member(jsii_name="targetjsonpath")
    def targetjsonpath(
        self,
    ) -> "SyntheticsTestApiStepAssertionTargetjsonpathOutputReference":
        return typing.cast("SyntheticsTestApiStepAssertionTargetjsonpathOutputReference", jsii.get(self, "targetjsonpath"))

    @builtins.property
    @jsii.member(jsii_name="targetxpath")
    def targetxpath(self) -> "SyntheticsTestApiStepAssertionTargetxpathOutputReference":
        return typing.cast("SyntheticsTestApiStepAssertionTargetxpathOutputReference", jsii.get(self, "targetxpath"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="propertyInput")
    def property_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "propertyInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="targetjsonpathInput")
    def targetjsonpath_input(
        self,
    ) -> typing.Optional["SyntheticsTestApiStepAssertionTargetjsonpath"]:
        return typing.cast(typing.Optional["SyntheticsTestApiStepAssertionTargetjsonpath"], jsii.get(self, "targetjsonpathInput"))

    @builtins.property
    @jsii.member(jsii_name="targetxpathInput")
    def targetxpath_input(
        self,
    ) -> typing.Optional["SyntheticsTestApiStepAssertionTargetxpath"]:
        return typing.cast(typing.Optional["SyntheticsTestApiStepAssertionTargetxpath"], jsii.get(self, "targetxpathInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90155739d5bd8896765bd13d02f97a23235658d3d841067ff16d11bf44075517)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="property")
    def property(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "property"))

    @property.setter
    def property(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18508b51e88b4640fc0ea9ae6a762f4342f0ad871f770852731062a4635992ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "property", value)

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__029efc83d81f4a929bd7b0946ff361e6d9602ea3de79194a146c4773c68d17a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67598d651c309557ff68d2e0a48ed66178030c25421b5141bb51e701c53433db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SyntheticsTestApiStepAssertion, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SyntheticsTestApiStepAssertion, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SyntheticsTestApiStepAssertion, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54055a44dc870c84915c6aded654f8e1a87718bcf653d0df2a15d759a1db1f6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepAssertionTargetjsonpath",
    jsii_struct_bases=[],
    name_mapping={
        "jsonpath": "jsonpath",
        "operator": "operator",
        "targetvalue": "targetvalue",
    },
)
class SyntheticsTestApiStepAssertionTargetjsonpath:
    def __init__(
        self,
        *,
        jsonpath: builtins.str,
        operator: builtins.str,
        targetvalue: builtins.str,
    ) -> None:
        '''
        :param jsonpath: The JSON path to assert. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#jsonpath SyntheticsTest#jsonpath}
        :param operator: The specific operator to use on the path. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#operator SyntheticsTest#operator}
        :param targetvalue: Expected matching value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#targetvalue SyntheticsTest#targetvalue}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b97ecd6f8f6690d295820867eb452b459246ac3638f37f79ab32a2811771e79)
            check_type(argname="argument jsonpath", value=jsonpath, expected_type=type_hints["jsonpath"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument targetvalue", value=targetvalue, expected_type=type_hints["targetvalue"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "jsonpath": jsonpath,
            "operator": operator,
            "targetvalue": targetvalue,
        }

    @builtins.property
    def jsonpath(self) -> builtins.str:
        '''The JSON path to assert.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#jsonpath SyntheticsTest#jsonpath}
        '''
        result = self._values.get("jsonpath")
        assert result is not None, "Required property 'jsonpath' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''The specific operator to use on the path.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#operator SyntheticsTest#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def targetvalue(self) -> builtins.str:
        '''Expected matching value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#targetvalue SyntheticsTest#targetvalue}
        '''
        result = self._values.get("targetvalue")
        assert result is not None, "Required property 'targetvalue' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestApiStepAssertionTargetjsonpath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestApiStepAssertionTargetjsonpathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepAssertionTargetjsonpathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24ef2e5240fc9e1add08f0e07c51f5df53e2cb2930137f16deb2257e9d229e08)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="jsonpathInput")
    def jsonpath_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jsonpathInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="targetvalueInput")
    def targetvalue_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetvalueInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonpath")
    def jsonpath(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jsonpath"))

    @jsonpath.setter
    def jsonpath(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc16e3306babb65470c459d18c415f928a36912440fd159c4f3ab160ab15c4a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonpath", value)

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43067fcd7e6108c1ecb616cf9fc3b0cd414a6098fdd1b5bf3f9e8818ee85ab1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="targetvalue")
    def targetvalue(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetvalue"))

    @targetvalue.setter
    def targetvalue(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0f49b83a01b630f7adadf98e2526383afbba2e7bb06c40bb2d216af354bf5ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetvalue", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SyntheticsTestApiStepAssertionTargetjsonpath]:
        return typing.cast(typing.Optional[SyntheticsTestApiStepAssertionTargetjsonpath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestApiStepAssertionTargetjsonpath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b401857bfe53fe39fc157a274358dc41cd2a8355880a77864de8a293dfeabc39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepAssertionTargetxpath",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "targetvalue": "targetvalue",
        "xpath": "xpath",
    },
)
class SyntheticsTestApiStepAssertionTargetxpath:
    def __init__(
        self,
        *,
        operator: builtins.str,
        targetvalue: builtins.str,
        xpath: builtins.str,
    ) -> None:
        '''
        :param operator: The specific operator to use on the path. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#operator SyntheticsTest#operator}
        :param targetvalue: Expected matching value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#targetvalue SyntheticsTest#targetvalue}
        :param xpath: The xpath to assert. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#xpath SyntheticsTest#xpath}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5f9cf4825faa95d883e253dac4201a721a1f912ba9f5d3b75d1d6153ef3f757)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument targetvalue", value=targetvalue, expected_type=type_hints["targetvalue"])
            check_type(argname="argument xpath", value=xpath, expected_type=type_hints["xpath"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "targetvalue": targetvalue,
            "xpath": xpath,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''The specific operator to use on the path.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#operator SyntheticsTest#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def targetvalue(self) -> builtins.str:
        '''Expected matching value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#targetvalue SyntheticsTest#targetvalue}
        '''
        result = self._values.get("targetvalue")
        assert result is not None, "Required property 'targetvalue' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def xpath(self) -> builtins.str:
        '''The xpath to assert.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#xpath SyntheticsTest#xpath}
        '''
        result = self._values.get("xpath")
        assert result is not None, "Required property 'xpath' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestApiStepAssertionTargetxpath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestApiStepAssertionTargetxpathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepAssertionTargetxpathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55aac1744fd5c3d4a8260aa51d2ecb50956e904f5d6120212e11fb525d6a051d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="targetvalueInput")
    def targetvalue_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetvalueInput"))

    @builtins.property
    @jsii.member(jsii_name="xpathInput")
    def xpath_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "xpathInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7af8428973a32b1e60fc488b7a0aa1838dde591130c84fe3cfc1fa7aa3d9c60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="targetvalue")
    def targetvalue(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetvalue"))

    @targetvalue.setter
    def targetvalue(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2ddebcb8a9187a05eee2734e1cff3da01bb67ab9643760bf32b71ab6679b272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetvalue", value)

    @builtins.property
    @jsii.member(jsii_name="xpath")
    def xpath(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "xpath"))

    @xpath.setter
    def xpath(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3df27bcb17cf012f04c887245eb9234363820a63888776be3579e1029dd14ba1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xpath", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SyntheticsTestApiStepAssertionTargetxpath]:
        return typing.cast(typing.Optional[SyntheticsTestApiStepAssertionTargetxpath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestApiStepAssertionTargetxpath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0a8bc7123353d7a4073bb748cc8aae0ba61fb77e391c09c785310a25586701e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepExtractedValue",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "parser": "parser",
        "type": "type",
        "field": "field",
    },
)
class SyntheticsTestApiStepExtractedValue:
    def __init__(
        self,
        *,
        name: builtins.str,
        parser: typing.Union["SyntheticsTestApiStepExtractedValueParser", typing.Dict[builtins.str, typing.Any]],
        type: builtins.str,
        field: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#name SyntheticsTest#name}.
        :param parser: parser block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#parser SyntheticsTest#parser}
        :param type: Property of the Synthetics Test Response to use for the variable. Valid values are ``http_body``, ``http_header``, ``local_variable``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        :param field: When type is ``http_header``, name of the header to use to extract the value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#field SyntheticsTest#field}
        '''
        if isinstance(parser, dict):
            parser = SyntheticsTestApiStepExtractedValueParser(**parser)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a861411ecd750d17513caf86cafaac5e6c6ff18df8e360dbe9e4a4f07ac5cc)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parser", value=parser, expected_type=type_hints["parser"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "parser": parser,
            "type": type,
        }
        if field is not None:
            self._values["field"] = field

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#name SyntheticsTest#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parser(self) -> "SyntheticsTestApiStepExtractedValueParser":
        '''parser block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#parser SyntheticsTest#parser}
        '''
        result = self._values.get("parser")
        assert result is not None, "Required property 'parser' is missing"
        return typing.cast("SyntheticsTestApiStepExtractedValueParser", result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Property of the Synthetics Test Response to use for the variable. Valid values are ``http_body``, ``http_header``, ``local_variable``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def field(self) -> typing.Optional[builtins.str]:
        '''When type is ``http_header``, name of the header to use to extract the value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#field SyntheticsTest#field}
        '''
        result = self._values.get("field")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestApiStepExtractedValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestApiStepExtractedValueList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepExtractedValueList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebe0d4b5954b81da6bfb0f47f41d09e2dad934e08ec6886ebc47a7770f2a3293)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SyntheticsTestApiStepExtractedValueOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bf1256ae876cf718db28df529c1d43fe87cab5a37bd582e6db2547b9b6495cc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SyntheticsTestApiStepExtractedValueOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6860e1ad8087f2695a690dcd90a44ed0392ce8727025575877c09887ad7554c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f62f79054767ef3cf88280507bb5807e16aeb0e92797a8ba53b7dba2f51e3958)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a3fa65287efb68dfccc162f3ab9be69d6a5c693232d76fa195fec5336cbf7f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestApiStepExtractedValue]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestApiStepExtractedValue]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestApiStepExtractedValue]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__598828a5f785842aeaa8e171408f3ab205002826fa4ca58a10ee5eb7c7039b6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SyntheticsTestApiStepExtractedValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepExtractedValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00106af481ec294c9351693e4d291e3cfa1acc23d5b7487a8bdddc6264d9ef04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putParser")
    def put_parser(
        self,
        *,
        type: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of parser for a Synthetics global variable from a synthetics test. Valid values are ``raw``, ``json_path``, ``regex``, ``x_path``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        :param value: Regex or JSON path used for the parser. Not used with type ``raw``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#value SyntheticsTest#value}
        '''
        value_ = SyntheticsTestApiStepExtractedValueParser(type=type, value=value)

        return typing.cast(None, jsii.invoke(self, "putParser", [value_]))

    @jsii.member(jsii_name="resetField")
    def reset_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetField", []))

    @builtins.property
    @jsii.member(jsii_name="parser")
    def parser(self) -> "SyntheticsTestApiStepExtractedValueParserOutputReference":
        return typing.cast("SyntheticsTestApiStepExtractedValueParserOutputReference", jsii.get(self, "parser"))

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parserInput")
    def parser_input(
        self,
    ) -> typing.Optional["SyntheticsTestApiStepExtractedValueParser"]:
        return typing.cast(typing.Optional["SyntheticsTestApiStepExtractedValueParser"], jsii.get(self, "parserInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "field"))

    @field.setter
    def field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e163300bd7bb43fb8a13e19a4c18e6bfc1942869199ef685d59619470677b777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "field", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49ac043db3e2504cbb304a071bbb5228307c3c09f48d9436cd6df083b57f880c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cd5c8335f32e622f1d62e1e9122396e6a47d9994c71d1c23de6e749743949eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SyntheticsTestApiStepExtractedValue, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SyntheticsTestApiStepExtractedValue, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SyntheticsTestApiStepExtractedValue, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a52671124a8438ba5580ea457e533b60a42f19da95e19ffd68d16c72e6eb186c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepExtractedValueParser",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class SyntheticsTestApiStepExtractedValueParser:
    def __init__(
        self,
        *,
        type: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of parser for a Synthetics global variable from a synthetics test. Valid values are ``raw``, ``json_path``, ``regex``, ``x_path``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        :param value: Regex or JSON path used for the parser. Not used with type ``raw``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#value SyntheticsTest#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72132190b1edd060e0da4e8a08bf4c498251b2734b641c00cd49348a5d1d235a)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of parser for a Synthetics global variable from a synthetics test. Valid values are ``raw``, ``json_path``, ``regex``, ``x_path``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Regex or JSON path used for the parser. Not used with type ``raw``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#value SyntheticsTest#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestApiStepExtractedValueParser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestApiStepExtractedValueParserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepExtractedValueParserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__804e9a54d4d9bc07bad059ddf0d4c36e13c4584cda175e7284962493056b86b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32e6d16c0ba023aaac6db353dcf759d3482075e37735476c8379b93982c2d527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0991b589c5f02e4807df7a9bb1494a9fd629275649a1d3692e50144a27a01033)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SyntheticsTestApiStepExtractedValueParser]:
        return typing.cast(typing.Optional[SyntheticsTestApiStepExtractedValueParser], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestApiStepExtractedValueParser],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07a25ac298488c675496bb0be38f7acebabadad024f32e014480064d88001ea3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SyntheticsTestApiStepList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35d64ac6ad416d2e2ad61b4a51f2050691d86fcdc1c18babbf55712c4149114c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SyntheticsTestApiStepOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c767edecb7215d9665b57be4b0abc1be29dfb3e2fa047f42c794fa5c3a6e4184)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SyntheticsTestApiStepOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27d31df5610beaa7616e3b55df4625ac6d93e19f1607af7ed6e0b40ec1f00179)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1507d17b25261ba5f3b86d0f8d5f270e01b9b062a7b277c5efff48c6c373c38)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6090f7f82a6987754551cb0e0fe4ae33be18a0c087e3a73e7185f27e944aaf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestApiStep]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestApiStep]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestApiStep]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad7b00c95c0c5d8fcb629847447a45c6358af36f6022bdc595d73f3020f27739)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SyntheticsTestApiStepOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f36b77a5c2d878aa56c43b5e02778ff1bb2377b24cd5e1c044fd8b2f3754faa4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAssertion")
    def put_assertion(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestApiStepAssertion, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc201daa3698f39c8d07469ef5cc3b67772cd4cc2eee73871da7771d019cf551)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAssertion", [value]))

    @jsii.member(jsii_name="putExtractedValue")
    def put_extracted_value(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestApiStepExtractedValue, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1655bf2763ac96dd22a8f9a73b8e5f26673ece692effb9f335dcc0aa4364ac85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExtractedValue", [value]))

    @jsii.member(jsii_name="putRequestBasicauth")
    def put_request_basicauth(
        self,
        *,
        access_key: typing.Optional[builtins.str] = None,
        access_token_url: typing.Optional[builtins.str] = None,
        audience: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        domain: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        service_name: typing.Optional[builtins.str] = None,
        session_token: typing.Optional[builtins.str] = None,
        token_api_authentication: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
        workstation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_key: Access key for ``SIGV4`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#access_key SyntheticsTest#access_key}
        :param access_token_url: Access token url for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#access_token_url SyntheticsTest#access_token_url}
        :param audience: Audience for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#audience SyntheticsTest#audience}
        :param client_id: Client ID for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#client_id SyntheticsTest#client_id}
        :param client_secret: Client secret for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#client_secret SyntheticsTest#client_secret}
        :param domain: Domain for ``ntlm`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#domain SyntheticsTest#domain}
        :param password: Password for authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#password SyntheticsTest#password}
        :param region: Region for ``SIGV4`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#region SyntheticsTest#region}
        :param resource: Resource for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#resource SyntheticsTest#resource}
        :param scope: Scope for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#scope SyntheticsTest#scope}
        :param secret_key: Secret key for ``SIGV4`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#secret_key SyntheticsTest#secret_key}
        :param service_name: Service name for ``SIGV4`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#service_name SyntheticsTest#service_name}
        :param session_token: Session token for ``SIGV4`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#session_token SyntheticsTest#session_token}
        :param token_api_authentication: Token API Authentication for ``oauth-client`` or ``oauth-rop`` authentication. Valid values are ``header``, ``body``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#token_api_authentication SyntheticsTest#token_api_authentication}
        :param type: Type of basic authentication to use when performing the test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        :param username: Username for authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#username SyntheticsTest#username}
        :param workstation: Workstation for ``ntlm`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#workstation SyntheticsTest#workstation}
        '''
        value = SyntheticsTestApiStepRequestBasicauth(
            access_key=access_key,
            access_token_url=access_token_url,
            audience=audience,
            client_id=client_id,
            client_secret=client_secret,
            domain=domain,
            password=password,
            region=region,
            resource=resource,
            scope=scope,
            secret_key=secret_key,
            service_name=service_name,
            session_token=session_token,
            token_api_authentication=token_api_authentication,
            type=type,
            username=username,
            workstation=workstation,
        )

        return typing.cast(None, jsii.invoke(self, "putRequestBasicauth", [value]))

    @jsii.member(jsii_name="putRequestClientCertificate")
    def put_request_client_certificate(
        self,
        *,
        cert: typing.Union["SyntheticsTestApiStepRequestClientCertificateCert", typing.Dict[builtins.str, typing.Any]],
        key: typing.Union["SyntheticsTestApiStepRequestClientCertificateKey", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param cert: cert block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#cert SyntheticsTest#cert}
        :param key: key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#key SyntheticsTest#key}
        '''
        value = SyntheticsTestApiStepRequestClientCertificate(cert=cert, key=key)

        return typing.cast(None, jsii.invoke(self, "putRequestClientCertificate", [value]))

    @jsii.member(jsii_name="putRequestDefinition")
    def put_request_definition(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        body: typing.Optional[builtins.str] = None,
        body_type: typing.Optional[builtins.str] = None,
        call_type: typing.Optional[builtins.str] = None,
        certificate_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        dns_server: typing.Optional[builtins.str] = None,
        dns_server_port: typing.Optional[jsii.Number] = None,
        follow_redirects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host: typing.Optional[builtins.str] = None,
        message: typing.Optional[builtins.str] = None,
        method: typing.Optional[builtins.str] = None,
        no_saving_response_body: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        number_of_packets: typing.Optional[jsii.Number] = None,
        port: typing.Optional[jsii.Number] = None,
        servername: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
        should_track_hops: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_insecure: Allows loading insecure content for an HTTP test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#allow_insecure SyntheticsTest#allow_insecure}
        :param body: The request body. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#body SyntheticsTest#body}
        :param body_type: Type of the request body. Valid values are ``text/plain``, ``application/json``, ``text/xml``, ``text/html``, ``application/x-www-form-urlencoded``, ``graphql``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#body_type SyntheticsTest#body_type}
        :param call_type: The type of gRPC call to perform. Valid values are ``healthcheck``, ``unary``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#call_type SyntheticsTest#call_type}
        :param certificate_domains: By default, the client certificate is applied on the domain of the starting URL for browser tests. If you want your client certificate to be applied on other domains instead, add them in ``certificate_domains``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#certificate_domains SyntheticsTest#certificate_domains}
        :param dns_server: DNS server to use for DNS tests (``subtype = "dns"``). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#dns_server SyntheticsTest#dns_server}
        :param dns_server_port: DNS server port to use for DNS tests. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#dns_server_port SyntheticsTest#dns_server_port}
        :param follow_redirects: Determines whether or not the API HTTP test should follow redirects. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#follow_redirects SyntheticsTest#follow_redirects}
        :param host: Host name to perform the test with. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#host SyntheticsTest#host}
        :param message: For UDP and websocket tests, message to send with the request. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#message SyntheticsTest#message}
        :param method: Either the HTTP method/verb to use or a gRPC method available on the service set in the ``service`` field. Required if ``subtype`` is ``HTTP`` or if ``subtype`` is ``grpc`` and ``callType`` is ``unary``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#method SyntheticsTest#method}
        :param no_saving_response_body: Determines whether or not to save the response body. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#no_saving_response_body SyntheticsTest#no_saving_response_body}
        :param number_of_packets: Number of pings to use per test for ICMP tests (``subtype = "icmp"``) between 0 and 10. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#number_of_packets SyntheticsTest#number_of_packets}
        :param port: Port to use when performing the test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#port SyntheticsTest#port}
        :param servername: For SSL tests, it specifies on which server you want to initiate the TLS handshake, allowing the server to present one of multiple possible certificates on the same IP address and TCP port number. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#servername SyntheticsTest#servername}
        :param service: The gRPC service on which you want to perform the gRPC call. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#service SyntheticsTest#service}
        :param should_track_hops: This will turn on a traceroute probe to discover all gateways along the path to the host destination. For ICMP tests (``subtype = "icmp"``). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#should_track_hops SyntheticsTest#should_track_hops}
        :param timeout: Timeout in seconds for the test. Defaults to ``60``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#timeout SyntheticsTest#timeout}
        :param url: The URL to send the request to. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#url SyntheticsTest#url}
        '''
        value = SyntheticsTestApiStepRequestDefinition(
            allow_insecure=allow_insecure,
            body=body,
            body_type=body_type,
            call_type=call_type,
            certificate_domains=certificate_domains,
            dns_server=dns_server,
            dns_server_port=dns_server_port,
            follow_redirects=follow_redirects,
            host=host,
            message=message,
            method=method,
            no_saving_response_body=no_saving_response_body,
            number_of_packets=number_of_packets,
            port=port,
            servername=servername,
            service=service,
            should_track_hops=should_track_hops,
            timeout=timeout,
            url=url,
        )

        return typing.cast(None, jsii.invoke(self, "putRequestDefinition", [value]))

    @jsii.member(jsii_name="putRequestProxy")
    def put_request_proxy(
        self,
        *,
        url: builtins.str,
        headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param url: URL of the proxy to perform the test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#url SyntheticsTest#url}
        :param headers: Header name and value map. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#headers SyntheticsTest#headers}
        '''
        value = SyntheticsTestApiStepRequestProxy(url=url, headers=headers)

        return typing.cast(None, jsii.invoke(self, "putRequestProxy", [value]))

    @jsii.member(jsii_name="putRetry")
    def put_retry(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: Number of retries needed to consider a location as failed before sending a notification alert. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#count SyntheticsTest#count}
        :param interval: Interval between a failed test and the next retry in milliseconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#interval SyntheticsTest#interval}
        '''
        value = SyntheticsTestApiStepRetry(count=count, interval=interval)

        return typing.cast(None, jsii.invoke(self, "putRetry", [value]))

    @jsii.member(jsii_name="resetAllowFailure")
    def reset_allow_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowFailure", []))

    @jsii.member(jsii_name="resetAssertion")
    def reset_assertion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssertion", []))

    @jsii.member(jsii_name="resetExtractedValue")
    def reset_extracted_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtractedValue", []))

    @jsii.member(jsii_name="resetIsCritical")
    def reset_is_critical(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsCritical", []))

    @jsii.member(jsii_name="resetRequestBasicauth")
    def reset_request_basicauth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestBasicauth", []))

    @jsii.member(jsii_name="resetRequestClientCertificate")
    def reset_request_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestClientCertificate", []))

    @jsii.member(jsii_name="resetRequestDefinition")
    def reset_request_definition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestDefinition", []))

    @jsii.member(jsii_name="resetRequestHeaders")
    def reset_request_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestHeaders", []))

    @jsii.member(jsii_name="resetRequestProxy")
    def reset_request_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestProxy", []))

    @jsii.member(jsii_name="resetRequestQuery")
    def reset_request_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestQuery", []))

    @jsii.member(jsii_name="resetRetry")
    def reset_retry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetry", []))

    @jsii.member(jsii_name="resetSubtype")
    def reset_subtype(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubtype", []))

    @builtins.property
    @jsii.member(jsii_name="assertion")
    def assertion(self) -> SyntheticsTestApiStepAssertionList:
        return typing.cast(SyntheticsTestApiStepAssertionList, jsii.get(self, "assertion"))

    @builtins.property
    @jsii.member(jsii_name="extractedValue")
    def extracted_value(self) -> SyntheticsTestApiStepExtractedValueList:
        return typing.cast(SyntheticsTestApiStepExtractedValueList, jsii.get(self, "extractedValue"))

    @builtins.property
    @jsii.member(jsii_name="requestBasicauth")
    def request_basicauth(
        self,
    ) -> "SyntheticsTestApiStepRequestBasicauthOutputReference":
        return typing.cast("SyntheticsTestApiStepRequestBasicauthOutputReference", jsii.get(self, "requestBasicauth"))

    @builtins.property
    @jsii.member(jsii_name="requestClientCertificate")
    def request_client_certificate(
        self,
    ) -> "SyntheticsTestApiStepRequestClientCertificateOutputReference":
        return typing.cast("SyntheticsTestApiStepRequestClientCertificateOutputReference", jsii.get(self, "requestClientCertificate"))

    @builtins.property
    @jsii.member(jsii_name="requestDefinition")
    def request_definition(
        self,
    ) -> "SyntheticsTestApiStepRequestDefinitionOutputReference":
        return typing.cast("SyntheticsTestApiStepRequestDefinitionOutputReference", jsii.get(self, "requestDefinition"))

    @builtins.property
    @jsii.member(jsii_name="requestProxy")
    def request_proxy(self) -> "SyntheticsTestApiStepRequestProxyOutputReference":
        return typing.cast("SyntheticsTestApiStepRequestProxyOutputReference", jsii.get(self, "requestProxy"))

    @builtins.property
    @jsii.member(jsii_name="retry")
    def retry(self) -> "SyntheticsTestApiStepRetryOutputReference":
        return typing.cast("SyntheticsTestApiStepRetryOutputReference", jsii.get(self, "retry"))

    @builtins.property
    @jsii.member(jsii_name="allowFailureInput")
    def allow_failure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="assertionInput")
    def assertion_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestApiStepAssertion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestApiStepAssertion]]], jsii.get(self, "assertionInput"))

    @builtins.property
    @jsii.member(jsii_name="extractedValueInput")
    def extracted_value_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestApiStepExtractedValue]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestApiStepExtractedValue]]], jsii.get(self, "extractedValueInput"))

    @builtins.property
    @jsii.member(jsii_name="isCriticalInput")
    def is_critical_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isCriticalInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="requestBasicauthInput")
    def request_basicauth_input(
        self,
    ) -> typing.Optional["SyntheticsTestApiStepRequestBasicauth"]:
        return typing.cast(typing.Optional["SyntheticsTestApiStepRequestBasicauth"], jsii.get(self, "requestBasicauthInput"))

    @builtins.property
    @jsii.member(jsii_name="requestClientCertificateInput")
    def request_client_certificate_input(
        self,
    ) -> typing.Optional["SyntheticsTestApiStepRequestClientCertificate"]:
        return typing.cast(typing.Optional["SyntheticsTestApiStepRequestClientCertificate"], jsii.get(self, "requestClientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="requestDefinitionInput")
    def request_definition_input(
        self,
    ) -> typing.Optional["SyntheticsTestApiStepRequestDefinition"]:
        return typing.cast(typing.Optional["SyntheticsTestApiStepRequestDefinition"], jsii.get(self, "requestDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeadersInput")
    def request_headers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "requestHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="requestProxyInput")
    def request_proxy_input(
        self,
    ) -> typing.Optional["SyntheticsTestApiStepRequestProxy"]:
        return typing.cast(typing.Optional["SyntheticsTestApiStepRequestProxy"], jsii.get(self, "requestProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="requestQueryInput")
    def request_query_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "requestQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="retryInput")
    def retry_input(self) -> typing.Optional["SyntheticsTestApiStepRetry"]:
        return typing.cast(typing.Optional["SyntheticsTestApiStepRetry"], jsii.get(self, "retryInput"))

    @builtins.property
    @jsii.member(jsii_name="subtypeInput")
    def subtype_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subtypeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowFailure")
    def allow_failure(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowFailure"))

    @allow_failure.setter
    def allow_failure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6694002e88b69d9e0e9a399877be5ca36218ecd8eccb0c5ee6333240a1431822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowFailure", value)

    @builtins.property
    @jsii.member(jsii_name="isCritical")
    def is_critical(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isCritical"))

    @is_critical.setter
    def is_critical(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adc60c33ab07a92ac1b29abb45863d8521903146956eedcfa5a8f52ee971397e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isCritical", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3bcd6982a727599f28f81e1a4f650a831bbb480a54d3464fcbf5f9b73f81120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="requestHeaders")
    def request_headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "requestHeaders"))

    @request_headers.setter
    def request_headers(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bacb1678c117d1d02cd315490fc1db9174bd8343390047bbb203d1bdafad83c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestHeaders", value)

    @builtins.property
    @jsii.member(jsii_name="requestQuery")
    def request_query(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "requestQuery"))

    @request_query.setter
    def request_query(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99afc3b1d9c8c3dc0125ec7abd8cbde6b2421c525743381042894cca1390dd23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestQuery", value)

    @builtins.property
    @jsii.member(jsii_name="subtype")
    def subtype(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subtype"))

    @subtype.setter
    def subtype(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__730d9d018da6f17b9fbfacff64dcb9ba7dfd84e3045f57ade596f9ad411f3653)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subtype", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SyntheticsTestApiStep, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SyntheticsTestApiStep, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SyntheticsTestApiStep, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607b745268b8eaf0fc19e4a4642c6f2f435d81677dc100c56aad8c2f2becba62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepRequestBasicauth",
    jsii_struct_bases=[],
    name_mapping={
        "access_key": "accessKey",
        "access_token_url": "accessTokenUrl",
        "audience": "audience",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "domain": "domain",
        "password": "password",
        "region": "region",
        "resource": "resource",
        "scope": "scope",
        "secret_key": "secretKey",
        "service_name": "serviceName",
        "session_token": "sessionToken",
        "token_api_authentication": "tokenApiAuthentication",
        "type": "type",
        "username": "username",
        "workstation": "workstation",
    },
)
class SyntheticsTestApiStepRequestBasicauth:
    def __init__(
        self,
        *,
        access_key: typing.Optional[builtins.str] = None,
        access_token_url: typing.Optional[builtins.str] = None,
        audience: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        domain: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        service_name: typing.Optional[builtins.str] = None,
        session_token: typing.Optional[builtins.str] = None,
        token_api_authentication: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
        workstation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_key: Access key for ``SIGV4`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#access_key SyntheticsTest#access_key}
        :param access_token_url: Access token url for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#access_token_url SyntheticsTest#access_token_url}
        :param audience: Audience for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#audience SyntheticsTest#audience}
        :param client_id: Client ID for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#client_id SyntheticsTest#client_id}
        :param client_secret: Client secret for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#client_secret SyntheticsTest#client_secret}
        :param domain: Domain for ``ntlm`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#domain SyntheticsTest#domain}
        :param password: Password for authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#password SyntheticsTest#password}
        :param region: Region for ``SIGV4`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#region SyntheticsTest#region}
        :param resource: Resource for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#resource SyntheticsTest#resource}
        :param scope: Scope for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#scope SyntheticsTest#scope}
        :param secret_key: Secret key for ``SIGV4`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#secret_key SyntheticsTest#secret_key}
        :param service_name: Service name for ``SIGV4`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#service_name SyntheticsTest#service_name}
        :param session_token: Session token for ``SIGV4`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#session_token SyntheticsTest#session_token}
        :param token_api_authentication: Token API Authentication for ``oauth-client`` or ``oauth-rop`` authentication. Valid values are ``header``, ``body``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#token_api_authentication SyntheticsTest#token_api_authentication}
        :param type: Type of basic authentication to use when performing the test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        :param username: Username for authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#username SyntheticsTest#username}
        :param workstation: Workstation for ``ntlm`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#workstation SyntheticsTest#workstation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9bb439d9854a2545b5777d4f0fb088cccf632bb73dc99896dd5e3db37d2abcd)
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument access_token_url", value=access_token_url, expected_type=type_hints["access_token_url"])
            check_type(argname="argument audience", value=audience, expected_type=type_hints["audience"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument session_token", value=session_token, expected_type=type_hints["session_token"])
            check_type(argname="argument token_api_authentication", value=token_api_authentication, expected_type=type_hints["token_api_authentication"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument workstation", value=workstation, expected_type=type_hints["workstation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_key is not None:
            self._values["access_key"] = access_key
        if access_token_url is not None:
            self._values["access_token_url"] = access_token_url
        if audience is not None:
            self._values["audience"] = audience
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if domain is not None:
            self._values["domain"] = domain
        if password is not None:
            self._values["password"] = password
        if region is not None:
            self._values["region"] = region
        if resource is not None:
            self._values["resource"] = resource
        if scope is not None:
            self._values["scope"] = scope
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if service_name is not None:
            self._values["service_name"] = service_name
        if session_token is not None:
            self._values["session_token"] = session_token
        if token_api_authentication is not None:
            self._values["token_api_authentication"] = token_api_authentication
        if type is not None:
            self._values["type"] = type
        if username is not None:
            self._values["username"] = username
        if workstation is not None:
            self._values["workstation"] = workstation

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''Access key for ``SIGV4`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#access_key SyntheticsTest#access_key}
        '''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_token_url(self) -> typing.Optional[builtins.str]:
        '''Access token url for ``oauth-client`` or ``oauth-rop`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#access_token_url SyntheticsTest#access_token_url}
        '''
        result = self._values.get("access_token_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def audience(self) -> typing.Optional[builtins.str]:
        '''Audience for ``oauth-client`` or ``oauth-rop`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#audience SyntheticsTest#audience}
        '''
        result = self._values.get("audience")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Client ID for ``oauth-client`` or ``oauth-rop`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#client_id SyntheticsTest#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''Client secret for ``oauth-client`` or ``oauth-rop`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#client_secret SyntheticsTest#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''Domain for ``ntlm`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#domain SyntheticsTest#domain}
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#password SyntheticsTest#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region for ``SIGV4`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#region SyntheticsTest#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''Resource for ``oauth-client`` or ``oauth-rop`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#resource SyntheticsTest#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''Scope for ``oauth-client`` or ``oauth-rop`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#scope SyntheticsTest#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''Secret key for ``SIGV4`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#secret_key SyntheticsTest#secret_key}
        '''
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''Service name for ``SIGV4`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#service_name SyntheticsTest#service_name}
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_token(self) -> typing.Optional[builtins.str]:
        '''Session token for ``SIGV4`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#session_token SyntheticsTest#session_token}
        '''
        result = self._values.get("session_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_api_authentication(self) -> typing.Optional[builtins.str]:
        '''Token API Authentication for ``oauth-client`` or ``oauth-rop`` authentication. Valid values are ``header``, ``body``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#token_api_authentication SyntheticsTest#token_api_authentication}
        '''
        result = self._values.get("token_api_authentication")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of basic authentication to use when performing the test.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username for authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#username SyntheticsTest#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workstation(self) -> typing.Optional[builtins.str]:
        '''Workstation for ``ntlm`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#workstation SyntheticsTest#workstation}
        '''
        result = self._values.get("workstation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestApiStepRequestBasicauth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestApiStepRequestBasicauthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepRequestBasicauthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9710464744c8854210acc91bbd14e89c69565e7f53ce1c1dc8db72fe29b5619b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccessKey")
    def reset_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessKey", []))

    @jsii.member(jsii_name="resetAccessTokenUrl")
    def reset_access_token_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessTokenUrl", []))

    @jsii.member(jsii_name="resetAudience")
    def reset_audience(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudience", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetDomain")
    def reset_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomain", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetResource")
    def reset_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResource", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @jsii.member(jsii_name="resetSecretKey")
    def reset_secret_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretKey", []))

    @jsii.member(jsii_name="resetServiceName")
    def reset_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceName", []))

    @jsii.member(jsii_name="resetSessionToken")
    def reset_session_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionToken", []))

    @jsii.member(jsii_name="resetTokenApiAuthentication")
    def reset_token_api_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenApiAuthentication", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @jsii.member(jsii_name="resetWorkstation")
    def reset_workstation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkstation", []))

    @builtins.property
    @jsii.member(jsii_name="accessKeyInput")
    def access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenUrlInput")
    def access_token_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="audienceInput")
    def audience_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audienceInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="secretKeyInput")
    def secret_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionTokenInput")
    def session_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenApiAuthenticationInput")
    def token_api_authentication_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenApiAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="workstationInput")
    def workstation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workstationInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKey")
    def access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKey"))

    @access_key.setter
    def access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e329d3fa0a4fd3e223a71136e5bec2f6fc39dd847a6569cc8a66a93d2501c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKey", value)

    @builtins.property
    @jsii.member(jsii_name="accessTokenUrl")
    def access_token_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessTokenUrl"))

    @access_token_url.setter
    def access_token_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db812987a7566f7a5d753b25e563f978c578a29750b67e4cd40711e94635cd1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessTokenUrl", value)

    @builtins.property
    @jsii.member(jsii_name="audience")
    def audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audience"))

    @audience.setter
    def audience(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e91c7bd0256ca000b6eb912a0f7825da85ba01020a5348ae2a5005143e7382b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audience", value)

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43c47170a5b6ae66a7771985e11767f4f61378aef5aca5a10a9894bfd1d3b256)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__289c33601c5eb28d72848f611f7d2fc525600d6c864f523b459ea3d165d08879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value)

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4fd0a10b8b8ee2030b624be7f7e9ef54622251ee6fe6946a4f2d75bec74d51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb64c956c7a73b4b80a761fb268e7e8db6e3921aed0c5d4d7fc4194eb3da0ec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce8952b4293c7caec3c02a322cbd85d0a6e0de759d8d156c7aeb28c7680eb5f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__200f5c6f7c7e713f902d3b54d4f32f7c3528c1f02e323745cc2c90d0e86f8a0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7dfd26c66c7cc6a258b38f7fa19d28ec91911be209569350ffbd9de8220f6d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value)

    @builtins.property
    @jsii.member(jsii_name="secretKey")
    def secret_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretKey"))

    @secret_key.setter
    def secret_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cf4aabdc24c37b0bea32b43b1563a1593763fee35f5e8dcad87dc1b13988577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretKey", value)

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__426378d764ba8631d8111075e48febfe540fa6b83906a7dfc68325544dde586f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value)

    @builtins.property
    @jsii.member(jsii_name="sessionToken")
    def session_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionToken"))

    @session_token.setter
    def session_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f928ea328da6cb2ac9356ed9f949fe013a7702e43196838dc6200fc71fd9c8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionToken", value)

    @builtins.property
    @jsii.member(jsii_name="tokenApiAuthentication")
    def token_api_authentication(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenApiAuthentication"))

    @token_api_authentication.setter
    def token_api_authentication(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c069fa43426f4af88fa2b54181af95a71e38275fe336e9512322933b25e82433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenApiAuthentication", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2b980e0d8646eb56a837fc19e8ae0951cdd7e5c613732f3476b6342cd1ddc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92fa823a27d867643a8b23a6efa79da5b217220b434c225a13e7599f6e6dbf2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="workstation")
    def workstation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workstation"))

    @workstation.setter
    def workstation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb508d4c85a103bb919c6732f5002b32a16a79556d522977b84e4e8c5c955cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workstation", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SyntheticsTestApiStepRequestBasicauth]:
        return typing.cast(typing.Optional[SyntheticsTestApiStepRequestBasicauth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestApiStepRequestBasicauth],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac67fb47d799b7ae9255a8fd41aaa2827110e36ffe7d56ae060a1945b5f82b78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepRequestClientCertificate",
    jsii_struct_bases=[],
    name_mapping={"cert": "cert", "key": "key"},
)
class SyntheticsTestApiStepRequestClientCertificate:
    def __init__(
        self,
        *,
        cert: typing.Union["SyntheticsTestApiStepRequestClientCertificateCert", typing.Dict[builtins.str, typing.Any]],
        key: typing.Union["SyntheticsTestApiStepRequestClientCertificateKey", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param cert: cert block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#cert SyntheticsTest#cert}
        :param key: key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#key SyntheticsTest#key}
        '''
        if isinstance(cert, dict):
            cert = SyntheticsTestApiStepRequestClientCertificateCert(**cert)
        if isinstance(key, dict):
            key = SyntheticsTestApiStepRequestClientCertificateKey(**key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b15fa8958c75e99e0888bcb1487279d33d603ec0a35be46ba617eb1667f37e32)
            check_type(argname="argument cert", value=cert, expected_type=type_hints["cert"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cert": cert,
            "key": key,
        }

    @builtins.property
    def cert(self) -> "SyntheticsTestApiStepRequestClientCertificateCert":
        '''cert block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#cert SyntheticsTest#cert}
        '''
        result = self._values.get("cert")
        assert result is not None, "Required property 'cert' is missing"
        return typing.cast("SyntheticsTestApiStepRequestClientCertificateCert", result)

    @builtins.property
    def key(self) -> "SyntheticsTestApiStepRequestClientCertificateKey":
        '''key block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#key SyntheticsTest#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast("SyntheticsTestApiStepRequestClientCertificateKey", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestApiStepRequestClientCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepRequestClientCertificateCert",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "filename": "filename"},
)
class SyntheticsTestApiStepRequestClientCertificateCert:
    def __init__(
        self,
        *,
        content: builtins.str,
        filename: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: Content of the certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#content SyntheticsTest#content}
        :param filename: File name for the certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#filename SyntheticsTest#filename}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4fddecf4d78c19ae0771bb4c5b3e6cb3894f08b8be59845ffc55016392bec19)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
        }
        if filename is not None:
            self._values["filename"] = filename

    @builtins.property
    def content(self) -> builtins.str:
        '''Content of the certificate.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#content SyntheticsTest#content}
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filename(self) -> typing.Optional[builtins.str]:
        '''File name for the certificate.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#filename SyntheticsTest#filename}
        '''
        result = self._values.get("filename")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestApiStepRequestClientCertificateCert(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestApiStepRequestClientCertificateCertOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepRequestClientCertificateCertOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f82258702c4f361fec13a67e59812db0f73d95778fcc9e6e18ca609a40ea7c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFilename")
    def reset_filename(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilename", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="filenameInput")
    def filename_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filenameInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__191aecae0efe5775594fd342351e019a7e0e2cd45e69986dd24f7d2371a27481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="filename")
    def filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filename"))

    @filename.setter
    def filename(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__320830d163d8989beaa91e2a3784d32b5546ad7e84e431ec2f05ede23080951c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filename", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SyntheticsTestApiStepRequestClientCertificateCert]:
        return typing.cast(typing.Optional[SyntheticsTestApiStepRequestClientCertificateCert], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestApiStepRequestClientCertificateCert],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b51c23e7a608828803c08efc3f48f41c79aaf5d161c18bb63a6263a1e7e9e57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepRequestClientCertificateKey",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "filename": "filename"},
)
class SyntheticsTestApiStepRequestClientCertificateKey:
    def __init__(
        self,
        *,
        content: builtins.str,
        filename: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: Content of the certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#content SyntheticsTest#content}
        :param filename: File name for the certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#filename SyntheticsTest#filename}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56d7577c3911479f67bd42bb852e440b956110cdfe556b12fb49e784db7fc663)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
        }
        if filename is not None:
            self._values["filename"] = filename

    @builtins.property
    def content(self) -> builtins.str:
        '''Content of the certificate.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#content SyntheticsTest#content}
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filename(self) -> typing.Optional[builtins.str]:
        '''File name for the certificate.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#filename SyntheticsTest#filename}
        '''
        result = self._values.get("filename")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestApiStepRequestClientCertificateKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestApiStepRequestClientCertificateKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepRequestClientCertificateKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2e2da7f73ef862c49bcc920015c875ab44dd74701c297ed73698ded61e24250)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFilename")
    def reset_filename(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilename", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="filenameInput")
    def filename_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filenameInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf2aac3168990b52dc1a67bc01fdf0a059707da6583eb2130c16769597114ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="filename")
    def filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filename"))

    @filename.setter
    def filename(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b720bcc93675964ee9438e164c9040a75268de90d24e514497e56f14775d4bab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filename", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SyntheticsTestApiStepRequestClientCertificateKey]:
        return typing.cast(typing.Optional[SyntheticsTestApiStepRequestClientCertificateKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestApiStepRequestClientCertificateKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd9fd72adb6f8cbbe9302f08b941f6a512cd9cef4930bafb639be76fb65a8274)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SyntheticsTestApiStepRequestClientCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepRequestClientCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aedfc5aae0f8ffa556f7f401283fbac70816fc00e4fc33e43a6fdbd62b4cf74e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCert")
    def put_cert(
        self,
        *,
        content: builtins.str,
        filename: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: Content of the certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#content SyntheticsTest#content}
        :param filename: File name for the certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#filename SyntheticsTest#filename}
        '''
        value = SyntheticsTestApiStepRequestClientCertificateCert(
            content=content, filename=filename
        )

        return typing.cast(None, jsii.invoke(self, "putCert", [value]))

    @jsii.member(jsii_name="putKey")
    def put_key(
        self,
        *,
        content: builtins.str,
        filename: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: Content of the certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#content SyntheticsTest#content}
        :param filename: File name for the certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#filename SyntheticsTest#filename}
        '''
        value = SyntheticsTestApiStepRequestClientCertificateKey(
            content=content, filename=filename
        )

        return typing.cast(None, jsii.invoke(self, "putKey", [value]))

    @builtins.property
    @jsii.member(jsii_name="cert")
    def cert(self) -> SyntheticsTestApiStepRequestClientCertificateCertOutputReference:
        return typing.cast(SyntheticsTestApiStepRequestClientCertificateCertOutputReference, jsii.get(self, "cert"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> SyntheticsTestApiStepRequestClientCertificateKeyOutputReference:
        return typing.cast(SyntheticsTestApiStepRequestClientCertificateKeyOutputReference, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="certInput")
    def cert_input(
        self,
    ) -> typing.Optional[SyntheticsTestApiStepRequestClientCertificateCert]:
        return typing.cast(typing.Optional[SyntheticsTestApiStepRequestClientCertificateCert], jsii.get(self, "certInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(
        self,
    ) -> typing.Optional[SyntheticsTestApiStepRequestClientCertificateKey]:
        return typing.cast(typing.Optional[SyntheticsTestApiStepRequestClientCertificateKey], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SyntheticsTestApiStepRequestClientCertificate]:
        return typing.cast(typing.Optional[SyntheticsTestApiStepRequestClientCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestApiStepRequestClientCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c45446ccab7ee888eac47f296d66334b3748a2938331c258b02c900896175da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepRequestDefinition",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "body": "body",
        "body_type": "bodyType",
        "call_type": "callType",
        "certificate_domains": "certificateDomains",
        "dns_server": "dnsServer",
        "dns_server_port": "dnsServerPort",
        "follow_redirects": "followRedirects",
        "host": "host",
        "message": "message",
        "method": "method",
        "no_saving_response_body": "noSavingResponseBody",
        "number_of_packets": "numberOfPackets",
        "port": "port",
        "servername": "servername",
        "service": "service",
        "should_track_hops": "shouldTrackHops",
        "timeout": "timeout",
        "url": "url",
    },
)
class SyntheticsTestApiStepRequestDefinition:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        body: typing.Optional[builtins.str] = None,
        body_type: typing.Optional[builtins.str] = None,
        call_type: typing.Optional[builtins.str] = None,
        certificate_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        dns_server: typing.Optional[builtins.str] = None,
        dns_server_port: typing.Optional[jsii.Number] = None,
        follow_redirects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host: typing.Optional[builtins.str] = None,
        message: typing.Optional[builtins.str] = None,
        method: typing.Optional[builtins.str] = None,
        no_saving_response_body: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        number_of_packets: typing.Optional[jsii.Number] = None,
        port: typing.Optional[jsii.Number] = None,
        servername: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
        should_track_hops: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_insecure: Allows loading insecure content for an HTTP test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#allow_insecure SyntheticsTest#allow_insecure}
        :param body: The request body. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#body SyntheticsTest#body}
        :param body_type: Type of the request body. Valid values are ``text/plain``, ``application/json``, ``text/xml``, ``text/html``, ``application/x-www-form-urlencoded``, ``graphql``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#body_type SyntheticsTest#body_type}
        :param call_type: The type of gRPC call to perform. Valid values are ``healthcheck``, ``unary``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#call_type SyntheticsTest#call_type}
        :param certificate_domains: By default, the client certificate is applied on the domain of the starting URL for browser tests. If you want your client certificate to be applied on other domains instead, add them in ``certificate_domains``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#certificate_domains SyntheticsTest#certificate_domains}
        :param dns_server: DNS server to use for DNS tests (``subtype = "dns"``). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#dns_server SyntheticsTest#dns_server}
        :param dns_server_port: DNS server port to use for DNS tests. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#dns_server_port SyntheticsTest#dns_server_port}
        :param follow_redirects: Determines whether or not the API HTTP test should follow redirects. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#follow_redirects SyntheticsTest#follow_redirects}
        :param host: Host name to perform the test with. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#host SyntheticsTest#host}
        :param message: For UDP and websocket tests, message to send with the request. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#message SyntheticsTest#message}
        :param method: Either the HTTP method/verb to use or a gRPC method available on the service set in the ``service`` field. Required if ``subtype`` is ``HTTP`` or if ``subtype`` is ``grpc`` and ``callType`` is ``unary``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#method SyntheticsTest#method}
        :param no_saving_response_body: Determines whether or not to save the response body. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#no_saving_response_body SyntheticsTest#no_saving_response_body}
        :param number_of_packets: Number of pings to use per test for ICMP tests (``subtype = "icmp"``) between 0 and 10. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#number_of_packets SyntheticsTest#number_of_packets}
        :param port: Port to use when performing the test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#port SyntheticsTest#port}
        :param servername: For SSL tests, it specifies on which server you want to initiate the TLS handshake, allowing the server to present one of multiple possible certificates on the same IP address and TCP port number. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#servername SyntheticsTest#servername}
        :param service: The gRPC service on which you want to perform the gRPC call. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#service SyntheticsTest#service}
        :param should_track_hops: This will turn on a traceroute probe to discover all gateways along the path to the host destination. For ICMP tests (``subtype = "icmp"``). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#should_track_hops SyntheticsTest#should_track_hops}
        :param timeout: Timeout in seconds for the test. Defaults to ``60``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#timeout SyntheticsTest#timeout}
        :param url: The URL to send the request to. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#url SyntheticsTest#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b7ecad871d76c1341fe87074869bbb285be183268adba97a18604dd499f279)
            check_type(argname="argument allow_insecure", value=allow_insecure, expected_type=type_hints["allow_insecure"])
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            check_type(argname="argument body_type", value=body_type, expected_type=type_hints["body_type"])
            check_type(argname="argument call_type", value=call_type, expected_type=type_hints["call_type"])
            check_type(argname="argument certificate_domains", value=certificate_domains, expected_type=type_hints["certificate_domains"])
            check_type(argname="argument dns_server", value=dns_server, expected_type=type_hints["dns_server"])
            check_type(argname="argument dns_server_port", value=dns_server_port, expected_type=type_hints["dns_server_port"])
            check_type(argname="argument follow_redirects", value=follow_redirects, expected_type=type_hints["follow_redirects"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument no_saving_response_body", value=no_saving_response_body, expected_type=type_hints["no_saving_response_body"])
            check_type(argname="argument number_of_packets", value=number_of_packets, expected_type=type_hints["number_of_packets"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument servername", value=servername, expected_type=type_hints["servername"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument should_track_hops", value=should_track_hops, expected_type=type_hints["should_track_hops"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_insecure is not None:
            self._values["allow_insecure"] = allow_insecure
        if body is not None:
            self._values["body"] = body
        if body_type is not None:
            self._values["body_type"] = body_type
        if call_type is not None:
            self._values["call_type"] = call_type
        if certificate_domains is not None:
            self._values["certificate_domains"] = certificate_domains
        if dns_server is not None:
            self._values["dns_server"] = dns_server
        if dns_server_port is not None:
            self._values["dns_server_port"] = dns_server_port
        if follow_redirects is not None:
            self._values["follow_redirects"] = follow_redirects
        if host is not None:
            self._values["host"] = host
        if message is not None:
            self._values["message"] = message
        if method is not None:
            self._values["method"] = method
        if no_saving_response_body is not None:
            self._values["no_saving_response_body"] = no_saving_response_body
        if number_of_packets is not None:
            self._values["number_of_packets"] = number_of_packets
        if port is not None:
            self._values["port"] = port
        if servername is not None:
            self._values["servername"] = servername
        if service is not None:
            self._values["service"] = service
        if should_track_hops is not None:
            self._values["should_track_hops"] = should_track_hops
        if timeout is not None:
            self._values["timeout"] = timeout
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def allow_insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allows loading insecure content for an HTTP test.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#allow_insecure SyntheticsTest#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def body(self) -> typing.Optional[builtins.str]:
        '''The request body.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#body SyntheticsTest#body}
        '''
        result = self._values.get("body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def body_type(self) -> typing.Optional[builtins.str]:
        '''Type of the request body. Valid values are ``text/plain``, ``application/json``, ``text/xml``, ``text/html``, ``application/x-www-form-urlencoded``, ``graphql``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#body_type SyntheticsTest#body_type}
        '''
        result = self._values.get("body_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def call_type(self) -> typing.Optional[builtins.str]:
        '''The type of gRPC call to perform. Valid values are ``healthcheck``, ``unary``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#call_type SyntheticsTest#call_type}
        '''
        result = self._values.get("call_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''By default, the client certificate is applied on the domain of the starting URL for browser tests.

        If you want your client certificate to be applied on other domains instead, add them in ``certificate_domains``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#certificate_domains SyntheticsTest#certificate_domains}
        '''
        result = self._values.get("certificate_domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dns_server(self) -> typing.Optional[builtins.str]:
        '''DNS server to use for DNS tests (``subtype = "dns"``).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#dns_server SyntheticsTest#dns_server}
        '''
        result = self._values.get("dns_server")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_server_port(self) -> typing.Optional[jsii.Number]:
        '''DNS server port to use for DNS tests.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#dns_server_port SyntheticsTest#dns_server_port}
        '''
        result = self._values.get("dns_server_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def follow_redirects(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether or not the API HTTP test should follow redirects.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#follow_redirects SyntheticsTest#follow_redirects}
        '''
        result = self._values.get("follow_redirects")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Host name to perform the test with.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#host SyntheticsTest#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''For UDP and websocket tests, message to send with the request.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#message SyntheticsTest#message}
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''Either the HTTP method/verb to use or a gRPC method available on the service set in the ``service`` field.

        Required if ``subtype`` is ``HTTP`` or if ``subtype`` is ``grpc`` and ``callType`` is ``unary``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#method SyntheticsTest#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_saving_response_body(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether or not to save the response body.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#no_saving_response_body SyntheticsTest#no_saving_response_body}
        '''
        result = self._values.get("no_saving_response_body")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def number_of_packets(self) -> typing.Optional[jsii.Number]:
        '''Number of pings to use per test for ICMP tests (``subtype = "icmp"``) between 0 and 10.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#number_of_packets SyntheticsTest#number_of_packets}
        '''
        result = self._values.get("number_of_packets")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port to use when performing the test.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#port SyntheticsTest#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def servername(self) -> typing.Optional[builtins.str]:
        '''For SSL tests, it specifies on which server you want to initiate the TLS handshake, allowing the server to present one of multiple possible certificates on the same IP address and TCP port number.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#servername SyntheticsTest#servername}
        '''
        result = self._values.get("servername")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''The gRPC service on which you want to perform the gRPC call.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#service SyntheticsTest#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def should_track_hops(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This will turn on a traceroute probe to discover all gateways along the path to the host destination.

        For ICMP tests (``subtype = "icmp"``).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#should_track_hops SyntheticsTest#should_track_hops}
        '''
        result = self._values.get("should_track_hops")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Timeout in seconds for the test. Defaults to ``60``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#timeout SyntheticsTest#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''The URL to send the request to.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#url SyntheticsTest#url}
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestApiStepRequestDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestApiStepRequestDefinitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepRequestDefinitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ede6ad30f5b25a9e1b321c9afed1100b9f773dd36c98e6828bd4de54cb1ae4a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowInsecure")
    def reset_allow_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowInsecure", []))

    @jsii.member(jsii_name="resetBody")
    def reset_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBody", []))

    @jsii.member(jsii_name="resetBodyType")
    def reset_body_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBodyType", []))

    @jsii.member(jsii_name="resetCallType")
    def reset_call_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCallType", []))

    @jsii.member(jsii_name="resetCertificateDomains")
    def reset_certificate_domains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateDomains", []))

    @jsii.member(jsii_name="resetDnsServer")
    def reset_dns_server(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsServer", []))

    @jsii.member(jsii_name="resetDnsServerPort")
    def reset_dns_server_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsServerPort", []))

    @jsii.member(jsii_name="resetFollowRedirects")
    def reset_follow_redirects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFollowRedirects", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetMessage")
    def reset_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessage", []))

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetNoSavingResponseBody")
    def reset_no_saving_response_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoSavingResponseBody", []))

    @jsii.member(jsii_name="resetNumberOfPackets")
    def reset_number_of_packets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberOfPackets", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetServername")
    def reset_servername(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServername", []))

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

    @jsii.member(jsii_name="resetShouldTrackHops")
    def reset_should_track_hops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShouldTrackHops", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="allowInsecureInput")
    def allow_insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowInsecureInput"))

    @builtins.property
    @jsii.member(jsii_name="bodyInput")
    def body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bodyInput"))

    @builtins.property
    @jsii.member(jsii_name="bodyTypeInput")
    def body_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bodyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="callTypeInput")
    def call_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "callTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateDomainsInput")
    def certificate_domains_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "certificateDomainsInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsServerInput")
    def dns_server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsServerInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsServerPortInput")
    def dns_server_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dnsServerPortInput"))

    @builtins.property
    @jsii.member(jsii_name="followRedirectsInput")
    def follow_redirects_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "followRedirectsInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="noSavingResponseBodyInput")
    def no_saving_response_body_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noSavingResponseBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="numberOfPacketsInput")
    def number_of_packets_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numberOfPacketsInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="servernameInput")
    def servername_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servernameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="shouldTrackHopsInput")
    def should_track_hops_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "shouldTrackHopsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecure")
    def allow_insecure(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowInsecure"))

    @allow_insecure.setter
    def allow_insecure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4815bab8a4dfa6f31127499e6028e569cf08763f3739aa894ee63f5d2790cc3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value)

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "body"))

    @body.setter
    def body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de19c0ba3c3703f89ab5d4f858319f0b746c1180a3dc7be49832c3e1e8352331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "body", value)

    @builtins.property
    @jsii.member(jsii_name="bodyType")
    def body_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bodyType"))

    @body_type.setter
    def body_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e74f6b01d27a8fc9c3bbf747ee571b53daa3de9f3573eadc8193455c55074505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bodyType", value)

    @builtins.property
    @jsii.member(jsii_name="callType")
    def call_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "callType"))

    @call_type.setter
    def call_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cee1168a40d5f1656adee3877f3b19343a662c1f4914479b3c338f16934fcd4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "callType", value)

    @builtins.property
    @jsii.member(jsii_name="certificateDomains")
    def certificate_domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "certificateDomains"))

    @certificate_domains.setter
    def certificate_domains(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bf8cdd238eca165744e8ef682150f0ba3d951641324340cc1b24080246d7785)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateDomains", value)

    @builtins.property
    @jsii.member(jsii_name="dnsServer")
    def dns_server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsServer"))

    @dns_server.setter
    def dns_server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52d7293d4e5123a12ec81258def6493af7dc75b73a3cf891dd34779032303dae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsServer", value)

    @builtins.property
    @jsii.member(jsii_name="dnsServerPort")
    def dns_server_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dnsServerPort"))

    @dns_server_port.setter
    def dns_server_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef06fcb3bc0bb44123d3c0cfad9e577126315ff449745737918f41ef0efddf07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsServerPort", value)

    @builtins.property
    @jsii.member(jsii_name="followRedirects")
    def follow_redirects(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "followRedirects"))

    @follow_redirects.setter
    def follow_redirects(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe1216699bb7e091374b9939ff1e0f467cb3610e5cf754b851cb3156e4d4893)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "followRedirects", value)

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88bc1be003a1700c729f7121c97f230d2e30032f20545b222a56562850f0604)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value)

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @message.setter
    def message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f53496ada838d7c34e17014a0624ad91e91cf5860d72eab130c4978e6ec899a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value)

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6628773fab9af66ec83ed5640eb097ec800e9183889f15ecef632b0327413508)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value)

    @builtins.property
    @jsii.member(jsii_name="noSavingResponseBody")
    def no_saving_response_body(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noSavingResponseBody"))

    @no_saving_response_body.setter
    def no_saving_response_body(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a06655a47a2542b75a4ff77380d489fabc88b6b87ce48ebf4aa5b2c2c6d44c6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noSavingResponseBody", value)

    @builtins.property
    @jsii.member(jsii_name="numberOfPackets")
    def number_of_packets(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberOfPackets"))

    @number_of_packets.setter
    def number_of_packets(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c0d4081f487131daf985ba7576afec6f1f73e8b7f907ca10aafa6380dbb8e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numberOfPackets", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e40b7fc4f4ed69f04548529d29c732ba99bb2c2e229db26f71f4b0a19606ca06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="servername")
    def servername(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servername"))

    @servername.setter
    def servername(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fb27272b7dca9380474f629a870bed0c2191722978790291dcae62f07761bef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servername", value)

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bbf3cefa6352b6472b13491f14731ab6e76796b33593dbf862a08072fe60334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value)

    @builtins.property
    @jsii.member(jsii_name="shouldTrackHops")
    def should_track_hops(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "shouldTrackHops"))

    @should_track_hops.setter
    def should_track_hops(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16740cf9990749666a228ca6e6a38690d427798a90317b6eb1ce4bbe5bafe5c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shouldTrackHops", value)

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9435dab16f6e26a844a7f48e9d42d0075bcedb92cc3987073ed1e366ba5c896a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__172587f1719bb68bd99c60b4ac768f402a1d36d0eade3bc7662aea059d37db0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SyntheticsTestApiStepRequestDefinition]:
        return typing.cast(typing.Optional[SyntheticsTestApiStepRequestDefinition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestApiStepRequestDefinition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fbc6ea3b856d32ed784588b640efe4894f3fba14d4be0f1855d1789b911a55b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepRequestProxy",
    jsii_struct_bases=[],
    name_mapping={"url": "url", "headers": "headers"},
)
class SyntheticsTestApiStepRequestProxy:
    def __init__(
        self,
        *,
        url: builtins.str,
        headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param url: URL of the proxy to perform the test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#url SyntheticsTest#url}
        :param headers: Header name and value map. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#headers SyntheticsTest#headers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a6b586490c6a8eb4ac03c07e0eec300cc3c452c48a3314c03726537e9a717e1)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if headers is not None:
            self._values["headers"] = headers

    @builtins.property
    def url(self) -> builtins.str:
        '''URL of the proxy to perform the test.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#url SyntheticsTest#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def headers(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Header name and value map.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#headers SyntheticsTest#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestApiStepRequestProxy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestApiStepRequestProxyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepRequestProxyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8afe44984e6d3025bf47f28328b40546863d794cfeff59c142abdd4b58b37d21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "headers"))

    @headers.setter
    def headers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb6631f6b5e0bcb40be0780532d5d2ec042aa8365c7b0ff31c0e4f62d55831d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headers", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a02dd7a29d23f1fe4cbec77cdc7d6342a28ec0cfd5e67c223b89cdf465b91d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SyntheticsTestApiStepRequestProxy]:
        return typing.cast(typing.Optional[SyntheticsTestApiStepRequestProxy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestApiStepRequestProxy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__448867a86985fe6720bf3cb87adffec3822dc6a76a5df9c5b72cbdc8b6881f5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepRetry",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "interval": "interval"},
)
class SyntheticsTestApiStepRetry:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: Number of retries needed to consider a location as failed before sending a notification alert. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#count SyntheticsTest#count}
        :param interval: Interval between a failed test and the next retry in milliseconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#interval SyntheticsTest#interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93202b1ed0aba7204e0eb616c5b350e597a30b5352d2eb607f00173a80d523db)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if interval is not None:
            self._values["interval"] = interval

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''Number of retries needed to consider a location as failed before sending a notification alert.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#count SyntheticsTest#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''Interval between a failed test and the next retry in milliseconds.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#interval SyntheticsTest#interval}
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestApiStepRetry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestApiStepRetryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestApiStepRetryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__079ff7f2ced2195bf68427b01a412d31df2556736d839556cde9f4574d1d6a98)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d454975e13067c05f175b3194bee22ca9971eaba058b7cb72942c01eee19cce8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37d8c3099af2188f6cc18fa631a4ded71c14e65c21ef00a3631ec807e1c531b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SyntheticsTestApiStepRetry]:
        return typing.cast(typing.Optional[SyntheticsTestApiStepRetry], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestApiStepRetry],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__add889335cc766e5867a30c6f3641d62f81f7a79388001cb49b8573b040bbdc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestAssertion",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "type": "type",
        "property": "property",
        "target": "target",
        "targetjsonpath": "targetjsonpath",
        "targetxpath": "targetxpath",
    },
)
class SyntheticsTestAssertion:
    def __init__(
        self,
        *,
        operator: builtins.str,
        type: builtins.str,
        property: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        targetjsonpath: typing.Optional[typing.Union["SyntheticsTestAssertionTargetjsonpath", typing.Dict[builtins.str, typing.Any]]] = None,
        targetxpath: typing.Optional[typing.Union["SyntheticsTestAssertionTargetxpath", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param operator: Assertion operator. **Note** Only some combinations of ``type`` and ``operator`` are valid (please refer to `Datadog documentation <https://docs.datadoghq.com/api/latest/synthetics/#create-a-test>`_). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#operator SyntheticsTest#operator}
        :param type: Type of assertion. **Note** Only some combinations of ``type`` and ``operator`` are valid (please refer to `Datadog documentation <https://docs.datadoghq.com/api/latest/synthetics/#create-a-test>`_). Valid values are ``body``, ``header``, ``statusCode``, ``certificate``, ``responseTime``, ``property``, ``recordEvery``, ``recordSome``, ``tlsVersion``, ``minTlsVersion``, ``latency``, ``packetLossPercentage``, ``packetsReceived``, ``networkHop``, ``receivedMessage``, ``grpcHealthcheckStatus``, ``connection``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        :param property: If assertion type is ``header``, this is the header name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#property SyntheticsTest#property}
        :param target: Expected value. Depends on the assertion type, refer to `Datadog documentation <https://docs.datadoghq.com/api/latest/synthetics/#create-a-test>`_ for details. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#target SyntheticsTest#target}
        :param targetjsonpath: targetjsonpath block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#targetjsonpath SyntheticsTest#targetjsonpath}
        :param targetxpath: targetxpath block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#targetxpath SyntheticsTest#targetxpath}
        '''
        if isinstance(targetjsonpath, dict):
            targetjsonpath = SyntheticsTestAssertionTargetjsonpath(**targetjsonpath)
        if isinstance(targetxpath, dict):
            targetxpath = SyntheticsTestAssertionTargetxpath(**targetxpath)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8f680cc39cf070e1447a0bd2ee97533a5f454c2f8b2ff8243121a09438fc107)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument property", value=property, expected_type=type_hints["property"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument targetjsonpath", value=targetjsonpath, expected_type=type_hints["targetjsonpath"])
            check_type(argname="argument targetxpath", value=targetxpath, expected_type=type_hints["targetxpath"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "type": type,
        }
        if property is not None:
            self._values["property"] = property
        if target is not None:
            self._values["target"] = target
        if targetjsonpath is not None:
            self._values["targetjsonpath"] = targetjsonpath
        if targetxpath is not None:
            self._values["targetxpath"] = targetxpath

    @builtins.property
    def operator(self) -> builtins.str:
        '''Assertion operator. **Note** Only some combinations of ``type`` and ``operator`` are valid (please refer to `Datadog documentation <https://docs.datadoghq.com/api/latest/synthetics/#create-a-test>`_).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#operator SyntheticsTest#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of assertion.

        **Note** Only some combinations of ``type`` and ``operator`` are valid (please refer to `Datadog documentation <https://docs.datadoghq.com/api/latest/synthetics/#create-a-test>`_). Valid values are ``body``, ``header``, ``statusCode``, ``certificate``, ``responseTime``, ``property``, ``recordEvery``, ``recordSome``, ``tlsVersion``, ``minTlsVersion``, ``latency``, ``packetLossPercentage``, ``packetsReceived``, ``networkHop``, ``receivedMessage``, ``grpcHealthcheckStatus``, ``connection``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def property(self) -> typing.Optional[builtins.str]:
        '''If assertion type is ``header``, this is the header name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#property SyntheticsTest#property}
        '''
        result = self._values.get("property")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Expected value. Depends on the assertion type, refer to `Datadog documentation <https://docs.datadoghq.com/api/latest/synthetics/#create-a-test>`_ for details.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#target SyntheticsTest#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def targetjsonpath(
        self,
    ) -> typing.Optional["SyntheticsTestAssertionTargetjsonpath"]:
        '''targetjsonpath block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#targetjsonpath SyntheticsTest#targetjsonpath}
        '''
        result = self._values.get("targetjsonpath")
        return typing.cast(typing.Optional["SyntheticsTestAssertionTargetjsonpath"], result)

    @builtins.property
    def targetxpath(self) -> typing.Optional["SyntheticsTestAssertionTargetxpath"]:
        '''targetxpath block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#targetxpath SyntheticsTest#targetxpath}
        '''
        result = self._values.get("targetxpath")
        return typing.cast(typing.Optional["SyntheticsTestAssertionTargetxpath"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestAssertion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestAssertionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestAssertionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca7f2d58e47f0d7520ece682adcb4b56748c4ed4a65f30716860703f3ab7f5c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SyntheticsTestAssertionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__337d51562deaee05934e41a3089343f6d08b66ff79bafb30929dbcac5059bd71)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SyntheticsTestAssertionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aedfbabe9c478cd330d54a16aea7f68da7b87adaf1374429952fcba5c4fde58b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d9c07a966e7415f877eb24338ee57b27bf0174e18b3fb9d8d4d6fdd3097ab0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55e652a162ead998a0d1d8a3a9ffc8b78b3cf3aa013469b593ccfb0d063d3733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestAssertion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestAssertion]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestAssertion]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d02b690f9350e1c0434e290ff5dbfb9316cf01e096581d1a5aad0ef5b2f37d7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SyntheticsTestAssertionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestAssertionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78d216a284f2803dad5c90dbc4efb4d8131ce265440c3539a96b37eb30c35e39)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTargetjsonpath")
    def put_targetjsonpath(
        self,
        *,
        jsonpath: builtins.str,
        operator: builtins.str,
        targetvalue: builtins.str,
    ) -> None:
        '''
        :param jsonpath: The JSON path to assert. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#jsonpath SyntheticsTest#jsonpath}
        :param operator: The specific operator to use on the path. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#operator SyntheticsTest#operator}
        :param targetvalue: Expected matching value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#targetvalue SyntheticsTest#targetvalue}
        '''
        value = SyntheticsTestAssertionTargetjsonpath(
            jsonpath=jsonpath, operator=operator, targetvalue=targetvalue
        )

        return typing.cast(None, jsii.invoke(self, "putTargetjsonpath", [value]))

    @jsii.member(jsii_name="putTargetxpath")
    def put_targetxpath(
        self,
        *,
        operator: builtins.str,
        targetvalue: builtins.str,
        xpath: builtins.str,
    ) -> None:
        '''
        :param operator: The specific operator to use on the path. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#operator SyntheticsTest#operator}
        :param targetvalue: Expected matching value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#targetvalue SyntheticsTest#targetvalue}
        :param xpath: The xpath to assert. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#xpath SyntheticsTest#xpath}
        '''
        value = SyntheticsTestAssertionTargetxpath(
            operator=operator, targetvalue=targetvalue, xpath=xpath
        )

        return typing.cast(None, jsii.invoke(self, "putTargetxpath", [value]))

    @jsii.member(jsii_name="resetProperty")
    def reset_property(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperty", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @jsii.member(jsii_name="resetTargetjsonpath")
    def reset_targetjsonpath(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetjsonpath", []))

    @jsii.member(jsii_name="resetTargetxpath")
    def reset_targetxpath(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetxpath", []))

    @builtins.property
    @jsii.member(jsii_name="targetjsonpath")
    def targetjsonpath(self) -> "SyntheticsTestAssertionTargetjsonpathOutputReference":
        return typing.cast("SyntheticsTestAssertionTargetjsonpathOutputReference", jsii.get(self, "targetjsonpath"))

    @builtins.property
    @jsii.member(jsii_name="targetxpath")
    def targetxpath(self) -> "SyntheticsTestAssertionTargetxpathOutputReference":
        return typing.cast("SyntheticsTestAssertionTargetxpathOutputReference", jsii.get(self, "targetxpath"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="propertyInput")
    def property_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "propertyInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="targetjsonpathInput")
    def targetjsonpath_input(
        self,
    ) -> typing.Optional["SyntheticsTestAssertionTargetjsonpath"]:
        return typing.cast(typing.Optional["SyntheticsTestAssertionTargetjsonpath"], jsii.get(self, "targetjsonpathInput"))

    @builtins.property
    @jsii.member(jsii_name="targetxpathInput")
    def targetxpath_input(
        self,
    ) -> typing.Optional["SyntheticsTestAssertionTargetxpath"]:
        return typing.cast(typing.Optional["SyntheticsTestAssertionTargetxpath"], jsii.get(self, "targetxpathInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__012f52448702dfeb235aaa7c61ad4da717a33214351a51ebbea56faf9332001c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="property")
    def property(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "property"))

    @property.setter
    def property(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85ffc09c8ade75e9cc43b15f99f5ae1e2120ce5029bc5e33f60ac4b617f539eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "property", value)

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__560fca9f4221d10abcb26359fe979e54d7c136e44e2c7b3f534759b28c710d83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab76e45c254bbf039909da9cb76596192eddaff2f027afae714ee4c6dacf9a6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SyntheticsTestAssertion, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SyntheticsTestAssertion, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SyntheticsTestAssertion, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d79f758131e4e1b3b57f6dd6ff76fb593ae39eedbb2092892c40ed672d3a386b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestAssertionTargetjsonpath",
    jsii_struct_bases=[],
    name_mapping={
        "jsonpath": "jsonpath",
        "operator": "operator",
        "targetvalue": "targetvalue",
    },
)
class SyntheticsTestAssertionTargetjsonpath:
    def __init__(
        self,
        *,
        jsonpath: builtins.str,
        operator: builtins.str,
        targetvalue: builtins.str,
    ) -> None:
        '''
        :param jsonpath: The JSON path to assert. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#jsonpath SyntheticsTest#jsonpath}
        :param operator: The specific operator to use on the path. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#operator SyntheticsTest#operator}
        :param targetvalue: Expected matching value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#targetvalue SyntheticsTest#targetvalue}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ffa57513c222e27013d3b57a97355879b583001e6995c55ec6b2d102a0973c5)
            check_type(argname="argument jsonpath", value=jsonpath, expected_type=type_hints["jsonpath"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument targetvalue", value=targetvalue, expected_type=type_hints["targetvalue"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "jsonpath": jsonpath,
            "operator": operator,
            "targetvalue": targetvalue,
        }

    @builtins.property
    def jsonpath(self) -> builtins.str:
        '''The JSON path to assert.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#jsonpath SyntheticsTest#jsonpath}
        '''
        result = self._values.get("jsonpath")
        assert result is not None, "Required property 'jsonpath' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''The specific operator to use on the path.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#operator SyntheticsTest#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def targetvalue(self) -> builtins.str:
        '''Expected matching value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#targetvalue SyntheticsTest#targetvalue}
        '''
        result = self._values.get("targetvalue")
        assert result is not None, "Required property 'targetvalue' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestAssertionTargetjsonpath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestAssertionTargetjsonpathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestAssertionTargetjsonpathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4afd6cce2cc60355c9d39831bed00fbcbf459842a28cc1b9b494a55f4aa54736)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="jsonpathInput")
    def jsonpath_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jsonpathInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="targetvalueInput")
    def targetvalue_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetvalueInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonpath")
    def jsonpath(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jsonpath"))

    @jsonpath.setter
    def jsonpath(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3456a3efb04700a3684fa686b26d63fdf78305d32c0fb43b640a2005603898cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonpath", value)

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa1782a7f290a8eed0ebccf4f85a1ade57c04b9e24e86d530b9629295009767b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="targetvalue")
    def targetvalue(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetvalue"))

    @targetvalue.setter
    def targetvalue(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13a184072dad3c082c190f7530c00e306c5aef585b52700e4d65a6bae3463b0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetvalue", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SyntheticsTestAssertionTargetjsonpath]:
        return typing.cast(typing.Optional[SyntheticsTestAssertionTargetjsonpath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestAssertionTargetjsonpath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed4073f8d6054cba2e662bc85ba93cb9cc846cb854798d955662ecdecdbaff21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestAssertionTargetxpath",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "targetvalue": "targetvalue",
        "xpath": "xpath",
    },
)
class SyntheticsTestAssertionTargetxpath:
    def __init__(
        self,
        *,
        operator: builtins.str,
        targetvalue: builtins.str,
        xpath: builtins.str,
    ) -> None:
        '''
        :param operator: The specific operator to use on the path. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#operator SyntheticsTest#operator}
        :param targetvalue: Expected matching value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#targetvalue SyntheticsTest#targetvalue}
        :param xpath: The xpath to assert. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#xpath SyntheticsTest#xpath}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3120d1914f6076cb9896c1a6be251cf70ba0b24166d11094743e117af51e8270)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument targetvalue", value=targetvalue, expected_type=type_hints["targetvalue"])
            check_type(argname="argument xpath", value=xpath, expected_type=type_hints["xpath"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "targetvalue": targetvalue,
            "xpath": xpath,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''The specific operator to use on the path.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#operator SyntheticsTest#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def targetvalue(self) -> builtins.str:
        '''Expected matching value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#targetvalue SyntheticsTest#targetvalue}
        '''
        result = self._values.get("targetvalue")
        assert result is not None, "Required property 'targetvalue' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def xpath(self) -> builtins.str:
        '''The xpath to assert.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#xpath SyntheticsTest#xpath}
        '''
        result = self._values.get("xpath")
        assert result is not None, "Required property 'xpath' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestAssertionTargetxpath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestAssertionTargetxpathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestAssertionTargetxpathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__585355cff70b8e62011a75cf23344b5848d8a0137bed1ba60f848eb923511f57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="targetvalueInput")
    def targetvalue_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetvalueInput"))

    @builtins.property
    @jsii.member(jsii_name="xpathInput")
    def xpath_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "xpathInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea2e9e592ced1ca582fd0346cf23538bc044da3f7c69986d01de4e348159b24e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="targetvalue")
    def targetvalue(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetvalue"))

    @targetvalue.setter
    def targetvalue(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d19738bb2a513c39da1d51e4b42e796e2b79a8b58e17aef1da58aec3fa043060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetvalue", value)

    @builtins.property
    @jsii.member(jsii_name="xpath")
    def xpath(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "xpath"))

    @xpath.setter
    def xpath(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f4bb94bc6482f59cf895943434995e3bd97d64875eed0f152ba8dac66e54a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xpath", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SyntheticsTestAssertionTargetxpath]:
        return typing.cast(typing.Optional[SyntheticsTestAssertionTargetxpath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestAssertionTargetxpath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__227cb7eb4ffa6242af307fced300fa328551f6fbe61c1894e1e4cc9ade6be5bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestBrowserStep",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "params": "params",
        "type": "type",
        "allow_failure": "allowFailure",
        "force_element_update": "forceElementUpdate",
        "is_critical": "isCritical",
        "timeout": "timeout",
    },
)
class SyntheticsTestBrowserStep:
    def __init__(
        self,
        *,
        name: builtins.str,
        params: typing.Union["SyntheticsTestBrowserStepParams", typing.Dict[builtins.str, typing.Any]],
        type: builtins.str,
        allow_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        force_element_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_critical: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: Name of the step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#name SyntheticsTest#name}
        :param params: params block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#params SyntheticsTest#params}
        :param type: Type of the step. Valid values are ``assertCurrentUrl``, ``assertElementAttribute``, ``assertElementContent``, ``assertElementPresent``, ``assertEmail``, ``assertFileDownload``, ``assertFromJavascript``, ``assertPageContains``, ``assertPageLacks``, ``click``, ``extractFromJavascript``, ``extractVariable``, ``goToEmailLink``, ``goToUrl``, ``goToUrlAndMeasureTti``, ``hover``, ``playSubTest``, ``pressKey``, ``refresh``, ``runApiTest``, ``scroll``, ``selectOption``, ``typeText``, ``uploadFiles``, ``wait``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        :param allow_failure: Determines if the step should be allowed to fail. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#allow_failure SyntheticsTest#allow_failure}
        :param force_element_update: Force update of the "element" parameter for the step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#force_element_update SyntheticsTest#force_element_update}
        :param is_critical: Determines whether or not to consider the entire test as failed if this step fails. Can be used only if ``allow_failure`` is ``true``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#is_critical SyntheticsTest#is_critical}
        :param timeout: Used to override the default timeout of a step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#timeout SyntheticsTest#timeout}
        '''
        if isinstance(params, dict):
            params = SyntheticsTestBrowserStepParams(**params)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bef9dfde181bc34f72586c78fb39d835c87236cf565b67e5f92703601ab35b0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument params", value=params, expected_type=type_hints["params"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument allow_failure", value=allow_failure, expected_type=type_hints["allow_failure"])
            check_type(argname="argument force_element_update", value=force_element_update, expected_type=type_hints["force_element_update"])
            check_type(argname="argument is_critical", value=is_critical, expected_type=type_hints["is_critical"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "params": params,
            "type": type,
        }
        if allow_failure is not None:
            self._values["allow_failure"] = allow_failure
        if force_element_update is not None:
            self._values["force_element_update"] = force_element_update
        if is_critical is not None:
            self._values["is_critical"] = is_critical
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the step.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#name SyntheticsTest#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def params(self) -> "SyntheticsTestBrowserStepParams":
        '''params block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#params SyntheticsTest#params}
        '''
        result = self._values.get("params")
        assert result is not None, "Required property 'params' is missing"
        return typing.cast("SyntheticsTestBrowserStepParams", result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of the step.

        Valid values are ``assertCurrentUrl``, ``assertElementAttribute``, ``assertElementContent``, ``assertElementPresent``, ``assertEmail``, ``assertFileDownload``, ``assertFromJavascript``, ``assertPageContains``, ``assertPageLacks``, ``click``, ``extractFromJavascript``, ``extractVariable``, ``goToEmailLink``, ``goToUrl``, ``goToUrlAndMeasureTti``, ``hover``, ``playSubTest``, ``pressKey``, ``refresh``, ``runApiTest``, ``scroll``, ``selectOption``, ``typeText``, ``uploadFiles``, ``wait``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_failure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines if the step should be allowed to fail.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#allow_failure SyntheticsTest#allow_failure}
        '''
        result = self._values.get("allow_failure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def force_element_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Force update of the "element" parameter for the step.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#force_element_update SyntheticsTest#force_element_update}
        '''
        result = self._values.get("force_element_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_critical(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether or not to consider the entire test as failed if this step fails.

        Can be used only if ``allow_failure`` is ``true``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#is_critical SyntheticsTest#is_critical}
        '''
        result = self._values.get("is_critical")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Used to override the default timeout of a step.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#timeout SyntheticsTest#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestBrowserStep(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestBrowserStepList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestBrowserStepList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a9b896de28b4dfa51d955060a2316d2e2f5b8637fc8a0d43c7cfdd65b7c4dd3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SyntheticsTestBrowserStepOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf7594dc10fe9f984ccb26e37ab0b9697b05a6e327495b4f0b54db094c9ccf6e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SyntheticsTestBrowserStepOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaf8c7e26f2a17aa4058c6327a958eed38514f9bc64b47298f5ef4068d924e6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e344cd935198389499f7635da7149f211a0cbd77c9cdb21a83ed0a20d873bfa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__923aa94d27a4e4b8ee1665312cc3a33e4e591014a31f74bb27ef69d84dae393b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestBrowserStep]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestBrowserStep]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestBrowserStep]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59a7bc160b4d6412d345bcae6cd67f725b3fd075bf179cb39585bd62f222c611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SyntheticsTestBrowserStepOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestBrowserStepOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdeb9037f8d3136c89b5558ba1b8b84727d14fb80682ccbc47ceb97a485bbcee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putParams")
    def put_params(
        self,
        *,
        attribute: typing.Optional[builtins.str] = None,
        check: typing.Optional[builtins.str] = None,
        click_type: typing.Optional[builtins.str] = None,
        code: typing.Optional[builtins.str] = None,
        delay: typing.Optional[jsii.Number] = None,
        element: typing.Optional[builtins.str] = None,
        element_user_locator: typing.Optional[typing.Union["SyntheticsTestBrowserStepParamsElementUserLocator", typing.Dict[builtins.str, typing.Any]]] = None,
        email: typing.Optional[builtins.str] = None,
        file: typing.Optional[builtins.str] = None,
        files: typing.Optional[builtins.str] = None,
        modifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        playing_tab_id: typing.Optional[builtins.str] = None,
        request: typing.Optional[builtins.str] = None,
        subtest_public_id: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
        variable: typing.Optional[typing.Union["SyntheticsTestBrowserStepParamsVariable", typing.Dict[builtins.str, typing.Any]]] = None,
        with_click: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param attribute: Name of the attribute to use for an "assert attribute" step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#attribute SyntheticsTest#attribute}
        :param check: Check type to use for an assertion step. Valid values are ``equals``, ``notEquals``, ``contains``, ``notContains``, ``startsWith``, ``notStartsWith``, ``greater``, ``lower``, ``greaterEquals``, ``lowerEquals``, ``matchRegex``, ``between``, ``isEmpty``, ``notIsEmpty``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#check SyntheticsTest#check}
        :param click_type: Type of click to use for a "click" step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#click_type SyntheticsTest#click_type}
        :param code: Javascript code to use for the step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#code SyntheticsTest#code}
        :param delay: Delay between each key stroke for a "type test" step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#delay SyntheticsTest#delay}
        :param element: Element to use for the step, json encoded string. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#element SyntheticsTest#element}
        :param element_user_locator: element_user_locator block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#element_user_locator SyntheticsTest#element_user_locator}
        :param email: Details of the email for an "assert email" step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#email SyntheticsTest#email}
        :param file: For an "assert download" step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#file SyntheticsTest#file}
        :param files: Details of the files for an "upload files" step, json encoded string. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#files SyntheticsTest#files}
        :param modifiers: Modifier to use for a "press key" step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#modifiers SyntheticsTest#modifiers}
        :param playing_tab_id: ID of the tab to play the subtest. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#playing_tab_id SyntheticsTest#playing_tab_id}
        :param request: Request for an API step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request SyntheticsTest#request}
        :param subtest_public_id: ID of the Synthetics test to use as subtest. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#subtest_public_id SyntheticsTest#subtest_public_id}
        :param value: Value of the step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#value SyntheticsTest#value}
        :param variable: variable block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#variable SyntheticsTest#variable}
        :param with_click: For "file upload" steps. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#with_click SyntheticsTest#with_click}
        :param x: X coordinates for a "scroll step". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#x SyntheticsTest#x}
        :param y: Y coordinates for a "scroll step". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#y SyntheticsTest#y}
        '''
        value_ = SyntheticsTestBrowserStepParams(
            attribute=attribute,
            check=check,
            click_type=click_type,
            code=code,
            delay=delay,
            element=element,
            element_user_locator=element_user_locator,
            email=email,
            file=file,
            files=files,
            modifiers=modifiers,
            playing_tab_id=playing_tab_id,
            request=request,
            subtest_public_id=subtest_public_id,
            value=value,
            variable=variable,
            with_click=with_click,
            x=x,
            y=y,
        )

        return typing.cast(None, jsii.invoke(self, "putParams", [value_]))

    @jsii.member(jsii_name="resetAllowFailure")
    def reset_allow_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowFailure", []))

    @jsii.member(jsii_name="resetForceElementUpdate")
    def reset_force_element_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceElementUpdate", []))

    @jsii.member(jsii_name="resetIsCritical")
    def reset_is_critical(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsCritical", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="params")
    def params(self) -> "SyntheticsTestBrowserStepParamsOutputReference":
        return typing.cast("SyntheticsTestBrowserStepParamsOutputReference", jsii.get(self, "params"))

    @builtins.property
    @jsii.member(jsii_name="allowFailureInput")
    def allow_failure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="forceElementUpdateInput")
    def force_element_update_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceElementUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="isCriticalInput")
    def is_critical_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isCriticalInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="paramsInput")
    def params_input(self) -> typing.Optional["SyntheticsTestBrowserStepParams"]:
        return typing.cast(typing.Optional["SyntheticsTestBrowserStepParams"], jsii.get(self, "paramsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowFailure")
    def allow_failure(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowFailure"))

    @allow_failure.setter
    def allow_failure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ae18289530ea4981c9278eec15ba8a13f3b02e4d981356d696cf059527f9c2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowFailure", value)

    @builtins.property
    @jsii.member(jsii_name="forceElementUpdate")
    def force_element_update(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceElementUpdate"))

    @force_element_update.setter
    def force_element_update(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58babd09c621ef72610027b2cad94b7f1c395bcfb01b44c532aca592afe754fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceElementUpdate", value)

    @builtins.property
    @jsii.member(jsii_name="isCritical")
    def is_critical(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isCritical"))

    @is_critical.setter
    def is_critical(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72917cd111cb88a23ef94877eeebbcc6bc4ba61f7664d0b90c747b98f2b302f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isCritical", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3110fbf0e9237e2de8c122c1cc2fa5bb8813c7bc33aaad5eba607aed7424483c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7f89e2a1af5b5e214519072df8bfe935be5ab41d1ec659d433cd08930f1901a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__686dee2dea23f439aeaa26c6780c2162e1e2d6de32a24d4d327ac3a17702aed4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SyntheticsTestBrowserStep, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SyntheticsTestBrowserStep, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SyntheticsTestBrowserStep, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e801e34d8760125a72c71344b3b0049a045bee54bc9d2c84149e56c840cae19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestBrowserStepParams",
    jsii_struct_bases=[],
    name_mapping={
        "attribute": "attribute",
        "check": "check",
        "click_type": "clickType",
        "code": "code",
        "delay": "delay",
        "element": "element",
        "element_user_locator": "elementUserLocator",
        "email": "email",
        "file": "file",
        "files": "files",
        "modifiers": "modifiers",
        "playing_tab_id": "playingTabId",
        "request": "request",
        "subtest_public_id": "subtestPublicId",
        "value": "value",
        "variable": "variable",
        "with_click": "withClick",
        "x": "x",
        "y": "y",
    },
)
class SyntheticsTestBrowserStepParams:
    def __init__(
        self,
        *,
        attribute: typing.Optional[builtins.str] = None,
        check: typing.Optional[builtins.str] = None,
        click_type: typing.Optional[builtins.str] = None,
        code: typing.Optional[builtins.str] = None,
        delay: typing.Optional[jsii.Number] = None,
        element: typing.Optional[builtins.str] = None,
        element_user_locator: typing.Optional[typing.Union["SyntheticsTestBrowserStepParamsElementUserLocator", typing.Dict[builtins.str, typing.Any]]] = None,
        email: typing.Optional[builtins.str] = None,
        file: typing.Optional[builtins.str] = None,
        files: typing.Optional[builtins.str] = None,
        modifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        playing_tab_id: typing.Optional[builtins.str] = None,
        request: typing.Optional[builtins.str] = None,
        subtest_public_id: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
        variable: typing.Optional[typing.Union["SyntheticsTestBrowserStepParamsVariable", typing.Dict[builtins.str, typing.Any]]] = None,
        with_click: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param attribute: Name of the attribute to use for an "assert attribute" step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#attribute SyntheticsTest#attribute}
        :param check: Check type to use for an assertion step. Valid values are ``equals``, ``notEquals``, ``contains``, ``notContains``, ``startsWith``, ``notStartsWith``, ``greater``, ``lower``, ``greaterEquals``, ``lowerEquals``, ``matchRegex``, ``between``, ``isEmpty``, ``notIsEmpty``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#check SyntheticsTest#check}
        :param click_type: Type of click to use for a "click" step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#click_type SyntheticsTest#click_type}
        :param code: Javascript code to use for the step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#code SyntheticsTest#code}
        :param delay: Delay between each key stroke for a "type test" step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#delay SyntheticsTest#delay}
        :param element: Element to use for the step, json encoded string. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#element SyntheticsTest#element}
        :param element_user_locator: element_user_locator block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#element_user_locator SyntheticsTest#element_user_locator}
        :param email: Details of the email for an "assert email" step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#email SyntheticsTest#email}
        :param file: For an "assert download" step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#file SyntheticsTest#file}
        :param files: Details of the files for an "upload files" step, json encoded string. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#files SyntheticsTest#files}
        :param modifiers: Modifier to use for a "press key" step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#modifiers SyntheticsTest#modifiers}
        :param playing_tab_id: ID of the tab to play the subtest. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#playing_tab_id SyntheticsTest#playing_tab_id}
        :param request: Request for an API step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request SyntheticsTest#request}
        :param subtest_public_id: ID of the Synthetics test to use as subtest. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#subtest_public_id SyntheticsTest#subtest_public_id}
        :param value: Value of the step. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#value SyntheticsTest#value}
        :param variable: variable block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#variable SyntheticsTest#variable}
        :param with_click: For "file upload" steps. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#with_click SyntheticsTest#with_click}
        :param x: X coordinates for a "scroll step". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#x SyntheticsTest#x}
        :param y: Y coordinates for a "scroll step". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#y SyntheticsTest#y}
        '''
        if isinstance(element_user_locator, dict):
            element_user_locator = SyntheticsTestBrowserStepParamsElementUserLocator(**element_user_locator)
        if isinstance(variable, dict):
            variable = SyntheticsTestBrowserStepParamsVariable(**variable)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__292471245b096e37334129ad026ea7b6b3974a8db36bb6c42ede8e9bb2c5042d)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
            check_type(argname="argument check", value=check, expected_type=type_hints["check"])
            check_type(argname="argument click_type", value=click_type, expected_type=type_hints["click_type"])
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument delay", value=delay, expected_type=type_hints["delay"])
            check_type(argname="argument element", value=element, expected_type=type_hints["element"])
            check_type(argname="argument element_user_locator", value=element_user_locator, expected_type=type_hints["element_user_locator"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument files", value=files, expected_type=type_hints["files"])
            check_type(argname="argument modifiers", value=modifiers, expected_type=type_hints["modifiers"])
            check_type(argname="argument playing_tab_id", value=playing_tab_id, expected_type=type_hints["playing_tab_id"])
            check_type(argname="argument request", value=request, expected_type=type_hints["request"])
            check_type(argname="argument subtest_public_id", value=subtest_public_id, expected_type=type_hints["subtest_public_id"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument variable", value=variable, expected_type=type_hints["variable"])
            check_type(argname="argument with_click", value=with_click, expected_type=type_hints["with_click"])
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
            check_type(argname="argument y", value=y, expected_type=type_hints["y"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attribute is not None:
            self._values["attribute"] = attribute
        if check is not None:
            self._values["check"] = check
        if click_type is not None:
            self._values["click_type"] = click_type
        if code is not None:
            self._values["code"] = code
        if delay is not None:
            self._values["delay"] = delay
        if element is not None:
            self._values["element"] = element
        if element_user_locator is not None:
            self._values["element_user_locator"] = element_user_locator
        if email is not None:
            self._values["email"] = email
        if file is not None:
            self._values["file"] = file
        if files is not None:
            self._values["files"] = files
        if modifiers is not None:
            self._values["modifiers"] = modifiers
        if playing_tab_id is not None:
            self._values["playing_tab_id"] = playing_tab_id
        if request is not None:
            self._values["request"] = request
        if subtest_public_id is not None:
            self._values["subtest_public_id"] = subtest_public_id
        if value is not None:
            self._values["value"] = value
        if variable is not None:
            self._values["variable"] = variable
        if with_click is not None:
            self._values["with_click"] = with_click
        if x is not None:
            self._values["x"] = x
        if y is not None:
            self._values["y"] = y

    @builtins.property
    def attribute(self) -> typing.Optional[builtins.str]:
        '''Name of the attribute to use for an "assert attribute" step.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#attribute SyntheticsTest#attribute}
        '''
        result = self._values.get("attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def check(self) -> typing.Optional[builtins.str]:
        '''Check type to use for an assertion step.

        Valid values are ``equals``, ``notEquals``, ``contains``, ``notContains``, ``startsWith``, ``notStartsWith``, ``greater``, ``lower``, ``greaterEquals``, ``lowerEquals``, ``matchRegex``, ``between``, ``isEmpty``, ``notIsEmpty``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#check SyntheticsTest#check}
        '''
        result = self._values.get("check")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def click_type(self) -> typing.Optional[builtins.str]:
        '''Type of click to use for a "click" step.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#click_type SyntheticsTest#click_type}
        '''
        result = self._values.get("click_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code(self) -> typing.Optional[builtins.str]:
        '''Javascript code to use for the step.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#code SyntheticsTest#code}
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delay(self) -> typing.Optional[jsii.Number]:
        '''Delay between each key stroke for a "type test" step.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#delay SyntheticsTest#delay}
        '''
        result = self._values.get("delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def element(self) -> typing.Optional[builtins.str]:
        '''Element to use for the step, json encoded string.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#element SyntheticsTest#element}
        '''
        result = self._values.get("element")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def element_user_locator(
        self,
    ) -> typing.Optional["SyntheticsTestBrowserStepParamsElementUserLocator"]:
        '''element_user_locator block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#element_user_locator SyntheticsTest#element_user_locator}
        '''
        result = self._values.get("element_user_locator")
        return typing.cast(typing.Optional["SyntheticsTestBrowserStepParamsElementUserLocator"], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Details of the email for an "assert email" step.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#email SyntheticsTest#email}
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file(self) -> typing.Optional[builtins.str]:
        '''For an "assert download" step.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#file SyntheticsTest#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def files(self) -> typing.Optional[builtins.str]:
        '''Details of the files for an "upload files" step, json encoded string.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#files SyntheticsTest#files}
        '''
        result = self._values.get("files")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def modifiers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Modifier to use for a "press key" step.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#modifiers SyntheticsTest#modifiers}
        '''
        result = self._values.get("modifiers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def playing_tab_id(self) -> typing.Optional[builtins.str]:
        '''ID of the tab to play the subtest.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#playing_tab_id SyntheticsTest#playing_tab_id}
        '''
        result = self._values.get("playing_tab_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request(self) -> typing.Optional[builtins.str]:
        '''Request for an API step.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request SyntheticsTest#request}
        '''
        result = self._values.get("request")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subtest_public_id(self) -> typing.Optional[builtins.str]:
        '''ID of the Synthetics test to use as subtest.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#subtest_public_id SyntheticsTest#subtest_public_id}
        '''
        result = self._values.get("subtest_public_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value of the step.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#value SyntheticsTest#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variable(self) -> typing.Optional["SyntheticsTestBrowserStepParamsVariable"]:
        '''variable block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#variable SyntheticsTest#variable}
        '''
        result = self._values.get("variable")
        return typing.cast(typing.Optional["SyntheticsTestBrowserStepParamsVariable"], result)

    @builtins.property
    def with_click(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''For "file upload" steps.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#with_click SyntheticsTest#with_click}
        '''
        result = self._values.get("with_click")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def x(self) -> typing.Optional[jsii.Number]:
        '''X coordinates for a "scroll step".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#x SyntheticsTest#x}
        '''
        result = self._values.get("x")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def y(self) -> typing.Optional[jsii.Number]:
        '''Y coordinates for a "scroll step".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#y SyntheticsTest#y}
        '''
        result = self._values.get("y")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestBrowserStepParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestBrowserStepParamsElementUserLocator",
    jsii_struct_bases=[],
    name_mapping={
        "value": "value",
        "fail_test_on_cannot_locate": "failTestOnCannotLocate",
    },
)
class SyntheticsTestBrowserStepParamsElementUserLocator:
    def __init__(
        self,
        *,
        value: typing.Union["SyntheticsTestBrowserStepParamsElementUserLocatorValue", typing.Dict[builtins.str, typing.Any]],
        fail_test_on_cannot_locate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param value: value block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#value SyntheticsTest#value}
        :param fail_test_on_cannot_locate: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#fail_test_on_cannot_locate SyntheticsTest#fail_test_on_cannot_locate}.
        '''
        if isinstance(value, dict):
            value = SyntheticsTestBrowserStepParamsElementUserLocatorValue(**value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8848942ea4950fe9d0316fa727fc5ee03d80ae2dc08eec4b2cc17d4fdff1acc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument fail_test_on_cannot_locate", value=fail_test_on_cannot_locate, expected_type=type_hints["fail_test_on_cannot_locate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }
        if fail_test_on_cannot_locate is not None:
            self._values["fail_test_on_cannot_locate"] = fail_test_on_cannot_locate

    @builtins.property
    def value(self) -> "SyntheticsTestBrowserStepParamsElementUserLocatorValue":
        '''value block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#value SyntheticsTest#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast("SyntheticsTestBrowserStepParamsElementUserLocatorValue", result)

    @builtins.property
    def fail_test_on_cannot_locate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#fail_test_on_cannot_locate SyntheticsTest#fail_test_on_cannot_locate}.'''
        result = self._values.get("fail_test_on_cannot_locate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestBrowserStepParamsElementUserLocator(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestBrowserStepParamsElementUserLocatorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestBrowserStepParamsElementUserLocatorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__423845ef8ecfbccbeab5a36bdf8a046102c68fcde14d800ebd92f12d03cb5a8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putValue")
    def put_value(
        self,
        *,
        value: builtins.str,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#value SyntheticsTest#value}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}.
        '''
        value_ = SyntheticsTestBrowserStepParamsElementUserLocatorValue(
            value=value, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putValue", [value_]))

    @jsii.member(jsii_name="resetFailTestOnCannotLocate")
    def reset_fail_test_on_cannot_locate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailTestOnCannotLocate", []))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(
        self,
    ) -> "SyntheticsTestBrowserStepParamsElementUserLocatorValueOutputReference":
        return typing.cast("SyntheticsTestBrowserStepParamsElementUserLocatorValueOutputReference", jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="failTestOnCannotLocateInput")
    def fail_test_on_cannot_locate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failTestOnCannotLocateInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(
        self,
    ) -> typing.Optional["SyntheticsTestBrowserStepParamsElementUserLocatorValue"]:
        return typing.cast(typing.Optional["SyntheticsTestBrowserStepParamsElementUserLocatorValue"], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="failTestOnCannotLocate")
    def fail_test_on_cannot_locate(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failTestOnCannotLocate"))

    @fail_test_on_cannot_locate.setter
    def fail_test_on_cannot_locate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b440170022a2f749c6302066935fe7f4ff119bbd95189dbc41bca8805c0eb15e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failTestOnCannotLocate", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SyntheticsTestBrowserStepParamsElementUserLocator]:
        return typing.cast(typing.Optional[SyntheticsTestBrowserStepParamsElementUserLocator], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestBrowserStepParamsElementUserLocator],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da61494c842471b1a4d07d899542648cdf587c38d11a671d4f77d14fe1e35e3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestBrowserStepParamsElementUserLocatorValue",
    jsii_struct_bases=[],
    name_mapping={"value": "value", "type": "type"},
)
class SyntheticsTestBrowserStepParamsElementUserLocatorValue:
    def __init__(
        self,
        *,
        value: builtins.str,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#value SyntheticsTest#value}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__354c42baed2b65beec0e41a15875f555e18e99ee00b509d802d33b2272a11c11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#value SyntheticsTest#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestBrowserStepParamsElementUserLocatorValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestBrowserStepParamsElementUserLocatorValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestBrowserStepParamsElementUserLocatorValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbd46900df8cfa32cca6e4a22da5054b1bd41e993da22680f3e76f01b17b8e93)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10b6ae149fea9edc0e8e6c09d6aef69c9072cbabc920cee283926f1e539316a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d128dda7f6f5660a7a1496cf9df4128f76bcee3826e1e29fd4ed16b70cdd0436)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SyntheticsTestBrowserStepParamsElementUserLocatorValue]:
        return typing.cast(typing.Optional[SyntheticsTestBrowserStepParamsElementUserLocatorValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestBrowserStepParamsElementUserLocatorValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96e71d9b7b73087259a9931952c23180cb9cded841e184ff4bd1a474020f88f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SyntheticsTestBrowserStepParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestBrowserStepParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab273075f0ea7fcaebf406465eda6dc1091571617a96a7802ec0e0c968570269)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putElementUserLocator")
    def put_element_user_locator(
        self,
        *,
        value: typing.Union[SyntheticsTestBrowserStepParamsElementUserLocatorValue, typing.Dict[builtins.str, typing.Any]],
        fail_test_on_cannot_locate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param value: value block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#value SyntheticsTest#value}
        :param fail_test_on_cannot_locate: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#fail_test_on_cannot_locate SyntheticsTest#fail_test_on_cannot_locate}.
        '''
        value_ = SyntheticsTestBrowserStepParamsElementUserLocator(
            value=value, fail_test_on_cannot_locate=fail_test_on_cannot_locate
        )

        return typing.cast(None, jsii.invoke(self, "putElementUserLocator", [value_]))

    @jsii.member(jsii_name="putVariable")
    def put_variable(
        self,
        *,
        example: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param example: Example of the extracted variable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#example SyntheticsTest#example}
        :param name: Name of the extracted variable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#name SyntheticsTest#name}
        '''
        value = SyntheticsTestBrowserStepParamsVariable(example=example, name=name)

        return typing.cast(None, jsii.invoke(self, "putVariable", [value]))

    @jsii.member(jsii_name="resetAttribute")
    def reset_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttribute", []))

    @jsii.member(jsii_name="resetCheck")
    def reset_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCheck", []))

    @jsii.member(jsii_name="resetClickType")
    def reset_click_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClickType", []))

    @jsii.member(jsii_name="resetCode")
    def reset_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCode", []))

    @jsii.member(jsii_name="resetDelay")
    def reset_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelay", []))

    @jsii.member(jsii_name="resetElement")
    def reset_element(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElement", []))

    @jsii.member(jsii_name="resetElementUserLocator")
    def reset_element_user_locator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElementUserLocator", []))

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetFile")
    def reset_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFile", []))

    @jsii.member(jsii_name="resetFiles")
    def reset_files(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFiles", []))

    @jsii.member(jsii_name="resetModifiers")
    def reset_modifiers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModifiers", []))

    @jsii.member(jsii_name="resetPlayingTabId")
    def reset_playing_tab_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlayingTabId", []))

    @jsii.member(jsii_name="resetRequest")
    def reset_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequest", []))

    @jsii.member(jsii_name="resetSubtestPublicId")
    def reset_subtest_public_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubtestPublicId", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @jsii.member(jsii_name="resetVariable")
    def reset_variable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariable", []))

    @jsii.member(jsii_name="resetWithClick")
    def reset_with_click(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithClick", []))

    @jsii.member(jsii_name="resetX")
    def reset_x(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetX", []))

    @jsii.member(jsii_name="resetY")
    def reset_y(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetY", []))

    @builtins.property
    @jsii.member(jsii_name="elementUserLocator")
    def element_user_locator(
        self,
    ) -> SyntheticsTestBrowserStepParamsElementUserLocatorOutputReference:
        return typing.cast(SyntheticsTestBrowserStepParamsElementUserLocatorOutputReference, jsii.get(self, "elementUserLocator"))

    @builtins.property
    @jsii.member(jsii_name="variable")
    def variable(self) -> "SyntheticsTestBrowserStepParamsVariableOutputReference":
        return typing.cast("SyntheticsTestBrowserStepParamsVariableOutputReference", jsii.get(self, "variable"))

    @builtins.property
    @jsii.member(jsii_name="attributeInput")
    def attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeInput"))

    @builtins.property
    @jsii.member(jsii_name="checkInput")
    def check_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "checkInput"))

    @builtins.property
    @jsii.member(jsii_name="clickTypeInput")
    def click_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clickTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="codeInput")
    def code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codeInput"))

    @builtins.property
    @jsii.member(jsii_name="delayInput")
    def delay_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "delayInput"))

    @builtins.property
    @jsii.member(jsii_name="elementInput")
    def element_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elementInput"))

    @builtins.property
    @jsii.member(jsii_name="elementUserLocatorInput")
    def element_user_locator_input(
        self,
    ) -> typing.Optional[SyntheticsTestBrowserStepParamsElementUserLocator]:
        return typing.cast(typing.Optional[SyntheticsTestBrowserStepParamsElementUserLocator], jsii.get(self, "elementUserLocatorInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="filesInput")
    def files_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filesInput"))

    @builtins.property
    @jsii.member(jsii_name="modifiersInput")
    def modifiers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "modifiersInput"))

    @builtins.property
    @jsii.member(jsii_name="playingTabIdInput")
    def playing_tab_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "playingTabIdInput"))

    @builtins.property
    @jsii.member(jsii_name="requestInput")
    def request_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestInput"))

    @builtins.property
    @jsii.member(jsii_name="subtestPublicIdInput")
    def subtest_public_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subtestPublicIdInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="variableInput")
    def variable_input(
        self,
    ) -> typing.Optional["SyntheticsTestBrowserStepParamsVariable"]:
        return typing.cast(typing.Optional["SyntheticsTestBrowserStepParamsVariable"], jsii.get(self, "variableInput"))

    @builtins.property
    @jsii.member(jsii_name="withClickInput")
    def with_click_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "withClickInput"))

    @builtins.property
    @jsii.member(jsii_name="xInput")
    def x_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "xInput"))

    @builtins.property
    @jsii.member(jsii_name="yInput")
    def y_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yInput"))

    @builtins.property
    @jsii.member(jsii_name="attribute")
    def attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attribute"))

    @attribute.setter
    def attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12d305220aadd56a3f48ccfb5de5d3d84860f23280e654ae7999e6bd54cf3147)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attribute", value)

    @builtins.property
    @jsii.member(jsii_name="check")
    def check(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "check"))

    @check.setter
    def check(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef0b0e62d9e8e603295b4fe29be2c5cb204dd945d5675552b899f82c649b47b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "check", value)

    @builtins.property
    @jsii.member(jsii_name="clickType")
    def click_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clickType"))

    @click_type.setter
    def click_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7f055399751e5b8b826b9b757a528edc8edde497078270b86a7aef15238df84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clickType", value)

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "code"))

    @code.setter
    def code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84d9dd433445fc803262bf4f9120dd65ae195ea2f9e692bfc2b7929dbceac895)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "code", value)

    @builtins.property
    @jsii.member(jsii_name="delay")
    def delay(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "delay"))

    @delay.setter
    def delay(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46bcad933b2dcd02890faaad4bc1b695f8a10bec3181ddb92cd250023e8a4c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delay", value)

    @builtins.property
    @jsii.member(jsii_name="element")
    def element(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "element"))

    @element.setter
    def element(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f2446a91058afcc1373344a7c27cacdb93c9d81351d9b7fe72df9585f8d7d6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "element", value)

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c43e9fddf4adefb4f643a32b6973cb6bc19f3022cf393f94c2facf475cb3c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value)

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "file"))

    @file.setter
    def file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__408db7762ac587d57b63224d404f80645f727b6ff93197dfdaa40bfcc673b234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "file", value)

    @builtins.property
    @jsii.member(jsii_name="files")
    def files(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "files"))

    @files.setter
    def files(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__808e6b76cc2a0a1ccd6aef422b5c4366f57a975227f626410afb5c720ea30f79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "files", value)

    @builtins.property
    @jsii.member(jsii_name="modifiers")
    def modifiers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "modifiers"))

    @modifiers.setter
    def modifiers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__743ab67f37f6996eccd110c51fde4e78c76102c0c29e9e17db2962b156eb6d05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modifiers", value)

    @builtins.property
    @jsii.member(jsii_name="playingTabId")
    def playing_tab_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "playingTabId"))

    @playing_tab_id.setter
    def playing_tab_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__968d86286b4914ab0e29dd2dc7a6605e9fc94514d743094e17ade549ab287b89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "playingTabId", value)

    @builtins.property
    @jsii.member(jsii_name="request")
    def request(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "request"))

    @request.setter
    def request(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bca409249f67d08abaf9760f86beb737fbef47963cd7132fbae3c0de88adf64c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "request", value)

    @builtins.property
    @jsii.member(jsii_name="subtestPublicId")
    def subtest_public_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subtestPublicId"))

    @subtest_public_id.setter
    def subtest_public_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ba6377caad7c5f24fa946db7d904dc60e5cebfa006675343c6c1ad513a84841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subtestPublicId", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df2abf4a4994c6b4a00dcc45c65fedeca495df411ba477ad4c38678f7e709acb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="withClick")
    def with_click(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "withClick"))

    @with_click.setter
    def with_click(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__216faeb1182592eb5c29060719b5e34cd03d9b9d46c8f42169df8e6b8181a546)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withClick", value)

    @builtins.property
    @jsii.member(jsii_name="x")
    def x(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "x"))

    @x.setter
    def x(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1f30b20f516acee825f40b0217bff49ffe46857cfd32df753e89735c74e4b90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "x", value)

    @builtins.property
    @jsii.member(jsii_name="y")
    def y(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "y"))

    @y.setter
    def y(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9ccbca395b62a0d30d7c03c46958e05ca5a18b92662637a6e397dbc5d17a38e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "y", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SyntheticsTestBrowserStepParams]:
        return typing.cast(typing.Optional[SyntheticsTestBrowserStepParams], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestBrowserStepParams],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dfd0b1c86e04ddfb827046b19b8d74dbbc8c1b8e69caca8f9f8f4da4607f7da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestBrowserStepParamsVariable",
    jsii_struct_bases=[],
    name_mapping={"example": "example", "name": "name"},
)
class SyntheticsTestBrowserStepParamsVariable:
    def __init__(
        self,
        *,
        example: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param example: Example of the extracted variable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#example SyntheticsTest#example}
        :param name: Name of the extracted variable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#name SyntheticsTest#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5905942d5b76c4cbe0b6d4672c950c27c4cf4ee3b85dfc9069a6d67b4f1a3dc)
            check_type(argname="argument example", value=example, expected_type=type_hints["example"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if example is not None:
            self._values["example"] = example
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def example(self) -> typing.Optional[builtins.str]:
        '''Example of the extracted variable.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#example SyntheticsTest#example}
        '''
        result = self._values.get("example")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the extracted variable.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#name SyntheticsTest#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestBrowserStepParamsVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestBrowserStepParamsVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestBrowserStepParamsVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8287eaef396e286cca42d0dee07f04c5d4959ff2c4268038f13c7c45f536619d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExample")
    def reset_example(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExample", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="exampleInput")
    def example_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exampleInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="example")
    def example(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "example"))

    @example.setter
    def example(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63d518bc24c6bae7be7f778f2fb2ca36733d8a51925a56ba668b9b6e800549cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "example", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a8ba732d65a17e139a0fbae04a115b9b74cb2fbdfeff60840068dcbf41c44a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SyntheticsTestBrowserStepParamsVariable]:
        return typing.cast(typing.Optional[SyntheticsTestBrowserStepParamsVariable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestBrowserStepParamsVariable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f95a65cfb4627f11df2e57ec738d34dbdcd735a11c033ddb05c67f827e6fdf05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestBrowserVariable",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "type": "type",
        "example": "example",
        "id": "id",
        "pattern": "pattern",
    },
)
class SyntheticsTestBrowserVariable:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        example: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        pattern: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the variable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#name SyntheticsTest#name}
        :param type: Type of browser test variable. Valid values are ``element``, ``email``, ``global``, ``javascript``, ``text``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        :param example: Example for the variable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#example SyntheticsTest#example}
        :param id: ID of the global variable to use. This is actually only used (and required) in the case of using a variable of type ``global``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#id SyntheticsTest#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param pattern: Pattern of the variable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#pattern SyntheticsTest#pattern}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d0aa4fe874f2e5ba5ae360f344c13b5104fb4eba24a6a54f4992aa80c4a168b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument example", value=example, expected_type=type_hints["example"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }
        if example is not None:
            self._values["example"] = example
        if id is not None:
            self._values["id"] = id
        if pattern is not None:
            self._values["pattern"] = pattern

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the variable.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#name SyntheticsTest#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of browser test variable. Valid values are ``element``, ``email``, ``global``, ``javascript``, ``text``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def example(self) -> typing.Optional[builtins.str]:
        '''Example for the variable.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#example SyntheticsTest#example}
        '''
        result = self._values.get("example")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''ID of the global variable to use.

        This is actually only used (and required) in the case of using a variable of type ``global``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#id SyntheticsTest#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pattern(self) -> typing.Optional[builtins.str]:
        '''Pattern of the variable.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#pattern SyntheticsTest#pattern}
        '''
        result = self._values.get("pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestBrowserVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestBrowserVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestBrowserVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1b002a2a3aaa14b3c5bc79edc6ae7a7a2bf29ff25022c3f95333801d67443c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SyntheticsTestBrowserVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44f19aee4b2a491e15a397468de2f906eb3da9618b754fca07f8c631a8e71cc3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SyntheticsTestBrowserVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f872764b7cc5b5bfaa56ec1d3f90f994ab1bf35d278d895c4fe1c384c6baec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae7b7e5248a7803e8a01069889b0512599d5a912ba0181455797220e3cd75a8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__415931a750780f3980c507a1bc0ac2058bf664f6647b7d01b08a4f6e3cce06d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestBrowserVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestBrowserVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestBrowserVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d1953e929a96086009a59ed23f2040f4c073edf5842cc1d153085c88f849d89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SyntheticsTestBrowserVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestBrowserVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b04fbc27bef9bbdcafe5a62b3e1d64cc27109f58b7ac1229b9fdf8ab815f5b50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExample")
    def reset_example(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExample", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPattern")
    def reset_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPattern", []))

    @builtins.property
    @jsii.member(jsii_name="exampleInput")
    def example_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exampleInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="example")
    def example(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "example"))

    @example.setter
    def example(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5ae2055780951f59b884518c8346f6c788e8b3d68ef4c26b780c4a1b213e37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "example", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d66fb5f6e38bff66acfeb3045151b08ddd10dfe1cab3c5cdac7e21fc87880bf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e80486ee4e75f8962f31659133729d3f2b40d2edda5a92c3b40668b85b9c637d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6cae8e08beca20df2edd49e4a4180f6952a24a85aa57b64f621758aac328596)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96f2c9687923ddc9d146ff68bf131159b41ef1847b3fcb67817eb5ef4378b0bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SyntheticsTestBrowserVariable, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SyntheticsTestBrowserVariable, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SyntheticsTestBrowserVariable, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__639aea83478bb9a62d10bf266b222833df27e9eaf7e919d0c5b521a8b4246ed3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "locations": "locations",
        "name": "name",
        "status": "status",
        "type": "type",
        "api_step": "apiStep",
        "assertion": "assertion",
        "browser_step": "browserStep",
        "browser_variable": "browserVariable",
        "config_variable": "configVariable",
        "device_ids": "deviceIds",
        "id": "id",
        "message": "message",
        "options_list": "optionsList",
        "request_basicauth": "requestBasicauth",
        "request_client_certificate": "requestClientCertificate",
        "request_definition": "requestDefinition",
        "request_headers": "requestHeaders",
        "request_proxy": "requestProxy",
        "request_query": "requestQuery",
        "set_cookie": "setCookie",
        "subtype": "subtype",
        "tags": "tags",
    },
)
class SyntheticsTestConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        locations: typing.Sequence[builtins.str],
        name: builtins.str,
        status: builtins.str,
        type: builtins.str,
        api_step: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestApiStep, typing.Dict[builtins.str, typing.Any]]]]] = None,
        assertion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestAssertion, typing.Dict[builtins.str, typing.Any]]]]] = None,
        browser_step: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestBrowserStep, typing.Dict[builtins.str, typing.Any]]]]] = None,
        browser_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestBrowserVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
        config_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsTestConfigVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        device_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        message: typing.Optional[builtins.str] = None,
        options_list: typing.Optional[typing.Union["SyntheticsTestOptionsList", typing.Dict[builtins.str, typing.Any]]] = None,
        request_basicauth: typing.Optional[typing.Union["SyntheticsTestRequestBasicauth", typing.Dict[builtins.str, typing.Any]]] = None,
        request_client_certificate: typing.Optional[typing.Union["SyntheticsTestRequestClientCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        request_definition: typing.Optional[typing.Union["SyntheticsTestRequestDefinition", typing.Dict[builtins.str, typing.Any]]] = None,
        request_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        request_proxy: typing.Optional[typing.Union["SyntheticsTestRequestProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        request_query: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        set_cookie: typing.Optional[builtins.str] = None,
        subtype: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param locations: Array of locations used to run the test. Refer to `the Datadog Synthetics location data source <https://registry.terraform.io/providers/DataDog/datadog/latest/docs/data-sources/synthetics_locations>`_ to retrieve the list of locations. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#locations SyntheticsTest#locations}
        :param name: Name of Datadog synthetics test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#name SyntheticsTest#name}
        :param status: Define whether you want to start (``live``) or pause (``paused``) a Synthetic test. Valid values are ``live``, ``paused``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#status SyntheticsTest#status}
        :param type: Synthetics test type. Valid values are ``api``, ``browser``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        :param api_step: api_step block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#api_step SyntheticsTest#api_step}
        :param assertion: assertion block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#assertion SyntheticsTest#assertion}
        :param browser_step: browser_step block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#browser_step SyntheticsTest#browser_step}
        :param browser_variable: browser_variable block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#browser_variable SyntheticsTest#browser_variable}
        :param config_variable: config_variable block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#config_variable SyntheticsTest#config_variable}
        :param device_ids: Required if ``type = "browser"``. Array with the different device IDs used to run the test. Valid values are ``laptop_large``, ``tablet``, ``mobile_small``, ``chrome.laptop_large``, ``chrome.tablet``, ``chrome.mobile_small``, ``firefox.laptop_large``, ``firefox.tablet``, ``firefox.mobile_small``, ``edge.laptop_large``, ``edge.tablet``, ``edge.mobile_small``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#device_ids SyntheticsTest#device_ids}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#id SyntheticsTest#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param message: A message to include with notifications for this synthetics test. Email notifications can be sent to specific users by using the same ``@username`` notation as events. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#message SyntheticsTest#message}
        :param options_list: options_list block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#options_list SyntheticsTest#options_list}
        :param request_basicauth: request_basicauth block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_basicauth SyntheticsTest#request_basicauth}
        :param request_client_certificate: request_client_certificate block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_client_certificate SyntheticsTest#request_client_certificate}
        :param request_definition: request_definition block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_definition SyntheticsTest#request_definition}
        :param request_headers: Header name and value map. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_headers SyntheticsTest#request_headers}
        :param request_proxy: request_proxy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_proxy SyntheticsTest#request_proxy}
        :param request_query: Query arguments name and value map. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_query SyntheticsTest#request_query}
        :param set_cookie: Cookies to be used for a browser test request, using the `Set-Cookie <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie>`_ syntax. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#set_cookie SyntheticsTest#set_cookie}
        :param subtype: The subtype of the Synthetic API test. Defaults to ``http``. Valid values are ``http``, ``ssl``, ``tcp``, ``dns``, ``multi``, ``icmp``, ``udp``, ``websocket``, ``grpc``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#subtype SyntheticsTest#subtype}
        :param tags: A list of tags to associate with your synthetics test. This can help you categorize and filter tests in the manage synthetics page of the UI. Default is an empty list (``[]``). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#tags SyntheticsTest#tags}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(options_list, dict):
            options_list = SyntheticsTestOptionsList(**options_list)
        if isinstance(request_basicauth, dict):
            request_basicauth = SyntheticsTestRequestBasicauth(**request_basicauth)
        if isinstance(request_client_certificate, dict):
            request_client_certificate = SyntheticsTestRequestClientCertificate(**request_client_certificate)
        if isinstance(request_definition, dict):
            request_definition = SyntheticsTestRequestDefinition(**request_definition)
        if isinstance(request_proxy, dict):
            request_proxy = SyntheticsTestRequestProxy(**request_proxy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0124c6c0dcd84fb2da5fd40130e734693b855c839f751073a8186ebff14a8481)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument api_step", value=api_step, expected_type=type_hints["api_step"])
            check_type(argname="argument assertion", value=assertion, expected_type=type_hints["assertion"])
            check_type(argname="argument browser_step", value=browser_step, expected_type=type_hints["browser_step"])
            check_type(argname="argument browser_variable", value=browser_variable, expected_type=type_hints["browser_variable"])
            check_type(argname="argument config_variable", value=config_variable, expected_type=type_hints["config_variable"])
            check_type(argname="argument device_ids", value=device_ids, expected_type=type_hints["device_ids"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument options_list", value=options_list, expected_type=type_hints["options_list"])
            check_type(argname="argument request_basicauth", value=request_basicauth, expected_type=type_hints["request_basicauth"])
            check_type(argname="argument request_client_certificate", value=request_client_certificate, expected_type=type_hints["request_client_certificate"])
            check_type(argname="argument request_definition", value=request_definition, expected_type=type_hints["request_definition"])
            check_type(argname="argument request_headers", value=request_headers, expected_type=type_hints["request_headers"])
            check_type(argname="argument request_proxy", value=request_proxy, expected_type=type_hints["request_proxy"])
            check_type(argname="argument request_query", value=request_query, expected_type=type_hints["request_query"])
            check_type(argname="argument set_cookie", value=set_cookie, expected_type=type_hints["set_cookie"])
            check_type(argname="argument subtype", value=subtype, expected_type=type_hints["subtype"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "locations": locations,
            "name": name,
            "status": status,
            "type": type,
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
        if api_step is not None:
            self._values["api_step"] = api_step
        if assertion is not None:
            self._values["assertion"] = assertion
        if browser_step is not None:
            self._values["browser_step"] = browser_step
        if browser_variable is not None:
            self._values["browser_variable"] = browser_variable
        if config_variable is not None:
            self._values["config_variable"] = config_variable
        if device_ids is not None:
            self._values["device_ids"] = device_ids
        if id is not None:
            self._values["id"] = id
        if message is not None:
            self._values["message"] = message
        if options_list is not None:
            self._values["options_list"] = options_list
        if request_basicauth is not None:
            self._values["request_basicauth"] = request_basicauth
        if request_client_certificate is not None:
            self._values["request_client_certificate"] = request_client_certificate
        if request_definition is not None:
            self._values["request_definition"] = request_definition
        if request_headers is not None:
            self._values["request_headers"] = request_headers
        if request_proxy is not None:
            self._values["request_proxy"] = request_proxy
        if request_query is not None:
            self._values["request_query"] = request_query
        if set_cookie is not None:
            self._values["set_cookie"] = set_cookie
        if subtype is not None:
            self._values["subtype"] = subtype
        if tags is not None:
            self._values["tags"] = tags

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
    def locations(self) -> typing.List[builtins.str]:
        '''Array of locations used to run the test.

        Refer to `the Datadog Synthetics location data source <https://registry.terraform.io/providers/DataDog/datadog/latest/docs/data-sources/synthetics_locations>`_ to retrieve the list of locations.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#locations SyntheticsTest#locations}
        '''
        result = self._values.get("locations")
        assert result is not None, "Required property 'locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of Datadog synthetics test.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#name SyntheticsTest#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def status(self) -> builtins.str:
        '''Define whether you want to start (``live``) or pause (``paused``) a Synthetic test. Valid values are ``live``, ``paused``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#status SyntheticsTest#status}
        '''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Synthetics test type. Valid values are ``api``, ``browser``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_step(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestApiStep]]]:
        '''api_step block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#api_step SyntheticsTest#api_step}
        '''
        result = self._values.get("api_step")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestApiStep]]], result)

    @builtins.property
    def assertion(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestAssertion]]]:
        '''assertion block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#assertion SyntheticsTest#assertion}
        '''
        result = self._values.get("assertion")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestAssertion]]], result)

    @builtins.property
    def browser_step(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestBrowserStep]]]:
        '''browser_step block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#browser_step SyntheticsTest#browser_step}
        '''
        result = self._values.get("browser_step")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestBrowserStep]]], result)

    @builtins.property
    def browser_variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestBrowserVariable]]]:
        '''browser_variable block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#browser_variable SyntheticsTest#browser_variable}
        '''
        result = self._values.get("browser_variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestBrowserVariable]]], result)

    @builtins.property
    def config_variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsTestConfigVariable"]]]:
        '''config_variable block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#config_variable SyntheticsTest#config_variable}
        '''
        result = self._values.get("config_variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsTestConfigVariable"]]], result)

    @builtins.property
    def device_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Required if ``type = "browser"``.

        Array with the different device IDs used to run the test. Valid values are ``laptop_large``, ``tablet``, ``mobile_small``, ``chrome.laptop_large``, ``chrome.tablet``, ``chrome.mobile_small``, ``firefox.laptop_large``, ``firefox.tablet``, ``firefox.mobile_small``, ``edge.laptop_large``, ``edge.tablet``, ``edge.mobile_small``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#device_ids SyntheticsTest#device_ids}
        '''
        result = self._values.get("device_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#id SyntheticsTest#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''A message to include with notifications for this synthetics test.

        Email notifications can be sent to specific users by using the same ``@username`` notation as events.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#message SyntheticsTest#message}
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def options_list(self) -> typing.Optional["SyntheticsTestOptionsList"]:
        '''options_list block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#options_list SyntheticsTest#options_list}
        '''
        result = self._values.get("options_list")
        return typing.cast(typing.Optional["SyntheticsTestOptionsList"], result)

    @builtins.property
    def request_basicauth(self) -> typing.Optional["SyntheticsTestRequestBasicauth"]:
        '''request_basicauth block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_basicauth SyntheticsTest#request_basicauth}
        '''
        result = self._values.get("request_basicauth")
        return typing.cast(typing.Optional["SyntheticsTestRequestBasicauth"], result)

    @builtins.property
    def request_client_certificate(
        self,
    ) -> typing.Optional["SyntheticsTestRequestClientCertificate"]:
        '''request_client_certificate block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_client_certificate SyntheticsTest#request_client_certificate}
        '''
        result = self._values.get("request_client_certificate")
        return typing.cast(typing.Optional["SyntheticsTestRequestClientCertificate"], result)

    @builtins.property
    def request_definition(self) -> typing.Optional["SyntheticsTestRequestDefinition"]:
        '''request_definition block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_definition SyntheticsTest#request_definition}
        '''
        result = self._values.get("request_definition")
        return typing.cast(typing.Optional["SyntheticsTestRequestDefinition"], result)

    @builtins.property
    def request_headers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Header name and value map.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_headers SyntheticsTest#request_headers}
        '''
        result = self._values.get("request_headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def request_proxy(self) -> typing.Optional["SyntheticsTestRequestProxy"]:
        '''request_proxy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_proxy SyntheticsTest#request_proxy}
        '''
        result = self._values.get("request_proxy")
        return typing.cast(typing.Optional["SyntheticsTestRequestProxy"], result)

    @builtins.property
    def request_query(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Query arguments name and value map.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#request_query SyntheticsTest#request_query}
        '''
        result = self._values.get("request_query")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def set_cookie(self) -> typing.Optional[builtins.str]:
        '''Cookies to be used for a browser test request, using the `Set-Cookie <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie>`_ syntax.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#set_cookie SyntheticsTest#set_cookie}
        '''
        result = self._values.get("set_cookie")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subtype(self) -> typing.Optional[builtins.str]:
        '''The subtype of the Synthetic API test.

        Defaults to ``http``. Valid values are ``http``, ``ssl``, ``tcp``, ``dns``, ``multi``, ``icmp``, ``udp``, ``websocket``, ``grpc``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#subtype SyntheticsTest#subtype}
        '''
        result = self._values.get("subtype")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of tags to associate with your synthetics test.

        This can help you categorize and filter tests in the manage synthetics page of the UI. Default is an empty list (``[]``).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#tags SyntheticsTest#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestConfigVariable",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "type": "type",
        "example": "example",
        "id": "id",
        "pattern": "pattern",
        "secure": "secure",
    },
)
class SyntheticsTestConfigVariable:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        example: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        pattern: typing.Optional[builtins.str] = None,
        secure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Name of the variable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#name SyntheticsTest#name}
        :param type: Type of test configuration variable. Valid values are ``global``, ``text``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        :param example: Example for the variable. This value is not returned by the api when ``secure = true``. Avoid drift by only making updates to this value from within Terraform. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#example SyntheticsTest#example}
        :param id: When type = ``global``, ID of the global variable to use. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#id SyntheticsTest#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param pattern: Pattern of the variable. This value is not returned by the api when ``secure = true``. Avoid drift by only making updates to this value from within Terraform. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#pattern SyntheticsTest#pattern}
        :param secure: Whether the value of this variable will be obfuscated in test results. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#secure SyntheticsTest#secure}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc81652e39c08ef70de8f9af7578b19d8491953961a9b658d4cd4ce1513ad980)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument example", value=example, expected_type=type_hints["example"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument secure", value=secure, expected_type=type_hints["secure"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }
        if example is not None:
            self._values["example"] = example
        if id is not None:
            self._values["id"] = id
        if pattern is not None:
            self._values["pattern"] = pattern
        if secure is not None:
            self._values["secure"] = secure

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the variable.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#name SyntheticsTest#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of test configuration variable. Valid values are ``global``, ``text``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def example(self) -> typing.Optional[builtins.str]:
        '''Example for the variable.

        This value is not returned by the api when ``secure = true``. Avoid drift by only making updates to this value from within Terraform.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#example SyntheticsTest#example}
        '''
        result = self._values.get("example")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''When type = ``global``, ID of the global variable to use.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#id SyntheticsTest#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pattern(self) -> typing.Optional[builtins.str]:
        '''Pattern of the variable.

        This value is not returned by the api when ``secure = true``. Avoid drift by only making updates to this value from within Terraform.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#pattern SyntheticsTest#pattern}
        '''
        result = self._values.get("pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the value of this variable will be obfuscated in test results.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#secure SyntheticsTest#secure}
        '''
        result = self._values.get("secure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestConfigVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestConfigVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestConfigVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdfb6ee78af081f7330a2703987d1a54b7951102c14a1dea49070faaf318a8fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SyntheticsTestConfigVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9915db1bde04681fe11a56bd209848ae0ab852575c9620f93ef114ec5ef226c5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SyntheticsTestConfigVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a40a387de5d8ffeebbde70cdef575dd47b1c8eb2759103e04b3975e256bd50f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91827bb9499c63cc4e8e2c3c67bf69fe76a1b3641cd78c7f510fec0843532fd5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8c9c9c17d582b09a5ae428cd456fb2565e32b6e9bbaae90da30e71ec725ccce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestConfigVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestConfigVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestConfigVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab406c2b919858e8dae21f82430aef3c902cd567e5a50ea9ab5a287823628c20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SyntheticsTestConfigVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestConfigVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34cc0e71b634067cc4f9796dc84c967f0557380898f91aeed3a7a6690f71ae20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExample")
    def reset_example(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExample", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPattern")
    def reset_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPattern", []))

    @jsii.member(jsii_name="resetSecure")
    def reset_secure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecure", []))

    @builtins.property
    @jsii.member(jsii_name="exampleInput")
    def example_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exampleInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="secureInput")
    def secure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "secureInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="example")
    def example(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "example"))

    @example.setter
    def example(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdf651112d71ebeec49217eb92719718e46f89ec3e300218f5bddb4eba71d9c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "example", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__040c59b88e79d1a92cfa4503e4443913ca2febc2d744149ebd006987aa4dd2f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83cba13412184e314f736f37ca293e3a5624e76ee5c536faa0c88fee44af069b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__774ea0cdfdbc2cdbd9919609f1b76e90e49cde88647115c20b86c4d6699b27e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value)

    @builtins.property
    @jsii.member(jsii_name="secure")
    def secure(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "secure"))

    @secure.setter
    def secure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e068641b65ab84e0b5171344cab1014834825ca36e99ec8434c9d0051b39928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secure", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84b369c8315ccc4927e11b51545d75035789c41a7b6177221923af78c0f5508e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SyntheticsTestConfigVariable, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SyntheticsTestConfigVariable, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SyntheticsTestConfigVariable, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b444e981176453dd5e922485f7598e82982d7d82eac74baa256f9087a7387d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestOptionsList",
    jsii_struct_bases=[],
    name_mapping={
        "tick_every": "tickEvery",
        "accept_self_signed": "acceptSelfSigned",
        "allow_insecure": "allowInsecure",
        "check_certificate_revocation": "checkCertificateRevocation",
        "ci": "ci",
        "disable_cors": "disableCors",
        "disable_csp": "disableCsp",
        "follow_redirects": "followRedirects",
        "ignore_server_certificate_error": "ignoreServerCertificateError",
        "initial_navigation_timeout": "initialNavigationTimeout",
        "min_failure_duration": "minFailureDuration",
        "min_location_failed": "minLocationFailed",
        "monitor_name": "monitorName",
        "monitor_options": "monitorOptions",
        "monitor_priority": "monitorPriority",
        "no_screenshot": "noScreenshot",
        "restricted_roles": "restrictedRoles",
        "retry": "retry",
        "rum_settings": "rumSettings",
    },
)
class SyntheticsTestOptionsList:
    def __init__(
        self,
        *,
        tick_every: jsii.Number,
        accept_self_signed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        check_certificate_revocation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ci: typing.Optional[typing.Union["SyntheticsTestOptionsListCi", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_cors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_csp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        follow_redirects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ignore_server_certificate_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        initial_navigation_timeout: typing.Optional[jsii.Number] = None,
        min_failure_duration: typing.Optional[jsii.Number] = None,
        min_location_failed: typing.Optional[jsii.Number] = None,
        monitor_name: typing.Optional[builtins.str] = None,
        monitor_options: typing.Optional[typing.Union["SyntheticsTestOptionsListMonitorOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor_priority: typing.Optional[jsii.Number] = None,
        no_screenshot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restricted_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        retry: typing.Optional[typing.Union["SyntheticsTestOptionsListRetry", typing.Dict[builtins.str, typing.Any]]] = None,
        rum_settings: typing.Optional[typing.Union["SyntheticsTestOptionsListRumSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param tick_every: How often the test should run (in seconds). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#tick_every SyntheticsTest#tick_every}
        :param accept_self_signed: For SSL test, whether or not the test should allow self signed certificates. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#accept_self_signed SyntheticsTest#accept_self_signed}
        :param allow_insecure: Allows loading insecure content for an HTTP test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#allow_insecure SyntheticsTest#allow_insecure}
        :param check_certificate_revocation: For SSL test, whether or not the test should fail on revoked certificate in stapled OCSP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#check_certificate_revocation SyntheticsTest#check_certificate_revocation}
        :param ci: ci block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#ci SyntheticsTest#ci}
        :param disable_cors: Disable Cross-Origin Resource Sharing for browser tests. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#disable_cors SyntheticsTest#disable_cors}
        :param disable_csp: Disable Content Security Policy for browser tests. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#disable_csp SyntheticsTest#disable_csp}
        :param follow_redirects: Determines whether or not the API HTTP test should follow redirects. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#follow_redirects SyntheticsTest#follow_redirects}
        :param ignore_server_certificate_error: Ignore server certificate error. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#ignore_server_certificate_error SyntheticsTest#ignore_server_certificate_error}
        :param initial_navigation_timeout: Timeout before declaring the initial step as failed (in seconds) for browser tests. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#initial_navigation_timeout SyntheticsTest#initial_navigation_timeout}
        :param min_failure_duration: Minimum amount of time in failure required to trigger an alert. Default is ``0``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#min_failure_duration SyntheticsTest#min_failure_duration}
        :param min_location_failed: Minimum number of locations in failure required to trigger an alert. Default is ``1``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#min_location_failed SyntheticsTest#min_location_failed}
        :param monitor_name: The monitor name is used for the alert title as well as for all monitor dashboard widgets and SLOs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#monitor_name SyntheticsTest#monitor_name}
        :param monitor_options: monitor_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#monitor_options SyntheticsTest#monitor_options}
        :param monitor_priority: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#monitor_priority SyntheticsTest#monitor_priority}.
        :param no_screenshot: Prevents saving screenshots of the steps. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#no_screenshot SyntheticsTest#no_screenshot}
        :param restricted_roles: A list of role identifiers pulled from the Roles API to restrict read and write access. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#restricted_roles SyntheticsTest#restricted_roles}
        :param retry: retry block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#retry SyntheticsTest#retry}
        :param rum_settings: rum_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#rum_settings SyntheticsTest#rum_settings}
        '''
        if isinstance(ci, dict):
            ci = SyntheticsTestOptionsListCi(**ci)
        if isinstance(monitor_options, dict):
            monitor_options = SyntheticsTestOptionsListMonitorOptions(**monitor_options)
        if isinstance(retry, dict):
            retry = SyntheticsTestOptionsListRetry(**retry)
        if isinstance(rum_settings, dict):
            rum_settings = SyntheticsTestOptionsListRumSettings(**rum_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__669a64b0c857b3913f6e1304a3b7506ac7351d32b12a1e69230b0fd453c12cb3)
            check_type(argname="argument tick_every", value=tick_every, expected_type=type_hints["tick_every"])
            check_type(argname="argument accept_self_signed", value=accept_self_signed, expected_type=type_hints["accept_self_signed"])
            check_type(argname="argument allow_insecure", value=allow_insecure, expected_type=type_hints["allow_insecure"])
            check_type(argname="argument check_certificate_revocation", value=check_certificate_revocation, expected_type=type_hints["check_certificate_revocation"])
            check_type(argname="argument ci", value=ci, expected_type=type_hints["ci"])
            check_type(argname="argument disable_cors", value=disable_cors, expected_type=type_hints["disable_cors"])
            check_type(argname="argument disable_csp", value=disable_csp, expected_type=type_hints["disable_csp"])
            check_type(argname="argument follow_redirects", value=follow_redirects, expected_type=type_hints["follow_redirects"])
            check_type(argname="argument ignore_server_certificate_error", value=ignore_server_certificate_error, expected_type=type_hints["ignore_server_certificate_error"])
            check_type(argname="argument initial_navigation_timeout", value=initial_navigation_timeout, expected_type=type_hints["initial_navigation_timeout"])
            check_type(argname="argument min_failure_duration", value=min_failure_duration, expected_type=type_hints["min_failure_duration"])
            check_type(argname="argument min_location_failed", value=min_location_failed, expected_type=type_hints["min_location_failed"])
            check_type(argname="argument monitor_name", value=monitor_name, expected_type=type_hints["monitor_name"])
            check_type(argname="argument monitor_options", value=monitor_options, expected_type=type_hints["monitor_options"])
            check_type(argname="argument monitor_priority", value=monitor_priority, expected_type=type_hints["monitor_priority"])
            check_type(argname="argument no_screenshot", value=no_screenshot, expected_type=type_hints["no_screenshot"])
            check_type(argname="argument restricted_roles", value=restricted_roles, expected_type=type_hints["restricted_roles"])
            check_type(argname="argument retry", value=retry, expected_type=type_hints["retry"])
            check_type(argname="argument rum_settings", value=rum_settings, expected_type=type_hints["rum_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tick_every": tick_every,
        }
        if accept_self_signed is not None:
            self._values["accept_self_signed"] = accept_self_signed
        if allow_insecure is not None:
            self._values["allow_insecure"] = allow_insecure
        if check_certificate_revocation is not None:
            self._values["check_certificate_revocation"] = check_certificate_revocation
        if ci is not None:
            self._values["ci"] = ci
        if disable_cors is not None:
            self._values["disable_cors"] = disable_cors
        if disable_csp is not None:
            self._values["disable_csp"] = disable_csp
        if follow_redirects is not None:
            self._values["follow_redirects"] = follow_redirects
        if ignore_server_certificate_error is not None:
            self._values["ignore_server_certificate_error"] = ignore_server_certificate_error
        if initial_navigation_timeout is not None:
            self._values["initial_navigation_timeout"] = initial_navigation_timeout
        if min_failure_duration is not None:
            self._values["min_failure_duration"] = min_failure_duration
        if min_location_failed is not None:
            self._values["min_location_failed"] = min_location_failed
        if monitor_name is not None:
            self._values["monitor_name"] = monitor_name
        if monitor_options is not None:
            self._values["monitor_options"] = monitor_options
        if monitor_priority is not None:
            self._values["monitor_priority"] = monitor_priority
        if no_screenshot is not None:
            self._values["no_screenshot"] = no_screenshot
        if restricted_roles is not None:
            self._values["restricted_roles"] = restricted_roles
        if retry is not None:
            self._values["retry"] = retry
        if rum_settings is not None:
            self._values["rum_settings"] = rum_settings

    @builtins.property
    def tick_every(self) -> jsii.Number:
        '''How often the test should run (in seconds).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#tick_every SyntheticsTest#tick_every}
        '''
        result = self._values.get("tick_every")
        assert result is not None, "Required property 'tick_every' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def accept_self_signed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''For SSL test, whether or not the test should allow self signed certificates.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#accept_self_signed SyntheticsTest#accept_self_signed}
        '''
        result = self._values.get("accept_self_signed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allows loading insecure content for an HTTP test.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#allow_insecure SyntheticsTest#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def check_certificate_revocation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''For SSL test, whether or not the test should fail on revoked certificate in stapled OCSP.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#check_certificate_revocation SyntheticsTest#check_certificate_revocation}
        '''
        result = self._values.get("check_certificate_revocation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ci(self) -> typing.Optional["SyntheticsTestOptionsListCi"]:
        '''ci block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#ci SyntheticsTest#ci}
        '''
        result = self._values.get("ci")
        return typing.cast(typing.Optional["SyntheticsTestOptionsListCi"], result)

    @builtins.property
    def disable_cors(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable Cross-Origin Resource Sharing for browser tests.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#disable_cors SyntheticsTest#disable_cors}
        '''
        result = self._values.get("disable_cors")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_csp(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable Content Security Policy for browser tests.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#disable_csp SyntheticsTest#disable_csp}
        '''
        result = self._values.get("disable_csp")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def follow_redirects(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether or not the API HTTP test should follow redirects.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#follow_redirects SyntheticsTest#follow_redirects}
        '''
        result = self._values.get("follow_redirects")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ignore_server_certificate_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ignore server certificate error.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#ignore_server_certificate_error SyntheticsTest#ignore_server_certificate_error}
        '''
        result = self._values.get("ignore_server_certificate_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def initial_navigation_timeout(self) -> typing.Optional[jsii.Number]:
        '''Timeout before declaring the initial step as failed (in seconds) for browser tests.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#initial_navigation_timeout SyntheticsTest#initial_navigation_timeout}
        '''
        result = self._values.get("initial_navigation_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_failure_duration(self) -> typing.Optional[jsii.Number]:
        '''Minimum amount of time in failure required to trigger an alert. Default is ``0``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#min_failure_duration SyntheticsTest#min_failure_duration}
        '''
        result = self._values.get("min_failure_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_location_failed(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of locations in failure required to trigger an alert. Default is ``1``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#min_location_failed SyntheticsTest#min_location_failed}
        '''
        result = self._values.get("min_location_failed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def monitor_name(self) -> typing.Optional[builtins.str]:
        '''The monitor name is used for the alert title as well as for all monitor dashboard widgets and SLOs.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#monitor_name SyntheticsTest#monitor_name}
        '''
        result = self._values.get("monitor_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitor_options(
        self,
    ) -> typing.Optional["SyntheticsTestOptionsListMonitorOptions"]:
        '''monitor_options block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#monitor_options SyntheticsTest#monitor_options}
        '''
        result = self._values.get("monitor_options")
        return typing.cast(typing.Optional["SyntheticsTestOptionsListMonitorOptions"], result)

    @builtins.property
    def monitor_priority(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#monitor_priority SyntheticsTest#monitor_priority}.'''
        result = self._values.get("monitor_priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def no_screenshot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Prevents saving screenshots of the steps.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#no_screenshot SyntheticsTest#no_screenshot}
        '''
        result = self._values.get("no_screenshot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def restricted_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of role identifiers pulled from the Roles API to restrict read and write access.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#restricted_roles SyntheticsTest#restricted_roles}
        '''
        result = self._values.get("restricted_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def retry(self) -> typing.Optional["SyntheticsTestOptionsListRetry"]:
        '''retry block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#retry SyntheticsTest#retry}
        '''
        result = self._values.get("retry")
        return typing.cast(typing.Optional["SyntheticsTestOptionsListRetry"], result)

    @builtins.property
    def rum_settings(self) -> typing.Optional["SyntheticsTestOptionsListRumSettings"]:
        '''rum_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#rum_settings SyntheticsTest#rum_settings}
        '''
        result = self._values.get("rum_settings")
        return typing.cast(typing.Optional["SyntheticsTestOptionsListRumSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestOptionsList(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestOptionsListCi",
    jsii_struct_bases=[],
    name_mapping={"execution_rule": "executionRule"},
)
class SyntheticsTestOptionsListCi:
    def __init__(self, *, execution_rule: typing.Optional[builtins.str] = None) -> None:
        '''
        :param execution_rule: Execution rule for a Synthetics test. Valid values are ``blocking``, ``non_blocking``, ``skipped``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#execution_rule SyntheticsTest#execution_rule}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0093f6a14d51c2ea4e6d07755ef1fdafdd0b8b9df89ddaf3c83bdcead75f6b1)
            check_type(argname="argument execution_rule", value=execution_rule, expected_type=type_hints["execution_rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if execution_rule is not None:
            self._values["execution_rule"] = execution_rule

    @builtins.property
    def execution_rule(self) -> typing.Optional[builtins.str]:
        '''Execution rule for a Synthetics test. Valid values are ``blocking``, ``non_blocking``, ``skipped``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#execution_rule SyntheticsTest#execution_rule}
        '''
        result = self._values.get("execution_rule")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestOptionsListCi(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestOptionsListCiOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestOptionsListCiOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19dc18ffff3c28626a3ab5e54dfa0b075dcc1a4dcf28e82041cbb2dd81cf3f9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExecutionRule")
    def reset_execution_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionRule", []))

    @builtins.property
    @jsii.member(jsii_name="executionRuleInput")
    def execution_rule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRule")
    def execution_rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionRule"))

    @execution_rule.setter
    def execution_rule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba5b924c0c2d71661d383ccc52c435dbd5dcd79f3c3c4418a73cb9892f64373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRule", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SyntheticsTestOptionsListCi]:
        return typing.cast(typing.Optional[SyntheticsTestOptionsListCi], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestOptionsListCi],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47321aa9e00a826069fb1c7aac4298bbab4283eba826267c5444050e93a55c8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestOptionsListMonitorOptions",
    jsii_struct_bases=[],
    name_mapping={"renotify_interval": "renotifyInterval"},
)
class SyntheticsTestOptionsListMonitorOptions:
    def __init__(
        self,
        *,
        renotify_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param renotify_interval: Specify a renotification frequency. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#renotify_interval SyntheticsTest#renotify_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28889328257d49fcc4bc5f51ec63aed2902e3d925d40bd6ed9edf1ec9b7ee0ce)
            check_type(argname="argument renotify_interval", value=renotify_interval, expected_type=type_hints["renotify_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if renotify_interval is not None:
            self._values["renotify_interval"] = renotify_interval

    @builtins.property
    def renotify_interval(self) -> typing.Optional[jsii.Number]:
        '''Specify a renotification frequency.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#renotify_interval SyntheticsTest#renotify_interval}
        '''
        result = self._values.get("renotify_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestOptionsListMonitorOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestOptionsListMonitorOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestOptionsListMonitorOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a1921fbce298cc6bd737c1910a355f48832cb4290fc1790935025a679d17796)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRenotifyInterval")
    def reset_renotify_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRenotifyInterval", []))

    @builtins.property
    @jsii.member(jsii_name="renotifyIntervalInput")
    def renotify_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "renotifyIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="renotifyInterval")
    def renotify_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "renotifyInterval"))

    @renotify_interval.setter
    def renotify_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ea4912ea852f77f5a70fa8fe028724b531792a135395e2a3f8ca89643afe9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "renotifyInterval", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SyntheticsTestOptionsListMonitorOptions]:
        return typing.cast(typing.Optional[SyntheticsTestOptionsListMonitorOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestOptionsListMonitorOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d8efaa9b18bd9c319279983db5109ac1996e2195bb489b733584961c476cda0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SyntheticsTestOptionsListOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestOptionsListOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78a25caa898b8d54783108c1e76beb3e94a916048730439ebeaa41e3f9b5f518)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCi")
    def put_ci(self, *, execution_rule: typing.Optional[builtins.str] = None) -> None:
        '''
        :param execution_rule: Execution rule for a Synthetics test. Valid values are ``blocking``, ``non_blocking``, ``skipped``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#execution_rule SyntheticsTest#execution_rule}
        '''
        value = SyntheticsTestOptionsListCi(execution_rule=execution_rule)

        return typing.cast(None, jsii.invoke(self, "putCi", [value]))

    @jsii.member(jsii_name="putMonitorOptions")
    def put_monitor_options(
        self,
        *,
        renotify_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param renotify_interval: Specify a renotification frequency. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#renotify_interval SyntheticsTest#renotify_interval}
        '''
        value = SyntheticsTestOptionsListMonitorOptions(
            renotify_interval=renotify_interval
        )

        return typing.cast(None, jsii.invoke(self, "putMonitorOptions", [value]))

    @jsii.member(jsii_name="putRetry")
    def put_retry(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: Number of retries needed to consider a location as failed before sending a notification alert. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#count SyntheticsTest#count}
        :param interval: Interval between a failed test and the next retry in milliseconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#interval SyntheticsTest#interval}
        '''
        value = SyntheticsTestOptionsListRetry(count=count, interval=interval)

        return typing.cast(None, jsii.invoke(self, "putRetry", [value]))

    @jsii.member(jsii_name="putRumSettings")
    def put_rum_settings(
        self,
        *,
        is_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        application_id: typing.Optional[builtins.str] = None,
        client_token_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param is_enabled: Determines whether RUM data is collected during test runs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#is_enabled SyntheticsTest#is_enabled}
        :param application_id: RUM application ID used to collect RUM data for the browser test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#application_id SyntheticsTest#application_id}
        :param client_token_id: RUM application API key ID used to collect RUM data for the browser test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#client_token_id SyntheticsTest#client_token_id}
        '''
        value = SyntheticsTestOptionsListRumSettings(
            is_enabled=is_enabled,
            application_id=application_id,
            client_token_id=client_token_id,
        )

        return typing.cast(None, jsii.invoke(self, "putRumSettings", [value]))

    @jsii.member(jsii_name="resetAcceptSelfSigned")
    def reset_accept_self_signed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceptSelfSigned", []))

    @jsii.member(jsii_name="resetAllowInsecure")
    def reset_allow_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowInsecure", []))

    @jsii.member(jsii_name="resetCheckCertificateRevocation")
    def reset_check_certificate_revocation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCheckCertificateRevocation", []))

    @jsii.member(jsii_name="resetCi")
    def reset_ci(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCi", []))

    @jsii.member(jsii_name="resetDisableCors")
    def reset_disable_cors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableCors", []))

    @jsii.member(jsii_name="resetDisableCsp")
    def reset_disable_csp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableCsp", []))

    @jsii.member(jsii_name="resetFollowRedirects")
    def reset_follow_redirects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFollowRedirects", []))

    @jsii.member(jsii_name="resetIgnoreServerCertificateError")
    def reset_ignore_server_certificate_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreServerCertificateError", []))

    @jsii.member(jsii_name="resetInitialNavigationTimeout")
    def reset_initial_navigation_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialNavigationTimeout", []))

    @jsii.member(jsii_name="resetMinFailureDuration")
    def reset_min_failure_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinFailureDuration", []))

    @jsii.member(jsii_name="resetMinLocationFailed")
    def reset_min_location_failed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinLocationFailed", []))

    @jsii.member(jsii_name="resetMonitorName")
    def reset_monitor_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitorName", []))

    @jsii.member(jsii_name="resetMonitorOptions")
    def reset_monitor_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitorOptions", []))

    @jsii.member(jsii_name="resetMonitorPriority")
    def reset_monitor_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitorPriority", []))

    @jsii.member(jsii_name="resetNoScreenshot")
    def reset_no_screenshot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoScreenshot", []))

    @jsii.member(jsii_name="resetRestrictedRoles")
    def reset_restricted_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictedRoles", []))

    @jsii.member(jsii_name="resetRetry")
    def reset_retry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetry", []))

    @jsii.member(jsii_name="resetRumSettings")
    def reset_rum_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRumSettings", []))

    @builtins.property
    @jsii.member(jsii_name="ci")
    def ci(self) -> SyntheticsTestOptionsListCiOutputReference:
        return typing.cast(SyntheticsTestOptionsListCiOutputReference, jsii.get(self, "ci"))

    @builtins.property
    @jsii.member(jsii_name="monitorOptions")
    def monitor_options(self) -> SyntheticsTestOptionsListMonitorOptionsOutputReference:
        return typing.cast(SyntheticsTestOptionsListMonitorOptionsOutputReference, jsii.get(self, "monitorOptions"))

    @builtins.property
    @jsii.member(jsii_name="retry")
    def retry(self) -> "SyntheticsTestOptionsListRetryOutputReference":
        return typing.cast("SyntheticsTestOptionsListRetryOutputReference", jsii.get(self, "retry"))

    @builtins.property
    @jsii.member(jsii_name="rumSettings")
    def rum_settings(self) -> "SyntheticsTestOptionsListRumSettingsOutputReference":
        return typing.cast("SyntheticsTestOptionsListRumSettingsOutputReference", jsii.get(self, "rumSettings"))

    @builtins.property
    @jsii.member(jsii_name="acceptSelfSignedInput")
    def accept_self_signed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "acceptSelfSignedInput"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecureInput")
    def allow_insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowInsecureInput"))

    @builtins.property
    @jsii.member(jsii_name="checkCertificateRevocationInput")
    def check_certificate_revocation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "checkCertificateRevocationInput"))

    @builtins.property
    @jsii.member(jsii_name="ciInput")
    def ci_input(self) -> typing.Optional[SyntheticsTestOptionsListCi]:
        return typing.cast(typing.Optional[SyntheticsTestOptionsListCi], jsii.get(self, "ciInput"))

    @builtins.property
    @jsii.member(jsii_name="disableCorsInput")
    def disable_cors_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableCorsInput"))

    @builtins.property
    @jsii.member(jsii_name="disableCspInput")
    def disable_csp_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableCspInput"))

    @builtins.property
    @jsii.member(jsii_name="followRedirectsInput")
    def follow_redirects_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "followRedirectsInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreServerCertificateErrorInput")
    def ignore_server_certificate_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreServerCertificateErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="initialNavigationTimeoutInput")
    def initial_navigation_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialNavigationTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="minFailureDurationInput")
    def min_failure_duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minFailureDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="minLocationFailedInput")
    def min_location_failed_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minLocationFailedInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorNameInput")
    def monitor_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "monitorNameInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorOptionsInput")
    def monitor_options_input(
        self,
    ) -> typing.Optional[SyntheticsTestOptionsListMonitorOptions]:
        return typing.cast(typing.Optional[SyntheticsTestOptionsListMonitorOptions], jsii.get(self, "monitorOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorPriorityInput")
    def monitor_priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monitorPriorityInput"))

    @builtins.property
    @jsii.member(jsii_name="noScreenshotInput")
    def no_screenshot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noScreenshotInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictedRolesInput")
    def restricted_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "restrictedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="retryInput")
    def retry_input(self) -> typing.Optional["SyntheticsTestOptionsListRetry"]:
        return typing.cast(typing.Optional["SyntheticsTestOptionsListRetry"], jsii.get(self, "retryInput"))

    @builtins.property
    @jsii.member(jsii_name="rumSettingsInput")
    def rum_settings_input(
        self,
    ) -> typing.Optional["SyntheticsTestOptionsListRumSettings"]:
        return typing.cast(typing.Optional["SyntheticsTestOptionsListRumSettings"], jsii.get(self, "rumSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="tickEveryInput")
    def tick_every_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tickEveryInput"))

    @builtins.property
    @jsii.member(jsii_name="acceptSelfSigned")
    def accept_self_signed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "acceptSelfSigned"))

    @accept_self_signed.setter
    def accept_self_signed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53d8cc461b8a175588b2371ab85da744cfbc1d28ee657a764ce99696f6fe5abf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptSelfSigned", value)

    @builtins.property
    @jsii.member(jsii_name="allowInsecure")
    def allow_insecure(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowInsecure"))

    @allow_insecure.setter
    def allow_insecure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__906fce1953d4c28ba2f11353abb9b392caddd0f4f980b25309db51dd0c9a9c61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value)

    @builtins.property
    @jsii.member(jsii_name="checkCertificateRevocation")
    def check_certificate_revocation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "checkCertificateRevocation"))

    @check_certificate_revocation.setter
    def check_certificate_revocation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a32c3a7384117855a7c629b949b1de291a32e238f72ddd1c7a4c2a1e5ad2767b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checkCertificateRevocation", value)

    @builtins.property
    @jsii.member(jsii_name="disableCors")
    def disable_cors(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableCors"))

    @disable_cors.setter
    def disable_cors(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b9a91a7f15f54a36f8146eca988c4c423d2799b508f48b6ff93b1e74c6d04d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableCors", value)

    @builtins.property
    @jsii.member(jsii_name="disableCsp")
    def disable_csp(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableCsp"))

    @disable_csp.setter
    def disable_csp(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a828f2f2bef55b4cd3c79f4d8b6c47f3bafb288b6938e80503c908fc12c870)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableCsp", value)

    @builtins.property
    @jsii.member(jsii_name="followRedirects")
    def follow_redirects(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "followRedirects"))

    @follow_redirects.setter
    def follow_redirects(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d00b97833d2dbef78a26064a602de75790e95112e4b030781b0f2cea9fff5bfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "followRedirects", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreServerCertificateError")
    def ignore_server_certificate_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreServerCertificateError"))

    @ignore_server_certificate_error.setter
    def ignore_server_certificate_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11b2b2eae7abfbcdbdd9ded17ab8fb42540bf2a3224afc34a660b3b94d2298f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreServerCertificateError", value)

    @builtins.property
    @jsii.member(jsii_name="initialNavigationTimeout")
    def initial_navigation_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialNavigationTimeout"))

    @initial_navigation_timeout.setter
    def initial_navigation_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__085bad40cf3518fd9cdc565cec5e66f2fee9b8e86b76d6fcd7b0b53079c40420)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialNavigationTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="minFailureDuration")
    def min_failure_duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minFailureDuration"))

    @min_failure_duration.setter
    def min_failure_duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81380c6e2b43101946551969262f72f5bfbedbf1c9264024d140575cdb54869)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minFailureDuration", value)

    @builtins.property
    @jsii.member(jsii_name="minLocationFailed")
    def min_location_failed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minLocationFailed"))

    @min_location_failed.setter
    def min_location_failed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d814b7fd09e8de93d2029a5aa5775ab294dad5122009f972d6f33cf8a3f27aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minLocationFailed", value)

    @builtins.property
    @jsii.member(jsii_name="monitorName")
    def monitor_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monitorName"))

    @monitor_name.setter
    def monitor_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604143bda0c23e6b2265036f1a03f897d17524780be0282b7a53c5bfa9b01eb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorName", value)

    @builtins.property
    @jsii.member(jsii_name="monitorPriority")
    def monitor_priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "monitorPriority"))

    @monitor_priority.setter
    def monitor_priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__540f0fa4d54daea7a660a4e69ca7bc1626abdf616ea9ef3fc8daaae0dba94932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorPriority", value)

    @builtins.property
    @jsii.member(jsii_name="noScreenshot")
    def no_screenshot(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noScreenshot"))

    @no_screenshot.setter
    def no_screenshot(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__068da975e3df412bc6fb59c03e825c41a7d5af36551c532ce316775c83fb2bf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noScreenshot", value)

    @builtins.property
    @jsii.member(jsii_name="restrictedRoles")
    def restricted_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "restrictedRoles"))

    @restricted_roles.setter
    def restricted_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef9908b06b86576577772fe00d5df0be963b39c1142a17f9e6aeb9f196f1bd86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restrictedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="tickEvery")
    def tick_every(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tickEvery"))

    @tick_every.setter
    def tick_every(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82e67e70c1e41308d26d3e1f4fd1c484ab3ab7b8ec6a7bd1a73ee6bce9579811)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tickEvery", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SyntheticsTestOptionsList]:
        return typing.cast(typing.Optional[SyntheticsTestOptionsList], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SyntheticsTestOptionsList]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f92ac44590f538d77cdce4d44de1454c856fc44753f6ddfa1fc43ab723ed6343)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestOptionsListRetry",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "interval": "interval"},
)
class SyntheticsTestOptionsListRetry:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: Number of retries needed to consider a location as failed before sending a notification alert. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#count SyntheticsTest#count}
        :param interval: Interval between a failed test and the next retry in milliseconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#interval SyntheticsTest#interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa0df52a234c3b47310cd58b4e593d79f53079a82be095d4e9a400d73721761)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if interval is not None:
            self._values["interval"] = interval

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''Number of retries needed to consider a location as failed before sending a notification alert.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#count SyntheticsTest#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''Interval between a failed test and the next retry in milliseconds.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#interval SyntheticsTest#interval}
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestOptionsListRetry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestOptionsListRetryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestOptionsListRetryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34f7a6dd118f08f139e5f7bad453d6db56808e858890e590831c06ea0b67d9b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf87c3848106f26b72761924188bfa8e1c621d5ff50f56303b3917d77ba3f61b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff86c0adf51363ef99f59806789280e4240ed96cb474f0d1c10bedfbbde53231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SyntheticsTestOptionsListRetry]:
        return typing.cast(typing.Optional[SyntheticsTestOptionsListRetry], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestOptionsListRetry],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ede7c007211f47688090c465f761136621636b662b5e7d5d74b059ea4c946b80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestOptionsListRumSettings",
    jsii_struct_bases=[],
    name_mapping={
        "is_enabled": "isEnabled",
        "application_id": "applicationId",
        "client_token_id": "clientTokenId",
    },
)
class SyntheticsTestOptionsListRumSettings:
    def __init__(
        self,
        *,
        is_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        application_id: typing.Optional[builtins.str] = None,
        client_token_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param is_enabled: Determines whether RUM data is collected during test runs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#is_enabled SyntheticsTest#is_enabled}
        :param application_id: RUM application ID used to collect RUM data for the browser test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#application_id SyntheticsTest#application_id}
        :param client_token_id: RUM application API key ID used to collect RUM data for the browser test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#client_token_id SyntheticsTest#client_token_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6b5f4754bdd2637d48c2b54704c64d2e1663b2f709176c1af7d043ac9495d03)
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument client_token_id", value=client_token_id, expected_type=type_hints["client_token_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "is_enabled": is_enabled,
        }
        if application_id is not None:
            self._values["application_id"] = application_id
        if client_token_id is not None:
            self._values["client_token_id"] = client_token_id

    @builtins.property
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Determines whether RUM data is collected during test runs.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#is_enabled SyntheticsTest#is_enabled}
        '''
        result = self._values.get("is_enabled")
        assert result is not None, "Required property 'is_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''RUM application ID used to collect RUM data for the browser test.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#application_id SyntheticsTest#application_id}
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_token_id(self) -> typing.Optional[jsii.Number]:
        '''RUM application API key ID used to collect RUM data for the browser test.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#client_token_id SyntheticsTest#client_token_id}
        '''
        result = self._values.get("client_token_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestOptionsListRumSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestOptionsListRumSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestOptionsListRumSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20d8766d459895f2e980c5ddba256e3843de943850f16b95e656f4654ff07697)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetApplicationId")
    def reset_application_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationId", []))

    @jsii.member(jsii_name="resetClientTokenId")
    def reset_client_token_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientTokenId", []))

    @builtins.property
    @jsii.member(jsii_name="applicationIdInput")
    def application_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientTokenIdInput")
    def client_token_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "clientTokenIdInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ea5e89582a6b6c11aaa9c5cf42d77175ec3fe0cd96be735cc5ec3e0565e572f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="clientTokenId")
    def client_token_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientTokenId"))

    @client_token_id.setter
    def client_token_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70e9a4e989e3e37e049769b11072525a15aad3d74e73e59e35fb80fa832a2a53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTokenId", value)

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aac0c828c4a937c80fe94ec79a2ceff1e6ad10dcba147d9b749326fc9a6afc9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SyntheticsTestOptionsListRumSettings]:
        return typing.cast(typing.Optional[SyntheticsTestOptionsListRumSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestOptionsListRumSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1663cc5a33c5ad00036ef45aeb874a10a96854513a0a61fb3ae644a5a5bddd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestRequestBasicauth",
    jsii_struct_bases=[],
    name_mapping={
        "access_key": "accessKey",
        "access_token_url": "accessTokenUrl",
        "audience": "audience",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "domain": "domain",
        "password": "password",
        "region": "region",
        "resource": "resource",
        "scope": "scope",
        "secret_key": "secretKey",
        "service_name": "serviceName",
        "session_token": "sessionToken",
        "token_api_authentication": "tokenApiAuthentication",
        "type": "type",
        "username": "username",
        "workstation": "workstation",
    },
)
class SyntheticsTestRequestBasicauth:
    def __init__(
        self,
        *,
        access_key: typing.Optional[builtins.str] = None,
        access_token_url: typing.Optional[builtins.str] = None,
        audience: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        domain: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        service_name: typing.Optional[builtins.str] = None,
        session_token: typing.Optional[builtins.str] = None,
        token_api_authentication: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
        workstation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_key: Access key for ``SIGV4`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#access_key SyntheticsTest#access_key}
        :param access_token_url: Access token url for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#access_token_url SyntheticsTest#access_token_url}
        :param audience: Audience for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#audience SyntheticsTest#audience}
        :param client_id: Client ID for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#client_id SyntheticsTest#client_id}
        :param client_secret: Client secret for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#client_secret SyntheticsTest#client_secret}
        :param domain: Domain for ``ntlm`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#domain SyntheticsTest#domain}
        :param password: Password for authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#password SyntheticsTest#password}
        :param region: Region for ``SIGV4`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#region SyntheticsTest#region}
        :param resource: Resource for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#resource SyntheticsTest#resource}
        :param scope: Scope for ``oauth-client`` or ``oauth-rop`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#scope SyntheticsTest#scope}
        :param secret_key: Secret key for ``SIGV4`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#secret_key SyntheticsTest#secret_key}
        :param service_name: Service name for ``SIGV4`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#service_name SyntheticsTest#service_name}
        :param session_token: Session token for ``SIGV4`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#session_token SyntheticsTest#session_token}
        :param token_api_authentication: Token API Authentication for ``oauth-client`` or ``oauth-rop`` authentication. Valid values are ``header``, ``body``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#token_api_authentication SyntheticsTest#token_api_authentication}
        :param type: Type of basic authentication to use when performing the test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        :param username: Username for authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#username SyntheticsTest#username}
        :param workstation: Workstation for ``ntlm`` authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#workstation SyntheticsTest#workstation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc5a48ceb2c2bf2e059d12af9f1e014c367434553afc8a2394e787c56f997510)
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument access_token_url", value=access_token_url, expected_type=type_hints["access_token_url"])
            check_type(argname="argument audience", value=audience, expected_type=type_hints["audience"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument session_token", value=session_token, expected_type=type_hints["session_token"])
            check_type(argname="argument token_api_authentication", value=token_api_authentication, expected_type=type_hints["token_api_authentication"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument workstation", value=workstation, expected_type=type_hints["workstation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_key is not None:
            self._values["access_key"] = access_key
        if access_token_url is not None:
            self._values["access_token_url"] = access_token_url
        if audience is not None:
            self._values["audience"] = audience
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if domain is not None:
            self._values["domain"] = domain
        if password is not None:
            self._values["password"] = password
        if region is not None:
            self._values["region"] = region
        if resource is not None:
            self._values["resource"] = resource
        if scope is not None:
            self._values["scope"] = scope
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if service_name is not None:
            self._values["service_name"] = service_name
        if session_token is not None:
            self._values["session_token"] = session_token
        if token_api_authentication is not None:
            self._values["token_api_authentication"] = token_api_authentication
        if type is not None:
            self._values["type"] = type
        if username is not None:
            self._values["username"] = username
        if workstation is not None:
            self._values["workstation"] = workstation

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''Access key for ``SIGV4`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#access_key SyntheticsTest#access_key}
        '''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_token_url(self) -> typing.Optional[builtins.str]:
        '''Access token url for ``oauth-client`` or ``oauth-rop`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#access_token_url SyntheticsTest#access_token_url}
        '''
        result = self._values.get("access_token_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def audience(self) -> typing.Optional[builtins.str]:
        '''Audience for ``oauth-client`` or ``oauth-rop`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#audience SyntheticsTest#audience}
        '''
        result = self._values.get("audience")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Client ID for ``oauth-client`` or ``oauth-rop`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#client_id SyntheticsTest#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''Client secret for ``oauth-client`` or ``oauth-rop`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#client_secret SyntheticsTest#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''Domain for ``ntlm`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#domain SyntheticsTest#domain}
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#password SyntheticsTest#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region for ``SIGV4`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#region SyntheticsTest#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''Resource for ``oauth-client`` or ``oauth-rop`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#resource SyntheticsTest#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''Scope for ``oauth-client`` or ``oauth-rop`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#scope SyntheticsTest#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''Secret key for ``SIGV4`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#secret_key SyntheticsTest#secret_key}
        '''
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''Service name for ``SIGV4`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#service_name SyntheticsTest#service_name}
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_token(self) -> typing.Optional[builtins.str]:
        '''Session token for ``SIGV4`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#session_token SyntheticsTest#session_token}
        '''
        result = self._values.get("session_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_api_authentication(self) -> typing.Optional[builtins.str]:
        '''Token API Authentication for ``oauth-client`` or ``oauth-rop`` authentication. Valid values are ``header``, ``body``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#token_api_authentication SyntheticsTest#token_api_authentication}
        '''
        result = self._values.get("token_api_authentication")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of basic authentication to use when performing the test.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#type SyntheticsTest#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username for authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#username SyntheticsTest#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workstation(self) -> typing.Optional[builtins.str]:
        '''Workstation for ``ntlm`` authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#workstation SyntheticsTest#workstation}
        '''
        result = self._values.get("workstation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestRequestBasicauth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestRequestBasicauthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestRequestBasicauthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f363a63fbb7d68690675b82d7ad4db22a093e8e160bade2261774912d98e56a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccessKey")
    def reset_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessKey", []))

    @jsii.member(jsii_name="resetAccessTokenUrl")
    def reset_access_token_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessTokenUrl", []))

    @jsii.member(jsii_name="resetAudience")
    def reset_audience(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudience", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetDomain")
    def reset_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomain", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetResource")
    def reset_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResource", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @jsii.member(jsii_name="resetSecretKey")
    def reset_secret_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretKey", []))

    @jsii.member(jsii_name="resetServiceName")
    def reset_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceName", []))

    @jsii.member(jsii_name="resetSessionToken")
    def reset_session_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionToken", []))

    @jsii.member(jsii_name="resetTokenApiAuthentication")
    def reset_token_api_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenApiAuthentication", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @jsii.member(jsii_name="resetWorkstation")
    def reset_workstation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkstation", []))

    @builtins.property
    @jsii.member(jsii_name="accessKeyInput")
    def access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenUrlInput")
    def access_token_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="audienceInput")
    def audience_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audienceInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="secretKeyInput")
    def secret_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionTokenInput")
    def session_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenApiAuthenticationInput")
    def token_api_authentication_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenApiAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="workstationInput")
    def workstation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workstationInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKey")
    def access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKey"))

    @access_key.setter
    def access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94cc4b8bb46ad62c603abf3f8028422298f7a9faf7ff70dee270ef76c40745d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKey", value)

    @builtins.property
    @jsii.member(jsii_name="accessTokenUrl")
    def access_token_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessTokenUrl"))

    @access_token_url.setter
    def access_token_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__407a74a9aa67b584155db592c566d50a22c93c7c2b70873d8bb9c4bf872c9798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessTokenUrl", value)

    @builtins.property
    @jsii.member(jsii_name="audience")
    def audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audience"))

    @audience.setter
    def audience(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10646dc290f3bbd55e5ededee9d22783f2140b08cecc8afd452df8c3f8d01420)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audience", value)

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81e6e2d2fbb236f8d2c62a79fc3eba04c547e916ef5ca6c1fbd60a031567c41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b30c5298a2ac1df214317c680f8dd0b634bfeba782bab17d0c0bc6642a109425)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value)

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9942ea490170d591200dd0804d13d7e99ca8903c6eabb18bdee2e9ad769f92ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e94ea991cb0b0161a981eab801a6abec63fe826fd9c0df2727d633094cc39894)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f69d7d1a7913259b72f2876586a2160743c54c21c4b32f5b5b66982c1f91fad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1752cc6b54989a3068f906c57912c83e2a9a362df18b3c294b1bc64d4c324959)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83510ed49c02884cf544baf531d7c220151f65e5d54467dd53e42477f1b3958b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value)

    @builtins.property
    @jsii.member(jsii_name="secretKey")
    def secret_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretKey"))

    @secret_key.setter
    def secret_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4455d75e86816f958c532b039686600adcc98f3e19fac180c2fedfbdac84f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretKey", value)

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3bc20ecdeb6b3599a72423380e50d3b3eb5a93edd426fabf3c1fbd3cef5dd99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value)

    @builtins.property
    @jsii.member(jsii_name="sessionToken")
    def session_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionToken"))

    @session_token.setter
    def session_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae5327fb3fc4f29c1fbdfc192c6fecaeaea59ee8474835e02e63edee700ddb62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionToken", value)

    @builtins.property
    @jsii.member(jsii_name="tokenApiAuthentication")
    def token_api_authentication(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenApiAuthentication"))

    @token_api_authentication.setter
    def token_api_authentication(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0b95996946838d7be31670b5b7a69ca242605c9107c8461514438e0a14f64ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenApiAuthentication", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8014a17c1d3c93819422ad6e35b3919072910c3bb9a007c3b9af7115c9576bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__635919ce63a9985f4ebd45e24b71fec931136896f5342f9d52c8b31eecaff218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="workstation")
    def workstation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workstation"))

    @workstation.setter
    def workstation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bbd253c6d10687001a5a9932a031b75098c35f3e0adff5b6c69fb720d26ed56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workstation", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SyntheticsTestRequestBasicauth]:
        return typing.cast(typing.Optional[SyntheticsTestRequestBasicauth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestRequestBasicauth],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a5530de0dfafbde27168d25cb0a83eb70d80e7127ea53e65211f99be46a0e73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestRequestClientCertificate",
    jsii_struct_bases=[],
    name_mapping={"cert": "cert", "key": "key"},
)
class SyntheticsTestRequestClientCertificate:
    def __init__(
        self,
        *,
        cert: typing.Union["SyntheticsTestRequestClientCertificateCert", typing.Dict[builtins.str, typing.Any]],
        key: typing.Union["SyntheticsTestRequestClientCertificateKey", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param cert: cert block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#cert SyntheticsTest#cert}
        :param key: key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#key SyntheticsTest#key}
        '''
        if isinstance(cert, dict):
            cert = SyntheticsTestRequestClientCertificateCert(**cert)
        if isinstance(key, dict):
            key = SyntheticsTestRequestClientCertificateKey(**key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92195cebae295ffd60c183c12604e2c5eb3c23f1c1e9b54c1d9796fb96b11f15)
            check_type(argname="argument cert", value=cert, expected_type=type_hints["cert"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cert": cert,
            "key": key,
        }

    @builtins.property
    def cert(self) -> "SyntheticsTestRequestClientCertificateCert":
        '''cert block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#cert SyntheticsTest#cert}
        '''
        result = self._values.get("cert")
        assert result is not None, "Required property 'cert' is missing"
        return typing.cast("SyntheticsTestRequestClientCertificateCert", result)

    @builtins.property
    def key(self) -> "SyntheticsTestRequestClientCertificateKey":
        '''key block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#key SyntheticsTest#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast("SyntheticsTestRequestClientCertificateKey", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestRequestClientCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestRequestClientCertificateCert",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "filename": "filename"},
)
class SyntheticsTestRequestClientCertificateCert:
    def __init__(
        self,
        *,
        content: builtins.str,
        filename: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: Content of the certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#content SyntheticsTest#content}
        :param filename: File name for the certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#filename SyntheticsTest#filename}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e334ed395f958380ee046623f4875bfa101e3334814a9ed13404290a242541c)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
        }
        if filename is not None:
            self._values["filename"] = filename

    @builtins.property
    def content(self) -> builtins.str:
        '''Content of the certificate.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#content SyntheticsTest#content}
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filename(self) -> typing.Optional[builtins.str]:
        '''File name for the certificate.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#filename SyntheticsTest#filename}
        '''
        result = self._values.get("filename")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestRequestClientCertificateCert(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestRequestClientCertificateCertOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestRequestClientCertificateCertOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b5f952859c609ed3e93e67f4181cd3f22f2f1275d641fb258e3b6bc8d099fc0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFilename")
    def reset_filename(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilename", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="filenameInput")
    def filename_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filenameInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73393d74b4e4061530a65b78a3e40a4594d9eb6ca71459fc714d79bb035fdbd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="filename")
    def filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filename"))

    @filename.setter
    def filename(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a291051fd7f0140080a06f6aebf3844d786d01d80c4bb74fc6d48047e69bbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filename", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SyntheticsTestRequestClientCertificateCert]:
        return typing.cast(typing.Optional[SyntheticsTestRequestClientCertificateCert], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestRequestClientCertificateCert],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b0acfa47ff2e9b82a4088756078469055d3f998b6de0477cf1b1b57b0c8bb93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestRequestClientCertificateKey",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "filename": "filename"},
)
class SyntheticsTestRequestClientCertificateKey:
    def __init__(
        self,
        *,
        content: builtins.str,
        filename: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: Content of the certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#content SyntheticsTest#content}
        :param filename: File name for the certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#filename SyntheticsTest#filename}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a570294e7d1b0d895e81a649f5fe9c23706cbfc8e04a38bc11740b39131df81)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
        }
        if filename is not None:
            self._values["filename"] = filename

    @builtins.property
    def content(self) -> builtins.str:
        '''Content of the certificate.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#content SyntheticsTest#content}
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filename(self) -> typing.Optional[builtins.str]:
        '''File name for the certificate.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#filename SyntheticsTest#filename}
        '''
        result = self._values.get("filename")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestRequestClientCertificateKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestRequestClientCertificateKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestRequestClientCertificateKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e0f4c3f898aa6e85acba9c04d949ab52f77462060e953fba560946384c5b39c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFilename")
    def reset_filename(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilename", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="filenameInput")
    def filename_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filenameInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8c8703066db497694006d4e4071b415c9e2789583af8c9cc66794756c52c3c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="filename")
    def filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filename"))

    @filename.setter
    def filename(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b40190193b767a3a35768dfc650f07900182adb89c5351f1b7002dc9a030c24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filename", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SyntheticsTestRequestClientCertificateKey]:
        return typing.cast(typing.Optional[SyntheticsTestRequestClientCertificateKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestRequestClientCertificateKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad54a6bbe9199c690a5ac54428ae67e07a7433c3b788c1b373c7cdda2eb6ca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SyntheticsTestRequestClientCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestRequestClientCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ad658790366cf2cdb8d801c83309677b409846ce2dd0ec6f93a1e55d6d8a118)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCert")
    def put_cert(
        self,
        *,
        content: builtins.str,
        filename: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: Content of the certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#content SyntheticsTest#content}
        :param filename: File name for the certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#filename SyntheticsTest#filename}
        '''
        value = SyntheticsTestRequestClientCertificateCert(
            content=content, filename=filename
        )

        return typing.cast(None, jsii.invoke(self, "putCert", [value]))

    @jsii.member(jsii_name="putKey")
    def put_key(
        self,
        *,
        content: builtins.str,
        filename: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: Content of the certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#content SyntheticsTest#content}
        :param filename: File name for the certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#filename SyntheticsTest#filename}
        '''
        value = SyntheticsTestRequestClientCertificateKey(
            content=content, filename=filename
        )

        return typing.cast(None, jsii.invoke(self, "putKey", [value]))

    @builtins.property
    @jsii.member(jsii_name="cert")
    def cert(self) -> SyntheticsTestRequestClientCertificateCertOutputReference:
        return typing.cast(SyntheticsTestRequestClientCertificateCertOutputReference, jsii.get(self, "cert"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> SyntheticsTestRequestClientCertificateKeyOutputReference:
        return typing.cast(SyntheticsTestRequestClientCertificateKeyOutputReference, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="certInput")
    def cert_input(self) -> typing.Optional[SyntheticsTestRequestClientCertificateCert]:
        return typing.cast(typing.Optional[SyntheticsTestRequestClientCertificateCert], jsii.get(self, "certInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[SyntheticsTestRequestClientCertificateKey]:
        return typing.cast(typing.Optional[SyntheticsTestRequestClientCertificateKey], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SyntheticsTestRequestClientCertificate]:
        return typing.cast(typing.Optional[SyntheticsTestRequestClientCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestRequestClientCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92d1b6d4c7268836db8c63ffbb98fb8a9768414a1a1b52137aae6b7ef0daa3ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestRequestDefinition",
    jsii_struct_bases=[],
    name_mapping={
        "body": "body",
        "body_type": "bodyType",
        "call_type": "callType",
        "certificate_domains": "certificateDomains",
        "dns_server": "dnsServer",
        "dns_server_port": "dnsServerPort",
        "host": "host",
        "message": "message",
        "method": "method",
        "no_saving_response_body": "noSavingResponseBody",
        "number_of_packets": "numberOfPackets",
        "port": "port",
        "servername": "servername",
        "service": "service",
        "should_track_hops": "shouldTrackHops",
        "timeout": "timeout",
        "url": "url",
    },
)
class SyntheticsTestRequestDefinition:
    def __init__(
        self,
        *,
        body: typing.Optional[builtins.str] = None,
        body_type: typing.Optional[builtins.str] = None,
        call_type: typing.Optional[builtins.str] = None,
        certificate_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        dns_server: typing.Optional[builtins.str] = None,
        dns_server_port: typing.Optional[jsii.Number] = None,
        host: typing.Optional[builtins.str] = None,
        message: typing.Optional[builtins.str] = None,
        method: typing.Optional[builtins.str] = None,
        no_saving_response_body: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        number_of_packets: typing.Optional[jsii.Number] = None,
        port: typing.Optional[jsii.Number] = None,
        servername: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
        should_track_hops: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param body: The request body. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#body SyntheticsTest#body}
        :param body_type: Type of the request body. Valid values are ``text/plain``, ``application/json``, ``text/xml``, ``text/html``, ``application/x-www-form-urlencoded``, ``graphql``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#body_type SyntheticsTest#body_type}
        :param call_type: The type of gRPC call to perform. Valid values are ``healthcheck``, ``unary``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#call_type SyntheticsTest#call_type}
        :param certificate_domains: By default, the client certificate is applied on the domain of the starting URL for browser tests. If you want your client certificate to be applied on other domains instead, add them in ``certificate_domains``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#certificate_domains SyntheticsTest#certificate_domains}
        :param dns_server: DNS server to use for DNS tests (``subtype = "dns"``). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#dns_server SyntheticsTest#dns_server}
        :param dns_server_port: DNS server port to use for DNS tests. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#dns_server_port SyntheticsTest#dns_server_port}
        :param host: Host name to perform the test with. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#host SyntheticsTest#host}
        :param message: For UDP and websocket tests, message to send with the request. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#message SyntheticsTest#message}
        :param method: Either the HTTP method/verb to use or a gRPC method available on the service set in the ``service`` field. Required if ``subtype`` is ``HTTP`` or if ``subtype`` is ``grpc`` and ``callType`` is ``unary``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#method SyntheticsTest#method}
        :param no_saving_response_body: Determines whether or not to save the response body. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#no_saving_response_body SyntheticsTest#no_saving_response_body}
        :param number_of_packets: Number of pings to use per test for ICMP tests (``subtype = "icmp"``) between 0 and 10. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#number_of_packets SyntheticsTest#number_of_packets}
        :param port: Port to use when performing the test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#port SyntheticsTest#port}
        :param servername: For SSL tests, it specifies on which server you want to initiate the TLS handshake, allowing the server to present one of multiple possible certificates on the same IP address and TCP port number. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#servername SyntheticsTest#servername}
        :param service: The gRPC service on which you want to perform the gRPC call. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#service SyntheticsTest#service}
        :param should_track_hops: This will turn on a traceroute probe to discover all gateways along the path to the host destination. For ICMP tests (``subtype = "icmp"``). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#should_track_hops SyntheticsTest#should_track_hops}
        :param timeout: Timeout in seconds for the test. Defaults to ``60``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#timeout SyntheticsTest#timeout}
        :param url: The URL to send the request to. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#url SyntheticsTest#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__204293cab905ee980b5021cd7bf01428689590962f898e248e4cc2fbd637f571)
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            check_type(argname="argument body_type", value=body_type, expected_type=type_hints["body_type"])
            check_type(argname="argument call_type", value=call_type, expected_type=type_hints["call_type"])
            check_type(argname="argument certificate_domains", value=certificate_domains, expected_type=type_hints["certificate_domains"])
            check_type(argname="argument dns_server", value=dns_server, expected_type=type_hints["dns_server"])
            check_type(argname="argument dns_server_port", value=dns_server_port, expected_type=type_hints["dns_server_port"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument no_saving_response_body", value=no_saving_response_body, expected_type=type_hints["no_saving_response_body"])
            check_type(argname="argument number_of_packets", value=number_of_packets, expected_type=type_hints["number_of_packets"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument servername", value=servername, expected_type=type_hints["servername"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument should_track_hops", value=should_track_hops, expected_type=type_hints["should_track_hops"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if body is not None:
            self._values["body"] = body
        if body_type is not None:
            self._values["body_type"] = body_type
        if call_type is not None:
            self._values["call_type"] = call_type
        if certificate_domains is not None:
            self._values["certificate_domains"] = certificate_domains
        if dns_server is not None:
            self._values["dns_server"] = dns_server
        if dns_server_port is not None:
            self._values["dns_server_port"] = dns_server_port
        if host is not None:
            self._values["host"] = host
        if message is not None:
            self._values["message"] = message
        if method is not None:
            self._values["method"] = method
        if no_saving_response_body is not None:
            self._values["no_saving_response_body"] = no_saving_response_body
        if number_of_packets is not None:
            self._values["number_of_packets"] = number_of_packets
        if port is not None:
            self._values["port"] = port
        if servername is not None:
            self._values["servername"] = servername
        if service is not None:
            self._values["service"] = service
        if should_track_hops is not None:
            self._values["should_track_hops"] = should_track_hops
        if timeout is not None:
            self._values["timeout"] = timeout
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def body(self) -> typing.Optional[builtins.str]:
        '''The request body.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#body SyntheticsTest#body}
        '''
        result = self._values.get("body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def body_type(self) -> typing.Optional[builtins.str]:
        '''Type of the request body. Valid values are ``text/plain``, ``application/json``, ``text/xml``, ``text/html``, ``application/x-www-form-urlencoded``, ``graphql``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#body_type SyntheticsTest#body_type}
        '''
        result = self._values.get("body_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def call_type(self) -> typing.Optional[builtins.str]:
        '''The type of gRPC call to perform. Valid values are ``healthcheck``, ``unary``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#call_type SyntheticsTest#call_type}
        '''
        result = self._values.get("call_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''By default, the client certificate is applied on the domain of the starting URL for browser tests.

        If you want your client certificate to be applied on other domains instead, add them in ``certificate_domains``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#certificate_domains SyntheticsTest#certificate_domains}
        '''
        result = self._values.get("certificate_domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dns_server(self) -> typing.Optional[builtins.str]:
        '''DNS server to use for DNS tests (``subtype = "dns"``).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#dns_server SyntheticsTest#dns_server}
        '''
        result = self._values.get("dns_server")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_server_port(self) -> typing.Optional[jsii.Number]:
        '''DNS server port to use for DNS tests.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#dns_server_port SyntheticsTest#dns_server_port}
        '''
        result = self._values.get("dns_server_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Host name to perform the test with.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#host SyntheticsTest#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''For UDP and websocket tests, message to send with the request.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#message SyntheticsTest#message}
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''Either the HTTP method/verb to use or a gRPC method available on the service set in the ``service`` field.

        Required if ``subtype`` is ``HTTP`` or if ``subtype`` is ``grpc`` and ``callType`` is ``unary``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#method SyntheticsTest#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_saving_response_body(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether or not to save the response body.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#no_saving_response_body SyntheticsTest#no_saving_response_body}
        '''
        result = self._values.get("no_saving_response_body")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def number_of_packets(self) -> typing.Optional[jsii.Number]:
        '''Number of pings to use per test for ICMP tests (``subtype = "icmp"``) between 0 and 10.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#number_of_packets SyntheticsTest#number_of_packets}
        '''
        result = self._values.get("number_of_packets")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port to use when performing the test.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#port SyntheticsTest#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def servername(self) -> typing.Optional[builtins.str]:
        '''For SSL tests, it specifies on which server you want to initiate the TLS handshake, allowing the server to present one of multiple possible certificates on the same IP address and TCP port number.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#servername SyntheticsTest#servername}
        '''
        result = self._values.get("servername")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''The gRPC service on which you want to perform the gRPC call.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#service SyntheticsTest#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def should_track_hops(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This will turn on a traceroute probe to discover all gateways along the path to the host destination.

        For ICMP tests (``subtype = "icmp"``).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#should_track_hops SyntheticsTest#should_track_hops}
        '''
        result = self._values.get("should_track_hops")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Timeout in seconds for the test. Defaults to ``60``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#timeout SyntheticsTest#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''The URL to send the request to.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#url SyntheticsTest#url}
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestRequestDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestRequestDefinitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestRequestDefinitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36aa03cfb1c3398ad404a394652bb2ab0cd375f4f4567d469863d2cdabe567b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBody")
    def reset_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBody", []))

    @jsii.member(jsii_name="resetBodyType")
    def reset_body_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBodyType", []))

    @jsii.member(jsii_name="resetCallType")
    def reset_call_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCallType", []))

    @jsii.member(jsii_name="resetCertificateDomains")
    def reset_certificate_domains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateDomains", []))

    @jsii.member(jsii_name="resetDnsServer")
    def reset_dns_server(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsServer", []))

    @jsii.member(jsii_name="resetDnsServerPort")
    def reset_dns_server_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsServerPort", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetMessage")
    def reset_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessage", []))

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetNoSavingResponseBody")
    def reset_no_saving_response_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoSavingResponseBody", []))

    @jsii.member(jsii_name="resetNumberOfPackets")
    def reset_number_of_packets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberOfPackets", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetServername")
    def reset_servername(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServername", []))

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

    @jsii.member(jsii_name="resetShouldTrackHops")
    def reset_should_track_hops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShouldTrackHops", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="bodyInput")
    def body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bodyInput"))

    @builtins.property
    @jsii.member(jsii_name="bodyTypeInput")
    def body_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bodyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="callTypeInput")
    def call_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "callTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateDomainsInput")
    def certificate_domains_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "certificateDomainsInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsServerInput")
    def dns_server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsServerInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsServerPortInput")
    def dns_server_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dnsServerPortInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="noSavingResponseBodyInput")
    def no_saving_response_body_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noSavingResponseBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="numberOfPacketsInput")
    def number_of_packets_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numberOfPacketsInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="servernameInput")
    def servername_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servernameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="shouldTrackHopsInput")
    def should_track_hops_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "shouldTrackHopsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "body"))

    @body.setter
    def body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b775df52ec9346c8a0e9d4ab191e27f3f1e2dc5a7585507f77fd2476c3b5d792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "body", value)

    @builtins.property
    @jsii.member(jsii_name="bodyType")
    def body_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bodyType"))

    @body_type.setter
    def body_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__808a9591c14b9ef47e341dee25bc7fb9e2a5e1d7d0f58f9a6adf9241918406a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bodyType", value)

    @builtins.property
    @jsii.member(jsii_name="callType")
    def call_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "callType"))

    @call_type.setter
    def call_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adac81cc4e3abde0ba49034c80787798692121808f9964f3bc3f28a66f138d12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "callType", value)

    @builtins.property
    @jsii.member(jsii_name="certificateDomains")
    def certificate_domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "certificateDomains"))

    @certificate_domains.setter
    def certificate_domains(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bf6f7043810ac439cf85763a5019a75e857d7b489416d934a09a083231b2e4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateDomains", value)

    @builtins.property
    @jsii.member(jsii_name="dnsServer")
    def dns_server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsServer"))

    @dns_server.setter
    def dns_server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3994fd35b4fe62230ea33649addbbdd86812627166f81ba22b064de26760d53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsServer", value)

    @builtins.property
    @jsii.member(jsii_name="dnsServerPort")
    def dns_server_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dnsServerPort"))

    @dns_server_port.setter
    def dns_server_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9640d8050d592db99c22416188d3035894cd40d5e3646229b589734fac42d38e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsServerPort", value)

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a4f0c6174cbb4b763aaef193137d64359f5e842ba752e7c62cea9d8908032c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value)

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @message.setter
    def message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db6015c8a31e1bb1b5ec89bdc862b8f7366f13d50ea25e112b53c2768563a813)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value)

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ada67fa8780d9dd378b02aedee0a5a43deafd5a586cf8329e20b1ae99f7650c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value)

    @builtins.property
    @jsii.member(jsii_name="noSavingResponseBody")
    def no_saving_response_body(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noSavingResponseBody"))

    @no_saving_response_body.setter
    def no_saving_response_body(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7862dc9e184ae4b8e194a92fad7bd5cd6e73d5bba3f67b702aa9c8984975752)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noSavingResponseBody", value)

    @builtins.property
    @jsii.member(jsii_name="numberOfPackets")
    def number_of_packets(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberOfPackets"))

    @number_of_packets.setter
    def number_of_packets(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e701488b2ba01d49f7157c6c28979cc93e0627367a84c79528949cbc0684930a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numberOfPackets", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71cab03288c12d040b75d4e3855bdbb2c5706162ce0d0d4e444778e58b844d9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="servername")
    def servername(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servername"))

    @servername.setter
    def servername(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c29d94389a8df406db7046a6b8b138499c88af59197859b0a220e29232082347)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servername", value)

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8224cb65c273862c114b1db8311074a1a7d2e7644d6c37454099855828d9edf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value)

    @builtins.property
    @jsii.member(jsii_name="shouldTrackHops")
    def should_track_hops(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "shouldTrackHops"))

    @should_track_hops.setter
    def should_track_hops(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66cedd9c86a2237f60a473434b50472f830d4a64b531a94a4ea82e99af263b5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shouldTrackHops", value)

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f44aaab3cf698ca7598ddfaab38e7ea8da8bdc0a789a777689b4c3658ffc8c8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6973962187880a1655e5b0605745e3270409c5ada28e1ac9168ae978a91925a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SyntheticsTestRequestDefinition]:
        return typing.cast(typing.Optional[SyntheticsTestRequestDefinition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestRequestDefinition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3cadac8db57ad6ea83ba41fdcc3ff2f70eeaebf49aec72bee831f9b8378e751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestRequestProxy",
    jsii_struct_bases=[],
    name_mapping={"url": "url", "headers": "headers"},
)
class SyntheticsTestRequestProxy:
    def __init__(
        self,
        *,
        url: builtins.str,
        headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param url: URL of the proxy to perform the test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#url SyntheticsTest#url}
        :param headers: Header name and value map. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#headers SyntheticsTest#headers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c92f485264d91a1bc9f0464a9a0f1d2117e4d99f4e8c921299594e1a03fdb768)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if headers is not None:
            self._values["headers"] = headers

    @builtins.property
    def url(self) -> builtins.str:
        '''URL of the proxy to perform the test.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#url SyntheticsTest#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def headers(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Header name and value map.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_test#headers SyntheticsTest#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsTestRequestProxy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsTestRequestProxyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsTest.SyntheticsTestRequestProxyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8d9c8d80f5f5336878542c371e983b5e286693a042ecf66131f715368da22be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "headers"))

    @headers.setter
    def headers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec209dd97b5593b2bc44acec5b8648f09ea70c5fa8875be1ba2b651a4e074565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headers", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80b1b4216953940b5c3072664cb093496150b4a0d2ca29e33d3720178557b362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SyntheticsTestRequestProxy]:
        return typing.cast(typing.Optional[SyntheticsTestRequestProxy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsTestRequestProxy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3a723a9f31d4b772e505fb5b9c826a969a0e915b983f6175f2f5153a78a596f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "SyntheticsTest",
    "SyntheticsTestApiStep",
    "SyntheticsTestApiStepAssertion",
    "SyntheticsTestApiStepAssertionList",
    "SyntheticsTestApiStepAssertionOutputReference",
    "SyntheticsTestApiStepAssertionTargetjsonpath",
    "SyntheticsTestApiStepAssertionTargetjsonpathOutputReference",
    "SyntheticsTestApiStepAssertionTargetxpath",
    "SyntheticsTestApiStepAssertionTargetxpathOutputReference",
    "SyntheticsTestApiStepExtractedValue",
    "SyntheticsTestApiStepExtractedValueList",
    "SyntheticsTestApiStepExtractedValueOutputReference",
    "SyntheticsTestApiStepExtractedValueParser",
    "SyntheticsTestApiStepExtractedValueParserOutputReference",
    "SyntheticsTestApiStepList",
    "SyntheticsTestApiStepOutputReference",
    "SyntheticsTestApiStepRequestBasicauth",
    "SyntheticsTestApiStepRequestBasicauthOutputReference",
    "SyntheticsTestApiStepRequestClientCertificate",
    "SyntheticsTestApiStepRequestClientCertificateCert",
    "SyntheticsTestApiStepRequestClientCertificateCertOutputReference",
    "SyntheticsTestApiStepRequestClientCertificateKey",
    "SyntheticsTestApiStepRequestClientCertificateKeyOutputReference",
    "SyntheticsTestApiStepRequestClientCertificateOutputReference",
    "SyntheticsTestApiStepRequestDefinition",
    "SyntheticsTestApiStepRequestDefinitionOutputReference",
    "SyntheticsTestApiStepRequestProxy",
    "SyntheticsTestApiStepRequestProxyOutputReference",
    "SyntheticsTestApiStepRetry",
    "SyntheticsTestApiStepRetryOutputReference",
    "SyntheticsTestAssertion",
    "SyntheticsTestAssertionList",
    "SyntheticsTestAssertionOutputReference",
    "SyntheticsTestAssertionTargetjsonpath",
    "SyntheticsTestAssertionTargetjsonpathOutputReference",
    "SyntheticsTestAssertionTargetxpath",
    "SyntheticsTestAssertionTargetxpathOutputReference",
    "SyntheticsTestBrowserStep",
    "SyntheticsTestBrowserStepList",
    "SyntheticsTestBrowserStepOutputReference",
    "SyntheticsTestBrowserStepParams",
    "SyntheticsTestBrowserStepParamsElementUserLocator",
    "SyntheticsTestBrowserStepParamsElementUserLocatorOutputReference",
    "SyntheticsTestBrowserStepParamsElementUserLocatorValue",
    "SyntheticsTestBrowserStepParamsElementUserLocatorValueOutputReference",
    "SyntheticsTestBrowserStepParamsOutputReference",
    "SyntheticsTestBrowserStepParamsVariable",
    "SyntheticsTestBrowserStepParamsVariableOutputReference",
    "SyntheticsTestBrowserVariable",
    "SyntheticsTestBrowserVariableList",
    "SyntheticsTestBrowserVariableOutputReference",
    "SyntheticsTestConfig",
    "SyntheticsTestConfigVariable",
    "SyntheticsTestConfigVariableList",
    "SyntheticsTestConfigVariableOutputReference",
    "SyntheticsTestOptionsList",
    "SyntheticsTestOptionsListCi",
    "SyntheticsTestOptionsListCiOutputReference",
    "SyntheticsTestOptionsListMonitorOptions",
    "SyntheticsTestOptionsListMonitorOptionsOutputReference",
    "SyntheticsTestOptionsListOutputReference",
    "SyntheticsTestOptionsListRetry",
    "SyntheticsTestOptionsListRetryOutputReference",
    "SyntheticsTestOptionsListRumSettings",
    "SyntheticsTestOptionsListRumSettingsOutputReference",
    "SyntheticsTestRequestBasicauth",
    "SyntheticsTestRequestBasicauthOutputReference",
    "SyntheticsTestRequestClientCertificate",
    "SyntheticsTestRequestClientCertificateCert",
    "SyntheticsTestRequestClientCertificateCertOutputReference",
    "SyntheticsTestRequestClientCertificateKey",
    "SyntheticsTestRequestClientCertificateKeyOutputReference",
    "SyntheticsTestRequestClientCertificateOutputReference",
    "SyntheticsTestRequestDefinition",
    "SyntheticsTestRequestDefinitionOutputReference",
    "SyntheticsTestRequestProxy",
    "SyntheticsTestRequestProxyOutputReference",
]

publication.publish()

def _typecheckingstub__5b89cc4269f63e8bc3807556eba7178a1b9be7920bf505519de4dc5256f1af23(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    locations: typing.Sequence[builtins.str],
    name: builtins.str,
    status: builtins.str,
    type: builtins.str,
    api_step: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestApiStep, typing.Dict[builtins.str, typing.Any]]]]] = None,
    assertion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestAssertion, typing.Dict[builtins.str, typing.Any]]]]] = None,
    browser_step: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestBrowserStep, typing.Dict[builtins.str, typing.Any]]]]] = None,
    browser_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestBrowserVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    config_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestConfigVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    device_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
    options_list: typing.Optional[typing.Union[SyntheticsTestOptionsList, typing.Dict[builtins.str, typing.Any]]] = None,
    request_basicauth: typing.Optional[typing.Union[SyntheticsTestRequestBasicauth, typing.Dict[builtins.str, typing.Any]]] = None,
    request_client_certificate: typing.Optional[typing.Union[SyntheticsTestRequestClientCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    request_definition: typing.Optional[typing.Union[SyntheticsTestRequestDefinition, typing.Dict[builtins.str, typing.Any]]] = None,
    request_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    request_proxy: typing.Optional[typing.Union[SyntheticsTestRequestProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    request_query: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    set_cookie: typing.Optional[builtins.str] = None,
    subtype: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__714fa4824f501a9e78f16c1c225a170563d35d7c401c2228564a2614c9e6ee69(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestApiStep, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1152431a587efd5665b5172fa29182f0ead17aa572b7a7c410f965ca3e3770b9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestAssertion, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0352caac120771a2ae9347ed37d0f13b0ab4ac90e9fed5eedd8afe187cdeb06(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestBrowserStep, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e00aef3187dd8efbf31c3893fc337f05695c973d91b075ddb7ea129fc2b10b0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestBrowserVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a343543ea8eca942656fc8b4fcb5c44e430fd889f34586dcdd24c85b446619c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestConfigVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e72b0d783535e75b1149bb24b6154e9942a4036100bb34641e696ef94c5515(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73225d0602a79ccaf9a581d4e1ad0188a66d4fd21c6ccaf84f01218e8bf8be90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0338904ab0eab2a8e34960cc132109d19549cf3e264f9395b04f57c1a65483d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f6359dc1a5c20ea2fcd22fdba30ffdc0b857740eb54291ff038c5b92c28e779(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbdf5872c6500ea5002e9a1093c2a11e3a9a5b378b2ae980d010cff34938a002(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b755f999797f910b20e2585b3cbf00b83516f3925175c2ad1d5d5d5d89c1e392(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35cec634470ee9480807a84a948b9a8afd673eab1cb11e4bada87cf35c4b8f13(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76cda7beaf463e1f3b43cc4d9d031f93bbee4be1f9711e95b7553da07535cece(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f8fd678b604b907b82b5ce637905f501dc0e919b6b237dcdb293288aa76a04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67fd2426599fed35a7500d6208da818fd80978ad848d9e02629e117d4ec18dc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f6088555e47ca20d3b571c37e39653d0bca80d7e788a555c9f179000747173e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63cde1b2d68674b5d959a7bd828c3acecd6b72eb5ab53e8a529d8a8ba6d4144a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__702cd51f3b0abb5ca3b5b9ca05bc1a1dce4a0837424e2b161aa3799d16972cc7(
    *,
    name: builtins.str,
    allow_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    assertion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestApiStepAssertion, typing.Dict[builtins.str, typing.Any]]]]] = None,
    extracted_value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestApiStepExtractedValue, typing.Dict[builtins.str, typing.Any]]]]] = None,
    is_critical: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    request_basicauth: typing.Optional[typing.Union[SyntheticsTestApiStepRequestBasicauth, typing.Dict[builtins.str, typing.Any]]] = None,
    request_client_certificate: typing.Optional[typing.Union[SyntheticsTestApiStepRequestClientCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    request_definition: typing.Optional[typing.Union[SyntheticsTestApiStepRequestDefinition, typing.Dict[builtins.str, typing.Any]]] = None,
    request_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    request_proxy: typing.Optional[typing.Union[SyntheticsTestApiStepRequestProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    request_query: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    retry: typing.Optional[typing.Union[SyntheticsTestApiStepRetry, typing.Dict[builtins.str, typing.Any]]] = None,
    subtype: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4da265a3569b7eb4f2ae85853e757e4297a4fa3c5d515ee9324c83ea3d9b8a(
    *,
    operator: builtins.str,
    type: builtins.str,
    property: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    targetjsonpath: typing.Optional[typing.Union[SyntheticsTestApiStepAssertionTargetjsonpath, typing.Dict[builtins.str, typing.Any]]] = None,
    targetxpath: typing.Optional[typing.Union[SyntheticsTestApiStepAssertionTargetxpath, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f67d7bff63235752cffdcac578cd1327d2f8e2db90b1ddc9f596e884bcc032b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d71161a87f6de471c2862d15d82a159ac7e2eaba7c1f0c2f0f51081942a1f4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdb90de66cfa2997e19b6cd7900f21d724b60e8d93a1c45478ba10046c90c55e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f0eac7ad47fc90c6c6792f54a2e2514478f696786025591381febd1fd64086c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7a4a8f25f93d4aedec9c438d57a894a38a6af30fff397d8abc1e8e2911ba58(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c876298ab44b3aad8bdc85080bc97f9d6bce30caef165d11e97e553122af0cbb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestApiStepAssertion]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9edf1952456d7b35f5c2347ca13b1eed33dbec4c605901f5e4036c42ea4379e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90155739d5bd8896765bd13d02f97a23235658d3d841067ff16d11bf44075517(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18508b51e88b4640fc0ea9ae6a762f4342f0ad871f770852731062a4635992ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029efc83d81f4a929bd7b0946ff361e6d9602ea3de79194a146c4773c68d17a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67598d651c309557ff68d2e0a48ed66178030c25421b5141bb51e701c53433db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54055a44dc870c84915c6aded654f8e1a87718bcf653d0df2a15d759a1db1f6c(
    value: typing.Optional[typing.Union[SyntheticsTestApiStepAssertion, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b97ecd6f8f6690d295820867eb452b459246ac3638f37f79ab32a2811771e79(
    *,
    jsonpath: builtins.str,
    operator: builtins.str,
    targetvalue: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ef2e5240fc9e1add08f0e07c51f5df53e2cb2930137f16deb2257e9d229e08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc16e3306babb65470c459d18c415f928a36912440fd159c4f3ab160ab15c4a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43067fcd7e6108c1ecb616cf9fc3b0cd414a6098fdd1b5bf3f9e8818ee85ab1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0f49b83a01b630f7adadf98e2526383afbba2e7bb06c40bb2d216af354bf5ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b401857bfe53fe39fc157a274358dc41cd2a8355880a77864de8a293dfeabc39(
    value: typing.Optional[SyntheticsTestApiStepAssertionTargetjsonpath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f9cf4825faa95d883e253dac4201a721a1f912ba9f5d3b75d1d6153ef3f757(
    *,
    operator: builtins.str,
    targetvalue: builtins.str,
    xpath: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55aac1744fd5c3d4a8260aa51d2ecb50956e904f5d6120212e11fb525d6a051d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7af8428973a32b1e60fc488b7a0aa1838dde591130c84fe3cfc1fa7aa3d9c60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2ddebcb8a9187a05eee2734e1cff3da01bb67ab9643760bf32b71ab6679b272(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df27bcb17cf012f04c887245eb9234363820a63888776be3579e1029dd14ba1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0a8bc7123353d7a4073bb748cc8aae0ba61fb77e391c09c785310a25586701e(
    value: typing.Optional[SyntheticsTestApiStepAssertionTargetxpath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a861411ecd750d17513caf86cafaac5e6c6ff18df8e360dbe9e4a4f07ac5cc(
    *,
    name: builtins.str,
    parser: typing.Union[SyntheticsTestApiStepExtractedValueParser, typing.Dict[builtins.str, typing.Any]],
    type: builtins.str,
    field: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe0d4b5954b81da6bfb0f47f41d09e2dad934e08ec6886ebc47a7770f2a3293(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf1256ae876cf718db28df529c1d43fe87cab5a37bd582e6db2547b9b6495cc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6860e1ad8087f2695a690dcd90a44ed0392ce8727025575877c09887ad7554c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62f79054767ef3cf88280507bb5807e16aeb0e92797a8ba53b7dba2f51e3958(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3fa65287efb68dfccc162f3ab9be69d6a5c693232d76fa195fec5336cbf7f8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__598828a5f785842aeaa8e171408f3ab205002826fa4ca58a10ee5eb7c7039b6b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestApiStepExtractedValue]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00106af481ec294c9351693e4d291e3cfa1acc23d5b7487a8bdddc6264d9ef04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e163300bd7bb43fb8a13e19a4c18e6bfc1942869199ef685d59619470677b777(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ac043db3e2504cbb304a071bbb5228307c3c09f48d9436cd6df083b57f880c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd5c8335f32e622f1d62e1e9122396e6a47d9994c71d1c23de6e749743949eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a52671124a8438ba5580ea457e533b60a42f19da95e19ffd68d16c72e6eb186c(
    value: typing.Optional[typing.Union[SyntheticsTestApiStepExtractedValue, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72132190b1edd060e0da4e8a08bf4c498251b2734b641c00cd49348a5d1d235a(
    *,
    type: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__804e9a54d4d9bc07bad059ddf0d4c36e13c4584cda175e7284962493056b86b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32e6d16c0ba023aaac6db353dcf759d3482075e37735476c8379b93982c2d527(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0991b589c5f02e4807df7a9bb1494a9fd629275649a1d3692e50144a27a01033(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a25ac298488c675496bb0be38f7acebabadad024f32e014480064d88001ea3(
    value: typing.Optional[SyntheticsTestApiStepExtractedValueParser],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35d64ac6ad416d2e2ad61b4a51f2050691d86fcdc1c18babbf55712c4149114c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c767edecb7215d9665b57be4b0abc1be29dfb3e2fa047f42c794fa5c3a6e4184(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d31df5610beaa7616e3b55df4625ac6d93e19f1607af7ed6e0b40ec1f00179(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1507d17b25261ba5f3b86d0f8d5f270e01b9b062a7b277c5efff48c6c373c38(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6090f7f82a6987754551cb0e0fe4ae33be18a0c087e3a73e7185f27e944aaf1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7b00c95c0c5d8fcb629847447a45c6358af36f6022bdc595d73f3020f27739(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestApiStep]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f36b77a5c2d878aa56c43b5e02778ff1bb2377b24cd5e1c044fd8b2f3754faa4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc201daa3698f39c8d07469ef5cc3b67772cd4cc2eee73871da7771d019cf551(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestApiStepAssertion, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1655bf2763ac96dd22a8f9a73b8e5f26673ece692effb9f335dcc0aa4364ac85(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestApiStepExtractedValue, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6694002e88b69d9e0e9a399877be5ca36218ecd8eccb0c5ee6333240a1431822(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adc60c33ab07a92ac1b29abb45863d8521903146956eedcfa5a8f52ee971397e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3bcd6982a727599f28f81e1a4f650a831bbb480a54d3464fcbf5f9b73f81120(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bacb1678c117d1d02cd315490fc1db9174bd8343390047bbb203d1bdafad83c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99afc3b1d9c8c3dc0125ec7abd8cbde6b2421c525743381042894cca1390dd23(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__730d9d018da6f17b9fbfacff64dcb9ba7dfd84e3045f57ade596f9ad411f3653(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607b745268b8eaf0fc19e4a4642c6f2f435d81677dc100c56aad8c2f2becba62(
    value: typing.Optional[typing.Union[SyntheticsTestApiStep, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9bb439d9854a2545b5777d4f0fb088cccf632bb73dc99896dd5e3db37d2abcd(
    *,
    access_key: typing.Optional[builtins.str] = None,
    access_token_url: typing.Optional[builtins.str] = None,
    audience: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    domain: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    secret_key: typing.Optional[builtins.str] = None,
    service_name: typing.Optional[builtins.str] = None,
    session_token: typing.Optional[builtins.str] = None,
    token_api_authentication: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
    workstation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9710464744c8854210acc91bbd14e89c69565e7f53ce1c1dc8db72fe29b5619b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e329d3fa0a4fd3e223a71136e5bec2f6fc39dd847a6569cc8a66a93d2501c83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db812987a7566f7a5d753b25e563f978c578a29750b67e4cd40711e94635cd1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e91c7bd0256ca000b6eb912a0f7825da85ba01020a5348ae2a5005143e7382b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43c47170a5b6ae66a7771985e11767f4f61378aef5aca5a10a9894bfd1d3b256(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__289c33601c5eb28d72848f611f7d2fc525600d6c864f523b459ea3d165d08879(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4fd0a10b8b8ee2030b624be7f7e9ef54622251ee6fe6946a4f2d75bec74d51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb64c956c7a73b4b80a761fb268e7e8db6e3921aed0c5d4d7fc4194eb3da0ec5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce8952b4293c7caec3c02a322cbd85d0a6e0de759d8d156c7aeb28c7680eb5f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__200f5c6f7c7e713f902d3b54d4f32f7c3528c1f02e323745cc2c90d0e86f8a0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7dfd26c66c7cc6a258b38f7fa19d28ec91911be209569350ffbd9de8220f6d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf4aabdc24c37b0bea32b43b1563a1593763fee35f5e8dcad87dc1b13988577(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__426378d764ba8631d8111075e48febfe540fa6b83906a7dfc68325544dde586f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f928ea328da6cb2ac9356ed9f949fe013a7702e43196838dc6200fc71fd9c8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c069fa43426f4af88fa2b54181af95a71e38275fe336e9512322933b25e82433(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2b980e0d8646eb56a837fc19e8ae0951cdd7e5c613732f3476b6342cd1ddc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92fa823a27d867643a8b23a6efa79da5b217220b434c225a13e7599f6e6dbf2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb508d4c85a103bb919c6732f5002b32a16a79556d522977b84e4e8c5c955cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac67fb47d799b7ae9255a8fd41aaa2827110e36ffe7d56ae060a1945b5f82b78(
    value: typing.Optional[SyntheticsTestApiStepRequestBasicauth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b15fa8958c75e99e0888bcb1487279d33d603ec0a35be46ba617eb1667f37e32(
    *,
    cert: typing.Union[SyntheticsTestApiStepRequestClientCertificateCert, typing.Dict[builtins.str, typing.Any]],
    key: typing.Union[SyntheticsTestApiStepRequestClientCertificateKey, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4fddecf4d78c19ae0771bb4c5b3e6cb3894f08b8be59845ffc55016392bec19(
    *,
    content: builtins.str,
    filename: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f82258702c4f361fec13a67e59812db0f73d95778fcc9e6e18ca609a40ea7c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__191aecae0efe5775594fd342351e019a7e0e2cd45e69986dd24f7d2371a27481(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320830d163d8989beaa91e2a3784d32b5546ad7e84e431ec2f05ede23080951c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b51c23e7a608828803c08efc3f48f41c79aaf5d161c18bb63a6263a1e7e9e57(
    value: typing.Optional[SyntheticsTestApiStepRequestClientCertificateCert],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56d7577c3911479f67bd42bb852e440b956110cdfe556b12fb49e784db7fc663(
    *,
    content: builtins.str,
    filename: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e2da7f73ef862c49bcc920015c875ab44dd74701c297ed73698ded61e24250(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf2aac3168990b52dc1a67bc01fdf0a059707da6583eb2130c16769597114ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b720bcc93675964ee9438e164c9040a75268de90d24e514497e56f14775d4bab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd9fd72adb6f8cbbe9302f08b941f6a512cd9cef4930bafb639be76fb65a8274(
    value: typing.Optional[SyntheticsTestApiStepRequestClientCertificateKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aedfc5aae0f8ffa556f7f401283fbac70816fc00e4fc33e43a6fdbd62b4cf74e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c45446ccab7ee888eac47f296d66334b3748a2938331c258b02c900896175da(
    value: typing.Optional[SyntheticsTestApiStepRequestClientCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b7ecad871d76c1341fe87074869bbb285be183268adba97a18604dd499f279(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    body: typing.Optional[builtins.str] = None,
    body_type: typing.Optional[builtins.str] = None,
    call_type: typing.Optional[builtins.str] = None,
    certificate_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    dns_server: typing.Optional[builtins.str] = None,
    dns_server_port: typing.Optional[jsii.Number] = None,
    follow_redirects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
    method: typing.Optional[builtins.str] = None,
    no_saving_response_body: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    number_of_packets: typing.Optional[jsii.Number] = None,
    port: typing.Optional[jsii.Number] = None,
    servername: typing.Optional[builtins.str] = None,
    service: typing.Optional[builtins.str] = None,
    should_track_hops: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ede6ad30f5b25a9e1b321c9afed1100b9f773dd36c98e6828bd4de54cb1ae4a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4815bab8a4dfa6f31127499e6028e569cf08763f3739aa894ee63f5d2790cc3e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de19c0ba3c3703f89ab5d4f858319f0b746c1180a3dc7be49832c3e1e8352331(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e74f6b01d27a8fc9c3bbf747ee571b53daa3de9f3573eadc8193455c55074505(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee1168a40d5f1656adee3877f3b19343a662c1f4914479b3c338f16934fcd4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf8cdd238eca165744e8ef682150f0ba3d951641324340cc1b24080246d7785(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52d7293d4e5123a12ec81258def6493af7dc75b73a3cf891dd34779032303dae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef06fcb3bc0bb44123d3c0cfad9e577126315ff449745737918f41ef0efddf07(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe1216699bb7e091374b9939ff1e0f467cb3610e5cf754b851cb3156e4d4893(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88bc1be003a1700c729f7121c97f230d2e30032f20545b222a56562850f0604(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53496ada838d7c34e17014a0624ad91e91cf5860d72eab130c4978e6ec899a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6628773fab9af66ec83ed5640eb097ec800e9183889f15ecef632b0327413508(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a06655a47a2542b75a4ff77380d489fabc88b6b87ce48ebf4aa5b2c2c6d44c6b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c0d4081f487131daf985ba7576afec6f1f73e8b7f907ca10aafa6380dbb8e8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40b7fc4f4ed69f04548529d29c732ba99bb2c2e229db26f71f4b0a19606ca06(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb27272b7dca9380474f629a870bed0c2191722978790291dcae62f07761bef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bbf3cefa6352b6472b13491f14731ab6e76796b33593dbf862a08072fe60334(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16740cf9990749666a228ca6e6a38690d427798a90317b6eb1ce4bbe5bafe5c2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9435dab16f6e26a844a7f48e9d42d0075bcedb92cc3987073ed1e366ba5c896a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__172587f1719bb68bd99c60b4ac768f402a1d36d0eade3bc7662aea059d37db0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fbc6ea3b856d32ed784588b640efe4894f3fba14d4be0f1855d1789b911a55b(
    value: typing.Optional[SyntheticsTestApiStepRequestDefinition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a6b586490c6a8eb4ac03c07e0eec300cc3c452c48a3314c03726537e9a717e1(
    *,
    url: builtins.str,
    headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8afe44984e6d3025bf47f28328b40546863d794cfeff59c142abdd4b58b37d21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6631f6b5e0bcb40be0780532d5d2ec042aa8365c7b0ff31c0e4f62d55831d8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a02dd7a29d23f1fe4cbec77cdc7d6342a28ec0cfd5e67c223b89cdf465b91d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448867a86985fe6720bf3cb87adffec3822dc6a76a5df9c5b72cbdc8b6881f5d(
    value: typing.Optional[SyntheticsTestApiStepRequestProxy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93202b1ed0aba7204e0eb616c5b350e597a30b5352d2eb607f00173a80d523db(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__079ff7f2ced2195bf68427b01a412d31df2556736d839556cde9f4574d1d6a98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d454975e13067c05f175b3194bee22ca9971eaba058b7cb72942c01eee19cce8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d8c3099af2188f6cc18fa631a4ded71c14e65c21ef00a3631ec807e1c531b7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__add889335cc766e5867a30c6f3641d62f81f7a79388001cb49b8573b040bbdc8(
    value: typing.Optional[SyntheticsTestApiStepRetry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8f680cc39cf070e1447a0bd2ee97533a5f454c2f8b2ff8243121a09438fc107(
    *,
    operator: builtins.str,
    type: builtins.str,
    property: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    targetjsonpath: typing.Optional[typing.Union[SyntheticsTestAssertionTargetjsonpath, typing.Dict[builtins.str, typing.Any]]] = None,
    targetxpath: typing.Optional[typing.Union[SyntheticsTestAssertionTargetxpath, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca7f2d58e47f0d7520ece682adcb4b56748c4ed4a65f30716860703f3ab7f5c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__337d51562deaee05934e41a3089343f6d08b66ff79bafb30929dbcac5059bd71(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aedfbabe9c478cd330d54a16aea7f68da7b87adaf1374429952fcba5c4fde58b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d9c07a966e7415f877eb24338ee57b27bf0174e18b3fb9d8d4d6fdd3097ab0b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e652a162ead998a0d1d8a3a9ffc8b78b3cf3aa013469b593ccfb0d063d3733(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d02b690f9350e1c0434e290ff5dbfb9316cf01e096581d1a5aad0ef5b2f37d7c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestAssertion]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78d216a284f2803dad5c90dbc4efb4d8131ce265440c3539a96b37eb30c35e39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__012f52448702dfeb235aaa7c61ad4da717a33214351a51ebbea56faf9332001c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ffc09c8ade75e9cc43b15f99f5ae1e2120ce5029bc5e33f60ac4b617f539eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560fca9f4221d10abcb26359fe979e54d7c136e44e2c7b3f534759b28c710d83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab76e45c254bbf039909da9cb76596192eddaff2f027afae714ee4c6dacf9a6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79f758131e4e1b3b57f6dd6ff76fb593ae39eedbb2092892c40ed672d3a386b(
    value: typing.Optional[typing.Union[SyntheticsTestAssertion, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ffa57513c222e27013d3b57a97355879b583001e6995c55ec6b2d102a0973c5(
    *,
    jsonpath: builtins.str,
    operator: builtins.str,
    targetvalue: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4afd6cce2cc60355c9d39831bed00fbcbf459842a28cc1b9b494a55f4aa54736(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3456a3efb04700a3684fa686b26d63fdf78305d32c0fb43b640a2005603898cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1782a7f290a8eed0ebccf4f85a1ade57c04b9e24e86d530b9629295009767b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a184072dad3c082c190f7530c00e306c5aef585b52700e4d65a6bae3463b0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed4073f8d6054cba2e662bc85ba93cb9cc846cb854798d955662ecdecdbaff21(
    value: typing.Optional[SyntheticsTestAssertionTargetjsonpath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3120d1914f6076cb9896c1a6be251cf70ba0b24166d11094743e117af51e8270(
    *,
    operator: builtins.str,
    targetvalue: builtins.str,
    xpath: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__585355cff70b8e62011a75cf23344b5848d8a0137bed1ba60f848eb923511f57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2e9e592ced1ca582fd0346cf23538bc044da3f7c69986d01de4e348159b24e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19738bb2a513c39da1d51e4b42e796e2b79a8b58e17aef1da58aec3fa043060(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4bb94bc6482f59cf895943434995e3bd97d64875eed0f152ba8dac66e54a10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__227cb7eb4ffa6242af307fced300fa328551f6fbe61c1894e1e4cc9ade6be5bf(
    value: typing.Optional[SyntheticsTestAssertionTargetxpath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bef9dfde181bc34f72586c78fb39d835c87236cf565b67e5f92703601ab35b0(
    *,
    name: builtins.str,
    params: typing.Union[SyntheticsTestBrowserStepParams, typing.Dict[builtins.str, typing.Any]],
    type: builtins.str,
    allow_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    force_element_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_critical: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a9b896de28b4dfa51d955060a2316d2e2f5b8637fc8a0d43c7cfdd65b7c4dd3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7594dc10fe9f984ccb26e37ab0b9697b05a6e327495b4f0b54db094c9ccf6e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaf8c7e26f2a17aa4058c6327a958eed38514f9bc64b47298f5ef4068d924e6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e344cd935198389499f7635da7149f211a0cbd77c9cdb21a83ed0a20d873bfa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__923aa94d27a4e4b8ee1665312cc3a33e4e591014a31f74bb27ef69d84dae393b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a7bc160b4d6412d345bcae6cd67f725b3fd075bf179cb39585bd62f222c611(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestBrowserStep]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdeb9037f8d3136c89b5558ba1b8b84727d14fb80682ccbc47ceb97a485bbcee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae18289530ea4981c9278eec15ba8a13f3b02e4d981356d696cf059527f9c2e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58babd09c621ef72610027b2cad94b7f1c395bcfb01b44c532aca592afe754fd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72917cd111cb88a23ef94877eeebbcc6bc4ba61f7664d0b90c747b98f2b302f2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3110fbf0e9237e2de8c122c1cc2fa5bb8813c7bc33aaad5eba607aed7424483c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f89e2a1af5b5e214519072df8bfe935be5ab41d1ec659d433cd08930f1901a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686dee2dea23f439aeaa26c6780c2162e1e2d6de32a24d4d327ac3a17702aed4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e801e34d8760125a72c71344b3b0049a045bee54bc9d2c84149e56c840cae19(
    value: typing.Optional[typing.Union[SyntheticsTestBrowserStep, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292471245b096e37334129ad026ea7b6b3974a8db36bb6c42ede8e9bb2c5042d(
    *,
    attribute: typing.Optional[builtins.str] = None,
    check: typing.Optional[builtins.str] = None,
    click_type: typing.Optional[builtins.str] = None,
    code: typing.Optional[builtins.str] = None,
    delay: typing.Optional[jsii.Number] = None,
    element: typing.Optional[builtins.str] = None,
    element_user_locator: typing.Optional[typing.Union[SyntheticsTestBrowserStepParamsElementUserLocator, typing.Dict[builtins.str, typing.Any]]] = None,
    email: typing.Optional[builtins.str] = None,
    file: typing.Optional[builtins.str] = None,
    files: typing.Optional[builtins.str] = None,
    modifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    playing_tab_id: typing.Optional[builtins.str] = None,
    request: typing.Optional[builtins.str] = None,
    subtest_public_id: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
    variable: typing.Optional[typing.Union[SyntheticsTestBrowserStepParamsVariable, typing.Dict[builtins.str, typing.Any]]] = None,
    with_click: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    x: typing.Optional[jsii.Number] = None,
    y: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8848942ea4950fe9d0316fa727fc5ee03d80ae2dc08eec4b2cc17d4fdff1acc6(
    *,
    value: typing.Union[SyntheticsTestBrowserStepParamsElementUserLocatorValue, typing.Dict[builtins.str, typing.Any]],
    fail_test_on_cannot_locate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__423845ef8ecfbccbeab5a36bdf8a046102c68fcde14d800ebd92f12d03cb5a8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b440170022a2f749c6302066935fe7f4ff119bbd95189dbc41bca8805c0eb15e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da61494c842471b1a4d07d899542648cdf587c38d11a671d4f77d14fe1e35e3a(
    value: typing.Optional[SyntheticsTestBrowserStepParamsElementUserLocator],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354c42baed2b65beec0e41a15875f555e18e99ee00b509d802d33b2272a11c11(
    *,
    value: builtins.str,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd46900df8cfa32cca6e4a22da5054b1bd41e993da22680f3e76f01b17b8e93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10b6ae149fea9edc0e8e6c09d6aef69c9072cbabc920cee283926f1e539316a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d128dda7f6f5660a7a1496cf9df4128f76bcee3826e1e29fd4ed16b70cdd0436(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e71d9b7b73087259a9931952c23180cb9cded841e184ff4bd1a474020f88f5(
    value: typing.Optional[SyntheticsTestBrowserStepParamsElementUserLocatorValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab273075f0ea7fcaebf406465eda6dc1091571617a96a7802ec0e0c968570269(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d305220aadd56a3f48ccfb5de5d3d84860f23280e654ae7999e6bd54cf3147(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef0b0e62d9e8e603295b4fe29be2c5cb204dd945d5675552b899f82c649b47b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7f055399751e5b8b826b9b757a528edc8edde497078270b86a7aef15238df84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d9dd433445fc803262bf4f9120dd65ae195ea2f9e692bfc2b7929dbceac895(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46bcad933b2dcd02890faaad4bc1b695f8a10bec3181ddb92cd250023e8a4c6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f2446a91058afcc1373344a7c27cacdb93c9d81351d9b7fe72df9585f8d7d6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c43e9fddf4adefb4f643a32b6973cb6bc19f3022cf393f94c2facf475cb3c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408db7762ac587d57b63224d404f80645f727b6ff93197dfdaa40bfcc673b234(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__808e6b76cc2a0a1ccd6aef422b5c4366f57a975227f626410afb5c720ea30f79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__743ab67f37f6996eccd110c51fde4e78c76102c0c29e9e17db2962b156eb6d05(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__968d86286b4914ab0e29dd2dc7a6605e9fc94514d743094e17ade549ab287b89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bca409249f67d08abaf9760f86beb737fbef47963cd7132fbae3c0de88adf64c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba6377caad7c5f24fa946db7d904dc60e5cebfa006675343c6c1ad513a84841(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df2abf4a4994c6b4a00dcc45c65fedeca495df411ba477ad4c38678f7e709acb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__216faeb1182592eb5c29060719b5e34cd03d9b9d46c8f42169df8e6b8181a546(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f30b20f516acee825f40b0217bff49ffe46857cfd32df753e89735c74e4b90(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ccbca395b62a0d30d7c03c46958e05ca5a18b92662637a6e397dbc5d17a38e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dfd0b1c86e04ddfb827046b19b8d74dbbc8c1b8e69caca8f9f8f4da4607f7da(
    value: typing.Optional[SyntheticsTestBrowserStepParams],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5905942d5b76c4cbe0b6d4672c950c27c4cf4ee3b85dfc9069a6d67b4f1a3dc(
    *,
    example: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8287eaef396e286cca42d0dee07f04c5d4959ff2c4268038f13c7c45f536619d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63d518bc24c6bae7be7f778f2fb2ca36733d8a51925a56ba668b9b6e800549cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a8ba732d65a17e139a0fbae04a115b9b74cb2fbdfeff60840068dcbf41c44a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f95a65cfb4627f11df2e57ec738d34dbdcd735a11c033ddb05c67f827e6fdf05(
    value: typing.Optional[SyntheticsTestBrowserStepParamsVariable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d0aa4fe874f2e5ba5ae360f344c13b5104fb4eba24a6a54f4992aa80c4a168b(
    *,
    name: builtins.str,
    type: builtins.str,
    example: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    pattern: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1b002a2a3aaa14b3c5bc79edc6ae7a7a2bf29ff25022c3f95333801d67443c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44f19aee4b2a491e15a397468de2f906eb3da9618b754fca07f8c631a8e71cc3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f872764b7cc5b5bfaa56ec1d3f90f994ab1bf35d278d895c4fe1c384c6baec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae7b7e5248a7803e8a01069889b0512599d5a912ba0181455797220e3cd75a8b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415931a750780f3980c507a1bc0ac2058bf664f6647b7d01b08a4f6e3cce06d6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d1953e929a96086009a59ed23f2040f4c073edf5842cc1d153085c88f849d89(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestBrowserVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b04fbc27bef9bbdcafe5a62b3e1d64cc27109f58b7ac1229b9fdf8ab815f5b50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5ae2055780951f59b884518c8346f6c788e8b3d68ef4c26b780c4a1b213e37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66fb5f6e38bff66acfeb3045151b08ddd10dfe1cab3c5cdac7e21fc87880bf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e80486ee4e75f8962f31659133729d3f2b40d2edda5a92c3b40668b85b9c637d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6cae8e08beca20df2edd49e4a4180f6952a24a85aa57b64f621758aac328596(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96f2c9687923ddc9d146ff68bf131159b41ef1847b3fcb67817eb5ef4378b0bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__639aea83478bb9a62d10bf266b222833df27e9eaf7e919d0c5b521a8b4246ed3(
    value: typing.Optional[typing.Union[SyntheticsTestBrowserVariable, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0124c6c0dcd84fb2da5fd40130e734693b855c839f751073a8186ebff14a8481(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    locations: typing.Sequence[builtins.str],
    name: builtins.str,
    status: builtins.str,
    type: builtins.str,
    api_step: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestApiStep, typing.Dict[builtins.str, typing.Any]]]]] = None,
    assertion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestAssertion, typing.Dict[builtins.str, typing.Any]]]]] = None,
    browser_step: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestBrowserStep, typing.Dict[builtins.str, typing.Any]]]]] = None,
    browser_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestBrowserVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    config_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsTestConfigVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    device_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
    options_list: typing.Optional[typing.Union[SyntheticsTestOptionsList, typing.Dict[builtins.str, typing.Any]]] = None,
    request_basicauth: typing.Optional[typing.Union[SyntheticsTestRequestBasicauth, typing.Dict[builtins.str, typing.Any]]] = None,
    request_client_certificate: typing.Optional[typing.Union[SyntheticsTestRequestClientCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    request_definition: typing.Optional[typing.Union[SyntheticsTestRequestDefinition, typing.Dict[builtins.str, typing.Any]]] = None,
    request_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    request_proxy: typing.Optional[typing.Union[SyntheticsTestRequestProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    request_query: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    set_cookie: typing.Optional[builtins.str] = None,
    subtype: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc81652e39c08ef70de8f9af7578b19d8491953961a9b658d4cd4ce1513ad980(
    *,
    name: builtins.str,
    type: builtins.str,
    example: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    pattern: typing.Optional[builtins.str] = None,
    secure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdfb6ee78af081f7330a2703987d1a54b7951102c14a1dea49070faaf318a8fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9915db1bde04681fe11a56bd209848ae0ab852575c9620f93ef114ec5ef226c5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a40a387de5d8ffeebbde70cdef575dd47b1c8eb2759103e04b3975e256bd50f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91827bb9499c63cc4e8e2c3c67bf69fe76a1b3641cd78c7f510fec0843532fd5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c9c9c17d582b09a5ae428cd456fb2565e32b6e9bbaae90da30e71ec725ccce(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab406c2b919858e8dae21f82430aef3c902cd567e5a50ea9ab5a287823628c20(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsTestConfigVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34cc0e71b634067cc4f9796dc84c967f0557380898f91aeed3a7a6690f71ae20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf651112d71ebeec49217eb92719718e46f89ec3e300218f5bddb4eba71d9c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__040c59b88e79d1a92cfa4503e4443913ca2febc2d744149ebd006987aa4dd2f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83cba13412184e314f736f37ca293e3a5624e76ee5c536faa0c88fee44af069b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__774ea0cdfdbc2cdbd9919609f1b76e90e49cde88647115c20b86c4d6699b27e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e068641b65ab84e0b5171344cab1014834825ca36e99ec8434c9d0051b39928(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84b369c8315ccc4927e11b51545d75035789c41a7b6177221923af78c0f5508e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b444e981176453dd5e922485f7598e82982d7d82eac74baa256f9087a7387d2(
    value: typing.Optional[typing.Union[SyntheticsTestConfigVariable, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__669a64b0c857b3913f6e1304a3b7506ac7351d32b12a1e69230b0fd453c12cb3(
    *,
    tick_every: jsii.Number,
    accept_self_signed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    check_certificate_revocation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ci: typing.Optional[typing.Union[SyntheticsTestOptionsListCi, typing.Dict[builtins.str, typing.Any]]] = None,
    disable_cors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_csp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    follow_redirects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ignore_server_certificate_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    initial_navigation_timeout: typing.Optional[jsii.Number] = None,
    min_failure_duration: typing.Optional[jsii.Number] = None,
    min_location_failed: typing.Optional[jsii.Number] = None,
    monitor_name: typing.Optional[builtins.str] = None,
    monitor_options: typing.Optional[typing.Union[SyntheticsTestOptionsListMonitorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor_priority: typing.Optional[jsii.Number] = None,
    no_screenshot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restricted_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    retry: typing.Optional[typing.Union[SyntheticsTestOptionsListRetry, typing.Dict[builtins.str, typing.Any]]] = None,
    rum_settings: typing.Optional[typing.Union[SyntheticsTestOptionsListRumSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0093f6a14d51c2ea4e6d07755ef1fdafdd0b8b9df89ddaf3c83bdcead75f6b1(
    *,
    execution_rule: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19dc18ffff3c28626a3ab5e54dfa0b075dcc1a4dcf28e82041cbb2dd81cf3f9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba5b924c0c2d71661d383ccc52c435dbd5dcd79f3c3c4418a73cb9892f64373(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47321aa9e00a826069fb1c7aac4298bbab4283eba826267c5444050e93a55c8a(
    value: typing.Optional[SyntheticsTestOptionsListCi],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28889328257d49fcc4bc5f51ec63aed2902e3d925d40bd6ed9edf1ec9b7ee0ce(
    *,
    renotify_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a1921fbce298cc6bd737c1910a355f48832cb4290fc1790935025a679d17796(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ea4912ea852f77f5a70fa8fe028724b531792a135395e2a3f8ca89643afe9d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d8efaa9b18bd9c319279983db5109ac1996e2195bb489b733584961c476cda0(
    value: typing.Optional[SyntheticsTestOptionsListMonitorOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a25caa898b8d54783108c1e76beb3e94a916048730439ebeaa41e3f9b5f518(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d8cc461b8a175588b2371ab85da744cfbc1d28ee657a764ce99696f6fe5abf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906fce1953d4c28ba2f11353abb9b392caddd0f4f980b25309db51dd0c9a9c61(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32c3a7384117855a7c629b949b1de291a32e238f72ddd1c7a4c2a1e5ad2767b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9a91a7f15f54a36f8146eca988c4c423d2799b508f48b6ff93b1e74c6d04d6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a828f2f2bef55b4cd3c79f4d8b6c47f3bafb288b6938e80503c908fc12c870(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00b97833d2dbef78a26064a602de75790e95112e4b030781b0f2cea9fff5bfa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11b2b2eae7abfbcdbdd9ded17ab8fb42540bf2a3224afc34a660b3b94d2298f7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085bad40cf3518fd9cdc565cec5e66f2fee9b8e86b76d6fcd7b0b53079c40420(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81380c6e2b43101946551969262f72f5bfbedbf1c9264024d140575cdb54869(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d814b7fd09e8de93d2029a5aa5775ab294dad5122009f972d6f33cf8a3f27aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604143bda0c23e6b2265036f1a03f897d17524780be0282b7a53c5bfa9b01eb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__540f0fa4d54daea7a660a4e69ca7bc1626abdf616ea9ef3fc8daaae0dba94932(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__068da975e3df412bc6fb59c03e825c41a7d5af36551c532ce316775c83fb2bf5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9908b06b86576577772fe00d5df0be963b39c1142a17f9e6aeb9f196f1bd86(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82e67e70c1e41308d26d3e1f4fd1c484ab3ab7b8ec6a7bd1a73ee6bce9579811(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f92ac44590f538d77cdce4d44de1454c856fc44753f6ddfa1fc43ab723ed6343(
    value: typing.Optional[SyntheticsTestOptionsList],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa0df52a234c3b47310cd58b4e593d79f53079a82be095d4e9a400d73721761(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f7a6dd118f08f139e5f7bad453d6db56808e858890e590831c06ea0b67d9b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf87c3848106f26b72761924188bfa8e1c621d5ff50f56303b3917d77ba3f61b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff86c0adf51363ef99f59806789280e4240ed96cb474f0d1c10bedfbbde53231(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ede7c007211f47688090c465f761136621636b662b5e7d5d74b059ea4c946b80(
    value: typing.Optional[SyntheticsTestOptionsListRetry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b5f4754bdd2637d48c2b54704c64d2e1663b2f709176c1af7d043ac9495d03(
    *,
    is_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    application_id: typing.Optional[builtins.str] = None,
    client_token_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20d8766d459895f2e980c5ddba256e3843de943850f16b95e656f4654ff07697(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea5e89582a6b6c11aaa9c5cf42d77175ec3fe0cd96be735cc5ec3e0565e572f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e9a4e989e3e37e049769b11072525a15aad3d74e73e59e35fb80fa832a2a53(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac0c828c4a937c80fe94ec79a2ceff1e6ad10dcba147d9b749326fc9a6afc9d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1663cc5a33c5ad00036ef45aeb874a10a96854513a0a61fb3ae644a5a5bddd8(
    value: typing.Optional[SyntheticsTestOptionsListRumSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc5a48ceb2c2bf2e059d12af9f1e014c367434553afc8a2394e787c56f997510(
    *,
    access_key: typing.Optional[builtins.str] = None,
    access_token_url: typing.Optional[builtins.str] = None,
    audience: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    domain: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    secret_key: typing.Optional[builtins.str] = None,
    service_name: typing.Optional[builtins.str] = None,
    session_token: typing.Optional[builtins.str] = None,
    token_api_authentication: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
    workstation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f363a63fbb7d68690675b82d7ad4db22a093e8e160bade2261774912d98e56a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94cc4b8bb46ad62c603abf3f8028422298f7a9faf7ff70dee270ef76c40745d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__407a74a9aa67b584155db592c566d50a22c93c7c2b70873d8bb9c4bf872c9798(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10646dc290f3bbd55e5ededee9d22783f2140b08cecc8afd452df8c3f8d01420(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81e6e2d2fbb236f8d2c62a79fc3eba04c547e916ef5ca6c1fbd60a031567c41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b30c5298a2ac1df214317c680f8dd0b634bfeba782bab17d0c0bc6642a109425(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9942ea490170d591200dd0804d13d7e99ca8903c6eabb18bdee2e9ad769f92ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e94ea991cb0b0161a981eab801a6abec63fe826fd9c0df2727d633094cc39894(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f69d7d1a7913259b72f2876586a2160743c54c21c4b32f5b5b66982c1f91fad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1752cc6b54989a3068f906c57912c83e2a9a362df18b3c294b1bc64d4c324959(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83510ed49c02884cf544baf531d7c220151f65e5d54467dd53e42477f1b3958b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4455d75e86816f958c532b039686600adcc98f3e19fac180c2fedfbdac84f38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3bc20ecdeb6b3599a72423380e50d3b3eb5a93edd426fabf3c1fbd3cef5dd99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae5327fb3fc4f29c1fbdfc192c6fecaeaea59ee8474835e02e63edee700ddb62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b95996946838d7be31670b5b7a69ca242605c9107c8461514438e0a14f64ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8014a17c1d3c93819422ad6e35b3919072910c3bb9a007c3b9af7115c9576bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635919ce63a9985f4ebd45e24b71fec931136896f5342f9d52c8b31eecaff218(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bbd253c6d10687001a5a9932a031b75098c35f3e0adff5b6c69fb720d26ed56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a5530de0dfafbde27168d25cb0a83eb70d80e7127ea53e65211f99be46a0e73(
    value: typing.Optional[SyntheticsTestRequestBasicauth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92195cebae295ffd60c183c12604e2c5eb3c23f1c1e9b54c1d9796fb96b11f15(
    *,
    cert: typing.Union[SyntheticsTestRequestClientCertificateCert, typing.Dict[builtins.str, typing.Any]],
    key: typing.Union[SyntheticsTestRequestClientCertificateKey, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e334ed395f958380ee046623f4875bfa101e3334814a9ed13404290a242541c(
    *,
    content: builtins.str,
    filename: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b5f952859c609ed3e93e67f4181cd3f22f2f1275d641fb258e3b6bc8d099fc0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73393d74b4e4061530a65b78a3e40a4594d9eb6ca71459fc714d79bb035fdbd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a291051fd7f0140080a06f6aebf3844d786d01d80c4bb74fc6d48047e69bbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b0acfa47ff2e9b82a4088756078469055d3f998b6de0477cf1b1b57b0c8bb93(
    value: typing.Optional[SyntheticsTestRequestClientCertificateCert],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a570294e7d1b0d895e81a649f5fe9c23706cbfc8e04a38bc11740b39131df81(
    *,
    content: builtins.str,
    filename: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0f4c3f898aa6e85acba9c04d949ab52f77462060e953fba560946384c5b39c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8c8703066db497694006d4e4071b415c9e2789583af8c9cc66794756c52c3c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b40190193b767a3a35768dfc650f07900182adb89c5351f1b7002dc9a030c24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad54a6bbe9199c690a5ac54428ae67e07a7433c3b788c1b373c7cdda2eb6ca2(
    value: typing.Optional[SyntheticsTestRequestClientCertificateKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad658790366cf2cdb8d801c83309677b409846ce2dd0ec6f93a1e55d6d8a118(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92d1b6d4c7268836db8c63ffbb98fb8a9768414a1a1b52137aae6b7ef0daa3ac(
    value: typing.Optional[SyntheticsTestRequestClientCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__204293cab905ee980b5021cd7bf01428689590962f898e248e4cc2fbd637f571(
    *,
    body: typing.Optional[builtins.str] = None,
    body_type: typing.Optional[builtins.str] = None,
    call_type: typing.Optional[builtins.str] = None,
    certificate_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    dns_server: typing.Optional[builtins.str] = None,
    dns_server_port: typing.Optional[jsii.Number] = None,
    host: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
    method: typing.Optional[builtins.str] = None,
    no_saving_response_body: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    number_of_packets: typing.Optional[jsii.Number] = None,
    port: typing.Optional[jsii.Number] = None,
    servername: typing.Optional[builtins.str] = None,
    service: typing.Optional[builtins.str] = None,
    should_track_hops: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36aa03cfb1c3398ad404a394652bb2ab0cd375f4f4567d469863d2cdabe567b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b775df52ec9346c8a0e9d4ab191e27f3f1e2dc5a7585507f77fd2476c3b5d792(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__808a9591c14b9ef47e341dee25bc7fb9e2a5e1d7d0f58f9a6adf9241918406a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adac81cc4e3abde0ba49034c80787798692121808f9964f3bc3f28a66f138d12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf6f7043810ac439cf85763a5019a75e857d7b489416d934a09a083231b2e4c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3994fd35b4fe62230ea33649addbbdd86812627166f81ba22b064de26760d53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9640d8050d592db99c22416188d3035894cd40d5e3646229b589734fac42d38e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a4f0c6174cbb4b763aaef193137d64359f5e842ba752e7c62cea9d8908032c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db6015c8a31e1bb1b5ec89bdc862b8f7366f13d50ea25e112b53c2768563a813(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada67fa8780d9dd378b02aedee0a5a43deafd5a586cf8329e20b1ae99f7650c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7862dc9e184ae4b8e194a92fad7bd5cd6e73d5bba3f67b702aa9c8984975752(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e701488b2ba01d49f7157c6c28979cc93e0627367a84c79528949cbc0684930a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71cab03288c12d040b75d4e3855bdbb2c5706162ce0d0d4e444778e58b844d9c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c29d94389a8df406db7046a6b8b138499c88af59197859b0a220e29232082347(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8224cb65c273862c114b1db8311074a1a7d2e7644d6c37454099855828d9edf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66cedd9c86a2237f60a473434b50472f830d4a64b531a94a4ea82e99af263b5f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f44aaab3cf698ca7598ddfaab38e7ea8da8bdc0a789a777689b4c3658ffc8c8d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6973962187880a1655e5b0605745e3270409c5ada28e1ac9168ae978a91925a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3cadac8db57ad6ea83ba41fdcc3ff2f70eeaebf49aec72bee831f9b8378e751(
    value: typing.Optional[SyntheticsTestRequestDefinition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c92f485264d91a1bc9f0464a9a0f1d2117e4d99f4e8c921299594e1a03fdb768(
    *,
    url: builtins.str,
    headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d9c8d80f5f5336878542c371e983b5e286693a042ecf66131f715368da22be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec209dd97b5593b2bc44acec5b8648f09ea70c5fa8875be1ba2b651a4e074565(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b1b4216953940b5c3072664cb093496150b4a0d2ca29e33d3720178557b362(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3a723a9f31d4b772e505fb5b9c826a969a0e915b983f6175f2f5153a78a596f(
    value: typing.Optional[SyntheticsTestRequestProxy],
) -> None:
    """Type checking stubs"""
    pass
