'''
# AWS Transfer for SFTP Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as transfer
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Transfer construct libraries](https://constructs.dev/search?q=transfer)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Transfer resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Transfer.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Transfer](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Transfer.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/master/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
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

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnAgreement(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_transfer.CfnAgreement",
):
    '''A CloudFormation ``AWS::Transfer::Agreement``.

    Creates an agreement. An agreement is a bilateral trading partner agreement, or partnership, between an AWS Transfer Family server and an AS2 process. The agreement defines the file and message transfer relationship between the server and the AS2 process. To define an agreement, Transfer Family combines a server, local profile, partner profile, certificate, and other attributes.

    The partner is identified with the ``PartnerProfileId`` , and the AS2 process is identified with the ``LocalProfileId`` .

    :cloudformationResource: AWS::Transfer::Agreement
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_transfer as transfer
        
        cfn_agreement = transfer.CfnAgreement(self, "MyCfnAgreement",
            access_role="accessRole",
            base_directory="baseDirectory",
            local_profile_id="localProfileId",
            partner_profile_id="partnerProfileId",
            server_id="serverId",
        
            # the properties below are optional
            description="description",
            status="status",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        access_role: builtins.str,
        base_directory: builtins.str,
        local_profile_id: builtins.str,
        partner_profile_id: builtins.str,
        server_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Transfer::Agreement``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param access_role: With AS2, you can send files by calling ``StartFileTransfer`` and specifying the file paths in the request parameter, ``SendFilePaths`` . We use the file’s parent directory (for example, for ``--send-file-paths /bucket/dir/file.txt`` , parent directory is ``/bucket/dir/`` ) to temporarily store a processed AS2 message file, store the MDN when we receive them from the partner, and write a final JSON file containing relevant metadata of the transmission. So, the ``AccessRole`` needs to provide read and write access to the parent directory of the file location used in the ``StartFileTransfer`` request. Additionally, you need to provide read and write access to the parent directory of the files that you intend to send with ``StartFileTransfer`` .
        :param base_directory: The landing directory (folder) for files that are transferred by using the AS2 protocol.
        :param local_profile_id: A unique identifier for the AS2 local profile.
        :param partner_profile_id: A unique identifier for the partner profile used in the agreement.
        :param server_id: A system-assigned unique identifier for a server instance. This identifier indicates the specific server that the agreement uses.
        :param description: The name or short description that's used to identify the agreement.
        :param status: The current status of the agreement, either ``ACTIVE`` or ``INACTIVE`` .
        :param tags: Key-value pairs that can be used to group and search for agreements.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__134ac265dd289ba5618fbd91064199ed20f2e0d343005babc69fac90c58a9b41)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAgreementProps(
            access_role=access_role,
            base_directory=base_directory,
            local_profile_id=local_profile_id,
            partner_profile_id=partner_profile_id,
            server_id=server_id,
            description=description,
            status=status,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82b6f39c4297036e4e8f3fa89f18debb725cf55aa3108623c1638044a711f068)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2dc063111b9f32e146b7da061febd8c0c6f98641bdb129870dc838d17da6039)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAgreementId")
    def attr_agreement_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: AgreementId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAgreementId"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Key-value pairs that can be used to group and search for agreements.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="accessRole")
    def access_role(self) -> builtins.str:
        '''With AS2, you can send files by calling ``StartFileTransfer`` and specifying the file paths in the request parameter, ``SendFilePaths`` .

        We use the file’s parent directory (for example, for ``--send-file-paths /bucket/dir/file.txt`` , parent directory is ``/bucket/dir/`` ) to temporarily store a processed AS2 message file, store the MDN when we receive them from the partner, and write a final JSON file containing relevant metadata of the transmission. So, the ``AccessRole`` needs to provide read and write access to the parent directory of the file location used in the ``StartFileTransfer`` request. Additionally, you need to provide read and write access to the parent directory of the files that you intend to send with ``StartFileTransfer`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-accessrole
        '''
        return typing.cast(builtins.str, jsii.get(self, "accessRole"))

    @access_role.setter
    def access_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e8102f6a51b4eb3c63a9ffaebd73dda2f8eb3b4919fb683c34eae15e608d16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessRole", value)

    @builtins.property
    @jsii.member(jsii_name="baseDirectory")
    def base_directory(self) -> builtins.str:
        '''The landing directory (folder) for files that are transferred by using the AS2 protocol.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-basedirectory
        '''
        return typing.cast(builtins.str, jsii.get(self, "baseDirectory"))

    @base_directory.setter
    def base_directory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e49b84094df16463717193c0096d4e7c3c6e03026003d389a1183224dbad75df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseDirectory", value)

    @builtins.property
    @jsii.member(jsii_name="localProfileId")
    def local_profile_id(self) -> builtins.str:
        '''A unique identifier for the AS2 local profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-localprofileid
        '''
        return typing.cast(builtins.str, jsii.get(self, "localProfileId"))

    @local_profile_id.setter
    def local_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22e9ab4d639c7742ee117326bcead033c3ca977cd7220b2773cf189ebe7a72c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="partnerProfileId")
    def partner_profile_id(self) -> builtins.str:
        '''A unique identifier for the partner profile used in the agreement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-partnerprofileid
        '''
        return typing.cast(builtins.str, jsii.get(self, "partnerProfileId"))

    @partner_profile_id.setter
    def partner_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0038c01636c581e21010bf8691cb6ec2b55aef6a1f759a0450f42ad0f1fff133)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partnerProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="serverId")
    def server_id(self) -> builtins.str:
        '''A system-assigned unique identifier for a server instance.

        This identifier indicates the specific server that the agreement uses.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-serverid
        '''
        return typing.cast(builtins.str, jsii.get(self, "serverId"))

    @server_id.setter
    def server_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a85bc483fda39fdf5c5fbdc370315c216d9b0d044684b923fe691fe193b28acc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The name or short description that's used to identify the agreement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4d4014dc136ed966206324426f76956920a746ddbbe50c5c2696524a109eb5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        '''The current status of the agreement, either ``ACTIVE`` or ``INACTIVE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-status
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "status"))

    @status.setter
    def status(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efd4a60054595db1e60bbf02ae812f5dc6d72f9cccdd0b8d20ba62c975bcb1ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)


