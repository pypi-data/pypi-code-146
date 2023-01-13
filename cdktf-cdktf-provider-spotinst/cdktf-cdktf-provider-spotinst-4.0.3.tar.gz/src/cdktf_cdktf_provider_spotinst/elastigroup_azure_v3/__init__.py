'''
# `spotinst_elastigroup_azure_v3`

Refer to the Terraform Registory for docs: [`spotinst_elastigroup_azure_v3`](https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3).
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


class ElastigroupAzureV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3 spotinst_elastigroup_azure_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        network: typing.Union["ElastigroupAzureV3Network", typing.Dict[builtins.str, typing.Any]],
        od_sizes: typing.Sequence[builtins.str],
        os: builtins.str,
        region: builtins.str,
        resource_group_name: builtins.str,
        spot_sizes: typing.Sequence[builtins.str],
        strategy: typing.Union["ElastigroupAzureV3Strategy", typing.Dict[builtins.str, typing.Any]],
        custom_data: typing.Optional[builtins.str] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastigroupAzureV3Image", typing.Dict[builtins.str, typing.Any]]]]] = None,
        login: typing.Optional[typing.Union["ElastigroupAzureV3Login", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_service_identity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastigroupAzureV3ManagedServiceIdentity", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_size: typing.Optional[jsii.Number] = None,
        min_size: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3 spotinst_elastigroup_azure_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#name ElastigroupAzureV3#name}.
        :param network: network block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#network ElastigroupAzureV3#network}
        :param od_sizes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#od_sizes ElastigroupAzureV3#od_sizes}.
        :param os: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#os ElastigroupAzureV3#os}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#region ElastigroupAzureV3#region}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#resource_group_name ElastigroupAzureV3#resource_group_name}.
        :param spot_sizes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#spot_sizes ElastigroupAzureV3#spot_sizes}.
        :param strategy: strategy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#strategy ElastigroupAzureV3#strategy}
        :param custom_data: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#custom_data ElastigroupAzureV3#custom_data}.
        :param desired_capacity: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#desired_capacity ElastigroupAzureV3#desired_capacity}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#id ElastigroupAzureV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image: image block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#image ElastigroupAzureV3#image}
        :param login: login block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#login ElastigroupAzureV3#login}
        :param managed_service_identity: managed_service_identity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#managed_service_identity ElastigroupAzureV3#managed_service_identity}
        :param max_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#max_size ElastigroupAzureV3#max_size}.
        :param min_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#min_size ElastigroupAzureV3#min_size}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53f7c061b4714ed0e34fd061e2e2b00e6d764bdcc37298b4b59f4797cf347893)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ElastigroupAzureV3Config(
            name=name,
            network=network,
            od_sizes=od_sizes,
            os=os,
            region=region,
            resource_group_name=resource_group_name,
            spot_sizes=spot_sizes,
            strategy=strategy,
            custom_data=custom_data,
            desired_capacity=desired_capacity,
            id=id,
            image=image,
            login=login,
            managed_service_identity=managed_service_identity,
            max_size=max_size,
            min_size=min_size,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putImage")
    def put_image(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastigroupAzureV3Image", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21d59cb1cb9dde435082d87fae76afe4c1f26e397ebd82861b71f68d27214b57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putImage", [value]))

    @jsii.member(jsii_name="putLogin")
    def put_login(
        self,
        *,
        user_name: builtins.str,
        password: typing.Optional[builtins.str] = None,
        ssh_public_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param user_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#user_name ElastigroupAzureV3#user_name}.
        :param password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#password ElastigroupAzureV3#password}.
        :param ssh_public_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#ssh_public_key ElastigroupAzureV3#ssh_public_key}.
        '''
        value = ElastigroupAzureV3Login(
            user_name=user_name, password=password, ssh_public_key=ssh_public_key
        )

        return typing.cast(None, jsii.invoke(self, "putLogin", [value]))

    @jsii.member(jsii_name="putManagedServiceIdentity")
    def put_managed_service_identity(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastigroupAzureV3ManagedServiceIdentity", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd7cd62849b1c2011977b8065f1f565cf340f1c12155e8213bb02a0b79f06dbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putManagedServiceIdentity", [value]))

    @jsii.member(jsii_name="putNetwork")
    def put_network(
        self,
        *,
        network_interfaces: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastigroupAzureV3NetworkNetworkInterfaces", typing.Dict[builtins.str, typing.Any]]]],
        resource_group_name: builtins.str,
        virtual_network_name: builtins.str,
    ) -> None:
        '''
        :param network_interfaces: network_interfaces block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#network_interfaces ElastigroupAzureV3#network_interfaces}
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#resource_group_name ElastigroupAzureV3#resource_group_name}.
        :param virtual_network_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#virtual_network_name ElastigroupAzureV3#virtual_network_name}.
        '''
        value = ElastigroupAzureV3Network(
            network_interfaces=network_interfaces,
            resource_group_name=resource_group_name,
            virtual_network_name=virtual_network_name,
        )

        return typing.cast(None, jsii.invoke(self, "putNetwork", [value]))

    @jsii.member(jsii_name="putStrategy")
    def put_strategy(
        self,
        *,
        draining_timeout: typing.Optional[jsii.Number] = None,
        fallback_to_on_demand: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        od_count: typing.Optional[jsii.Number] = None,
        spot_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param draining_timeout: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#draining_timeout ElastigroupAzureV3#draining_timeout}.
        :param fallback_to_on_demand: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#fallback_to_on_demand ElastigroupAzureV3#fallback_to_on_demand}.
        :param od_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#od_count ElastigroupAzureV3#od_count}.
        :param spot_percentage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#spot_percentage ElastigroupAzureV3#spot_percentage}.
        '''
        value = ElastigroupAzureV3Strategy(
            draining_timeout=draining_timeout,
            fallback_to_on_demand=fallback_to_on_demand,
            od_count=od_count,
            spot_percentage=spot_percentage,
        )

        return typing.cast(None, jsii.invoke(self, "putStrategy", [value]))

    @jsii.member(jsii_name="resetCustomData")
    def reset_custom_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomData", []))

    @jsii.member(jsii_name="resetDesiredCapacity")
    def reset_desired_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDesiredCapacity", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @jsii.member(jsii_name="resetLogin")
    def reset_login(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogin", []))

    @jsii.member(jsii_name="resetManagedServiceIdentity")
    def reset_managed_service_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedServiceIdentity", []))

    @jsii.member(jsii_name="resetMaxSize")
    def reset_max_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxSize", []))

    @jsii.member(jsii_name="resetMinSize")
    def reset_min_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinSize", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> "ElastigroupAzureV3ImageList":
        return typing.cast("ElastigroupAzureV3ImageList", jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="login")
    def login(self) -> "ElastigroupAzureV3LoginOutputReference":
        return typing.cast("ElastigroupAzureV3LoginOutputReference", jsii.get(self, "login"))

    @builtins.property
    @jsii.member(jsii_name="managedServiceIdentity")
    def managed_service_identity(
        self,
    ) -> "ElastigroupAzureV3ManagedServiceIdentityList":
        return typing.cast("ElastigroupAzureV3ManagedServiceIdentityList", jsii.get(self, "managedServiceIdentity"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> "ElastigroupAzureV3NetworkOutputReference":
        return typing.cast("ElastigroupAzureV3NetworkOutputReference", jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def strategy(self) -> "ElastigroupAzureV3StrategyOutputReference":
        return typing.cast("ElastigroupAzureV3StrategyOutputReference", jsii.get(self, "strategy"))

    @builtins.property
    @jsii.member(jsii_name="customDataInput")
    def custom_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customDataInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredCapacityInput")
    def desired_capacity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "desiredCapacityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastigroupAzureV3Image"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastigroupAzureV3Image"]]], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="loginInput")
    def login_input(self) -> typing.Optional["ElastigroupAzureV3Login"]:
        return typing.cast(typing.Optional["ElastigroupAzureV3Login"], jsii.get(self, "loginInput"))

    @builtins.property
    @jsii.member(jsii_name="managedServiceIdentityInput")
    def managed_service_identity_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastigroupAzureV3ManagedServiceIdentity"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastigroupAzureV3ManagedServiceIdentity"]]], jsii.get(self, "managedServiceIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="maxSizeInput")
    def max_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="minSizeInput")
    def min_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional["ElastigroupAzureV3Network"]:
        return typing.cast(typing.Optional["ElastigroupAzureV3Network"], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="odSizesInput")
    def od_sizes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "odSizesInput"))

    @builtins.property
    @jsii.member(jsii_name="osInput")
    def os_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="spotSizesInput")
    def spot_sizes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "spotSizesInput"))

    @builtins.property
    @jsii.member(jsii_name="strategyInput")
    def strategy_input(self) -> typing.Optional["ElastigroupAzureV3Strategy"]:
        return typing.cast(typing.Optional["ElastigroupAzureV3Strategy"], jsii.get(self, "strategyInput"))

    @builtins.property
    @jsii.member(jsii_name="customData")
    def custom_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customData"))

    @custom_data.setter
    def custom_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f876fbc4c7e79444086b5095158074843d1ff30b801c390e6a7240fb37d355d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customData", value)

    @builtins.property
    @jsii.member(jsii_name="desiredCapacity")
    def desired_capacity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "desiredCapacity"))

    @desired_capacity.setter
    def desired_capacity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe58ccb567210b120ce792fbbaa40aaa6dc07467cd0cc77229a285f4f2e574dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desiredCapacity", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f6d034d8a92d25a595356eda4160ff0849c893aa239daa1d6c9c22fb5162645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="maxSize")
    def max_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxSize"))

    @max_size.setter
    def max_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcd725f02a67b5ef7be31ba86897bf88c4e9077077ace70cf5da84203ca86879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSize", value)

    @builtins.property
    @jsii.member(jsii_name="minSize")
    def min_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minSize"))

    @min_size.setter
    def min_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f86b94b66b7a2f2a5077c493e3902acf43a99720cc101fcefc9ccc39fbbb8e84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minSize", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__662bb7b3318d34466a4f81f5394d52df5875516081bdcb71ba2155735ae3a99b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="odSizes")
    def od_sizes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "odSizes"))

    @od_sizes.setter
    def od_sizes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6557631629e2ab0f73736eefa1321f86a4e885f12b67a49a5d316d3a92a9787b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "odSizes", value)

    @builtins.property
    @jsii.member(jsii_name="os")
    def os(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "os"))

    @os.setter
    def os(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397fa1b95dee853896ce46be6ba62e69a3b6e2532fe28d9b4927a9af4f7e4d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "os", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07807e45fbffe00c3e7a6a9bdbecf1c268dfe46ca1a61df7a3a50468e72e25c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c628008e7b0a6e19c06d95614a1d68262e64998203a6d686308f4a7e15b13f67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="spotSizes")
    def spot_sizes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "spotSizes"))

    @spot_sizes.setter
    def spot_sizes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f95ad81266b6eb3cd6df1290086b54a7385c3d2763ea456ebd9716b7ff3aaa4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spotSizes", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3Config",
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
        "network": "network",
        "od_sizes": "odSizes",
        "os": "os",
        "region": "region",
        "resource_group_name": "resourceGroupName",
        "spot_sizes": "spotSizes",
        "strategy": "strategy",
        "custom_data": "customData",
        "desired_capacity": "desiredCapacity",
        "id": "id",
        "image": "image",
        "login": "login",
        "managed_service_identity": "managedServiceIdentity",
        "max_size": "maxSize",
        "min_size": "minSize",
    },
)
class ElastigroupAzureV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        network: typing.Union["ElastigroupAzureV3Network", typing.Dict[builtins.str, typing.Any]],
        od_sizes: typing.Sequence[builtins.str],
        os: builtins.str,
        region: builtins.str,
        resource_group_name: builtins.str,
        spot_sizes: typing.Sequence[builtins.str],
        strategy: typing.Union["ElastigroupAzureV3Strategy", typing.Dict[builtins.str, typing.Any]],
        custom_data: typing.Optional[builtins.str] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastigroupAzureV3Image", typing.Dict[builtins.str, typing.Any]]]]] = None,
        login: typing.Optional[typing.Union["ElastigroupAzureV3Login", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_service_identity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastigroupAzureV3ManagedServiceIdentity", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_size: typing.Optional[jsii.Number] = None,
        min_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#name ElastigroupAzureV3#name}.
        :param network: network block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#network ElastigroupAzureV3#network}
        :param od_sizes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#od_sizes ElastigroupAzureV3#od_sizes}.
        :param os: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#os ElastigroupAzureV3#os}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#region ElastigroupAzureV3#region}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#resource_group_name ElastigroupAzureV3#resource_group_name}.
        :param spot_sizes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#spot_sizes ElastigroupAzureV3#spot_sizes}.
        :param strategy: strategy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#strategy ElastigroupAzureV3#strategy}
        :param custom_data: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#custom_data ElastigroupAzureV3#custom_data}.
        :param desired_capacity: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#desired_capacity ElastigroupAzureV3#desired_capacity}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#id ElastigroupAzureV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image: image block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#image ElastigroupAzureV3#image}
        :param login: login block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#login ElastigroupAzureV3#login}
        :param managed_service_identity: managed_service_identity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#managed_service_identity ElastigroupAzureV3#managed_service_identity}
        :param max_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#max_size ElastigroupAzureV3#max_size}.
        :param min_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#min_size ElastigroupAzureV3#min_size}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(network, dict):
            network = ElastigroupAzureV3Network(**network)
        if isinstance(strategy, dict):
            strategy = ElastigroupAzureV3Strategy(**strategy)
        if isinstance(login, dict):
            login = ElastigroupAzureV3Login(**login)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a37fe9b0cf973e4644ab1bc2acecfc0f26ff2d3f60a2da163bfb6cf20b5f8d38)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument od_sizes", value=od_sizes, expected_type=type_hints["od_sizes"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument spot_sizes", value=spot_sizes, expected_type=type_hints["spot_sizes"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument custom_data", value=custom_data, expected_type=type_hints["custom_data"])
            check_type(argname="argument desired_capacity", value=desired_capacity, expected_type=type_hints["desired_capacity"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument login", value=login, expected_type=type_hints["login"])
            check_type(argname="argument managed_service_identity", value=managed_service_identity, expected_type=type_hints["managed_service_identity"])
            check_type(argname="argument max_size", value=max_size, expected_type=type_hints["max_size"])
            check_type(argname="argument min_size", value=min_size, expected_type=type_hints["min_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "network": network,
            "od_sizes": od_sizes,
            "os": os,
            "region": region,
            "resource_group_name": resource_group_name,
            "spot_sizes": spot_sizes,
            "strategy": strategy,
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
        if custom_data is not None:
            self._values["custom_data"] = custom_data
        if desired_capacity is not None:
            self._values["desired_capacity"] = desired_capacity
        if id is not None:
            self._values["id"] = id
        if image is not None:
            self._values["image"] = image
        if login is not None:
            self._values["login"] = login
        if managed_service_identity is not None:
            self._values["managed_service_identity"] = managed_service_identity
        if max_size is not None:
            self._values["max_size"] = max_size
        if min_size is not None:
            self._values["min_size"] = min_size

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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#name ElastigroupAzureV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network(self) -> "ElastigroupAzureV3Network":
        '''network block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#network ElastigroupAzureV3#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast("ElastigroupAzureV3Network", result)

    @builtins.property
    def od_sizes(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#od_sizes ElastigroupAzureV3#od_sizes}.'''
        result = self._values.get("od_sizes")
        assert result is not None, "Required property 'od_sizes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def os(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#os ElastigroupAzureV3#os}.'''
        result = self._values.get("os")
        assert result is not None, "Required property 'os' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#region ElastigroupAzureV3#region}.'''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#resource_group_name ElastigroupAzureV3#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spot_sizes(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#spot_sizes ElastigroupAzureV3#spot_sizes}.'''
        result = self._values.get("spot_sizes")
        assert result is not None, "Required property 'spot_sizes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def strategy(self) -> "ElastigroupAzureV3Strategy":
        '''strategy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#strategy ElastigroupAzureV3#strategy}
        '''
        result = self._values.get("strategy")
        assert result is not None, "Required property 'strategy' is missing"
        return typing.cast("ElastigroupAzureV3Strategy", result)

    @builtins.property
    def custom_data(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#custom_data ElastigroupAzureV3#custom_data}.'''
        result = self._values.get("custom_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#desired_capacity ElastigroupAzureV3#desired_capacity}.'''
        result = self._values.get("desired_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#id ElastigroupAzureV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastigroupAzureV3Image"]]]:
        '''image block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#image ElastigroupAzureV3#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastigroupAzureV3Image"]]], result)

    @builtins.property
    def login(self) -> typing.Optional["ElastigroupAzureV3Login"]:
        '''login block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#login ElastigroupAzureV3#login}
        '''
        result = self._values.get("login")
        return typing.cast(typing.Optional["ElastigroupAzureV3Login"], result)

    @builtins.property
    def managed_service_identity(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastigroupAzureV3ManagedServiceIdentity"]]]:
        '''managed_service_identity block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#managed_service_identity ElastigroupAzureV3#managed_service_identity}
        '''
        result = self._values.get("managed_service_identity")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastigroupAzureV3ManagedServiceIdentity"]]], result)

    @builtins.property
    def max_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#max_size ElastigroupAzureV3#max_size}.'''
        result = self._values.get("max_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#min_size ElastigroupAzureV3#min_size}.'''
        result = self._values.get("min_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastigroupAzureV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3Image",
    jsii_struct_bases=[],
    name_mapping={"custom": "custom", "marketplace": "marketplace"},
)
class ElastigroupAzureV3Image:
    def __init__(
        self,
        *,
        custom: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastigroupAzureV3ImageCustom", typing.Dict[builtins.str, typing.Any]]]]] = None,
        marketplace: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastigroupAzureV3ImageMarketplace", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param custom: custom block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#custom ElastigroupAzureV3#custom}
        :param marketplace: marketplace block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#marketplace ElastigroupAzureV3#marketplace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e10ba92c93d701fe0b4671d34e6c5ca1181d7604075bed1ddcc49858691fdf)
            check_type(argname="argument custom", value=custom, expected_type=type_hints["custom"])
            check_type(argname="argument marketplace", value=marketplace, expected_type=type_hints["marketplace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom is not None:
            self._values["custom"] = custom
        if marketplace is not None:
            self._values["marketplace"] = marketplace

    @builtins.property
    def custom(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastigroupAzureV3ImageCustom"]]]:
        '''custom block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#custom ElastigroupAzureV3#custom}
        '''
        result = self._values.get("custom")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastigroupAzureV3ImageCustom"]]], result)

    @builtins.property
    def marketplace(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastigroupAzureV3ImageMarketplace"]]]:
        '''marketplace block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#marketplace ElastigroupAzureV3#marketplace}
        '''
        result = self._values.get("marketplace")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastigroupAzureV3ImageMarketplace"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastigroupAzureV3Image(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3ImageCustom",
    jsii_struct_bases=[],
    name_mapping={
        "image_name": "imageName",
        "resource_group_name": "resourceGroupName",
    },
)
class ElastigroupAzureV3ImageCustom:
    def __init__(
        self,
        *,
        image_name: builtins.str,
        resource_group_name: builtins.str,
    ) -> None:
        '''
        :param image_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#image_name ElastigroupAzureV3#image_name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#resource_group_name ElastigroupAzureV3#resource_group_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b706e3fe3641269bc9c82998132305b573f433a63a553abc727dbbb296d5130)
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_name": image_name,
            "resource_group_name": resource_group_name,
        }

    @builtins.property
    def image_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#image_name ElastigroupAzureV3#image_name}.'''
        result = self._values.get("image_name")
        assert result is not None, "Required property 'image_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#resource_group_name ElastigroupAzureV3#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastigroupAzureV3ImageCustom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElastigroupAzureV3ImageCustomList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3ImageCustomList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba5532510f93dc827388ebded4851439b11c80358ace880f3768d97ed0affa28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ElastigroupAzureV3ImageCustomOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc91d2bf6bcfa551e272ba0e42dfce2ec79f6500561e7caceb1e9cd5efc2b9c4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ElastigroupAzureV3ImageCustomOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc9d9211714e8fb04527e7c4fbc0b73d978fd7d593a00acfed5f9ddc565af68)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a8fe0c671d3f2d4f01a0290f5a65b6c56ca224063523220e7882237d7918d3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51d8e154ba707b556409151e5176c095a784236e0d80edbacc89236090e0ce69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3ImageCustom]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3ImageCustom]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3ImageCustom]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d94eb8aeb647c69af925e5434d8de1d2ea4b9d40c417cd11a4797a0f9aee260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ElastigroupAzureV3ImageCustomOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3ImageCustomOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aba67e046e4dba931158e7ecd756b672e41b27963fae66860e364c4d2cc3cb73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="imageNameInput")
    def image_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageNameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa2a32b33b4082f7b1785585cf0418815f2a7b49482a81070a43e54e5d4e981)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae96aec00ed532d217647415d8eb425097fb4fee62a7ee45ffaccf30d7a64243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ElastigroupAzureV3ImageCustom, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ElastigroupAzureV3ImageCustom, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ElastigroupAzureV3ImageCustom, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63d119cdf05fb3731072049dc8d33c44a47f81b61cdff33f1c4d0b0ea4e1ea98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ElastigroupAzureV3ImageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3ImageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__416ce0ca42bbb32cc14d2505433ac3693e67e3c152e939336fdcd85afce1b8b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ElastigroupAzureV3ImageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__468380111501a6465c8ae3a0703665d86eb7ee9ac975a1e18433c8178756a9c7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ElastigroupAzureV3ImageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f7b55af6b5d6b1d5cb90b0fdbcb78f8b7a2f75b3f9543770f516c43c42169a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbe2151d99337411bc3723d4698735d8c88d5e8fae0516abf3a2d291f8b63d5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb6722460a5428272015e082bdd10541638dad20fb4eac4ad1eb122b8156043f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3Image]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3Image]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3Image]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a9acbe14471a5e031a401f42cacbe658dc0c347593a496fef1ecc0c2d587a25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3ImageMarketplace",
    jsii_struct_bases=[],
    name_mapping={
        "offer": "offer",
        "publisher": "publisher",
        "sku": "sku",
        "version": "version",
    },
)
class ElastigroupAzureV3ImageMarketplace:
    def __init__(
        self,
        *,
        offer: builtins.str,
        publisher: builtins.str,
        sku: builtins.str,
        version: builtins.str,
    ) -> None:
        '''
        :param offer: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#offer ElastigroupAzureV3#offer}.
        :param publisher: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#publisher ElastigroupAzureV3#publisher}.
        :param sku: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#sku ElastigroupAzureV3#sku}.
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#version ElastigroupAzureV3#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8388e3e4a39e3a9906e4a3c60449851ac382528556695e6608e02457da5d8604)
            check_type(argname="argument offer", value=offer, expected_type=type_hints["offer"])
            check_type(argname="argument publisher", value=publisher, expected_type=type_hints["publisher"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "offer": offer,
            "publisher": publisher,
            "sku": sku,
            "version": version,
        }

    @builtins.property
    def offer(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#offer ElastigroupAzureV3#offer}.'''
        result = self._values.get("offer")
        assert result is not None, "Required property 'offer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def publisher(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#publisher ElastigroupAzureV3#publisher}.'''
        result = self._values.get("publisher")
        assert result is not None, "Required property 'publisher' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sku(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#sku ElastigroupAzureV3#sku}.'''
        result = self._values.get("sku")
        assert result is not None, "Required property 'sku' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#version ElastigroupAzureV3#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastigroupAzureV3ImageMarketplace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElastigroupAzureV3ImageMarketplaceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3ImageMarketplaceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a539ce4d98452bb0a77ce65d692f808993b324f7076015c71b0f8b152c0913c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ElastigroupAzureV3ImageMarketplaceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__974bb7a284d976dbdcc8437293205705a062c232577a5d79965133ab75d3310c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ElastigroupAzureV3ImageMarketplaceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7df089e1553109bb55a3650ca5ccb451901179a080616d4f3c3a6a0c63889b3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d126e300dd7135dc38269521d604bdf9c3e9c328ec830cf8a805661f60aa20a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46f3ca5715d90382ad9893877f6e1760c4f61079a51f93e700b739cf121fc4b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3ImageMarketplace]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3ImageMarketplace]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3ImageMarketplace]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c04388dd152c1f70b530992cffdfaf37a833c6ac818523419ac0eb4f747b243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ElastigroupAzureV3ImageMarketplaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3ImageMarketplaceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3d1e7ac780e3d6e6f9765278895c0fcdb34be3b7981074826b93fa998064b72)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="offerInput")
    def offer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "offerInput"))

    @builtins.property
    @jsii.member(jsii_name="publisherInput")
    def publisher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publisherInput"))

    @builtins.property
    @jsii.member(jsii_name="skuInput")
    def sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="offer")
    def offer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "offer"))

    @offer.setter
    def offer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dfac443fed60e9ae17966508bfda3d870aca29c6c7b3597f3d37b4802277ae6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offer", value)

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisher"))

    @publisher.setter
    def publisher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__050b06d421cc3dd599bfb73b8763918320df14ffd5d41dde23c05d55de7d5957)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisher", value)

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sku"))

    @sku.setter
    def sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2e219391bd4962f59722ead5c749e304c5949aff0dcc1fc6c4c4bc4abadeab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sku", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__439bab063883d4ca5150b5437e1241bb4b81050df54babd28e8e2f84e2a95cf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ElastigroupAzureV3ImageMarketplace, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ElastigroupAzureV3ImageMarketplace, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ElastigroupAzureV3ImageMarketplace, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd87a4925a335ac29914978f5cd347e18d44e73a1629f95a593794214dbba7b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ElastigroupAzureV3ImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3ImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0626ca52cb736b9797c33941ed114ca7e7d50a76d1ef1e17d783932b7dc96fd7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCustom")
    def put_custom(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3ImageCustom, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd0bf1d928c0b830ab973bbcd4f06b0f7c78f97790df36f352f26f8e37cc08ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustom", [value]))

    @jsii.member(jsii_name="putMarketplace")
    def put_marketplace(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3ImageMarketplace, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a81b3a7351bc4c0dfa160e2cbcc26732c8beb5b1ee6f8ae64b2a7d0b0c4bee25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMarketplace", [value]))

    @jsii.member(jsii_name="resetCustom")
    def reset_custom(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustom", []))

    @jsii.member(jsii_name="resetMarketplace")
    def reset_marketplace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMarketplace", []))

    @builtins.property
    @jsii.member(jsii_name="custom")
    def custom(self) -> ElastigroupAzureV3ImageCustomList:
        return typing.cast(ElastigroupAzureV3ImageCustomList, jsii.get(self, "custom"))

    @builtins.property
    @jsii.member(jsii_name="marketplace")
    def marketplace(self) -> ElastigroupAzureV3ImageMarketplaceList:
        return typing.cast(ElastigroupAzureV3ImageMarketplaceList, jsii.get(self, "marketplace"))

    @builtins.property
    @jsii.member(jsii_name="customInput")
    def custom_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3ImageCustom]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3ImageCustom]]], jsii.get(self, "customInput"))

    @builtins.property
    @jsii.member(jsii_name="marketplaceInput")
    def marketplace_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3ImageMarketplace]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3ImageMarketplace]]], jsii.get(self, "marketplaceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ElastigroupAzureV3Image, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ElastigroupAzureV3Image, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ElastigroupAzureV3Image, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d64abb228c01ee3b5723124e63bd8b9efcb6f2a9b27cc6a7672d6f3250469b9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3Login",
    jsii_struct_bases=[],
    name_mapping={
        "user_name": "userName",
        "password": "password",
        "ssh_public_key": "sshPublicKey",
    },
)
class ElastigroupAzureV3Login:
    def __init__(
        self,
        *,
        user_name: builtins.str,
        password: typing.Optional[builtins.str] = None,
        ssh_public_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param user_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#user_name ElastigroupAzureV3#user_name}.
        :param password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#password ElastigroupAzureV3#password}.
        :param ssh_public_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#ssh_public_key ElastigroupAzureV3#ssh_public_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b1d1d9b43783755cdf7e18cc7daf7a64c654bfe52af2a762bfabd1ce1080664)
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument ssh_public_key", value=ssh_public_key, expected_type=type_hints["ssh_public_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_name": user_name,
        }
        if password is not None:
            self._values["password"] = password
        if ssh_public_key is not None:
            self._values["ssh_public_key"] = ssh_public_key

    @builtins.property
    def user_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#user_name ElastigroupAzureV3#user_name}.'''
        result = self._values.get("user_name")
        assert result is not None, "Required property 'user_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#password ElastigroupAzureV3#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_public_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#ssh_public_key ElastigroupAzureV3#ssh_public_key}.'''
        result = self._values.get("ssh_public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastigroupAzureV3Login(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElastigroupAzureV3LoginOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3LoginOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4486581ac2e21e7b2898e2badf02e67b266ced01fcd51cea8e9715f008b976f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetSshPublicKey")
    def reset_ssh_public_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshPublicKey", []))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeyInput")
    def ssh_public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshPublicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameInput")
    def user_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e8ddca03805e1ea13540a628ec9dcd10c5a8edda3c25108834f3ad5cc58331c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="sshPublicKey")
    def ssh_public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshPublicKey"))

    @ssh_public_key.setter
    def ssh_public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba02e2542838a2460bd9c20bb142b21a0c36ffdd431c276e7ea56b83cd9345ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPublicKey", value)

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44c9edfe177aab34c4b5698177c504aaf83350ec08e99e0639af3a583fe10c1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ElastigroupAzureV3Login]:
        return typing.cast(typing.Optional[ElastigroupAzureV3Login], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ElastigroupAzureV3Login]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4442eb8284d124c692f5fddd175c31a3d64fee50ae8418d6a8879ec77efee795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3ManagedServiceIdentity",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "resource_group_name": "resourceGroupName"},
)
class ElastigroupAzureV3ManagedServiceIdentity:
    def __init__(
        self,
        *,
        name: builtins.str,
        resource_group_name: builtins.str,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#name ElastigroupAzureV3#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#resource_group_name ElastigroupAzureV3#resource_group_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cd77a5a5e1bbf3e1e171cec737b8810efcc36fbdd5e05992d206af79d5147de)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "resource_group_name": resource_group_name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#name ElastigroupAzureV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#resource_group_name ElastigroupAzureV3#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastigroupAzureV3ManagedServiceIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElastigroupAzureV3ManagedServiceIdentityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3ManagedServiceIdentityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39830ecba4af83ef97289b94582719b096e548af55b16d38ba716a690a913abc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ElastigroupAzureV3ManagedServiceIdentityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb651768f6f25e72f16c428089b518ea7188c81a50e6a20129ee479e25fa54fd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ElastigroupAzureV3ManagedServiceIdentityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa5ab7a1fca0bcf0fa1c60a262520f6b1055683e4a0e1b4d790c369936423f22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0537a932103cd191f1c3cd89ee4599e99654640061399614cdaa4565517107f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7875ad0aee5a3cb311b4b395adf75e139458191c74c90c1adc12a15d153b2e3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3ManagedServiceIdentity]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3ManagedServiceIdentity]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3ManagedServiceIdentity]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398f7d010935d7a55b9272dbb97855bc03faf6efdc0d33005ca2478965be3216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ElastigroupAzureV3ManagedServiceIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3ManagedServiceIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd915668226e77ea7d731a67a7b350e36a88e9a4164ef401911daa4bff13e35a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df369b05a3a8e9383939ca0b04a1a2f5c3669756f9707a155ef5ab956223272a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09b62879c72cafe40ff2f7699bed99e242919b7cebc4eab0b25c3eed2317cfaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ElastigroupAzureV3ManagedServiceIdentity, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ElastigroupAzureV3ManagedServiceIdentity, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ElastigroupAzureV3ManagedServiceIdentity, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0247675ff18d3b3a3a278c7925d5437e4982a9ca157d9a0772aeb3384a6d4710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3Network",
    jsii_struct_bases=[],
    name_mapping={
        "network_interfaces": "networkInterfaces",
        "resource_group_name": "resourceGroupName",
        "virtual_network_name": "virtualNetworkName",
    },
)
class ElastigroupAzureV3Network:
    def __init__(
        self,
        *,
        network_interfaces: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastigroupAzureV3NetworkNetworkInterfaces", typing.Dict[builtins.str, typing.Any]]]],
        resource_group_name: builtins.str,
        virtual_network_name: builtins.str,
    ) -> None:
        '''
        :param network_interfaces: network_interfaces block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#network_interfaces ElastigroupAzureV3#network_interfaces}
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#resource_group_name ElastigroupAzureV3#resource_group_name}.
        :param virtual_network_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#virtual_network_name ElastigroupAzureV3#virtual_network_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad1f2de604be5662221076d1e442d12906d979412eda559f5a64217832abe28)
            check_type(argname="argument network_interfaces", value=network_interfaces, expected_type=type_hints["network_interfaces"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument virtual_network_name", value=virtual_network_name, expected_type=type_hints["virtual_network_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_interfaces": network_interfaces,
            "resource_group_name": resource_group_name,
            "virtual_network_name": virtual_network_name,
        }

    @builtins.property
    def network_interfaces(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastigroupAzureV3NetworkNetworkInterfaces"]]:
        '''network_interfaces block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#network_interfaces ElastigroupAzureV3#network_interfaces}
        '''
        result = self._values.get("network_interfaces")
        assert result is not None, "Required property 'network_interfaces' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastigroupAzureV3NetworkNetworkInterfaces"]], result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#resource_group_name ElastigroupAzureV3#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_network_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#virtual_network_name ElastigroupAzureV3#virtual_network_name}.'''
        result = self._values.get("virtual_network_name")
        assert result is not None, "Required property 'virtual_network_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastigroupAzureV3Network(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3NetworkNetworkInterfaces",
    jsii_struct_bases=[],
    name_mapping={
        "assign_public_ip": "assignPublicIp",
        "is_primary": "isPrimary",
        "subnet_name": "subnetName",
        "additional_ip_configs": "additionalIpConfigs",
        "application_security_group": "applicationSecurityGroup",
    },
)
class ElastigroupAzureV3NetworkNetworkInterfaces:
    def __init__(
        self,
        *,
        assign_public_ip: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        is_primary: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        subnet_name: builtins.str,
        additional_ip_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        application_security_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroup", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param assign_public_ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#assign_public_ip ElastigroupAzureV3#assign_public_ip}.
        :param is_primary: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#is_primary ElastigroupAzureV3#is_primary}.
        :param subnet_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#subnet_name ElastigroupAzureV3#subnet_name}.
        :param additional_ip_configs: additional_ip_configs block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#additional_ip_configs ElastigroupAzureV3#additional_ip_configs}
        :param application_security_group: application_security_group block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#application_security_group ElastigroupAzureV3#application_security_group}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1164f1e62c0db97ffaa3e7ad90b071722095b4018292ac3c717412f1bd568078)
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument is_primary", value=is_primary, expected_type=type_hints["is_primary"])
            check_type(argname="argument subnet_name", value=subnet_name, expected_type=type_hints["subnet_name"])
            check_type(argname="argument additional_ip_configs", value=additional_ip_configs, expected_type=type_hints["additional_ip_configs"])
            check_type(argname="argument application_security_group", value=application_security_group, expected_type=type_hints["application_security_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "assign_public_ip": assign_public_ip,
            "is_primary": is_primary,
            "subnet_name": subnet_name,
        }
        if additional_ip_configs is not None:
            self._values["additional_ip_configs"] = additional_ip_configs
        if application_security_group is not None:
            self._values["application_security_group"] = application_security_group

    @builtins.property
    def assign_public_ip(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#assign_public_ip ElastigroupAzureV3#assign_public_ip}.'''
        result = self._values.get("assign_public_ip")
        assert result is not None, "Required property 'assign_public_ip' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def is_primary(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#is_primary ElastigroupAzureV3#is_primary}.'''
        result = self._values.get("is_primary")
        assert result is not None, "Required property 'is_primary' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def subnet_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#subnet_name ElastigroupAzureV3#subnet_name}.'''
        result = self._values.get("subnet_name")
        assert result is not None, "Required property 'subnet_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_ip_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigs"]]]:
        '''additional_ip_configs block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#additional_ip_configs ElastigroupAzureV3#additional_ip_configs}
        '''
        result = self._values.get("additional_ip_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigs"]]], result)

    @builtins.property
    def application_security_group(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroup"]]]:
        '''application_security_group block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#application_security_group ElastigroupAzureV3#application_security_group}
        '''
        result = self._values.get("application_security_group")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroup"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastigroupAzureV3NetworkNetworkInterfaces(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigs",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "private_ip_version": "privateIpVersion"},
)
class ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigs:
    def __init__(
        self,
        *,
        name: builtins.str,
        private_ip_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#name ElastigroupAzureV3#name}.
        :param private_ip_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#private_ip_version ElastigroupAzureV3#private_ip_version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d4d3434341c207b3ec51f6d668e14ca7107101d1fee721d55e5aefef05d83c3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument private_ip_version", value=private_ip_version, expected_type=type_hints["private_ip_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if private_ip_version is not None:
            self._values["private_ip_version"] = private_ip_version

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#name ElastigroupAzureV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def private_ip_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#private_ip_version ElastigroupAzureV3#private_ip_version}.'''
        result = self._values.get("private_ip_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3803d49b5fa57a5101f0b447936f2991f0f7ec901102032e77c82187507ccdf4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27ab624df4e11dd4560d6f957e10b270305a74303569831751a6a1c66f913656)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e2a5d19ddc93f43529326a40e34b9429722f065c278c55989347abdfed57b7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c68c8d5b0ffd385db80361863d8253944a34f7f342085dc7c2dd745537c9939)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c97be3744c82a6be2aeaa64d13610d269e6ba75dba86e78d8358394be7ecad1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09e7c284f5ddee1882d17a8c31757fca8d5b88cea25bde78a2b37fabeba923cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8f243a4832d5755c3a56eaf3a31629c38535c58221cd3ee1e371421cde6cc5c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPrivateIpVersion")
    def reset_private_ip_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIpVersion", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpVersionInput")
    def private_ip_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d512576860dd3679731f08f5860bbcda631106257078f7453426bf8e4829110f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="privateIpVersion")
    def private_ip_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpVersion"))

    @private_ip_version.setter
    def private_ip_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0931ac945b76e2846114d31710d793ff821005e7ca9913ed5f7dacee394c7fd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpVersion", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigs, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigs, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigs, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e5f8997cd092fab7efcb7236e4cc06e27cee5321804d6f063f0a9e521b474a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroup",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "resource_group_name": "resourceGroupName"},
)
class ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroup:
    def __init__(
        self,
        *,
        name: builtins.str,
        resource_group_name: builtins.str,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#name ElastigroupAzureV3#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#resource_group_name ElastigroupAzureV3#resource_group_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__069e5262d21768eda7fbe63efe689bfa156a7a881f515c81f9bb7759cadde0fa)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "resource_group_name": resource_group_name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#name ElastigroupAzureV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#resource_group_name ElastigroupAzureV3#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroupList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroupList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee9b39024740c6a07a0a7bce6a7796d2fa23bf89d389165cc346942c24008359)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroupOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b344f1763181d8852ed702ee38a4f8b6eea8176aa059c614d0f15c79bfb93ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroupOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a334b16050c5514e674652464dc0b092cb2b6e6bcbdeb9d453e60e8b0aaaedc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__beb68546299f4373f8390d647e6b783d93b4258d87f9288136f57a7a45c245a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9493b82111ad39e8436b96d724678b43209cd62a641113cfb74280595fa5290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroup]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroup]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ca3592a4e239bad279dfc031b3b1903100e0bcf68e63e947b1694589501867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6db43efef1e1b0285545a4e043aebe5d559f5dcbe0881cd9e1059d017f05b92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cb1c62f0ff02975a21ef54ea813d64474c71aa0b41f86698bd7e0d7b262f903)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de8bc6c2577554052714902e60e27cbb5fdc0a30359fcd5edde1a6a67df2f83a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroup, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroup, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroup, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a53a28f44f14a4ee3ccf23abba226e5fbd0ae7eff777c6ca9da8c15393bbbad3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ElastigroupAzureV3NetworkNetworkInterfacesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3NetworkNetworkInterfacesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b300f518196c9a299f7e624fdc72d6bff3cd931a7e89b9bb86c1ec8fbb24f50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ElastigroupAzureV3NetworkNetworkInterfacesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71379ed071e6f73460cdfe2f005b131b2ea9066af94ad87a1047b90f411aba54)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ElastigroupAzureV3NetworkNetworkInterfacesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0de009dbea5e8c23906a5e0d20fc49d2900e2fd8d3d35bccb4f7da798bd77988)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47ef9cf98151345850f79d78832c522ab934b08cea5470810bae0e3f7e830aa5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25f8db7188f11e25187fb72d0dfaafd02622e19799dcc73f51ceffbcd2a2f250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3NetworkNetworkInterfaces]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3NetworkNetworkInterfaces]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3NetworkNetworkInterfaces]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cf921ecec5596b0c838f5871eae2f7e00f96f5f1d2e7955a0cb381ac8208134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ElastigroupAzureV3NetworkNetworkInterfacesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3NetworkNetworkInterfacesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c360ea491c0ed2616b14c409fd03abfae141a882d2f379347701ae8f4f876c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAdditionalIpConfigs")
    def put_additional_ip_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f0311baec94a2c5bed16aa63d074801c231e846d3ce73c100b110091f0acc82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalIpConfigs", [value]))

    @jsii.member(jsii_name="putApplicationSecurityGroup")
    def put_application_security_group(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroup, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3674d5efc0563324862aed029173f7e58654de011b9a3741ebbc04b2eb14a1e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putApplicationSecurityGroup", [value]))

    @jsii.member(jsii_name="resetAdditionalIpConfigs")
    def reset_additional_ip_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalIpConfigs", []))

    @jsii.member(jsii_name="resetApplicationSecurityGroup")
    def reset_application_security_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationSecurityGroup", []))

    @builtins.property
    @jsii.member(jsii_name="additionalIpConfigs")
    def additional_ip_configs(
        self,
    ) -> ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigsList:
        return typing.cast(ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigsList, jsii.get(self, "additionalIpConfigs"))

    @builtins.property
    @jsii.member(jsii_name="applicationSecurityGroup")
    def application_security_group(
        self,
    ) -> ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroupList:
        return typing.cast(ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroupList, jsii.get(self, "applicationSecurityGroup"))

    @builtins.property
    @jsii.member(jsii_name="additionalIpConfigsInput")
    def additional_ip_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigs]]], jsii.get(self, "additionalIpConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationSecurityGroupInput")
    def application_security_group_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroup]]], jsii.get(self, "applicationSecurityGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="assignPublicIpInput")
    def assign_public_ip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "assignPublicIpInput"))

    @builtins.property
    @jsii.member(jsii_name="isPrimaryInput")
    def is_primary_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isPrimaryInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetNameInput")
    def subnet_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "assignPublicIp"))

    @assign_public_ip.setter
    def assign_public_ip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d68b53344d678a6906a12d5b6c66166415b62f0934b97aa91ecf9e42d33eb7c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assignPublicIp", value)

    @builtins.property
    @jsii.member(jsii_name="isPrimary")
    def is_primary(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isPrimary"))

    @is_primary.setter
    def is_primary(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16161fec59a4e9e1a1df69078e0d87731f49e5e45acc85eb17f47708fdd39b45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isPrimary", value)

    @builtins.property
    @jsii.member(jsii_name="subnetName")
    def subnet_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetName"))

    @subnet_name.setter
    def subnet_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cf9bf0b8e3f28eae29ef52bfdb4acac52f6f064c982e118c238cbb4b44c0d98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ElastigroupAzureV3NetworkNetworkInterfaces, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ElastigroupAzureV3NetworkNetworkInterfaces, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ElastigroupAzureV3NetworkNetworkInterfaces, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fe32d5d42799ac42ac0cdca668ac02d5af53af8d610a54578df1c5b92b02575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ElastigroupAzureV3NetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3NetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60fa0ce4ad59907ad9343caba70f4323864a6ca66f53223eae29265e5a23abb8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNetworkInterfaces")
    def put_network_interfaces(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3NetworkNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da5cc9a5e0de23908a7d5607142470f724e26c3670f1b1706ac13a036ff14fe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworkInterfaces", [value]))

    @builtins.property
    @jsii.member(jsii_name="networkInterfaces")
    def network_interfaces(self) -> ElastigroupAzureV3NetworkNetworkInterfacesList:
        return typing.cast(ElastigroupAzureV3NetworkNetworkInterfacesList, jsii.get(self, "networkInterfaces"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfacesInput")
    def network_interfaces_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3NetworkNetworkInterfaces]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3NetworkNetworkInterfaces]]], jsii.get(self, "networkInterfacesInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkNameInput")
    def virtual_network_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkNameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b2c49aa895598ee323243c62b314534c44ab5e7b795f97e8342553bc4ed455)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkName")
    def virtual_network_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkName"))

    @virtual_network_name.setter
    def virtual_network_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c74a488ca47ae06f34ff31d020eaca8150a35ce413626b9d0c864198e313f35f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ElastigroupAzureV3Network]:
        return typing.cast(typing.Optional[ElastigroupAzureV3Network], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ElastigroupAzureV3Network]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f704e47e954be4cf434ea9a09bf2f4de140868054034bf52cf79d3836c52f04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3Strategy",
    jsii_struct_bases=[],
    name_mapping={
        "draining_timeout": "drainingTimeout",
        "fallback_to_on_demand": "fallbackToOnDemand",
        "od_count": "odCount",
        "spot_percentage": "spotPercentage",
    },
)
class ElastigroupAzureV3Strategy:
    def __init__(
        self,
        *,
        draining_timeout: typing.Optional[jsii.Number] = None,
        fallback_to_on_demand: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        od_count: typing.Optional[jsii.Number] = None,
        spot_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param draining_timeout: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#draining_timeout ElastigroupAzureV3#draining_timeout}.
        :param fallback_to_on_demand: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#fallback_to_on_demand ElastigroupAzureV3#fallback_to_on_demand}.
        :param od_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#od_count ElastigroupAzureV3#od_count}.
        :param spot_percentage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#spot_percentage ElastigroupAzureV3#spot_percentage}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a897e4fc9edb678a4ffe7b9e411d52707749f7443b53df2eea8daf41113c6f75)
            check_type(argname="argument draining_timeout", value=draining_timeout, expected_type=type_hints["draining_timeout"])
            check_type(argname="argument fallback_to_on_demand", value=fallback_to_on_demand, expected_type=type_hints["fallback_to_on_demand"])
            check_type(argname="argument od_count", value=od_count, expected_type=type_hints["od_count"])
            check_type(argname="argument spot_percentage", value=spot_percentage, expected_type=type_hints["spot_percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if draining_timeout is not None:
            self._values["draining_timeout"] = draining_timeout
        if fallback_to_on_demand is not None:
            self._values["fallback_to_on_demand"] = fallback_to_on_demand
        if od_count is not None:
            self._values["od_count"] = od_count
        if spot_percentage is not None:
            self._values["spot_percentage"] = spot_percentage

    @builtins.property
    def draining_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#draining_timeout ElastigroupAzureV3#draining_timeout}.'''
        result = self._values.get("draining_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fallback_to_on_demand(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#fallback_to_on_demand ElastigroupAzureV3#fallback_to_on_demand}.'''
        result = self._values.get("fallback_to_on_demand")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def od_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#od_count ElastigroupAzureV3#od_count}.'''
        result = self._values.get("od_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def spot_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/elastigroup_azure_v3#spot_percentage ElastigroupAzureV3#spot_percentage}.'''
        result = self._values.get("spot_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastigroupAzureV3Strategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElastigroupAzureV3StrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.elastigroupAzureV3.ElastigroupAzureV3StrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__186ef4435d0e90ceead66ccba1aa1d8128476d2950623c03f9a68c3e2916908a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDrainingTimeout")
    def reset_draining_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDrainingTimeout", []))

    @jsii.member(jsii_name="resetFallbackToOnDemand")
    def reset_fallback_to_on_demand(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFallbackToOnDemand", []))

    @jsii.member(jsii_name="resetOdCount")
    def reset_od_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOdCount", []))

    @jsii.member(jsii_name="resetSpotPercentage")
    def reset_spot_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpotPercentage", []))

    @builtins.property
    @jsii.member(jsii_name="drainingTimeoutInput")
    def draining_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "drainingTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="fallbackToOnDemandInput")
    def fallback_to_on_demand_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fallbackToOnDemandInput"))

    @builtins.property
    @jsii.member(jsii_name="odCountInput")
    def od_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "odCountInput"))

    @builtins.property
    @jsii.member(jsii_name="spotPercentageInput")
    def spot_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "spotPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="drainingTimeout")
    def draining_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "drainingTimeout"))

    @draining_timeout.setter
    def draining_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa5754de73dc2191c76cb49e18d711d29d0270320be632149daa5b14cfb1bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "drainingTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="fallbackToOnDemand")
    def fallback_to_on_demand(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fallbackToOnDemand"))

    @fallback_to_on_demand.setter
    def fallback_to_on_demand(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd9bfa1dd355c80568ed5f451e1201434903a610300e1128a95e0488b3257337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fallbackToOnDemand", value)

    @builtins.property
    @jsii.member(jsii_name="odCount")
    def od_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "odCount"))

    @od_count.setter
    def od_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c61f554738c530c45797b3b97035733fdd242938a61015a20a74b070563ee49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "odCount", value)

    @builtins.property
    @jsii.member(jsii_name="spotPercentage")
    def spot_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "spotPercentage"))

    @spot_percentage.setter
    def spot_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0a9a90250dffa5c02824ff561f504bac408685e68785f8d79645bc7b446f80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spotPercentage", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ElastigroupAzureV3Strategy]:
        return typing.cast(typing.Optional[ElastigroupAzureV3Strategy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElastigroupAzureV3Strategy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__353f94f214ceedc5645068d01cde335bc16a8d65dfe42ebee654cd0922d30eb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ElastigroupAzureV3",
    "ElastigroupAzureV3Config",
    "ElastigroupAzureV3Image",
    "ElastigroupAzureV3ImageCustom",
    "ElastigroupAzureV3ImageCustomList",
    "ElastigroupAzureV3ImageCustomOutputReference",
    "ElastigroupAzureV3ImageList",
    "ElastigroupAzureV3ImageMarketplace",
    "ElastigroupAzureV3ImageMarketplaceList",
    "ElastigroupAzureV3ImageMarketplaceOutputReference",
    "ElastigroupAzureV3ImageOutputReference",
    "ElastigroupAzureV3Login",
    "ElastigroupAzureV3LoginOutputReference",
    "ElastigroupAzureV3ManagedServiceIdentity",
    "ElastigroupAzureV3ManagedServiceIdentityList",
    "ElastigroupAzureV3ManagedServiceIdentityOutputReference",
    "ElastigroupAzureV3Network",
    "ElastigroupAzureV3NetworkNetworkInterfaces",
    "ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigs",
    "ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigsList",
    "ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigsOutputReference",
    "ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroup",
    "ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroupList",
    "ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroupOutputReference",
    "ElastigroupAzureV3NetworkNetworkInterfacesList",
    "ElastigroupAzureV3NetworkNetworkInterfacesOutputReference",
    "ElastigroupAzureV3NetworkOutputReference",
    "ElastigroupAzureV3Strategy",
    "ElastigroupAzureV3StrategyOutputReference",
]

publication.publish()

def _typecheckingstub__53f7c061b4714ed0e34fd061e2e2b00e6d764bdcc37298b4b59f4797cf347893(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    network: typing.Union[ElastigroupAzureV3Network, typing.Dict[builtins.str, typing.Any]],
    od_sizes: typing.Sequence[builtins.str],
    os: builtins.str,
    region: builtins.str,
    resource_group_name: builtins.str,
    spot_sizes: typing.Sequence[builtins.str],
    strategy: typing.Union[ElastigroupAzureV3Strategy, typing.Dict[builtins.str, typing.Any]],
    custom_data: typing.Optional[builtins.str] = None,
    desired_capacity: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3Image, typing.Dict[builtins.str, typing.Any]]]]] = None,
    login: typing.Optional[typing.Union[ElastigroupAzureV3Login, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_service_identity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3ManagedServiceIdentity, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_size: typing.Optional[jsii.Number] = None,
    min_size: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__21d59cb1cb9dde435082d87fae76afe4c1f26e397ebd82861b71f68d27214b57(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3Image, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7cd62849b1c2011977b8065f1f565cf340f1c12155e8213bb02a0b79f06dbe(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3ManagedServiceIdentity, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f876fbc4c7e79444086b5095158074843d1ff30b801c390e6a7240fb37d355d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe58ccb567210b120ce792fbbaa40aaa6dc07467cd0cc77229a285f4f2e574dd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f6d034d8a92d25a595356eda4160ff0849c893aa239daa1d6c9c22fb5162645(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd725f02a67b5ef7be31ba86897bf88c4e9077077ace70cf5da84203ca86879(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f86b94b66b7a2f2a5077c493e3902acf43a99720cc101fcefc9ccc39fbbb8e84(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662bb7b3318d34466a4f81f5394d52df5875516081bdcb71ba2155735ae3a99b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6557631629e2ab0f73736eefa1321f86a4e885f12b67a49a5d316d3a92a9787b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397fa1b95dee853896ce46be6ba62e69a3b6e2532fe28d9b4927a9af4f7e4d96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07807e45fbffe00c3e7a6a9bdbecf1c268dfe46ca1a61df7a3a50468e72e25c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c628008e7b0a6e19c06d95614a1d68262e64998203a6d686308f4a7e15b13f67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f95ad81266b6eb3cd6df1290086b54a7385c3d2763ea456ebd9716b7ff3aaa4a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a37fe9b0cf973e4644ab1bc2acecfc0f26ff2d3f60a2da163bfb6cf20b5f8d38(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    network: typing.Union[ElastigroupAzureV3Network, typing.Dict[builtins.str, typing.Any]],
    od_sizes: typing.Sequence[builtins.str],
    os: builtins.str,
    region: builtins.str,
    resource_group_name: builtins.str,
    spot_sizes: typing.Sequence[builtins.str],
    strategy: typing.Union[ElastigroupAzureV3Strategy, typing.Dict[builtins.str, typing.Any]],
    custom_data: typing.Optional[builtins.str] = None,
    desired_capacity: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3Image, typing.Dict[builtins.str, typing.Any]]]]] = None,
    login: typing.Optional[typing.Union[ElastigroupAzureV3Login, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_service_identity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3ManagedServiceIdentity, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_size: typing.Optional[jsii.Number] = None,
    min_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e10ba92c93d701fe0b4671d34e6c5ca1181d7604075bed1ddcc49858691fdf(
    *,
    custom: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3ImageCustom, typing.Dict[builtins.str, typing.Any]]]]] = None,
    marketplace: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3ImageMarketplace, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b706e3fe3641269bc9c82998132305b573f433a63a553abc727dbbb296d5130(
    *,
    image_name: builtins.str,
    resource_group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba5532510f93dc827388ebded4851439b11c80358ace880f3768d97ed0affa28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc91d2bf6bcfa551e272ba0e42dfce2ec79f6500561e7caceb1e9cd5efc2b9c4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc9d9211714e8fb04527e7c4fbc0b73d978fd7d593a00acfed5f9ddc565af68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a8fe0c671d3f2d4f01a0290f5a65b6c56ca224063523220e7882237d7918d3a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d8e154ba707b556409151e5176c095a784236e0d80edbacc89236090e0ce69(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d94eb8aeb647c69af925e5434d8de1d2ea4b9d40c417cd11a4797a0f9aee260(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3ImageCustom]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba67e046e4dba931158e7ecd756b672e41b27963fae66860e364c4d2cc3cb73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa2a32b33b4082f7b1785585cf0418815f2a7b49482a81070a43e54e5d4e981(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae96aec00ed532d217647415d8eb425097fb4fee62a7ee45ffaccf30d7a64243(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63d119cdf05fb3731072049dc8d33c44a47f81b61cdff33f1c4d0b0ea4e1ea98(
    value: typing.Optional[typing.Union[ElastigroupAzureV3ImageCustom, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__416ce0ca42bbb32cc14d2505433ac3693e67e3c152e939336fdcd85afce1b8b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468380111501a6465c8ae3a0703665d86eb7ee9ac975a1e18433c8178756a9c7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f7b55af6b5d6b1d5cb90b0fdbcb78f8b7a2f75b3f9543770f516c43c42169a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe2151d99337411bc3723d4698735d8c88d5e8fae0516abf3a2d291f8b63d5e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6722460a5428272015e082bdd10541638dad20fb4eac4ad1eb122b8156043f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9acbe14471a5e031a401f42cacbe658dc0c347593a496fef1ecc0c2d587a25(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3Image]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8388e3e4a39e3a9906e4a3c60449851ac382528556695e6608e02457da5d8604(
    *,
    offer: builtins.str,
    publisher: builtins.str,
    sku: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a539ce4d98452bb0a77ce65d692f808993b324f7076015c71b0f8b152c0913c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__974bb7a284d976dbdcc8437293205705a062c232577a5d79965133ab75d3310c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df089e1553109bb55a3650ca5ccb451901179a080616d4f3c3a6a0c63889b3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d126e300dd7135dc38269521d604bdf9c3e9c328ec830cf8a805661f60aa20a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f3ca5715d90382ad9893877f6e1760c4f61079a51f93e700b739cf121fc4b4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c04388dd152c1f70b530992cffdfaf37a833c6ac818523419ac0eb4f747b243(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3ImageMarketplace]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d1e7ac780e3d6e6f9765278895c0fcdb34be3b7981074826b93fa998064b72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dfac443fed60e9ae17966508bfda3d870aca29c6c7b3597f3d37b4802277ae6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050b06d421cc3dd599bfb73b8763918320df14ffd5d41dde23c05d55de7d5957(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e219391bd4962f59722ead5c749e304c5949aff0dcc1fc6c4c4bc4abadeab2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__439bab063883d4ca5150b5437e1241bb4b81050df54babd28e8e2f84e2a95cf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd87a4925a335ac29914978f5cd347e18d44e73a1629f95a593794214dbba7b1(
    value: typing.Optional[typing.Union[ElastigroupAzureV3ImageMarketplace, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0626ca52cb736b9797c33941ed114ca7e7d50a76d1ef1e17d783932b7dc96fd7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0bf1d928c0b830ab973bbcd4f06b0f7c78f97790df36f352f26f8e37cc08ed(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3ImageCustom, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81b3a7351bc4c0dfa160e2cbcc26732c8beb5b1ee6f8ae64b2a7d0b0c4bee25(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3ImageMarketplace, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64abb228c01ee3b5723124e63bd8b9efcb6f2a9b27cc6a7672d6f3250469b9a(
    value: typing.Optional[typing.Union[ElastigroupAzureV3Image, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b1d1d9b43783755cdf7e18cc7daf7a64c654bfe52af2a762bfabd1ce1080664(
    *,
    user_name: builtins.str,
    password: typing.Optional[builtins.str] = None,
    ssh_public_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4486581ac2e21e7b2898e2badf02e67b266ced01fcd51cea8e9715f008b976f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e8ddca03805e1ea13540a628ec9dcd10c5a8edda3c25108834f3ad5cc58331c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba02e2542838a2460bd9c20bb142b21a0c36ffdd431c276e7ea56b83cd9345ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c9edfe177aab34c4b5698177c504aaf83350ec08e99e0639af3a583fe10c1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4442eb8284d124c692f5fddd175c31a3d64fee50ae8418d6a8879ec77efee795(
    value: typing.Optional[ElastigroupAzureV3Login],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd77a5a5e1bbf3e1e171cec737b8810efcc36fbdd5e05992d206af79d5147de(
    *,
    name: builtins.str,
    resource_group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39830ecba4af83ef97289b94582719b096e548af55b16d38ba716a690a913abc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb651768f6f25e72f16c428089b518ea7188c81a50e6a20129ee479e25fa54fd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa5ab7a1fca0bcf0fa1c60a262520f6b1055683e4a0e1b4d790c369936423f22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0537a932103cd191f1c3cd89ee4599e99654640061399614cdaa4565517107f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7875ad0aee5a3cb311b4b395adf75e139458191c74c90c1adc12a15d153b2e3c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398f7d010935d7a55b9272dbb97855bc03faf6efdc0d33005ca2478965be3216(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3ManagedServiceIdentity]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd915668226e77ea7d731a67a7b350e36a88e9a4164ef401911daa4bff13e35a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df369b05a3a8e9383939ca0b04a1a2f5c3669756f9707a155ef5ab956223272a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b62879c72cafe40ff2f7699bed99e242919b7cebc4eab0b25c3eed2317cfaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0247675ff18d3b3a3a278c7925d5437e4982a9ca157d9a0772aeb3384a6d4710(
    value: typing.Optional[typing.Union[ElastigroupAzureV3ManagedServiceIdentity, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad1f2de604be5662221076d1e442d12906d979412eda559f5a64217832abe28(
    *,
    network_interfaces: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3NetworkNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]],
    resource_group_name: builtins.str,
    virtual_network_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1164f1e62c0db97ffaa3e7ad90b071722095b4018292ac3c717412f1bd568078(
    *,
    assign_public_ip: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    is_primary: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    subnet_name: builtins.str,
    additional_ip_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    application_security_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroup, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d4d3434341c207b3ec51f6d668e14ca7107101d1fee721d55e5aefef05d83c3(
    *,
    name: builtins.str,
    private_ip_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3803d49b5fa57a5101f0b447936f2991f0f7ec901102032e77c82187507ccdf4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ab624df4e11dd4560d6f957e10b270305a74303569831751a6a1c66f913656(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2a5d19ddc93f43529326a40e34b9429722f065c278c55989347abdfed57b7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c68c8d5b0ffd385db80361863d8253944a34f7f342085dc7c2dd745537c9939(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c97be3744c82a6be2aeaa64d13610d269e6ba75dba86e78d8358394be7ecad1b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e7c284f5ddee1882d17a8c31757fca8d5b88cea25bde78a2b37fabeba923cc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f243a4832d5755c3a56eaf3a31629c38535c58221cd3ee1e371421cde6cc5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d512576860dd3679731f08f5860bbcda631106257078f7453426bf8e4829110f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0931ac945b76e2846114d31710d793ff821005e7ca9913ed5f7dacee394c7fd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e5f8997cd092fab7efcb7236e4cc06e27cee5321804d6f063f0a9e521b474a8(
    value: typing.Optional[typing.Union[ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigs, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__069e5262d21768eda7fbe63efe689bfa156a7a881f515c81f9bb7759cadde0fa(
    *,
    name: builtins.str,
    resource_group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9b39024740c6a07a0a7bce6a7796d2fa23bf89d389165cc346942c24008359(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b344f1763181d8852ed702ee38a4f8b6eea8176aa059c614d0f15c79bfb93ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a334b16050c5514e674652464dc0b092cb2b6e6bcbdeb9d453e60e8b0aaaedc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb68546299f4373f8390d647e6b783d93b4258d87f9288136f57a7a45c245a0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9493b82111ad39e8436b96d724678b43209cd62a641113cfb74280595fa5290(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ca3592a4e239bad279dfc031b3b1903100e0bcf68e63e947b1694589501867(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroup]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6db43efef1e1b0285545a4e043aebe5d559f5dcbe0881cd9e1059d017f05b92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb1c62f0ff02975a21ef54ea813d64474c71aa0b41f86698bd7e0d7b262f903(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8bc6c2577554052714902e60e27cbb5fdc0a30359fcd5edde1a6a67df2f83a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a53a28f44f14a4ee3ccf23abba226e5fbd0ae7eff777c6ca9da8c15393bbbad3(
    value: typing.Optional[typing.Union[ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroup, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b300f518196c9a299f7e624fdc72d6bff3cd931a7e89b9bb86c1ec8fbb24f50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71379ed071e6f73460cdfe2f005b131b2ea9066af94ad87a1047b90f411aba54(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0de009dbea5e8c23906a5e0d20fc49d2900e2fd8d3d35bccb4f7da798bd77988(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ef9cf98151345850f79d78832c522ab934b08cea5470810bae0e3f7e830aa5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f8db7188f11e25187fb72d0dfaafd02622e19799dcc73f51ceffbcd2a2f250(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf921ecec5596b0c838f5871eae2f7e00f96f5f1d2e7955a0cb381ac8208134(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastigroupAzureV3NetworkNetworkInterfaces]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c360ea491c0ed2616b14c409fd03abfae141a882d2f379347701ae8f4f876c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0311baec94a2c5bed16aa63d074801c231e846d3ce73c100b110091f0acc82(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3NetworkNetworkInterfacesAdditionalIpConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3674d5efc0563324862aed029173f7e58654de011b9a3741ebbc04b2eb14a1e6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3NetworkNetworkInterfacesApplicationSecurityGroup, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d68b53344d678a6906a12d5b6c66166415b62f0934b97aa91ecf9e42d33eb7c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16161fec59a4e9e1a1df69078e0d87731f49e5e45acc85eb17f47708fdd39b45(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf9bf0b8e3f28eae29ef52bfdb4acac52f6f064c982e118c238cbb4b44c0d98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe32d5d42799ac42ac0cdca668ac02d5af53af8d610a54578df1c5b92b02575(
    value: typing.Optional[typing.Union[ElastigroupAzureV3NetworkNetworkInterfaces, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60fa0ce4ad59907ad9343caba70f4323864a6ca66f53223eae29265e5a23abb8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da5cc9a5e0de23908a7d5607142470f724e26c3670f1b1706ac13a036ff14fe1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastigroupAzureV3NetworkNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b2c49aa895598ee323243c62b314534c44ab5e7b795f97e8342553bc4ed455(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c74a488ca47ae06f34ff31d020eaca8150a35ce413626b9d0c864198e313f35f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f704e47e954be4cf434ea9a09bf2f4de140868054034bf52cf79d3836c52f04(
    value: typing.Optional[ElastigroupAzureV3Network],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a897e4fc9edb678a4ffe7b9e411d52707749f7443b53df2eea8daf41113c6f75(
    *,
    draining_timeout: typing.Optional[jsii.Number] = None,
    fallback_to_on_demand: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    od_count: typing.Optional[jsii.Number] = None,
    spot_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186ef4435d0e90ceead66ccba1aa1d8128476d2950623c03f9a68c3e2916908a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa5754de73dc2191c76cb49e18d711d29d0270320be632149daa5b14cfb1bac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd9bfa1dd355c80568ed5f451e1201434903a610300e1128a95e0488b3257337(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c61f554738c530c45797b3b97035733fdd242938a61015a20a74b070563ee49(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0a9a90250dffa5c02824ff561f504bac408685e68785f8d79645bc7b446f80(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__353f94f214ceedc5645068d01cde335bc16a8d65dfe42ebee654cd0922d30eb5(
    value: typing.Optional[ElastigroupAzureV3Strategy],
) -> None:
    """Type checking stubs"""
    pass
