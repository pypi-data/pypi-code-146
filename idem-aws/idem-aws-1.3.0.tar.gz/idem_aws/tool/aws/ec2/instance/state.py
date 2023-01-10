"""
Contains functions that are useful for describing instances in a consistent manner
"""
import asyncio
import base64
from typing import Any
from typing import Dict
from typing import Tuple


async def convert_to_present(
    hub, ctx, describe_instances: Dict[str, Any], name: str = None
) -> Dict[str, Any]:
    """
    Convert instances from ec2.describe_instances() to aws.ec2.instance.present states

    This is the preferred "meta" function for collecting information about multiple instances
    """
    result = {}
    coros = []
    for reservation in describe_instances.get("Reservations", []):
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            placement = instance.get("Placement", {})
            metadata_options = instance.get("MetadataOptions", {})
            private_dns_name_options = instance.get("PrivateDnsNameOptions", {})
            result[instance_id] = dict(
                name=name or instance_id,
                resource_id=instance_id,
                image_id=instance.get("ImageId"),
                instance_type=instance.get("InstanceType"),
                volume_attachments=None,
                block_device_mappings=instance.get("BlockDeviceMappings"),
                ebs_optimized=instance.get("EbsOptimized"),
                kernel_id=instance.get("KernelId"),
                subnet_id=instance.get("SubnetId"),
                network_interfaces=instance.get("NetworkInterfaces"),
                monitoring_enabled=instance.get("Monitoring", {}).get("State")
                == "enabled",
                root_device_name=instance.get("RootDeviceName"),
                client_token=instance.get("ClientToken"),
                product_codes=instance.get("ProductCodes"),
                source_dest_check=instance.get("SourceDestCheck"),
                running=instance.get("State", {}).get("Name") == "running",
                private_ip_address=instance.get("PrivateIpAddress"),
                reservation_id=reservation.get("ReservationId"),
                owner_id=reservation.get("OwnerId"),
                availability_zone=placement.get("AvailabilityZone"),
                affinity=placement.get("Affinity"),
                group_name=placement.get("GroupName"),
                partition_number=placement.get("PartitionNumber"),
                host_id=placement.get("HostId"),
                tenancy=placement.get("Tenancy"),
                spread_domain=placement.get("SpreadDomain"),
                host_resource_group_arn=placement.get("HostResourceGroupArn"),
                user_data=None,
                disable_api_termination=None,
                ram_disk_id=instance.get("RamdiskId"),
                tags={tag["Key"]: tag["Value"] for tag in instance.get("Tags", [])},
                iam_instance_profile_arn=instance.get("IamInstanceProfile", {}).get(
                    "Arn"
                ),
                instance_initiated_shutdown_behavior=None,
                elastic_inference_accelerators=instance.get(
                    "ElasticInferenceAcceleratorAssociations"
                ),
                auto_recovery_enabled=not (
                    instance.get("MaintenanceOptions", {}).get("AutoRecovery")
                    == "disabled"
                ),
                sriov_net_support=instance.get("SriovNetSupport"),
                key_name=instance.get("KeyName"),
                elastic_gpu_specificatiosn=instance.get("ElasticGpuAssociations"),
                nitro_enclave_enabled=instance.get("EnclaveOptions", {}).get("Enabled"),
                license_arns=[
                    license_["LicenseConfigurationArn"]
                    for license_ in instance.get("Licenses", [])
                ],
                hibernation_enabled=instance.get("HibernationOptions", {}).get(
                    "Configured"
                ),
                market_type=None,
                max_price=None,
                spot_instance_type=None,
                block_duration_minutes=None,
                valid_until=None,
                instance_interruption_behavior=None,
                cpu_credits=None,
                cpu_core_count=instance.get("CpuOptions", {}).get("CoreCount"),
                cpu_threads_per_core=instance.get("CpuOptions", {}).get(
                    "ThreadsPerCore"
                ),
                http_tokens=metadata_options.get("HttpTokens"),
                http_put_response_hop_limit=metadata_options.get(
                    "HttpPutResponseHopLimit"
                ),
                http_endpoint_enabled=metadata_options.get("HttpEndpoint") == "enabled",
                http_protocol_ipv6_enabled=metadata_options.get("HttpProtocolIpv6")
                == "enabled",
                metadata_tags_enabled=metadata_options.get("InstanceMetadataTags")
                == "enabled",
                hostname_type=private_dns_name_options.get("HostnameType"),
                enable_resource_name_dns_a_record=private_dns_name_options.get(
                    "EnableResourceNameDnsARecord"
                ),
                enable_resource_name_dns_aaaa_record=private_dns_name_options.get(
                    "EnableResourceNameDnsAAAARecord"
                ),
                capacity_reservation_preference=instance.get(
                    "CapacityReservationSpecification", {}
                ).get("CapacityReservationPreference"),
                bootstrap=[],
            )
            if instance.get("BlockDeviceMappings"):
                result[instance_id][
                    "block_device_mappings"
                ] = await hub.tool.aws.ec2.instance.state.parse_block_device_mapping(
                    ctx, instance.get("BlockDeviceMappings")
                )
            coros.append(
                # launch_template config get most parameters for an instance
                hub.tool.aws.ec2.instance.state.config(ctx, instance_id=instance_id)
            )

    # This can be a heavy process if there are many instances, use coroutines to collect them all at simultaneously
    for ret in asyncio.as_completed(coros):
        instance_id, config = await ret
        result[instance_id].update(config)

    return hub.tool.aws.ec2.instance.data.sanitize_dict(result)


