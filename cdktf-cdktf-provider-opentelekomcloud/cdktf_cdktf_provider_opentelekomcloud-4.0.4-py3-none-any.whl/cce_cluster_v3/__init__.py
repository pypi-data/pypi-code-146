'''
# `opentelekomcloud_cce_cluster_v3`

Refer to the Terraform Registory for docs: [`opentelekomcloud_cce_cluster_v3`](https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3).
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


class CceClusterV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceClusterV3.CceClusterV3",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3 opentelekomcloud_cce_cluster_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_type: builtins.str,
        container_network_type: builtins.str,
        flavor_id: builtins.str,
        name: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        authenticating_proxy: typing.Optional[typing.Union["CceClusterV3AuthenticatingProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        authenticating_proxy_ca: typing.Optional[builtins.str] = None,
        authentication_mode: typing.Optional[builtins.str] = None,
        billing_mode: typing.Optional[jsii.Number] = None,
        cluster_version: typing.Optional[builtins.str] = None,
        container_network_cidr: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        eip: typing.Optional[builtins.str] = None,
        eni_subnet_cidr: typing.Optional[builtins.str] = None,
        eni_subnet_id: typing.Optional[builtins.str] = None,
        extend_param: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        highway_subnet_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_addons: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kube_proxy_mode: typing.Optional[builtins.str] = None,
        kubernetes_svc_ip_range: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        multi_az: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        no_addons: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CceClusterV3Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3 opentelekomcloud_cce_cluster_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#cluster_type CceClusterV3#cluster_type}.
        :param container_network_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#container_network_type CceClusterV3#container_network_type}.
        :param flavor_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#flavor_id CceClusterV3#flavor_id}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#name CceClusterV3#name}.
        :param subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#subnet_id CceClusterV3#subnet_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#vpc_id CceClusterV3#vpc_id}.
        :param annotations: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#annotations CceClusterV3#annotations}.
        :param authenticating_proxy: authenticating_proxy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#authenticating_proxy CceClusterV3#authenticating_proxy}
        :param authenticating_proxy_ca: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#authenticating_proxy_ca CceClusterV3#authenticating_proxy_ca}.
        :param authentication_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#authentication_mode CceClusterV3#authentication_mode}.
        :param billing_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#billing_mode CceClusterV3#billing_mode}.
        :param cluster_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#cluster_version CceClusterV3#cluster_version}.
        :param container_network_cidr: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#container_network_cidr CceClusterV3#container_network_cidr}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#description CceClusterV3#description}.
        :param eip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#eip CceClusterV3#eip}.
        :param eni_subnet_cidr: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#eni_subnet_cidr CceClusterV3#eni_subnet_cidr}.
        :param eni_subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#eni_subnet_id CceClusterV3#eni_subnet_id}.
        :param extend_param: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#extend_param CceClusterV3#extend_param}.
        :param highway_subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#highway_subnet_id CceClusterV3#highway_subnet_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#id CceClusterV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_addons: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#ignore_addons CceClusterV3#ignore_addons}.
        :param kube_proxy_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#kube_proxy_mode CceClusterV3#kube_proxy_mode}.
        :param kubernetes_svc_ip_range: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#kubernetes_svc_ip_range CceClusterV3#kubernetes_svc_ip_range}.
        :param labels: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#labels CceClusterV3#labels}.
        :param multi_az: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#multi_az CceClusterV3#multi_az}.
        :param no_addons: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#no_addons CceClusterV3#no_addons}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#region CceClusterV3#region}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#timeouts CceClusterV3#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32e12eba2304face71ef8e9fdefb3c681346e3305b6644e9bc90d9cfae87e043)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CceClusterV3Config(
            cluster_type=cluster_type,
            container_network_type=container_network_type,
            flavor_id=flavor_id,
            name=name,
            subnet_id=subnet_id,
            vpc_id=vpc_id,
            annotations=annotations,
            authenticating_proxy=authenticating_proxy,
            authenticating_proxy_ca=authenticating_proxy_ca,
            authentication_mode=authentication_mode,
            billing_mode=billing_mode,
            cluster_version=cluster_version,
            container_network_cidr=container_network_cidr,
            description=description,
            eip=eip,
            eni_subnet_cidr=eni_subnet_cidr,
            eni_subnet_id=eni_subnet_id,
            extend_param=extend_param,
            highway_subnet_id=highway_subnet_id,
            id=id,
            ignore_addons=ignore_addons,
            kube_proxy_mode=kube_proxy_mode,
            kubernetes_svc_ip_range=kubernetes_svc_ip_range,
            labels=labels,
            multi_az=multi_az,
            no_addons=no_addons,
            region=region,
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

    @jsii.member(jsii_name="putAuthenticatingProxy")
    def put_authenticating_proxy(
        self,
        *,
        ca: builtins.str,
        cert: builtins.str,
        private_key: builtins.str,
    ) -> None:
        '''
        :param ca: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#ca CceClusterV3#ca}.
        :param cert: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#cert CceClusterV3#cert}.
        :param private_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#private_key CceClusterV3#private_key}.
        '''
        value = CceClusterV3AuthenticatingProxy(
            ca=ca, cert=cert, private_key=private_key
        )

        return typing.cast(None, jsii.invoke(self, "putAuthenticatingProxy", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#create CceClusterV3#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#delete CceClusterV3#delete}.
        '''
        value = CceClusterV3Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetAuthenticatingProxy")
    def reset_authenticating_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticatingProxy", []))

    @jsii.member(jsii_name="resetAuthenticatingProxyCa")
    def reset_authenticating_proxy_ca(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticatingProxyCa", []))

    @jsii.member(jsii_name="resetAuthenticationMode")
    def reset_authentication_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationMode", []))

    @jsii.member(jsii_name="resetBillingMode")
    def reset_billing_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBillingMode", []))

    @jsii.member(jsii_name="resetClusterVersion")
    def reset_cluster_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterVersion", []))

    @jsii.member(jsii_name="resetContainerNetworkCidr")
    def reset_container_network_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerNetworkCidr", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEip")
    def reset_eip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEip", []))

    @jsii.member(jsii_name="resetEniSubnetCidr")
    def reset_eni_subnet_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEniSubnetCidr", []))

    @jsii.member(jsii_name="resetEniSubnetId")
    def reset_eni_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEniSubnetId", []))

    @jsii.member(jsii_name="resetExtendParam")
    def reset_extend_param(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtendParam", []))

    @jsii.member(jsii_name="resetHighwaySubnetId")
    def reset_highway_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHighwaySubnetId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIgnoreAddons")
    def reset_ignore_addons(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreAddons", []))

    @jsii.member(jsii_name="resetKubeProxyMode")
    def reset_kube_proxy_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubeProxyMode", []))

    @jsii.member(jsii_name="resetKubernetesSvcIpRange")
    def reset_kubernetes_svc_ip_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubernetesSvcIpRange", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMultiAz")
    def reset_multi_az(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiAz", []))

    @jsii.member(jsii_name="resetNoAddons")
    def reset_no_addons(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoAddons", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="authenticatingProxy")
    def authenticating_proxy(self) -> "CceClusterV3AuthenticatingProxyOutputReference":
        return typing.cast("CceClusterV3AuthenticatingProxyOutputReference", jsii.get(self, "authenticatingProxy"))

    @builtins.property
    @jsii.member(jsii_name="certificateClusters")
    def certificate_clusters(self) -> "CceClusterV3CertificateClustersList":
        return typing.cast("CceClusterV3CertificateClustersList", jsii.get(self, "certificateClusters"))

    @builtins.property
    @jsii.member(jsii_name="certificateUsers")
    def certificate_users(self) -> "CceClusterV3CertificateUsersList":
        return typing.cast("CceClusterV3CertificateUsersList", jsii.get(self, "certificateUsers"))

    @builtins.property
    @jsii.member(jsii_name="external")
    def external(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "external"))

    @builtins.property
    @jsii.member(jsii_name="externalOtc")
    def external_otc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalOtc"))

    @builtins.property
    @jsii.member(jsii_name="installedAddons")
    def installed_addons(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "installedAddons"))

    @builtins.property
    @jsii.member(jsii_name="internal")
    def internal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "internal"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupControl")
    def security_group_control(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupControl"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupNode")
    def security_group_node(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupNode"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CceClusterV3TimeoutsOutputReference":
        return typing.cast("CceClusterV3TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticatingProxyCaInput")
    def authenticating_proxy_ca_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticatingProxyCaInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticatingProxyInput")
    def authenticating_proxy_input(
        self,
    ) -> typing.Optional["CceClusterV3AuthenticatingProxy"]:
        return typing.cast(typing.Optional["CceClusterV3AuthenticatingProxy"], jsii.get(self, "authenticatingProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationModeInput")
    def authentication_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="billingModeInput")
    def billing_mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "billingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterTypeInput")
    def cluster_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterVersionInput")
    def cluster_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="containerNetworkCidrInput")
    def container_network_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerNetworkCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="containerNetworkTypeInput")
    def container_network_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerNetworkTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="eipInput")
    def eip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eipInput"))

    @builtins.property
    @jsii.member(jsii_name="eniSubnetCidrInput")
    def eni_subnet_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eniSubnetCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="eniSubnetIdInput")
    def eni_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eniSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="extendParamInput")
    def extend_param_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "extendParamInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorIdInput")
    def flavor_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="highwaySubnetIdInput")
    def highway_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "highwaySubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreAddonsInput")
    def ignore_addons_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreAddonsInput"))

    @builtins.property
    @jsii.member(jsii_name="kubeProxyModeInput")
    def kube_proxy_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubeProxyModeInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesSvcIpRangeInput")
    def kubernetes_svc_ip_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubernetesSvcIpRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="multiAzInput")
    def multi_az_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "multiAzInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="noAddonsInput")
    def no_addons_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noAddonsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["CceClusterV3Timeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["CceClusterV3Timeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93c789b96bcdb8fa4c5fc3168a34dcd9d0a39fdac6d5311547c67b3cafb76988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value)

    @builtins.property
    @jsii.member(jsii_name="authenticatingProxyCa")
    def authenticating_proxy_ca(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticatingProxyCa"))

    @authenticating_proxy_ca.setter
    def authenticating_proxy_ca(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b9047f06352b37a5b86999361165230cf9d4a6f51310a339f7d1b906e085b72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticatingProxyCa", value)

    @builtins.property
    @jsii.member(jsii_name="authenticationMode")
    def authentication_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationMode"))

    @authentication_mode.setter
    def authentication_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__800c9d349a71b5ef8ccdd58c1f50e4af31bcf5976331fba808fb43f3477ed196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationMode", value)

    @builtins.property
    @jsii.member(jsii_name="billingMode")
    def billing_mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "billingMode"))

    @billing_mode.setter
    def billing_mode(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48ccb6e5aa904db74372aaac39542f86b103829ead3c20f74fc867ba5fa3a235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingMode", value)

    @builtins.property
    @jsii.member(jsii_name="clusterType")
    def cluster_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterType"))

    @cluster_type.setter
    def cluster_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__806fa037bf3b995008dd98639dcd948e0093e2a3d8506d5a84efa85961d17553)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterType", value)

    @builtins.property
    @jsii.member(jsii_name="clusterVersion")
    def cluster_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterVersion"))

    @cluster_version.setter
    def cluster_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e763fcc5702cf8f5a15cb08fa37da0f5ca180d928e3be3438296230cf67a6cfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterVersion", value)

    @builtins.property
    @jsii.member(jsii_name="containerNetworkCidr")
    def container_network_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerNetworkCidr"))

    @container_network_cidr.setter
    def container_network_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a5ea903425f5f8f2df12e19f150952c01440b0227560c90b958fa3647f0023f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerNetworkCidr", value)

    @builtins.property
    @jsii.member(jsii_name="containerNetworkType")
    def container_network_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerNetworkType"))

    @container_network_type.setter
    def container_network_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8b439fd1dcb3b4f9ff2b6fe3ed8a9c8362c510317486af02ab2052d53dab926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerNetworkType", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf0a865a3eab0798e6b8997b39ae3dc47c43f68799bc3b5d859a48d6186fc65f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="eip")
    def eip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eip"))

    @eip.setter
    def eip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c37c3c4dcddf688edbc6923eea9dfca090faa47f5c9b6c56c53e0c31d343322b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eip", value)

    @builtins.property
    @jsii.member(jsii_name="eniSubnetCidr")
    def eni_subnet_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eniSubnetCidr"))

    @eni_subnet_cidr.setter
    def eni_subnet_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cedf5069e876d89d2887ee92b987c0e2a6e538b3b6a64d44aadaa4db6f2d0d0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eniSubnetCidr", value)

    @builtins.property
    @jsii.member(jsii_name="eniSubnetId")
    def eni_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eniSubnetId"))

    @eni_subnet_id.setter
    def eni_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5146a6b5381ebab92b274783215aa65d96e33b7e2e4d21f1d0dae4dac98065d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eniSubnetId", value)

    @builtins.property
    @jsii.member(jsii_name="extendParam")
    def extend_param(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "extendParam"))

    @extend_param.setter
    def extend_param(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08961c021474bba1e06dd160279d09a5151d4380158f7a8358d2f44ee3b2b280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendParam", value)

    @builtins.property
    @jsii.member(jsii_name="flavorId")
    def flavor_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavorId"))

    @flavor_id.setter
    def flavor_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63388d30f95061e51464f8ac754e3457737bf2a359e364e03c67f834d1e8666f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavorId", value)

    @builtins.property
    @jsii.member(jsii_name="highwaySubnetId")
    def highway_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "highwaySubnetId"))

    @highway_subnet_id.setter
    def highway_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a06b8c35f4a78ff9bae8b45826a7cb9398f1eb9f656483b38db90be088c0a88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "highwaySubnetId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bbfcda3faf566f4415f6290ee11c039395c8a44b862c4461e643c78c76a0d10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreAddons")
    def ignore_addons(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreAddons"))

    @ignore_addons.setter
    def ignore_addons(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92363afb0b4a3a5e80c601a69ce2cd3c3cc348295a158dfd66ff32c59d71208f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreAddons", value)

    @builtins.property
    @jsii.member(jsii_name="kubeProxyMode")
    def kube_proxy_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubeProxyMode"))

    @kube_proxy_mode.setter
    def kube_proxy_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c6556cf1e25586128747efb7996b8bd33e3fc047fb0811576f8a3b0bd19b7dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubeProxyMode", value)

    @builtins.property
    @jsii.member(jsii_name="kubernetesSvcIpRange")
    def kubernetes_svc_ip_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesSvcIpRange"))

    @kubernetes_svc_ip_range.setter
    def kubernetes_svc_ip_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df80591fb0665f93c31ff15a8cf398fbb6e9ef0c086308ac4b75ded6e84ad906)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubernetesSvcIpRange", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2ad34b16bc98900e9c084b81c0483f81ee12c2bce3f8cb9009489233a746263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="multiAz")
    def multi_az(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "multiAz"))

    @multi_az.setter
    def multi_az(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b558912d01e8c27d16b088f32d432032099d9f746c524fb2cef4bbdab8c41198)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiAz", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c528c2f53cf2b360b860d38ba0f275d7752803b53e95fc4b1d56f3b474e51785)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="noAddons")
    def no_addons(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noAddons"))

    @no_addons.setter
    def no_addons(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87bf2811452ff1d407c45e0afbd04bdc5c3edb00f466cd0a1e3f0ad10ee69d5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noAddons", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c934d10082c63fbf1868438659acee8a461e413c2012fba48bf8da3fb545ad26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e279c62dd1698352c2bb894ab9f4d66256557a1df30bb3c928c4bc20cf04e63b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value)

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c10485c5d0c61d59047fde5a9b1fbcc652c4d0dd30776c9228a07cb880519c5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceClusterV3.CceClusterV3AuthenticatingProxy",
    jsii_struct_bases=[],
    name_mapping={"ca": "ca", "cert": "cert", "private_key": "privateKey"},
)
class CceClusterV3AuthenticatingProxy:
    def __init__(
        self,
        *,
        ca: builtins.str,
        cert: builtins.str,
        private_key: builtins.str,
    ) -> None:
        '''
        :param ca: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#ca CceClusterV3#ca}.
        :param cert: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#cert CceClusterV3#cert}.
        :param private_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#private_key CceClusterV3#private_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe6d9daf308f6e57b70233f67c564f06ce549eee7106817f908df0d5766a524)
            check_type(argname="argument ca", value=ca, expected_type=type_hints["ca"])
            check_type(argname="argument cert", value=cert, expected_type=type_hints["cert"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ca": ca,
            "cert": cert,
            "private_key": private_key,
        }

    @builtins.property
    def ca(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#ca CceClusterV3#ca}.'''
        result = self._values.get("ca")
        assert result is not None, "Required property 'ca' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cert(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#cert CceClusterV3#cert}.'''
        result = self._values.get("cert")
        assert result is not None, "Required property 'cert' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def private_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#private_key CceClusterV3#private_key}.'''
        result = self._values.get("private_key")
        assert result is not None, "Required property 'private_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceClusterV3AuthenticatingProxy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceClusterV3AuthenticatingProxyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceClusterV3.CceClusterV3AuthenticatingProxyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0ec9a1ffe9972ad47fad590a3346fc1c1d72d38a90966e87774714f0b6c5514)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="caInput")
    def ca_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caInput"))

    @builtins.property
    @jsii.member(jsii_name="certInput")
    def cert_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyInput")
    def private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="ca")
    def ca(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ca"))

    @ca.setter
    def ca(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__739f5df43aee79540b744cbb01c26b71c1c6ad137c13a8deb8385d3faad3fa65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ca", value)

    @builtins.property
    @jsii.member(jsii_name="cert")
    def cert(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cert"))

    @cert.setter
    def cert(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f84bf313f63fb87e18841059a84ffd861d26cfc9790efd626053fb0452b6327c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cert", value)

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c92f32ddf95cfb9727f04841ed608fd48bec2861ab8dee99fbbc2807cc02264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CceClusterV3AuthenticatingProxy]:
        return typing.cast(typing.Optional[CceClusterV3AuthenticatingProxy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CceClusterV3AuthenticatingProxy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2d8086005c2a0f9524869a92c03915698979df1d5475493a9b076dc186904cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceClusterV3.CceClusterV3CertificateClusters",
    jsii_struct_bases=[],
    name_mapping={},
)
class CceClusterV3CertificateClusters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceClusterV3CertificateClusters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceClusterV3CertificateClustersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceClusterV3.CceClusterV3CertificateClustersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97adab6f111c82eac678ca218cdbd038a24759af74e9e24c14a3a5eb40ba8141)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CceClusterV3CertificateClustersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1d5e13156638c47a358447f97f81fe13b92a737a9f7068fc774989b18da499a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CceClusterV3CertificateClustersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__305b88ad7de7310cac99dce56d47e34450d6b5d51c5f9dc91fbf54c1fb3354f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9909340a9bc76e7dba32c2ae7215e94926ceafb6cc28c40dfb799e16bda20c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26cf44d0cb08547ea20cc297000387c42ecc9dfa17f79c1834a1c06d569e04c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class CceClusterV3CertificateClustersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceClusterV3.CceClusterV3CertificateClustersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ddd2afc4c52cd6282a3d55d2cb1578f2c80e3ee10cd041054445bdfc6cfd7fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityData")
    def certificate_authority_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateAuthorityData"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CceClusterV3CertificateClusters]:
        return typing.cast(typing.Optional[CceClusterV3CertificateClusters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CceClusterV3CertificateClusters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8306dc9e78ff46f44c44937329cbe8aff1f967fd50c038cad60caee527abd42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceClusterV3.CceClusterV3CertificateUsers",
    jsii_struct_bases=[],
    name_mapping={},
)
class CceClusterV3CertificateUsers:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceClusterV3CertificateUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceClusterV3CertificateUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceClusterV3.CceClusterV3CertificateUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2090f406feef2ac0b4fbd8d18ca3bd3de588102ba659e1a7d7b503e6a477baa9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CceClusterV3CertificateUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047a427474b67b1fc0404de58ce69ab27a9463b0db7655630c4bd4404836ae46)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CceClusterV3CertificateUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f88b664c469f306132ed3c6055b22da79fbd7f07a3d2c5d1c5643e7176ee1c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ff4c983a1ed13186b07b6f727bab3ee2a6935f94304d1699ad2712ed0e6ac28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f00f78e25d487adad6ac96288cacac2632b8a638ffe11eb586f4aaf016ff3175)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class CceClusterV3CertificateUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceClusterV3.CceClusterV3CertificateUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbbe6b25940a672bdbeeacf06a90dbe0635134c4b18fe3b3f82404fe79508a4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="clientCertificateData")
    def client_certificate_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateData"))

    @builtins.property
    @jsii.member(jsii_name="clientKeyData")
    def client_key_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientKeyData"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CceClusterV3CertificateUsers]:
        return typing.cast(typing.Optional[CceClusterV3CertificateUsers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CceClusterV3CertificateUsers],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5ffd9e532666c9769aaefcff6579170c2b47634dda445b3dccacc53ae28439f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceClusterV3.CceClusterV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster_type": "clusterType",
        "container_network_type": "containerNetworkType",
        "flavor_id": "flavorId",
        "name": "name",
        "subnet_id": "subnetId",
        "vpc_id": "vpcId",
        "annotations": "annotations",
        "authenticating_proxy": "authenticatingProxy",
        "authenticating_proxy_ca": "authenticatingProxyCa",
        "authentication_mode": "authenticationMode",
        "billing_mode": "billingMode",
        "cluster_version": "clusterVersion",
        "container_network_cidr": "containerNetworkCidr",
        "description": "description",
        "eip": "eip",
        "eni_subnet_cidr": "eniSubnetCidr",
        "eni_subnet_id": "eniSubnetId",
        "extend_param": "extendParam",
        "highway_subnet_id": "highwaySubnetId",
        "id": "id",
        "ignore_addons": "ignoreAddons",
        "kube_proxy_mode": "kubeProxyMode",
        "kubernetes_svc_ip_range": "kubernetesSvcIpRange",
        "labels": "labels",
        "multi_az": "multiAz",
        "no_addons": "noAddons",
        "region": "region",
        "timeouts": "timeouts",
    },
)
class CceClusterV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cluster_type: builtins.str,
        container_network_type: builtins.str,
        flavor_id: builtins.str,
        name: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        authenticating_proxy: typing.Optional[typing.Union[CceClusterV3AuthenticatingProxy, typing.Dict[builtins.str, typing.Any]]] = None,
        authenticating_proxy_ca: typing.Optional[builtins.str] = None,
        authentication_mode: typing.Optional[builtins.str] = None,
        billing_mode: typing.Optional[jsii.Number] = None,
        cluster_version: typing.Optional[builtins.str] = None,
        container_network_cidr: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        eip: typing.Optional[builtins.str] = None,
        eni_subnet_cidr: typing.Optional[builtins.str] = None,
        eni_subnet_id: typing.Optional[builtins.str] = None,
        extend_param: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        highway_subnet_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_addons: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kube_proxy_mode: typing.Optional[builtins.str] = None,
        kubernetes_svc_ip_range: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        multi_az: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        no_addons: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CceClusterV3Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#cluster_type CceClusterV3#cluster_type}.
        :param container_network_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#container_network_type CceClusterV3#container_network_type}.
        :param flavor_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#flavor_id CceClusterV3#flavor_id}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#name CceClusterV3#name}.
        :param subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#subnet_id CceClusterV3#subnet_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#vpc_id CceClusterV3#vpc_id}.
        :param annotations: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#annotations CceClusterV3#annotations}.
        :param authenticating_proxy: authenticating_proxy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#authenticating_proxy CceClusterV3#authenticating_proxy}
        :param authenticating_proxy_ca: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#authenticating_proxy_ca CceClusterV3#authenticating_proxy_ca}.
        :param authentication_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#authentication_mode CceClusterV3#authentication_mode}.
        :param billing_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#billing_mode CceClusterV3#billing_mode}.
        :param cluster_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#cluster_version CceClusterV3#cluster_version}.
        :param container_network_cidr: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#container_network_cidr CceClusterV3#container_network_cidr}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#description CceClusterV3#description}.
        :param eip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#eip CceClusterV3#eip}.
        :param eni_subnet_cidr: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#eni_subnet_cidr CceClusterV3#eni_subnet_cidr}.
        :param eni_subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#eni_subnet_id CceClusterV3#eni_subnet_id}.
        :param extend_param: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#extend_param CceClusterV3#extend_param}.
        :param highway_subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#highway_subnet_id CceClusterV3#highway_subnet_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#id CceClusterV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_addons: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#ignore_addons CceClusterV3#ignore_addons}.
        :param kube_proxy_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#kube_proxy_mode CceClusterV3#kube_proxy_mode}.
        :param kubernetes_svc_ip_range: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#kubernetes_svc_ip_range CceClusterV3#kubernetes_svc_ip_range}.
        :param labels: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#labels CceClusterV3#labels}.
        :param multi_az: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#multi_az CceClusterV3#multi_az}.
        :param no_addons: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#no_addons CceClusterV3#no_addons}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#region CceClusterV3#region}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#timeouts CceClusterV3#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(authenticating_proxy, dict):
            authenticating_proxy = CceClusterV3AuthenticatingProxy(**authenticating_proxy)
        if isinstance(timeouts, dict):
            timeouts = CceClusterV3Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0018adff4c4f0557be1ac98a122bacc94570e0375fcf04e887e36283c512e43b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster_type", value=cluster_type, expected_type=type_hints["cluster_type"])
            check_type(argname="argument container_network_type", value=container_network_type, expected_type=type_hints["container_network_type"])
            check_type(argname="argument flavor_id", value=flavor_id, expected_type=type_hints["flavor_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument authenticating_proxy", value=authenticating_proxy, expected_type=type_hints["authenticating_proxy"])
            check_type(argname="argument authenticating_proxy_ca", value=authenticating_proxy_ca, expected_type=type_hints["authenticating_proxy_ca"])
            check_type(argname="argument authentication_mode", value=authentication_mode, expected_type=type_hints["authentication_mode"])
            check_type(argname="argument billing_mode", value=billing_mode, expected_type=type_hints["billing_mode"])
            check_type(argname="argument cluster_version", value=cluster_version, expected_type=type_hints["cluster_version"])
            check_type(argname="argument container_network_cidr", value=container_network_cidr, expected_type=type_hints["container_network_cidr"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument eip", value=eip, expected_type=type_hints["eip"])
            check_type(argname="argument eni_subnet_cidr", value=eni_subnet_cidr, expected_type=type_hints["eni_subnet_cidr"])
            check_type(argname="argument eni_subnet_id", value=eni_subnet_id, expected_type=type_hints["eni_subnet_id"])
            check_type(argname="argument extend_param", value=extend_param, expected_type=type_hints["extend_param"])
            check_type(argname="argument highway_subnet_id", value=highway_subnet_id, expected_type=type_hints["highway_subnet_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ignore_addons", value=ignore_addons, expected_type=type_hints["ignore_addons"])
            check_type(argname="argument kube_proxy_mode", value=kube_proxy_mode, expected_type=type_hints["kube_proxy_mode"])
            check_type(argname="argument kubernetes_svc_ip_range", value=kubernetes_svc_ip_range, expected_type=type_hints["kubernetes_svc_ip_range"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument multi_az", value=multi_az, expected_type=type_hints["multi_az"])
            check_type(argname="argument no_addons", value=no_addons, expected_type=type_hints["no_addons"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_type": cluster_type,
            "container_network_type": container_network_type,
            "flavor_id": flavor_id,
            "name": name,
            "subnet_id": subnet_id,
            "vpc_id": vpc_id,
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
        if annotations is not None:
            self._values["annotations"] = annotations
        if authenticating_proxy is not None:
            self._values["authenticating_proxy"] = authenticating_proxy
        if authenticating_proxy_ca is not None:
            self._values["authenticating_proxy_ca"] = authenticating_proxy_ca
        if authentication_mode is not None:
            self._values["authentication_mode"] = authentication_mode
        if billing_mode is not None:
            self._values["billing_mode"] = billing_mode
        if cluster_version is not None:
            self._values["cluster_version"] = cluster_version
        if container_network_cidr is not None:
            self._values["container_network_cidr"] = container_network_cidr
        if description is not None:
            self._values["description"] = description
        if eip is not None:
            self._values["eip"] = eip
        if eni_subnet_cidr is not None:
            self._values["eni_subnet_cidr"] = eni_subnet_cidr
        if eni_subnet_id is not None:
            self._values["eni_subnet_id"] = eni_subnet_id
        if extend_param is not None:
            self._values["extend_param"] = extend_param
        if highway_subnet_id is not None:
            self._values["highway_subnet_id"] = highway_subnet_id
        if id is not None:
            self._values["id"] = id
        if ignore_addons is not None:
            self._values["ignore_addons"] = ignore_addons
        if kube_proxy_mode is not None:
            self._values["kube_proxy_mode"] = kube_proxy_mode
        if kubernetes_svc_ip_range is not None:
            self._values["kubernetes_svc_ip_range"] = kubernetes_svc_ip_range
        if labels is not None:
            self._values["labels"] = labels
        if multi_az is not None:
            self._values["multi_az"] = multi_az
        if no_addons is not None:
            self._values["no_addons"] = no_addons
        if region is not None:
            self._values["region"] = region
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
    def cluster_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#cluster_type CceClusterV3#cluster_type}.'''
        result = self._values.get("cluster_type")
        assert result is not None, "Required property 'cluster_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_network_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#container_network_type CceClusterV3#container_network_type}.'''
        result = self._values.get("container_network_type")
        assert result is not None, "Required property 'container_network_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def flavor_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#flavor_id CceClusterV3#flavor_id}.'''
        result = self._values.get("flavor_id")
        assert result is not None, "Required property 'flavor_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#name CceClusterV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#subnet_id CceClusterV3#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#vpc_id CceClusterV3#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#annotations CceClusterV3#annotations}.'''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def authenticating_proxy(self) -> typing.Optional[CceClusterV3AuthenticatingProxy]:
        '''authenticating_proxy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#authenticating_proxy CceClusterV3#authenticating_proxy}
        '''
        result = self._values.get("authenticating_proxy")
        return typing.cast(typing.Optional[CceClusterV3AuthenticatingProxy], result)

    @builtins.property
    def authenticating_proxy_ca(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#authenticating_proxy_ca CceClusterV3#authenticating_proxy_ca}.'''
        result = self._values.get("authenticating_proxy_ca")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authentication_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#authentication_mode CceClusterV3#authentication_mode}.'''
        result = self._values.get("authentication_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def billing_mode(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#billing_mode CceClusterV3#billing_mode}.'''
        result = self._values.get("billing_mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cluster_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#cluster_version CceClusterV3#cluster_version}.'''
        result = self._values.get("cluster_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_network_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#container_network_cidr CceClusterV3#container_network_cidr}.'''
        result = self._values.get("container_network_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#description CceClusterV3#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#eip CceClusterV3#eip}.'''
        result = self._values.get("eip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eni_subnet_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#eni_subnet_cidr CceClusterV3#eni_subnet_cidr}.'''
        result = self._values.get("eni_subnet_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eni_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#eni_subnet_id CceClusterV3#eni_subnet_id}.'''
        result = self._values.get("eni_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extend_param(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#extend_param CceClusterV3#extend_param}.'''
        result = self._values.get("extend_param")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def highway_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#highway_subnet_id CceClusterV3#highway_subnet_id}.'''
        result = self._values.get("highway_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#id CceClusterV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_addons(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#ignore_addons CceClusterV3#ignore_addons}.'''
        result = self._values.get("ignore_addons")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kube_proxy_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#kube_proxy_mode CceClusterV3#kube_proxy_mode}.'''
        result = self._values.get("kube_proxy_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kubernetes_svc_ip_range(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#kubernetes_svc_ip_range CceClusterV3#kubernetes_svc_ip_range}.'''
        result = self._values.get("kubernetes_svc_ip_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#labels CceClusterV3#labels}.'''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def multi_az(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#multi_az CceClusterV3#multi_az}.'''
        result = self._values.get("multi_az")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def no_addons(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#no_addons CceClusterV3#no_addons}.'''
        result = self._values.get("no_addons")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#region CceClusterV3#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CceClusterV3Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#timeouts CceClusterV3#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CceClusterV3Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceClusterV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceClusterV3.CceClusterV3Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class CceClusterV3Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#create CceClusterV3#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#delete CceClusterV3#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba781513e5c3394c568f795a2c8bd1a8cd6777880a04a6cc11197678d1cad104)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#create CceClusterV3#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_cluster_v3#delete CceClusterV3#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceClusterV3Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceClusterV3TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceClusterV3.CceClusterV3TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5803e1b95951c157dad6c48b42603e29c2b44d886c0e518eb82ee2d740ce8d22)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db9cb6d5ebcf98e8825e0f17214077ca5f10112cab4a6f3cddeb461f4510ecb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f8196410f6ae43ad238e9c7357b8e52f4cb916618f48fd9fdf647087e711087)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CceClusterV3Timeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CceClusterV3Timeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CceClusterV3Timeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de262efc7b642c4b609fb0c24ba92a248890c6e18ff478907424d8daa0ba218c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "CceClusterV3",
    "CceClusterV3AuthenticatingProxy",
    "CceClusterV3AuthenticatingProxyOutputReference",
    "CceClusterV3CertificateClusters",
    "CceClusterV3CertificateClustersList",
    "CceClusterV3CertificateClustersOutputReference",
    "CceClusterV3CertificateUsers",
    "CceClusterV3CertificateUsersList",
    "CceClusterV3CertificateUsersOutputReference",
    "CceClusterV3Config",
    "CceClusterV3Timeouts",
    "CceClusterV3TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__32e12eba2304face71ef8e9fdefb3c681346e3305b6644e9bc90d9cfae87e043(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_type: builtins.str,
    container_network_type: builtins.str,
    flavor_id: builtins.str,
    name: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    authenticating_proxy: typing.Optional[typing.Union[CceClusterV3AuthenticatingProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    authenticating_proxy_ca: typing.Optional[builtins.str] = None,
    authentication_mode: typing.Optional[builtins.str] = None,
    billing_mode: typing.Optional[jsii.Number] = None,
    cluster_version: typing.Optional[builtins.str] = None,
    container_network_cidr: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    eip: typing.Optional[builtins.str] = None,
    eni_subnet_cidr: typing.Optional[builtins.str] = None,
    eni_subnet_id: typing.Optional[builtins.str] = None,
    extend_param: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    highway_subnet_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_addons: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    kube_proxy_mode: typing.Optional[builtins.str] = None,
    kubernetes_svc_ip_range: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    multi_az: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    no_addons: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CceClusterV3Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__93c789b96bcdb8fa4c5fc3168a34dcd9d0a39fdac6d5311547c67b3cafb76988(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9047f06352b37a5b86999361165230cf9d4a6f51310a339f7d1b906e085b72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__800c9d349a71b5ef8ccdd58c1f50e4af31bcf5976331fba808fb43f3477ed196(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48ccb6e5aa904db74372aaac39542f86b103829ead3c20f74fc867ba5fa3a235(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806fa037bf3b995008dd98639dcd948e0093e2a3d8506d5a84efa85961d17553(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e763fcc5702cf8f5a15cb08fa37da0f5ca180d928e3be3438296230cf67a6cfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5ea903425f5f8f2df12e19f150952c01440b0227560c90b958fa3647f0023f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b439fd1dcb3b4f9ff2b6fe3ed8a9c8362c510317486af02ab2052d53dab926(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf0a865a3eab0798e6b8997b39ae3dc47c43f68799bc3b5d859a48d6186fc65f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37c3c4dcddf688edbc6923eea9dfca090faa47f5c9b6c56c53e0c31d343322b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cedf5069e876d89d2887ee92b987c0e2a6e538b3b6a64d44aadaa4db6f2d0d0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5146a6b5381ebab92b274783215aa65d96e33b7e2e4d21f1d0dae4dac98065d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08961c021474bba1e06dd160279d09a5151d4380158f7a8358d2f44ee3b2b280(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63388d30f95061e51464f8ac754e3457737bf2a359e364e03c67f834d1e8666f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a06b8c35f4a78ff9bae8b45826a7cb9398f1eb9f656483b38db90be088c0a88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bbfcda3faf566f4415f6290ee11c039395c8a44b862c4461e643c78c76a0d10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92363afb0b4a3a5e80c601a69ce2cd3c3cc348295a158dfd66ff32c59d71208f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6556cf1e25586128747efb7996b8bd33e3fc047fb0811576f8a3b0bd19b7dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df80591fb0665f93c31ff15a8cf398fbb6e9ef0c086308ac4b75ded6e84ad906(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ad34b16bc98900e9c084b81c0483f81ee12c2bce3f8cb9009489233a746263(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b558912d01e8c27d16b088f32d432032099d9f746c524fb2cef4bbdab8c41198(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c528c2f53cf2b360b860d38ba0f275d7752803b53e95fc4b1d56f3b474e51785(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87bf2811452ff1d407c45e0afbd04bdc5c3edb00f466cd0a1e3f0ad10ee69d5f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c934d10082c63fbf1868438659acee8a461e413c2012fba48bf8da3fb545ad26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e279c62dd1698352c2bb894ab9f4d66256557a1df30bb3c928c4bc20cf04e63b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c10485c5d0c61d59047fde5a9b1fbcc652c4d0dd30776c9228a07cb880519c5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe6d9daf308f6e57b70233f67c564f06ce549eee7106817f908df0d5766a524(
    *,
    ca: builtins.str,
    cert: builtins.str,
    private_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ec9a1ffe9972ad47fad590a3346fc1c1d72d38a90966e87774714f0b6c5514(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739f5df43aee79540b744cbb01c26b71c1c6ad137c13a8deb8385d3faad3fa65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f84bf313f63fb87e18841059a84ffd861d26cfc9790efd626053fb0452b6327c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c92f32ddf95cfb9727f04841ed608fd48bec2861ab8dee99fbbc2807cc02264(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2d8086005c2a0f9524869a92c03915698979df1d5475493a9b076dc186904cd(
    value: typing.Optional[CceClusterV3AuthenticatingProxy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97adab6f111c82eac678ca218cdbd038a24759af74e9e24c14a3a5eb40ba8141(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d5e13156638c47a358447f97f81fe13b92a737a9f7068fc774989b18da499a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__305b88ad7de7310cac99dce56d47e34450d6b5d51c5f9dc91fbf54c1fb3354f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9909340a9bc76e7dba32c2ae7215e94926ceafb6cc28c40dfb799e16bda20c6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26cf44d0cb08547ea20cc297000387c42ecc9dfa17f79c1834a1c06d569e04c3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ddd2afc4c52cd6282a3d55d2cb1578f2c80e3ee10cd041054445bdfc6cfd7fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8306dc9e78ff46f44c44937329cbe8aff1f967fd50c038cad60caee527abd42(
    value: typing.Optional[CceClusterV3CertificateClusters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2090f406feef2ac0b4fbd8d18ca3bd3de588102ba659e1a7d7b503e6a477baa9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047a427474b67b1fc0404de58ce69ab27a9463b0db7655630c4bd4404836ae46(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f88b664c469f306132ed3c6055b22da79fbd7f07a3d2c5d1c5643e7176ee1c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff4c983a1ed13186b07b6f727bab3ee2a6935f94304d1699ad2712ed0e6ac28(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00f78e25d487adad6ac96288cacac2632b8a638ffe11eb586f4aaf016ff3175(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbbe6b25940a672bdbeeacf06a90dbe0635134c4b18fe3b3f82404fe79508a4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ffd9e532666c9769aaefcff6579170c2b47634dda445b3dccacc53ae28439f(
    value: typing.Optional[CceClusterV3CertificateUsers],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0018adff4c4f0557be1ac98a122bacc94570e0375fcf04e887e36283c512e43b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_type: builtins.str,
    container_network_type: builtins.str,
    flavor_id: builtins.str,
    name: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    authenticating_proxy: typing.Optional[typing.Union[CceClusterV3AuthenticatingProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    authenticating_proxy_ca: typing.Optional[builtins.str] = None,
    authentication_mode: typing.Optional[builtins.str] = None,
    billing_mode: typing.Optional[jsii.Number] = None,
    cluster_version: typing.Optional[builtins.str] = None,
    container_network_cidr: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    eip: typing.Optional[builtins.str] = None,
    eni_subnet_cidr: typing.Optional[builtins.str] = None,
    eni_subnet_id: typing.Optional[builtins.str] = None,
    extend_param: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    highway_subnet_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_addons: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    kube_proxy_mode: typing.Optional[builtins.str] = None,
    kubernetes_svc_ip_range: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    multi_az: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    no_addons: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CceClusterV3Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba781513e5c3394c568f795a2c8bd1a8cd6777880a04a6cc11197678d1cad104(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5803e1b95951c157dad6c48b42603e29c2b44d886c0e518eb82ee2d740ce8d22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9cb6d5ebcf98e8825e0f17214077ca5f10112cab4a6f3cddeb461f4510ecb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f8196410f6ae43ad238e9c7357b8e52f4cb916618f48fd9fdf647087e711087(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de262efc7b642c4b609fb0c24ba92a248890c6e18ff478907424d8daa0ba218c(
    value: typing.Optional[typing.Union[CceClusterV3Timeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