@jsii.data_type(
    jsii_type="monocdk.aws_transfer.CfnAgreementProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_role": "accessRole",
        "base_directory": "baseDirectory",
        "local_profile_id": "localProfileId",
        "partner_profile_id": "partnerProfileId",
        "server_id": "serverId",
        "description": "description",
        "status": "status",
        "tags": "tags",
    },
)
class CfnAgreementProps:
    def __init__(
        self,
        *,
        access_role: builtins.str,
        base_directory: builtins.str,
        local_profile_id: builtins.str,
        partner_profile_id: builtins.str,
        server_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAgreement``.

        :param access_role: With AS2, you can send files by calling ``StartFileTransfer`` and specifying the file paths in the request parameter, ``SendFilePaths`` . We use the file’s parent directory (for example, for ``--send-file-paths /bucket/dir/file.txt`` , parent directory is ``/bucket/dir/`` ) to temporarily store a processed AS2 message file, store the MDN when we receive them from the partner, and write a final JSON file containing relevant metadata of the transmission. So, the ``AccessRole`` needs to provide read and write access to the parent directory of the file location used in the ``StartFileTransfer`` request. Additionally, you need to provide read and write access to the parent directory of the files that you intend to send with ``StartFileTransfer`` .
        :param base_directory: The landing directory (folder) for files that are transferred by using the AS2 protocol.
        :param local_profile_id: A unique identifier for the AS2 local profile.
        :param partner_profile_id: A unique identifier for the partner profile used in the agreement.
        :param server_id: A system-assigned unique identifier for a server instance. This identifier indicates the specific server that the agreement uses.
        :param description: The name or short description that's used to identify the agreement.
        :param status: The current status of the agreement, either ``ACTIVE`` or ``INACTIVE`` .
        :param tags: Key-value pairs that can be used to group and search for agreements.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_transfer as transfer
            
            cfn_agreement_props = transfer.CfnAgreementProps(
                access_role="accessRole",
                base_directory="baseDirectory",
                local_profile_id="localProfileId",
                partner_profile_id="partnerProfileId",
                server_id="serverId",
            
                # the properties below are optional
                description="description",
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85db52acaba061f601c6ce38f4da9214bebacd0dddf81b18265913d0c5772e20)
            check_type(argname="argument access_role", value=access_role, expected_type=type_hints["access_role"])
            check_type(argname="argument base_directory", value=base_directory, expected_type=type_hints["base_directory"])
            check_type(argname="argument local_profile_id", value=local_profile_id, expected_type=type_hints["local_profile_id"])
            check_type(argname="argument partner_profile_id", value=partner_profile_id, expected_type=type_hints["partner_profile_id"])
            check_type(argname="argument server_id", value=server_id, expected_type=type_hints["server_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_role": access_role,
            "base_directory": base_directory,
            "local_profile_id": local_profile_id,
            "partner_profile_id": partner_profile_id,
            "server_id": server_id,
        }
        if description is not None:
            self._values["description"] = description
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def access_role(self) -> builtins.str:
        '''With AS2, you can send files by calling ``StartFileTransfer`` and specifying the file paths in the request parameter, ``SendFilePaths`` .

        We use the file’s parent directory (for example, for ``--send-file-paths /bucket/dir/file.txt`` , parent directory is ``/bucket/dir/`` ) to temporarily store a processed AS2 message file, store the MDN when we receive them from the partner, and write a final JSON file containing relevant metadata of the transmission. So, the ``AccessRole`` needs to provide read and write access to the parent directory of the file location used in the ``StartFileTransfer`` request. Additionally, you need to provide read and write access to the parent directory of the files that you intend to send with ``StartFileTransfer`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-accessrole
        '''
        result = self._values.get("access_role")
        assert result is not None, "Required property 'access_role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def base_directory(self) -> builtins.str:
        '''The landing directory (folder) for files that are transferred by using the AS2 protocol.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-basedirectory
        '''
        result = self._values.get("base_directory")
        assert result is not None, "Required property 'base_directory' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_profile_id(self) -> builtins.str:
        '''A unique identifier for the AS2 local profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-localprofileid
        '''
        result = self._values.get("local_profile_id")
        assert result is not None, "Required property 'local_profile_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def partner_profile_id(self) -> builtins.str:
        '''A unique identifier for the partner profile used in the agreement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-partnerprofileid
        '''
        result = self._values.get("partner_profile_id")
        assert result is not None, "Required property 'partner_profile_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server_id(self) -> builtins.str:
        '''A system-assigned unique identifier for a server instance.

        This identifier indicates the specific server that the agreement uses.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-serverid
        '''
        result = self._values.get("server_id")
        assert result is not None, "Required property 'server_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The name or short description that's used to identify the agreement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The current status of the agreement, either ``ACTIVE`` or ``INACTIVE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Key-value pairs that can be used to group and search for agreements.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAgreementProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnCertificate(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_transfer.CfnCertificate",
):
    '''A CloudFormation ``AWS::Transfer::Certificate``.

    Imports the signing and encryption certificates that you need to create local (AS2) profiles and partner profiles.

    :cloudformationResource: AWS::Transfer::Certificate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_transfer as transfer
        
        cfn_certificate = transfer.CfnCertificate(self, "MyCfnCertificate",
            certificate="certificate",
            usage="usage",
        
            # the properties below are optional
            active_date="activeDate",
            certificate_chain="certificateChain",
            description="description",
            inactive_date="inactiveDate",
            private_key="privateKey",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        certificate: builtins.str,
        usage: builtins.str,
        active_date: typing.Optional[builtins.str] = None,
        certificate_chain: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        inactive_date: typing.Optional[builtins.str] = None,
        private_key: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Transfer::Certificate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param certificate: The file name for the certificate.
        :param usage: Specifies whether this certificate is used for signing or encryption.
        :param active_date: An optional date that specifies when the certificate becomes active.
        :param certificate_chain: The list of certificates that make up the chain for the certificate.
        :param description: The name or description that's used to identity the certificate.
        :param inactive_date: An optional date that specifies when the certificate becomes inactive.
        :param private_key: The file that contains the private key for the certificate that's being imported.
        :param tags: Key-value pairs that can be used to group and search for certificates.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d43491862cd588c88ad1d78265c893bf01147132b2a135f865cf80d23f3bf73f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCertificateProps(
            certificate=certificate,
            usage=usage,
            active_date=active_date,
            certificate_chain=certificate_chain,
            description=description,
            inactive_date=inactive_date,
            private_key=private_key,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5183da02df7a82320f1799e730b9a6a32ecea270722ed82afaf89ef0bb129396)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57b28b97c4064ca3e2de22f419aabb70dedc46b065b3f52f9cd33ab6c5eee1a3)
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
        '''The unique Amazon Resource Name (ARN) for the certificate.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCertificateId")
    def attr_certificate_id(self) -> builtins.str:
        '''An array of identifiers for the imported certificates.

        You use this identifier for working with profiles and partner profiles.

        :cloudformationAttribute: CertificateId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCertificateId"))

    @builtins.property
    @jsii.member(jsii_name="attrNotAfterDate")
    def attr_not_after_date(self) -> builtins.str:
        '''The final date that the certificate is valid.

        :cloudformationAttribute: NotAfterDate
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrNotAfterDate"))

    @builtins.property
    @jsii.member(jsii_name="attrNotBeforeDate")
    def attr_not_before_date(self) -> builtins.str:
        '''The earliest date that the certificate is valid.

        :cloudformationAttribute: NotBeforeDate
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrNotBeforeDate"))

    @builtins.property
    @jsii.member(jsii_name="attrSerial")
    def attr_serial(self) -> builtins.str:
        '''The serial number for the certificate.

        :cloudformationAttribute: Serial
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSerial"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The certificate can be either ``ACTIVE`` , ``PENDING_ROTATION`` , or ``INACTIVE`` .

        ``PENDING_ROTATION`` means that this certificate will replace the current certificate when it expires.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrType")
    def attr_type(self) -> builtins.str:
        '''If a private key has been specified for the certificate, its type is ``CERTIFICATE_WITH_PRIVATE_KEY`` .

        If there is no private key, the type is ``CERTIFICATE`` .

        :cloudformationAttribute: Type
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrType"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Key-value pairs that can be used to group and search for certificates.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        '''The file name for the certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-certificate
        '''
        return typing.cast(builtins.str, jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b605f1495cc8a3cc3de85f56830592e17a896e84759b36c77d3973caeb95d04a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="usage")
    def usage(self) -> builtins.str:
        '''Specifies whether this certificate is used for signing or encryption.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-usage
        '''
        return typing.cast(builtins.str, jsii.get(self, "usage"))

    @usage.setter
    def usage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4627978c67efffef809ec7dd495d0b83ed4a16f6d03d8d092fd749e6d478929)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usage", value)

    @builtins.property
    @jsii.member(jsii_name="activeDate")
    def active_date(self) -> typing.Optional[builtins.str]:
        '''An optional date that specifies when the certificate becomes active.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-activedate
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "activeDate"))

    @active_date.setter
    def active_date(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44755a8522e524e922655abc094063e699553311290bc79a81841a896a754e75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activeDate", value)

    @builtins.property
    @jsii.member(jsii_name="certificateChain")
    def certificate_chain(self) -> typing.Optional[builtins.str]:
        '''The list of certificates that make up the chain for the certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-certificatechain
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateChain"))

    @certificate_chain.setter
    def certificate_chain(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36c89e1c655700623e39ff924fade459f81425928742fa8d469263a0f4ab216e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateChain", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The name or description that's used to identity the certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c72fc0e92c82b4ebad556953917bad67331bd218dd960f56c960b0b5bc585a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="inactiveDate")
    def inactive_date(self) -> typing.Optional[builtins.str]:
        '''An optional date that specifies when the certificate becomes inactive.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-inactivedate
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inactiveDate"))

    @inactive_date.setter
    def inactive_date(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93628e5f976dc54245b41abdd0ecda5b4f3b5bda080812b772aa7322f58a6356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inactiveDate", value)

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The file that contains the private key for the certificate that's being imported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-privatekey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1a2aec6b7c6cc42729096854b0d645764b2d91343226179c87d2809871e49a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value)


@jsii.data_type(
    jsii_type="monocdk.aws_transfer.CfnCertificateProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate": "certificate",
        "usage": "usage",
        "active_date": "activeDate",
        "certificate_chain": "certificateChain",
        "description": "description",
        "inactive_date": "inactiveDate",
        "private_key": "privateKey",
        "tags": "tags",
    },
)
class CfnCertificateProps:
    def __init__(
        self,
        *,
        certificate: builtins.str,
        usage: builtins.str,
        active_date: typing.Optional[builtins.str] = None,
        certificate_chain: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        inactive_date: typing.Optional[builtins.str] = None,
        private_key: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnCertificate``.

        :param certificate: The file name for the certificate.
        :param usage: Specifies whether this certificate is used for signing or encryption.
        :param active_date: An optional date that specifies when the certificate becomes active.
        :param certificate_chain: The list of certificates that make up the chain for the certificate.
        :param description: The name or description that's used to identity the certificate.
        :param inactive_date: An optional date that specifies when the certificate becomes inactive.
        :param private_key: The file that contains the private key for the certificate that's being imported.
        :param tags: Key-value pairs that can be used to group and search for certificates.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_transfer as transfer
            
            cfn_certificate_props = transfer.CfnCertificateProps(
                certificate="certificate",
                usage="usage",
            
                # the properties below are optional
                active_date="activeDate",
                certificate_chain="certificateChain",
                description="description",
                inactive_date="inactiveDate",
                private_key="privateKey",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd66966550b89bf450519253b17798a8a754aca6381aa18653886a6598ef328)
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument usage", value=usage, expected_type=type_hints["usage"])
            check_type(argname="argument active_date", value=active_date, expected_type=type_hints["active_date"])
            check_type(argname="argument certificate_chain", value=certificate_chain, expected_type=type_hints["certificate_chain"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument inactive_date", value=inactive_date, expected_type=type_hints["inactive_date"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate": certificate,
            "usage": usage,
        }
        if active_date is not None:
            self._values["active_date"] = active_date
        if certificate_chain is not None:
            self._values["certificate_chain"] = certificate_chain
        if description is not None:
            self._values["description"] = description
        if inactive_date is not None:
            self._values["inactive_date"] = inactive_date
        if private_key is not None:
            self._values["private_key"] = private_key
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def certificate(self) -> builtins.str:
        '''The file name for the certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-certificate
        '''
        result = self._values.get("certificate")
        assert result is not None, "Required property 'certificate' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def usage(self) -> builtins.str:
        '''Specifies whether this certificate is used for signing or encryption.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-usage
        '''
        result = self._values.get("usage")
        assert result is not None, "Required property 'usage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def active_date(self) -> typing.Optional[builtins.str]:
        '''An optional date that specifies when the certificate becomes active.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-activedate
        '''
        result = self._values.get("active_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_chain(self) -> typing.Optional[builtins.str]:
        '''The list of certificates that make up the chain for the certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-certificatechain
        '''
        result = self._values.get("certificate_chain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The name or description that's used to identity the certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inactive_date(self) -> typing.Optional[builtins.str]:
        '''An optional date that specifies when the certificate becomes inactive.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-inactivedate
        '''
        result = self._values.get("inactive_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The file that contains the private key for the certificate that's being imported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-privatekey
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Key-value pairs that can be used to group and search for certificates.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCertificateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnConnector(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_transfer.CfnConnector",
):
    '''A CloudFormation ``AWS::Transfer::Connector``.

    Creates the connector, which captures the parameters for an outbound connection for the AS2 protocol. The connector is required for sending files to an externally hosted AS2 server. For more details about connectors, see `Create AS2 connectors <https://docs.aws.amazon.com/transfer/latest/userguide/create-b2b-server.html#configure-as2-connector>`_ .

    :cloudformationResource: AWS::Transfer::Connector
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_transfer as transfer
        
        # as2_config: Any
        
        cfn_connector = transfer.CfnConnector(self, "MyCfnConnector",
            access_role="accessRole",
            as2_config=as2_config,
            url="url",
        
            # the properties below are optional
            logging_role="loggingRole",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        access_role: builtins.str,
        as2_config: typing.Any,
        url: builtins.str,
        logging_role: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Transfer::Connector``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param access_role: With AS2, you can send files by calling ``StartFileTransfer`` and specifying the file paths in the request parameter, ``SendFilePaths`` . We use the file’s parent directory (for example, for ``--send-file-paths /bucket/dir/file.txt`` , parent directory is ``/bucket/dir/`` ) to temporarily store a processed AS2 message file, store the MDN when we receive them from the partner, and write a final JSON file containing relevant metadata of the transmission. So, the ``AccessRole`` needs to provide read and write access to the parent directory of the file location used in the ``StartFileTransfer`` request. Additionally, you need to provide read and write access to the parent directory of the files that you intend to send with ``StartFileTransfer`` .
        :param as2_config: A structure that contains the parameters for a connector object.
        :param url: The URL of the partner's AS2 endpoint.
        :param logging_role: The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that allows a connector to turn on CloudWatch logging for Amazon S3 events. When set, you can view connector activity in your CloudWatch logs.
        :param tags: Key-value pairs that can be used to group and search for connectors.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dd88525c1d58175c9d6dd85c85d38fb58f7673111ce0badabd573b79748ef52)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnConnectorProps(
            access_role=access_role,
            as2_config=as2_config,
            url=url,
            logging_role=logging_role,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10b81c5c3a5bbf5c466697baf4ec957ecd3ea156a60b9dcda492fcba69573a54)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31d71f668080348885a55058bd21c3b7cabb2ce4d3fc5f1f72c3face54a4634a)
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
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrConnectorId")
    def attr_connector_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: ConnectorId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConnectorId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Key-value pairs that can be used to group and search for connectors.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html#cfn-transfer-connector-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="accessRole")
    def access_role(self) -> builtins.str:
        '''With AS2, you can send files by calling ``StartFileTransfer`` and specifying the file paths in the request parameter, ``SendFilePaths`` .

        We use the file’s parent directory (for example, for ``--send-file-paths /bucket/dir/file.txt`` , parent directory is ``/bucket/dir/`` ) to temporarily store a processed AS2 message file, store the MDN when we receive them from the partner, and write a final JSON file containing relevant metadata of the transmission. So, the ``AccessRole`` needs to provide read and write access to the parent directory of the file location used in the ``StartFileTransfer`` request. Additionally, you need to provide read and write access to the parent directory of the files that you intend to send with ``StartFileTransfer`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html#cfn-transfer-connector-accessrole
        '''
        return typing.cast(builtins.str, jsii.get(self, "accessRole"))

    @access_role.setter
    def access_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80ffd4896a613038476b7396e806e81f43d5404e6ff147d3aa575c5433af5f70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessRole", value)

    @builtins.property
    @jsii.member(jsii_name="as2Config")
    def as2_config(self) -> typing.Any:
        '''A structure that contains the parameters for a connector object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html#cfn-transfer-connector-as2config
        '''
        return typing.cast(typing.Any, jsii.get(self, "as2Config"))

    @as2_config.setter
    def as2_config(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a782191976a9b43922fdf6df907dacde3272fc9e1c77be8ecdc9a46c8490414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "as2Config", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        '''The URL of the partner's AS2 endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html#cfn-transfer-connector-url
        '''
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1000819cbfa7eb644e93ff9a76ca8ab09b077e91a9e4c3f15781a241c153c78c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)

    @builtins.property
    @jsii.member(jsii_name="loggingRole")
    def logging_role(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that allows a connector to turn on CloudWatch logging for Amazon S3 events.

        When set, you can view connector activity in your CloudWatch logs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html#cfn-transfer-connector-loggingrole
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loggingRole"))

    @logging_role.setter
    def logging_role(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac953273fd9a91cb0fbf716529c26650eb88b7431904bac25fd2dcbbe10d9846)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingRole", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_transfer.CfnConnector.As2ConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "compression": "compression",
            "encryption_algorithm": "encryptionAlgorithm",
            "local_profile_id": "localProfileId",
            "mdn_response": "mdnResponse",
            "mdn_signing_algorithm": "mdnSigningAlgorithm",
            "message_subject": "messageSubject",
            "partner_profile_id": "partnerProfileId",
            "signing_algorithm": "signingAlgorithm",
        },
    )
    class As2ConfigProperty:
        def __init__(
            self,
            *,
            compression: typing.Optional[builtins.str] = None,
            encryption_algorithm: typing.Optional[builtins.str] = None,
            local_profile_id: typing.Optional[builtins.str] = None,
            mdn_response: typing.Optional[builtins.str] = None,
            mdn_signing_algorithm: typing.Optional[builtins.str] = None,
            message_subject: typing.Optional[builtins.str] = None,
            partner_profile_id: typing.Optional[builtins.str] = None,
            signing_algorithm: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param compression: ``CfnConnector.As2ConfigProperty.Compression``.
            :param encryption_algorithm: ``CfnConnector.As2ConfigProperty.EncryptionAlgorithm``.
            :param local_profile_id: ``CfnConnector.As2ConfigProperty.LocalProfileId``.
            :param mdn_response: ``CfnConnector.As2ConfigProperty.MdnResponse``.
            :param mdn_signing_algorithm: ``CfnConnector.As2ConfigProperty.MdnSigningAlgorithm``.
            :param message_subject: ``CfnConnector.As2ConfigProperty.MessageSubject``.
            :param partner_profile_id: ``CfnConnector.As2ConfigProperty.PartnerProfileId``.
            :param signing_algorithm: ``CfnConnector.As2ConfigProperty.SigningAlgorithm``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-as2config.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_transfer as transfer
                
                as2_config_property = transfer.CfnConnector.As2ConfigProperty(
                    compression="compression",
                    encryption_algorithm="encryptionAlgorithm",
                    local_profile_id="localProfileId",
                    mdn_response="mdnResponse",
                    mdn_signing_algorithm="mdnSigningAlgorithm",
                    message_subject="messageSubject",
                    partner_profile_id="partnerProfileId",
                    signing_algorithm="signingAlgorithm"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4b1d9d705075f1026020ad89416a4c0a069541b673c1ad0db9578248190e83f8)
                check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
                check_type(argname="argument encryption_algorithm", value=encryption_algorithm, expected_type=type_hints["encryption_algorithm"])
                check_type(argname="argument local_profile_id", value=local_profile_id, expected_type=type_hints["local_profile_id"])
                check_type(argname="argument mdn_response", value=mdn_response, expected_type=type_hints["mdn_response"])
                check_type(argname="argument mdn_signing_algorithm", value=mdn_signing_algorithm, expected_type=type_hints["mdn_signing_algorithm"])
                check_type(argname="argument message_subject", value=message_subject, expected_type=type_hints["message_subject"])
                check_type(argname="argument partner_profile_id", value=partner_profile_id, expected_type=type_hints["partner_profile_id"])
                check_type(argname="argument signing_algorithm", value=signing_algorithm, expected_type=type_hints["signing_algorithm"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if compression is not None:
                self._values["compression"] = compression
            if encryption_algorithm is not None:
                self._values["encryption_algorithm"] = encryption_algorithm
            if local_profile_id is not None:
                self._values["local_profile_id"] = local_profile_id
            if mdn_response is not None:
                self._values["mdn_response"] = mdn_response
            if mdn_signing_algorithm is not None:
                self._values["mdn_signing_algorithm"] = mdn_signing_algorithm
            if message_subject is not None:
                self._values["message_subject"] = message_subject
            if partner_profile_id is not None:
                self._values["partner_profile_id"] = partner_profile_id
            if signing_algorithm is not None:
                self._values["signing_algorithm"] = signing_algorithm

        @builtins.property
        def compression(self) -> typing.Optional[builtins.str]:
            '''``CfnConnector.As2ConfigProperty.Compression``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-as2config.html#cfn-transfer-connector-as2config-compression
            '''
            result = self._values.get("compression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_algorithm(self) -> typing.Optional[builtins.str]:
            '''``CfnConnector.As2ConfigProperty.EncryptionAlgorithm``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-as2config.html#cfn-transfer-connector-as2config-encryptionalgorithm
            '''
            result = self._values.get("encryption_algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def local_profile_id(self) -> typing.Optional[builtins.str]:
            '''``CfnConnector.As2ConfigProperty.LocalProfileId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-as2config.html#cfn-transfer-connector-as2config-localprofileid
            '''
            result = self._values.get("local_profile_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mdn_response(self) -> typing.Optional[builtins.str]:
            '''``CfnConnector.As2ConfigProperty.MdnResponse``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-as2config.html#cfn-transfer-connector-as2config-mdnresponse
            '''
            result = self._values.get("mdn_response")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mdn_signing_algorithm(self) -> typing.Optional[builtins.str]:
            '''``CfnConnector.As2ConfigProperty.MdnSigningAlgorithm``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-as2config.html#cfn-transfer-connector-as2config-mdnsigningalgorithm
            '''
            result = self._values.get("mdn_signing_algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message_subject(self) -> typing.Optional[builtins.str]:
            '''``CfnConnector.As2ConfigProperty.MessageSubject``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-as2config.html#cfn-transfer-connector-as2config-messagesubject
            '''
            result = self._values.get("message_subject")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def partner_profile_id(self) -> typing.Optional[builtins.str]:
            '''``CfnConnector.As2ConfigProperty.PartnerProfileId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-as2config.html#cfn-transfer-connector-as2config-partnerprofileid
            '''
            result = self._values.get("partner_profile_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def signing_algorithm(self) -> typing.Optional[builtins.str]:
            '''``CfnConnector.As2ConfigProperty.SigningAlgorithm``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-as2config.html#cfn-transfer-connector-as2config-signingalgorithm
            '''
            result = self._values.get("signing_algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "As2ConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_transfer.CfnConnectorProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_role": "accessRole",
        "as2_config": "as2Config",
        "url": "url",
        "logging_role": "loggingRole",
        "tags": "tags",
    },
)
class CfnConnectorProps:
    def __init__(
        self,
        *,
        access_role: builtins.str,
        as2_config: typing.Any,
        url: builtins.str,
        logging_role: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnConnector``.

        :param access_role: With AS2, you can send files by calling ``StartFileTransfer`` and specifying the file paths in the request parameter, ``SendFilePaths`` . We use the file’s parent directory (for example, for ``--send-file-paths /bucket/dir/file.txt`` , parent directory is ``/bucket/dir/`` ) to temporarily store a processed AS2 message file, store the MDN when we receive them from the partner, and write a final JSON file containing relevant metadata of the transmission. So, the ``AccessRole`` needs to provide read and write access to the parent directory of the file location used in the ``StartFileTransfer`` request. Additionally, you need to provide read and write access to the parent directory of the files that you intend to send with ``StartFileTransfer`` .
        :param as2_config: A structure that contains the parameters for a connector object.
        :param url: The URL of the partner's AS2 endpoint.
        :param logging_role: The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that allows a connector to turn on CloudWatch logging for Amazon S3 events. When set, you can view connector activity in your CloudWatch logs.
        :param tags: Key-value pairs that can be used to group and search for connectors.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_transfer as transfer
            
            # as2_config: Any
            
            cfn_connector_props = transfer.CfnConnectorProps(
                access_role="accessRole",
                as2_config=as2_config,
                url="url",
            
                # the properties below are optional
                logging_role="loggingRole",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__424e64f552dddea19abf0cf15f3a2262188be07a6f64355fb834c35a70a9ddb4)
            check_type(argname="argument access_role", value=access_role, expected_type=type_hints["access_role"])
            check_type(argname="argument as2_config", value=as2_config, expected_type=type_hints["as2_config"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument logging_role", value=logging_role, expected_type=type_hints["logging_role"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_role": access_role,
            "as2_config": as2_config,
            "url": url,
        }
        if logging_role is not None:
            self._values["logging_role"] = logging_role
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def access_role(self) -> builtins.str:
        '''With AS2, you can send files by calling ``StartFileTransfer`` and specifying the file paths in the request parameter, ``SendFilePaths`` .

        We use the file’s parent directory (for example, for ``--send-file-paths /bucket/dir/file.txt`` , parent directory is ``/bucket/dir/`` ) to temporarily store a processed AS2 message file, store the MDN when we receive them from the partner, and write a final JSON file containing relevant metadata of the transmission. So, the ``AccessRole`` needs to provide read and write access to the parent directory of the file location used in the ``StartFileTransfer`` request. Additionally, you need to provide read and write access to the parent directory of the files that you intend to send with ``StartFileTransfer`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html#cfn-transfer-connector-accessrole
        '''
        result = self._values.get("access_role")
        assert result is not None, "Required property 'access_role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def as2_config(self) -> typing.Any:
        '''A structure that contains the parameters for a connector object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html#cfn-transfer-connector-as2config
        '''
        result = self._values.get("as2_config")
        assert result is not None, "Required property 'as2_config' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''The URL of the partner's AS2 endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html#cfn-transfer-connector-url
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def logging_role(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that allows a connector to turn on CloudWatch logging for Amazon S3 events.

        When set, you can view connector activity in your CloudWatch logs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html#cfn-transfer-connector-loggingrole
        '''
        result = self._values.get("logging_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Key-value pairs that can be used to group and search for connectors.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html#cfn-transfer-connector-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnProfile(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_transfer.CfnProfile",
):
    '''A CloudFormation ``AWS::Transfer::Profile``.

    Creates the local or partner profile to use for AS2 transfers.

    :cloudformationResource: AWS::Transfer::Profile
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-profile.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_transfer as transfer
        
        cfn_profile = transfer.CfnProfile(self, "MyCfnProfile",
            as2_id="as2Id",
            profile_type="profileType",
        
            # the properties below are optional
            certificate_ids=["certificateIds"],
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        as2_id: builtins.str,
        profile_type: builtins.str,
        certificate_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Transfer::Profile``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param as2_id: The ``As2Id`` is the *AS2-name* , as defined in the `RFC 4130 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc4130>`_ . For inbound transfers, this is the ``AS2-From`` header for the AS2 messages sent from the partner. For outbound connectors, this is the ``AS2-To`` header for the AS2 messages sent to the partner using the ``StartFileTransfer`` API operation. This ID cannot include spaces.
        :param profile_type: Indicates whether to list only ``LOCAL`` type profiles or only ``PARTNER`` type profiles. If not supplied in the request, the command lists all types of profiles.
        :param certificate_ids: An array of identifiers for the imported certificates. You use this identifier for working with profiles and partner profiles.
        :param tags: Key-value pairs that can be used to group and search for profiles.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1214dbae9407b5aa3b5f795879c88279a81606fa3a1b4701f68c9d336372d1ae)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnProfileProps(
            as2_id=as2_id,
            profile_type=profile_type,
            certificate_ids=certificate_ids,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e2d85f151ab9ea787f667701affa2bf96fb67168d67d1c0d7d1b5051021e87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e665dee77f2b91690cd9de47b1e814fac74f411d8d9765b07f69f7fe9b0cbb50)
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
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrProfileId")
    def attr_profile_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: ProfileId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProfileId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Key-value pairs that can be used to group and search for profiles.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-profile.html#cfn-transfer-profile-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="as2Id")
    def as2_id(self) -> builtins.str:
        '''The ``As2Id`` is the *AS2-name* , as defined in the `RFC 4130 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc4130>`_ . For inbound transfers, this is the ``AS2-From`` header for the AS2 messages sent from the partner. For outbound connectors, this is the ``AS2-To`` header for the AS2 messages sent to the partner using the ``StartFileTransfer`` API operation. This ID cannot include spaces.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-profile.html#cfn-transfer-profile-as2id
        '''
        return typing.cast(builtins.str, jsii.get(self, "as2Id"))

    @as2_id.setter
    def as2_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bef576741c4b4bb72ca8ae7bb792ceb2a57aab5736b380d7034eb9a7eb4114d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "as2Id", value)

    @builtins.property
    @jsii.member(jsii_name="profileType")
    def profile_type(self) -> builtins.str:
        '''Indicates whether to list only ``LOCAL`` type profiles or only ``PARTNER`` type profiles.

        If not supplied in the request, the command lists all types of profiles.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-profile.html#cfn-transfer-profile-profiletype
        '''
        return typing.cast(builtins.str, jsii.get(self, "profileType"))

    @profile_type.setter
    def profile_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee2fa6cb852f014c06e7fd08d82e510c6f15af2015a395a30d7c5d59dfb20887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileType", value)

    @builtins.property
    @jsii.member(jsii_name="certificateIds")
    def certificate_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of identifiers for the imported certificates.

        You use this identifier for working with profiles and partner profiles.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-profile.html#cfn-transfer-profile-certificateids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "certificateIds"))

    @certificate_ids.setter
    def certificate_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4edafdae663f5b5b3f80fae40fff73284f051b23b3c64ca6a51d7a62251ce2b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateIds", value)


@jsii.data_type(
    jsii_type="monocdk.aws_transfer.CfnProfileProps",
    jsii_struct_bases=[],
    name_mapping={
        "as2_id": "as2Id",
        "profile_type": "profileType",
        "certificate_ids": "certificateIds",
        "tags": "tags",
    },
)
class CfnProfileProps:
    def __init__(
        self,
        *,
        as2_id: builtins.str,
        profile_type: builtins.str,
        certificate_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnProfile``.

        :param as2_id: The ``As2Id`` is the *AS2-name* , as defined in the `RFC 4130 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc4130>`_ . For inbound transfers, this is the ``AS2-From`` header for the AS2 messages sent from the partner. For outbound connectors, this is the ``AS2-To`` header for the AS2 messages sent to the partner using the ``StartFileTransfer`` API operation. This ID cannot include spaces.
        :param profile_type: Indicates whether to list only ``LOCAL`` type profiles or only ``PARTNER`` type profiles. If not supplied in the request, the command lists all types of profiles.
        :param certificate_ids: An array of identifiers for the imported certificates. You use this identifier for working with profiles and partner profiles.
        :param tags: Key-value pairs that can be used to group and search for profiles.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-profile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_transfer as transfer
            
            cfn_profile_props = transfer.CfnProfileProps(
                as2_id="as2Id",
                profile_type="profileType",
            
                # the properties below are optional
                certificate_ids=["certificateIds"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b098ee24393f17cdbe0789645f469958513aa7a4258564c5d97bc311be3e55f)
            check_type(argname="argument as2_id", value=as2_id, expected_type=type_hints["as2_id"])
            check_type(argname="argument profile_type", value=profile_type, expected_type=type_hints["profile_type"])
            check_type(argname="argument certificate_ids", value=certificate_ids, expected_type=type_hints["certificate_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "as2_id": as2_id,
            "profile_type": profile_type,
        }
        if certificate_ids is not None:
            self._values["certificate_ids"] = certificate_ids
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def as2_id(self) -> builtins.str:
        '''The ``As2Id`` is the *AS2-name* , as defined in the `RFC 4130 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc4130>`_ . For inbound transfers, this is the ``AS2-From`` header for the AS2 messages sent from the partner. For outbound connectors, this is the ``AS2-To`` header for the AS2 messages sent to the partner using the ``StartFileTransfer`` API operation. This ID cannot include spaces.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-profile.html#cfn-transfer-profile-as2id
        '''
        result = self._values.get("as2_id")
        assert result is not None, "Required property 'as2_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def profile_type(self) -> builtins.str:
        '''Indicates whether to list only ``LOCAL`` type profiles or only ``PARTNER`` type profiles.

        If not supplied in the request, the command lists all types of profiles.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-profile.html#cfn-transfer-profile-profiletype
        '''
        result = self._values.get("profile_type")
        assert result is not None, "Required property 'profile_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of identifiers for the imported certificates.

        You use this identifier for working with profiles and partner profiles.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-profile.html#cfn-transfer-profile-certificateids
        '''
        result = self._values.get("certificate_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Key-value pairs that can be used to group and search for profiles.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-profile.html#cfn-transfer-profile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnServer(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_transfer.CfnServer",
):
    '''A CloudFormation ``AWS::Transfer::Server``.

    Instantiates an auto-scaling virtual server based on the selected file transfer protocol in AWS . When you make updates to your file transfer protocol-enabled server or when you work with users, use the service-generated ``ServerId`` property that is assigned to the newly created server.

    :cloudformationResource: AWS::Transfer::Server
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_transfer as transfer
        
        cfn_server = transfer.CfnServer(self, "MyCfnServer",
            certificate="certificate",
            domain="domain",
            endpoint_details=transfer.CfnServer.EndpointDetailsProperty(
                address_allocation_ids=["addressAllocationIds"],
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"],
                vpc_endpoint_id="vpcEndpointId",
                vpc_id="vpcId"
            ),
            endpoint_type="endpointType",
            identity_provider_details=transfer.CfnServer.IdentityProviderDetailsProperty(
                directory_id="directoryId",
                function="function",
                invocation_role="invocationRole",
                url="url"
            ),
            identity_provider_type="identityProviderType",
            logging_role="loggingRole",
            post_authentication_login_banner="postAuthenticationLoginBanner",
            pre_authentication_login_banner="preAuthenticationLoginBanner",
            protocol_details=transfer.CfnServer.ProtocolDetailsProperty(
                as2_transports=["as2Transports"],
                passive_ip="passiveIp",
                set_stat_option="setStatOption",
                tls_session_resumption_mode="tlsSessionResumptionMode"
            ),
            protocols=["protocols"],
            security_policy_name="securityPolicyName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            workflow_details=transfer.CfnServer.WorkflowDetailsProperty(
                on_partial_upload=[transfer.CfnServer.WorkflowDetailProperty(
                    execution_role="executionRole",
                    workflow_id="workflowId"
                )],
                on_upload=[transfer.CfnServer.WorkflowDetailProperty(
                    execution_role="executionRole",
                    workflow_id="workflowId"
                )]
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        certificate: typing.Optional[builtins.str] = None,
        domain: typing.Optional[builtins.str] = None,
        endpoint_details: typing.Optional[typing.Union[typing.Union["CfnServer.EndpointDetailsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        endpoint_type: typing.Optional[builtins.str] = None,
        identity_provider_details: typing.Optional[typing.Union[typing.Union["CfnServer.IdentityProviderDetailsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        identity_provider_type: typing.Optional[builtins.str] = None,
        logging_role: typing.Optional[builtins.str] = None,
        post_authentication_login_banner: typing.Optional[builtins.str] = None,
        pre_authentication_login_banner: typing.Optional[builtins.str] = None,
        protocol_details: typing.Optional[typing.Union[typing.Union["CfnServer.ProtocolDetailsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_policy_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        workflow_details: typing.Optional[typing.Union[typing.Union["CfnServer.WorkflowDetailsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::Transfer::Server``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param certificate: The Amazon Resource Name (ARN) of the AWS Certificate Manager (ACM) certificate. Required when ``Protocols`` is set to ``FTPS`` . To request a new public certificate, see `Request a public certificate <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-public.html>`_ in the *AWS Certificate Manager User Guide* . To import an existing certificate into ACM, see `Importing certificates into ACM <https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html>`_ in the *AWS Certificate Manager User Guide* . To request a private certificate to use FTPS through private IP addresses, see `Request a private certificate <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-private.html>`_ in the *AWS Certificate Manager User Guide* . Certificates with the following cryptographic algorithms and key sizes are supported: - 2048-bit RSA (RSA_2048) - 4096-bit RSA (RSA_4096) - Elliptic Prime Curve 256 bit (EC_prime256v1) - Elliptic Prime Curve 384 bit (EC_secp384r1) - Elliptic Prime Curve 521 bit (EC_secp521r1) .. epigraph:: The certificate must be a valid SSL/TLS X.509 version 3 certificate with FQDN or IP address specified and information about the issuer.
        :param domain: Specifies the domain of the storage system that is used for file transfers.
        :param endpoint_details: The virtual private cloud (VPC) endpoint settings that are configured for your server. When you host your endpoint within your VPC, you can make your endpoint accessible only to resources within your VPC, or you can attach Elastic IP addresses and make your endpoint accessible to clients over the internet. Your VPC's default security groups are automatically assigned to your endpoint.
        :param endpoint_type: The type of endpoint that you want your server to use. You can choose to make your server's endpoint publicly accessible (PUBLIC) or host it inside your VPC. With an endpoint that is hosted in a VPC, you can restrict access to your server and resources only within your VPC or choose to make it internet facing by attaching Elastic IP addresses directly to it.
        :param identity_provider_details: Required when ``IdentityProviderType`` is set to ``AWS_DIRECTORY_SERVICE`` or ``API_GATEWAY`` . Accepts an array containing all of the information required to use a directory in ``AWS_DIRECTORY_SERVICE`` or invoke a customer-supplied authentication API, including the API Gateway URL. Not required when ``IdentityProviderType`` is set to ``SERVICE_MANAGED`` .
        :param identity_provider_type: The mode of authentication for a server. The default value is ``SERVICE_MANAGED`` , which allows you to store and access user credentials within the AWS Transfer Family service. Use ``AWS_DIRECTORY_SERVICE`` to provide access to Active Directory groups in AWS Directory Service for Microsoft Active Directory or Microsoft Active Directory in your on-premises environment or in AWS using AD Connector. This option also requires you to provide a Directory ID by using the ``IdentityProviderDetails`` parameter. Use the ``API_GATEWAY`` value to integrate with an identity provider of your choosing. The ``API_GATEWAY`` setting requires you to provide an Amazon API Gateway endpoint URL to call for authentication by using the ``IdentityProviderDetails`` parameter. Use the ``AWS_LAMBDA`` value to directly use an AWS Lambda function as your identity provider. If you choose this value, you must specify the ARN for the Lambda function in the ``Function`` parameter or the ``IdentityProviderDetails`` data type.
        :param logging_role: The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that allows a server to turn on Amazon CloudWatch logging for Amazon S3 or Amazon EFSevents. When set, you can view user activity in your CloudWatch logs.
        :param post_authentication_login_banner: Specifies a string to display when users connect to a server. This string is displayed after the user authenticates. .. epigraph:: The SFTP protocol does not support post-authentication display banners.
        :param pre_authentication_login_banner: Specifies a string to display when users connect to a server. This string is displayed before the user authenticates. For example, the following banner displays details about using the system: ``This system is for the use of authorized users only. Individuals using this computer system without authority, or in excess of their authority, are subject to having all of their activities on this system monitored and recorded by system personnel.``
        :param protocol_details: The protocol settings that are configured for your server. - To indicate passive mode (for FTP and FTPS protocols), use the ``PassiveIp`` parameter. Enter a single dotted-quad IPv4 address, such as the external IP address of a firewall, router, or load balancer. - To ignore the error that is generated when the client attempts to use the ``SETSTAT`` command on a file that you are uploading to an Amazon S3 bucket, use the ``SetStatOption`` parameter. To have the AWS Transfer Family server ignore the ``SETSTAT`` command and upload files without needing to make any changes to your SFTP client, set the value to ``ENABLE_NO_OP`` . If you set the ``SetStatOption`` parameter to ``ENABLE_NO_OP`` , Transfer Family generates a log entry to Amazon CloudWatch Logs, so that you can determine when the client is making a ``SETSTAT`` call. - To determine whether your AWS Transfer Family server resumes recent, negotiated sessions through a unique session ID, use the ``TlsSessionResumptionMode`` parameter. - ``As2Transports`` indicates the transport method for the AS2 messages. Currently, only HTTP is supported.
        :param protocols: Specifies the file transfer protocol or protocols over which your file transfer protocol client can connect to your server's endpoint. The available protocols are: - ``SFTP`` (Secure Shell (SSH) File Transfer Protocol): File transfer over SSH - ``FTPS`` (File Transfer Protocol Secure): File transfer with TLS encryption - ``FTP`` (File Transfer Protocol): Unencrypted file transfer - ``AS2`` (Applicability Statement 2): used for transporting structured business-to-business data .. epigraph:: - If you select ``FTPS`` , you must choose a certificate stored in AWS Certificate Manager (ACM) which is used to identify your server when clients connect to it over FTPS. - If ``Protocol`` includes either ``FTP`` or ``FTPS`` , then the ``EndpointType`` must be ``VPC`` and the ``IdentityProviderType`` must be either ``AWS_DIRECTORY_SERVICE`` , ``AWS_LAMBDA`` , or ``API_GATEWAY`` . - If ``Protocol`` includes ``FTP`` , then ``AddressAllocationIds`` cannot be associated. - If ``Protocol`` is set only to ``SFTP`` , the ``EndpointType`` can be set to ``PUBLIC`` and the ``IdentityProviderType`` can be set any of the supported identity types: ``SERVICE_MANAGED`` , ``AWS_DIRECTORY_SERVICE`` , ``AWS_LAMBDA`` , or ``API_GATEWAY`` . - If ``Protocol`` includes ``AS2`` , then the ``EndpointType`` must be ``VPC`` , and domain must be Amazon S3.
        :param security_policy_name: Specifies the name of the security policy that is attached to the server.
        :param tags: Key-value pairs that can be used to group and search for servers.
        :param workflow_details: Specifies the workflow ID for the workflow to assign and the execution role that's used for executing the workflow. In addition to a workflow to execute when a file is uploaded completely, ``WorkflowDetails`` can also contain a workflow ID (and execution role) for a workflow to execute on partial upload. A partial upload occurs when a file is open when the session disconnects.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d9bf7e751a0730ea2df11510a4080e1fd8fb0aa877bd8a8ef4cccc6a04cf511)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServerProps(
            certificate=certificate,
            domain=domain,
            endpoint_details=endpoint_details,
            endpoint_type=endpoint_type,
            identity_provider_details=identity_provider_details,
            identity_provider_type=identity_provider_type,
            logging_role=logging_role,
            post_authentication_login_banner=post_authentication_login_banner,
            pre_authentication_login_banner=pre_authentication_login_banner,
            protocol_details=protocol_details,
            protocols=protocols,
            security_policy_name=security_policy_name,
            tags=tags,
            workflow_details=workflow_details,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee508fc6cfb0790567e3b88faa66829b940207c7b7a40bdfb30906e8e011a66a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__628449ae5bca14d695aa159e94885ec91d6027ed72730616a8f78be614b5b970)
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
        '''The Amazon Resource Name associated with the server, in the form ``arn:aws:transfer:region: *account-id* :server/ *server-id* /`` .

        An example of a server ARN is: ``arn:aws:transfer:us-east-1:123456789012:server/s-01234567890abcdef`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrServerId")
    def attr_server_id(self) -> builtins.str:
        '''The service-assigned ID of the server that is created.

        An example ``ServerId`` is ``s-01234567890abcdef`` .

        :cloudformationAttribute: ServerId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServerId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Key-value pairs that can be used to group and search for servers.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS Certificate Manager (ACM) certificate.

        Required when ``Protocols`` is set to ``FTPS`` .

        To request a new public certificate, see `Request a public certificate <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-public.html>`_ in the *AWS Certificate Manager User Guide* .

        To import an existing certificate into ACM, see `Importing certificates into ACM <https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html>`_ in the *AWS Certificate Manager User Guide* .

        To request a private certificate to use FTPS through private IP addresses, see `Request a private certificate <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-private.html>`_ in the *AWS Certificate Manager User Guide* .

        Certificates with the following cryptographic algorithms and key sizes are supported:

        - 2048-bit RSA (RSA_2048)
        - 4096-bit RSA (RSA_4096)
        - Elliptic Prime Curve 256 bit (EC_prime256v1)
        - Elliptic Prime Curve 384 bit (EC_secp384r1)
        - Elliptic Prime Curve 521 bit (EC_secp521r1)

        .. epigraph::

           The certificate must be a valid SSL/TLS X.509 version 3 certificate with FQDN or IP address specified and information about the issuer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-certificate
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eceec3cdaad0f84bd64bc19530c7678e8d44c996fad04b7cdb8a6b1e117cc99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> typing.Optional[builtins.str]:
        '''Specifies the domain of the storage system that is used for file transfers.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-domain
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33b24d42be648882df8c049b485bb5b9d6fb665c3eaecfc6a26e2a1615037770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value)

    @builtins.property
    @jsii.member(jsii_name="endpointDetails")
    def endpoint_details(
        self,
    ) -> typing.Optional[typing.Union["CfnServer.EndpointDetailsProperty", _IResolvable_a771d0ef]]:
        '''The virtual private cloud (VPC) endpoint settings that are configured for your server.

        When you host your endpoint within your VPC, you can make your endpoint accessible only to resources within your VPC, or you can attach Elastic IP addresses and make your endpoint accessible to clients over the internet. Your VPC's default security groups are automatically assigned to your endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-endpointdetails
        '''
        return typing.cast(typing.Optional[typing.Union["CfnServer.EndpointDetailsProperty", _IResolvable_a771d0ef]], jsii.get(self, "endpointDetails"))

    @endpoint_details.setter
    def endpoint_details(
        self,
        value: typing.Optional[typing.Union["CfnServer.EndpointDetailsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__509b3b21f54fc905415cd934bc12a170bf7dc5b9ae17e822ab5a356b17dc2a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointDetails", value)

    @builtins.property
    @jsii.member(jsii_name="endpointType")
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        '''The type of endpoint that you want your server to use.

        You can choose to make your server's endpoint publicly accessible (PUBLIC) or host it inside your VPC. With an endpoint that is hosted in a VPC, you can restrict access to your server and resources only within your VPC or choose to make it internet facing by attaching Elastic IP addresses directly to it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-endpointtype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointType"))

    @endpoint_type.setter
    def endpoint_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81552e27323810d71b87571f785bb22344c9eaa43d096d71aa1dfe1602acf898)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointType", value)

    @builtins.property
    @jsii.member(jsii_name="identityProviderDetails")
    def identity_provider_details(
        self,
    ) -> typing.Optional[typing.Union["CfnServer.IdentityProviderDetailsProperty", _IResolvable_a771d0ef]]:
        '''Required when ``IdentityProviderType`` is set to ``AWS_DIRECTORY_SERVICE`` or ``API_GATEWAY`` .

        Accepts an array containing all of the information required to use a directory in ``AWS_DIRECTORY_SERVICE`` or invoke a customer-supplied authentication API, including the API Gateway URL. Not required when ``IdentityProviderType`` is set to ``SERVICE_MANAGED`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-identityproviderdetails
        '''
        return typing.cast(typing.Optional[typing.Union["CfnServer.IdentityProviderDetailsProperty", _IResolvable_a771d0ef]], jsii.get(self, "identityProviderDetails"))

    @identity_provider_details.setter
    def identity_provider_details(
        self,
        value: typing.Optional[typing.Union["CfnServer.IdentityProviderDetailsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e25062a39baf983e3131469ee48f4c33522360ed64817c8ef7b047ede35ecc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProviderDetails", value)

    @builtins.property
    @jsii.member(jsii_name="identityProviderType")
    def identity_provider_type(self) -> typing.Optional[builtins.str]:
        '''The mode of authentication for a server.

        The default value is ``SERVICE_MANAGED`` , which allows you to store and access user credentials within the AWS Transfer Family service.

        Use ``AWS_DIRECTORY_SERVICE`` to provide access to Active Directory groups in AWS Directory Service for Microsoft Active Directory or Microsoft Active Directory in your on-premises environment or in AWS using AD Connector. This option also requires you to provide a Directory ID by using the ``IdentityProviderDetails`` parameter.

        Use the ``API_GATEWAY`` value to integrate with an identity provider of your choosing. The ``API_GATEWAY`` setting requires you to provide an Amazon API Gateway endpoint URL to call for authentication by using the ``IdentityProviderDetails`` parameter.

        Use the ``AWS_LAMBDA`` value to directly use an AWS Lambda function as your identity provider. If you choose this value, you must specify the ARN for the Lambda function in the ``Function`` parameter or the ``IdentityProviderDetails`` data type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-identityprovidertype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityProviderType"))

    @identity_provider_type.setter
    def identity_provider_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c189403fd2efaf177ae31b001970dabc32612e9c998d4be759abbb6f3147773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProviderType", value)

    @builtins.property
    @jsii.member(jsii_name="loggingRole")
    def logging_role(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that allows a server to turn on Amazon CloudWatch logging for Amazon S3 or Amazon EFSevents.

        When set, you can view user activity in your CloudWatch logs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-loggingrole
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loggingRole"))

    @logging_role.setter
    def logging_role(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00431c85189d75ae5f73627be25a0110e5335ccb11fd2655fa51c4c4f23fcba0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingRole", value)

    @builtins.property
    @jsii.member(jsii_name="postAuthenticationLoginBanner")
    def post_authentication_login_banner(self) -> typing.Optional[builtins.str]:
        '''Specifies a string to display when users connect to a server. This string is displayed after the user authenticates.

        .. epigraph::

           The SFTP protocol does not support post-authentication display banners.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-postauthenticationloginbanner
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postAuthenticationLoginBanner"))

    @post_authentication_login_banner.setter
    def post_authentication_login_banner(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f186ac6bf763e3e0ff1f072779f105b571e0c764b9353155b9697097b7fbe9fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postAuthenticationLoginBanner", value)

    @builtins.property
    @jsii.member(jsii_name="preAuthenticationLoginBanner")
    def pre_authentication_login_banner(self) -> typing.Optional[builtins.str]:
        '''Specifies a string to display when users connect to a server.

        This string is displayed before the user authenticates. For example, the following banner displays details about using the system:

        ``This system is for the use of authorized users only. Individuals using this computer system without authority, or in excess of their authority, are subject to having all of their activities on this system monitored and recorded by system personnel.``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-preauthenticationloginbanner
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preAuthenticationLoginBanner"))

    @pre_authentication_login_banner.setter
    def pre_authentication_login_banner(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e82252e450e05ae66e08c314a4bf4dc773a3431c2617250ad84989f371eeef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preAuthenticationLoginBanner", value)

    @builtins.property
    @jsii.member(jsii_name="protocolDetails")
    def protocol_details(
        self,
    ) -> typing.Optional[typing.Union["CfnServer.ProtocolDetailsProperty", _IResolvable_a771d0ef]]:
        '''The protocol settings that are configured for your server.

        - To indicate passive mode (for FTP and FTPS protocols), use the ``PassiveIp`` parameter. Enter a single dotted-quad IPv4 address, such as the external IP address of a firewall, router, or load balancer.
        - To ignore the error that is generated when the client attempts to use the ``SETSTAT`` command on a file that you are uploading to an Amazon S3 bucket, use the ``SetStatOption`` parameter. To have the AWS Transfer Family server ignore the ``SETSTAT`` command and upload files without needing to make any changes to your SFTP client, set the value to ``ENABLE_NO_OP`` . If you set the ``SetStatOption`` parameter to ``ENABLE_NO_OP`` , Transfer Family generates a log entry to Amazon CloudWatch Logs, so that you can determine when the client is making a ``SETSTAT`` call.
        - To determine whether your AWS Transfer Family server resumes recent, negotiated sessions through a unique session ID, use the ``TlsSessionResumptionMode`` parameter.
        - ``As2Transports`` indicates the transport method for the AS2 messages. Currently, only HTTP is supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-protocoldetails
        '''
        return typing.cast(typing.Optional[typing.Union["CfnServer.ProtocolDetailsProperty", _IResolvable_a771d0ef]], jsii.get(self, "protocolDetails"))

    @protocol_details.setter
    def protocol_details(
        self,
        value: typing.Optional[typing.Union["CfnServer.ProtocolDetailsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94208a56d565c10ddedac8b79ee054fc14650c8b71712542cc1c3b6c6f02b0a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolDetails", value)

    @builtins.property
    @jsii.member(jsii_name="protocols")
    def protocols(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the file transfer protocol or protocols over which your file transfer protocol client can connect to your server's endpoint.

        The available protocols are:

        - ``SFTP`` (Secure Shell (SSH) File Transfer Protocol): File transfer over SSH
        - ``FTPS`` (File Transfer Protocol Secure): File transfer with TLS encryption
        - ``FTP`` (File Transfer Protocol): Unencrypted file transfer
        - ``AS2`` (Applicability Statement 2): used for transporting structured business-to-business data

        .. epigraph::

           - If you select ``FTPS`` , you must choose a certificate stored in AWS Certificate Manager (ACM) which is used to identify your server when clients connect to it over FTPS.
           - If ``Protocol`` includes either ``FTP`` or ``FTPS`` , then the ``EndpointType`` must be ``VPC`` and the ``IdentityProviderType`` must be either ``AWS_DIRECTORY_SERVICE`` , ``AWS_LAMBDA`` , or ``API_GATEWAY`` .
           - If ``Protocol`` includes ``FTP`` , then ``AddressAllocationIds`` cannot be associated.
           - If ``Protocol`` is set only to ``SFTP`` , the ``EndpointType`` can be set to ``PUBLIC`` and the ``IdentityProviderType`` can be set any of the supported identity types: ``SERVICE_MANAGED`` , ``AWS_DIRECTORY_SERVICE`` , ``AWS_LAMBDA`` , or ``API_GATEWAY`` .
           - If ``Protocol`` includes ``AS2`` , then the ``EndpointType`` must be ``VPC`` , and domain must be Amazon S3.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-protocols
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "protocols"))

    @protocols.setter
    def protocols(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4aa06bbc2a56d1bea2584e2dd86acc645caf049f7ac5840468e302435bf7e63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocols", value)

    @builtins.property
    @jsii.member(jsii_name="securityPolicyName")
    def security_policy_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the security policy that is attached to the server.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-securitypolicyname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityPolicyName"))

    @security_policy_name.setter
    def security_policy_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e034e555acbdc422eda08639e550ae3c67b4b324294aa1c023e659d87e54d77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityPolicyName", value)

    @builtins.property
    @jsii.member(jsii_name="workflowDetails")
    def workflow_details(
        self,
    ) -> typing.Optional[typing.Union["CfnServer.WorkflowDetailsProperty", _IResolvable_a771d0ef]]:
        '''Specifies the workflow ID for the workflow to assign and the execution role that's used for executing the workflow.

        In addition to a workflow to execute when a file is uploaded completely, ``WorkflowDetails`` can also contain a workflow ID (and execution role) for a workflow to execute on partial upload. A partial upload occurs when a file is open when the session disconnects.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-workflowdetails
        '''
        return typing.cast(typing.Optional[typing.Union["CfnServer.WorkflowDetailsProperty", _IResolvable_a771d0ef]], jsii.get(self, "workflowDetails"))

    @workflow_details.setter
    def workflow_details(
        self,
        value: typing.Optional[typing.Union["CfnServer.WorkflowDetailsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__214c68c65a7c0f3e45e763adf074c0d0fda039ca811dad4d1c66bf0c7418481e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workflowDetails", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_transfer.CfnServer.EndpointDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "address_allocation_ids": "addressAllocationIds",
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
            "vpc_endpoint_id": "vpcEndpointId",
            "vpc_id": "vpcId",
        },
    )
    class EndpointDetailsProperty:
        def __init__(
            self,
            *,
            address_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            vpc_endpoint_id: typing.Optional[builtins.str] = None,
            vpc_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The virtual private cloud (VPC) endpoint settings that are configured for your server.

            When you host your endpoint within your VPC, you can make your endpoint accessible only to resources within your VPC, or you can attach Elastic IP addresses and make your endpoint accessible to clients over the internet. Your VPC's default security groups are automatically assigned to your endpoint.

            :param address_allocation_ids: A list of address allocation IDs that are required to attach an Elastic IP address to your server's endpoint. .. epigraph:: This property can only be set when ``EndpointType`` is set to ``VPC`` and it is only valid in the ``UpdateServer`` API.
            :param security_group_ids: A list of security groups IDs that are available to attach to your server's endpoint. .. epigraph:: This property can only be set when ``EndpointType`` is set to ``VPC`` . You can edit the ``SecurityGroupIds`` property in the `UpdateServer <https://docs.aws.amazon.com/transfer/latest/userguide/API_UpdateServer.html>`_ API only if you are changing the ``EndpointType`` from ``PUBLIC`` or ``VPC_ENDPOINT`` to ``VPC`` . To change security groups associated with your server's VPC endpoint after creation, use the Amazon EC2 `ModifyVpcEndpoint <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyVpcEndpoint.html>`_ API.
            :param subnet_ids: A list of subnet IDs that are required to host your server endpoint in your VPC. .. epigraph:: This property can only be set when ``EndpointType`` is set to ``VPC`` .
            :param vpc_endpoint_id: The ID of the VPC endpoint. .. epigraph:: This property can only be set when ``EndpointType`` is set to ``VPC_ENDPOINT`` .
            :param vpc_id: The VPC ID of the virtual private cloud in which the server's endpoint will be hosted. .. epigraph:: This property can only be set when ``EndpointType`` is set to ``VPC`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_transfer as transfer
                
                endpoint_details_property = transfer.CfnServer.EndpointDetailsProperty(
                    address_allocation_ids=["addressAllocationIds"],
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"],
                    vpc_endpoint_id="vpcEndpointId",
                    vpc_id="vpcId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a676ac4c89bd836d2f828f0b22f4dd67bd533227c3728c9f2e7de26aa619f07)
                check_type(argname="argument address_allocation_ids", value=address_allocation_ids, expected_type=type_hints["address_allocation_ids"])
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
                check_type(argname="argument vpc_endpoint_id", value=vpc_endpoint_id, expected_type=type_hints["vpc_endpoint_id"])
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address_allocation_ids is not None:
                self._values["address_allocation_ids"] = address_allocation_ids
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids
            if vpc_endpoint_id is not None:
                self._values["vpc_endpoint_id"] = vpc_endpoint_id
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def address_allocation_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of address allocation IDs that are required to attach an Elastic IP address to your server's endpoint.

            .. epigraph::

               This property can only be set when ``EndpointType`` is set to ``VPC`` and it is only valid in the ``UpdateServer`` API.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html#cfn-transfer-server-endpointdetails-addressallocationids
            '''
            result = self._values.get("address_allocation_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of security groups IDs that are available to attach to your server's endpoint.

            .. epigraph::

               This property can only be set when ``EndpointType`` is set to ``VPC`` .

               You can edit the ``SecurityGroupIds`` property in the `UpdateServer <https://docs.aws.amazon.com/transfer/latest/userguide/API_UpdateServer.html>`_ API only if you are changing the ``EndpointType`` from ``PUBLIC`` or ``VPC_ENDPOINT`` to ``VPC`` . To change security groups associated with your server's VPC endpoint after creation, use the Amazon EC2 `ModifyVpcEndpoint <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyVpcEndpoint.html>`_ API.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html#cfn-transfer-server-endpointdetails-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of subnet IDs that are required to host your server endpoint in your VPC.

            .. epigraph::

               This property can only be set when ``EndpointType`` is set to ``VPC`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html#cfn-transfer-server-endpointdetails-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def vpc_endpoint_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the VPC endpoint.

            .. epigraph::

               This property can only be set when ``EndpointType`` is set to ``VPC_ENDPOINT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html#cfn-transfer-server-endpointdetails-vpcendpointid
            '''
            result = self._values.get("vpc_endpoint_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''The VPC ID of the virtual private cloud in which the server's endpoint will be hosted.

            .. epigraph::

               This property can only be set when ``EndpointType`` is set to ``VPC`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html#cfn-transfer-server-endpointdetails-vpcid
            '''
            result = self._values.get("vpc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_transfer.CfnServer.IdentityProviderDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "directory_id": "directoryId",
            "function": "function",
            "invocation_role": "invocationRole",
            "url": "url",
        },
    )
    class IdentityProviderDetailsProperty:
        def __init__(
            self,
            *,
            directory_id: typing.Optional[builtins.str] = None,
            function: typing.Optional[builtins.str] = None,
            invocation_role: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Required when ``IdentityProviderType`` is set to ``AWS_DIRECTORY_SERVICE`` or ``API_GATEWAY`` .

            Accepts an array containing all of the information required to use a directory in ``AWS_DIRECTORY_SERVICE`` or invoke a customer-supplied authentication API, including the API Gateway URL. Not required when ``IdentityProviderType`` is set to ``SERVICE_MANAGED`` .

            :param directory_id: The identifier of the AWS Directory Service directory that you want to stop sharing.
            :param function: The ARN for a lambda function to use for the Identity provider.
            :param invocation_role: Provides the type of ``InvocationRole`` used to authenticate the user account.
            :param url: Provides the location of the service endpoint used to authenticate users.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-identityproviderdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_transfer as transfer
                
                identity_provider_details_property = transfer.CfnServer.IdentityProviderDetailsProperty(
                    directory_id="directoryId",
                    function="function",
                    invocation_role="invocationRole",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7b9df9ad578d061e8e01d8c63353ac3d9a3c7f83484840ea793274cce5a417b4)
                check_type(argname="argument directory_id", value=directory_id, expected_type=type_hints["directory_id"])
                check_type(argname="argument function", value=function, expected_type=type_hints["function"])
                check_type(argname="argument invocation_role", value=invocation_role, expected_type=type_hints["invocation_role"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if directory_id is not None:
                self._values["directory_id"] = directory_id
            if function is not None:
                self._values["function"] = function
            if invocation_role is not None:
                self._values["invocation_role"] = invocation_role
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def directory_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the AWS Directory Service directory that you want to stop sharing.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-identityproviderdetails.html#cfn-transfer-server-identityproviderdetails-directoryid
            '''
            result = self._values.get("directory_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def function(self) -> typing.Optional[builtins.str]:
            '''The ARN for a lambda function to use for the Identity provider.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-identityproviderdetails.html#cfn-transfer-server-identityproviderdetails-function
            '''
            result = self._values.get("function")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def invocation_role(self) -> typing.Optional[builtins.str]:
            '''Provides the type of ``InvocationRole`` used to authenticate the user account.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-identityproviderdetails.html#cfn-transfer-server-identityproviderdetails-invocationrole
            '''
            result = self._values.get("invocation_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''Provides the location of the service endpoint used to authenticate users.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-identityproviderdetails.html#cfn-transfer-server-identityproviderdetails-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdentityProviderDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_transfer.CfnServer.ProtocolDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "as2_transports": "as2Transports",
            "passive_ip": "passiveIp",
            "set_stat_option": "setStatOption",
            "tls_session_resumption_mode": "tlsSessionResumptionMode",
        },
    )
    class ProtocolDetailsProperty:
        def __init__(
            self,
            *,
            as2_transports: typing.Optional[typing.Sequence[builtins.str]] = None,
            passive_ip: typing.Optional[builtins.str] = None,
            set_stat_option: typing.Optional[builtins.str] = None,
            tls_session_resumption_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Protocol settings that are configured for your server.

            :param as2_transports: List of ``As2Transport`` objects.
            :param passive_ip: Indicates passive mode, for FTP and FTPS protocols. Enter a single IPv4 address, such as the public IP address of a firewall, router, or load balancer. For example: ``aws transfer update-server --protocol-details PassiveIp=0.0.0.0`` Replace ``0.0.0.0`` in the example above with the actual IP address you want to use. .. epigraph:: If you change the ``PassiveIp`` value, you must stop and then restart your Transfer Family server for the change to take effect. For details on using passive mode (PASV) in a NAT environment, see `Configuring your FTPS server behind a firewall or NAT with AWS Transfer Family <https://docs.aws.amazon.com/storage/configuring-your-ftps-server-behind-a-firewall-or-nat-with-aws-transfer-family/>`_ . *Special values* The ``AUTO`` and ``0.0.0.0`` are special values for the ``PassiveIp`` parameter. The value ``PassiveIp=AUTO`` is assigned by default to FTP and FTPS type servers. In this case, the server automatically responds with one of the endpoint IPs within the PASV response. ``PassiveIp=0.0.0.0`` has a more unique application for its usage. For example, if you have a High Availability (HA) Network Load Balancer (NLB) environment, where you have 3 subnets, you can only specify a single IP address using the ``PassiveIp`` parameter. This reduces the effectiveness of having High Availability. In this case, you can specify ``PassiveIp=0.0.0.0`` . This tells the client to use the same IP address as the Control connection and utilize all AZs for their connections. Note, however, that not all FTP clients support the ``PassiveIp=0.0.0.0`` response. FileZilla and WinSCP do support it. If you are using other clients, check to see if your client supports the ``PassiveIp=0.0.0.0`` response.
            :param set_stat_option: Use the ``SetStatOption`` to ignore the error that is generated when the client attempts to use ``SETSTAT`` on a file you are uploading to an S3 bucket. Some SFTP file transfer clients can attempt to change the attributes of remote files, including timestamp and permissions, using commands, such as ``SETSTAT`` when uploading the file. However, these commands are not compatible with object storage systems, such as Amazon S3. Due to this incompatibility, file uploads from these clients can result in errors even when the file is otherwise successfully uploaded. Set the value to ``ENABLE_NO_OP`` to have the Transfer Family server ignore the ``SETSTAT`` command, and upload files without needing to make any changes to your SFTP client. While the ``SetStatOption`` ``ENABLE_NO_OP`` setting ignores the error, it does generate a log entry in Amazon CloudWatch Logs, so you can determine when the client is making a ``SETSTAT`` call. .. epigraph:: If you want to preserve the original timestamp for your file, and modify other file attributes using ``SETSTAT`` , you can use Amazon EFS as backend storage with Transfer Family.
            :param tls_session_resumption_mode: A property used with Transfer Family servers that use the FTPS protocol. TLS Session Resumption provides a mechanism to resume or share a negotiated secret key between the control and data connection for an FTPS session. ``TlsSessionResumptionMode`` determines whether or not the server resumes recent, negotiated sessions through a unique session ID. This property is available during ``CreateServer`` and ``UpdateServer`` calls. If a ``TlsSessionResumptionMode`` value is not specified during ``CreateServer`` , it is set to ``ENFORCED`` by default. - ``DISABLED`` : the server does not process TLS session resumption client requests and creates a new TLS session for each request. - ``ENABLED`` : the server processes and accepts clients that are performing TLS session resumption. The server doesn't reject client data connections that do not perform the TLS session resumption client processing. - ``ENFORCED`` : the server processes and accepts clients that are performing TLS session resumption. The server rejects client data connections that do not perform the TLS session resumption client processing. Before you set the value to ``ENFORCED`` , test your clients. .. epigraph:: Not all FTPS clients perform TLS session resumption. So, if you choose to enforce TLS session resumption, you prevent any connections from FTPS clients that don't perform the protocol negotiation. To determine whether or not you can use the ``ENFORCED`` value, you need to test your clients.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-protocoldetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_transfer as transfer
                
                protocol_details_property = transfer.CfnServer.ProtocolDetailsProperty(
                    as2_transports=["as2Transports"],
                    passive_ip="passiveIp",
                    set_stat_option="setStatOption",
                    tls_session_resumption_mode="tlsSessionResumptionMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c49b75d67550e4173969ef74afe66d171181eb35103f7f7a265e94c4f9ab478c)
                check_type(argname="argument as2_transports", value=as2_transports, expected_type=type_hints["as2_transports"])
                check_type(argname="argument passive_ip", value=passive_ip, expected_type=type_hints["passive_ip"])
                check_type(argname="argument set_stat_option", value=set_stat_option, expected_type=type_hints["set_stat_option"])
                check_type(argname="argument tls_session_resumption_mode", value=tls_session_resumption_mode, expected_type=type_hints["tls_session_resumption_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if as2_transports is not None:
                self._values["as2_transports"] = as2_transports
            if passive_ip is not None:
                self._values["passive_ip"] = passive_ip
            if set_stat_option is not None:
                self._values["set_stat_option"] = set_stat_option
            if tls_session_resumption_mode is not None:
                self._values["tls_session_resumption_mode"] = tls_session_resumption_mode

        @builtins.property
        def as2_transports(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of ``As2Transport`` objects.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-protocoldetails.html#cfn-transfer-server-protocoldetails-as2transports
            '''
            result = self._values.get("as2_transports")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def passive_ip(self) -> typing.Optional[builtins.str]:
            '''Indicates passive mode, for FTP and FTPS protocols.

            Enter a single IPv4 address, such as the public IP address of a firewall, router, or load balancer. For example:

            ``aws transfer update-server --protocol-details PassiveIp=0.0.0.0``

            Replace ``0.0.0.0`` in the example above with the actual IP address you want to use.
            .. epigraph::

               If you change the ``PassiveIp`` value, you must stop and then restart your Transfer Family server for the change to take effect. For details on using passive mode (PASV) in a NAT environment, see `Configuring your FTPS server behind a firewall or NAT with AWS Transfer Family <https://docs.aws.amazon.com/storage/configuring-your-ftps-server-behind-a-firewall-or-nat-with-aws-transfer-family/>`_ .

            *Special values*

            The ``AUTO`` and ``0.0.0.0`` are special values for the ``PassiveIp`` parameter. The value ``PassiveIp=AUTO`` is assigned by default to FTP and FTPS type servers. In this case, the server automatically responds with one of the endpoint IPs within the PASV response. ``PassiveIp=0.0.0.0`` has a more unique application for its usage. For example, if you have a High Availability (HA) Network Load Balancer (NLB) environment, where you have 3 subnets, you can only specify a single IP address using the ``PassiveIp`` parameter. This reduces the effectiveness of having High Availability. In this case, you can specify ``PassiveIp=0.0.0.0`` . This tells the client to use the same IP address as the Control connection and utilize all AZs for their connections. Note, however, that not all FTP clients support the ``PassiveIp=0.0.0.0`` response. FileZilla and WinSCP do support it. If you are using other clients, check to see if your client supports the ``PassiveIp=0.0.0.0`` response.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-protocoldetails.html#cfn-transfer-server-protocoldetails-passiveip
            '''
            result = self._values.get("passive_ip")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def set_stat_option(self) -> typing.Optional[builtins.str]:
            '''Use the ``SetStatOption`` to ignore the error that is generated when the client attempts to use ``SETSTAT`` on a file you are uploading to an S3 bucket.

            Some SFTP file transfer clients can attempt to change the attributes of remote files, including timestamp and permissions, using commands, such as ``SETSTAT`` when uploading the file. However, these commands are not compatible with object storage systems, such as Amazon S3. Due to this incompatibility, file uploads from these clients can result in errors even when the file is otherwise successfully uploaded.

            Set the value to ``ENABLE_NO_OP`` to have the Transfer Family server ignore the ``SETSTAT`` command, and upload files without needing to make any changes to your SFTP client. While the ``SetStatOption`` ``ENABLE_NO_OP`` setting ignores the error, it does generate a log entry in Amazon CloudWatch Logs, so you can determine when the client is making a ``SETSTAT`` call.
            .. epigraph::

               If you want to preserve the original timestamp for your file, and modify other file attributes using ``SETSTAT`` , you can use Amazon EFS as backend storage with Transfer Family.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-protocoldetails.html#cfn-transfer-server-protocoldetails-setstatoption
            '''
            result = self._values.get("set_stat_option")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tls_session_resumption_mode(self) -> typing.Optional[builtins.str]:
            '''A property used with Transfer Family servers that use the FTPS protocol.

            TLS Session Resumption provides a mechanism to resume or share a negotiated secret key between the control and data connection for an FTPS session. ``TlsSessionResumptionMode`` determines whether or not the server resumes recent, negotiated sessions through a unique session ID. This property is available during ``CreateServer`` and ``UpdateServer`` calls. If a ``TlsSessionResumptionMode`` value is not specified during ``CreateServer`` , it is set to ``ENFORCED`` by default.

            - ``DISABLED`` : the server does not process TLS session resumption client requests and creates a new TLS session for each request.
            - ``ENABLED`` : the server processes and accepts clients that are performing TLS session resumption. The server doesn't reject client data connections that do not perform the TLS session resumption client processing.
            - ``ENFORCED`` : the server processes and accepts clients that are performing TLS session resumption. The server rejects client data connections that do not perform the TLS session resumption client processing. Before you set the value to ``ENFORCED`` , test your clients.

            .. epigraph::

               Not all FTPS clients perform TLS session resumption. So, if you choose to enforce TLS session resumption, you prevent any connections from FTPS clients that don't perform the protocol negotiation. To determine whether or not you can use the ``ENFORCED`` value, you need to test your clients.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-protocoldetails.html#cfn-transfer-server-protocoldetails-tlssessionresumptionmode
            '''
            result = self._values.get("tls_session_resumption_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProtocolDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_transfer.CfnServer.WorkflowDetailProperty",
        jsii_struct_bases=[],
        name_mapping={"execution_role": "executionRole", "workflow_id": "workflowId"},
    )
    class WorkflowDetailProperty:
        def __init__(
            self,
            *,
            execution_role: builtins.str,
            workflow_id: builtins.str,
        ) -> None:
            '''Specifies the workflow ID for the workflow to assign and the execution role that's used for executing the workflow.

            In addition to a workflow to execute when a file is uploaded completely, ``WorkflowDetails`` can also contain a workflow ID (and execution role) for a workflow to execute on partial upload. A partial upload occurs when a file is open when the session disconnects.

            :param execution_role: Includes the necessary permissions for S3, EFS, and Lambda operations that Transfer can assume, so that all workflow steps can operate on the required resources.
            :param workflow_id: A unique identifier for the workflow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-workflowdetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_transfer as transfer
                
                workflow_detail_property = transfer.CfnServer.WorkflowDetailProperty(
                    execution_role="executionRole",
                    workflow_id="workflowId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__17849a405a080c9f8ea5d8627fadee3faf08fb13e5cbb2cfa037346f67321ffb)
                check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
                check_type(argname="argument workflow_id", value=workflow_id, expected_type=type_hints["workflow_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "execution_role": execution_role,
                "workflow_id": workflow_id,
            }

        @builtins.property
        def execution_role(self) -> builtins.str:
            '''Includes the necessary permissions for S3, EFS, and Lambda operations that Transfer can assume, so that all workflow steps can operate on the required resources.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-workflowdetail.html#cfn-transfer-server-workflowdetail-executionrole
            '''
            result = self._values.get("execution_role")
            assert result is not None, "Required property 'execution_role' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def workflow_id(self) -> builtins.str:
            '''A unique identifier for the workflow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-workflowdetail.html#cfn-transfer-server-workflowdetail-workflowid
            '''
            result = self._values.get("workflow_id")
            assert result is not None, "Required property 'workflow_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkflowDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_transfer.CfnServer.WorkflowDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"on_partial_upload": "onPartialUpload", "on_upload": "onUpload"},
    )
    class WorkflowDetailsProperty:
        def __init__(
            self,
            *,
            on_partial_upload: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnServer.WorkflowDetailProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            on_upload: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnServer.WorkflowDetailProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''Container for the ``WorkflowDetail`` data type.

            It is used by actions that trigger a workflow to begin execution.

            :param on_partial_upload: A trigger that starts a workflow if a file is only partially uploaded. You can attach a workflow to a server that executes whenever there is a partial upload. A *partial upload* occurs when a file is open when the session disconnects.
            :param on_upload: A trigger that starts a workflow: the workflow begins to execute after a file is uploaded. To remove an associated workflow from a server, you can provide an empty ``OnUpload`` object, as in the following example. ``aws transfer update-server --server-id s-01234567890abcdef --workflow-details '{"OnUpload":[]}'``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-workflowdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_transfer as transfer
                
                workflow_details_property = transfer.CfnServer.WorkflowDetailsProperty(
                    on_partial_upload=[transfer.CfnServer.WorkflowDetailProperty(
                        execution_role="executionRole",
                        workflow_id="workflowId"
                    )],
                    on_upload=[transfer.CfnServer.WorkflowDetailProperty(
                        execution_role="executionRole",
                        workflow_id="workflowId"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7654f3686762abc0f070cc9055a19b439d8c910e8a82727eb5b3ebeb80b3bb28)
                check_type(argname="argument on_partial_upload", value=on_partial_upload, expected_type=type_hints["on_partial_upload"])
                check_type(argname="argument on_upload", value=on_upload, expected_type=type_hints["on_upload"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if on_partial_upload is not None:
                self._values["on_partial_upload"] = on_partial_upload
            if on_upload is not None:
                self._values["on_upload"] = on_upload

        @builtins.property
        def on_partial_upload(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnServer.WorkflowDetailProperty", _IResolvable_a771d0ef]]]]:
            '''A trigger that starts a workflow if a file is only partially uploaded.

            You can attach a workflow to a server that executes whenever there is a partial upload.

            A *partial upload* occurs when a file is open when the session disconnects.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-workflowdetails.html#cfn-transfer-server-workflowdetails-onpartialupload
            '''
            result = self._values.get("on_partial_upload")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnServer.WorkflowDetailProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def on_upload(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnServer.WorkflowDetailProperty", _IResolvable_a771d0ef]]]]:
            '''A trigger that starts a workflow: the workflow begins to execute after a file is uploaded.

            To remove an associated workflow from a server, you can provide an empty ``OnUpload`` object, as in the following example.

            ``aws transfer update-server --server-id s-01234567890abcdef --workflow-details '{"OnUpload":[]}'``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-workflowdetails.html#cfn-transfer-server-workflowdetails-onupload
            '''
            result = self._values.get("on_upload")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnServer.WorkflowDetailProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkflowDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_transfer.CfnServerProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate": "certificate",
        "domain": "domain",
        "endpoint_details": "endpointDetails",
        "endpoint_type": "endpointType",
        "identity_provider_details": "identityProviderDetails",
        "identity_provider_type": "identityProviderType",
        "logging_role": "loggingRole",
        "post_authentication_login_banner": "postAuthenticationLoginBanner",
        "pre_authentication_login_banner": "preAuthenticationLoginBanner",
        "protocol_details": "protocolDetails",
        "protocols": "protocols",
        "security_policy_name": "securityPolicyName",
        "tags": "tags",
        "workflow_details": "workflowDetails",
    },
)
class CfnServerProps:
    def __init__(
        self,
        *,
        certificate: typing.Optional[builtins.str] = None,
        domain: typing.Optional[builtins.str] = None,
        endpoint_details: typing.Optional[typing.Union[typing.Union[CfnServer.EndpointDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        endpoint_type: typing.Optional[builtins.str] = None,
        identity_provider_details: typing.Optional[typing.Union[typing.Union[CfnServer.IdentityProviderDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        identity_provider_type: typing.Optional[builtins.str] = None,
        logging_role: typing.Optional[builtins.str] = None,
        post_authentication_login_banner: typing.Optional[builtins.str] = None,
        pre_authentication_login_banner: typing.Optional[builtins.str] = None,
        protocol_details: typing.Optional[typing.Union[typing.Union[CfnServer.ProtocolDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_policy_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        workflow_details: typing.Optional[typing.Union[typing.Union[CfnServer.WorkflowDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnServer``.

        :param certificate: The Amazon Resource Name (ARN) of the AWS Certificate Manager (ACM) certificate. Required when ``Protocols`` is set to ``FTPS`` . To request a new public certificate, see `Request a public certificate <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-public.html>`_ in the *AWS Certificate Manager User Guide* . To import an existing certificate into ACM, see `Importing certificates into ACM <https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html>`_ in the *AWS Certificate Manager User Guide* . To request a private certificate to use FTPS through private IP addresses, see `Request a private certificate <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-private.html>`_ in the *AWS Certificate Manager User Guide* . Certificates with the following cryptographic algorithms and key sizes are supported: - 2048-bit RSA (RSA_2048) - 4096-bit RSA (RSA_4096) - Elliptic Prime Curve 256 bit (EC_prime256v1) - Elliptic Prime Curve 384 bit (EC_secp384r1) - Elliptic Prime Curve 521 bit (EC_secp521r1) .. epigraph:: The certificate must be a valid SSL/TLS X.509 version 3 certificate with FQDN or IP address specified and information about the issuer.
        :param domain: Specifies the domain of the storage system that is used for file transfers.
        :param endpoint_details: The virtual private cloud (VPC) endpoint settings that are configured for your server. When you host your endpoint within your VPC, you can make your endpoint accessible only to resources within your VPC, or you can attach Elastic IP addresses and make your endpoint accessible to clients over the internet. Your VPC's default security groups are automatically assigned to your endpoint.
        :param endpoint_type: The type of endpoint that you want your server to use. You can choose to make your server's endpoint publicly accessible (PUBLIC) or host it inside your VPC. With an endpoint that is hosted in a VPC, you can restrict access to your server and resources only within your VPC or choose to make it internet facing by attaching Elastic IP addresses directly to it.
        :param identity_provider_details: Required when ``IdentityProviderType`` is set to ``AWS_DIRECTORY_SERVICE`` or ``API_GATEWAY`` . Accepts an array containing all of the information required to use a directory in ``AWS_DIRECTORY_SERVICE`` or invoke a customer-supplied authentication API, including the API Gateway URL. Not required when ``IdentityProviderType`` is set to ``SERVICE_MANAGED`` .
        :param identity_provider_type: The mode of authentication for a server. The default value is ``SERVICE_MANAGED`` , which allows you to store and access user credentials within the AWS Transfer Family service. Use ``AWS_DIRECTORY_SERVICE`` to provide access to Active Directory groups in AWS Directory Service for Microsoft Active Directory or Microsoft Active Directory in your on-premises environment or in AWS using AD Connector. This option also requires you to provide a Directory ID by using the ``IdentityProviderDetails`` parameter. Use the ``API_GATEWAY`` value to integrate with an identity provider of your choosing. The ``API_GATEWAY`` setting requires you to provide an Amazon API Gateway endpoint URL to call for authentication by using the ``IdentityProviderDetails`` parameter. Use the ``AWS_LAMBDA`` value to directly use an AWS Lambda function as your identity provider. If you choose this value, you must specify the ARN for the Lambda function in the ``Function`` parameter or the ``IdentityProviderDetails`` data type.
        :param logging_role: The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that allows a server to turn on Amazon CloudWatch logging for Amazon S3 or Amazon EFSevents. When set, you can view user activity in your CloudWatch logs.
        :param post_authentication_login_banner: Specifies a string to display when users connect to a server. This string is displayed after the user authenticates. .. epigraph:: The SFTP protocol does not support post-authentication display banners.
        :param pre_authentication_login_banner: Specifies a string to display when users connect to a server. This string is displayed before the user authenticates. For example, the following banner displays details about using the system: ``This system is for the use of authorized users only. Individuals using this computer system without authority, or in excess of their authority, are subject to having all of their activities on this system monitored and recorded by system personnel.``
        :param protocol_details: The protocol settings that are configured for your server. - To indicate passive mode (for FTP and FTPS protocols), use the ``PassiveIp`` parameter. Enter a single dotted-quad IPv4 address, such as the external IP address of a firewall, router, or load balancer. - To ignore the error that is generated when the client attempts to use the ``SETSTAT`` command on a file that you are uploading to an Amazon S3 bucket, use the ``SetStatOption`` parameter. To have the AWS Transfer Family server ignore the ``SETSTAT`` command and upload files without needing to make any changes to your SFTP client, set the value to ``ENABLE_NO_OP`` . If you set the ``SetStatOption`` parameter to ``ENABLE_NO_OP`` , Transfer Family generates a log entry to Amazon CloudWatch Logs, so that you can determine when the client is making a ``SETSTAT`` call. - To determine whether your AWS Transfer Family server resumes recent, negotiated sessions through a unique session ID, use the ``TlsSessionResumptionMode`` parameter. - ``As2Transports`` indicates the transport method for the AS2 messages. Currently, only HTTP is supported.
        :param protocols: Specifies the file transfer protocol or protocols over which your file transfer protocol client can connect to your server's endpoint. The available protocols are: - ``SFTP`` (Secure Shell (SSH) File Transfer Protocol): File transfer over SSH - ``FTPS`` (File Transfer Protocol Secure): File transfer with TLS encryption - ``FTP`` (File Transfer Protocol): Unencrypted file transfer - ``AS2`` (Applicability Statement 2): used for transporting structured business-to-business data .. epigraph:: - If you select ``FTPS`` , you must choose a certificate stored in AWS Certificate Manager (ACM) which is used to identify your server when clients connect to it over FTPS. - If ``Protocol`` includes either ``FTP`` or ``FTPS`` , then the ``EndpointType`` must be ``VPC`` and the ``IdentityProviderType`` must be either ``AWS_DIRECTORY_SERVICE`` , ``AWS_LAMBDA`` , or ``API_GATEWAY`` . - If ``Protocol`` includes ``FTP`` , then ``AddressAllocationIds`` cannot be associated. - If ``Protocol`` is set only to ``SFTP`` , the ``EndpointType`` can be set to ``PUBLIC`` and the ``IdentityProviderType`` can be set any of the supported identity types: ``SERVICE_MANAGED`` , ``AWS_DIRECTORY_SERVICE`` , ``AWS_LAMBDA`` , or ``API_GATEWAY`` . - If ``Protocol`` includes ``AS2`` , then the ``EndpointType`` must be ``VPC`` , and domain must be Amazon S3.
        :param security_policy_name: Specifies the name of the security policy that is attached to the server.
        :param tags: Key-value pairs that can be used to group and search for servers.
        :param workflow_details: Specifies the workflow ID for the workflow to assign and the execution role that's used for executing the workflow. In addition to a workflow to execute when a file is uploaded completely, ``WorkflowDetails`` can also contain a workflow ID (and execution role) for a workflow to execute on partial upload. A partial upload occurs when a file is open when the session disconnects.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_transfer as transfer
            
            cfn_server_props = transfer.CfnServerProps(
                certificate="certificate",
                domain="domain",
                endpoint_details=transfer.CfnServer.EndpointDetailsProperty(
                    address_allocation_ids=["addressAllocationIds"],
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"],
                    vpc_endpoint_id="vpcEndpointId",
                    vpc_id="vpcId"
                ),
                endpoint_type="endpointType",
                identity_provider_details=transfer.CfnServer.IdentityProviderDetailsProperty(
                    directory_id="directoryId",
                    function="function",
                    invocation_role="invocationRole",
                    url="url"
                ),
                identity_provider_type="identityProviderType",
                logging_role="loggingRole",
                post_authentication_login_banner="postAuthenticationLoginBanner",
                pre_authentication_login_banner="preAuthenticationLoginBanner",
                protocol_details=transfer.CfnServer.ProtocolDetailsProperty(
                    as2_transports=["as2Transports"],
                    passive_ip="passiveIp",
                    set_stat_option="setStatOption",
                    tls_session_resumption_mode="tlsSessionResumptionMode"
                ),
                protocols=["protocols"],
                security_policy_name="securityPolicyName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                workflow_details=transfer.CfnServer.WorkflowDetailsProperty(
                    on_partial_upload=[transfer.CfnServer.WorkflowDetailProperty(
                        execution_role="executionRole",
                        workflow_id="workflowId"
                    )],
                    on_upload=[transfer.CfnServer.WorkflowDetailProperty(
                        execution_role="executionRole",
                        workflow_id="workflowId"
                    )]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c2192d128a659920a1ac1e2d0fa0cd150ca704eff394a392614500863148522)
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument endpoint_details", value=endpoint_details, expected_type=type_hints["endpoint_details"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
            check_type(argname="argument identity_provider_details", value=identity_provider_details, expected_type=type_hints["identity_provider_details"])
            check_type(argname="argument identity_provider_type", value=identity_provider_type, expected_type=type_hints["identity_provider_type"])
            check_type(argname="argument logging_role", value=logging_role, expected_type=type_hints["logging_role"])
            check_type(argname="argument post_authentication_login_banner", value=post_authentication_login_banner, expected_type=type_hints["post_authentication_login_banner"])
            check_type(argname="argument pre_authentication_login_banner", value=pre_authentication_login_banner, expected_type=type_hints["pre_authentication_login_banner"])
            check_type(argname="argument protocol_details", value=protocol_details, expected_type=type_hints["protocol_details"])
            check_type(argname="argument protocols", value=protocols, expected_type=type_hints["protocols"])
            check_type(argname="argument security_policy_name", value=security_policy_name, expected_type=type_hints["security_policy_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workflow_details", value=workflow_details, expected_type=type_hints["workflow_details"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate is not None:
            self._values["certificate"] = certificate
        if domain is not None:
            self._values["domain"] = domain
        if endpoint_details is not None:
            self._values["endpoint_details"] = endpoint_details
        if endpoint_type is not None:
            self._values["endpoint_type"] = endpoint_type
        if identity_provider_details is not None:
            self._values["identity_provider_details"] = identity_provider_details
        if identity_provider_type is not None:
            self._values["identity_provider_type"] = identity_provider_type
        if logging_role is not None:
            self._values["logging_role"] = logging_role
        if post_authentication_login_banner is not None:
            self._values["post_authentication_login_banner"] = post_authentication_login_banner
        if pre_authentication_login_banner is not None:
            self._values["pre_authentication_login_banner"] = pre_authentication_login_banner
        if protocol_details is not None:
            self._values["protocol_details"] = protocol_details
        if protocols is not None:
            self._values["protocols"] = protocols
        if security_policy_name is not None:
            self._values["security_policy_name"] = security_policy_name
        if tags is not None:
            self._values["tags"] = tags
        if workflow_details is not None:
            self._values["workflow_details"] = workflow_details

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS Certificate Manager (ACM) certificate.

        Required when ``Protocols`` is set to ``FTPS`` .

        To request a new public certificate, see `Request a public certificate <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-public.html>`_ in the *AWS Certificate Manager User Guide* .

        To import an existing certificate into ACM, see `Importing certificates into ACM <https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html>`_ in the *AWS Certificate Manager User Guide* .

        To request a private certificate to use FTPS through private IP addresses, see `Request a private certificate <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-private.html>`_ in the *AWS Certificate Manager User Guide* .

        Certificates with the following cryptographic algorithms and key sizes are supported:

        - 2048-bit RSA (RSA_2048)
        - 4096-bit RSA (RSA_4096)
        - Elliptic Prime Curve 256 bit (EC_prime256v1)
        - Elliptic Prime Curve 384 bit (EC_secp384r1)
        - Elliptic Prime Curve 521 bit (EC_secp521r1)

        .. epigraph::

           The certificate must be a valid SSL/TLS X.509 version 3 certificate with FQDN or IP address specified and information about the issuer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-certificate
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''Specifies the domain of the storage system that is used for file transfers.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_details(
        self,
    ) -> typing.Optional[typing.Union[CfnServer.EndpointDetailsProperty, _IResolvable_a771d0ef]]:
        '''The virtual private cloud (VPC) endpoint settings that are configured for your server.

        When you host your endpoint within your VPC, you can make your endpoint accessible only to resources within your VPC, or you can attach Elastic IP addresses and make your endpoint accessible to clients over the internet. Your VPC's default security groups are automatically assigned to your endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-endpointdetails
        '''
        result = self._values.get("endpoint_details")
        return typing.cast(typing.Optional[typing.Union[CfnServer.EndpointDetailsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        '''The type of endpoint that you want your server to use.

        You can choose to make your server's endpoint publicly accessible (PUBLIC) or host it inside your VPC. With an endpoint that is hosted in a VPC, you can restrict access to your server and resources only within your VPC or choose to make it internet facing by attaching Elastic IP addresses directly to it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-endpointtype
        '''
        result = self._values.get("endpoint_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_provider_details(
        self,
    ) -> typing.Optional[typing.Union[CfnServer.IdentityProviderDetailsProperty, _IResolvable_a771d0ef]]:
        '''Required when ``IdentityProviderType`` is set to ``AWS_DIRECTORY_SERVICE`` or ``API_GATEWAY`` .

        Accepts an array containing all of the information required to use a directory in ``AWS_DIRECTORY_SERVICE`` or invoke a customer-supplied authentication API, including the API Gateway URL. Not required when ``IdentityProviderType`` is set to ``SERVICE_MANAGED`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-identityproviderdetails
        '''
        result = self._values.get("identity_provider_details")
        return typing.cast(typing.Optional[typing.Union[CfnServer.IdentityProviderDetailsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def identity_provider_type(self) -> typing.Optional[builtins.str]:
        '''The mode of authentication for a server.

        The default value is ``SERVICE_MANAGED`` , which allows you to store and access user credentials within the AWS Transfer Family service.

        Use ``AWS_DIRECTORY_SERVICE`` to provide access to Active Directory groups in AWS Directory Service for Microsoft Active Directory or Microsoft Active Directory in your on-premises environment or in AWS using AD Connector. This option also requires you to provide a Directory ID by using the ``IdentityProviderDetails`` parameter.

        Use the ``API_GATEWAY`` value to integrate with an identity provider of your choosing. The ``API_GATEWAY`` setting requires you to provide an Amazon API Gateway endpoint URL to call for authentication by using the ``IdentityProviderDetails`` parameter.

        Use the ``AWS_LAMBDA`` value to directly use an AWS Lambda function as your identity provider. If you choose this value, you must specify the ARN for the Lambda function in the ``Function`` parameter or the ``IdentityProviderDetails`` data type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-identityprovidertype
        '''
        result = self._values.get("identity_provider_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_role(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that allows a server to turn on Amazon CloudWatch logging for Amazon S3 or Amazon EFSevents.

        When set, you can view user activity in your CloudWatch logs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-loggingrole
        '''
        result = self._values.get("logging_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_authentication_login_banner(self) -> typing.Optional[builtins.str]:
        '''Specifies a string to display when users connect to a server. This string is displayed after the user authenticates.

        .. epigraph::

           The SFTP protocol does not support post-authentication display banners.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-postauthenticationloginbanner
        '''
        result = self._values.get("post_authentication_login_banner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pre_authentication_login_banner(self) -> typing.Optional[builtins.str]:
        '''Specifies a string to display when users connect to a server.

        This string is displayed before the user authenticates. For example, the following banner displays details about using the system:

        ``This system is for the use of authorized users only. Individuals using this computer system without authority, or in excess of their authority, are subject to having all of their activities on this system monitored and recorded by system personnel.``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-preauthenticationloginbanner
        '''
        result = self._values.get("pre_authentication_login_banner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol_details(
        self,
    ) -> typing.Optional[typing.Union[CfnServer.ProtocolDetailsProperty, _IResolvable_a771d0ef]]:
        '''The protocol settings that are configured for your server.

        - To indicate passive mode (for FTP and FTPS protocols), use the ``PassiveIp`` parameter. Enter a single dotted-quad IPv4 address, such as the external IP address of a firewall, router, or load balancer.
        - To ignore the error that is generated when the client attempts to use the ``SETSTAT`` command on a file that you are uploading to an Amazon S3 bucket, use the ``SetStatOption`` parameter. To have the AWS Transfer Family server ignore the ``SETSTAT`` command and upload files without needing to make any changes to your SFTP client, set the value to ``ENABLE_NO_OP`` . If you set the ``SetStatOption`` parameter to ``ENABLE_NO_OP`` , Transfer Family generates a log entry to Amazon CloudWatch Logs, so that you can determine when the client is making a ``SETSTAT`` call.
        - To determine whether your AWS Transfer Family server resumes recent, negotiated sessions through a unique session ID, use the ``TlsSessionResumptionMode`` parameter.
        - ``As2Transports`` indicates the transport method for the AS2 messages. Currently, only HTTP is supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-protocoldetails
        '''
        result = self._values.get("protocol_details")
        return typing.cast(typing.Optional[typing.Union[CfnServer.ProtocolDetailsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def protocols(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the file transfer protocol or protocols over which your file transfer protocol client can connect to your server's endpoint.

        The available protocols are:

        - ``SFTP`` (Secure Shell (SSH) File Transfer Protocol): File transfer over SSH
        - ``FTPS`` (File Transfer Protocol Secure): File transfer with TLS encryption
        - ``FTP`` (File Transfer Protocol): Unencrypted file transfer
        - ``AS2`` (Applicability Statement 2): used for transporting structured business-to-business data

        .. epigraph::

           - If you select ``FTPS`` , you must choose a certificate stored in AWS Certificate Manager (ACM) which is used to identify your server when clients connect to it over FTPS.
           - If ``Protocol`` includes either ``FTP`` or ``FTPS`` , then the ``EndpointType`` must be ``VPC`` and the ``IdentityProviderType`` must be either ``AWS_DIRECTORY_SERVICE`` , ``AWS_LAMBDA`` , or ``API_GATEWAY`` .
           - If ``Protocol`` includes ``FTP`` , then ``AddressAllocationIds`` cannot be associated.
           - If ``Protocol`` is set only to ``SFTP`` , the ``EndpointType`` can be set to ``PUBLIC`` and the ``IdentityProviderType`` can be set any of the supported identity types: ``SERVICE_MANAGED`` , ``AWS_DIRECTORY_SERVICE`` , ``AWS_LAMBDA`` , or ``API_GATEWAY`` .
           - If ``Protocol`` includes ``AS2`` , then the ``EndpointType`` must be ``VPC`` , and domain must be Amazon S3.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-protocols
        '''
        result = self._values.get("protocols")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def security_policy_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the security policy that is attached to the server.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-securitypolicyname
        '''
        result = self._values.get("security_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Key-value pairs that can be used to group and search for servers.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def workflow_details(
        self,
    ) -> typing.Optional[typing.Union[CfnServer.WorkflowDetailsProperty, _IResolvable_a771d0ef]]:
        '''Specifies the workflow ID for the workflow to assign and the execution role that's used for executing the workflow.

        In addition to a workflow to execute when a file is uploaded completely, ``WorkflowDetails`` can also contain a workflow ID (and execution role) for a workflow to execute on partial upload. A partial upload occurs when a file is open when the session disconnects.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-workflowdetails
        '''
        result = self._values.get("workflow_details")
        return typing.cast(typing.Optional[typing.Union[CfnServer.WorkflowDetailsProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnUser(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_transfer.CfnUser",
):
    '''A CloudFormation ``AWS::Transfer::User``.

    The ``AWS::Transfer::User`` resource creates a user and associates them with an existing server. You can only create and associate users with servers that have the ``IdentityProviderType`` set to ``SERVICE_MANAGED`` . Using parameters for ``CreateUser`` , you can specify the user name, set the home directory, store the user's public key, and assign the user's AWS Identity and Access Management (IAM) role. You can also optionally add a session policy, and assign metadata with tags that can be used to group and search for users.

    :cloudformationResource: AWS::Transfer::User
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_transfer as transfer
        
        cfn_user = transfer.CfnUser(self, "MyCfnUser",
            role="role",
            server_id="serverId",
            user_name="userName",
        
            # the properties below are optional
            home_directory="homeDirectory",
            home_directory_mappings=[transfer.CfnUser.HomeDirectoryMapEntryProperty(
                entry="entry",
                target="target"
            )],
            home_directory_type="homeDirectoryType",
            policy="policy",
            posix_profile=transfer.CfnUser.PosixProfileProperty(
                gid=123,
                uid=123,
        
                # the properties below are optional
                secondary_gids=[123]
            ),
            ssh_public_keys=["sshPublicKeys"],
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        role: builtins.str,
        server_id: builtins.str,
        user_name: builtins.str,
        home_directory: typing.Optional[builtins.str] = None,
        home_directory_mappings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnUser.HomeDirectoryMapEntryProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        home_directory_type: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        posix_profile: typing.Optional[typing.Union[typing.Union["CfnUser.PosixProfileProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Transfer::User``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param role: The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that controls your users' access to your Amazon S3 bucket or Amazon EFS file system. The policies attached to this role determine the level of access that you want to provide your users when transferring files into and out of your Amazon S3 bucket or Amazon EFS file system. The IAM role should also contain a trust relationship that allows the server to access your resources when servicing your users' transfer requests.
        :param server_id: A system-assigned unique identifier for a server instance. This is the specific server that you added your user to.
        :param user_name: A unique string that identifies a user and is associated with a ``ServerId`` . This user name must be a minimum of 3 and a maximum of 100 characters long. The following are valid characters: a-z, A-Z, 0-9, underscore '_', hyphen '-', period '.', and at sign '@'. The user name can't start with a hyphen, period, or at sign.
        :param home_directory: The landing directory (folder) for a user when they log in to the server using the client. A ``HomeDirectory`` example is ``/bucket_name/home/mydirectory`` .
        :param home_directory_mappings: Logical directory mappings that specify what Amazon S3 paths and keys should be visible to your user and how you want to make them visible. You will need to specify the " ``Entry`` " and " ``Target`` " pair, where ``Entry`` shows how the path is made visible and ``Target`` is the actual Amazon S3 path. If you only specify a target, it will be displayed as is. You will need to also make sure that your IAM role provides access to paths in ``Target`` . The following is an example. ``'[ { "Entry": "/", "Target": "/bucket3/customized-reports/" } ]'`` In most cases, you can use this value instead of the session policy to lock your user down to the designated home directory ("chroot"). To do this, you can set ``Entry`` to '/' and set ``Target`` to the HomeDirectory parameter value. .. epigraph:: If the target of a logical directory entry does not exist in Amazon S3, the entry will be ignored. As a workaround, you can use the Amazon S3 API to create 0 byte objects as place holders for your directory. If using the CLI, use the ``s3api`` call instead of ``s3`` so you can use the put-object operation. For example, you use the following: ``AWS s3api put-object --bucket bucketname --key path/to/folder/`` . Make sure that the end of the key name ends in a '/' for it to be considered a folder.
        :param home_directory_type: The type of landing directory (folder) that you want your users' home directory to be when they log in to the server. If you set it to ``PATH`` , the user will see the absolute Amazon S3 bucket or EFS paths as is in their file transfer protocol clients. If you set it ``LOGICAL`` , you need to provide mappings in the ``HomeDirectoryMappings`` for how you want to make Amazon S3 or Amazon EFS paths visible to your users.
        :param policy: A session policy for your user so you can use the same IAM role across multiple users. This policy restricts user access to portions of their Amazon S3 bucket. Variables that you can use inside this policy include ``${Transfer:UserName}`` , ``${Transfer:HomeDirectory}`` , and ``${Transfer:HomeBucket}`` . .. epigraph:: For session policies, AWS Transfer Family stores the policy as a JSON blob, instead of the Amazon Resource Name (ARN) of the policy. You save the policy as a JSON blob and pass it in the ``Policy`` argument. For an example of a session policy, see `Example session policy <https://docs.aws.amazon.com/transfer/latest/userguide/session-policy.html>`_ . For more information, see `AssumeRole <https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html>`_ in the *AWS Security Token Service API Reference* .
        :param posix_profile: Specifies the full POSIX identity, including user ID ( ``Uid`` ), group ID ( ``Gid`` ), and any secondary groups IDs ( ``SecondaryGids`` ), that controls your users' access to your Amazon Elastic File System (Amazon EFS) file systems. The POSIX permissions that are set on files and directories in your file system determine the level of access your users get when transferring files into and out of your Amazon EFS file systems.
        :param ssh_public_keys: Specifies the public key portion of the Secure Shell (SSH) keys stored for the described user.
        :param tags: Key-value pairs that can be used to group and search for users. Tags are metadata attached to users for any purpose.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb4401d90893fd77882d7cebe976c9aaf1f7d9539246b4f68ed680642e5959c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnUserProps(
            role=role,
            server_id=server_id,
            user_name=user_name,
            home_directory=home_directory,
            home_directory_mappings=home_directory_mappings,
            home_directory_type=home_directory_type,
            policy=policy,
            posix_profile=posix_profile,
            ssh_public_keys=ssh_public_keys,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82dac26b83ecf09e18ba22ec2f4573ddb5117fc8d388707b237e3970f21e6bb0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6019858d44c330c0b77848c7670abd53758291702a692b3e79d4a126f47a40ca)
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
        '''The Amazon Resource Name associated with the user, in the form ``arn:aws:transfer:region: *account-id* :user/ *server-id* / *username*`` .

        An example of a user ARN is: ``arn:aws:transfer:us-east-1:123456789012:user/user1`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrServerId")
    def attr_server_id(self) -> builtins.str:
        '''The ID of the server to which the user is attached.

        An example ``ServerId`` is ``s-01234567890abcdef`` .

        :cloudformationAttribute: ServerId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServerId"))

    @builtins.property
    @jsii.member(jsii_name="attrUserName")
    def attr_user_name(self) -> builtins.str:
        '''A unique string that identifies a user account associated with a server.

        An example ``UserName`` is ``transfer-user-1`` .

        :cloudformationAttribute: UserName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUserName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Key-value pairs that can be used to group and search for users.

        Tags are metadata attached to users for any purpose.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that controls your users' access to your Amazon S3 bucket or Amazon EFS file system.

        The policies attached to this role determine the level of access that you want to provide your users when transferring files into and out of your Amazon S3 bucket or Amazon EFS file system. The IAM role should also contain a trust relationship that allows the server to access your resources when servicing your users' transfer requests.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-role
        '''
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93f5ff55965043dfa8a65ee289cdb386f9756088672b2d7f0d31c420c89362ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value)

    @builtins.property
    @jsii.member(jsii_name="serverId")
    def server_id(self) -> builtins.str:
        '''A system-assigned unique identifier for a server instance.

        This is the specific server that you added your user to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-serverid
        '''
        return typing.cast(builtins.str, jsii.get(self, "serverId"))

    @server_id.setter
    def server_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d84ea843a0d23cd5c80511998c77f96c2d5aa55c7a527bb09c95562e4bfa0af5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverId", value)

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        '''A unique string that identifies a user and is associated with a ``ServerId`` .

        This user name must be a minimum of 3 and a maximum of 100 characters long. The following are valid characters: a-z, A-Z, 0-9, underscore '_', hyphen '-', period '.', and at sign '@'. The user name can't start with a hyphen, period, or at sign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-username
        '''
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b600192d84c466f6549b196e725d0ca244de25a9a4e5d7b2886847ac35d40c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value)

    @builtins.property
    @jsii.member(jsii_name="homeDirectory")
    def home_directory(self) -> typing.Optional[builtins.str]:
        '''The landing directory (folder) for a user when they log in to the server using the client.

        A ``HomeDirectory`` example is ``/bucket_name/home/mydirectory`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectory
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "homeDirectory"))

    @home_directory.setter
    def home_directory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__382612d6ada64616e11caf0e5b52bcb09e2646026cdced2250c91f2268187f13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "homeDirectory", value)

    @builtins.property
    @jsii.member(jsii_name="homeDirectoryMappings")
    def home_directory_mappings(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnUser.HomeDirectoryMapEntryProperty", _IResolvable_a771d0ef]]]]:
        '''Logical directory mappings that specify what Amazon S3 paths and keys should be visible to your user and how you want to make them visible.

        You will need to specify the " ``Entry`` " and " ``Target`` " pair, where ``Entry`` shows how the path is made visible and ``Target`` is the actual Amazon S3 path. If you only specify a target, it will be displayed as is. You will need to also make sure that your IAM role provides access to paths in ``Target`` . The following is an example.

        ``'[ { "Entry": "/", "Target": "/bucket3/customized-reports/" } ]'``

        In most cases, you can use this value instead of the session policy to lock your user down to the designated home directory ("chroot"). To do this, you can set ``Entry`` to '/' and set ``Target`` to the HomeDirectory parameter value.
        .. epigraph::

           If the target of a logical directory entry does not exist in Amazon S3, the entry will be ignored. As a workaround, you can use the Amazon S3 API to create 0 byte objects as place holders for your directory. If using the CLI, use the ``s3api`` call instead of ``s3`` so you can use the put-object operation. For example, you use the following: ``AWS s3api put-object --bucket bucketname --key path/to/folder/`` . Make sure that the end of the key name ends in a '/' for it to be considered a folder.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectorymappings
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnUser.HomeDirectoryMapEntryProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "homeDirectoryMappings"))

    @home_directory_mappings.setter
    def home_directory_mappings(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnUser.HomeDirectoryMapEntryProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__733aa462c6fa0bec683b7ac2ca22a87f8e23504c3a7e7107bffa90695654d370)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "homeDirectoryMappings", value)

    @builtins.property
    @jsii.member(jsii_name="homeDirectoryType")
    def home_directory_type(self) -> typing.Optional[builtins.str]:
        '''The type of landing directory (folder) that you want your users' home directory to be when they log in to the server.

        If you set it to ``PATH`` , the user will see the absolute Amazon S3 bucket or EFS paths as is in their file transfer protocol clients. If you set it ``LOGICAL`` , you need to provide mappings in the ``HomeDirectoryMappings`` for how you want to make Amazon S3 or Amazon EFS paths visible to your users.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectorytype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "homeDirectoryType"))

    @home_directory_type.setter
    def home_directory_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52dbc4984c04c5379c8e470bf643c0c7717eddb9233bfcc07069fb77e249a808)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "homeDirectoryType", value)

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Optional[builtins.str]:
        '''A session policy for your user so you can use the same IAM role across multiple users.

        This policy restricts user access to portions of their Amazon S3 bucket. Variables that you can use inside this policy include ``${Transfer:UserName}`` , ``${Transfer:HomeDirectory}`` , and ``${Transfer:HomeBucket}`` .
        .. epigraph::

           For session policies, AWS Transfer Family stores the policy as a JSON blob, instead of the Amazon Resource Name (ARN) of the policy. You save the policy as a JSON blob and pass it in the ``Policy`` argument.

           For an example of a session policy, see `Example session policy <https://docs.aws.amazon.com/transfer/latest/userguide/session-policy.html>`_ .

           For more information, see `AssumeRole <https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html>`_ in the *AWS Security Token Service API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-policy
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39b7dab8e16ca064a4ccad807ceff07c20f609b99b068869481c944c26cc1de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="posixProfile")
    def posix_profile(
        self,
    ) -> typing.Optional[typing.Union["CfnUser.PosixProfileProperty", _IResolvable_a771d0ef]]:
        '''Specifies the full POSIX identity, including user ID ( ``Uid`` ), group ID ( ``Gid`` ), and any secondary groups IDs ( ``SecondaryGids`` ), that controls your users' access to your Amazon Elastic File System (Amazon EFS) file systems.

        The POSIX permissions that are set on files and directories in your file system determine the level of access your users get when transferring files into and out of your Amazon EFS file systems.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-posixprofile
        '''
        return typing.cast(typing.Optional[typing.Union["CfnUser.PosixProfileProperty", _IResolvable_a771d0ef]], jsii.get(self, "posixProfile"))

    @posix_profile.setter
    def posix_profile(
        self,
        value: typing.Optional[typing.Union["CfnUser.PosixProfileProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe410783679319447d1d16258439e03f35e715f19b3a99fbd6b0b9b0f8adafd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "posixProfile", value)

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeys")
    def ssh_public_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the public key portion of the Secure Shell (SSH) keys stored for the described user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-sshpublickeys
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sshPublicKeys"))

    @ssh_public_keys.setter
    def ssh_public_keys(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__083ee541decfa5e46ec61e649b35c7a2e4ec85d8f677dfd87e32ffb2ba5d1a29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPublicKeys", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_transfer.CfnUser.HomeDirectoryMapEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"entry": "entry", "target": "target"},
    )
    class HomeDirectoryMapEntryProperty:
        def __init__(self, *, entry: builtins.str, target: builtins.str) -> None:
            '''Represents an object that contains entries and targets for ``HomeDirectoryMappings`` .

            :param entry: Represents an entry for ``HomeDirectoryMappings`` .
            :param target: Represents the map target that is used in a ``HomeDirectorymapEntry`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-homedirectorymapentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_transfer as transfer
                
                home_directory_map_entry_property = transfer.CfnUser.HomeDirectoryMapEntryProperty(
                    entry="entry",
                    target="target"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__84cc8144aa15b6294c3fb5beca80b67cf1200ea6dd5f30242b1963715d31297c)
                check_type(argname="argument entry", value=entry, expected_type=type_hints["entry"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "entry": entry,
                "target": target,
            }

        @builtins.property
        def entry(self) -> builtins.str:
            '''Represents an entry for ``HomeDirectoryMappings`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-homedirectorymapentry.html#cfn-transfer-user-homedirectorymapentry-entry
            '''
            result = self._values.get("entry")
            assert result is not None, "Required property 'entry' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def target(self) -> builtins.str:
            '''Represents the map target that is used in a ``HomeDirectorymapEntry`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-homedirectorymapentry.html#cfn-transfer-user-homedirectorymapentry-target
            '''
            result = self._values.get("target")
            assert result is not None, "Required property 'target' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HomeDirectoryMapEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_transfer.CfnUser.PosixProfileProperty",
        jsii_struct_bases=[],
        name_mapping={"gid": "gid", "uid": "uid", "secondary_gids": "secondaryGids"},
    )
    class PosixProfileProperty:
        def __init__(
            self,
            *,
            gid: jsii.Number,
            uid: jsii.Number,
            secondary_gids: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[jsii.Number]]] = None,
        ) -> None:
            '''The full POSIX identity, including user ID ( ``Uid`` ), group ID ( ``Gid`` ), and any secondary groups IDs ( ``SecondaryGids`` ), that controls your users' access to your Amazon EFS file systems.

            The POSIX permissions that are set on files and directories in your file system determine the level of access your users get when transferring files into and out of your Amazon EFS file systems.

            :param gid: The POSIX group ID used for all EFS operations by this user.
            :param uid: The POSIX user ID used for all EFS operations by this user.
            :param secondary_gids: The secondary POSIX group IDs used for all EFS operations by this user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-posixprofile.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_transfer as transfer
                
                posix_profile_property = transfer.CfnUser.PosixProfileProperty(
                    gid=123,
                    uid=123,
                
                    # the properties below are optional
                    secondary_gids=[123]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b36fc617c16bc733ea8ded419ee62a5d1505f1c3940dfc19705a5bb9c3942df7)
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
        def gid(self) -> jsii.Number:
            '''The POSIX group ID used for all EFS operations by this user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-posixprofile.html#cfn-transfer-user-posixprofile-gid
            '''
            result = self._values.get("gid")
            assert result is not None, "Required property 'gid' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def uid(self) -> jsii.Number:
            '''The POSIX user ID used for all EFS operations by this user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-posixprofile.html#cfn-transfer-user-posixprofile-uid
            '''
            result = self._values.get("uid")
            assert result is not None, "Required property 'uid' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def secondary_gids(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[jsii.Number]]]:
            '''The secondary POSIX group IDs used for all EFS operations by this user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-posixprofile.html#cfn-transfer-user-posixprofile-secondarygids
            '''
            result = self._values.get("secondary_gids")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[jsii.Number]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PosixProfileProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_transfer.CfnUserProps",
    jsii_struct_bases=[],
    name_mapping={
        "role": "role",
        "server_id": "serverId",
        "user_name": "userName",
        "home_directory": "homeDirectory",
        "home_directory_mappings": "homeDirectoryMappings",
        "home_directory_type": "homeDirectoryType",
        "policy": "policy",
        "posix_profile": "posixProfile",
        "ssh_public_keys": "sshPublicKeys",
        "tags": "tags",
    },
)
class CfnUserProps:
    def __init__(
        self,
        *,
        role: builtins.str,
        server_id: builtins.str,
        user_name: builtins.str,
        home_directory: typing.Optional[builtins.str] = None,
        home_directory_mappings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnUser.HomeDirectoryMapEntryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        home_directory_type: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        posix_profile: typing.Optional[typing.Union[typing.Union[CfnUser.PosixProfileProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnUser``.

        :param role: The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that controls your users' access to your Amazon S3 bucket or Amazon EFS file system. The policies attached to this role determine the level of access that you want to provide your users when transferring files into and out of your Amazon S3 bucket or Amazon EFS file system. The IAM role should also contain a trust relationship that allows the server to access your resources when servicing your users' transfer requests.
        :param server_id: A system-assigned unique identifier for a server instance. This is the specific server that you added your user to.
        :param user_name: A unique string that identifies a user and is associated with a ``ServerId`` . This user name must be a minimum of 3 and a maximum of 100 characters long. The following are valid characters: a-z, A-Z, 0-9, underscore '_', hyphen '-', period '.', and at sign '@'. The user name can't start with a hyphen, period, or at sign.
        :param home_directory: The landing directory (folder) for a user when they log in to the server using the client. A ``HomeDirectory`` example is ``/bucket_name/home/mydirectory`` .
        :param home_directory_mappings: Logical directory mappings that specify what Amazon S3 paths and keys should be visible to your user and how you want to make them visible. You will need to specify the " ``Entry`` " and " ``Target`` " pair, where ``Entry`` shows how the path is made visible and ``Target`` is the actual Amazon S3 path. If you only specify a target, it will be displayed as is. You will need to also make sure that your IAM role provides access to paths in ``Target`` . The following is an example. ``'[ { "Entry": "/", "Target": "/bucket3/customized-reports/" } ]'`` In most cases, you can use this value instead of the session policy to lock your user down to the designated home directory ("chroot"). To do this, you can set ``Entry`` to '/' and set ``Target`` to the HomeDirectory parameter value. .. epigraph:: If the target of a logical directory entry does not exist in Amazon S3, the entry will be ignored. As a workaround, you can use the Amazon S3 API to create 0 byte objects as place holders for your directory. If using the CLI, use the ``s3api`` call instead of ``s3`` so you can use the put-object operation. For example, you use the following: ``AWS s3api put-object --bucket bucketname --key path/to/folder/`` . Make sure that the end of the key name ends in a '/' for it to be considered a folder.
        :param home_directory_type: The type of landing directory (folder) that you want your users' home directory to be when they log in to the server. If you set it to ``PATH`` , the user will see the absolute Amazon S3 bucket or EFS paths as is in their file transfer protocol clients. If you set it ``LOGICAL`` , you need to provide mappings in the ``HomeDirectoryMappings`` for how you want to make Amazon S3 or Amazon EFS paths visible to your users.
        :param policy: A session policy for your user so you can use the same IAM role across multiple users. This policy restricts user access to portions of their Amazon S3 bucket. Variables that you can use inside this policy include ``${Transfer:UserName}`` , ``${Transfer:HomeDirectory}`` , and ``${Transfer:HomeBucket}`` . .. epigraph:: For session policies, AWS Transfer Family stores the policy as a JSON blob, instead of the Amazon Resource Name (ARN) of the policy. You save the policy as a JSON blob and pass it in the ``Policy`` argument. For an example of a session policy, see `Example session policy <https://docs.aws.amazon.com/transfer/latest/userguide/session-policy.html>`_ . For more information, see `AssumeRole <https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html>`_ in the *AWS Security Token Service API Reference* .
        :param posix_profile: Specifies the full POSIX identity, including user ID ( ``Uid`` ), group ID ( ``Gid`` ), and any secondary groups IDs ( ``SecondaryGids`` ), that controls your users' access to your Amazon Elastic File System (Amazon EFS) file systems. The POSIX permissions that are set on files and directories in your file system determine the level of access your users get when transferring files into and out of your Amazon EFS file systems.
        :param ssh_public_keys: Specifies the public key portion of the Secure Shell (SSH) keys stored for the described user.
        :param tags: Key-value pairs that can be used to group and search for users. Tags are metadata attached to users for any purpose.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_transfer as transfer
            
            cfn_user_props = transfer.CfnUserProps(
                role="role",
                server_id="serverId",
                user_name="userName",
            
                # the properties below are optional
                home_directory="homeDirectory",
                home_directory_mappings=[transfer.CfnUser.HomeDirectoryMapEntryProperty(
                    entry="entry",
                    target="target"
                )],
                home_directory_type="homeDirectoryType",
                policy="policy",
                posix_profile=transfer.CfnUser.PosixProfileProperty(
                    gid=123,
                    uid=123,
            
                    # the properties below are optional
                    secondary_gids=[123]
                ),
                ssh_public_keys=["sshPublicKeys"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7758b0720cc4c7377ad15a6c6bfd32aebb27fef00c3ddfcb9f87a9d9f9ddcfe8)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument server_id", value=server_id, expected_type=type_hints["server_id"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
            check_type(argname="argument home_directory", value=home_directory, expected_type=type_hints["home_directory"])
            check_type(argname="argument home_directory_mappings", value=home_directory_mappings, expected_type=type_hints["home_directory_mappings"])
            check_type(argname="argument home_directory_type", value=home_directory_type, expected_type=type_hints["home_directory_type"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument posix_profile", value=posix_profile, expected_type=type_hints["posix_profile"])
            check_type(argname="argument ssh_public_keys", value=ssh_public_keys, expected_type=type_hints["ssh_public_keys"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role": role,
            "server_id": server_id,
            "user_name": user_name,
        }
        if home_directory is not None:
            self._values["home_directory"] = home_directory
        if home_directory_mappings is not None:
            self._values["home_directory_mappings"] = home_directory_mappings
        if home_directory_type is not None:
            self._values["home_directory_type"] = home_directory_type
        if policy is not None:
            self._values["policy"] = policy
        if posix_profile is not None:
            self._values["posix_profile"] = posix_profile
        if ssh_public_keys is not None:
            self._values["ssh_public_keys"] = ssh_public_keys
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def role(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that controls your users' access to your Amazon S3 bucket or Amazon EFS file system.

        The policies attached to this role determine the level of access that you want to provide your users when transferring files into and out of your Amazon S3 bucket or Amazon EFS file system. The IAM role should also contain a trust relationship that allows the server to access your resources when servicing your users' transfer requests.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-role
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server_id(self) -> builtins.str:
        '''A system-assigned unique identifier for a server instance.

        This is the specific server that you added your user to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-serverid
        '''
        result = self._values.get("server_id")
        assert result is not None, "Required property 'server_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_name(self) -> builtins.str:
        '''A unique string that identifies a user and is associated with a ``ServerId`` .

        This user name must be a minimum of 3 and a maximum of 100 characters long. The following are valid characters: a-z, A-Z, 0-9, underscore '_', hyphen '-', period '.', and at sign '@'. The user name can't start with a hyphen, period, or at sign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-username
        '''
        result = self._values.get("user_name")
        assert result is not None, "Required property 'user_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def home_directory(self) -> typing.Optional[builtins.str]:
        '''The landing directory (folder) for a user when they log in to the server using the client.

        A ``HomeDirectory`` example is ``/bucket_name/home/mydirectory`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectory
        '''
        result = self._values.get("home_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def home_directory_mappings(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnUser.HomeDirectoryMapEntryProperty, _IResolvable_a771d0ef]]]]:
        '''Logical directory mappings that specify what Amazon S3 paths and keys should be visible to your user and how you want to make them visible.

        You will need to specify the " ``Entry`` " and " ``Target`` " pair, where ``Entry`` shows how the path is made visible and ``Target`` is the actual Amazon S3 path. If you only specify a target, it will be displayed as is. You will need to also make sure that your IAM role provides access to paths in ``Target`` . The following is an example.

        ``'[ { "Entry": "/", "Target": "/bucket3/customized-reports/" } ]'``

        In most cases, you can use this value instead of the session policy to lock your user down to the designated home directory ("chroot"). To do this, you can set ``Entry`` to '/' and set ``Target`` to the HomeDirectory parameter value.
        .. epigraph::

           If the target of a logical directory entry does not exist in Amazon S3, the entry will be ignored. As a workaround, you can use the Amazon S3 API to create 0 byte objects as place holders for your directory. If using the CLI, use the ``s3api`` call instead of ``s3`` so you can use the put-object operation. For example, you use the following: ``AWS s3api put-object --bucket bucketname --key path/to/folder/`` . Make sure that the end of the key name ends in a '/' for it to be considered a folder.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectorymappings
        '''
        result = self._values.get("home_directory_mappings")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnUser.HomeDirectoryMapEntryProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def home_directory_type(self) -> typing.Optional[builtins.str]:
        '''The type of landing directory (folder) that you want your users' home directory to be when they log in to the server.

        If you set it to ``PATH`` , the user will see the absolute Amazon S3 bucket or EFS paths as is in their file transfer protocol clients. If you set it ``LOGICAL`` , you need to provide mappings in the ``HomeDirectoryMappings`` for how you want to make Amazon S3 or Amazon EFS paths visible to your users.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectorytype
        '''
        result = self._values.get("home_directory_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''A session policy for your user so you can use the same IAM role across multiple users.

        This policy restricts user access to portions of their Amazon S3 bucket. Variables that you can use inside this policy include ``${Transfer:UserName}`` , ``${Transfer:HomeDirectory}`` , and ``${Transfer:HomeBucket}`` .
        .. epigraph::

           For session policies, AWS Transfer Family stores the policy as a JSON blob, instead of the Amazon Resource Name (ARN) of the policy. You save the policy as a JSON blob and pass it in the ``Policy`` argument.

           For an example of a session policy, see `Example session policy <https://docs.aws.amazon.com/transfer/latest/userguide/session-policy.html>`_ .

           For more information, see `AssumeRole <https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html>`_ in the *AWS Security Token Service API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def posix_profile(
        self,
    ) -> typing.Optional[typing.Union[CfnUser.PosixProfileProperty, _IResolvable_a771d0ef]]:
        '''Specifies the full POSIX identity, including user ID ( ``Uid`` ), group ID ( ``Gid`` ), and any secondary groups IDs ( ``SecondaryGids`` ), that controls your users' access to your Amazon Elastic File System (Amazon EFS) file systems.

        The POSIX permissions that are set on files and directories in your file system determine the level of access your users get when transferring files into and out of your Amazon EFS file systems.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-posixprofile
        '''
        result = self._values.get("posix_profile")
        return typing.cast(typing.Optional[typing.Union[CfnUser.PosixProfileProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def ssh_public_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the public key portion of the Secure Shell (SSH) keys stored for the described user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-sshpublickeys
        '''
        result = self._values.get("ssh_public_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Key-value pairs that can be used to group and search for users.

        Tags are metadata attached to users for any purpose.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnWorkflow(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_transfer.CfnWorkflow",
):
    '''A CloudFormation ``AWS::Transfer::Workflow``.

    Allows you to create a workflow with specified steps and step details the workflow invokes after file transfer completes. After creating a workflow, you can associate the workflow created with any transfer servers by specifying the ``workflow-details`` field in ``CreateServer`` and ``UpdateServer`` operations.

    :cloudformationResource: AWS::Transfer::Workflow
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-workflow.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_transfer as transfer
        
        # copy_step_details: Any
        # custom_step_details: Any
        # delete_step_details: Any
        # tag_step_details: Any
        
        cfn_workflow = transfer.CfnWorkflow(self, "MyCfnWorkflow",
            steps=[transfer.CfnWorkflow.WorkflowStepProperty(
                copy_step_details=copy_step_details,
                custom_step_details=custom_step_details,
                delete_step_details=delete_step_details,
                tag_step_details=tag_step_details,
                type="type"
            )],
        
            # the properties below are optional
            description="description",
            on_exception_steps=[transfer.CfnWorkflow.WorkflowStepProperty(
                copy_step_details=copy_step_details,
                custom_step_details=custom_step_details,
                delete_step_details=delete_step_details,
                tag_step_details=tag_step_details,
                type="type"
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        steps: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnWorkflow.WorkflowStepProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        description: typing.Optional[builtins.str] = None,
        on_exception_steps: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnWorkflow.WorkflowStepProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Transfer::Workflow``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param steps: Specifies the details for the steps that are in the specified workflow.
        :param description: Specifies the text description for the workflow.
        :param on_exception_steps: Specifies the steps (actions) to take if errors are encountered during execution of the workflow.
        :param tags: Key-value pairs that can be used to group and search for workflows. Tags are metadata attached to workflows for any purpose.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f7c0e7de6df5a62b77260c7c9743fcbbd75dcad772ef7f5d1a1bc68d0f15f56)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnWorkflowProps(
            steps=steps,
            description=description,
            on_exception_steps=on_exception_steps,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e58126c90486ce5c7f551795fa2e8914328081df8abf56930dbb2bf378d3cf2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78e7c3433bffc2d2a3374286772adc707f5d8ac40225d6c1112e7b5b9da66820)
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
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrWorkflowId")
    def attr_workflow_id(self) -> builtins.str:
        '''A unique identifier for a workflow.

        :cloudformationAttribute: WorkflowId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrWorkflowId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Key-value pairs that can be used to group and search for workflows.

        Tags are metadata attached to workflows for any purpose.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-workflow.html#cfn-transfer-workflow-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="steps")
    def steps(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWorkflow.WorkflowStepProperty", _IResolvable_a771d0ef]]]:
        '''Specifies the details for the steps that are in the specified workflow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-workflow.html#cfn-transfer-workflow-steps
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWorkflow.WorkflowStepProperty", _IResolvable_a771d0ef]]], jsii.get(self, "steps"))

    @steps.setter
    def steps(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWorkflow.WorkflowStepProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__734c89b07d3abcb03f134a41cc782223f69e4ced43e7e10e6e9dd1003c2d03dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "steps", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''Specifies the text description for the workflow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-workflow.html#cfn-transfer-workflow-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d313251e441899e0dc53545a170c751f2ba1bb4d4a0a461ae14f1add81b52f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="onExceptionSteps")
    def on_exception_steps(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWorkflow.WorkflowStepProperty", _IResolvable_a771d0ef]]]]:
        '''Specifies the steps (actions) to take if errors are encountered during execution of the workflow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-workflow.html#cfn-transfer-workflow-onexceptionsteps
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWorkflow.WorkflowStepProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "onExceptionSteps"))

    @on_exception_steps.setter
    def on_exception_steps(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWorkflow.WorkflowStepProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be27949f0bbb762aa40f7d7ee8dea91afae2bae9fc9fa859bb718f9097d4f764)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onExceptionSteps", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_transfer.CfnWorkflow.CopyStepDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_file_location": "destinationFileLocation",
            "name": "name",
            "overwrite_existing": "overwriteExisting",
            "source_file_location": "sourceFileLocation",
        },
    )
    class CopyStepDetailsProperty:
        def __init__(
            self,
            *,
            destination_file_location: typing.Optional[typing.Union[typing.Union["CfnWorkflow.InputFileLocationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            name: typing.Optional[builtins.str] = None,
            overwrite_existing: typing.Optional[builtins.str] = None,
            source_file_location: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param destination_file_location: ``CfnWorkflow.CopyStepDetailsProperty.DestinationFileLocation``.
            :param name: ``CfnWorkflow.CopyStepDetailsProperty.Name``.
            :param overwrite_existing: ``CfnWorkflow.CopyStepDetailsProperty.OverwriteExisting``.
            :param source_file_location: ``CfnWorkflow.CopyStepDetailsProperty.SourceFileLocation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-copystepdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_transfer as transfer
                
                copy_step_details_property = transfer.CfnWorkflow.CopyStepDetailsProperty(
                    destination_file_location=transfer.CfnWorkflow.InputFileLocationProperty(
                        s3_file_location=transfer.CfnWorkflow.S3InputFileLocationProperty(
                            bucket="bucket",
                            key="key"
                        )
                    ),
                    name="name",
                    overwrite_existing="overwriteExisting",
                    source_file_location="sourceFileLocation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd9b2e270da41a3efb64a198573971551db963a577277e3252e38eb65fbeb097)
                check_type(argname="argument destination_file_location", value=destination_file_location, expected_type=type_hints["destination_file_location"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument overwrite_existing", value=overwrite_existing, expected_type=type_hints["overwrite_existing"])
                check_type(argname="argument source_file_location", value=source_file_location, expected_type=type_hints["source_file_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_file_location is not None:
                self._values["destination_file_location"] = destination_file_location
            if name is not None:
                self._values["name"] = name
            if overwrite_existing is not None:
                self._values["overwrite_existing"] = overwrite_existing
            if source_file_location is not None:
                self._values["source_file_location"] = source_file_location

        @builtins.property
        def destination_file_location(
            self,
        ) -> typing.Optional[typing.Union["CfnWorkflow.InputFileLocationProperty", _IResolvable_a771d0ef]]:
            '''``CfnWorkflow.CopyStepDetailsProperty.DestinationFileLocation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-copystepdetails.html#cfn-transfer-workflow-copystepdetails-destinationfilelocation
            '''
            result = self._values.get("destination_file_location")
            return typing.cast(typing.Optional[typing.Union["CfnWorkflow.InputFileLocationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''``CfnWorkflow.CopyStepDetailsProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-copystepdetails.html#cfn-transfer-workflow-copystepdetails-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def overwrite_existing(self) -> typing.Optional[builtins.str]:
            '''``CfnWorkflow.CopyStepDetailsProperty.OverwriteExisting``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-copystepdetails.html#cfn-transfer-workflow-copystepdetails-overwriteexisting
            '''
            result = self._values.get("overwrite_existing")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_file_location(self) -> typing.Optional[builtins.str]:
            '''``CfnWorkflow.CopyStepDetailsProperty.SourceFileLocation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-copystepdetails.html#cfn-transfer-workflow-copystepdetails-sourcefilelocation
            '''
            result = self._values.get("source_file_location")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CopyStepDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_transfer.CfnWorkflow.CustomStepDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "source_file_location": "sourceFileLocation",
            "target": "target",
            "timeout_seconds": "timeoutSeconds",
        },
    )
    class CustomStepDetailsProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            source_file_location: typing.Optional[builtins.str] = None,
            target: typing.Optional[builtins.str] = None,
            timeout_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param name: ``CfnWorkflow.CustomStepDetailsProperty.Name``.
            :param source_file_location: ``CfnWorkflow.CustomStepDetailsProperty.SourceFileLocation``.
            :param target: ``CfnWorkflow.CustomStepDetailsProperty.Target``.
            :param timeout_seconds: ``CfnWorkflow.CustomStepDetailsProperty.TimeoutSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-customstepdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_transfer as transfer
                
                custom_step_details_property = transfer.CfnWorkflow.CustomStepDetailsProperty(
                    name="name",
                    source_file_location="sourceFileLocation",
                    target="target",
                    timeout_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2e05e30bfe1f26b375391cf4e2715e90678771bc30ebfc23fed3e7923b683bc1)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument source_file_location", value=source_file_location, expected_type=type_hints["source_file_location"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
                check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if source_file_location is not None:
                self._values["source_file_location"] = source_file_location
            if target is not None:
                self._values["target"] = target
            if timeout_seconds is not None:
                self._values["timeout_seconds"] = timeout_seconds

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''``CfnWorkflow.CustomStepDetailsProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-customstepdetails.html#cfn-transfer-workflow-customstepdetails-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_file_location(self) -> typing.Optional[builtins.str]:
            '''``CfnWorkflow.CustomStepDetailsProperty.SourceFileLocation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-customstepdetails.html#cfn-transfer-workflow-customstepdetails-sourcefilelocation
            '''
            result = self._values.get("source_file_location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target(self) -> typing.Optional[builtins.str]:
            '''``CfnWorkflow.CustomStepDetailsProperty.Target``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-customstepdetails.html#cfn-transfer-workflow-customstepdetails-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timeout_seconds(self) -> typing.Optional[jsii.Number]:
            '''``CfnWorkflow.CustomStepDetailsProperty.TimeoutSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-customstepdetails.html#cfn-transfer-workflow-customstepdetails-timeoutseconds
            '''
            result = self._values.get("timeout_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomStepDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_transfer.CfnWorkflow.DeleteStepDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "source_file_location": "sourceFileLocation"},
    )
    class DeleteStepDetailsProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            source_file_location: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param name: ``CfnWorkflow.DeleteStepDetailsProperty.Name``.
            :param source_file_location: ``CfnWorkflow.DeleteStepDetailsProperty.SourceFileLocation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-deletestepdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_transfer as transfer
                
                delete_step_details_property = transfer.CfnWorkflow.DeleteStepDetailsProperty(
                    name="name",
                    source_file_location="sourceFileLocation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__df1a1662e1c6302f1ab8ff77f09a67e7e03df46ea9066ee9cdf8228a4dc7bf92)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument source_file_location", value=source_file_location, expected_type=type_hints["source_file_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if source_file_location is not None:
                self._values["source_file_location"] = source_file_location

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''``CfnWorkflow.DeleteStepDetailsProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-deletestepdetails.html#cfn-transfer-workflow-deletestepdetails-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_file_location(self) -> typing.Optional[builtins.str]:
            '''``CfnWorkflow.DeleteStepDetailsProperty.SourceFileLocation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-deletestepdetails.html#cfn-transfer-workflow-deletestepdetails-sourcefilelocation
            '''
            result = self._values.get("source_file_location")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeleteStepDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_transfer.CfnWorkflow.InputFileLocationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_file_location": "s3FileLocation"},
    )
    class InputFileLocationProperty:
        def __init__(
            self,
            *,
            s3_file_location: typing.Optional[typing.Union[typing.Union["CfnWorkflow.S3InputFileLocationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param s3_file_location: ``CfnWorkflow.InputFileLocationProperty.S3FileLocation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-inputfilelocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_transfer as transfer
                
                input_file_location_property = transfer.CfnWorkflow.InputFileLocationProperty(
                    s3_file_location=transfer.CfnWorkflow.S3InputFileLocationProperty(
                        bucket="bucket",
                        key="key"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__64aba613b264d5936d69670a1c35e344aa4f77e535fafc9885b7f150113fcafa)
                check_type(argname="argument s3_file_location", value=s3_file_location, expected_type=type_hints["s3_file_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_file_location is not None:
                self._values["s3_file_location"] = s3_file_location

        @builtins.property
        def s3_file_location(
            self,
        ) -> typing.Optional[typing.Union["CfnWorkflow.S3InputFileLocationProperty", _IResolvable_a771d0ef]]:
            '''``CfnWorkflow.InputFileLocationProperty.S3FileLocation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-inputfilelocation.html#cfn-transfer-workflow-inputfilelocation-s3filelocation
            '''
            result = self._values.get("s3_file_location")
            return typing.cast(typing.Optional[typing.Union["CfnWorkflow.S3InputFileLocationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputFileLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_transfer.CfnWorkflow.S3InputFileLocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key"},
    )
    class S3InputFileLocationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param bucket: ``CfnWorkflow.S3InputFileLocationProperty.Bucket``.
            :param key: ``CfnWorkflow.S3InputFileLocationProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-s3inputfilelocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_transfer as transfer
                
                s3_input_file_location_property = transfer.CfnWorkflow.S3InputFileLocationProperty(
                    bucket="bucket",
                    key="key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a2f55151eb6e4120eaca2484ceb5b05ed088c5a22a44d0ab62e3d35b73bdc0e9)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key is not None:
                self._values["key"] = key

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''``CfnWorkflow.S3InputFileLocationProperty.Bucket``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-s3inputfilelocation.html#cfn-transfer-workflow-s3inputfilelocation-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''``CfnWorkflow.S3InputFileLocationProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-s3inputfilelocation.html#cfn-transfer-workflow-s3inputfilelocation-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3InputFileLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_transfer.CfnWorkflow.S3TagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class S3TagProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''
            :param key: ``CfnWorkflow.S3TagProperty.Key``.
            :param value: ``CfnWorkflow.S3TagProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-s3tag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_transfer as transfer
                
                s3_tag_property = transfer.CfnWorkflow.S3TagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a188eed3ea42978e921ae464b788a291ade7eba2b84870ab17defa07746c79a)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnWorkflow.S3TagProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-s3tag.html#cfn-transfer-workflow-s3tag-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''``CfnWorkflow.S3TagProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-s3tag.html#cfn-transfer-workflow-s3tag-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3TagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_transfer.CfnWorkflow.TagStepDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "source_file_location": "sourceFileLocation",
            "tags": "tags",
        },
    )
    class TagStepDetailsProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            source_file_location: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union["CfnWorkflow.S3TagProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param name: ``CfnWorkflow.TagStepDetailsProperty.Name``.
            :param source_file_location: ``CfnWorkflow.TagStepDetailsProperty.SourceFileLocation``.
            :param tags: ``CfnWorkflow.TagStepDetailsProperty.Tags``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-tagstepdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_transfer as transfer
                
                tag_step_details_property = transfer.CfnWorkflow.TagStepDetailsProperty(
                    name="name",
                    source_file_location="sourceFileLocation",
                    tags=[transfer.CfnWorkflow.S3TagProperty(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e715cefe0852909456367af1440aa124288de6accdc06b764013304ede292e06)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument source_file_location", value=source_file_location, expected_type=type_hints["source_file_location"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if source_file_location is not None:
                self._values["source_file_location"] = source_file_location
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''``CfnWorkflow.TagStepDetailsProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-tagstepdetails.html#cfn-transfer-workflow-tagstepdetails-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_file_location(self) -> typing.Optional[builtins.str]:
            '''``CfnWorkflow.TagStepDetailsProperty.SourceFileLocation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-tagstepdetails.html#cfn-transfer-workflow-tagstepdetails-sourcefilelocation
            '''
            result = self._values.get("source_file_location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List["CfnWorkflow.S3TagProperty"]]:
            '''``CfnWorkflow.TagStepDetailsProperty.Tags``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-tagstepdetails.html#cfn-transfer-workflow-tagstepdetails-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List["CfnWorkflow.S3TagProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagStepDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_transfer.CfnWorkflow.WorkflowStepProperty",
        jsii_struct_bases=[],
        name_mapping={
            "copy_step_details": "copyStepDetails",
            "custom_step_details": "customStepDetails",
            "delete_step_details": "deleteStepDetails",
            "tag_step_details": "tagStepDetails",
            "type": "type",
        },
    )
    class WorkflowStepProperty:
        def __init__(
            self,
            *,
            copy_step_details: typing.Any = None,
            custom_step_details: typing.Any = None,
            delete_step_details: typing.Any = None,
            tag_step_details: typing.Any = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The basic building block of a workflow.

            :param copy_step_details: Details for a step that performs a file copy. Consists of the following values: - A description - An Amazon S3 location for the destination of the file copy. - A flag that indicates whether to overwrite an existing file of the same name. The default is ``FALSE`` .
            :param custom_step_details: Details for a step that invokes an AWS Lambda function. Consists of the Lambda function's name, target, and timeout (in seconds).
            :param delete_step_details: Details for a step that deletes the file.
            :param tag_step_details: Details for a step that creates one or more tags. You specify one or more tags. Each tag contains a key-value pair.
            :param type: Currently, the following step types are supported. - *``COPY``* - Copy the file to another location. - *``CUSTOM``* - Perform a custom step with an AWS Lambda function target. - *``DECRYPT``* - Decrypt a file that was encrypted before it was uploaded. - *``DELETE``* - Delete the file. - *``TAG``* - Add a tag to the file.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-workflowstep.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_transfer as transfer
                
                # copy_step_details: Any
                # custom_step_details: Any
                # delete_step_details: Any
                # tag_step_details: Any
                
                workflow_step_property = transfer.CfnWorkflow.WorkflowStepProperty(
                    copy_step_details=copy_step_details,
                    custom_step_details=custom_step_details,
                    delete_step_details=delete_step_details,
                    tag_step_details=tag_step_details,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__886dea18b09b99665439c5e4e487ed5385709af9d50696335e50d7bbea5bc49e)
                check_type(argname="argument copy_step_details", value=copy_step_details, expected_type=type_hints["copy_step_details"])
                check_type(argname="argument custom_step_details", value=custom_step_details, expected_type=type_hints["custom_step_details"])
                check_type(argname="argument delete_step_details", value=delete_step_details, expected_type=type_hints["delete_step_details"])
                check_type(argname="argument tag_step_details", value=tag_step_details, expected_type=type_hints["tag_step_details"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if copy_step_details is not None:
                self._values["copy_step_details"] = copy_step_details
            if custom_step_details is not None:
                self._values["custom_step_details"] = custom_step_details
            if delete_step_details is not None:
                self._values["delete_step_details"] = delete_step_details
            if tag_step_details is not None:
                self._values["tag_step_details"] = tag_step_details
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def copy_step_details(self) -> typing.Any:
            '''Details for a step that performs a file copy.

            Consists of the following values:

            - A description
            - An Amazon S3 location for the destination of the file copy.
            - A flag that indicates whether to overwrite an existing file of the same name. The default is ``FALSE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-workflowstep.html#cfn-transfer-workflow-workflowstep-copystepdetails
            '''
            result = self._values.get("copy_step_details")
            return typing.cast(typing.Any, result)

        @builtins.property
        def custom_step_details(self) -> typing.Any:
            '''Details for a step that invokes an AWS Lambda function.

            Consists of the Lambda function's name, target, and timeout (in seconds).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-workflowstep.html#cfn-transfer-workflow-workflowstep-customstepdetails
            '''
            result = self._values.get("custom_step_details")
            return typing.cast(typing.Any, result)

        @builtins.property
        def delete_step_details(self) -> typing.Any:
            '''Details for a step that deletes the file.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-workflowstep.html#cfn-transfer-workflow-workflowstep-deletestepdetails
            '''
            result = self._values.get("delete_step_details")
            return typing.cast(typing.Any, result)

        @builtins.property
        def tag_step_details(self) -> typing.Any:
            '''Details for a step that creates one or more tags.

            You specify one or more tags. Each tag contains a key-value pair.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-workflowstep.html#cfn-transfer-workflow-workflowstep-tagstepdetails
            '''
            result = self._values.get("tag_step_details")
            return typing.cast(typing.Any, result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Currently, the following step types are supported.

            - *``COPY``* - Copy the file to another location.
            - *``CUSTOM``* - Perform a custom step with an AWS Lambda function target.
            - *``DECRYPT``* - Decrypt a file that was encrypted before it was uploaded.
            - *``DELETE``* - Delete the file.
            - *``TAG``* - Add a tag to the file.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-workflowstep.html#cfn-transfer-workflow-workflowstep-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkflowStepProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_transfer.CfnWorkflowProps",
    jsii_struct_bases=[],
    name_mapping={
        "steps": "steps",
        "description": "description",
        "on_exception_steps": "onExceptionSteps",
        "tags": "tags",
    },
)
class CfnWorkflowProps:
    def __init__(
        self,
        *,
        steps: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnWorkflow.WorkflowStepProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        description: typing.Optional[builtins.str] = None,
        on_exception_steps: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnWorkflow.WorkflowStepProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnWorkflow``.

        :param steps: Specifies the details for the steps that are in the specified workflow.
        :param description: Specifies the text description for the workflow.
        :param on_exception_steps: Specifies the steps (actions) to take if errors are encountered during execution of the workflow.
        :param tags: Key-value pairs that can be used to group and search for workflows. Tags are metadata attached to workflows for any purpose.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-workflow.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_transfer as transfer
            
            # copy_step_details: Any
            # custom_step_details: Any
            # delete_step_details: Any
            # tag_step_details: Any
            
            cfn_workflow_props = transfer.CfnWorkflowProps(
                steps=[transfer.CfnWorkflow.WorkflowStepProperty(
                    copy_step_details=copy_step_details,
                    custom_step_details=custom_step_details,
                    delete_step_details=delete_step_details,
                    tag_step_details=tag_step_details,
                    type="type"
                )],
            
                # the properties below are optional
                description="description",
                on_exception_steps=[transfer.CfnWorkflow.WorkflowStepProperty(
                    copy_step_details=copy_step_details,
                    custom_step_details=custom_step_details,
                    delete_step_details=delete_step_details,
                    tag_step_details=tag_step_details,
                    type="type"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc23441355750d733c11d873abc0b944d6daa6424a84761c0fbf05a5dc1dc385)
            check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument on_exception_steps", value=on_exception_steps, expected_type=type_hints["on_exception_steps"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "steps": steps,
        }
        if description is not None:
            self._values["description"] = description
        if on_exception_steps is not None:
            self._values["on_exception_steps"] = on_exception_steps
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def steps(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnWorkflow.WorkflowStepProperty, _IResolvable_a771d0ef]]]:
        '''Specifies the details for the steps that are in the specified workflow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-workflow.html#cfn-transfer-workflow-steps
        '''
        result = self._values.get("steps")
        assert result is not None, "Required property 'steps' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnWorkflow.WorkflowStepProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Specifies the text description for the workflow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-workflow.html#cfn-transfer-workflow-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_exception_steps(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnWorkflow.WorkflowStepProperty, _IResolvable_a771d0ef]]]]:
        '''Specifies the steps (actions) to take if errors are encountered during execution of the workflow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-workflow.html#cfn-transfer-workflow-onexceptionsteps
        '''
        result = self._values.get("on_exception_steps")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnWorkflow.WorkflowStepProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Key-value pairs that can be used to group and search for workflows.

        Tags are metadata attached to workflows for any purpose.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-workflow.html#cfn-transfer-workflow-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkflowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAgreement",
    "CfnAgreementProps",
    "CfnCertificate",
    "CfnCertificateProps",
    "CfnConnector",
    "CfnConnectorProps",
    "CfnProfile",
    "CfnProfileProps",
    "CfnServer",
    "CfnServerProps",
    "CfnUser",
    "CfnUserProps",
    "CfnWorkflow",
    "CfnWorkflowProps",
]

publication.publish()

def _typecheckingstub__134ac265dd289ba5618fbd91064199ed20f2e0d343005babc69fac90c58a9b41(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    access_role: builtins.str,
    base_directory: builtins.str,
    local_profile_id: builtins.str,
    partner_profile_id: builtins.str,
    server_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b6f39c4297036e4e8f3fa89f18debb725cf55aa3108623c1638044a711f068(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2dc063111b9f32e146b7da061febd8c0c6f98641bdb129870dc838d17da6039(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e8102f6a51b4eb3c63a9ffaebd73dda2f8eb3b4919fb683c34eae15e608d16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e49b84094df16463717193c0096d4e7c3c6e03026003d389a1183224dbad75df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e9ab4d639c7742ee117326bcead033c3ca977cd7220b2773cf189ebe7a72c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0038c01636c581e21010bf8691cb6ec2b55aef6a1f759a0450f42ad0f1fff133(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a85bc483fda39fdf5c5fbdc370315c216d9b0d044684b923fe691fe193b28acc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d4014dc136ed966206324426f76956920a746ddbbe50c5c2696524a109eb5e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd4a60054595db1e60bbf02ae812f5dc6d72f9cccdd0b8d20ba62c975bcb1ff(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85db52acaba061f601c6ce38f4da9214bebacd0dddf81b18265913d0c5772e20(
    *,
    access_role: builtins.str,
    base_directory: builtins.str,
    local_profile_id: builtins.str,
    partner_profile_id: builtins.str,
    server_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43491862cd588c88ad1d78265c893bf01147132b2a135f865cf80d23f3bf73f(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    certificate: builtins.str,
    usage: builtins.str,
    active_date: typing.Optional[builtins.str] = None,
    certificate_chain: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    inactive_date: typing.Optional[builtins.str] = None,
    private_key: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5183da02df7a82320f1799e730b9a6a32ecea270722ed82afaf89ef0bb129396(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b28b97c4064ca3e2de22f419aabb70dedc46b065b3f52f9cd33ab6c5eee1a3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b605f1495cc8a3cc3de85f56830592e17a896e84759b36c77d3973caeb95d04a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4627978c67efffef809ec7dd495d0b83ed4a16f6d03d8d092fd749e6d478929(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44755a8522e524e922655abc094063e699553311290bc79a81841a896a754e75(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c89e1c655700623e39ff924fade459f81425928742fa8d469263a0f4ab216e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c72fc0e92c82b4ebad556953917bad67331bd218dd960f56c960b0b5bc585a3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93628e5f976dc54245b41abdd0ecda5b4f3b5bda080812b772aa7322f58a6356(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1a2aec6b7c6cc42729096854b0d645764b2d91343226179c87d2809871e49a1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd66966550b89bf450519253b17798a8a754aca6381aa18653886a6598ef328(
    *,
    certificate: builtins.str,
    usage: builtins.str,
    active_date: typing.Optional[builtins.str] = None,
    certificate_chain: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    inactive_date: typing.Optional[builtins.str] = None,
    private_key: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd88525c1d58175c9d6dd85c85d38fb58f7673111ce0badabd573b79748ef52(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    access_role: builtins.str,
    as2_config: typing.Any,
    url: builtins.str,
    logging_role: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10b81c5c3a5bbf5c466697baf4ec957ecd3ea156a60b9dcda492fcba69573a54(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d71f668080348885a55058bd21c3b7cabb2ce4d3fc5f1f72c3face54a4634a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ffd4896a613038476b7396e806e81f43d5404e6ff147d3aa575c5433af5f70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a782191976a9b43922fdf6df907dacde3272fc9e1c77be8ecdc9a46c8490414(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1000819cbfa7eb644e93ff9a76ca8ab09b077e91a9e4c3f15781a241c153c78c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac953273fd9a91cb0fbf716529c26650eb88b7431904bac25fd2dcbbe10d9846(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b1d9d705075f1026020ad89416a4c0a069541b673c1ad0db9578248190e83f8(
    *,
    compression: typing.Optional[builtins.str] = None,
    encryption_algorithm: typing.Optional[builtins.str] = None,
    local_profile_id: typing.Optional[builtins.str] = None,
    mdn_response: typing.Optional[builtins.str] = None,
    mdn_signing_algorithm: typing.Optional[builtins.str] = None,
    message_subject: typing.Optional[builtins.str] = None,
    partner_profile_id: typing.Optional[builtins.str] = None,
    signing_algorithm: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424e64f552dddea19abf0cf15f3a2262188be07a6f64355fb834c35a70a9ddb4(
    *,
    access_role: builtins.str,
    as2_config: typing.Any,
    url: builtins.str,
    logging_role: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1214dbae9407b5aa3b5f795879c88279a81606fa3a1b4701f68c9d336372d1ae(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    as2_id: builtins.str,
    profile_type: builtins.str,
    certificate_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e2d85f151ab9ea787f667701affa2bf96fb67168d67d1c0d7d1b5051021e87(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e665dee77f2b91690cd9de47b1e814fac74f411d8d9765b07f69f7fe9b0cbb50(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bef576741c4b4bb72ca8ae7bb792ceb2a57aab5736b380d7034eb9a7eb4114d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2fa6cb852f014c06e7fd08d82e510c6f15af2015a395a30d7c5d59dfb20887(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4edafdae663f5b5b3f80fae40fff73284f051b23b3c64ca6a51d7a62251ce2b4(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b098ee24393f17cdbe0789645f469958513aa7a4258564c5d97bc311be3e55f(
    *,
    as2_id: builtins.str,
    profile_type: builtins.str,
    certificate_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d9bf7e751a0730ea2df11510a4080e1fd8fb0aa877bd8a8ef4cccc6a04cf511(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    certificate: typing.Optional[builtins.str] = None,
    domain: typing.Optional[builtins.str] = None,
    endpoint_details: typing.Optional[typing.Union[typing.Union[CfnServer.EndpointDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    endpoint_type: typing.Optional[builtins.str] = None,
    identity_provider_details: typing.Optional[typing.Union[typing.Union[CfnServer.IdentityProviderDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    identity_provider_type: typing.Optional[builtins.str] = None,
    logging_role: typing.Optional[builtins.str] = None,
    post_authentication_login_banner: typing.Optional[builtins.str] = None,
    pre_authentication_login_banner: typing.Optional[builtins.str] = None,
    protocol_details: typing.Optional[typing.Union[typing.Union[CfnServer.ProtocolDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_policy_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    workflow_details: typing.Optional[typing.Union[typing.Union[CfnServer.WorkflowDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee508fc6cfb0790567e3b88faa66829b940207c7b7a40bdfb30906e8e011a66a(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__628449ae5bca14d695aa159e94885ec91d6027ed72730616a8f78be614b5b970(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eceec3cdaad0f84bd64bc19530c7678e8d44c996fad04b7cdb8a6b1e117cc99(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b24d42be648882df8c049b485bb5b9d6fb665c3eaecfc6a26e2a1615037770(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__509b3b21f54fc905415cd934bc12a170bf7dc5b9ae17e822ab5a356b17dc2a77(
    value: typing.Optional[typing.Union[CfnServer.EndpointDetailsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81552e27323810d71b87571f785bb22344c9eaa43d096d71aa1dfe1602acf898(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e25062a39baf983e3131469ee48f4c33522360ed64817c8ef7b047ede35ecc2(
    value: typing.Optional[typing.Union[CfnServer.IdentityProviderDetailsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c189403fd2efaf177ae31b001970dabc32612e9c998d4be759abbb6f3147773(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00431c85189d75ae5f73627be25a0110e5335ccb11fd2655fa51c4c4f23fcba0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f186ac6bf763e3e0ff1f072779f105b571e0c764b9353155b9697097b7fbe9fe(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e82252e450e05ae66e08c314a4bf4dc773a3431c2617250ad84989f371eeef(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94208a56d565c10ddedac8b79ee054fc14650c8b71712542cc1c3b6c6f02b0a6(
    value: typing.Optional[typing.Union[CfnServer.ProtocolDetailsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4aa06bbc2a56d1bea2584e2dd86acc645caf049f7ac5840468e302435bf7e63(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e034e555acbdc422eda08639e550ae3c67b4b324294aa1c023e659d87e54d77(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__214c68c65a7c0f3e45e763adf074c0d0fda039ca811dad4d1c66bf0c7418481e(
    value: typing.Optional[typing.Union[CfnServer.WorkflowDetailsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a676ac4c89bd836d2f828f0b22f4dd67bd533227c3728c9f2e7de26aa619f07(
    *,
    address_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_endpoint_id: typing.Optional[builtins.str] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b9df9ad578d061e8e01d8c63353ac3d9a3c7f83484840ea793274cce5a417b4(
    *,
    directory_id: typing.Optional[builtins.str] = None,
    function: typing.Optional[builtins.str] = None,
    invocation_role: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c49b75d67550e4173969ef74afe66d171181eb35103f7f7a265e94c4f9ab478c(
    *,
    as2_transports: typing.Optional[typing.Sequence[builtins.str]] = None,
    passive_ip: typing.Optional[builtins.str] = None,
    set_stat_option: typing.Optional[builtins.str] = None,
    tls_session_resumption_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17849a405a080c9f8ea5d8627fadee3faf08fb13e5cbb2cfa037346f67321ffb(
    *,
    execution_role: builtins.str,
    workflow_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7654f3686762abc0f070cc9055a19b439d8c910e8a82727eb5b3ebeb80b3bb28(
    *,
    on_partial_upload: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnServer.WorkflowDetailProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    on_upload: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnServer.WorkflowDetailProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2192d128a659920a1ac1e2d0fa0cd150ca704eff394a392614500863148522(
    *,
    certificate: typing.Optional[builtins.str] = None,
    domain: typing.Optional[builtins.str] = None,
    endpoint_details: typing.Optional[typing.Union[typing.Union[CfnServer.EndpointDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    endpoint_type: typing.Optional[builtins.str] = None,
    identity_provider_details: typing.Optional[typing.Union[typing.Union[CfnServer.IdentityProviderDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    identity_provider_type: typing.Optional[builtins.str] = None,
    logging_role: typing.Optional[builtins.str] = None,
    post_authentication_login_banner: typing.Optional[builtins.str] = None,
    pre_authentication_login_banner: typing.Optional[builtins.str] = None,
    protocol_details: typing.Optional[typing.Union[typing.Union[CfnServer.ProtocolDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_policy_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    workflow_details: typing.Optional[typing.Union[typing.Union[CfnServer.WorkflowDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb4401d90893fd77882d7cebe976c9aaf1f7d9539246b4f68ed680642e5959c(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    role: builtins.str,
    server_id: builtins.str,
    user_name: builtins.str,
    home_directory: typing.Optional[builtins.str] = None,
    home_directory_mappings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnUser.HomeDirectoryMapEntryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    home_directory_type: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
    posix_profile: typing.Optional[typing.Union[typing.Union[CfnUser.PosixProfileProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82dac26b83ecf09e18ba22ec2f4573ddb5117fc8d388707b237e3970f21e6bb0(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6019858d44c330c0b77848c7670abd53758291702a692b3e79d4a126f47a40ca(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f5ff55965043dfa8a65ee289cdb386f9756088672b2d7f0d31c420c89362ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d84ea843a0d23cd5c80511998c77f96c2d5aa55c7a527bb09c95562e4bfa0af5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b600192d84c466f6549b196e725d0ca244de25a9a4e5d7b2886847ac35d40c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382612d6ada64616e11caf0e5b52bcb09e2646026cdced2250c91f2268187f13(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__733aa462c6fa0bec683b7ac2ca22a87f8e23504c3a7e7107bffa90695654d370(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnUser.HomeDirectoryMapEntryProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52dbc4984c04c5379c8e470bf643c0c7717eddb9233bfcc07069fb77e249a808(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39b7dab8e16ca064a4ccad807ceff07c20f609b99b068869481c944c26cc1de(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe410783679319447d1d16258439e03f35e715f19b3a99fbd6b0b9b0f8adafd9(
    value: typing.Optional[typing.Union[CfnUser.PosixProfileProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083ee541decfa5e46ec61e649b35c7a2e4ec85d8f677dfd87e32ffb2ba5d1a29(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84cc8144aa15b6294c3fb5beca80b67cf1200ea6dd5f30242b1963715d31297c(
    *,
    entry: builtins.str,
    target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b36fc617c16bc733ea8ded419ee62a5d1505f1c3940dfc19705a5bb9c3942df7(
    *,
    gid: jsii.Number,
    uid: jsii.Number,
    secondary_gids: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[jsii.Number]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7758b0720cc4c7377ad15a6c6bfd32aebb27fef00c3ddfcb9f87a9d9f9ddcfe8(
    *,
    role: builtins.str,
    server_id: builtins.str,
    user_name: builtins.str,
    home_directory: typing.Optional[builtins.str] = None,
    home_directory_mappings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnUser.HomeDirectoryMapEntryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    home_directory_type: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
    posix_profile: typing.Optional[typing.Union[typing.Union[CfnUser.PosixProfileProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f7c0e7de6df5a62b77260c7c9743fcbbd75dcad772ef7f5d1a1bc68d0f15f56(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    steps: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnWorkflow.WorkflowStepProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    description: typing.Optional[builtins.str] = None,
    on_exception_steps: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnWorkflow.WorkflowStepProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e58126c90486ce5c7f551795fa2e8914328081df8abf56930dbb2bf378d3cf2(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e7c3433bffc2d2a3374286772adc707f5d8ac40225d6c1112e7b5b9da66820(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__734c89b07d3abcb03f134a41cc782223f69e4ced43e7e10e6e9dd1003c2d03dd(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnWorkflow.WorkflowStepProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d313251e441899e0dc53545a170c751f2ba1bb4d4a0a461ae14f1add81b52f1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be27949f0bbb762aa40f7d7ee8dea91afae2bae9fc9fa859bb718f9097d4f764(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnWorkflow.WorkflowStepProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9b2e270da41a3efb64a198573971551db963a577277e3252e38eb65fbeb097(
    *,
    destination_file_location: typing.Optional[typing.Union[typing.Union[CfnWorkflow.InputFileLocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
    overwrite_existing: typing.Optional[builtins.str] = None,
    source_file_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e05e30bfe1f26b375391cf4e2715e90678771bc30ebfc23fed3e7923b683bc1(
    *,
    name: typing.Optional[builtins.str] = None,
    source_file_location: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df1a1662e1c6302f1ab8ff77f09a67e7e03df46ea9066ee9cdf8228a4dc7bf92(
    *,
    name: typing.Optional[builtins.str] = None,
    source_file_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64aba613b264d5936d69670a1c35e344aa4f77e535fafc9885b7f150113fcafa(
    *,
    s3_file_location: typing.Optional[typing.Union[typing.Union[CfnWorkflow.S3InputFileLocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2f55151eb6e4120eaca2484ceb5b05ed088c5a22a44d0ab62e3d35b73bdc0e9(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a188eed3ea42978e921ae464b788a291ade7eba2b84870ab17defa07746c79a(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e715cefe0852909456367af1440aa124288de6accdc06b764013304ede292e06(
    *,
    name: typing.Optional[builtins.str] = None,
    source_file_location: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnWorkflow.S3TagProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__886dea18b09b99665439c5e4e487ed5385709af9d50696335e50d7bbea5bc49e(
    *,
    copy_step_details: typing.Any = None,
    custom_step_details: typing.Any = None,
    delete_step_details: typing.Any = None,
    tag_step_details: typing.Any = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc23441355750d733c11d873abc0b944d6daa6424a84761c0fbf05a5dc1dc385(
    *,
    steps: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnWorkflow.WorkflowStepProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    description: typing.Optional[builtins.str] = None,
    on_exception_steps: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnWorkflow.WorkflowStepProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