async def parse_block_device_mapping(hub, ctx, block_device_mappings):
    for bdm in block_device_mappings:
        ebs = bdm.get("Ebs")
        volume_id = ebs.get("VolumeId")
        ret = await hub.exec.boto3.client.ec2.describe_volumes(
            ctx, VolumeIds=[volume_id]
        )
        new_ebs = {"DeleteOnTermination": ebs.get("DeleteOnTermination")}
        if ret:
            for volume in ret.ret.get("Volumes", ()):
                new_ebs["VolumeSize"] = volume.get("Size")
                new_ebs["VolumeType"] = volume.get("VolumeType")
                new_ebs["SnapshotId"] = volume.get("SnapshotId")
                new_ebs["Iops"] = volume.get("Iops")
                new_ebs["Throughput"] = volume.get("Throughput")
                new_ebs["Encrypted"] = volume.get("Encrypted")
        bdm["Ebs"] = new_ebs
    return block_device_mappings


async def config(hub, ctx, *, instance_id: str) -> Tuple[str, Dict[str, Any]]:
    """
    Retrieves the configuration data of the specified instance.

    This action calls on other describe actions to get instance information.
    Depending on your instance configuration, you may need to allow the following actions in your IAM policy:
        - DescribeSpotInstanceRequests
        - DescribeInstanceCreditSpecifications
        - DescribeVolumes
        - DescribeInstanceAttribute
        - DescribeElasticGpus.
    Or, you can allow describe* depending on your instance requirements.
    """
    config = {}
    response = await hub.exec.boto3.client.ec2.get_launch_template_data(
        ctx, InstanceId=instance_id
    )
    if response:
        hub.log.trace(
            f"Collecting instance '{instance_id}' config from launch template data"
        )
        # This is ideal and concise
        launch_config = hub.tool.aws.ec2.instance.state.parse_launch_template_data(
            **response.ret["LaunchTemplateData"]
        )
        for key, value in launch_config.items():
            if config.get(key):
                continue
            config[key] = value
    else:
        # Maybe we lack permissions, or we are using localstack and get_launch_template_data is not implemented yet
        # Get that same information elsewhere
        hub.log.trace(f"Collecting instance '{instance_id}' config manually")
        attributes_ = await hub.tool.aws.ec2.instance.state.attributes(
            ctx, instance_id=instance_id
        )
        for key, value in attributes_.items():
            if config.get(key):
                continue
            config[key] = value

    # Collect information that was not part of the launch template
    extended_attributes_ = await hub.tool.aws.ec2.instance.state.extended_attributes(
        ctx, instance_id=instance_id
    )
    for key, value in extended_attributes_.items():
        if config.get(key):
            continue
        config[key] = value

    return instance_id, config


