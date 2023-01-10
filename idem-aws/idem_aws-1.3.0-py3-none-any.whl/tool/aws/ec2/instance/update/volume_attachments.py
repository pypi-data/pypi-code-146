from typing import Dict
from typing import List


async def apply(
    hub,
    ctx,
    resource,
    *,
    old_value: Dict[str, str],
    new_value: Dict[str, str],
    comments: List[str],
) -> bool:
    """
    Modify an ec2 instance based on a single parameter in it's "present" state

      - volume_attachments:
          /dev/xvda: vol-0f0c6dac5d13b9dc4

    Args:
        hub:
        ctx: The ctx from a state module call
        resource: An ec2 instance resource object
        old_value: The previous value from the attributes of an existing instance
        new_value: The desired value from the ec2 instance present state parameters
        comments: A running list of comments abound the update process
    """
    # Attach new volumes
    # If a device name is in the new mappings, but not the old, its a new volume to attach
    volumes_to_attach = set(new_value.keys()) - set(old_value.keys())
    for device_name in volumes_to_attach:
        volume_id = new_value[device_name]
        ret = await hub.boto3.client.ec2.attach_volume(
            ctx, Device=device_name, InstanceId=resource.id, VolumeId=volume_id
        )
        if ret.comment:
            comments.append(ret.comment)
        if not ret.result:
            comments.append(f"Could not attach volume: {volume_id} to instance")
            return False

    # Remove old volumes
    # If a device name is in the old mappings, but not the new, it's a volume to detach
    volumes_to_remove = set(old_value.keys()) - set(new_value.keys())
    for device_name in volumes_to_remove:
        volume_id = old_value[device_name]
        ret = await hub.boto3.client.ec2.detach_volume(
            ctx, Device=device_name, InstanceId=resource.id, VolumeId=volume_id
        )
        if ret.comment:
            comments.append(ret.comment)
        if not ret.result:
            comments.append(f"Could not detach volume: {volume_id} from instance")
            return False

    # If a volume exists in both places then check if the volume id has changed
    volumes_to_move = set(old_value.keys()).intersection(set(new_value.keys()))
    for device_name in volumes_to_move:
        if old_value[device_name] != new_value[device_name]:
            # Detach the old volume
            volume_id = old_value[device_name]
            ret = await hub.boto3.client.ec2.detach_volume(
                ctx, Device=device_name, InstanceId=resource.id, VolumeId=volume_id
            )
            if ret.comment:
                comments.append(ret.comment)
            if not ret.result:
                comments.append(f"Could not detach volume: {volume_id} from instance")
                return False

            # Attach the new volume
            volume_id = new_value[device_name]
            ret = await hub.boto3.client.ec2.attach_volume(
                ctx, Device=device_name, InstanceId=resource.id, VolumeId=volume_id
            )
            if ret.comment:
                comments.append(ret.comment)
            if not ret.result:
                comments.append(f"Could not attach volume: {volume_id} to instance")
                return False

    return True
