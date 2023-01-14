"""State module for managing AWS S3 bucket encryption."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]

STATE_NAME = "aws.s3.bucket_encryption"


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    *,
    bucket: str,
    server_side_encryption_configuration: make_dataclass(
        "ServerSideEncryptionConfiguration",
        [
            (
                "Rules",
                List[
                    make_dataclass(
                        "ServerSideEncryptionRule",
                        [
                            (
                                "ApplyServerSideEncryptionByDefault",
                                make_dataclass(
                                    "ServerSideEncryptionByDefault",
                                    [
                                        ("SSEAlgorithm", str),
                                        ("KMSMasterKeyID", str, field(default=None)),
                                    ],
                                ),
                                field(default=None),
                            ),
                            ("BucketKeyEnabled", bool, field(default=None)),
                        ],
                    )
                ],
            )
        ],
    ),
    timeout: make_dataclass(
        "Timeout",
        [
            (
                "update",
                make_dataclass(
                    "UpdateTimeout",
                    [
                        ("delay", int, field(default=4)),
                        ("max_attempts", int, field(default=30)),
                    ],
                ),
                field(default=None),
            )
        ],
    ) = None,
) -> Dict[str, Any]:
    """Creates an encryption configuration for an S3 bucket resource.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            The name of the S3 bucket in Amazon Web Services. It must be equal to the bucket parameter.

        bucket(str):
            The name of the S3 bucket in Amazon Web Services.

        server_side_encryption_configuration(dict):
            The server-side-encryption configuration for the S3 bucket.

        timeout(dict, Optional):
            Timeout configuration for S3 bucket encryption configuration.

            * update (str):
                Timeout configuration for updating the S3 bucket encryption configuration.

                * delay (int, Optional):
                    The amount of time in seconds to wait between attempts. Defaults to 4 seconds.

                * max_attempts (int, Optional):
                    Maximum attempts of waiting for the update. Defaults to 30 attempts.

    Request Syntax:
        .. code-block:: yaml

            [idem_test_aws_s3_bucket_encryption]:
              aws.s3.bucket_encryption.present:
                - name: 'string'
                - bucket: 'string'
                - server_side_encryption_configuration: {'string': []}

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: yaml

            idem_test_aws_s3_bucket_encryption:
              aws.s3.bucket_encryption.present:
                - name: value
                - bucket: value
                - server_side_encryption_configuration:
                    Rules:
                    - ApplyServerSideEncryptionByDefault:
                        SSEAlgorithm: 'AES256'
                        KMSMasterKeyID: 'string'
                      BucketKeyEnabled: True
    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    before_ret = None

    if resource_id:
        if resource_id != bucket:
            result["result"] = False
            result["comment"] = (
                f"Bucket '{bucket}' and resource_id '{resource_id}' parameters must be the same",
            )
            return result

        before_ret = await hub.exec.boto3.client.s3.get_bucket_encryption(
            ctx, Bucket=resource_id
        )
        if not before_ret["result"]:
            result["result"] = False
            result["comment"] = before_ret["comment"]
            return result

    if before_ret:
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type=STATE_NAME, name=name
        )
        result[
            "old_state"
        ] = hub.tool.aws.s3.bucket_encryption.convert_raw_bucket_encryption_to_present(
            bucket=resource_id,
            raw_resource=before_ret.get("ret"),
            idem_resource_name=name,
        )
        result["new_state"] = copy.deepcopy(result["old_state"])

        resource_parameters = {
            "server_side_encryption_configuration": server_side_encryption_configuration,
        }

        if hub.tool.aws.s3.bucket_encryption.is_bucket_encryption_configuration_identical(
            resource_parameters, result["old_state"]
        ):
            # no updates to apply
            return result

        if ctx.get("test", False):
            result["new_state"].update(resource_parameters)
            result["comment"] = result[
                "comment"
            ] + hub.tool.aws.comment_utils.would_update_comment(
                resource_type=STATE_NAME, name=name
            )
            return result
        else:
            result["comment"] = result[
                "comment"
            ] + hub.tool.aws.comment_utils.update_comment(
                resource_type=STATE_NAME, name=name
            )
    else:
        if ctx.get("test", False):
            result[
                "new_state"
            ] = raw_resource = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "bucket": bucket,
                    "server_side_encryption_configuration": server_side_encryption_configuration,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type=STATE_NAME, name=name
            )
            return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type=STATE_NAME, name=name
        )

    put_ret = await hub.exec.boto3.client.s3.put_bucket_encryption(
        ctx,
        Bucket=bucket,
        ServerSideEncryptionConfiguration=server_side_encryption_configuration,
    )
    if not put_ret["result"]:
        result["result"] = False
        result["comment"] = result["comment"] + put_ret["comment"]
        return result

    wait_for_updates_ret = await hub.tool.aws.s3.bucket_encryption.wait_for_updates(
        ctx,
        bucket=bucket,
        server_side_encryption_configuration=server_side_encryption_configuration,
        timeout=timeout.get("update") if timeout else None,
    )
    if not wait_for_updates_ret["result"]:
        result["result"] = False
        result["comment"] += wait_for_updates_ret["comment"]
        return result

    result[
        "new_state"
    ] = hub.tool.aws.s3.bucket_encryption.convert_raw_bucket_encryption_to_present(
        bucket=bucket,
        raw_resource=wait_for_updates_ret.get("ret"),
        idem_resource_name=name,
    )

    return result


