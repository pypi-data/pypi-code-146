'''
# `newrelic_cloud_aws_integrations`

Refer to the Terraform Registory for docs: [`newrelic_cloud_aws_integrations`](https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations).
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


class CloudAwsIntegrations(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrations",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations newrelic_cloud_aws_integrations}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        linked_account_id: jsii.Number,
        account_id: typing.Optional[jsii.Number] = None,
        billing: typing.Optional[typing.Union["CloudAwsIntegrationsBilling", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudtrail: typing.Optional[typing.Union["CloudAwsIntegrationsCloudtrail", typing.Dict[builtins.str, typing.Any]]] = None,
        doc_db: typing.Optional[typing.Union["CloudAwsIntegrationsDocDb", typing.Dict[builtins.str, typing.Any]]] = None,
        health: typing.Optional[typing.Union["CloudAwsIntegrationsHealth", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        s3: typing.Optional[typing.Union["CloudAwsIntegrationsS3", typing.Dict[builtins.str, typing.Any]]] = None,
        trusted_advisor: typing.Optional[typing.Union["CloudAwsIntegrationsTrustedAdvisor", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[typing.Union["CloudAwsIntegrationsVpc", typing.Dict[builtins.str, typing.Any]]] = None,
        x_ray: typing.Optional[typing.Union["CloudAwsIntegrationsXRay", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations newrelic_cloud_aws_integrations} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param linked_account_id: The ID of the linked AWS account in New Relic. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#linked_account_id CloudAwsIntegrations#linked_account_id}
        :param account_id: The ID of the account in New Relic. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#account_id CloudAwsIntegrations#account_id}
        :param billing: billing block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#billing CloudAwsIntegrations#billing}
        :param cloudtrail: cloudtrail block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#cloudtrail CloudAwsIntegrations#cloudtrail}
        :param doc_db: doc_db block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#doc_db CloudAwsIntegrations#doc_db}
        :param health: health block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#health CloudAwsIntegrations#health}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#id CloudAwsIntegrations#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param s3: s3 block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#s3 CloudAwsIntegrations#s3}
        :param trusted_advisor: trusted_advisor block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#trusted_advisor CloudAwsIntegrations#trusted_advisor}
        :param vpc: vpc block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#vpc CloudAwsIntegrations#vpc}
        :param x_ray: x_ray block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#x_ray CloudAwsIntegrations#x_ray}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__218636da2f5c84b07b8f11f887c728956d546cee837b90d553762da5832a9fd8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudAwsIntegrationsConfig(
            linked_account_id=linked_account_id,
            account_id=account_id,
            billing=billing,
            cloudtrail=cloudtrail,
            doc_db=doc_db,
            health=health,
            id=id,
            s3=s3,
            trusted_advisor=trusted_advisor,
            vpc=vpc,
            x_ray=x_ray,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putBilling")
    def put_billing(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsBilling(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putBilling", [value]))

    @jsii.member(jsii_name="putCloudtrail")
    def put_cloudtrail(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsCloudtrail(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putCloudtrail", [value]))

    @jsii.member(jsii_name="putDocDb")
    def put_doc_db(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsDocDb(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putDocDb", [value]))

    @jsii.member(jsii_name="putHealth")
    def put_health(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsHealth(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putHealth", [value]))

    @jsii.member(jsii_name="putS3")
    def put_s3(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsS3(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="putTrustedAdvisor")
    def put_trusted_advisor(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsTrustedAdvisor(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putTrustedAdvisor", [value]))

    @jsii.member(jsii_name="putVpc")
    def put_vpc(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_nat_gateway: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_vpn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_nat_gateway: Specify if NAT gateway should be monitored. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#fetch_nat_gateway CloudAwsIntegrations#fetch_nat_gateway}
        :param fetch_vpn: Specify if VPN should be monitored. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#fetch_vpn CloudAwsIntegrations#fetch_vpn}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsVpc(
            aws_regions=aws_regions,
            fetch_nat_gateway=fetch_nat_gateway,
            fetch_vpn=fetch_vpn,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putVpc", [value]))

    @jsii.member(jsii_name="putXRay")
    def put_x_ray(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsXRay(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putXRay", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetBilling")
    def reset_billing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBilling", []))

    @jsii.member(jsii_name="resetCloudtrail")
    def reset_cloudtrail(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudtrail", []))

    @jsii.member(jsii_name="resetDocDb")
    def reset_doc_db(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocDb", []))

    @jsii.member(jsii_name="resetHealth")
    def reset_health(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealth", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

    @jsii.member(jsii_name="resetTrustedAdvisor")
    def reset_trusted_advisor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedAdvisor", []))

    @jsii.member(jsii_name="resetVpc")
    def reset_vpc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpc", []))

    @jsii.member(jsii_name="resetXRay")
    def reset_x_ray(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXRay", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="billing")
    def billing(self) -> "CloudAwsIntegrationsBillingOutputReference":
        return typing.cast("CloudAwsIntegrationsBillingOutputReference", jsii.get(self, "billing"))

    @builtins.property
    @jsii.member(jsii_name="cloudtrail")
    def cloudtrail(self) -> "CloudAwsIntegrationsCloudtrailOutputReference":
        return typing.cast("CloudAwsIntegrationsCloudtrailOutputReference", jsii.get(self, "cloudtrail"))

    @builtins.property
    @jsii.member(jsii_name="docDb")
    def doc_db(self) -> "CloudAwsIntegrationsDocDbOutputReference":
        return typing.cast("CloudAwsIntegrationsDocDbOutputReference", jsii.get(self, "docDb"))

    @builtins.property
    @jsii.member(jsii_name="health")
    def health(self) -> "CloudAwsIntegrationsHealthOutputReference":
        return typing.cast("CloudAwsIntegrationsHealthOutputReference", jsii.get(self, "health"))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(self) -> "CloudAwsIntegrationsS3OutputReference":
        return typing.cast("CloudAwsIntegrationsS3OutputReference", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="trustedAdvisor")
    def trusted_advisor(self) -> "CloudAwsIntegrationsTrustedAdvisorOutputReference":
        return typing.cast("CloudAwsIntegrationsTrustedAdvisorOutputReference", jsii.get(self, "trustedAdvisor"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> "CloudAwsIntegrationsVpcOutputReference":
        return typing.cast("CloudAwsIntegrationsVpcOutputReference", jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="xRay")
    def x_ray(self) -> "CloudAwsIntegrationsXRayOutputReference":
        return typing.cast("CloudAwsIntegrationsXRayOutputReference", jsii.get(self, "xRay"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="billingInput")
    def billing_input(self) -> typing.Optional["CloudAwsIntegrationsBilling"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsBilling"], jsii.get(self, "billingInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudtrailInput")
    def cloudtrail_input(self) -> typing.Optional["CloudAwsIntegrationsCloudtrail"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsCloudtrail"], jsii.get(self, "cloudtrailInput"))

    @builtins.property
    @jsii.member(jsii_name="docDbInput")
    def doc_db_input(self) -> typing.Optional["CloudAwsIntegrationsDocDb"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsDocDb"], jsii.get(self, "docDbInput"))

    @builtins.property
    @jsii.member(jsii_name="healthInput")
    def health_input(self) -> typing.Optional["CloudAwsIntegrationsHealth"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsHealth"], jsii.get(self, "healthInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedAccountIdInput")
    def linked_account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "linkedAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(self) -> typing.Optional["CloudAwsIntegrationsS3"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsS3"], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="trustedAdvisorInput")
    def trusted_advisor_input(
        self,
    ) -> typing.Optional["CloudAwsIntegrationsTrustedAdvisor"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsTrustedAdvisor"], jsii.get(self, "trustedAdvisorInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcInput")
    def vpc_input(self) -> typing.Optional["CloudAwsIntegrationsVpc"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsVpc"], jsii.get(self, "vpcInput"))

    @builtins.property
    @jsii.member(jsii_name="xRayInput")
    def x_ray_input(self) -> typing.Optional["CloudAwsIntegrationsXRay"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsXRay"], jsii.get(self, "xRayInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5219cec395e62e4e80020a1434f822e106636205b1c60eb208915ae3fb2ebcc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53bc997685d6f8091c1aeb3bc838d3517467f180193964c59a5ff4dec857a6d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="linkedAccountId")
    def linked_account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "linkedAccountId"))

    @linked_account_id.setter
    def linked_account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__947ffbc6d56f727b440fd8f8118b85c3b51c796e2061df9d54dc4f7e8a8ac873)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedAccountId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsBilling",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudAwsIntegrationsBilling:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e9ccb32fc89d2507f407cef214d9b76981c4a2617faf94bdbaa95a6ca60f3d7)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsBilling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsBillingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsBillingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a62b82999bd05c07ebf66e82fc1cd50209c887f3e8d6dc616b8642f2880f4679)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5dcbb93b5a3ec7ecb2b967fb94b1d9617184e309d8b240bc3497a0639781d84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsBilling]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsBilling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsBilling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d9b69b3eb4d71e529ac6b4536b8ceaaf0ec2e61eb0d3064868b86777f85484d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsCloudtrail",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsCloudtrail:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9133ba564bcdd8e4779348d80ab1c85ac796b37f55e670dd76c7e2d6c8aa73fb)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsCloudtrail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsCloudtrailOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsCloudtrailOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b6ddf9f2bfcf0c0e767bae6f5221261f7773891ee8bb2cb0935bb827b27f74a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a8e5ffa65cec1a9d99267d29a7d0df8763911839b2c7fc3ec6b822357589d34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value)

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ac2025d900c573c9470c10047d81f45e617e5ba44b85dab88d0e5f8141da6b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsCloudtrail]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsCloudtrail], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsCloudtrail],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2520ae8e39751ad9964fa5eb5ebc623daec32d6e9e54c03ba08593b5e99b0f82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "linked_account_id": "linkedAccountId",
        "account_id": "accountId",
        "billing": "billing",
        "cloudtrail": "cloudtrail",
        "doc_db": "docDb",
        "health": "health",
        "id": "id",
        "s3": "s3",
        "trusted_advisor": "trustedAdvisor",
        "vpc": "vpc",
        "x_ray": "xRay",
    },
)
class CloudAwsIntegrationsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        linked_account_id: jsii.Number,
        account_id: typing.Optional[jsii.Number] = None,
        billing: typing.Optional[typing.Union[CloudAwsIntegrationsBilling, typing.Dict[builtins.str, typing.Any]]] = None,
        cloudtrail: typing.Optional[typing.Union[CloudAwsIntegrationsCloudtrail, typing.Dict[builtins.str, typing.Any]]] = None,
        doc_db: typing.Optional[typing.Union["CloudAwsIntegrationsDocDb", typing.Dict[builtins.str, typing.Any]]] = None,
        health: typing.Optional[typing.Union["CloudAwsIntegrationsHealth", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        s3: typing.Optional[typing.Union["CloudAwsIntegrationsS3", typing.Dict[builtins.str, typing.Any]]] = None,
        trusted_advisor: typing.Optional[typing.Union["CloudAwsIntegrationsTrustedAdvisor", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[typing.Union["CloudAwsIntegrationsVpc", typing.Dict[builtins.str, typing.Any]]] = None,
        x_ray: typing.Optional[typing.Union["CloudAwsIntegrationsXRay", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param linked_account_id: The ID of the linked AWS account in New Relic. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#linked_account_id CloudAwsIntegrations#linked_account_id}
        :param account_id: The ID of the account in New Relic. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#account_id CloudAwsIntegrations#account_id}
        :param billing: billing block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#billing CloudAwsIntegrations#billing}
        :param cloudtrail: cloudtrail block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#cloudtrail CloudAwsIntegrations#cloudtrail}
        :param doc_db: doc_db block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#doc_db CloudAwsIntegrations#doc_db}
        :param health: health block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#health CloudAwsIntegrations#health}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#id CloudAwsIntegrations#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param s3: s3 block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#s3 CloudAwsIntegrations#s3}
        :param trusted_advisor: trusted_advisor block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#trusted_advisor CloudAwsIntegrations#trusted_advisor}
        :param vpc: vpc block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#vpc CloudAwsIntegrations#vpc}
        :param x_ray: x_ray block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#x_ray CloudAwsIntegrations#x_ray}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(billing, dict):
            billing = CloudAwsIntegrationsBilling(**billing)
        if isinstance(cloudtrail, dict):
            cloudtrail = CloudAwsIntegrationsCloudtrail(**cloudtrail)
        if isinstance(doc_db, dict):
            doc_db = CloudAwsIntegrationsDocDb(**doc_db)
        if isinstance(health, dict):
            health = CloudAwsIntegrationsHealth(**health)
        if isinstance(s3, dict):
            s3 = CloudAwsIntegrationsS3(**s3)
        if isinstance(trusted_advisor, dict):
            trusted_advisor = CloudAwsIntegrationsTrustedAdvisor(**trusted_advisor)
        if isinstance(vpc, dict):
            vpc = CloudAwsIntegrationsVpc(**vpc)
        if isinstance(x_ray, dict):
            x_ray = CloudAwsIntegrationsXRay(**x_ray)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc3ac5886f8796b4cd2e377d13a118f9277a15b3d6884b09bb067e13e9f18b87)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument linked_account_id", value=linked_account_id, expected_type=type_hints["linked_account_id"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument billing", value=billing, expected_type=type_hints["billing"])
            check_type(argname="argument cloudtrail", value=cloudtrail, expected_type=type_hints["cloudtrail"])
            check_type(argname="argument doc_db", value=doc_db, expected_type=type_hints["doc_db"])
            check_type(argname="argument health", value=health, expected_type=type_hints["health"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument trusted_advisor", value=trusted_advisor, expected_type=type_hints["trusted_advisor"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument x_ray", value=x_ray, expected_type=type_hints["x_ray"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "linked_account_id": linked_account_id,
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
        if account_id is not None:
            self._values["account_id"] = account_id
        if billing is not None:
            self._values["billing"] = billing
        if cloudtrail is not None:
            self._values["cloudtrail"] = cloudtrail
        if doc_db is not None:
            self._values["doc_db"] = doc_db
        if health is not None:
            self._values["health"] = health
        if id is not None:
            self._values["id"] = id
        if s3 is not None:
            self._values["s3"] = s3
        if trusted_advisor is not None:
            self._values["trusted_advisor"] = trusted_advisor
        if vpc is not None:
            self._values["vpc"] = vpc
        if x_ray is not None:
            self._values["x_ray"] = x_ray

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
    def linked_account_id(self) -> jsii.Number:
        '''The ID of the linked AWS account in New Relic.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#linked_account_id CloudAwsIntegrations#linked_account_id}
        '''
        result = self._values.get("linked_account_id")
        assert result is not None, "Required property 'linked_account_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of the account in New Relic.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#account_id CloudAwsIntegrations#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def billing(self) -> typing.Optional[CloudAwsIntegrationsBilling]:
        '''billing block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#billing CloudAwsIntegrations#billing}
        '''
        result = self._values.get("billing")
        return typing.cast(typing.Optional[CloudAwsIntegrationsBilling], result)

    @builtins.property
    def cloudtrail(self) -> typing.Optional[CloudAwsIntegrationsCloudtrail]:
        '''cloudtrail block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#cloudtrail CloudAwsIntegrations#cloudtrail}
        '''
        result = self._values.get("cloudtrail")
        return typing.cast(typing.Optional[CloudAwsIntegrationsCloudtrail], result)

    @builtins.property
    def doc_db(self) -> typing.Optional["CloudAwsIntegrationsDocDb"]:
        '''doc_db block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#doc_db CloudAwsIntegrations#doc_db}
        '''
        result = self._values.get("doc_db")
        return typing.cast(typing.Optional["CloudAwsIntegrationsDocDb"], result)

    @builtins.property
    def health(self) -> typing.Optional["CloudAwsIntegrationsHealth"]:
        '''health block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#health CloudAwsIntegrations#health}
        '''
        result = self._values.get("health")
        return typing.cast(typing.Optional["CloudAwsIntegrationsHealth"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#id CloudAwsIntegrations#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3(self) -> typing.Optional["CloudAwsIntegrationsS3"]:
        '''s3 block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#s3 CloudAwsIntegrations#s3}
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional["CloudAwsIntegrationsS3"], result)

    @builtins.property
    def trusted_advisor(self) -> typing.Optional["CloudAwsIntegrationsTrustedAdvisor"]:
        '''trusted_advisor block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#trusted_advisor CloudAwsIntegrations#trusted_advisor}
        '''
        result = self._values.get("trusted_advisor")
        return typing.cast(typing.Optional["CloudAwsIntegrationsTrustedAdvisor"], result)

    @builtins.property
    def vpc(self) -> typing.Optional["CloudAwsIntegrationsVpc"]:
        '''vpc block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#vpc CloudAwsIntegrations#vpc}
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional["CloudAwsIntegrationsVpc"], result)

    @builtins.property
    def x_ray(self) -> typing.Optional["CloudAwsIntegrationsXRay"]:
        '''x_ray block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#x_ray CloudAwsIntegrations#x_ray}
        '''
        result = self._values.get("x_ray")
        return typing.cast(typing.Optional["CloudAwsIntegrationsXRay"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsDocDb",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudAwsIntegrationsDocDb:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b58ef8635db36e48a559b28b40b82ec4dd41bcbf964598d8e8c2610059fab98)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsDocDb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsDocDbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsDocDbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1ceccfccb2c01b0f9212f0432a797550e67fbdd0276877c6b924299041c1031)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0251404e38849d33ade8e61fb4a4f375b9f0abdad07106312e45c3d4b21750a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsDocDb]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsDocDb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsDocDb]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bc4f66bc4ff0d503483eee5301c5ff5f022809adb60e47f7984abedc805bb6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsHealth",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudAwsIntegrationsHealth:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c219d859d9fa6c3f00149ad1692a19b0b2ab9eec6f51eacdd9731529b70b36)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsHealth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsHealthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsHealthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f86711bd01ca429e5db58f084e73315a1b7be773c21e46bb74a94ed2a1845097)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b2e7878d24eba1730c9b8637f82d3912d9cab70e21be12e9c6003a465cd62f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsHealth]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsHealth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsHealth],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24de463ea31715daafca9d6f499d395e152ac71f03aea5f4055fc70ff230ee33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsS3",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudAwsIntegrationsS3:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ab9b96b00818e6013fe2103e98626b3ebfb0e15dda0b7f25488ae4ca0a47e8)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsS3OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9e785c94925ae01e650b7ed9f3f0da5e0411ad1fc02448a3cc694243e0db6dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6039bca92dc66d6f16736123bcf25b9ff1cdd5a6c24ea16785e120d7afc838d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsS3]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsS3], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsS3]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__683ccb60ceff40081ecf5543bc48e2f1fe43c3201e15763be3993daa3aa831cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsTrustedAdvisor",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudAwsIntegrationsTrustedAdvisor:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__668858f73919a08f504c8a90bb65ffb65bc1d01d05572ddba939811087652a14)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsTrustedAdvisor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsTrustedAdvisorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsTrustedAdvisorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8a147261cc3bf496a0e170a5e441607f620af5f12ed60056d946be7f8b8c0f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec4f346a457cb1508ddb025b8d144de7b4840241fc61fa8191b69cf6be3c6e85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsTrustedAdvisor]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsTrustedAdvisor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsTrustedAdvisor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4bc63cefa256d5b5346d16c3750a584927d393bdf9459dbab1f2801aa2c8f36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsVpc",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_nat_gateway": "fetchNatGateway",
        "fetch_vpn": "fetchVpn",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsVpc:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_nat_gateway: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_vpn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_nat_gateway: Specify if NAT gateway should be monitored. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#fetch_nat_gateway CloudAwsIntegrations#fetch_nat_gateway}
        :param fetch_vpn: Specify if VPN should be monitored. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#fetch_vpn CloudAwsIntegrations#fetch_vpn}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5a05e1712a6079eebfb1cebb9021117640ecdb1735fc94235af901ee1bb64db)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument fetch_nat_gateway", value=fetch_nat_gateway, expected_type=type_hints["fetch_nat_gateway"])
            check_type(argname="argument fetch_vpn", value=fetch_vpn, expected_type=type_hints["fetch_vpn"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if fetch_nat_gateway is not None:
            self._values["fetch_nat_gateway"] = fetch_nat_gateway
        if fetch_vpn is not None:
            self._values["fetch_vpn"] = fetch_vpn
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_nat_gateway(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if NAT gateway should be monitored.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#fetch_nat_gateway CloudAwsIntegrations#fetch_nat_gateway}
        '''
        result = self._values.get("fetch_nat_gateway")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fetch_vpn(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if VPN should be monitored.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#fetch_vpn CloudAwsIntegrations#fetch_vpn}
        '''
        result = self._values.get("fetch_vpn")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsVpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsVpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsVpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc03184763dca962a4a8ab314c5c148983b1f331637301224bdc278d238f3491)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetFetchNatGateway")
    def reset_fetch_nat_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchNatGateway", []))

    @jsii.member(jsii_name="resetFetchVpn")
    def reset_fetch_vpn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchVpn", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchNatGatewayInput")
    def fetch_nat_gateway_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchNatGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchVpnInput")
    def fetch_vpn_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchVpnInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__555e7d85f2e58ac7b541bacd19f13077a47af6954e80f4b40ac339755b9b7896)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value)

    @builtins.property
    @jsii.member(jsii_name="fetchNatGateway")
    def fetch_nat_gateway(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchNatGateway"))

    @fetch_nat_gateway.setter
    def fetch_nat_gateway(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b2657609fdf500a4e737b95dd4cc4b3d5550f0c3ef0c867e038437ea0e58637)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchNatGateway", value)

    @builtins.property
    @jsii.member(jsii_name="fetchVpn")
    def fetch_vpn(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchVpn"))

    @fetch_vpn.setter
    def fetch_vpn(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da72c88928d008dd41e6355c8234df0e259a01b0abb531818bb0b36c7caf2c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchVpn", value)

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9579bf68121b247cafa084f153862e870a9191414d93835d82fabaa96a992f14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value)

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac7fa1649a4d226ab4fb2c00a338e4d9911e66ca678b5bcc71bd5245e0bb120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value)

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ea2f558eb8f44587d62e70414f9e1cafca3e2ec1df4590a34f1a3d47499183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsVpc]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsVpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsVpc]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4ac68e78d33565f199421a44fdec8c9985ca38d90c14b0a0d05bbf25fe5b8d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsXRay",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsXRay:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8df10b2612d85d90190d8350575e635e7b3cef8ab626c415ebe5664e6ba53fa3)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsXRay(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsXRayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsXRayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a6346257c8ea2f1ec9b3140050ddcbf2de3e49b2b5a0d947981b6092478178a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79083a4b7f98cacdf2df9c5b1d5b897d17ff97f9019b6f6c3ae30bb3bebc0d61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value)

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4546e51c704af084ceb7556b0b73a76c7e2723052e3525aec1976082b7e3d1a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsXRay]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsXRay], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsXRay]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a89f8a3bae21c57127494ed28f6b8aaadeb03b9affab91c6a763edc84787e128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "CloudAwsIntegrations",
    "CloudAwsIntegrationsBilling",
    "CloudAwsIntegrationsBillingOutputReference",
    "CloudAwsIntegrationsCloudtrail",
    "CloudAwsIntegrationsCloudtrailOutputReference",
    "CloudAwsIntegrationsConfig",
    "CloudAwsIntegrationsDocDb",
    "CloudAwsIntegrationsDocDbOutputReference",
    "CloudAwsIntegrationsHealth",
    "CloudAwsIntegrationsHealthOutputReference",
    "CloudAwsIntegrationsS3",
    "CloudAwsIntegrationsS3OutputReference",
    "CloudAwsIntegrationsTrustedAdvisor",
    "CloudAwsIntegrationsTrustedAdvisorOutputReference",
    "CloudAwsIntegrationsVpc",
    "CloudAwsIntegrationsVpcOutputReference",
    "CloudAwsIntegrationsXRay",
    "CloudAwsIntegrationsXRayOutputReference",
]

publication.publish()

def _typecheckingstub__218636da2f5c84b07b8f11f887c728956d546cee837b90d553762da5832a9fd8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    linked_account_id: jsii.Number,
    account_id: typing.Optional[jsii.Number] = None,
    billing: typing.Optional[typing.Union[CloudAwsIntegrationsBilling, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudtrail: typing.Optional[typing.Union[CloudAwsIntegrationsCloudtrail, typing.Dict[builtins.str, typing.Any]]] = None,
    doc_db: typing.Optional[typing.Union[CloudAwsIntegrationsDocDb, typing.Dict[builtins.str, typing.Any]]] = None,
    health: typing.Optional[typing.Union[CloudAwsIntegrationsHealth, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    s3: typing.Optional[typing.Union[CloudAwsIntegrationsS3, typing.Dict[builtins.str, typing.Any]]] = None,
    trusted_advisor: typing.Optional[typing.Union[CloudAwsIntegrationsTrustedAdvisor, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[typing.Union[CloudAwsIntegrationsVpc, typing.Dict[builtins.str, typing.Any]]] = None,
    x_ray: typing.Optional[typing.Union[CloudAwsIntegrationsXRay, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5219cec395e62e4e80020a1434f822e106636205b1c60eb208915ae3fb2ebcc2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53bc997685d6f8091c1aeb3bc838d3517467f180193964c59a5ff4dec857a6d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947ffbc6d56f727b440fd8f8118b85c3b51c796e2061df9d54dc4f7e8a8ac873(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9ccb32fc89d2507f407cef214d9b76981c4a2617faf94bdbaa95a6ca60f3d7(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a62b82999bd05c07ebf66e82fc1cd50209c887f3e8d6dc616b8642f2880f4679(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5dcbb93b5a3ec7ecb2b967fb94b1d9617184e309d8b240bc3497a0639781d84(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9b69b3eb4d71e529ac6b4536b8ceaaf0ec2e61eb0d3064868b86777f85484d(
    value: typing.Optional[CloudAwsIntegrationsBilling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9133ba564bcdd8e4779348d80ab1c85ac796b37f55e670dd76c7e2d6c8aa73fb(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b6ddf9f2bfcf0c0e767bae6f5221261f7773891ee8bb2cb0935bb827b27f74a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a8e5ffa65cec1a9d99267d29a7d0df8763911839b2c7fc3ec6b822357589d34(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac2025d900c573c9470c10047d81f45e617e5ba44b85dab88d0e5f8141da6b1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2520ae8e39751ad9964fa5eb5ebc623daec32d6e9e54c03ba08593b5e99b0f82(
    value: typing.Optional[CloudAwsIntegrationsCloudtrail],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3ac5886f8796b4cd2e377d13a118f9277a15b3d6884b09bb067e13e9f18b87(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    linked_account_id: jsii.Number,
    account_id: typing.Optional[jsii.Number] = None,
    billing: typing.Optional[typing.Union[CloudAwsIntegrationsBilling, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudtrail: typing.Optional[typing.Union[CloudAwsIntegrationsCloudtrail, typing.Dict[builtins.str, typing.Any]]] = None,
    doc_db: typing.Optional[typing.Union[CloudAwsIntegrationsDocDb, typing.Dict[builtins.str, typing.Any]]] = None,
    health: typing.Optional[typing.Union[CloudAwsIntegrationsHealth, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    s3: typing.Optional[typing.Union[CloudAwsIntegrationsS3, typing.Dict[builtins.str, typing.Any]]] = None,
    trusted_advisor: typing.Optional[typing.Union[CloudAwsIntegrationsTrustedAdvisor, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[typing.Union[CloudAwsIntegrationsVpc, typing.Dict[builtins.str, typing.Any]]] = None,
    x_ray: typing.Optional[typing.Union[CloudAwsIntegrationsXRay, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b58ef8635db36e48a559b28b40b82ec4dd41bcbf964598d8e8c2610059fab98(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ceccfccb2c01b0f9212f0432a797550e67fbdd0276877c6b924299041c1031(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0251404e38849d33ade8e61fb4a4f375b9f0abdad07106312e45c3d4b21750a1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc4f66bc4ff0d503483eee5301c5ff5f022809adb60e47f7984abedc805bb6e(
    value: typing.Optional[CloudAwsIntegrationsDocDb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c219d859d9fa6c3f00149ad1692a19b0b2ab9eec6f51eacdd9731529b70b36(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f86711bd01ca429e5db58f084e73315a1b7be773c21e46bb74a94ed2a1845097(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b2e7878d24eba1730c9b8637f82d3912d9cab70e21be12e9c6003a465cd62f3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24de463ea31715daafca9d6f499d395e152ac71f03aea5f4055fc70ff230ee33(
    value: typing.Optional[CloudAwsIntegrationsHealth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ab9b96b00818e6013fe2103e98626b3ebfb0e15dda0b7f25488ae4ca0a47e8(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e785c94925ae01e650b7ed9f3f0da5e0411ad1fc02448a3cc694243e0db6dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6039bca92dc66d6f16736123bcf25b9ff1cdd5a6c24ea16785e120d7afc838d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__683ccb60ceff40081ecf5543bc48e2f1fe43c3201e15763be3993daa3aa831cc(
    value: typing.Optional[CloudAwsIntegrationsS3],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668858f73919a08f504c8a90bb65ffb65bc1d01d05572ddba939811087652a14(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a147261cc3bf496a0e170a5e441607f620af5f12ed60056d946be7f8b8c0f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec4f346a457cb1508ddb025b8d144de7b4840241fc61fa8191b69cf6be3c6e85(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4bc63cefa256d5b5346d16c3750a584927d393bdf9459dbab1f2801aa2c8f36(
    value: typing.Optional[CloudAwsIntegrationsTrustedAdvisor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5a05e1712a6079eebfb1cebb9021117640ecdb1735fc94235af901ee1bb64db(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_nat_gateway: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fetch_vpn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc03184763dca962a4a8ab314c5c148983b1f331637301224bdc278d238f3491(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__555e7d85f2e58ac7b541bacd19f13077a47af6954e80f4b40ac339755b9b7896(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b2657609fdf500a4e737b95dd4cc4b3d5550f0c3ef0c867e038437ea0e58637(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da72c88928d008dd41e6355c8234df0e259a01b0abb531818bb0b36c7caf2c8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9579bf68121b247cafa084f153862e870a9191414d93835d82fabaa96a992f14(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac7fa1649a4d226ab4fb2c00a338e4d9911e66ca678b5bcc71bd5245e0bb120(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ea2f558eb8f44587d62e70414f9e1cafca3e2ec1df4590a34f1a3d47499183(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ac68e78d33565f199421a44fdec8c9985ca38d90c14b0a0d05bbf25fe5b8d7(
    value: typing.Optional[CloudAwsIntegrationsVpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df10b2612d85d90190d8350575e635e7b3cef8ab626c415ebe5664e6ba53fa3(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a6346257c8ea2f1ec9b3140050ddcbf2de3e49b2b5a0d947981b6092478178a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79083a4b7f98cacdf2df9c5b1d5b897d17ff97f9019b6f6c3ae30bb3bebc0d61(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4546e51c704af084ceb7556b0b73a76c7e2723052e3525aec1976082b7e3d1a3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89f8a3bae21c57127494ed28f6b8aaadeb03b9affab91c6a763edc84787e128(
    value: typing.Optional[CloudAwsIntegrationsXRay],
) -> None:
    """Type checking stubs"""
    pass