def parse_launch_template_data(hub, **launch_config) -> Dict[str, Any]:
    """
    Parse LaunchTemplateData to collect information about a single instance
    """
    placement = launch_config.get("Placement", {})
    instance_market_options = launch_config.get("InstanceMarketOptions", {})
    spot_options = instance_market_options.get("SpotOptions", {})
    metadata_options = launch_config.get("MetadataOptions", {})
    private_dns_name_options = launch_config.get("PrivateDnsNameOptions", {})
    user_data = launch_config.get("UserData")
    if user_data:
        user_data = base64.b64decode(user_data).decode()

    tags = {}
    for tag_spec in launch_config.get("TagSpecifications", []):
        if tag_spec["ResourceType"] == "instance":
            for tag in tag_spec["Tags"]:
                tags[tag["Key"]] = tag["Value"]

    return dict(
        image_id=launch_config.get("ImageId"),
        instance_type=launch_config.get("InstanceType"),
        # block_device_mappings
        ebs_optimized=launch_config.get("EbsOptimized"),
        kernel_id=launch_config.get("KernelId"),
        # subnet_id=None,
        network_interfaces=launch_config.get("NetworkInterfaces"),
        monitoring_enabled=launch_config.get("Monitoring", {}).get("Enabled"),
        # root_device_name
        # product_codes
        # source_dest_check
        # running
        # private_ip_address
        # reservation_id
        # owner_id
        availability_zone=placement.get("AvailabilityZone"),
        affinity=placement.get("Affinity"),
        group_name=placement.get("GroupName"),
        partition_number=placement.get("PartitionNumber"),
        host_id=placement.get("HostId"),
        tenancy=placement.get("Tenancy"),
        spread_domain=placement.get("SpreadDomain"),
        host_resource_group_arn=placement.get("HostResourceGroupArn"),
        user_data=user_data,
        disable_api_termination=launch_config.get("DisableApiTermination"),
        ram_disk_id=launch_config.get("RamDiskId"),
        tags=tags,
        # iam_instance_profile_arn
        instance_initiated_shutdown_behavior=launch_config.get(
            "InstanceInitiatedShutdownBehavior"
        ),
        elastic_inference_accelerators=launch_config.get(
            "ElasticInferenceAccelerators"
        ),
        # auto_recovery_enabled
        # sriov_net_support
        # key_name
        elastic_gpu_specifications=launch_config.get("ElasticGpuSpecifications"),
        nitro_enclave_enabled=launch_config.get("EnclaveOptions", {}).get("Enabled"),
        hibernation_enabled=launch_config.get("HibernationOptions", {}).get(
            "Configured"
        ),
        market_type=instance_market_options.get("MarketType"),
        max_price=spot_options.get("MaxPrice"),
        spot_instance_type=spot_options.get("SpotInstanceType"),
        block_duration_minutes=spot_options.get("BlockDurationMinutes"),
        valid_until=str(spot_options.get("ValidUntil", "")),
        instance_interruption_behavior=spot_options.get("InstanceInterruptionBehavior"),
        cpu_credits=launch_config.get("CreditSpecification", {}).get("CpuCredits"),
        cpu_core_count=launch_config.get("CpuOptions", {}).get("CoreCount"),
        cpu_threads_per_core=launch_config.get("CpuOptions", {}).get("ThreadsPerCore"),
        http_tokens=metadata_options.get("HttpTokens"),
        http_put_response_hop_limit=metadata_options.get("HttpPutResponseHopLimit"),
        http_endpoint_enabled=metadata_options.get("HttpEndpoint") == "enabled",
        http_protocol_ipv6_enabled=metadata_options.get("HttpProtocolIpv6")
        == "enabled",
        metadata_tags_enabled=metadata_options.get("InstanceMetadataTags") == "enabled",
        hostname_type=private_dns_name_options.get("HostnameType"),
        enable_resource_name_dns_a_record=private_dns_name_options.get(
            "EnableResourceNameDnsARecord"
        )
        == "enabled",
        enable_resource_name_dns_aaaa_record=private_dns_name_options.get(
            "EnableResourceNameDnsAAAARecord"
        )
        == "enabled",
        capacity_reservation_preference=launch_config.get(
            "CapacityReservationSpecification", {}
        ).get("CapacityReservationPreference"),
        # bootstrap
    )