async def absent(
    hub, ctx, name: str, resource_id: str = None, timeout: Dict = None
) -> Dict[str, Any]:
    """Deletes an encryption configuration from an S3 bucket resource.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            The name of the S3 bucket in Amazon Web Services.
            Idem automatically considers this resource being absent if this field is not specified.

        timeout(dict, Optional):
            Timeout configuration for S3 bucket encryption configuration.

            * delete (str):
                Timeout configuration for deleting the S3 bucket encryption configuration.

                * delay (int, Optional):
                    The amount of time in seconds to wait between attempts. Defaults to 4 seconds.

                * max_attempts (int, Optional):
                    Maximum attempts of waiting for the deletion. Defaults to 30 attempts.

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_s3_bucket_encryption:
              aws.s3.bucket_encryption.absent:
                - name: value
                - resource_id: value
    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type=STATE_NAME, name=name
        )
        return result

    before_ret = await hub.exec.boto3.client.s3.get_bucket_encryption(
        ctx, Bucket=resource_id
    )
    if not before_ret["result"]:
        if "ServerSideEncryptionConfigurationNotFoundError" not in str(
            before_ret["comment"][0]
        ):
            result["result"] = False
            result["comment"] = before_ret["comment"]
        else:
            result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
                resource_type=STATE_NAME, name=name
            )
        return result

    result[
        "old_state"
    ] = hub.tool.aws.s3.bucket_encryption.convert_raw_bucket_encryption_to_present(
        bucket=resource_id, raw_resource=before_ret["ret"], idem_resource_name=name
    )

    if ctx.get("test", False):
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type=STATE_NAME, name=name
        )
        return result

    delete_ret = await hub.exec.boto3.client.s3.delete_bucket_encryption(
        ctx, Bucket=resource_id
    )
    if not delete_ret["result"]:
        result["result"] = False
        result["comment"] = delete_ret["comment"]
        return result

    wait_for_delete_ret = await hub.tool.aws.s3.bucket_encryption.wait_for_delete(
        ctx,
        bucket=resource_id,
        timeout=timeout.get("delete") if timeout else None,
    )
    if not wait_for_delete_ret["result"]:
        result["result"] = False
        result["comment"] = wait_for_delete_ret["comment"]
        return result

    result["comment"] = hub.tool.aws.comment_utils.delete_comment(
        resource_type=STATE_NAME, name=name
    )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Gets the encryption configuration for each S3 bucket under the given AWS account.

    Returns:
        dict[str, dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.s3.bucket_encryption
    """
    result = {}

    list_buckets_ret = await hub.exec.boto3.client.s3.list_buckets(ctx)
    if not list_buckets_ret["result"]:
        hub.log.debug(f"Could not list S3 buckets: {list_buckets_ret['comment']}")
        return result

    for bucket in list_buckets_ret["ret"]["Buckets"]:
        bucket_name = bucket.get("Name")

        get_bucket_encryption_ret = (
            await hub.exec.boto3.client.s3.get_bucket_encryption(
                ctx, Bucket=bucket_name
            )
        )
        if not get_bucket_encryption_ret["result"]:
            if "ServerSideEncryptionConfigurationNotFoundError" not in str(
                get_bucket_encryption_ret["comment"][0]
            ):
                hub.log.debug(
                    f"Could not get encryption configuration for S3 bucket '{bucket_name}': "
                    f"{get_bucket_encryption_ret['comment']}. Describe will skip this S3 bucket and continue."
                )
            continue

        resource_translated = (
            hub.tool.aws.s3.bucket_encryption.convert_raw_bucket_encryption_to_present(
                bucket=bucket_name,
                raw_resource=get_bucket_encryption_ret["ret"],
            )
        )

        result[resource_translated["name"]] = {
            f"{STATE_NAME}.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }

    return result
