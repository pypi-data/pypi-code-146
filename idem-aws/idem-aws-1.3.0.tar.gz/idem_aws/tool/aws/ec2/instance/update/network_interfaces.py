from typing import Any
from typing import Dict
from typing import List


async def apply(
    hub,
    ctx,
    resource,
    *,
    old_value: List[Dict[str, Any]],
    new_value: List[Dict[str, Any]],
    comments: List[str],
) -> bool:
    """
    Modify an ec2 instance based on a single parameter in its "present" state

    - network_interfaces:
        - AssociatePublicIpAddress: true
          DeleteOnTermination: true
          Description: ''
          DeviceIndex: 0
          Groups:
          - sg-XXXXXXXX
          InterfaceType: interface
          Ipv6Addresses: []
          NetworkCardIndex: 0
          PrivateIpAddresses:
          - Primary: true
            PrivateIpAddress: 888.88.88.888
          SubnetId: subnet-XXXXXXXX

    Args:
        hub:
        ctx: The ctx from a state module call
        resource: An ec2 instance resource object
        old_value: The previous value from the attributes of an existing instance
        new_value: The desired value from the ec2 instance present state parameters
        comments: A running list of comments abound the update process
    """
    comments.append(f"Unable to modify network interfaces at this time")
    return True
    result = True
    new_interfaces = {interface["DeviceIndex"]: interface for interface in new_value}
    old_interfaces = {interface["DeviceIndex"]: interface for interface in old_value}

    # create new interfaces
    interfaces_to_create = set(new_interfaces.keys()) - set(old_interfaces.keys())
    for device_index in interfaces_to_create:
        result &= await hub.tool.aws.ec2.instance.update.network_interfaces.create(
            ctx,
            resource,
            comments,
            device_index=device_index,
            new_interfaces=new_interfaces,
        )

    # Delete interfaces that were removed from the state
    interfaces_to_delete = set(old_interfaces.keys()) - set(new_interfaces.keys())
    for device_index in interfaces_to_delete:
        result &= await hub.tool.aws.ec2.instance.update.network_interfaces.delete(
            ctx,
            resource,
            comments,
            device_index=device_index,
            old_interfaces=old_interfaces,
        )

    # Modify existing network interfaces as needed
    interfaces_to_modify = set(old_interfaces.keys()).intersection(
        new_interfaces.keys()
    )
    for device_index in interfaces_to_modify:
        result &= await hub.tool.aws.ec2.instance.update.network_interfaces.modify(
            ctx,
            resource,
            comments,
            device_index=device_index,
            old_value=old_value,
            new_value=new_value,
        )

    return result


async def create(
    hub,
    ctx,
    resource,
    comments: List[str],
    device_index: int,
    old_interfaces: List[Dict[str, Any]],
) -> bool:
    attributes = old_interfaces[device_index]

    # Create the new interface
    ret = await hub.exec.boto3.client.ec2.create_network_interface(
        ctx,
        Description=attributes.get("Description"),
        DeviceIndex=device_index,
        Groups=attributes.get("Groups"),
        InterfaceType=attributes.get("InterfaceType"),
        Ipv6Addresses=attributes.get("Ipv6Addresses"),
        PrivateIpAddresses=attributes.get("PrivateIpAddresses"),
        # Use the subnet defined in the network interface, but fallback to the one used by the instance
        SubnetId=attributes.get("SubnetId", resource.subnet_id),
    )
    if ret.comment:
        comments.append(ret.comment)
    if not ret.result:
        return False

    # Attach the new interface to the instance
    interface_id = ret.ret["NetworkInterface"]["NetworkInterfaceId"]
    ret = await hub.exec.boto3.client.ec2.attach_network_interface(
        ctx,
        DeviceIndex=device_index,
        InstanceId=resource.id,
        NetworkInterfaceId=interface_id,
        NetworkCardIndex=attributes.get("NetworkCardIndex"),
    )
    if ret.comment:
        comments.append(ret.comment)
    if not ret.result:
        return False


async def delete(
    hub,
    ctx,
    resource,
    comments: List[str],
    device_index: int,
    new_interfaces: List[Dict[str, Any]],
) -> bool:
    ret = await hub.exec.boto3.client.ec2.describe_network_interfaces(
        ctx,
        Filters=[
            {"Name": "attachment.instance-id", "Values": [resource.id]},
            {"Name": "attachment.device-index", "Values": [device_index]},
        ],
    )

    if not ret:
        comments.append(f"Interface is already absent from index: {device_index}")
        return True

    # There will only be one result
    attachment_id = next(iter(ret.ret["NetworkInterfaces"]))["Attachment"][
        "AttachmentId"
    ]

    ret = await hub.exec.boto3.client.ec2.detach_network_interface(
        ctx, AttachmentId=attachment_id, Force=False
    )
    if ret.comment:
        comments.append(ret.comment)
    if not ret:
        return False


async def modify(
    hub,
    ctx,
    resource,
    comments: List[str],
    device_index: int,
    old_value: List[Dict[str, Any]],
    new_value: List[Dict[str, Any]],
) -> bool:
    if old_value[device_index] == new_value[device_index]:
        return True

    ret = await hub.exec.boto3.client.ec2.describe_network_interfaces(
        ctx,
        Filters=[
            {"Name": "attachment.instance-id", "Values": [resource.id]},
            {"Name": "attachment.device-index", "Values": [str(device_index)]},
        ],
    )
    if ret.comment:
        comments.append(ret.comment)
    if not ret.result:
        return False

    # There will only be one result
    interface = next(iter(ret.ret["NetworkInterfaces"]))

    # Check for changes to groups
    if old_value[device_index].get("Groups") != new_value[device_index].get("Groups"):
        ret = await hub.exec.boto3.client.ec2.modify_network_interface_attribute(
            ctx,
            NetworkInterfaceId=interface["NetworkInterfaceId"],
            Groups=new_value[device_index].get("Groups", []),
        )
        if ret.comment:
            comments.append(ret.comment)
        if not ret.result:
            return False

    # Check for changes to description
    if old_value[device_index].get("Description") != new_value[device_index].get(
        "Description"
    ):
        ret = await hub.exec.boto3.client.ec2.modify_network_interface_attribute(
            ctx,
            NetworkInterfaceId=interface["NetworkInterfaceId"],
            Description=new_value[device_index].get("Description", ""),
        )
        if ret.comment:
            comments.append(ret.comment)
        if not ret.result:
            return False

    # Check for changes to Delete On Termination
    if old_value[device_index].get("DeleteOnTermination") != new_value[
        device_index
    ].get("DeleteOnTermination"):
        ret = await hub.exec.boto3.client.ec2.modify_network_interface_attribute(
            ctx,
            NetworkInterfaceId=interface["NetworkInterfaceId"],
            Attachment=dict(
                AttachmentId=interface["Attachment"]["AttachmentId"],
                DeleteOnTermination=new_value[device_index].get("DeleteOnTermination"),
            ),
        )
        if ret.comment:
            comments.append(ret.comment)
        if not ret.result:
            return False