async def attributes(hub, ctx, *, instance_id: str) -> Dict[str, Any]:
    """
    Manually collect information about a single instance, these are also gathered from parsing launch template data
    """
    instance = {}

    ret = await hub.exec.boto3.client.ec2.describe_instance_attribute(
        ctx, Attribute="userData", InstanceId=instance_id
    )
    if ret:
        user_data = ret.ret.get("UserData")
        if user_data:
            user_data = base64.b64decode(user_data).decode()
        instance["user_data"] = user_data

    ret = await hub.exec.boto3.client.ec2.describe_instance_attribute(
        ctx, Attribute="disableApiTermination", InstanceId=instance_id
    )
    if ret:
        instance["disable_api_termination"] = ret.ret["DisableApiTermination"].get(
            "Value"
        )

    ret = await hub.exec.boto3.client.ec2.describe_instance_attribute(
        ctx, Attribute="instanceInitiatedShutdownBehavior", InstanceId=instance_id
    )
    if ret:
        instance["instance_initiated_shutdown_behavior"] = ret.ret[
            "InstanceInitiatedShutdownBehavior"
        ].get("Value")

    ret = await hub.exec.boto3.client.ec2.describe_instance_attribute(
        ctx, Attribute="enclaveOptions", InstanceId=instance_id
    )
    if ret:
        # This is not supported by AWS yet
        instance["enclave_options"] = ret.ret["EnclaveOptions"]["Enabled"]

    ret = await hub.exec.boto3.client.ec2.describe_instance_attribute(
        ctx, Attribute="ramdisk", InstanceId=instance_id
    )
    if ret:
        instance["ram_disk_id"] = ret.ret["RamdiskId"]

    ret = await hub.exec.boto3.client.ec2.describe_tags(
        ctx,
        Filters=[
            {"Name": "resource-id", "Values": [instance_id]},
        ],
    )
    if ret:
        instance["tags"] = {tag["Key"]: tag.get("Value") for tag in ret.ret["Tags"]}

    return instance


async def extended_attributes(hub, ctx, *, instance_id: str) -> Dict[str, Any]:
    """
    Manually collect information about a single instance
    These are not gathered from parsing launch template data or from describe_instances
    """
    instance = {}

    # iam_instance_profile_arn
    ret = await hub.exec.boto3.client.ec2.describe_iam_instance_profile_associations(
        ctx, Filters=[{"Name": "instance-id", "Values": [instance_id]}]
    )
    if ret:
        instance["iam_instance_profile_arn"] = {}
        for association in ret.ret["IamInstanceProfileAssociations"]:
            if association["State"] == "associating":
                # Prefer reporting what will soon be true
                instance["iam_instance_profile_arn"] = association[
                    "IamInstanceProfile"
                ]["Arn"]
                break
            elif association["State"] == "associated":
                # Fallback to the current configuration
                instance["iam_instance_profile_arn"] = association[
                    "IamInstanceProfile"
                ]["Arn"]
                break
            else:
                instance["iam_instance_profile_arn"] = association[
                    "IamInstanceProfile"
                ]["Arn"]
                # Don't break, this might be disassociated

    # sriov_net_support
    ret = await hub.exec.boto3.client.ec2.describe_instance_attribute(
        ctx, Attribute="sriovNetSupport", InstanceId=instance_id
    )
    if ret:
        instance["sriov_net_support"] = ret.ret["SriovNetSupport"].get("Value")

    # volume attachments
    volume_attachments = {}
    ret = await hub.exec.boto3.client.ec2.describe_volumes(
        ctx, Filters=[{"Name": "attachment.instance-id", "Values": [instance_id]}]
    )
    if ret:
        for volume in ret.ret.get("Volumes", ()):
            for attachment in volume.get("Attachments", ()):
                if attachment["InstanceId"] == instance_id:
                    device = attachment["Device"]
                    volume_attachments[device] = volume["VolumeId"]

    instance["volume_attachments"] = volume_attachments

    # bootstrap
    bootstraps = []

    # Detect known bootstrap methods already running on the instance
    heist_managers = hub.tool.heist.bootstrap.managers(hub.heist)
    for heist_manager in heist_managers:
        # TODO What is the actual function call that should be made?
        # if hub.heist[heist_manager].exists():
        #    bootstraps.append(heist_manager)
        ...

    instance["bootstrap"] = bootstraps

    return instance


def test(hub, **kwargs) -> Dict[str, Any]:
    """
    Compute the state based on the parameters passed to an instance.present function for ctx.test
    """
    result = {}
    for k, v in kwargs.items():
        # Ignore kwargs that were None
        if v is None:
            continue
        result[k] = v
    return result
