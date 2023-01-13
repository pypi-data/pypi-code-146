'''
# `azurerm_databox_edge_order`

Refer to the Terraform Registory for docs: [`azurerm_databox_edge_order`](https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order).
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


class DataboxEdgeOrder(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.databoxEdgeOrder.DataboxEdgeOrder",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order azurerm_databox_edge_order}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        contact: typing.Union["DataboxEdgeOrderContact", typing.Dict[builtins.str, typing.Any]],
        device_name: builtins.str,
        resource_group_name: builtins.str,
        shipment_address: typing.Union["DataboxEdgeOrderShipmentAddress", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataboxEdgeOrderTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order azurerm_databox_edge_order} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param contact: contact block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#contact DataboxEdgeOrder#contact}
        :param device_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#device_name DataboxEdgeOrder#device_name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#resource_group_name DataboxEdgeOrder#resource_group_name}.
        :param shipment_address: shipment_address block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#shipment_address DataboxEdgeOrder#shipment_address}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#id DataboxEdgeOrder#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#timeouts DataboxEdgeOrder#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c81f5018a593189e0f71a71166a0552c57709efa87b1df4de7c6cb30f35bec0e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataboxEdgeOrderConfig(
            contact=contact,
            device_name=device_name,
            resource_group_name=resource_group_name,
            shipment_address=shipment_address,
            id=id,
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

    @jsii.member(jsii_name="putContact")
    def put_contact(
        self,
        *,
        company_name: builtins.str,
        emails: typing.Sequence[builtins.str],
        name: builtins.str,
        phone_number: builtins.str,
    ) -> None:
        '''
        :param company_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#company_name DataboxEdgeOrder#company_name}.
        :param emails: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#emails DataboxEdgeOrder#emails}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#name DataboxEdgeOrder#name}.
        :param phone_number: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#phone_number DataboxEdgeOrder#phone_number}.
        '''
        value = DataboxEdgeOrderContact(
            company_name=company_name,
            emails=emails,
            name=name,
            phone_number=phone_number,
        )

        return typing.cast(None, jsii.invoke(self, "putContact", [value]))

    @jsii.member(jsii_name="putShipmentAddress")
    def put_shipment_address(
        self,
        *,
        address: typing.Sequence[builtins.str],
        city: builtins.str,
        country: builtins.str,
        postal_code: builtins.str,
        state: builtins.str,
    ) -> None:
        '''
        :param address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#address DataboxEdgeOrder#address}.
        :param city: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#city DataboxEdgeOrder#city}.
        :param country: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#country DataboxEdgeOrder#country}.
        :param postal_code: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#postal_code DataboxEdgeOrder#postal_code}.
        :param state: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#state DataboxEdgeOrder#state}.
        '''
        value = DataboxEdgeOrderShipmentAddress(
            address=address,
            city=city,
            country=country,
            postal_code=postal_code,
            state=state,
        )

        return typing.cast(None, jsii.invoke(self, "putShipmentAddress", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#create DataboxEdgeOrder#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#delete DataboxEdgeOrder#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#read DataboxEdgeOrder#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#update DataboxEdgeOrder#update}.
        '''
        value = DataboxEdgeOrderTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="contact")
    def contact(self) -> "DataboxEdgeOrderContactOutputReference":
        return typing.cast("DataboxEdgeOrderContactOutputReference", jsii.get(self, "contact"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="returnTracking")
    def return_tracking(self) -> "DataboxEdgeOrderReturnTrackingList":
        return typing.cast("DataboxEdgeOrderReturnTrackingList", jsii.get(self, "returnTracking"))

    @builtins.property
    @jsii.member(jsii_name="serialNumber")
    def serial_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serialNumber"))

    @builtins.property
    @jsii.member(jsii_name="shipmentAddress")
    def shipment_address(self) -> "DataboxEdgeOrderShipmentAddressOutputReference":
        return typing.cast("DataboxEdgeOrderShipmentAddressOutputReference", jsii.get(self, "shipmentAddress"))

    @builtins.property
    @jsii.member(jsii_name="shipmentHistory")
    def shipment_history(self) -> "DataboxEdgeOrderShipmentHistoryList":
        return typing.cast("DataboxEdgeOrderShipmentHistoryList", jsii.get(self, "shipmentHistory"))

    @builtins.property
    @jsii.member(jsii_name="shipmentTracking")
    def shipment_tracking(self) -> "DataboxEdgeOrderShipmentTrackingList":
        return typing.cast("DataboxEdgeOrderShipmentTrackingList", jsii.get(self, "shipmentTracking"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "DataboxEdgeOrderStatusList":
        return typing.cast("DataboxEdgeOrderStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataboxEdgeOrderTimeoutsOutputReference":
        return typing.cast("DataboxEdgeOrderTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="contactInput")
    def contact_input(self) -> typing.Optional["DataboxEdgeOrderContact"]:
        return typing.cast(typing.Optional["DataboxEdgeOrderContact"], jsii.get(self, "contactInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceNameInput")
    def device_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="shipmentAddressInput")
    def shipment_address_input(
        self,
    ) -> typing.Optional["DataboxEdgeOrderShipmentAddress"]:
        return typing.cast(typing.Optional["DataboxEdgeOrderShipmentAddress"], jsii.get(self, "shipmentAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["DataboxEdgeOrderTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["DataboxEdgeOrderTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceName")
    def device_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceName"))

    @device_name.setter
    def device_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e042c7a13d181f826025c875b673c535ce9dd34582e81aaebd2c320c91128d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__683fb02119551443ba1e9b8f070e15331744156f4115ee37ea849a91bc154ae9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__307c3845b4023857a35003668ad6591530cddcaab859488128858b515602b2bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.databoxEdgeOrder.DataboxEdgeOrderConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "contact": "contact",
        "device_name": "deviceName",
        "resource_group_name": "resourceGroupName",
        "shipment_address": "shipmentAddress",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class DataboxEdgeOrderConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        contact: typing.Union["DataboxEdgeOrderContact", typing.Dict[builtins.str, typing.Any]],
        device_name: builtins.str,
        resource_group_name: builtins.str,
        shipment_address: typing.Union["DataboxEdgeOrderShipmentAddress", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataboxEdgeOrderTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param contact: contact block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#contact DataboxEdgeOrder#contact}
        :param device_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#device_name DataboxEdgeOrder#device_name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#resource_group_name DataboxEdgeOrder#resource_group_name}.
        :param shipment_address: shipment_address block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#shipment_address DataboxEdgeOrder#shipment_address}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#id DataboxEdgeOrder#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#timeouts DataboxEdgeOrder#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(contact, dict):
            contact = DataboxEdgeOrderContact(**contact)
        if isinstance(shipment_address, dict):
            shipment_address = DataboxEdgeOrderShipmentAddress(**shipment_address)
        if isinstance(timeouts, dict):
            timeouts = DataboxEdgeOrderTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8e6e9f6e20d91186e7c2a3fca3f76c3a686d31d8895366a78cb496faa20dfc2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument contact", value=contact, expected_type=type_hints["contact"])
            check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument shipment_address", value=shipment_address, expected_type=type_hints["shipment_address"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "contact": contact,
            "device_name": device_name,
            "resource_group_name": resource_group_name,
            "shipment_address": shipment_address,
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
        if id is not None:
            self._values["id"] = id
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
    def contact(self) -> "DataboxEdgeOrderContact":
        '''contact block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#contact DataboxEdgeOrder#contact}
        '''
        result = self._values.get("contact")
        assert result is not None, "Required property 'contact' is missing"
        return typing.cast("DataboxEdgeOrderContact", result)

    @builtins.property
    def device_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#device_name DataboxEdgeOrder#device_name}.'''
        result = self._values.get("device_name")
        assert result is not None, "Required property 'device_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#resource_group_name DataboxEdgeOrder#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def shipment_address(self) -> "DataboxEdgeOrderShipmentAddress":
        '''shipment_address block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#shipment_address DataboxEdgeOrder#shipment_address}
        '''
        result = self._values.get("shipment_address")
        assert result is not None, "Required property 'shipment_address' is missing"
        return typing.cast("DataboxEdgeOrderShipmentAddress", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#id DataboxEdgeOrder#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataboxEdgeOrderTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#timeouts DataboxEdgeOrder#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataboxEdgeOrderTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataboxEdgeOrderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.databoxEdgeOrder.DataboxEdgeOrderContact",
    jsii_struct_bases=[],
    name_mapping={
        "company_name": "companyName",
        "emails": "emails",
        "name": "name",
        "phone_number": "phoneNumber",
    },
)
class DataboxEdgeOrderContact:
    def __init__(
        self,
        *,
        company_name: builtins.str,
        emails: typing.Sequence[builtins.str],
        name: builtins.str,
        phone_number: builtins.str,
    ) -> None:
        '''
        :param company_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#company_name DataboxEdgeOrder#company_name}.
        :param emails: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#emails DataboxEdgeOrder#emails}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#name DataboxEdgeOrder#name}.
        :param phone_number: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#phone_number DataboxEdgeOrder#phone_number}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91b7f60b25f40bd7b2e7f633fd93302251fa20aa4cf7c01d0ad18f0407365d3e)
            check_type(argname="argument company_name", value=company_name, expected_type=type_hints["company_name"])
            check_type(argname="argument emails", value=emails, expected_type=type_hints["emails"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "company_name": company_name,
            "emails": emails,
            "name": name,
            "phone_number": phone_number,
        }

    @builtins.property
    def company_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#company_name DataboxEdgeOrder#company_name}.'''
        result = self._values.get("company_name")
        assert result is not None, "Required property 'company_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def emails(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#emails DataboxEdgeOrder#emails}.'''
        result = self._values.get("emails")
        assert result is not None, "Required property 'emails' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#name DataboxEdgeOrder#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def phone_number(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#phone_number DataboxEdgeOrder#phone_number}.'''
        result = self._values.get("phone_number")
        assert result is not None, "Required property 'phone_number' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataboxEdgeOrderContact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataboxEdgeOrderContactOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.databoxEdgeOrder.DataboxEdgeOrderContactOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__761b2b28fa7de44f46ec31a9bec68a7f4080a0f6325cf19fd806b9726d903c6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="companyNameInput")
    def company_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "companyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="emailsInput")
    def emails_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="companyName")
    def company_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "companyName"))

    @company_name.setter
    def company_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__311405b79bb8db5e67a568d04dbf1e45d423e53e82f4e8a9165810902a393e5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "companyName", value)

    @builtins.property
    @jsii.member(jsii_name="emails")
    def emails(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emails"))

    @emails.setter
    def emails(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1a17e974bf7b58fe5d3c744ba7e90c7f239a33268c0a6a42898b64e16a8b962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emails", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__730ab850aad711a30b64ef6058c861e02e1bde8b85a2a471db741547f1faa1bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__184349800ab835ec7d75d7f3177bf8c2c8f0d528592efe5ec43181dadecc9c56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataboxEdgeOrderContact]:
        return typing.cast(typing.Optional[DataboxEdgeOrderContact], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataboxEdgeOrderContact]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf3af821ebec4eca8b10a04a337ba8c7ef6f6e458c4e00c1729d977f7709c570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.databoxEdgeOrder.DataboxEdgeOrderReturnTracking",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataboxEdgeOrderReturnTracking:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataboxEdgeOrderReturnTracking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataboxEdgeOrderReturnTrackingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.databoxEdgeOrder.DataboxEdgeOrderReturnTrackingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d3886ba6c0c44f06b36da2ea760018b47b4cd091d114fccc09d0605f7bda0da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataboxEdgeOrderReturnTrackingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c72342ac683dd2d1d8b74ee9cece00ef647b6955c3208987e695691ee3ce49b2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataboxEdgeOrderReturnTrackingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc1a495a291ee323e40ab30858c5a3987aa600d6d6399c6a88b1116b1a0c4e02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c156aeb93af03eb2879cc9dec14aeb2bfbf470eb2d023be7cd826bfb27731517)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9b069c614c0e06bb64728b99470329814cb7d23be68f3423ef876236b7e3719)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataboxEdgeOrderReturnTrackingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.databoxEdgeOrder.DataboxEdgeOrderReturnTrackingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a720c1f41ee19cf9dcbc045b9f58531af8746d4c41a6a2284e730f4fdbcb3903)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="carrierName")
    def carrier_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "carrierName"))

    @builtins.property
    @jsii.member(jsii_name="serialNumber")
    def serial_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serialNumber"))

    @builtins.property
    @jsii.member(jsii_name="trackingId")
    def tracking_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trackingId"))

    @builtins.property
    @jsii.member(jsii_name="trackingUrl")
    def tracking_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trackingUrl"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataboxEdgeOrderReturnTracking]:
        return typing.cast(typing.Optional[DataboxEdgeOrderReturnTracking], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataboxEdgeOrderReturnTracking],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de6ce4680910f055d938a2a4a3ee6e5f8a963497653c9d0d606526cb58e3336e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.databoxEdgeOrder.DataboxEdgeOrderShipmentAddress",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "city": "city",
        "country": "country",
        "postal_code": "postalCode",
        "state": "state",
    },
)
class DataboxEdgeOrderShipmentAddress:
    def __init__(
        self,
        *,
        address: typing.Sequence[builtins.str],
        city: builtins.str,
        country: builtins.str,
        postal_code: builtins.str,
        state: builtins.str,
    ) -> None:
        '''
        :param address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#address DataboxEdgeOrder#address}.
        :param city: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#city DataboxEdgeOrder#city}.
        :param country: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#country DataboxEdgeOrder#country}.
        :param postal_code: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#postal_code DataboxEdgeOrder#postal_code}.
        :param state: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#state DataboxEdgeOrder#state}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7821851ddc87b6c84aadee92d434bbde063897c3a81d3a915b042f868ef0953b)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument city", value=city, expected_type=type_hints["city"])
            check_type(argname="argument country", value=country, expected_type=type_hints["country"])
            check_type(argname="argument postal_code", value=postal_code, expected_type=type_hints["postal_code"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address": address,
            "city": city,
            "country": country,
            "postal_code": postal_code,
            "state": state,
        }

    @builtins.property
    def address(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#address DataboxEdgeOrder#address}.'''
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def city(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#city DataboxEdgeOrder#city}.'''
        result = self._values.get("city")
        assert result is not None, "Required property 'city' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def country(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#country DataboxEdgeOrder#country}.'''
        result = self._values.get("country")
        assert result is not None, "Required property 'country' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postal_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#postal_code DataboxEdgeOrder#postal_code}.'''
        result = self._values.get("postal_code")
        assert result is not None, "Required property 'postal_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#state DataboxEdgeOrder#state}.'''
        result = self._values.get("state")
        assert result is not None, "Required property 'state' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataboxEdgeOrderShipmentAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataboxEdgeOrderShipmentAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.databoxEdgeOrder.DataboxEdgeOrderShipmentAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cecfb7e04a915785098786b03779863796525136c84a80189798fb1553225b46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="cityInput")
    def city_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cityInput"))

    @builtins.property
    @jsii.member(jsii_name="countryInput")
    def country_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryInput"))

    @builtins.property
    @jsii.member(jsii_name="postalCodeInput")
    def postal_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postalCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "address"))

    @address.setter
    def address(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a36c8029b8f6338c7ff1bfb4099fe400ee3d6ea5a251a6b166129774425744b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value)

    @builtins.property
    @jsii.member(jsii_name="city")
    def city(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "city"))

    @city.setter
    def city(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2dca2a053333c686b97e3a168b9221597a574d84db58060bf1a3663abc0d485)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "city", value)

    @builtins.property
    @jsii.member(jsii_name="country")
    def country(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "country"))

    @country.setter
    def country(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aedb3d0b9fd58d3cba0214212ae965e7d8b9fbce0c28cf59dc141652f15be996)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "country", value)

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @postal_code.setter
    def postal_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a0a7b2a5d9b66d63f50e4da02a6ffed9014f060a932f9abb7078f21f7eb3f0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postalCode", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86ec5a73d9cf50569e1ee39c0aef62707198e27f61bcc9ec07a310f7d1f6c63c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataboxEdgeOrderShipmentAddress]:
        return typing.cast(typing.Optional[DataboxEdgeOrderShipmentAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataboxEdgeOrderShipmentAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de0b7a7e8a86ae43202447a96a3fc81548c0b47561a8e7e48301d49bf2cfd1b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.databoxEdgeOrder.DataboxEdgeOrderShipmentHistory",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataboxEdgeOrderShipmentHistory:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataboxEdgeOrderShipmentHistory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataboxEdgeOrderShipmentHistoryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.databoxEdgeOrder.DataboxEdgeOrderShipmentHistoryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88fe3fd9872ff297463809b1f87219c200ba7398591234fafeb4f28b43890208)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataboxEdgeOrderShipmentHistoryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb69b92ae67baf11871eb4a04a08aaf210a8734a553c60e5a00ccfe6005a008f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataboxEdgeOrderShipmentHistoryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d0cfec506421b97c6f765f234e98b0a6f7ef5b1a0902dd023290dc524f3f884)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcc097c97eb4c5a00e4949e7f93d0bb9c0c7214f5de24bc79d1165516cd1a1c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__030d1acf562b05828e775c4ddf24e27297215320fa34a3c57f380e6862e718c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataboxEdgeOrderShipmentHistoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.databoxEdgeOrder.DataboxEdgeOrderShipmentHistoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3e4d8a9e7d7da6391a15a39d1e646b397536ede34767bd5b1e0426257aa4607)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="additionalDetails")
    def additional_details(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "additionalDetails"))

    @builtins.property
    @jsii.member(jsii_name="comments")
    def comments(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comments"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdate")
    def last_update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdate"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataboxEdgeOrderShipmentHistory]:
        return typing.cast(typing.Optional[DataboxEdgeOrderShipmentHistory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataboxEdgeOrderShipmentHistory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb184c5a4b4a19d583af9323c869324aa8d5848b84b2b86f3de2c62ba2cc4434)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.databoxEdgeOrder.DataboxEdgeOrderShipmentTracking",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataboxEdgeOrderShipmentTracking:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataboxEdgeOrderShipmentTracking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataboxEdgeOrderShipmentTrackingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.databoxEdgeOrder.DataboxEdgeOrderShipmentTrackingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bf112bc212e9fbb44840bbb350de0a1ed7c70598f7ba25d76d1e3278fcc8e95)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataboxEdgeOrderShipmentTrackingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b99c3143473b37a5bc44b1c8dc7907ebd820d65ef5be5e147d39b2851d658f9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataboxEdgeOrderShipmentTrackingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa4f76d123d83f0509cadc9a26d33bc45bef2e2f68bb8e8305349d4a55faefe6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fff7562b7797a3b9df9991aa21f8d63442d4cadfe8946036cad60540117d74af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ee94c78e5e58f48d805a5662ce9fbc71e64a6a77ace4f85755d0d545b2b15fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataboxEdgeOrderShipmentTrackingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.databoxEdgeOrder.DataboxEdgeOrderShipmentTrackingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6f2ca5cda5b6102c35cb47bb516ca36a1958bacf4338772d79cb154efc931a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="carrierName")
    def carrier_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "carrierName"))

    @builtins.property
    @jsii.member(jsii_name="serialNumber")
    def serial_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serialNumber"))

    @builtins.property
    @jsii.member(jsii_name="trackingId")
    def tracking_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trackingId"))

    @builtins.property
    @jsii.member(jsii_name="trackingUrl")
    def tracking_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trackingUrl"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataboxEdgeOrderShipmentTracking]:
        return typing.cast(typing.Optional[DataboxEdgeOrderShipmentTracking], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataboxEdgeOrderShipmentTracking],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__305c490032b7461e8f6756ab6e157df16ad16ca19b53d0054a5aac4d3ba7ad0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.databoxEdgeOrder.DataboxEdgeOrderStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataboxEdgeOrderStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataboxEdgeOrderStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataboxEdgeOrderStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.databoxEdgeOrder.DataboxEdgeOrderStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52fe1feaff748e2fd8cffad3cf7a3dcfe5b17d09fbc236e3cc9b36292db5e2b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataboxEdgeOrderStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4692b8b43f3e12684d6ff1fad184edf1428cfbc322e4baf889df5c98a119c7bc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataboxEdgeOrderStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2f32c8e43d8eb1c341f56f6fd49ffe80c58e16d7a4d7a1b0ae39da322381320)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc3e46e685876d33099a53c2228eab21e37d12a8cdfd77ae2cfd7363f2f0b2cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__931541cf34afe0c22b0d99d2ff8874c8e61a88aec145943ad6a1c834b634fe02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataboxEdgeOrderStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.databoxEdgeOrder.DataboxEdgeOrderStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b6380963de3179d3d89d67b37fde9c6fdc41413c4a1eee7b0aed0c6a312cbb4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="additionalDetails")
    def additional_details(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "additionalDetails"))

    @builtins.property
    @jsii.member(jsii_name="comments")
    def comments(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comments"))

    @builtins.property
    @jsii.member(jsii_name="info")
    def info(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "info"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdate")
    def last_update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdate"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataboxEdgeOrderStatus]:
        return typing.cast(typing.Optional[DataboxEdgeOrderStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataboxEdgeOrderStatus]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eabedb8e24bf91a8f454ed1292f34da1887271886926c456cee8934e39f82a25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.databoxEdgeOrder.DataboxEdgeOrderTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class DataboxEdgeOrderTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#create DataboxEdgeOrder#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#delete DataboxEdgeOrder#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#read DataboxEdgeOrder#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#update DataboxEdgeOrder#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13b94a55fad0550de13485776e7c6639d8d8edb7760c7c413dc8373de907ba4e)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#create DataboxEdgeOrder#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#delete DataboxEdgeOrder#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#read DataboxEdgeOrder#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databox_edge_order#update DataboxEdgeOrder#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataboxEdgeOrderTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataboxEdgeOrderTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.databoxEdgeOrder.DataboxEdgeOrderTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__054e0130b88a59951c3910ad417bbd90e634ead61f98c716765f76f5c71fda3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ddef9c4b62c0cd9b16a2cba00b3ad7774d307b1ecbabf6de7aa7bed75989211b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bbcd45698ba680740a9fbd5e28036f0adcd01088efd0bd23b0909fd7127d051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a69d32a554fd409a51badfe61ec6becef1b7a6bb46de681330ada5142e0282ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4465ea2b15fa464dfc0b7fa8f4732eec34179ed4c4b009eb136adea78cfd4eaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataboxEdgeOrderTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataboxEdgeOrderTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataboxEdgeOrderTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f0a351900081baa144cac7d8aa513a9df73d502b8e496145d37e1e3bdeb1227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataboxEdgeOrder",
    "DataboxEdgeOrderConfig",
    "DataboxEdgeOrderContact",
    "DataboxEdgeOrderContactOutputReference",
    "DataboxEdgeOrderReturnTracking",
    "DataboxEdgeOrderReturnTrackingList",
    "DataboxEdgeOrderReturnTrackingOutputReference",
    "DataboxEdgeOrderShipmentAddress",
    "DataboxEdgeOrderShipmentAddressOutputReference",
    "DataboxEdgeOrderShipmentHistory",
    "DataboxEdgeOrderShipmentHistoryList",
    "DataboxEdgeOrderShipmentHistoryOutputReference",
    "DataboxEdgeOrderShipmentTracking",
    "DataboxEdgeOrderShipmentTrackingList",
    "DataboxEdgeOrderShipmentTrackingOutputReference",
    "DataboxEdgeOrderStatus",
    "DataboxEdgeOrderStatusList",
    "DataboxEdgeOrderStatusOutputReference",
    "DataboxEdgeOrderTimeouts",
    "DataboxEdgeOrderTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c81f5018a593189e0f71a71166a0552c57709efa87b1df4de7c6cb30f35bec0e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    contact: typing.Union[DataboxEdgeOrderContact, typing.Dict[builtins.str, typing.Any]],
    device_name: builtins.str,
    resource_group_name: builtins.str,
    shipment_address: typing.Union[DataboxEdgeOrderShipmentAddress, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataboxEdgeOrderTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__24e042c7a13d181f826025c875b673c535ce9dd34582e81aaebd2c320c91128d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__683fb02119551443ba1e9b8f070e15331744156f4115ee37ea849a91bc154ae9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__307c3845b4023857a35003668ad6591530cddcaab859488128858b515602b2bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e6e9f6e20d91186e7c2a3fca3f76c3a686d31d8895366a78cb496faa20dfc2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    contact: typing.Union[DataboxEdgeOrderContact, typing.Dict[builtins.str, typing.Any]],
    device_name: builtins.str,
    resource_group_name: builtins.str,
    shipment_address: typing.Union[DataboxEdgeOrderShipmentAddress, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataboxEdgeOrderTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91b7f60b25f40bd7b2e7f633fd93302251fa20aa4cf7c01d0ad18f0407365d3e(
    *,
    company_name: builtins.str,
    emails: typing.Sequence[builtins.str],
    name: builtins.str,
    phone_number: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761b2b28fa7de44f46ec31a9bec68a7f4080a0f6325cf19fd806b9726d903c6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311405b79bb8db5e67a568d04dbf1e45d423e53e82f4e8a9165810902a393e5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a17e974bf7b58fe5d3c744ba7e90c7f239a33268c0a6a42898b64e16a8b962(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__730ab850aad711a30b64ef6058c861e02e1bde8b85a2a471db741547f1faa1bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__184349800ab835ec7d75d7f3177bf8c2c8f0d528592efe5ec43181dadecc9c56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3af821ebec4eca8b10a04a337ba8c7ef6f6e458c4e00c1729d977f7709c570(
    value: typing.Optional[DataboxEdgeOrderContact],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d3886ba6c0c44f06b36da2ea760018b47b4cd091d114fccc09d0605f7bda0da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72342ac683dd2d1d8b74ee9cece00ef647b6955c3208987e695691ee3ce49b2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1a495a291ee323e40ab30858c5a3987aa600d6d6399c6a88b1116b1a0c4e02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c156aeb93af03eb2879cc9dec14aeb2bfbf470eb2d023be7cd826bfb27731517(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b069c614c0e06bb64728b99470329814cb7d23be68f3423ef876236b7e3719(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a720c1f41ee19cf9dcbc045b9f58531af8746d4c41a6a2284e730f4fdbcb3903(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de6ce4680910f055d938a2a4a3ee6e5f8a963497653c9d0d606526cb58e3336e(
    value: typing.Optional[DataboxEdgeOrderReturnTracking],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7821851ddc87b6c84aadee92d434bbde063897c3a81d3a915b042f868ef0953b(
    *,
    address: typing.Sequence[builtins.str],
    city: builtins.str,
    country: builtins.str,
    postal_code: builtins.str,
    state: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cecfb7e04a915785098786b03779863796525136c84a80189798fb1553225b46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a36c8029b8f6338c7ff1bfb4099fe400ee3d6ea5a251a6b166129774425744b7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2dca2a053333c686b97e3a168b9221597a574d84db58060bf1a3663abc0d485(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aedb3d0b9fd58d3cba0214212ae965e7d8b9fbce0c28cf59dc141652f15be996(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a0a7b2a5d9b66d63f50e4da02a6ffed9014f060a932f9abb7078f21f7eb3f0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ec5a73d9cf50569e1ee39c0aef62707198e27f61bcc9ec07a310f7d1f6c63c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de0b7a7e8a86ae43202447a96a3fc81548c0b47561a8e7e48301d49bf2cfd1b6(
    value: typing.Optional[DataboxEdgeOrderShipmentAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88fe3fd9872ff297463809b1f87219c200ba7398591234fafeb4f28b43890208(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb69b92ae67baf11871eb4a04a08aaf210a8734a553c60e5a00ccfe6005a008f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d0cfec506421b97c6f765f234e98b0a6f7ef5b1a0902dd023290dc524f3f884(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc097c97eb4c5a00e4949e7f93d0bb9c0c7214f5de24bc79d1165516cd1a1c6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030d1acf562b05828e775c4ddf24e27297215320fa34a3c57f380e6862e718c8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e4d8a9e7d7da6391a15a39d1e646b397536ede34767bd5b1e0426257aa4607(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb184c5a4b4a19d583af9323c869324aa8d5848b84b2b86f3de2c62ba2cc4434(
    value: typing.Optional[DataboxEdgeOrderShipmentHistory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf112bc212e9fbb44840bbb350de0a1ed7c70598f7ba25d76d1e3278fcc8e95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b99c3143473b37a5bc44b1c8dc7907ebd820d65ef5be5e147d39b2851d658f9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa4f76d123d83f0509cadc9a26d33bc45bef2e2f68bb8e8305349d4a55faefe6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff7562b7797a3b9df9991aa21f8d63442d4cadfe8946036cad60540117d74af(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee94c78e5e58f48d805a5662ce9fbc71e64a6a77ace4f85755d0d545b2b15fc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6f2ca5cda5b6102c35cb47bb516ca36a1958bacf4338772d79cb154efc931a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__305c490032b7461e8f6756ab6e157df16ad16ca19b53d0054a5aac4d3ba7ad0c(
    value: typing.Optional[DataboxEdgeOrderShipmentTracking],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52fe1feaff748e2fd8cffad3cf7a3dcfe5b17d09fbc236e3cc9b36292db5e2b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4692b8b43f3e12684d6ff1fad184edf1428cfbc322e4baf889df5c98a119c7bc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2f32c8e43d8eb1c341f56f6fd49ffe80c58e16d7a4d7a1b0ae39da322381320(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3e46e685876d33099a53c2228eab21e37d12a8cdfd77ae2cfd7363f2f0b2cf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931541cf34afe0c22b0d99d2ff8874c8e61a88aec145943ad6a1c834b634fe02(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b6380963de3179d3d89d67b37fde9c6fdc41413c4a1eee7b0aed0c6a312cbb4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eabedb8e24bf91a8f454ed1292f34da1887271886926c456cee8934e39f82a25(
    value: typing.Optional[DataboxEdgeOrderStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13b94a55fad0550de13485776e7c6639d8d8edb7760c7c413dc8373de907ba4e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__054e0130b88a59951c3910ad417bbd90e634ead61f98c716765f76f5c71fda3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddef9c4b62c0cd9b16a2cba00b3ad7774d307b1ecbabf6de7aa7bed75989211b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bbcd45698ba680740a9fbd5e28036f0adcd01088efd0bd23b0909fd7127d051(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a69d32a554fd409a51badfe61ec6becef1b7a6bb46de681330ada5142e0282ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4465ea2b15fa464dfc0b7fa8f4732eec34179ed4c4b009eb136adea78cfd4eaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f0a351900081baa144cac7d8aa513a9df73d502b8e496145d37e1e3bdeb1227(
    value: typing.Optional[typing.Union[DataboxEdgeOrderTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
