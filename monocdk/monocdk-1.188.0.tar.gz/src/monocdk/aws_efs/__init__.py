'''
# Amazon Elastic File System Construct Library

[Amazon Elastic File System](https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html) (Amazon EFS) provides a simple, scalable,
fully managed elastic NFS file system for use with AWS Cloud services and on-premises resources.
Amazon EFS provides file storage in the AWS Cloud. With Amazon EFS, you can create a file system,
mount the file system on an Amazon EC2 instance, and then read and write data to and from your file system.

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## File Systems

Amazon EFS provides elastic, shared file storage that is POSIX-compliant. The file system you create
supports concurrent read and write access from multiple Amazon EC2 instances and is accessible from
all of the Availability Zones in the AWS Region where it is created. Learn more about [EFS file systems](https://docs.aws.amazon.com/efs/latest/ug/creating-using.html)

### Create an Amazon EFS file system

A Virtual Private Cloud (VPC) is required to create an Amazon EFS file system.
The following example creates a file system that is encrypted at rest, running in `General Purpose`
performance mode, and `Bursting` throughput mode and does not transition files to the Infrequent
Access (IA) storage class.

```python
file_system = efs.FileSystem(self, "MyEfsFileSystem",
    vpc=ec2.Vpc(self, "VPC"),
    lifecycle_policy=efs.LifecyclePolicy.AFTER_14_DAYS,  # files are not transitioned to infrequent access (IA) storage by default
    performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,  # default
    out_of_infrequent_access_policy=efs.OutOfInfrequentAccessPolicy.AFTER_1_ACCESS
)
```

⚠️ An Amazon EFS file system's performance mode can't be changed after the file system has been created.
Updating this property will replace the file system.

Any file system that has been created outside the stack can be imported into your CDK app.

Use the `fromFileSystemAttributes()` API to import an existing file system.
Here is an example of giving a role write permissions on a file system.

```python
import monocdk as iam


imported_file_system = efs.FileSystem.from_file_system_attributes(self, "existingFS",
    file_system_id="fs-12345678",  # You can also use fileSystemArn instead of fileSystemId.
    security_group=ec2.SecurityGroup.from_security_group_id(self, "SG", "sg-123456789",
        allow_all_outbound=False
    )
)
```

### Permissions

If you need to grant file system permissions to another resource, you can use the `.grant()` API.
As an example, the following code gives `elasticfilesystem:ClientWrite` permissions to an IAM role.

```python
role = iam.Role(self, "Role",
    assumed_by=iam.AnyPrincipal()
)

file_system.grant(role, "elasticfilesystem:ClientWrite")
```

### Access Point

An access point is an application-specific view into an EFS file system that applies an operating
system user and group, and a file system path, to any file system request made through the access
point. The operating system user and group override any identity information provided by the NFS
client. The file system path is exposed as the access point's root directory. Applications using
the access point can only access data in its own directory and below. To learn more, see [Mounting a File System Using EFS Access Points](https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html).

Use the `addAccessPoint` API to create an access point from a fileSystem.

```python
file_system.add_access_point("AccessPoint")
```

By default, when you create an access point, the root(`/`) directory is exposed to the client
connecting to the access point. You can specify a custom path with the `path` property.

If `path` does not exist, it will be created with the settings defined in the `creationInfo`.
See [Creating Access Points](https://docs.aws.amazon.com/efs/latest/ug/create-access-point.html) for more details.

Any access point that has been created outside the stack can be imported into your CDK app.

Use the `fromAccessPointAttributes()` API to import an existing access point.

```python
efs.AccessPoint.from_access_point_attributes(self, "ap",
    access_point_id="fsap-1293c4d9832fo0912",
    file_system=efs.FileSystem.from_file_system_attributes(self, "efs",
        file_system_id="fs-099d3e2f",
        security_group=ec2.SecurityGroup.from_security_group_id(self, "sg", "sg-51530134")
    )
)
```

⚠️ Notice: When importing an Access Point using `fromAccessPointAttributes()`, you must make sure
the mount targets are deployed and their lifecycle state is `available`. Otherwise, you may encounter
the following error when deploying:

> EFS file system <ARN of efs> referenced by access point <ARN of access point of EFS> has
> mount targets created in all availability zones the function will execute in, but not all
> are in the available life cycle state yet. Please wait for them to become available and
> try the request again.

### Connecting

To control who can access the EFS, use the `.connections` attribute. EFS has
a fixed default port, so you don't need to specify the port:

```python
file_system.connections.allow_default_port_from(instance)
```

Learn more about [managing file system network accessibility](https://docs.aws.amazon.com/efs/latest/ug/manage-fs-access.html)

### Mounting the file system using User Data

After you create a file system, you can create mount targets. Then you can mount the file system on
EC2 instances, containers, and Lambda functions in your virtual private cloud (VPC).

The following example automatically mounts a file system during instance launch.

```python
file_system.connections.allow_default_port_from(instance)

instance.user_data.add_commands("yum check-update -y", "yum upgrade -y", "yum install -y amazon-efs-utils", "yum install -y nfs-utils", "file_system_id_1=" + file_system.file_system_id, "efs_mount_point_1=/mnt/efs/fs1", "mkdir -p \"${efs_mount_point_1}\"", "test -f \"/sbin/mount.efs\" && echo \"${file_system_id_1}:/ ${efs_mount_point_1} efs defaults,_netdev\" >> /etc/fstab || " + "echo \"${file_system_id_1}.efs." + Stack.of(self).region + ".amazonaws.com:/ ${efs_mount_point_1} nfs4 nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport,_netdev 0 0\" >> /etc/fstab", "mount -a -t efs,nfs4 defaults")
```

Learn more about [mounting EFS file systems](https://docs.aws.amazon.com/efs/latest/ug/mounting-fs.html)

### Deleting

Since file systems are stateful resources, by default the file system will not be deleted when your
stack is deleted.

You can configure the file system to be destroyed on stack deletion by setting a `removalPolicy`

```python
file_system = efs.FileSystem(self, "EfsFileSystem",
    vpc=ec2.Vpc(self, "VPC"),
    removal_policy=RemovalPolicy.DESTROY
)
```
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

import constructs as _constructs_77d1e7e8
from .. import (
    CfnResource as _CfnResource_e0a482dc,
    Construct as _Construct_e78e779f,
    IDependable as _IDependable_1175c9f7,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    RemovalPolicy as _RemovalPolicy_c97e7a20,
    Resource as _Resource_abff4495,
    Size as _Size_7fbd4337,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_ec2 import (
    Connections as _Connections_57ccbda9,
    IConnectable as _IConnectable_c1c0e72c,
    ISecurityGroup as _ISecurityGroup_cdbba9d3,
    IVpc as _IVpc_6d1f76c4,
    SubnetSelection as _SubnetSelection_1284e62c,
)
from ..aws_iam import Grant as _Grant_bcb5eae7, IGrantable as _IGrantable_4c5a91d1
from ..aws_kms import IKey as _IKey_36930160


@jsii.data_type(
    jsii_type="monocdk.aws_efs.AccessPointAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "access_point_arn": "accessPointArn",
        "access_point_id": "accessPointId",
        "file_system": "fileSystem",
    },
)
class AccessPointAttributes:
    def __init__(
        self,
        *,
        access_point_arn: typing.Optional[builtins.str] = None,
        access_point_id: typing.Optional[builtins.str] = None,
        file_system: typing.Optional["IFileSystem"] = None,
    ) -> None:
        '''(experimental) Attributes that can be specified when importing an AccessPoint.

        :param access_point_arn: (experimental) The ARN of the AccessPoint One of this, or {@link accessPointId} is required. Default: - determined based on accessPointId
        :param access_point_id: (experimental) The ID of the AccessPoint One of this, or {@link accessPointArn} is required. Default: - determined based on accessPointArn
        :param file_system: (experimental) The EFS file system. Default: - no EFS file system

        :stability: experimental
        :exampleMetadata: infused

        Example::

            efs.AccessPoint.from_access_point_attributes(self, "ap",
                access_point_id="fsap-1293c4d9832fo0912",
                file_system=efs.FileSystem.from_file_system_attributes(self, "efs",
                    file_system_id="fs-099d3e2f",
                    security_group=ec2.SecurityGroup.from_security_group_id(self, "sg", "sg-51530134")
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb4f45b836dd028aad10b6c18cd54bf762cee1b21fb7f4994881e33caefeb014)
            check_type(argname="argument access_point_arn", value=access_point_arn, expected_type=type_hints["access_point_arn"])
            check_type(argname="argument access_point_id", value=access_point_id, expected_type=type_hints["access_point_id"])
            check_type(argname="argument file_system", value=file_system, expected_type=type_hints["file_system"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_point_arn is not None:
            self._values["access_point_arn"] = access_point_arn
        if access_point_id is not None:
            self._values["access_point_id"] = access_point_id
        if file_system is not None:
            self._values["file_system"] = file_system

    @builtins.property
    def access_point_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the AccessPoint One of this, or {@link accessPointId} is required.

        :default: - determined based on accessPointId

        :stability: experimental
        '''
        result = self._values.get("access_point_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_point_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ID of the AccessPoint One of this, or {@link accessPointArn} is required.

        :default: - determined based on accessPointArn

        :stability: experimental
        '''
        result = self._values.get("access_point_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_system(self) -> typing.Optional["IFileSystem"]:
        '''(experimental) The EFS file system.

        :default: - no EFS file system

        :stability: experimental
        '''
        result = self._values.get("file_system")
        return typing.cast(typing.Optional["IFileSystem"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPointAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_efs.AccessPointOptions",
    jsii_struct_bases=[],
    name_mapping={
        "create_acl": "createAcl",
        "path": "path",
        "posix_user": "posixUser",
    },
)
class AccessPointOptions:
    def __init__(
        self,
        *,
        create_acl: typing.Optional[typing.Union["Acl", typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[builtins.str] = None,
        posix_user: typing.Optional[typing.Union["PosixUser", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options to create an AccessPoint.

        :param create_acl: (experimental) Specifies the POSIX IDs and permissions to apply when creating the access point's root directory. If the root directory specified by ``path`` does not exist, EFS creates the root directory and applies the permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``. Default: - None. The directory specified by ``path`` must exist.
        :param path: (experimental) Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system. Default: '/'
        :param posix_user: (experimental) The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point. Specify this to enforce a user identity using an access point. Default: - user identity not enforced

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as ec2
            import monocdk as efs
            
            
            # create a new VPC
            vpc = ec2.Vpc(self, "VPC")
            
            # create a new Amazon EFS filesystem
            file_system = efs.FileSystem(self, "Efs", vpc=vpc)
            
            # create a new access point from the filesystem
            access_point = file_system.add_access_point("AccessPoint",
                # set /export/lambda as the root of the access point
                path="/export/lambda",
                # as /export/lambda does not exist in a new efs filesystem, the efs will create the directory with the following createAcl
                create_acl=ec2.aws_efs.Acl(
                    owner_uid="1001",
                    owner_gid="1001",
                    permissions="750"
                ),
                # enforce the POSIX identity so lambda function will access with this identity
                posix_user=ec2.aws_efs.PosixUser(
                    uid="1001",
                    gid="1001"
                )
            )
            
            fn = lambda_.Function(self, "MyLambda",
                # mount the access point to /mnt/msg in the lambda runtime environment
                filesystem=lambda_.FileSystem.from_efs_access_point(access_point, "/mnt/msg"),
                runtime=lambda_.Runtime.NODEJS_16_X,
                handler="index.handler",
                code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
                vpc=vpc
            )
        '''
        if isinstance(create_acl, dict):
            create_acl = Acl(**create_acl)
        if isinstance(posix_user, dict):
            posix_user = PosixUser(**posix_user)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04457de26c72a8724950fa6ad7baa5e81e15f68681da1be8e840ca6382cd1d7a)
            check_type(argname="argument create_acl", value=create_acl, expected_type=type_hints["create_acl"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument posix_user", value=posix_user, expected_type=type_hints["posix_user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create_acl is not None:
            self._values["create_acl"] = create_acl
        if path is not None:
            self._values["path"] = path
        if posix_user is not None:
            self._values["posix_user"] = posix_user

    @builtins.property
    def create_acl(self) -> typing.Optional["Acl"]:
        '''(experimental) Specifies the POSIX IDs and permissions to apply when creating the access point's root directory.

        If the
        root directory specified by ``path`` does not exist, EFS creates the root directory and applies the
        permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``.

        :default: - None. The directory specified by ``path`` must exist.

        :stability: experimental
        '''
        result = self._values.get("create_acl")
        return typing.cast(typing.Optional["Acl"], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system.

        :default: '/'

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def posix_user(self) -> typing.Optional["PosixUser"]:
        '''(experimental) The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point.

        Specify this to enforce a user identity using an access point.

        :default: - user identity not enforced

        :see: - `Enforcing a User Identity Using an Access Point <https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html>`_
        :stability: experimental
        '''
        result = self._values.get("posix_user")
        return typing.cast(typing.Optional["PosixUser"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPointOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_efs.AccessPointProps",
    jsii_struct_bases=[AccessPointOptions],
    name_mapping={
        "create_acl": "createAcl",
        "path": "path",
        "posix_user": "posixUser",
        "file_system": "fileSystem",
    },
)
class AccessPointProps(AccessPointOptions):
    def __init__(
        self,
        *,
        create_acl: typing.Optional[typing.Union["Acl", typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[builtins.str] = None,
        posix_user: typing.Optional[typing.Union["PosixUser", typing.Dict[builtins.str, typing.Any]]] = None,
        file_system: "IFileSystem",
    ) -> None:
        '''(experimental) Properties for the AccessPoint.

        :param create_acl: (experimental) Specifies the POSIX IDs and permissions to apply when creating the access point's root directory. If the root directory specified by ``path`` does not exist, EFS creates the root directory and applies the permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``. Default: - None. The directory specified by ``path`` must exist.
        :param path: (experimental) Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system. Default: '/'
        :param posix_user: (experimental) The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point. Specify this to enforce a user identity using an access point. Default: - user identity not enforced
        :param file_system: (experimental) The efs filesystem.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_efs as efs
            
            # file_system: efs.FileSystem
            
            access_point_props = efs.AccessPointProps(
                file_system=file_system,
            
                # the properties below are optional
                create_acl=efs.Acl(
                    owner_gid="ownerGid",
                    owner_uid="ownerUid",
                    permissions="permissions"
                ),
                path="path",
                posix_user=efs.PosixUser(
                    gid="gid",
                    uid="uid",
            
                    # the properties below are optional
                    secondary_gids=["secondaryGids"]
                )
            )
        '''
        if isinstance(create_acl, dict):
            create_acl = Acl(**create_acl)
        if isinstance(posix_user, dict):
            posix_user = PosixUser(**posix_user)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f87bd0ce42e43fe9db8139f1c4da324c8bf3aa43fe6b60ceef852c64dddb52b6)
            check_type(argname="argument create_acl", value=create_acl, expected_type=type_hints["create_acl"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument posix_user", value=posix_user, expected_type=type_hints["posix_user"])
            check_type(argname="argument file_system", value=file_system, expected_type=type_hints["file_system"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file_system": file_system,
        }
        if create_acl is not None:
            self._values["create_acl"] = create_acl
        if path is not None:
            self._values["path"] = path
        if posix_user is not None:
            self._values["posix_user"] = posix_user

    @builtins.property
    def create_acl(self) -> typing.Optional["Acl"]:
        '''(experimental) Specifies the POSIX IDs and permissions to apply when creating the access point's root directory.

        If the
        root directory specified by ``path`` does not exist, EFS creates the root directory and applies the
        permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``.

        :default: - None. The directory specified by ``path`` must exist.

        :stability: experimental
        '''
        result = self._values.get("create_acl")
        return typing.cast(typing.Optional["Acl"], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system.

        :default: '/'

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def posix_user(self) -> typing.Optional["PosixUser"]:
        '''(experimental) The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point.

        Specify this to enforce a user identity using an access point.

        :default: - user identity not enforced

        :see: - `Enforcing a User Identity Using an Access Point <https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html>`_
        :stability: experimental
        '''
        result = self._values.get("posix_user")
        return typing.cast(typing.Optional["PosixUser"], result)

    @builtins.property
    def file_system(self) -> "IFileSystem":
        '''(experimental) The efs filesystem.

        :stability: experimental
        '''
        result = self._values.get("file_system")
        assert result is not None, "Required property 'file_system' is missing"
        return typing.cast("IFileSystem", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_efs.Acl",
    jsii_struct_bases=[],
    name_mapping={
        "owner_gid": "ownerGid",
        "owner_uid": "ownerUid",
        "permissions": "permissions",
    },
)
class Acl:
    def __init__(
        self,
        *,
        owner_gid: builtins.str,
        owner_uid: builtins.str,
        permissions: builtins.str,
    ) -> None:
        '''(experimental) Permissions as POSIX ACL.

        :param owner_gid: (experimental) Specifies the POSIX group ID to apply to the RootDirectory. Accepts values from 0 to 2^32 (4294967295).
        :param owner_uid: (experimental) Specifies the POSIX user ID to apply to the RootDirectory. Accepts values from 0 to 2^32 (4294967295).
        :param permissions: (experimental) Specifies the POSIX permissions to apply to the RootDirectory, in the format of an octal number representing the file's mode bits.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as ec2
            import monocdk as efs
            
            
            # create a new VPC
            vpc = ec2.Vpc(self, "VPC")
            
            # create a new Amazon EFS filesystem
            file_system = efs.FileSystem(self, "Efs", vpc=vpc)
            
            # create a new access point from the filesystem
            access_point = file_system.add_access_point("AccessPoint",
                # set /export/lambda as the root of the access point
                path="/export/lambda",
                # as /export/lambda does not exist in a new efs filesystem, the efs will create the directory with the following createAcl
                create_acl=ec2.aws_efs.Acl(
                    owner_uid="1001",
                    owner_gid="1001",
                    permissions="750"
                ),
                # enforce the POSIX identity so lambda function will access with this identity
                posix_user=ec2.aws_efs.PosixUser(
                    uid="1001",
                    gid="1001"
                )
            )
            
            fn = lambda_.Function(self, "MyLambda",
                # mount the access point to /mnt/msg in the lambda runtime environment
                filesystem=lambda_.FileSystem.from_efs_access_point(access_point, "/mnt/msg"),
                runtime=lambda_.Runtime.NODEJS_16_X,
                handler="index.handler",
                code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
                vpc=vpc
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf4f3c53a86c9e8103f4c9af8047128c63b714aac04d1cb324880a9f3ba1a738)
            check_type(argname="argument owner_gid", value=owner_gid, expected_type=type_hints["owner_gid"])
            check_type(argname="argument owner_uid", value=owner_uid, expected_type=type_hints["owner_uid"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "owner_gid": owner_gid,
            "owner_uid": owner_uid,
            "permissions": permissions,
        }

    @builtins.property
    def owner_gid(self) -> builtins.str:
        '''(experimental) Specifies the POSIX group ID to apply to the RootDirectory.

        Accepts values from 0 to 2^32 (4294967295).

        :stability: experimental
        '''
        result = self._values.get("owner_gid")
        assert result is not None, "Required property 'owner_gid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def owner_uid(self) -> builtins.str:
        '''(experimental) Specifies the POSIX user ID to apply to the RootDirectory.

        Accepts values from 0 to 2^32 (4294967295).

        :stability: experimental
        '''
        result = self._values.get("owner_uid")
        assert result is not None, "Required property 'owner_uid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def permissions(self) -> builtins.str:
        '''(experimental) Specifies the POSIX permissions to apply to the RootDirectory, in the format of an octal number representing the file's mode bits.

        :stability: experimental
        '''
        result = self._values.get("permissions")
        assert result is not None, "Required property 'permissions' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Acl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnAccessPoint(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_efs.CfnAccessPoint",
):
    '''A CloudFormation ``AWS::EFS::AccessPoint``.

    The ``AWS::EFS::AccessPoint`` resource creates an EFS access point. An access point is an application-specific view into an EFS file system that applies an operating system user and group, and a file system path, to any file system request made through the access point. The operating system user and group override any identity information provided by the NFS client. The file system path is exposed as the access point's root directory. Applications using the access point can only access data in its own directory and below. To learn more, see `Mounting a file system using EFS access points <https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html>`_ .

    This operation requires permissions for the ``elasticfilesystem:CreateAccessPoint`` action.

    :cloudformationResource: AWS::EFS::AccessPoint
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_efs as efs
        
        cfn_access_point = efs.CfnAccessPoint(self, "MyCfnAccessPoint",
            file_system_id="fileSystemId",
        
            # the properties below are optional
            access_point_tags=[efs.CfnAccessPoint.AccessPointTagProperty(
                key="key",
                value="value"
            )],
            client_token="clientToken",
            posix_user=efs.CfnAccessPoint.PosixUserProperty(
                gid="gid",
                uid="uid",
        
                # the properties below are optional
                secondary_gids=["secondaryGids"]
            ),
            root_directory=efs.CfnAccessPoint.RootDirectoryProperty(
                creation_info=efs.CfnAccessPoint.CreationInfoProperty(
                    owner_gid="ownerGid",
                    owner_uid="ownerUid",
                    permissions="permissions"
                ),
                path="path"
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        file_system_id: builtins.str,
        access_point_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAccessPoint.AccessPointTagProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        client_token: typing.Optional[builtins.str] = None,
        posix_user: typing.Optional[typing.Union[typing.Union["CfnAccessPoint.PosixUserProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        root_directory: typing.Optional[typing.Union[typing.Union["CfnAccessPoint.RootDirectoryProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::EFS::AccessPoint``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param file_system_id: The ID of the EFS file system that the access point applies to. Accepts only the ID format for input when specifying a file system, for example ``fs-0123456789abcedf2`` .
        :param access_point_tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param client_token: The opaque string specified in the request to ensure idempotent creation.
        :param posix_user: The full POSIX identity, including the user ID, group ID, and secondary group IDs on the access point that is used for all file operations by NFS clients using the access point.
        :param root_directory: The directory on the Amazon EFS file system that the access point exposes as the root directory to NFS clients using the access point.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f32c4a24917986082671fc977a5d82607d505538779b484916fb7848304135da)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAccessPointProps(
            file_system_id=file_system_id,
            access_point_tags=access_point_tags,
            client_token=client_token,
            posix_user=posix_user,
            root_directory=root_directory,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a5ad3bd290d125ca66755280ed34c773b967e49185628ad7a7cc8d3d62711a9)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7765f019eff1b33671948fbafb4285c7aa4f9eb7b667470c7e686c74016db257)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAccessPointId")
    def attr_access_point_id(self) -> builtins.str:
        '''The ID of the EFS access point.

        :cloudformationAttribute: AccessPointId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAccessPointId"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the access point.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> builtins.str:
        '''The ID of the EFS file system that the access point applies to.

        Accepts only the ID format for input when specifying a file system, for example ``fs-0123456789abcedf2`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-filesystemid
        '''
        return typing.cast(builtins.str, jsii.get(self, "fileSystemId"))

    @file_system_id.setter
    def file_system_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25759ba94eaa0f570ccbf7f9435279d13cb81cbe846f5d996e6ef11c79d713d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileSystemId", value)

    @builtins.property
    @jsii.member(jsii_name="accessPointTags")
    def access_point_tags(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAccessPoint.AccessPointTagProperty", _IResolvable_a771d0ef]]]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-accesspointtags
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAccessPoint.AccessPointTagProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "accessPointTags"))

    @access_point_tags.setter
    def access_point_tags(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAccessPoint.AccessPointTagProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3205c38dcb273ae02e63aec1881ca0ff7ec5e4538dd8cd71a185c5d0a70984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessPointTags", value)

    @builtins.property
    @jsii.member(jsii_name="clientToken")
    def client_token(self) -> typing.Optional[builtins.str]:
        '''The opaque string specified in the request to ensure idempotent creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-clienttoken
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientToken"))

    @client_token.setter
    def client_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1703204e32c64998cc4da211cc0cbe9a7c56a8b8a45c593e5b8f053e641d4828)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientToken", value)

    @builtins.property
    @jsii.member(jsii_name="posixUser")
    def posix_user(
        self,
    ) -> typing.Optional[typing.Union["CfnAccessPoint.PosixUserProperty", _IResolvable_a771d0ef]]:
        '''The full POSIX identity, including the user ID, group ID, and secondary group IDs on the access point that is used for all file operations by NFS clients using the access point.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-posixuser
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAccessPoint.PosixUserProperty", _IResolvable_a771d0ef]], jsii.get(self, "posixUser"))

    @posix_user.setter
    def posix_user(
        self,
        value: typing.Optional[typing.Union["CfnAccessPoint.PosixUserProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a789f5efecfb6eaa71be9279197a92a00ccd4b5d1622cc1ed2ab0ebe31ef2590)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "posixUser", value)

    @builtins.property
    @jsii.member(jsii_name="rootDirectory")
    def root_directory(
        self,
    ) -> typing.Optional[typing.Union["CfnAccessPoint.RootDirectoryProperty", _IResolvable_a771d0ef]]:
        '''The directory on the Amazon EFS file system that the access point exposes as the root directory to NFS clients using the access point.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-rootdirectory
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAccessPoint.RootDirectoryProperty", _IResolvable_a771d0ef]], jsii.get(self, "rootDirectory"))

    @root_directory.setter
    def root_directory(
        self,
        value: typing.Optional[typing.Union["CfnAccessPoint.RootDirectoryProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed29aa5ab85ee8989982dce7208c403f2ac4b8399ead09548841451800a5271)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootDirectory", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_efs.CfnAccessPoint.AccessPointTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class AccessPointTagProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A tag is a key-value pair attached to a file system.

            Allowed characters in the ``Key`` and ``Value`` properties are letters, white space, and numbers that can be represented in UTF-8, and the following characters: ``+ - = . _ : /``

            :param key: The tag key (String). The key can't start with ``aws:`` .
            :param value: The value of the tag key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-accesspointtag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_efs as efs
                
                access_point_tag_property = efs.CfnAccessPoint.AccessPointTagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2bad9274deae6c8646b9dba6e6bc7b58ae3538fef4d545924742231085fc5b25)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The tag key (String).

            The key can't start with ``aws:`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-accesspointtag.html#cfn-efs-accesspoint-accesspointtag-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the tag key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-accesspointtag.html#cfn-efs-accesspoint-accesspointtag-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessPointTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_efs.CfnAccessPoint.CreationInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "owner_gid": "ownerGid",
            "owner_uid": "ownerUid",
            "permissions": "permissions",
        },
    )
    class CreationInfoProperty:
        def __init__(
            self,
            *,
            owner_gid: builtins.str,
            owner_uid: builtins.str,
            permissions: builtins.str,
        ) -> None:
            '''Required if the ``RootDirectory`` > ``Path`` specified does not exist.

            Specifies the POSIX IDs and permissions to apply to the access point's ``RootDirectory`` > ``Path`` . If the access point root directory does not exist, EFS creates it with these settings when a client connects to the access point. When specifying ``CreationInfo`` , you must include values for all properties.

            Amazon EFS creates a root directory only if you have provided the CreationInfo: OwnUid, OwnGID, and permissions for the directory. If you do not provide this information, Amazon EFS does not create the root directory. If the root directory does not exist, attempts to mount using the access point will fail.
            .. epigraph::

               If you do not provide ``CreationInfo`` and the specified ``RootDirectory`` does not exist, attempts to mount the file system using the access point will fail.

            :param owner_gid: Specifies the POSIX group ID to apply to the ``RootDirectory`` . Accepts values from 0 to 2^32 (4294967295).
            :param owner_uid: Specifies the POSIX user ID to apply to the ``RootDirectory`` . Accepts values from 0 to 2^32 (4294967295).
            :param permissions: Specifies the POSIX permissions to apply to the ``RootDirectory`` , in the format of an octal number representing the file's mode bits.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-creationinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_efs as efs
                
                creation_info_property = efs.CfnAccessPoint.CreationInfoProperty(
                    owner_gid="ownerGid",
                    owner_uid="ownerUid",
                    permissions="permissions"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d5a8cab115cb36e8085151ede3e5ae9f8d4421f293558cbdc9d7f0538e257e06)
                check_type(argname="argument owner_gid", value=owner_gid, expected_type=type_hints["owner_gid"])
                check_type(argname="argument owner_uid", value=owner_uid, expected_type=type_hints["owner_uid"])
                check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "owner_gid": owner_gid,
                "owner_uid": owner_uid,
                "permissions": permissions,
            }

        @builtins.property
        def owner_gid(self) -> builtins.str:
            '''Specifies the POSIX group ID to apply to the ``RootDirectory`` .

            Accepts values from 0 to 2^32 (4294967295).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-creationinfo.html#cfn-efs-accesspoint-creationinfo-ownergid
            '''
            result = self._values.get("owner_gid")
            assert result is not None, "Required property 'owner_gid' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def owner_uid(self) -> builtins.str:
            '''Specifies the POSIX user ID to apply to the ``RootDirectory`` .

            Accepts values from 0 to 2^32 (4294967295).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-creationinfo.html#cfn-efs-accesspoint-creationinfo-owneruid
            '''
            result = self._values.get("owner_uid")
            assert result is not None, "Required property 'owner_uid' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def permissions(self) -> builtins.str:
            '''Specifies the POSIX permissions to apply to the ``RootDirectory`` , in the format of an octal number representing the file's mode bits.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-creationinfo.html#cfn-efs-accesspoint-creationinfo-permissions
            '''
            result = self._values.get("permissions")
            assert result is not None, "Required property 'permissions' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CreationInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_efs.CfnAccessPoint.PosixUserProperty",
        jsii_struct_bases=[],
        name_mapping={"gid": "gid", "uid": "uid", "secondary_gids": "secondaryGids"},
    )
    class PosixUserProperty:
        def __init__(
            self,
            *,
            gid: builtins.str,
            uid: builtins.str,
            secondary_gids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point.

            :param gid: The POSIX group ID used for all file system operations using this access point.
            :param uid: The POSIX user ID used for all file system operations using this access point.
            :param secondary_gids: Secondary POSIX group IDs used for all file system operations using this access point.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-posixuser.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_efs as efs
                
                posix_user_property = efs.CfnAccessPoint.PosixUserProperty(
                    gid="gid",
                    uid="uid",
                
                    # the properties below are optional
                    secondary_gids=["secondaryGids"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9a11f23b12483ffa015eea74b622cc21f8d72f20f77491d7ed54c3ce6806bc5a)
                check_type(argname="argument gid", value=gid, expected_type=type_hints["gid"])
                check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
                check_type(argname="argument secondary_gids", value=secondary_gids, expected_type=type_hints["secondary_gids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "gid": gid,
                "uid": uid,
            }
            if secondary_gids is not None:
                self._values["secondary_gids"] = secondary_gids

        @builtins.property
        def gid(self) -> builtins.str:
            '''The POSIX group ID used for all file system operations using this access point.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-posixuser.html#cfn-efs-accesspoint-posixuser-gid
            '''
            result = self._values.get("gid")
            assert result is not None, "Required property 'gid' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def uid(self) -> builtins.str:
            '''The POSIX user ID used for all file system operations using this access point.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-posixuser.html#cfn-efs-accesspoint-posixuser-uid
            '''
            result = self._values.get("uid")
            assert result is not None, "Required property 'uid' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def secondary_gids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Secondary POSIX group IDs used for all file system operations using this access point.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-posixuser.html#cfn-efs-accesspoint-posixuser-secondarygids
            '''
            result = self._values.get("secondary_gids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PosixUserProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_efs.CfnAccessPoint.RootDirectoryProperty",
        jsii_struct_bases=[],
        name_mapping={"creation_info": "creationInfo", "path": "path"},
    )
    class RootDirectoryProperty:
        def __init__(
            self,
            *,
            creation_info: typing.Optional[typing.Union[typing.Union["CfnAccessPoint.CreationInfoProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the directory on the Amazon EFS file system that the access point provides access to.

            The access point exposes the specified file system path as the root directory of your file system to applications using the access point. NFS clients using the access point can only access data in the access point's ``RootDirectory`` and it's subdirectories.

            :param creation_info: (Optional) Specifies the POSIX IDs and permissions to apply to the access point's ``RootDirectory`` . If the ``RootDirectory`` > ``Path`` specified does not exist, EFS creates the root directory using the ``CreationInfo`` settings when a client connects to an access point. When specifying the ``CreationInfo`` , you must provide values for all properties. .. epigraph:: If you do not provide ``CreationInfo`` and the specified ``RootDirectory`` > ``Path`` does not exist, attempts to mount the file system using the access point will fail.
            :param path: Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system. A path can have up to four subdirectories. If the specified path does not exist, you are required to provide the ``CreationInfo`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-rootdirectory.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_efs as efs
                
                root_directory_property = efs.CfnAccessPoint.RootDirectoryProperty(
                    creation_info=efs.CfnAccessPoint.CreationInfoProperty(
                        owner_gid="ownerGid",
                        owner_uid="ownerUid",
                        permissions="permissions"
                    ),
                    path="path"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cf8917b2c4c52d1f6208de95be4ab891aa9739d9c41cb3c47cfb99167c157093)
                check_type(argname="argument creation_info", value=creation_info, expected_type=type_hints["creation_info"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if creation_info is not None:
                self._values["creation_info"] = creation_info
            if path is not None:
                self._values["path"] = path

        @builtins.property
        def creation_info(
            self,
        ) -> typing.Optional[typing.Union["CfnAccessPoint.CreationInfoProperty", _IResolvable_a771d0ef]]:
            '''(Optional) Specifies the POSIX IDs and permissions to apply to the access point's ``RootDirectory`` .

            If the ``RootDirectory`` > ``Path`` specified does not exist, EFS creates the root directory using the ``CreationInfo`` settings when a client connects to an access point. When specifying the ``CreationInfo`` , you must provide values for all properties.
            .. epigraph::

               If you do not provide ``CreationInfo`` and the specified ``RootDirectory`` > ``Path`` does not exist, attempts to mount the file system using the access point will fail.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-rootdirectory.html#cfn-efs-accesspoint-rootdirectory-creationinfo
            '''
            result = self._values.get("creation_info")
            return typing.cast(typing.Optional[typing.Union["CfnAccessPoint.CreationInfoProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system.

            A path can have up to four subdirectories. If the specified path does not exist, you are required to provide the ``CreationInfo`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-rootdirectory.html#cfn-efs-accesspoint-rootdirectory-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RootDirectoryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_efs.CfnAccessPointProps",
    jsii_struct_bases=[],
    name_mapping={
        "file_system_id": "fileSystemId",
        "access_point_tags": "accessPointTags",
        "client_token": "clientToken",
        "posix_user": "posixUser",
        "root_directory": "rootDirectory",
    },
)
class CfnAccessPointProps:
    def __init__(
        self,
        *,
        file_system_id: builtins.str,
        access_point_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAccessPoint.AccessPointTagProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        client_token: typing.Optional[builtins.str] = None,
        posix_user: typing.Optional[typing.Union[typing.Union[CfnAccessPoint.PosixUserProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        root_directory: typing.Optional[typing.Union[typing.Union[CfnAccessPoint.RootDirectoryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAccessPoint``.

        :param file_system_id: The ID of the EFS file system that the access point applies to. Accepts only the ID format for input when specifying a file system, for example ``fs-0123456789abcedf2`` .
        :param access_point_tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param client_token: The opaque string specified in the request to ensure idempotent creation.
        :param posix_user: The full POSIX identity, including the user ID, group ID, and secondary group IDs on the access point that is used for all file operations by NFS clients using the access point.
        :param root_directory: The directory on the Amazon EFS file system that the access point exposes as the root directory to NFS clients using the access point.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_efs as efs
            
            cfn_access_point_props = efs.CfnAccessPointProps(
                file_system_id="fileSystemId",
            
                # the properties below are optional
                access_point_tags=[efs.CfnAccessPoint.AccessPointTagProperty(
                    key="key",
                    value="value"
                )],
                client_token="clientToken",
                posix_user=efs.CfnAccessPoint.PosixUserProperty(
                    gid="gid",
                    uid="uid",
            
                    # the properties below are optional
                    secondary_gids=["secondaryGids"]
                ),
                root_directory=efs.CfnAccessPoint.RootDirectoryProperty(
                    creation_info=efs.CfnAccessPoint.CreationInfoProperty(
                        owner_gid="ownerGid",
                        owner_uid="ownerUid",
                        permissions="permissions"
                    ),
                    path="path"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ab6a1017fd34b079bb62e6dd8bd5205d00f5ce5dbf46ad848bb3dfdce002aab)
            check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
            check_type(argname="argument access_point_tags", value=access_point_tags, expected_type=type_hints["access_point_tags"])
            check_type(argname="argument client_token", value=client_token, expected_type=type_hints["client_token"])
            check_type(argname="argument posix_user", value=posix_user, expected_type=type_hints["posix_user"])
            check_type(argname="argument root_directory", value=root_directory, expected_type=type_hints["root_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file_system_id": file_system_id,
        }
        if access_point_tags is not None:
            self._values["access_point_tags"] = access_point_tags
        if client_token is not None:
            self._values["client_token"] = client_token
        if posix_user is not None:
            self._values["posix_user"] = posix_user
        if root_directory is not None:
            self._values["root_directory"] = root_directory

    @builtins.property
    def file_system_id(self) -> builtins.str:
        '''The ID of the EFS file system that the access point applies to.

        Accepts only the ID format for input when specifying a file system, for example ``fs-0123456789abcedf2`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-filesystemid
        '''
        result = self._values.get("file_system_id")
        assert result is not None, "Required property 'file_system_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_point_tags(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAccessPoint.AccessPointTagProperty, _IResolvable_a771d0ef]]]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-accesspointtags
        '''
        result = self._values.get("access_point_tags")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAccessPoint.AccessPointTagProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def client_token(self) -> typing.Optional[builtins.str]:
        '''The opaque string specified in the request to ensure idempotent creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-clienttoken
        '''
        result = self._values.get("client_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def posix_user(
        self,
    ) -> typing.Optional[typing.Union[CfnAccessPoint.PosixUserProperty, _IResolvable_a771d0ef]]:
        '''The full POSIX identity, including the user ID, group ID, and secondary group IDs on the access point that is used for all file operations by NFS clients using the access point.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-posixuser
        '''
        result = self._values.get("posix_user")
        return typing.cast(typing.Optional[typing.Union[CfnAccessPoint.PosixUserProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def root_directory(
        self,
    ) -> typing.Optional[typing.Union[CfnAccessPoint.RootDirectoryProperty, _IResolvable_a771d0ef]]:
        '''The directory on the Amazon EFS file system that the access point exposes as the root directory to NFS clients using the access point.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-rootdirectory
        '''
        result = self._values.get("root_directory")
        return typing.cast(typing.Optional[typing.Union[CfnAccessPoint.RootDirectoryProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessPointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnFileSystem(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_efs.CfnFileSystem",
):
    '''A CloudFormation ``AWS::EFS::FileSystem``.

    The ``AWS::EFS::FileSystem`` resource creates a new, empty file system in Amazon Elastic File System ( Amazon EFS ). You must create a mount target ( `AWS::EFS::MountTarget <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html>`_ ) to mount your EFS file system on an Amazon EC2 or other AWS cloud compute resource.

    :cloudformationResource: AWS::EFS::FileSystem
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_efs as efs
        
        # file_system_policy: Any
        
        cfn_file_system = efs.CfnFileSystem(self, "MyCfnFileSystem",
            availability_zone_name="availabilityZoneName",
            backup_policy=efs.CfnFileSystem.BackupPolicyProperty(
                status="status"
            ),
            bypass_policy_lockout_safety_check=False,
            encrypted=False,
            file_system_policy=file_system_policy,
            file_system_tags=[efs.CfnFileSystem.ElasticFileSystemTagProperty(
                key="key",
                value="value"
            )],
            kms_key_id="kmsKeyId",
            lifecycle_policies=[efs.CfnFileSystem.LifecyclePolicyProperty(
                transition_to_ia="transitionToIa",
                transition_to_primary_storage_class="transitionToPrimaryStorageClass"
            )],
            performance_mode="performanceMode",
            provisioned_throughput_in_mibps=123,
            throughput_mode="throughputMode"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        availability_zone_name: typing.Optional[builtins.str] = None,
        backup_policy: typing.Optional[typing.Union[typing.Union["CfnFileSystem.BackupPolicyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        bypass_policy_lockout_safety_check: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        encrypted: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        file_system_policy: typing.Any = None,
        file_system_tags: typing.Optional[typing.Sequence[typing.Union["CfnFileSystem.ElasticFileSystemTagProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        lifecycle_policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnFileSystem.LifecyclePolicyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        performance_mode: typing.Optional[builtins.str] = None,
        provisioned_throughput_in_mibps: typing.Optional[jsii.Number] = None,
        throughput_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::EFS::FileSystem``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param availability_zone_name: Used to create a file system that uses One Zone storage classes. It specifies the AWS Availability Zone in which to create the file system. Use the format ``us-east-1a`` to specify the Availability Zone. For more information about One Zone storage classes, see `Using EFS storage classes <https://docs.aws.amazon.com/efs/latest/ug/storage-classes.html>`_ in the *Amazon EFS User Guide* . .. epigraph:: One Zone storage classes are not available in all Availability Zones in AWS Regions where Amazon EFS is available.
        :param backup_policy: Use the ``BackupPolicy`` to turn automatic backups on or off for the file system.
        :param bypass_policy_lockout_safety_check: (Optional) A boolean that specifies whether or not to bypass the ``FileSystemPolicy`` lockout safety check. The lockout safety check determines whether the policy in the request will lock out, or prevent, the IAM principal that is making the request from making future ``PutFileSystemPolicy`` requests on this file system. Set ``BypassPolicyLockoutSafetyCheck`` to ``True`` only when you intend to prevent the IAM principal that is making the request from making subsequent ``PutFileSystemPolicy`` requests on this file system. The default value is ``False`` .
        :param encrypted: A Boolean value that, if true, creates an encrypted file system. When creating an encrypted file system, you have the option of specifying a KmsKeyId for an existing AWS KMS key . If you don't specify a KMS key , then the default KMS key for Amazon EFS , ``/aws/elasticfilesystem`` , is used to protect the encrypted file system.
        :param file_system_policy: The ``FileSystemPolicy`` for the EFS file system. A file system policy is an IAM resource policy used to control NFS access to an EFS file system. For more information, see `Using IAM to control NFS access to Amazon EFS <https://docs.aws.amazon.com/efs/latest/ug/iam-access-control-nfs-efs.html>`_ in the *Amazon EFS User Guide* .
        :param file_system_tags: Use to create one or more tags associated with the file system. Each tag is a user-defined key-value pair. Name your file system on creation by including a ``"Key":"Name","Value":"{value}"`` key-value pair. Each key must be unique. For more information, see `Tagging AWS resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in the *AWS General Reference Guide* .
        :param kms_key_id: The ID of the AWS KMS key to be used to protect the encrypted file system. This parameter is only required if you want to use a nondefault KMS key . If this parameter is not specified, the default KMS key for Amazon EFS is used. This ID can be in one of the following formats: - Key ID - A unique identifier of the key, for example ``1234abcd-12ab-34cd-56ef-1234567890ab`` . - ARN - An Amazon Resource Name (ARN) for the key, for example ``arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` . - Key alias - A previously created display name for a key, for example ``alias/projectKey1`` . - Key alias ARN - An ARN for a key alias, for example ``arn:aws:kms:us-west-2:444455556666:alias/projectKey1`` . If ``KmsKeyId`` is specified, the ``Encrypted`` parameter must be set to true.
        :param lifecycle_policies: An array of ``LifecyclePolicy`` objects that define the file system's ``LifecycleConfiguration`` object. A ``LifecycleConfiguration`` object informs EFS lifecycle management and intelligent tiering of the following: - When to move files in the file system from primary storage to the IA storage class. - When to move files that are in IA storage to primary storage. .. epigraph:: Amazon EFS requires that each ``LifecyclePolicy`` object have only a single transition. This means that in a request body, ``LifecyclePolicies`` needs to be structured as an array of ``LifecyclePolicy`` objects, one object for each transition, ``TransitionToIA`` , ``TransitionToPrimaryStorageClass`` . See the example requests in the following section for more information.
        :param performance_mode: The performance mode of the file system. We recommend ``generalPurpose`` performance mode for most file systems. File systems using the ``maxIO`` performance mode can scale to higher levels of aggregate throughput and operations per second with a tradeoff of slightly higher latencies for most file operations. The performance mode can't be changed after the file system has been created. .. epigraph:: The ``maxIO`` mode is not supported on file systems using One Zone storage classes.
        :param provisioned_throughput_in_mibps: The throughput, measured in MiB/s, that you want to provision for a file system that you're creating. Valid values are 1-1024. Required if ``ThroughputMode`` is set to ``provisioned`` . The upper limit for throughput is 1024 MiB/s. To increase this limit, contact AWS Support . For more information, see `Amazon EFS quotas that you can increase <https://docs.aws.amazon.com/efs/latest/ug/limits.html#soft-limits>`_ in the *Amazon EFS User Guide* .
        :param throughput_mode: Specifies the throughput mode for the file system. The mode can be ``bursting`` , ``provisioned`` , or ``elastic`` . If you set ``ThroughputMode`` to ``provisioned`` , you must also set a value for ``ProvisionedThroughputInMibps`` . After you create the file system, you can decrease your file system's throughput in Provisioned Throughput mode or change between the throughput modes, with certain time restrictions. For more information, see `Specifying throughput with provisioned mode <https://docs.aws.amazon.com/efs/latest/ug/performance.html#provisioned-throughput>`_ in the *Amazon EFS User Guide* . Default is ``bursting`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fbfdc5ac9791e193151a0e3604c198c382fdfe82e3c3a98f3c335354c952aee)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFileSystemProps(
            availability_zone_name=availability_zone_name,
            backup_policy=backup_policy,
            bypass_policy_lockout_safety_check=bypass_policy_lockout_safety_check,
            encrypted=encrypted,
            file_system_policy=file_system_policy,
            file_system_tags=file_system_tags,
            kms_key_id=kms_key_id,
            lifecycle_policies=lifecycle_policies,
            performance_mode=performance_mode,
            provisioned_throughput_in_mibps=provisioned_throughput_in_mibps,
            throughput_mode=throughput_mode,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b113d15551cf887a56515a93c679210d6423cf76c7800ac8af9096c0b2159ad5)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__530bfcf5954fc9512793028f1b1715d4b972629ce7a3551104a5071e2dc44052)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the EFS file system.

        Example: ``arn:aws:elasticfilesystem:us-west-2:1111333322228888:file-system/fs-0123456789abcdef8``

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrFileSystemId")
    def attr_file_system_id(self) -> builtins.str:
        '''The ID of the EFS file system.

        For example: ``fs-abcdef0123456789a``

        :cloudformationAttribute: FileSystemId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFileSystemId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Use to create one or more tags associated with the file system.

        Each tag is a user-defined key-value pair. Name your file system on creation by including a ``"Key":"Name","Value":"{value}"`` key-value pair. Each key must be unique. For more information, see `Tagging AWS resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in the *AWS General Reference Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-filesystemtags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="fileSystemPolicy")
    def file_system_policy(self) -> typing.Any:
        '''The ``FileSystemPolicy`` for the EFS file system.

        A file system policy is an IAM resource policy used to control NFS access to an EFS file system. For more information, see `Using IAM to control NFS access to Amazon EFS <https://docs.aws.amazon.com/efs/latest/ug/iam-access-control-nfs-efs.html>`_ in the *Amazon EFS User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-filesystempolicy
        '''
        return typing.cast(typing.Any, jsii.get(self, "fileSystemPolicy"))

    @file_system_policy.setter
    def file_system_policy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc32f07cb33878a98c83197764127a5caacf2475eaf82c2c75ca8cd0757f33b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileSystemPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneName")
    def availability_zone_name(self) -> typing.Optional[builtins.str]:
        '''Used to create a file system that uses One Zone storage classes.

        It specifies the AWS Availability Zone in which to create the file system. Use the format ``us-east-1a`` to specify the Availability Zone. For more information about One Zone storage classes, see `Using EFS storage classes <https://docs.aws.amazon.com/efs/latest/ug/storage-classes.html>`_ in the *Amazon EFS User Guide* .
        .. epigraph::

           One Zone storage classes are not available in all Availability Zones in AWS Regions where Amazon EFS is available.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-availabilityzonename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneName"))

    @availability_zone_name.setter
    def availability_zone_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__786daabc2f260621ca464ff65d790b18858ee0dc673d17c46535da8c414b5f51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZoneName", value)

    @builtins.property
    @jsii.member(jsii_name="backupPolicy")
    def backup_policy(
        self,
    ) -> typing.Optional[typing.Union["CfnFileSystem.BackupPolicyProperty", _IResolvable_a771d0ef]]:
        '''Use the ``BackupPolicy`` to turn automatic backups on or off for the file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-backuppolicy
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFileSystem.BackupPolicyProperty", _IResolvable_a771d0ef]], jsii.get(self, "backupPolicy"))

    @backup_policy.setter
    def backup_policy(
        self,
        value: typing.Optional[typing.Union["CfnFileSystem.BackupPolicyProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__822ae90bc3dea0639f23b489fb6613c1b93b82d8243e044cfd9fdcc9b9da702d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="bypassPolicyLockoutSafetyCheck")
    def bypass_policy_lockout_safety_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''(Optional) A boolean that specifies whether or not to bypass the ``FileSystemPolicy`` lockout safety check.

        The lockout safety check determines whether the policy in the request will lock out, or prevent, the IAM principal that is making the request from making future ``PutFileSystemPolicy`` requests on this file system. Set ``BypassPolicyLockoutSafetyCheck`` to ``True`` only when you intend to prevent the IAM principal that is making the request from making subsequent ``PutFileSystemPolicy`` requests on this file system. The default value is ``False`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-bypasspolicylockoutsafetycheck
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "bypassPolicyLockoutSafetyCheck"))

    @bypass_policy_lockout_safety_check.setter
    def bypass_policy_lockout_safety_check(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69843bd15ad8c783de034d9088b85ff53e08b7f8bc5ae96dbf598e3eae056e52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bypassPolicyLockoutSafetyCheck", value)

    @builtins.property
    @jsii.member(jsii_name="encrypted")
    def encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A Boolean value that, if true, creates an encrypted file system.

        When creating an encrypted file system, you have the option of specifying a KmsKeyId for an existing AWS KMS key . If you don't specify a KMS key , then the default KMS key for Amazon EFS , ``/aws/elasticfilesystem`` , is used to protect the encrypted file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-encrypted
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "encrypted"))

    @encrypted.setter
    def encrypted(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb986bd8841c04e164ded7be1170526ec0b99894c44484ffc5338c9bfe1e0b4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encrypted", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the AWS KMS key to be used to protect the encrypted file system.

        This parameter is only required if you want to use a nondefault KMS key . If this parameter is not specified, the default KMS key for Amazon EFS is used. This ID can be in one of the following formats:

        - Key ID - A unique identifier of the key, for example ``1234abcd-12ab-34cd-56ef-1234567890ab`` .
        - ARN - An Amazon Resource Name (ARN) for the key, for example ``arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` .
        - Key alias - A previously created display name for a key, for example ``alias/projectKey1`` .
        - Key alias ARN - An ARN for a key alias, for example ``arn:aws:kms:us-west-2:444455556666:alias/projectKey1`` .

        If ``KmsKeyId`` is specified, the ``Encrypted`` parameter must be set to true.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c803f81a2309c5265fa2b1ebef94fda0b79d1b33d949d75e64990289f14302)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="lifecyclePolicies")
    def lifecycle_policies(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFileSystem.LifecyclePolicyProperty", _IResolvable_a771d0ef]]]]:
        '''An array of ``LifecyclePolicy`` objects that define the file system's ``LifecycleConfiguration`` object.

        A ``LifecycleConfiguration`` object informs EFS lifecycle management and intelligent tiering of the following:

        - When to move files in the file system from primary storage to the IA storage class.
        - When to move files that are in IA storage to primary storage.

        .. epigraph::

           Amazon EFS requires that each ``LifecyclePolicy`` object have only a single transition. This means that in a request body, ``LifecyclePolicies`` needs to be structured as an array of ``LifecyclePolicy`` objects, one object for each transition, ``TransitionToIA`` , ``TransitionToPrimaryStorageClass`` . See the example requests in the following section for more information.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-lifecyclepolicies
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFileSystem.LifecyclePolicyProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "lifecyclePolicies"))

    @lifecycle_policies.setter
    def lifecycle_policies(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFileSystem.LifecyclePolicyProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3002ad338eb254fa6d0b293d30d2359d4fd9638312f95d1319b3a4b4d4b49226)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecyclePolicies", value)

    @builtins.property
    @jsii.member(jsii_name="performanceMode")
    def performance_mode(self) -> typing.Optional[builtins.str]:
        '''The performance mode of the file system.

        We recommend ``generalPurpose`` performance mode for most file systems. File systems using the ``maxIO`` performance mode can scale to higher levels of aggregate throughput and operations per second with a tradeoff of slightly higher latencies for most file operations. The performance mode can't be changed after the file system has been created.
        .. epigraph::

           The ``maxIO`` mode is not supported on file systems using One Zone storage classes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-performancemode
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "performanceMode"))

    @performance_mode.setter
    def performance_mode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a91d33319b31091e69dd52610642caee420496f1877b83937fc4f3fc4dcf1ee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "performanceMode", value)

    @builtins.property
    @jsii.member(jsii_name="provisionedThroughputInMibps")
    def provisioned_throughput_in_mibps(self) -> typing.Optional[jsii.Number]:
        '''The throughput, measured in MiB/s, that you want to provision for a file system that you're creating.

        Valid values are 1-1024. Required if ``ThroughputMode`` is set to ``provisioned`` . The upper limit for throughput is 1024 MiB/s. To increase this limit, contact AWS Support . For more information, see `Amazon EFS quotas that you can increase <https://docs.aws.amazon.com/efs/latest/ug/limits.html#soft-limits>`_ in the *Amazon EFS User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-provisionedthroughputinmibps
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "provisionedThroughputInMibps"))

    @provisioned_throughput_in_mibps.setter
    def provisioned_throughput_in_mibps(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8df260ee49d07c86ded8349f56072a5d18b5d0909afbcbd65af0bb6fdd75f518)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedThroughputInMibps", value)

    @builtins.property
    @jsii.member(jsii_name="throughputMode")
    def throughput_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies the throughput mode for the file system.

        The mode can be ``bursting`` , ``provisioned`` , or ``elastic`` . If you set ``ThroughputMode`` to ``provisioned`` , you must also set a value for ``ProvisionedThroughputInMibps`` . After you create the file system, you can decrease your file system's throughput in Provisioned Throughput mode or change between the throughput modes, with certain time restrictions. For more information, see `Specifying throughput with provisioned mode <https://docs.aws.amazon.com/efs/latest/ug/performance.html#provisioned-throughput>`_ in the *Amazon EFS User Guide* .

        Default is ``bursting`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-throughputmode
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "throughputMode"))

    @throughput_mode.setter
    def throughput_mode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78d1b54c4227c2be55780451e0a8ccf0a8b7e01f754919c53166a8ab4294b63b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throughputMode", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_efs.CfnFileSystem.BackupPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status"},
    )
    class BackupPolicyProperty:
        def __init__(self, *, status: builtins.str) -> None:
            '''The backup policy turns automatic backups for the file system on or off.

            :param status: Set the backup policy status for the file system. - *``ENABLED``* - Turns automatic backups on for the file system. - *``DISABLED``* - Turns automatic backups off for the file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-backuppolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_efs as efs
                
                backup_policy_property = efs.CfnFileSystem.BackupPolicyProperty(
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4497d90fea9873f99722ce59e614a8e0bca03493cafe7cc72dbb6d4344b7866f)
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "status": status,
            }

        @builtins.property
        def status(self) -> builtins.str:
            '''Set the backup policy status for the file system.

            - *``ENABLED``* - Turns automatic backups on for the file system.
            - *``DISABLED``* - Turns automatic backups off for the file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-backuppolicy.html#cfn-efs-filesystem-backuppolicy-status
            '''
            result = self._values.get("status")
            assert result is not None, "Required property 'status' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BackupPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_efs.CfnFileSystem.ElasticFileSystemTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ElasticFileSystemTagProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''A tag is a key-value pair attached to a file system.

            Allowed characters in the ``Key`` and ``Value`` properties are letters, white space, and numbers that can be represented in UTF-8, and the following characters: ``+ - = . _ : /``

            :param key: The tag key (String). The key can't start with ``aws:`` .
            :param value: The value of the tag key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-elasticfilesystemtag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_efs as efs
                
                elastic_file_system_tag_property = efs.CfnFileSystem.ElasticFileSystemTagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b07cec98f984f384f7cc5799e97aa57d998b7b08acefcef7ba0b9c4edcf56644)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''The tag key (String).

            The key can't start with ``aws:`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-elasticfilesystemtag.html#cfn-efs-filesystem-elasticfilesystemtag-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The value of the tag key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-elasticfilesystemtag.html#cfn-efs-filesystem-elasticfilesystemtag-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ElasticFileSystemTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_efs.CfnFileSystem.LifecyclePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "transition_to_ia": "transitionToIa",
            "transition_to_primary_storage_class": "transitionToPrimaryStorageClass",
        },
    )
    class LifecyclePolicyProperty:
        def __init__(
            self,
            *,
            transition_to_ia: typing.Optional[builtins.str] = None,
            transition_to_primary_storage_class: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a policy used by EFS lifecycle management and EFS Intelligent-Tiering that specifies when to transition files into and out of the file system's Infrequent Access (IA) storage class.

            For more information, see `EFS Intelligent‐Tiering and EFS Lifecycle Management <https://docs.aws.amazon.com/efs/latest/ug/lifecycle-management-efs.html>`_ .
            .. epigraph::

               - Each ``LifecyclePolicy`` object can have only a single transition. This means that in a request body, ``LifecyclePolicies`` must be structured as an array of ``LifecyclePolicy`` objects, one object for each transition, ``TransitionToIA`` , ``TransitionToPrimaryStorageClass`` .
               - See the AWS::EFS::FileSystem examples for the correct ``LifecyclePolicy`` structure. Do not use the syntax shown on this page.

            :param transition_to_ia: Describes the period of time that a file is not accessed, after which it transitions to IA storage. Metadata operations such as listing the contents of a directory don't count as file access events.
            :param transition_to_primary_storage_class: Describes when to transition a file from IA storage to primary storage. Metadata operations such as listing the contents of a directory don't count as file access events.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-lifecyclepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_efs as efs
                
                lifecycle_policy_property = efs.CfnFileSystem.LifecyclePolicyProperty(
                    transition_to_ia="transitionToIa",
                    transition_to_primary_storage_class="transitionToPrimaryStorageClass"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__77dd394973e6bb6d12ea785565784eaf5876a316fc2022ba37d951c5e99e983c)
                check_type(argname="argument transition_to_ia", value=transition_to_ia, expected_type=type_hints["transition_to_ia"])
                check_type(argname="argument transition_to_primary_storage_class", value=transition_to_primary_storage_class, expected_type=type_hints["transition_to_primary_storage_class"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if transition_to_ia is not None:
                self._values["transition_to_ia"] = transition_to_ia
            if transition_to_primary_storage_class is not None:
                self._values["transition_to_primary_storage_class"] = transition_to_primary_storage_class

        @builtins.property
        def transition_to_ia(self) -> typing.Optional[builtins.str]:
            '''Describes the period of time that a file is not accessed, after which it transitions to IA storage.

            Metadata operations such as listing the contents of a directory don't count as file access events.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-lifecyclepolicy.html#cfn-efs-filesystem-lifecyclepolicy-transitiontoia
            '''
            result = self._values.get("transition_to_ia")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def transition_to_primary_storage_class(self) -> typing.Optional[builtins.str]:
            '''Describes when to transition a file from IA storage to primary storage.

            Metadata operations such as listing the contents of a directory don't count as file access events.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-lifecyclepolicy.html#cfn-efs-filesystem-lifecyclepolicy-transitiontoprimarystorageclass
            '''
            result = self._values.get("transition_to_primary_storage_class")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LifecyclePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_efs.CfnFileSystemProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone_name": "availabilityZoneName",
        "backup_policy": "backupPolicy",
        "bypass_policy_lockout_safety_check": "bypassPolicyLockoutSafetyCheck",
        "encrypted": "encrypted",
        "file_system_policy": "fileSystemPolicy",
        "file_system_tags": "fileSystemTags",
        "kms_key_id": "kmsKeyId",
        "lifecycle_policies": "lifecyclePolicies",
        "performance_mode": "performanceMode",
        "provisioned_throughput_in_mibps": "provisionedThroughputInMibps",
        "throughput_mode": "throughputMode",
    },
)
class CfnFileSystemProps:
    def __init__(
        self,
        *,
        availability_zone_name: typing.Optional[builtins.str] = None,
        backup_policy: typing.Optional[typing.Union[typing.Union[CfnFileSystem.BackupPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        bypass_policy_lockout_safety_check: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        encrypted: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        file_system_policy: typing.Any = None,
        file_system_tags: typing.Optional[typing.Sequence[typing.Union[CfnFileSystem.ElasticFileSystemTagProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        lifecycle_policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFileSystem.LifecyclePolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        performance_mode: typing.Optional[builtins.str] = None,
        provisioned_throughput_in_mibps: typing.Optional[jsii.Number] = None,
        throughput_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnFileSystem``.

        :param availability_zone_name: Used to create a file system that uses One Zone storage classes. It specifies the AWS Availability Zone in which to create the file system. Use the format ``us-east-1a`` to specify the Availability Zone. For more information about One Zone storage classes, see `Using EFS storage classes <https://docs.aws.amazon.com/efs/latest/ug/storage-classes.html>`_ in the *Amazon EFS User Guide* . .. epigraph:: One Zone storage classes are not available in all Availability Zones in AWS Regions where Amazon EFS is available.
        :param backup_policy: Use the ``BackupPolicy`` to turn automatic backups on or off for the file system.
        :param bypass_policy_lockout_safety_check: (Optional) A boolean that specifies whether or not to bypass the ``FileSystemPolicy`` lockout safety check. The lockout safety check determines whether the policy in the request will lock out, or prevent, the IAM principal that is making the request from making future ``PutFileSystemPolicy`` requests on this file system. Set ``BypassPolicyLockoutSafetyCheck`` to ``True`` only when you intend to prevent the IAM principal that is making the request from making subsequent ``PutFileSystemPolicy`` requests on this file system. The default value is ``False`` .
        :param encrypted: A Boolean value that, if true, creates an encrypted file system. When creating an encrypted file system, you have the option of specifying a KmsKeyId for an existing AWS KMS key . If you don't specify a KMS key , then the default KMS key for Amazon EFS , ``/aws/elasticfilesystem`` , is used to protect the encrypted file system.
        :param file_system_policy: The ``FileSystemPolicy`` for the EFS file system. A file system policy is an IAM resource policy used to control NFS access to an EFS file system. For more information, see `Using IAM to control NFS access to Amazon EFS <https://docs.aws.amazon.com/efs/latest/ug/iam-access-control-nfs-efs.html>`_ in the *Amazon EFS User Guide* .
        :param file_system_tags: Use to create one or more tags associated with the file system. Each tag is a user-defined key-value pair. Name your file system on creation by including a ``"Key":"Name","Value":"{value}"`` key-value pair. Each key must be unique. For more information, see `Tagging AWS resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in the *AWS General Reference Guide* .
        :param kms_key_id: The ID of the AWS KMS key to be used to protect the encrypted file system. This parameter is only required if you want to use a nondefault KMS key . If this parameter is not specified, the default KMS key for Amazon EFS is used. This ID can be in one of the following formats: - Key ID - A unique identifier of the key, for example ``1234abcd-12ab-34cd-56ef-1234567890ab`` . - ARN - An Amazon Resource Name (ARN) for the key, for example ``arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` . - Key alias - A previously created display name for a key, for example ``alias/projectKey1`` . - Key alias ARN - An ARN for a key alias, for example ``arn:aws:kms:us-west-2:444455556666:alias/projectKey1`` . If ``KmsKeyId`` is specified, the ``Encrypted`` parameter must be set to true.
        :param lifecycle_policies: An array of ``LifecyclePolicy`` objects that define the file system's ``LifecycleConfiguration`` object. A ``LifecycleConfiguration`` object informs EFS lifecycle management and intelligent tiering of the following: - When to move files in the file system from primary storage to the IA storage class. - When to move files that are in IA storage to primary storage. .. epigraph:: Amazon EFS requires that each ``LifecyclePolicy`` object have only a single transition. This means that in a request body, ``LifecyclePolicies`` needs to be structured as an array of ``LifecyclePolicy`` objects, one object for each transition, ``TransitionToIA`` , ``TransitionToPrimaryStorageClass`` . See the example requests in the following section for more information.
        :param performance_mode: The performance mode of the file system. We recommend ``generalPurpose`` performance mode for most file systems. File systems using the ``maxIO`` performance mode can scale to higher levels of aggregate throughput and operations per second with a tradeoff of slightly higher latencies for most file operations. The performance mode can't be changed after the file system has been created. .. epigraph:: The ``maxIO`` mode is not supported on file systems using One Zone storage classes.
        :param provisioned_throughput_in_mibps: The throughput, measured in MiB/s, that you want to provision for a file system that you're creating. Valid values are 1-1024. Required if ``ThroughputMode`` is set to ``provisioned`` . The upper limit for throughput is 1024 MiB/s. To increase this limit, contact AWS Support . For more information, see `Amazon EFS quotas that you can increase <https://docs.aws.amazon.com/efs/latest/ug/limits.html#soft-limits>`_ in the *Amazon EFS User Guide* .
        :param throughput_mode: Specifies the throughput mode for the file system. The mode can be ``bursting`` , ``provisioned`` , or ``elastic`` . If you set ``ThroughputMode`` to ``provisioned`` , you must also set a value for ``ProvisionedThroughputInMibps`` . After you create the file system, you can decrease your file system's throughput in Provisioned Throughput mode or change between the throughput modes, with certain time restrictions. For more information, see `Specifying throughput with provisioned mode <https://docs.aws.amazon.com/efs/latest/ug/performance.html#provisioned-throughput>`_ in the *Amazon EFS User Guide* . Default is ``bursting`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_efs as efs
            
            # file_system_policy: Any
            
            cfn_file_system_props = efs.CfnFileSystemProps(
                availability_zone_name="availabilityZoneName",
                backup_policy=efs.CfnFileSystem.BackupPolicyProperty(
                    status="status"
                ),
                bypass_policy_lockout_safety_check=False,
                encrypted=False,
                file_system_policy=file_system_policy,
                file_system_tags=[efs.CfnFileSystem.ElasticFileSystemTagProperty(
                    key="key",
                    value="value"
                )],
                kms_key_id="kmsKeyId",
                lifecycle_policies=[efs.CfnFileSystem.LifecyclePolicyProperty(
                    transition_to_ia="transitionToIa",
                    transition_to_primary_storage_class="transitionToPrimaryStorageClass"
                )],
                performance_mode="performanceMode",
                provisioned_throughput_in_mibps=123,
                throughput_mode="throughputMode"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5022f30cdc0fc98689ac1ee8421efec19737b18b9e687c740277e6c4a6923689)
            check_type(argname="argument availability_zone_name", value=availability_zone_name, expected_type=type_hints["availability_zone_name"])
            check_type(argname="argument backup_policy", value=backup_policy, expected_type=type_hints["backup_policy"])
            check_type(argname="argument bypass_policy_lockout_safety_check", value=bypass_policy_lockout_safety_check, expected_type=type_hints["bypass_policy_lockout_safety_check"])
            check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
            check_type(argname="argument file_system_policy", value=file_system_policy, expected_type=type_hints["file_system_policy"])
            check_type(argname="argument file_system_tags", value=file_system_tags, expected_type=type_hints["file_system_tags"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument lifecycle_policies", value=lifecycle_policies, expected_type=type_hints["lifecycle_policies"])
            check_type(argname="argument performance_mode", value=performance_mode, expected_type=type_hints["performance_mode"])
            check_type(argname="argument provisioned_throughput_in_mibps", value=provisioned_throughput_in_mibps, expected_type=type_hints["provisioned_throughput_in_mibps"])
            check_type(argname="argument throughput_mode", value=throughput_mode, expected_type=type_hints["throughput_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zone_name is not None:
            self._values["availability_zone_name"] = availability_zone_name
        if backup_policy is not None:
            self._values["backup_policy"] = backup_policy
        if bypass_policy_lockout_safety_check is not None:
            self._values["bypass_policy_lockout_safety_check"] = bypass_policy_lockout_safety_check
        if encrypted is not None:
            self._values["encrypted"] = encrypted
        if file_system_policy is not None:
            self._values["file_system_policy"] = file_system_policy
        if file_system_tags is not None:
            self._values["file_system_tags"] = file_system_tags
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if lifecycle_policies is not None:
            self._values["lifecycle_policies"] = lifecycle_policies
        if performance_mode is not None:
            self._values["performance_mode"] = performance_mode
        if provisioned_throughput_in_mibps is not None:
            self._values["provisioned_throughput_in_mibps"] = provisioned_throughput_in_mibps
        if throughput_mode is not None:
            self._values["throughput_mode"] = throughput_mode

    @builtins.property
    def availability_zone_name(self) -> typing.Optional[builtins.str]:
        '''Used to create a file system that uses One Zone storage classes.

        It specifies the AWS Availability Zone in which to create the file system. Use the format ``us-east-1a`` to specify the Availability Zone. For more information about One Zone storage classes, see `Using EFS storage classes <https://docs.aws.amazon.com/efs/latest/ug/storage-classes.html>`_ in the *Amazon EFS User Guide* .
        .. epigraph::

           One Zone storage classes are not available in all Availability Zones in AWS Regions where Amazon EFS is available.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-availabilityzonename
        '''
        result = self._values.get("availability_zone_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_policy(
        self,
    ) -> typing.Optional[typing.Union[CfnFileSystem.BackupPolicyProperty, _IResolvable_a771d0ef]]:
        '''Use the ``BackupPolicy`` to turn automatic backups on or off for the file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-backuppolicy
        '''
        result = self._values.get("backup_policy")
        return typing.cast(typing.Optional[typing.Union[CfnFileSystem.BackupPolicyProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def bypass_policy_lockout_safety_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''(Optional) A boolean that specifies whether or not to bypass the ``FileSystemPolicy`` lockout safety check.

        The lockout safety check determines whether the policy in the request will lock out, or prevent, the IAM principal that is making the request from making future ``PutFileSystemPolicy`` requests on this file system. Set ``BypassPolicyLockoutSafetyCheck`` to ``True`` only when you intend to prevent the IAM principal that is making the request from making subsequent ``PutFileSystemPolicy`` requests on this file system. The default value is ``False`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-bypasspolicylockoutsafetycheck
        '''
        result = self._values.get("bypass_policy_lockout_safety_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A Boolean value that, if true, creates an encrypted file system.

        When creating an encrypted file system, you have the option of specifying a KmsKeyId for an existing AWS KMS key . If you don't specify a KMS key , then the default KMS key for Amazon EFS , ``/aws/elasticfilesystem`` , is used to protect the encrypted file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-encrypted
        '''
        result = self._values.get("encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def file_system_policy(self) -> typing.Any:
        '''The ``FileSystemPolicy`` for the EFS file system.

        A file system policy is an IAM resource policy used to control NFS access to an EFS file system. For more information, see `Using IAM to control NFS access to Amazon EFS <https://docs.aws.amazon.com/efs/latest/ug/iam-access-control-nfs-efs.html>`_ in the *Amazon EFS User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-filesystempolicy
        '''
        result = self._values.get("file_system_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def file_system_tags(
        self,
    ) -> typing.Optional[typing.List[CfnFileSystem.ElasticFileSystemTagProperty]]:
        '''Use to create one or more tags associated with the file system.

        Each tag is a user-defined key-value pair. Name your file system on creation by including a ``"Key":"Name","Value":"{value}"`` key-value pair. Each key must be unique. For more information, see `Tagging AWS resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in the *AWS General Reference Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-filesystemtags
        '''
        result = self._values.get("file_system_tags")
        return typing.cast(typing.Optional[typing.List[CfnFileSystem.ElasticFileSystemTagProperty]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the AWS KMS key to be used to protect the encrypted file system.

        This parameter is only required if you want to use a nondefault KMS key . If this parameter is not specified, the default KMS key for Amazon EFS is used. This ID can be in one of the following formats:

        - Key ID - A unique identifier of the key, for example ``1234abcd-12ab-34cd-56ef-1234567890ab`` .
        - ARN - An Amazon Resource Name (ARN) for the key, for example ``arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` .
        - Key alias - A previously created display name for a key, for example ``alias/projectKey1`` .
        - Key alias ARN - An ARN for a key alias, for example ``arn:aws:kms:us-west-2:444455556666:alias/projectKey1`` .

        If ``KmsKeyId`` is specified, the ``Encrypted`` parameter must be set to true.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_policies(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFileSystem.LifecyclePolicyProperty, _IResolvable_a771d0ef]]]]:
        '''An array of ``LifecyclePolicy`` objects that define the file system's ``LifecycleConfiguration`` object.

        A ``LifecycleConfiguration`` object informs EFS lifecycle management and intelligent tiering of the following:

        - When to move files in the file system from primary storage to the IA storage class.
        - When to move files that are in IA storage to primary storage.

        .. epigraph::

           Amazon EFS requires that each ``LifecyclePolicy`` object have only a single transition. This means that in a request body, ``LifecyclePolicies`` needs to be structured as an array of ``LifecyclePolicy`` objects, one object for each transition, ``TransitionToIA`` , ``TransitionToPrimaryStorageClass`` . See the example requests in the following section for more information.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-lifecyclepolicies
        '''
        result = self._values.get("lifecycle_policies")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFileSystem.LifecyclePolicyProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def performance_mode(self) -> typing.Optional[builtins.str]:
        '''The performance mode of the file system.

        We recommend ``generalPurpose`` performance mode for most file systems. File systems using the ``maxIO`` performance mode can scale to higher levels of aggregate throughput and operations per second with a tradeoff of slightly higher latencies for most file operations. The performance mode can't be changed after the file system has been created.
        .. epigraph::

           The ``maxIO`` mode is not supported on file systems using One Zone storage classes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-performancemode
        '''
        result = self._values.get("performance_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioned_throughput_in_mibps(self) -> typing.Optional[jsii.Number]:
        '''The throughput, measured in MiB/s, that you want to provision for a file system that you're creating.

        Valid values are 1-1024. Required if ``ThroughputMode`` is set to ``provisioned`` . The upper limit for throughput is 1024 MiB/s. To increase this limit, contact AWS Support . For more information, see `Amazon EFS quotas that you can increase <https://docs.aws.amazon.com/efs/latest/ug/limits.html#soft-limits>`_ in the *Amazon EFS User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-provisionedthroughputinmibps
        '''
        result = self._values.get("provisioned_throughput_in_mibps")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throughput_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies the throughput mode for the file system.

        The mode can be ``bursting`` , ``provisioned`` , or ``elastic`` . If you set ``ThroughputMode`` to ``provisioned`` , you must also set a value for ``ProvisionedThroughputInMibps`` . After you create the file system, you can decrease your file system's throughput in Provisioned Throughput mode or change between the throughput modes, with certain time restrictions. For more information, see `Specifying throughput with provisioned mode <https://docs.aws.amazon.com/efs/latest/ug/performance.html#provisioned-throughput>`_ in the *Amazon EFS User Guide* .

        Default is ``bursting`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-throughputmode
        '''
        result = self._values.get("throughput_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFileSystemProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnMountTarget(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_efs.CfnMountTarget",
):
    '''A CloudFormation ``AWS::EFS::MountTarget``.

    The ``AWS::EFS::MountTarget`` resource is an Amazon EFS resource that creates a mount target for an EFS file system. You can then mount the file system on Amazon EC2 instances or other resources by using the mount target.

    :cloudformationResource: AWS::EFS::MountTarget
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_efs as efs
        
        cfn_mount_target = efs.CfnMountTarget(self, "MyCfnMountTarget",
            file_system_id="fileSystemId",
            security_groups=["securityGroups"],
            subnet_id="subnetId",
        
            # the properties below are optional
            ip_address="ipAddress"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        file_system_id: builtins.str,
        security_groups: typing.Sequence[builtins.str],
        subnet_id: builtins.str,
        ip_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::EFS::MountTarget``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param file_system_id: The ID of the file system for which to create the mount target.
        :param security_groups: Up to five VPC security group IDs, of the form ``sg-xxxxxxxx`` . These must be for the same VPC as subnet specified.
        :param subnet_id: The ID of the subnet to add the mount target in. For file systems that use One Zone storage classes, use the subnet that is associated with the file system's Availability Zone.
        :param ip_address: Valid IPv4 address within the address range of the specified subnet.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dc9f3b59466c869ca74899702fe649aaff25f4a5470e1386ec05eda21609227)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMountTargetProps(
            file_system_id=file_system_id,
            security_groups=security_groups,
            subnet_id=subnet_id,
            ip_address=ip_address,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3e6a1cbb4916c04d8bd873bad82a044f6f565540f7e067511a9d0fb1f901c82)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9216740b6d2d959e668bdb98e05e03e5f5e9922b6fc6e2dbe1078ca7dd5b85e8)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the Amazon EFS file system that the mount target provides access to.

        Example: ``fs-0123456789111222a``

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrIpAddress")
    def attr_ip_address(self) -> builtins.str:
        '''The IPv4 address of the mount target.

        Example: 192.0.2.0

        :cloudformationAttribute: IpAddress
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> builtins.str:
        '''The ID of the file system for which to create the mount target.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-filesystemid
        '''
        return typing.cast(builtins.str, jsii.get(self, "fileSystemId"))

    @file_system_id.setter
    def file_system_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6ff86a9a5df33cb96a093da2c46a32f394226c4ebd09045578581781dc89b72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileSystemId", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[builtins.str]:
        '''Up to five VPC security group IDs, of the form ``sg-xxxxxxxx`` .

        These must be for the same VPC as subnet specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-securitygroups
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c445bb65e9b96da27b0d9f5fcc45da645f6b829b1322427fb9bb0ddb354387c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value)

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        '''The ID of the subnet to add the mount target in.

        For file systems that use One Zone storage classes, use the subnet that is associated with the file system's Availability Zone.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-subnetid
        '''
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80938068805d871ba4976b05a1f232bb8d0a7cf5d5660ef40cec3b9276214781)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''Valid IPv4 address within the address range of the specified subnet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-ipaddress
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__891a7b9d8842ad8534e3533479357ac2ada34875f781cb70fa04ddff531e8f70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value)


@jsii.data_type(
    jsii_type="monocdk.aws_efs.CfnMountTargetProps",
    jsii_struct_bases=[],
    name_mapping={
        "file_system_id": "fileSystemId",
        "security_groups": "securityGroups",
        "subnet_id": "subnetId",
        "ip_address": "ipAddress",
    },
)
class CfnMountTargetProps:
    def __init__(
        self,
        *,
        file_system_id: builtins.str,
        security_groups: typing.Sequence[builtins.str],
        subnet_id: builtins.str,
        ip_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnMountTarget``.

        :param file_system_id: The ID of the file system for which to create the mount target.
        :param security_groups: Up to five VPC security group IDs, of the form ``sg-xxxxxxxx`` . These must be for the same VPC as subnet specified.
        :param subnet_id: The ID of the subnet to add the mount target in. For file systems that use One Zone storage classes, use the subnet that is associated with the file system's Availability Zone.
        :param ip_address: Valid IPv4 address within the address range of the specified subnet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_efs as efs
            
            cfn_mount_target_props = efs.CfnMountTargetProps(
                file_system_id="fileSystemId",
                security_groups=["securityGroups"],
                subnet_id="subnetId",
            
                # the properties below are optional
                ip_address="ipAddress"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__365847ab0b4ae35d3f541ec9dffb2a0b5385b5af11bd1c71d5f15e36fe6d0d7d)
            check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file_system_id": file_system_id,
            "security_groups": security_groups,
            "subnet_id": subnet_id,
        }
        if ip_address is not None:
            self._values["ip_address"] = ip_address

    @builtins.property
    def file_system_id(self) -> builtins.str:
        '''The ID of the file system for which to create the mount target.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-filesystemid
        '''
        result = self._values.get("file_system_id")
        assert result is not None, "Required property 'file_system_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_groups(self) -> typing.List[builtins.str]:
        '''Up to five VPC security group IDs, of the form ``sg-xxxxxxxx`` .

        These must be for the same VPC as subnet specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-securitygroups
        '''
        result = self._values.get("security_groups")
        assert result is not None, "Required property 'security_groups' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''The ID of the subnet to add the mount target in.

        For file systems that use One Zone storage classes, use the subnet that is associated with the file system's Availability Zone.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-subnetid
        '''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''Valid IPv4 address within the address range of the specified subnet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-ipaddress
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMountTargetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_efs.FileSystemAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "security_group": "securityGroup",
        "file_system_arn": "fileSystemArn",
        "file_system_id": "fileSystemId",
    },
)
class FileSystemAttributes:
    def __init__(
        self,
        *,
        security_group: _ISecurityGroup_cdbba9d3,
        file_system_arn: typing.Optional[builtins.str] = None,
        file_system_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties that describe an existing EFS file system.

        :param security_group: (experimental) The security group of the file system.
        :param file_system_arn: (experimental) The File System's Arn. Default: - determined based on fileSystemId
        :param file_system_id: (experimental) The File System's ID. Default: - determined based on fileSystemArn

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as iam
            
            
            imported_file_system = efs.FileSystem.from_file_system_attributes(self, "existingFS",
                file_system_id="fs-12345678",  # You can also use fileSystemArn instead of fileSystemId.
                security_group=ec2.SecurityGroup.from_security_group_id(self, "SG", "sg-123456789",
                    allow_all_outbound=False
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a32c2b6d7c5663618c62bcebfa71d19a76889140b082358b765605f1e8d3b7f)
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument file_system_arn", value=file_system_arn, expected_type=type_hints["file_system_arn"])
            check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "security_group": security_group,
        }
        if file_system_arn is not None:
            self._values["file_system_arn"] = file_system_arn
        if file_system_id is not None:
            self._values["file_system_id"] = file_system_id

    @builtins.property
    def security_group(self) -> _ISecurityGroup_cdbba9d3:
        '''(experimental) The security group of the file system.

        :stability: experimental
        '''
        result = self._values.get("security_group")
        assert result is not None, "Required property 'security_group' is missing"
        return typing.cast(_ISecurityGroup_cdbba9d3, result)

    @builtins.property
    def file_system_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The File System's Arn.

        :default: - determined based on fileSystemId

        :stability: experimental
        '''
        result = self._values.get("file_system_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_system_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The File System's ID.

        :default: - determined based on fileSystemArn

        :stability: experimental
        '''
        result = self._values.get("file_system_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileSystemAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_efs.FileSystemProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "enable_automatic_backups": "enableAutomaticBackups",
        "encrypted": "encrypted",
        "file_system_name": "fileSystemName",
        "kms_key": "kmsKey",
        "lifecycle_policy": "lifecyclePolicy",
        "out_of_infrequent_access_policy": "outOfInfrequentAccessPolicy",
        "performance_mode": "performanceMode",
        "provisioned_throughput_per_second": "provisionedThroughputPerSecond",
        "removal_policy": "removalPolicy",
        "security_group": "securityGroup",
        "throughput_mode": "throughputMode",
        "vpc_subnets": "vpcSubnets",
    },
)
class FileSystemProps:
    def __init__(
        self,
        *,
        vpc: _IVpc_6d1f76c4,
        enable_automatic_backups: typing.Optional[builtins.bool] = None,
        encrypted: typing.Optional[builtins.bool] = None,
        file_system_name: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_IKey_36930160] = None,
        lifecycle_policy: typing.Optional["LifecyclePolicy"] = None,
        out_of_infrequent_access_policy: typing.Optional["OutOfInfrequentAccessPolicy"] = None,
        performance_mode: typing.Optional["PerformanceMode"] = None,
        provisioned_throughput_per_second: typing.Optional[_Size_7fbd4337] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
        throughput_mode: typing.Optional["ThroughputMode"] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties of EFS FileSystem.

        :param vpc: (experimental) VPC to launch the file system in.
        :param enable_automatic_backups: (experimental) Whether to enable automatic backups for the file system. Default: false
        :param encrypted: (experimental) Defines if the data at rest in the file system is encrypted or not. Default: - If your application has the '
        :param file_system_name: (experimental) The file system's name. Default: - CDK generated name
        :param kms_key: (experimental) The KMS key used for encryption. This is required to encrypt the data at rest if @encrypted is set to true. Default: - if 'encrypted' is true, the default key for EFS (/aws/elasticfilesystem) is used
        :param lifecycle_policy: (experimental) A policy used by EFS lifecycle management to transition files to the Infrequent Access (IA) storage class. Default: - None. EFS will not transition files to the IA storage class.
        :param out_of_infrequent_access_policy: (experimental) A policy used by EFS lifecycle management to transition files from Infrequent Access (IA) storage class to primary storage class. Default: - None. EFS will not transition files from IA storage to primary storage.
        :param performance_mode: (experimental) The performance mode that the file system will operate under. An Amazon EFS file system's performance mode can't be changed after the file system has been created. Updating this property will replace the file system. Default: PerformanceMode.GENERAL_PURPOSE
        :param provisioned_throughput_per_second: (experimental) Provisioned throughput for the file system. This is a required property if the throughput mode is set to PROVISIONED. Must be at least 1MiB/s. Default: - none, errors out
        :param removal_policy: (experimental) The removal policy to apply to the file system. Default: RemovalPolicy.RETAIN
        :param security_group: (experimental) Security Group to assign to this file system. Default: - creates new security group which allows all outbound traffic
        :param throughput_mode: (experimental) Enum to mention the throughput mode of the file system. Default: ThroughputMode.BURSTING
        :param vpc_subnets: (experimental) Which subnets to place the mount target in the VPC. Default: - the Vpc default strategy if not specified

        :stability: experimental
        :exampleMetadata: infused

        Example::

            file_system = efs.FileSystem(self, "MyEfsFileSystem",
                vpc=ec2.Vpc(self, "VPC"),
                lifecycle_policy=efs.LifecyclePolicy.AFTER_14_DAYS,  # files are not transitioned to infrequent access (IA) storage by default
                performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,  # default
                out_of_infrequent_access_policy=efs.OutOfInfrequentAccessPolicy.AFTER_1_ACCESS
            )
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_1284e62c(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b677fbb05149a7ebdc9a9fb627ba251c236e4b06c7eb65bc3345c1108858d456)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument enable_automatic_backups", value=enable_automatic_backups, expected_type=type_hints["enable_automatic_backups"])
            check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
            check_type(argname="argument file_system_name", value=file_system_name, expected_type=type_hints["file_system_name"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument lifecycle_policy", value=lifecycle_policy, expected_type=type_hints["lifecycle_policy"])
            check_type(argname="argument out_of_infrequent_access_policy", value=out_of_infrequent_access_policy, expected_type=type_hints["out_of_infrequent_access_policy"])
            check_type(argname="argument performance_mode", value=performance_mode, expected_type=type_hints["performance_mode"])
            check_type(argname="argument provisioned_throughput_per_second", value=provisioned_throughput_per_second, expected_type=type_hints["provisioned_throughput_per_second"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument throughput_mode", value=throughput_mode, expected_type=type_hints["throughput_mode"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if enable_automatic_backups is not None:
            self._values["enable_automatic_backups"] = enable_automatic_backups
        if encrypted is not None:
            self._values["encrypted"] = encrypted
        if file_system_name is not None:
            self._values["file_system_name"] = file_system_name
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if lifecycle_policy is not None:
            self._values["lifecycle_policy"] = lifecycle_policy
        if out_of_infrequent_access_policy is not None:
            self._values["out_of_infrequent_access_policy"] = out_of_infrequent_access_policy
        if performance_mode is not None:
            self._values["performance_mode"] = performance_mode
        if provisioned_throughput_per_second is not None:
            self._values["provisioned_throughput_per_second"] = provisioned_throughput_per_second
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if security_group is not None:
            self._values["security_group"] = security_group
        if throughput_mode is not None:
            self._values["throughput_mode"] = throughput_mode
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> _IVpc_6d1f76c4:
        '''(experimental) VPC to launch the file system in.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_IVpc_6d1f76c4, result)

    @builtins.property
    def enable_automatic_backups(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable automatic backups for the file system.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("enable_automatic_backups")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encrypted(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Defines if the data at rest in the file system is encrypted or not.

        :default: - If your application has the '

        :stability: experimental
        :aws-cdk: /aws-efs:defaultEncryptionAtRest' feature flag set, the default is true, otherwise, the default is false.
        :link: https://docs.aws.amazon.com/cdk/latest/guide/featureflags.html
        '''
        result = self._values.get("encrypted")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def file_system_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The file system's name.

        :default: - CDK generated name

        :stability: experimental
        '''
        result = self._values.get("file_system_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The KMS key used for encryption.

        This is required to encrypt the data at rest if @encrypted is set to true.

        :default: - if 'encrypted' is true, the default key for EFS (/aws/elasticfilesystem) is used

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def lifecycle_policy(self) -> typing.Optional["LifecyclePolicy"]:
        '''(experimental) A policy used by EFS lifecycle management to transition files to the Infrequent Access (IA) storage class.

        :default: - None. EFS will not transition files to the IA storage class.

        :stability: experimental
        '''
        result = self._values.get("lifecycle_policy")
        return typing.cast(typing.Optional["LifecyclePolicy"], result)

    @builtins.property
    def out_of_infrequent_access_policy(
        self,
    ) -> typing.Optional["OutOfInfrequentAccessPolicy"]:
        '''(experimental) A policy used by EFS lifecycle management to transition files from Infrequent Access (IA) storage class to primary storage class.

        :default: - None. EFS will not transition files from IA storage to primary storage.

        :stability: experimental
        '''
        result = self._values.get("out_of_infrequent_access_policy")
        return typing.cast(typing.Optional["OutOfInfrequentAccessPolicy"], result)

    @builtins.property
    def performance_mode(self) -> typing.Optional["PerformanceMode"]:
        '''(experimental) The performance mode that the file system will operate under.

        An Amazon EFS file system's performance mode can't be changed after the file system has been created.
        Updating this property will replace the file system.

        :default: PerformanceMode.GENERAL_PURPOSE

        :stability: experimental
        '''
        result = self._values.get("performance_mode")
        return typing.cast(typing.Optional["PerformanceMode"], result)

    @builtins.property
    def provisioned_throughput_per_second(self) -> typing.Optional[_Size_7fbd4337]:
        '''(experimental) Provisioned throughput for the file system.

        This is a required property if the throughput mode is set to PROVISIONED.
        Must be at least 1MiB/s.

        :default: - none, errors out

        :stability: experimental
        '''
        result = self._values.get("provisioned_throughput_per_second")
        return typing.cast(typing.Optional[_Size_7fbd4337], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) The removal policy to apply to the file system.

        :default: RemovalPolicy.RETAIN

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_cdbba9d3]:
        '''(experimental) Security Group to assign to this file system.

        :default: - creates new security group which allows all outbound traffic

        :stability: experimental
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_ISecurityGroup_cdbba9d3], result)

    @builtins.property
    def throughput_mode(self) -> typing.Optional["ThroughputMode"]:
        '''(experimental) Enum to mention the throughput mode of the file system.

        :default: ThroughputMode.BURSTING

        :stability: experimental
        '''
        result = self._values.get("throughput_mode")
        return typing.cast(typing.Optional["ThroughputMode"], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) Which subnets to place the mount target in the VPC.

        :default: - the Vpc default strategy if not specified

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileSystemProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_efs.IAccessPoint")
class IAccessPoint(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Represents an EFS AccessPoint.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="accessPointArn")
    def access_point_arn(self) -> builtins.str:
        '''(experimental) The ARN of the AccessPoint.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="accessPointId")
    def access_point_id(self) -> builtins.str:
        '''(experimental) The ID of the AccessPoint.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="fileSystem")
    def file_system(self) -> "IFileSystem":
        '''(experimental) The EFS file system.

        :stability: experimental
        '''
        ...


class _IAccessPointProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) Represents an EFS AccessPoint.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_efs.IAccessPoint"

    @builtins.property
    @jsii.member(jsii_name="accessPointArn")
    def access_point_arn(self) -> builtins.str:
        '''(experimental) The ARN of the AccessPoint.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "accessPointArn"))

    @builtins.property
    @jsii.member(jsii_name="accessPointId")
    def access_point_id(self) -> builtins.str:
        '''(experimental) The ID of the AccessPoint.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "accessPointId"))

    @builtins.property
    @jsii.member(jsii_name="fileSystem")
    def file_system(self) -> "IFileSystem":
        '''(experimental) The EFS file system.

        :stability: experimental
        '''
        return typing.cast("IFileSystem", jsii.get(self, "fileSystem"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAccessPoint).__jsii_proxy_class__ = lambda : _IAccessPointProxy


@jsii.interface(jsii_type="monocdk.aws_efs.IFileSystem")
class IFileSystem(
    _IConnectable_c1c0e72c,
    _IResource_8c1dbbbd,
    typing_extensions.Protocol,
):
    '''(experimental) Represents an Amazon EFS file system.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="fileSystemArn")
    def file_system_arn(self) -> builtins.str:
        '''(experimental) The ARN of the file system.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> builtins.str:
        '''(experimental) The ID of the file system, assigned by Amazon EFS.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="mountTargetsAvailable")
    def mount_targets_available(self) -> _IDependable_1175c9f7:
        '''(experimental) Dependable that can be depended upon to ensure the mount targets of the filesystem are ready.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the actions defined in actions to the given grantee on this File System resource.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        ...


class _IFileSystemProxy(
    jsii.proxy_for(_IConnectable_c1c0e72c), # type: ignore[misc]
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) Represents an Amazon EFS file system.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_efs.IFileSystem"

    @builtins.property
    @jsii.member(jsii_name="fileSystemArn")
    def file_system_arn(self) -> builtins.str:
        '''(experimental) The ARN of the file system.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "fileSystemArn"))

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> builtins.str:
        '''(experimental) The ID of the file system, assigned by Amazon EFS.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "fileSystemId"))

    @builtins.property
    @jsii.member(jsii_name="mountTargetsAvailable")
    def mount_targets_available(self) -> _IDependable_1175c9f7:
        '''(experimental) Dependable that can be depended upon to ensure the mount targets of the filesystem are ready.

        :stability: experimental
        '''
        return typing.cast(_IDependable_1175c9f7, jsii.get(self, "mountTargetsAvailable"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the actions defined in actions to the given grantee on this File System resource.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ece5ed399573018da8f2dea2bd92e7b6dc2c8d65e0cc5c380d3374862eb1f023)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grant", [grantee, *actions]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFileSystem).__jsii_proxy_class__ = lambda : _IFileSystemProxy


@jsii.enum(jsii_type="monocdk.aws_efs.LifecyclePolicy")
class LifecyclePolicy(enum.Enum):
    '''(experimental) EFS Lifecycle Policy, if a file is not accessed for given days, it will move to EFS Infrequent Access.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-elasticfilesystem-filesystem-lifecyclepolicies
    :stability: experimental
    :exampleMetadata: infused

    Example::

        file_system = efs.FileSystem(self, "MyEfsFileSystem",
            vpc=ec2.Vpc(self, "VPC"),
            lifecycle_policy=efs.LifecyclePolicy.AFTER_14_DAYS,  # files are not transitioned to infrequent access (IA) storage by default
            performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,  # default
            out_of_infrequent_access_policy=efs.OutOfInfrequentAccessPolicy.AFTER_1_ACCESS
        )
    '''

    AFTER_7_DAYS = "AFTER_7_DAYS"
    '''(experimental) After 7 days of not being accessed.

    :stability: experimental
    '''
    AFTER_14_DAYS = "AFTER_14_DAYS"
    '''(experimental) After 14 days of not being accessed.

    :stability: experimental
    '''
    AFTER_30_DAYS = "AFTER_30_DAYS"
    '''(experimental) After 30 days of not being accessed.

    :stability: experimental
    '''
    AFTER_60_DAYS = "AFTER_60_DAYS"
    '''(experimental) After 60 days of not being accessed.

    :stability: experimental
    '''
    AFTER_90_DAYS = "AFTER_90_DAYS"
    '''(experimental) After 90 days of not being accessed.

    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.aws_efs.OutOfInfrequentAccessPolicy")
class OutOfInfrequentAccessPolicy(enum.Enum):
    '''(experimental) EFS Out Of Infrequent Access Policy, if a file is accessed given times, it will move back to primary storage class.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-lifecyclepolicy.html#cfn-efs-filesystem-lifecyclepolicy-transitiontoprimarystorageclass
    :stability: experimental
    :exampleMetadata: infused

    Example::

        file_system = efs.FileSystem(self, "MyEfsFileSystem",
            vpc=ec2.Vpc(self, "VPC"),
            lifecycle_policy=efs.LifecyclePolicy.AFTER_14_DAYS,  # files are not transitioned to infrequent access (IA) storage by default
            performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,  # default
            out_of_infrequent_access_policy=efs.OutOfInfrequentAccessPolicy.AFTER_1_ACCESS
        )
    '''

    AFTER_1_ACCESS = "AFTER_1_ACCESS"
    '''(experimental) After 1 access.

    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.aws_efs.PerformanceMode")
class PerformanceMode(enum.Enum):
    '''(experimental) EFS Performance mode.

    :see: https://docs.aws.amazon.com/efs/latest/ug/performance.html#performancemodes
    :stability: experimental
    :exampleMetadata: infused

    Example::

        file_system = efs.FileSystem(self, "MyEfsFileSystem",
            vpc=ec2.Vpc(self, "VPC"),
            lifecycle_policy=efs.LifecyclePolicy.AFTER_14_DAYS,  # files are not transitioned to infrequent access (IA) storage by default
            performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,  # default
            out_of_infrequent_access_policy=efs.OutOfInfrequentAccessPolicy.AFTER_1_ACCESS
        )
    '''

    GENERAL_PURPOSE = "GENERAL_PURPOSE"
    '''(experimental) General Purpose is ideal for latency-sensitive use cases, like web serving environments, content management systems, home directories, and general file serving.

    Recommended for the majority of Amazon EFS file systems.

    :stability: experimental
    '''
    MAX_IO = "MAX_IO"
    '''(experimental) File systems in the Max I/O mode can scale to higher levels of aggregate throughput and operations per second.

    This scaling is done with a tradeoff
    of slightly higher latencies for file metadata operations.
    Highly parallelized applications and workloads, such as big data analysis,
    media processing, and genomics analysis, can benefit from this mode.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_efs.PosixUser",
    jsii_struct_bases=[],
    name_mapping={"gid": "gid", "uid": "uid", "secondary_gids": "secondaryGids"},
)
class PosixUser:
    def __init__(
        self,
        *,
        gid: builtins.str,
        uid: builtins.str,
        secondary_gids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Represents the PosixUser.

        :param gid: (experimental) The POSIX group ID used for all file system operations using this access point.
        :param uid: (experimental) The POSIX user ID used for all file system operations using this access point.
        :param secondary_gids: (experimental) Secondary POSIX group IDs used for all file system operations using this access point. Default: - None

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as ec2
            import monocdk as efs
            
            
            # create a new VPC
            vpc = ec2.Vpc(self, "VPC")
            
            # create a new Amazon EFS filesystem
            file_system = efs.FileSystem(self, "Efs", vpc=vpc)
            
            # create a new access point from the filesystem
            access_point = file_system.add_access_point("AccessPoint",
                # set /export/lambda as the root of the access point
                path="/export/lambda",
                # as /export/lambda does not exist in a new efs filesystem, the efs will create the directory with the following createAcl
                create_acl=ec2.aws_efs.Acl(
                    owner_uid="1001",
                    owner_gid="1001",
                    permissions="750"
                ),
                # enforce the POSIX identity so lambda function will access with this identity
                posix_user=ec2.aws_efs.PosixUser(
                    uid="1001",
                    gid="1001"
                )
            )
            
            fn = lambda_.Function(self, "MyLambda",
                # mount the access point to /mnt/msg in the lambda runtime environment
                filesystem=lambda_.FileSystem.from_efs_access_point(access_point, "/mnt/msg"),
                runtime=lambda_.Runtime.NODEJS_16_X,
                handler="index.handler",
                code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
                vpc=vpc
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b62cebca87e50fd4d0472365fe77cce1115937dfc4b475c5558f5852d64c74)
            check_type(argname="argument gid", value=gid, expected_type=type_hints["gid"])
            check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
            check_type(argname="argument secondary_gids", value=secondary_gids, expected_type=type_hints["secondary_gids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gid": gid,
            "uid": uid,
        }
        if secondary_gids is not None:
            self._values["secondary_gids"] = secondary_gids

    @builtins.property
    def gid(self) -> builtins.str:
        '''(experimental) The POSIX group ID used for all file system operations using this access point.

        :stability: experimental
        '''
        result = self._values.get("gid")
        assert result is not None, "Required property 'gid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uid(self) -> builtins.str:
        '''(experimental) The POSIX user ID used for all file system operations using this access point.

        :stability: experimental
        '''
        result = self._values.get("uid")
        assert result is not None, "Required property 'uid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secondary_gids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Secondary POSIX group IDs used for all file system operations using this access point.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("secondary_gids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PosixUser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_efs.ThroughputMode")
class ThroughputMode(enum.Enum):
    '''(experimental) EFS Throughput mode.

    :see: https://docs.aws.amazon.com/efs/latest/ug/performance.html#throughput-modes
    :stability: experimental
    '''

    BURSTING = "BURSTING"
    '''(experimental) This mode on Amazon EFS scales as the size of the file system in the standard storage class grows.

    :stability: experimental
    '''
    PROVISIONED = "PROVISIONED"
    '''(experimental) This mode can instantly provision the throughput of the file system (in MiB/s) independent of the amount of data stored.

    :stability: experimental
    '''


@jsii.implements(IAccessPoint)
class AccessPoint(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_efs.AccessPoint",
):
    '''(experimental) Represents the AccessPoint.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        efs.AccessPoint.from_access_point_attributes(self, "ap",
            access_point_id="fsap-1293c4d9832fo0912",
            file_system=efs.FileSystem.from_file_system_attributes(self, "efs",
                file_system_id="fs-099d3e2f",
                security_group=ec2.SecurityGroup.from_security_group_id(self, "sg", "sg-51530134")
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        file_system: IFileSystem,
        create_acl: typing.Optional[typing.Union[Acl, typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[builtins.str] = None,
        posix_user: typing.Optional[typing.Union[PosixUser, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param file_system: (experimental) The efs filesystem.
        :param create_acl: (experimental) Specifies the POSIX IDs and permissions to apply when creating the access point's root directory. If the root directory specified by ``path`` does not exist, EFS creates the root directory and applies the permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``. Default: - None. The directory specified by ``path`` must exist.
        :param path: (experimental) Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system. Default: '/'
        :param posix_user: (experimental) The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point. Specify this to enforce a user identity using an access point. Default: - user identity not enforced

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe851054b4e764116abc99b89c2e62292359007fb188fbbb4d2698272bb167f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AccessPointProps(
            file_system=file_system,
            create_acl=create_acl,
            path=path,
            posix_user=posix_user,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromAccessPointAttributes")
    @builtins.classmethod
    def from_access_point_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_point_arn: typing.Optional[builtins.str] = None,
        access_point_id: typing.Optional[builtins.str] = None,
        file_system: typing.Optional[IFileSystem] = None,
    ) -> IAccessPoint:
        '''(experimental) Import an existing Access Point by attributes.

        :param scope: -
        :param id: -
        :param access_point_arn: (experimental) The ARN of the AccessPoint One of this, or {@link accessPointId} is required. Default: - determined based on accessPointId
        :param access_point_id: (experimental) The ID of the AccessPoint One of this, or {@link accessPointArn} is required. Default: - determined based on accessPointArn
        :param file_system: (experimental) The EFS file system. Default: - no EFS file system

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e5a4fb7e576d35ccbe5bb21d0ce65020f89a63b9c75cfa0658c8ac25f6a728a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = AccessPointAttributes(
            access_point_arn=access_point_arn,
            access_point_id=access_point_id,
            file_system=file_system,
        )

        return typing.cast(IAccessPoint, jsii.sinvoke(cls, "fromAccessPointAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromAccessPointId")
    @builtins.classmethod
    def from_access_point_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        access_point_id: builtins.str,
    ) -> IAccessPoint:
        '''(experimental) Import an existing Access Point by id.

        :param scope: -
        :param id: -
        :param access_point_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__763e9bb073ac3f149e4c64c0b2c6e2389f651d255138ea6c724ae440ef61e7a8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument access_point_id", value=access_point_id, expected_type=type_hints["access_point_id"])
        return typing.cast(IAccessPoint, jsii.sinvoke(cls, "fromAccessPointId", [scope, id, access_point_id]))

    @builtins.property
    @jsii.member(jsii_name="accessPointArn")
    def access_point_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Access Point.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "accessPointArn"))

    @builtins.property
    @jsii.member(jsii_name="accessPointId")
    def access_point_id(self) -> builtins.str:
        '''(experimental) The ID of the Access Point.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "accessPointId"))

    @builtins.property
    @jsii.member(jsii_name="fileSystem")
    def file_system(self) -> IFileSystem:
        '''(experimental) The file system of the access point.

        :stability: experimental
        '''
        return typing.cast(IFileSystem, jsii.get(self, "fileSystem"))


@jsii.implements(IFileSystem)
class FileSystem(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_efs.FileSystem",
):
    '''(experimental) The Elastic File System implementation of IFileSystem.

    It creates a new, empty file system in Amazon Elastic File System (Amazon EFS).
    It also creates mount target (AWS::EFS::MountTarget) implicitly to mount the
    EFS file system on an Amazon Elastic Compute Cloud (Amazon EC2) instance or another resource.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html
    :stability: experimental
    :resource: AWS::EFS::FileSystem
    :exampleMetadata: infused

    Example::

        file_system = efs.FileSystem(self, "MyEfsFileSystem",
            vpc=ec2.Vpc(self, "VPC"),
            lifecycle_policy=efs.LifecyclePolicy.AFTER_14_DAYS,  # files are not transitioned to infrequent access (IA) storage by default
            performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,  # default
            out_of_infrequent_access_policy=efs.OutOfInfrequentAccessPolicy.AFTER_1_ACCESS
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc: _IVpc_6d1f76c4,
        enable_automatic_backups: typing.Optional[builtins.bool] = None,
        encrypted: typing.Optional[builtins.bool] = None,
        file_system_name: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_IKey_36930160] = None,
        lifecycle_policy: typing.Optional[LifecyclePolicy] = None,
        out_of_infrequent_access_policy: typing.Optional[OutOfInfrequentAccessPolicy] = None,
        performance_mode: typing.Optional[PerformanceMode] = None,
        provisioned_throughput_per_second: typing.Optional[_Size_7fbd4337] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
        throughput_mode: typing.Optional[ThroughputMode] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Constructor for creating a new EFS FileSystem.

        :param scope: -
        :param id: -
        :param vpc: (experimental) VPC to launch the file system in.
        :param enable_automatic_backups: (experimental) Whether to enable automatic backups for the file system. Default: false
        :param encrypted: (experimental) Defines if the data at rest in the file system is encrypted or not. Default: - If your application has the '
        :param file_system_name: (experimental) The file system's name. Default: - CDK generated name
        :param kms_key: (experimental) The KMS key used for encryption. This is required to encrypt the data at rest if @encrypted is set to true. Default: - if 'encrypted' is true, the default key for EFS (/aws/elasticfilesystem) is used
        :param lifecycle_policy: (experimental) A policy used by EFS lifecycle management to transition files to the Infrequent Access (IA) storage class. Default: - None. EFS will not transition files to the IA storage class.
        :param out_of_infrequent_access_policy: (experimental) A policy used by EFS lifecycle management to transition files from Infrequent Access (IA) storage class to primary storage class. Default: - None. EFS will not transition files from IA storage to primary storage.
        :param performance_mode: (experimental) The performance mode that the file system will operate under. An Amazon EFS file system's performance mode can't be changed after the file system has been created. Updating this property will replace the file system. Default: PerformanceMode.GENERAL_PURPOSE
        :param provisioned_throughput_per_second: (experimental) Provisioned throughput for the file system. This is a required property if the throughput mode is set to PROVISIONED. Must be at least 1MiB/s. Default: - none, errors out
        :param removal_policy: (experimental) The removal policy to apply to the file system. Default: RemovalPolicy.RETAIN
        :param security_group: (experimental) Security Group to assign to this file system. Default: - creates new security group which allows all outbound traffic
        :param throughput_mode: (experimental) Enum to mention the throughput mode of the file system. Default: ThroughputMode.BURSTING
        :param vpc_subnets: (experimental) Which subnets to place the mount target in the VPC. Default: - the Vpc default strategy if not specified

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b74d2e20d80386eeaa930f280b609ed4894d89297210d5c114907a709f443e2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FileSystemProps(
            vpc=vpc,
            enable_automatic_backups=enable_automatic_backups,
            encrypted=encrypted,
            file_system_name=file_system_name,
            kms_key=kms_key,
            lifecycle_policy=lifecycle_policy,
            out_of_infrequent_access_policy=out_of_infrequent_access_policy,
            performance_mode=performance_mode,
            provisioned_throughput_per_second=provisioned_throughput_per_second,
            removal_policy=removal_policy,
            security_group=security_group,
            throughput_mode=throughput_mode,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromFileSystemAttributes")
    @builtins.classmethod
    def from_file_system_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        security_group: _ISecurityGroup_cdbba9d3,
        file_system_arn: typing.Optional[builtins.str] = None,
        file_system_id: typing.Optional[builtins.str] = None,
    ) -> IFileSystem:
        '''(experimental) Import an existing File System from the given properties.

        :param scope: -
        :param id: -
        :param security_group: (experimental) The security group of the file system.
        :param file_system_arn: (experimental) The File System's Arn. Default: - determined based on fileSystemId
        :param file_system_id: (experimental) The File System's ID. Default: - determined based on fileSystemArn

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9acb6511c7b399dcbcfcd7906e9fc002e8a8f521c536099b19108fa41e9fad93)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = FileSystemAttributes(
            security_group=security_group,
            file_system_arn=file_system_arn,
            file_system_id=file_system_id,
        )

        return typing.cast(IFileSystem, jsii.sinvoke(cls, "fromFileSystemAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addAccessPoint")
    def add_access_point(
        self,
        id: builtins.str,
        *,
        create_acl: typing.Optional[typing.Union[Acl, typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[builtins.str] = None,
        posix_user: typing.Optional[typing.Union[PosixUser, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> AccessPoint:
        '''(experimental) create access point from this filesystem.

        :param id: -
        :param create_acl: (experimental) Specifies the POSIX IDs and permissions to apply when creating the access point's root directory. If the root directory specified by ``path`` does not exist, EFS creates the root directory and applies the permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``. Default: - None. The directory specified by ``path`` must exist.
        :param path: (experimental) Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system. Default: '/'
        :param posix_user: (experimental) The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point. Specify this to enforce a user identity using an access point. Default: - user identity not enforced

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7602c05b49aff5b39a57d74361c99930d883b17612fe278a3e6282147130a5c3)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        access_point_options = AccessPointOptions(
            create_acl=create_acl, path=path, posix_user=posix_user
        )

        return typing.cast(AccessPoint, jsii.invoke(self, "addAccessPoint", [id, access_point_options]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the actions defined in actions to the given grantee on this File System resource.

        :param grantee: Principal to grant right to.
        :param actions: The actions to grant.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0993e15d2297516b90689ad319904e8309cfde19a71ab95b0261b6d59a0005a2)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_PORT")
    def DEFAULT_PORT(cls) -> jsii.Number:
        '''(experimental) The default port File System listens on.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.sget(cls, "DEFAULT_PORT"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_57ccbda9:
        '''(experimental) The security groups/rules used to allow network connections to the file system.

        :stability: experimental
        '''
        return typing.cast(_Connections_57ccbda9, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="fileSystemArn")
    def file_system_arn(self) -> builtins.str:
        '''(experimental) The ARN of the file system.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "fileSystemArn"))

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> builtins.str:
        '''(experimental) The ID of the file system, assigned by Amazon EFS.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "fileSystemId"))

    @builtins.property
    @jsii.member(jsii_name="mountTargetsAvailable")
    def mount_targets_available(self) -> _IDependable_1175c9f7:
        '''(experimental) Dependable that can be depended upon to ensure the mount targets of the filesystem are ready.

        :stability: experimental
        '''
        return typing.cast(_IDependable_1175c9f7, jsii.get(self, "mountTargetsAvailable"))


__all__ = [
    "AccessPoint",
    "AccessPointAttributes",
    "AccessPointOptions",
    "AccessPointProps",
    "Acl",
    "CfnAccessPoint",
    "CfnAccessPointProps",
    "CfnFileSystem",
    "CfnFileSystemProps",
    "CfnMountTarget",
    "CfnMountTargetProps",
    "FileSystem",
    "FileSystemAttributes",
    "FileSystemProps",
    "IAccessPoint",
    "IFileSystem",
    "LifecyclePolicy",
    "OutOfInfrequentAccessPolicy",
    "PerformanceMode",
    "PosixUser",
    "ThroughputMode",
]

publication.publish()

def _typecheckingstub__bb4f45b836dd028aad10b6c18cd54bf762cee1b21fb7f4994881e33caefeb014(
    *,
    access_point_arn: typing.Optional[builtins.str] = None,
    access_point_id: typing.Optional[builtins.str] = None,
    file_system: typing.Optional[IFileSystem] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04457de26c72a8724950fa6ad7baa5e81e15f68681da1be8e840ca6382cd1d7a(
    *,
    create_acl: typing.Optional[typing.Union[Acl, typing.Dict[builtins.str, typing.Any]]] = None,
    path: typing.Optional[builtins.str] = None,
    posix_user: typing.Optional[typing.Union[PosixUser, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f87bd0ce42e43fe9db8139f1c4da324c8bf3aa43fe6b60ceef852c64dddb52b6(
    *,
    create_acl: typing.Optional[typing.Union[Acl, typing.Dict[builtins.str, typing.Any]]] = None,
    path: typing.Optional[builtins.str] = None,
    posix_user: typing.Optional[typing.Union[PosixUser, typing.Dict[builtins.str, typing.Any]]] = None,
    file_system: IFileSystem,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4f3c53a86c9e8103f4c9af8047128c63b714aac04d1cb324880a9f3ba1a738(
    *,
    owner_gid: builtins.str,
    owner_uid: builtins.str,
    permissions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f32c4a24917986082671fc977a5d82607d505538779b484916fb7848304135da(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    file_system_id: builtins.str,
    access_point_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAccessPoint.AccessPointTagProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    client_token: typing.Optional[builtins.str] = None,
    posix_user: typing.Optional[typing.Union[typing.Union[CfnAccessPoint.PosixUserProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    root_directory: typing.Optional[typing.Union[typing.Union[CfnAccessPoint.RootDirectoryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a5ad3bd290d125ca66755280ed34c773b967e49185628ad7a7cc8d3d62711a9(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7765f019eff1b33671948fbafb4285c7aa4f9eb7b667470c7e686c74016db257(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25759ba94eaa0f570ccbf7f9435279d13cb81cbe846f5d996e6ef11c79d713d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3205c38dcb273ae02e63aec1881ca0ff7ec5e4538dd8cd71a185c5d0a70984(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAccessPoint.AccessPointTagProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1703204e32c64998cc4da211cc0cbe9a7c56a8b8a45c593e5b8f053e641d4828(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a789f5efecfb6eaa71be9279197a92a00ccd4b5d1622cc1ed2ab0ebe31ef2590(
    value: typing.Optional[typing.Union[CfnAccessPoint.PosixUserProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed29aa5ab85ee8989982dce7208c403f2ac4b8399ead09548841451800a5271(
    value: typing.Optional[typing.Union[CfnAccessPoint.RootDirectoryProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bad9274deae6c8646b9dba6e6bc7b58ae3538fef4d545924742231085fc5b25(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a8cab115cb36e8085151ede3e5ae9f8d4421f293558cbdc9d7f0538e257e06(
    *,
    owner_gid: builtins.str,
    owner_uid: builtins.str,
    permissions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a11f23b12483ffa015eea74b622cc21f8d72f20f77491d7ed54c3ce6806bc5a(
    *,
    gid: builtins.str,
    uid: builtins.str,
    secondary_gids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf8917b2c4c52d1f6208de95be4ab891aa9739d9c41cb3c47cfb99167c157093(
    *,
    creation_info: typing.Optional[typing.Union[typing.Union[CfnAccessPoint.CreationInfoProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ab6a1017fd34b079bb62e6dd8bd5205d00f5ce5dbf46ad848bb3dfdce002aab(
    *,
    file_system_id: builtins.str,
    access_point_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAccessPoint.AccessPointTagProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    client_token: typing.Optional[builtins.str] = None,
    posix_user: typing.Optional[typing.Union[typing.Union[CfnAccessPoint.PosixUserProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    root_directory: typing.Optional[typing.Union[typing.Union[CfnAccessPoint.RootDirectoryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fbfdc5ac9791e193151a0e3604c198c382fdfe82e3c3a98f3c335354c952aee(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    availability_zone_name: typing.Optional[builtins.str] = None,
    backup_policy: typing.Optional[typing.Union[typing.Union[CfnFileSystem.BackupPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    bypass_policy_lockout_safety_check: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    encrypted: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    file_system_policy: typing.Any = None,
    file_system_tags: typing.Optional[typing.Sequence[typing.Union[CfnFileSystem.ElasticFileSystemTagProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    lifecycle_policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFileSystem.LifecyclePolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    performance_mode: typing.Optional[builtins.str] = None,
    provisioned_throughput_in_mibps: typing.Optional[jsii.Number] = None,
    throughput_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b113d15551cf887a56515a93c679210d6423cf76c7800ac8af9096c0b2159ad5(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530bfcf5954fc9512793028f1b1715d4b972629ce7a3551104a5071e2dc44052(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc32f07cb33878a98c83197764127a5caacf2475eaf82c2c75ca8cd0757f33b2(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__786daabc2f260621ca464ff65d790b18858ee0dc673d17c46535da8c414b5f51(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__822ae90bc3dea0639f23b489fb6613c1b93b82d8243e044cfd9fdcc9b9da702d(
    value: typing.Optional[typing.Union[CfnFileSystem.BackupPolicyProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69843bd15ad8c783de034d9088b85ff53e08b7f8bc5ae96dbf598e3eae056e52(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb986bd8841c04e164ded7be1170526ec0b99894c44484ffc5338c9bfe1e0b4b(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c803f81a2309c5265fa2b1ebef94fda0b79d1b33d949d75e64990289f14302(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3002ad338eb254fa6d0b293d30d2359d4fd9638312f95d1319b3a4b4d4b49226(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFileSystem.LifecyclePolicyProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a91d33319b31091e69dd52610642caee420496f1877b83937fc4f3fc4dcf1ee7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df260ee49d07c86ded8349f56072a5d18b5d0909afbcbd65af0bb6fdd75f518(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78d1b54c4227c2be55780451e0a8ccf0a8b7e01f754919c53166a8ab4294b63b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4497d90fea9873f99722ce59e614a8e0bca03493cafe7cc72dbb6d4344b7866f(
    *,
    status: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b07cec98f984f384f7cc5799e97aa57d998b7b08acefcef7ba0b9c4edcf56644(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77dd394973e6bb6d12ea785565784eaf5876a316fc2022ba37d951c5e99e983c(
    *,
    transition_to_ia: typing.Optional[builtins.str] = None,
    transition_to_primary_storage_class: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5022f30cdc0fc98689ac1ee8421efec19737b18b9e687c740277e6c4a6923689(
    *,
    availability_zone_name: typing.Optional[builtins.str] = None,
    backup_policy: typing.Optional[typing.Union[typing.Union[CfnFileSystem.BackupPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    bypass_policy_lockout_safety_check: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    encrypted: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    file_system_policy: typing.Any = None,
    file_system_tags: typing.Optional[typing.Sequence[typing.Union[CfnFileSystem.ElasticFileSystemTagProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    lifecycle_policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFileSystem.LifecyclePolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    performance_mode: typing.Optional[builtins.str] = None,
    provisioned_throughput_in_mibps: typing.Optional[jsii.Number] = None,
    throughput_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc9f3b59466c869ca74899702fe649aaff25f4a5470e1386ec05eda21609227(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    file_system_id: builtins.str,
    security_groups: typing.Sequence[builtins.str],
    subnet_id: builtins.str,
    ip_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e6a1cbb4916c04d8bd873bad82a044f6f565540f7e067511a9d0fb1f901c82(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9216740b6d2d959e668bdb98e05e03e5f5e9922b6fc6e2dbe1078ca7dd5b85e8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6ff86a9a5df33cb96a093da2c46a32f394226c4ebd09045578581781dc89b72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c445bb65e9b96da27b0d9f5fcc45da645f6b829b1322427fb9bb0ddb354387c8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80938068805d871ba4976b05a1f232bb8d0a7cf5d5660ef40cec3b9276214781(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891a7b9d8842ad8534e3533479357ac2ada34875f781cb70fa04ddff531e8f70(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__365847ab0b4ae35d3f541ec9dffb2a0b5385b5af11bd1c71d5f15e36fe6d0d7d(
    *,
    file_system_id: builtins.str,
    security_groups: typing.Sequence[builtins.str],
    subnet_id: builtins.str,
    ip_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a32c2b6d7c5663618c62bcebfa71d19a76889140b082358b765605f1e8d3b7f(
    *,
    security_group: _ISecurityGroup_cdbba9d3,
    file_system_arn: typing.Optional[builtins.str] = None,
    file_system_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b677fbb05149a7ebdc9a9fb627ba251c236e4b06c7eb65bc3345c1108858d456(
    *,
    vpc: _IVpc_6d1f76c4,
    enable_automatic_backups: typing.Optional[builtins.bool] = None,
    encrypted: typing.Optional[builtins.bool] = None,
    file_system_name: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_IKey_36930160] = None,
    lifecycle_policy: typing.Optional[LifecyclePolicy] = None,
    out_of_infrequent_access_policy: typing.Optional[OutOfInfrequentAccessPolicy] = None,
    performance_mode: typing.Optional[PerformanceMode] = None,
    provisioned_throughput_per_second: typing.Optional[_Size_7fbd4337] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
    throughput_mode: typing.Optional[ThroughputMode] = None,
    vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece5ed399573018da8f2dea2bd92e7b6dc2c8d65e0cc5c380d3374862eb1f023(
    grantee: _IGrantable_4c5a91d1,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b62cebca87e50fd4d0472365fe77cce1115937dfc4b475c5558f5852d64c74(
    *,
    gid: builtins.str,
    uid: builtins.str,
    secondary_gids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe851054b4e764116abc99b89c2e62292359007fb188fbbb4d2698272bb167f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    file_system: IFileSystem,
    create_acl: typing.Optional[typing.Union[Acl, typing.Dict[builtins.str, typing.Any]]] = None,
    path: typing.Optional[builtins.str] = None,
    posix_user: typing.Optional[typing.Union[PosixUser, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e5a4fb7e576d35ccbe5bb21d0ce65020f89a63b9c75cfa0658c8ac25f6a728a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_point_arn: typing.Optional[builtins.str] = None,
    access_point_id: typing.Optional[builtins.str] = None,
    file_system: typing.Optional[IFileSystem] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__763e9bb073ac3f149e4c64c0b2c6e2389f651d255138ea6c724ae440ef61e7a8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    access_point_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b74d2e20d80386eeaa930f280b609ed4894d89297210d5c114907a709f443e2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: _IVpc_6d1f76c4,
    enable_automatic_backups: typing.Optional[builtins.bool] = None,
    encrypted: typing.Optional[builtins.bool] = None,
    file_system_name: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_IKey_36930160] = None,
    lifecycle_policy: typing.Optional[LifecyclePolicy] = None,
    out_of_infrequent_access_policy: typing.Optional[OutOfInfrequentAccessPolicy] = None,
    performance_mode: typing.Optional[PerformanceMode] = None,
    provisioned_throughput_per_second: typing.Optional[_Size_7fbd4337] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
    throughput_mode: typing.Optional[ThroughputMode] = None,
    vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9acb6511c7b399dcbcfcd7906e9fc002e8a8f521c536099b19108fa41e9fad93(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    security_group: _ISecurityGroup_cdbba9d3,
    file_system_arn: typing.Optional[builtins.str] = None,
    file_system_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7602c05b49aff5b39a57d74361c99930d883b17612fe278a3e6282147130a5c3(
    id: builtins.str,
    *,
    create_acl: typing.Optional[typing.Union[Acl, typing.Dict[builtins.str, typing.Any]]] = None,
    path: typing.Optional[builtins.str] = None,
    posix_user: typing.Optional[typing.Union[PosixUser, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0993e15d2297516b90689ad319904e8309cfde19a71ab95b0261b6d59a0005a2(
    grantee: _IGrantable_4c5a91d1,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
