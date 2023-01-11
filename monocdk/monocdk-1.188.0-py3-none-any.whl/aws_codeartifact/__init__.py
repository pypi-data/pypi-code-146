'''
# AWS::CodeArtifact Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as codeartifact
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for CodeArtifact construct libraries](https://constructs.dev/search?q=codeartifact)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::CodeArtifact resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CodeArtifact.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::CodeArtifact](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CodeArtifact.html).

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
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnDomain(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codeartifact.CfnDomain",
):
    '''A CloudFormation ``AWS::CodeArtifact::Domain``.

    The ``AWS::CodeArtifact::Domain`` resource creates an AWS CodeArtifact domain. CodeArtifact *domains* make it easier to manage multiple repositories across an organization. You can use a domain to apply permissions across many repositories owned by different AWS accounts. For more information about domains, see the `Domain concepts information <https://docs.aws.amazon.com/codeartifact/latest/ug/codeartifact-concepts.html#welcome-concepts-domain>`_ in the *CodeArtifact User Guide* . For more information about the ``CreateDomain`` API, see `CreateDomain <https://docs.aws.amazon.com/codeartifact/latest/APIReference/API_CreateDomain.html>`_ in the *CodeArtifact API Reference* .

    :cloudformationResource: AWS::CodeArtifact::Domain
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-domain.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_codeartifact as codeartifact
        
        # permissions_policy_document: Any
        
        cfn_domain = codeartifact.CfnDomain(self, "MyCfnDomain",
            domain_name="domainName",
        
            # the properties below are optional
            encryption_key="encryptionKey",
            permissions_policy_document=permissions_policy_document,
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
        domain_name: builtins.str,
        encryption_key: typing.Optional[builtins.str] = None,
        permissions_policy_document: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::CodeArtifact::Domain``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param domain_name: A string that specifies the name of the requested domain.
        :param encryption_key: The key used to encrypt the domain.
        :param permissions_policy_document: The document that defines the resource policy that is set on a domain.
        :param tags: A list of tags to be applied to the domain.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46bd830d13f2252bff0b03ae80230bad9057d3635d220b46f1c480f1172f021f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDomainProps(
            domain_name=domain_name,
            encryption_key=encryption_key,
            permissions_policy_document=permissions_policy_document,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca70bafd86e74bed544d264e027b8f2916766699cd0d66b71e8503577ea238fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83570d56280d96e991aebc0c405daeb30de1056c5726e1396fe5a54838b3cb2a)
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
        '''When you pass the logical ID of this resource, the function returns the Amazon Resource Name (ARN) of the domain.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrEncryptionKey")
    def attr_encryption_key(self) -> builtins.str:
        '''When you pass the logical ID of this resource, the function returns the key used to encrypt the domain.

        :cloudformationAttribute: EncryptionKey
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''When you pass the logical ID of this resource, the function returns the name of the domain.

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="attrOwner")
    def attr_owner(self) -> builtins.str:
        '''When you pass the logical ID of this resource, the function returns the 12-digit account number of the AWS account that owns the domain.

        :cloudformationAttribute: Owner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrOwner"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of tags to be applied to the domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-domain.html#cfn-codeartifact-domain-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''A string that specifies the name of the requested domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-domain.html#cfn-codeartifact-domain-domainname
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62ed2d6ff457b8e42a55cf060b3a311cc9db25830f4af807d42f3e72e04ce487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="permissionsPolicyDocument")
    def permissions_policy_document(self) -> typing.Any:
        '''The document that defines the resource policy that is set on a domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-domain.html#cfn-codeartifact-domain-permissionspolicydocument
        '''
        return typing.cast(typing.Any, jsii.get(self, "permissionsPolicyDocument"))

    @permissions_policy_document.setter
    def permissions_policy_document(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb90e3f7a3c6f10b4017ba1865fdc3adf14646378fa7bd725691c85d41cec0ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionsPolicyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[builtins.str]:
        '''The key used to encrypt the domain.

        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-domain.html#cfn-codeartifact-domain-encryptionkey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKey"))

    @encryption_key.setter
    def encryption_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af4a6722e40e9a10b357d9f56a1f8830f71a73eadf6c433c95ab87ef3f35c76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKey", value)


@jsii.data_type(
    jsii_type="monocdk.aws_codeartifact.CfnDomainProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "encryption_key": "encryptionKey",
        "permissions_policy_document": "permissionsPolicyDocument",
        "tags": "tags",
    },
)
class CfnDomainProps:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        encryption_key: typing.Optional[builtins.str] = None,
        permissions_policy_document: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDomain``.

        :param domain_name: A string that specifies the name of the requested domain.
        :param encryption_key: The key used to encrypt the domain.
        :param permissions_policy_document: The document that defines the resource policy that is set on a domain.
        :param tags: A list of tags to be applied to the domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-domain.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codeartifact as codeartifact
            
            # permissions_policy_document: Any
            
            cfn_domain_props = codeartifact.CfnDomainProps(
                domain_name="domainName",
            
                # the properties below are optional
                encryption_key="encryptionKey",
                permissions_policy_document=permissions_policy_document,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8526022dc29bf048819bd5107de54c31efeb0533b3f66d97b700da23aadfdcaf)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument permissions_policy_document", value=permissions_policy_document, expected_type=type_hints["permissions_policy_document"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if permissions_policy_document is not None:
            self._values["permissions_policy_document"] = permissions_policy_document
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''A string that specifies the name of the requested domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-domain.html#cfn-codeartifact-domain-domainname
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[builtins.str]:
        '''The key used to encrypt the domain.

        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-domain.html#cfn-codeartifact-domain-encryptionkey
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_policy_document(self) -> typing.Any:
        '''The document that defines the resource policy that is set on a domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-domain.html#cfn-codeartifact-domain-permissionspolicydocument
        '''
        result = self._values.get("permissions_policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of tags to be applied to the domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-domain.html#cfn-codeartifact-domain-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnRepository(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codeartifact.CfnRepository",
):
    '''A CloudFormation ``AWS::CodeArtifact::Repository``.

    The ``AWS::CodeArtifact::Repository`` resource creates an AWS CodeArtifact repository. CodeArtifact *repositories* contain a set of package versions. For more information about repositories, see the `Repository concepts information <https://docs.aws.amazon.com/codeartifact/latest/ug/codeartifact-concepts.html#welcome-concepts-repository>`_ in the *CodeArtifact User Guide* . For more information about the ``CreateRepository`` API, see `CreateRepository <https://docs.aws.amazon.com/codeartifact/latest/APIReference/API_CreateRepository.html>`_ in the *CodeArtifact API Reference* .

    :cloudformationResource: AWS::CodeArtifact::Repository
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_codeartifact as codeartifact
        
        # permissions_policy_document: Any
        
        cfn_repository = codeartifact.CfnRepository(self, "MyCfnRepository",
            domain_name="domainName",
            repository_name="repositoryName",
        
            # the properties below are optional
            description="description",
            domain_owner="domainOwner",
            external_connections=["externalConnections"],
            permissions_policy_document=permissions_policy_document,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            upstreams=["upstreams"]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        domain_name: builtins.str,
        repository_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        domain_owner: typing.Optional[builtins.str] = None,
        external_connections: typing.Optional[typing.Sequence[builtins.str]] = None,
        permissions_policy_document: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        upstreams: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::CodeArtifact::Repository``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param domain_name: The name of the domain that contains the repository.
        :param repository_name: The name of an upstream repository.
        :param description: A text description of the repository.
        :param domain_owner: The 12-digit account number of the AWS account that owns the domain that contains the repository. It does not include dashes or spaces.
        :param external_connections: An array of external connections associated with the repository.
        :param permissions_policy_document: The document that defines the resource policy that is set on a repository.
        :param tags: A list of tags to be applied to the repository.
        :param upstreams: A list of upstream repositories to associate with the repository. The order of the upstream repositories in the list determines their priority order when AWS CodeArtifact looks for a requested package version. For more information, see `Working with upstream repositories <https://docs.aws.amazon.com/codeartifact/latest/ug/repos-upstream.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4beda843f7cd85c507b77f13f8108ca6903d38b5fd30a22540ff5c94e5bc1e9a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRepositoryProps(
            domain_name=domain_name,
            repository_name=repository_name,
            description=description,
            domain_owner=domain_owner,
            external_connections=external_connections,
            permissions_policy_document=permissions_policy_document,
            tags=tags,
            upstreams=upstreams,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf3ad9a87b5c518d7de036221c6b719bd98bbbd1553c73482b1004ccc6965cad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df6f1708c7c3f287e5f742ae660465434b90d0a16c4123f1d1d62baa7afede25)
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
        '''When you pass the logical ID of this resource, the function returns the Amazon Resource Name (ARN) of the repository.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrDomainName")
    def attr_domain_name(self) -> builtins.str:
        '''When you pass the logical ID of this resource, the function returns the domain name that contains the repository.

        :cloudformationAttribute: DomainName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDomainName"))

    @builtins.property
    @jsii.member(jsii_name="attrDomainOwner")
    def attr_domain_owner(self) -> builtins.str:
        '''When you pass the logical ID of this resource, the function returns the 12-digit account number of the AWS account that owns the domain that contains the repository.

        :cloudformationAttribute: DomainOwner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDomainOwner"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''When you pass the logical ID of this resource, the function returns the name of the repository.

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of tags to be applied to the repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''The name of the domain that contains the repository.

        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-domainname
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4bc436178cb5d88df038bce563f5a73547f15191897783655e01dea20daecec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="permissionsPolicyDocument")
    def permissions_policy_document(self) -> typing.Any:
        '''The document that defines the resource policy that is set on a repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-permissionspolicydocument
        '''
        return typing.cast(typing.Any, jsii.get(self, "permissionsPolicyDocument"))

    @permissions_policy_document.setter
    def permissions_policy_document(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36f1f5bf7d528c7441228961473c2aed8489f8480fd6d02701abffc14580491e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionsPolicyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        '''The name of an upstream repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-repositoryname
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryName"))

    @repository_name.setter
    def repository_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76fc4bad794ceb2c53f7683ed3b2626166cd9ea3df536dc3d9b797219c4d8876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryName", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A text description of the repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20f018e2994306d33f8838eca5917efe41939ee4caca2bc5e9bea5a840b84592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="domainOwner")
    def domain_owner(self) -> typing.Optional[builtins.str]:
        '''The 12-digit account number of the AWS account that owns the domain that contains the repository.

        It does not include dashes or spaces.

        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-domainowner
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainOwner"))

    @domain_owner.setter
    def domain_owner(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88037ea7e4f977db784470653a701189c8bfa00ccea03fe4b32af961677876f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainOwner", value)

    @builtins.property
    @jsii.member(jsii_name="externalConnections")
    def external_connections(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of external connections associated with the repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-externalconnections
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalConnections"))

    @external_connections.setter
    def external_connections(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e06cfd4d9c08109aa9ec478c7d9392c836ab21a90d92ee1bc68022226387f54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalConnections", value)

    @builtins.property
    @jsii.member(jsii_name="upstreams")
    def upstreams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of upstream repositories to associate with the repository.

        The order of the upstream repositories in the list determines their priority order when AWS CodeArtifact looks for a requested package version. For more information, see `Working with upstream repositories <https://docs.aws.amazon.com/codeartifact/latest/ug/repos-upstream.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-upstreams
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "upstreams"))

    @upstreams.setter
    def upstreams(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3f65776d300caddb09b3c6764062172885fe51b5ded337d12cd5340835c02db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "upstreams", value)


@jsii.data_type(
    jsii_type="monocdk.aws_codeartifact.CfnRepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "repository_name": "repositoryName",
        "description": "description",
        "domain_owner": "domainOwner",
        "external_connections": "externalConnections",
        "permissions_policy_document": "permissionsPolicyDocument",
        "tags": "tags",
        "upstreams": "upstreams",
    },
)
class CfnRepositoryProps:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        repository_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        domain_owner: typing.Optional[builtins.str] = None,
        external_connections: typing.Optional[typing.Sequence[builtins.str]] = None,
        permissions_policy_document: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        upstreams: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRepository``.

        :param domain_name: The name of the domain that contains the repository.
        :param repository_name: The name of an upstream repository.
        :param description: A text description of the repository.
        :param domain_owner: The 12-digit account number of the AWS account that owns the domain that contains the repository. It does not include dashes or spaces.
        :param external_connections: An array of external connections associated with the repository.
        :param permissions_policy_document: The document that defines the resource policy that is set on a repository.
        :param tags: A list of tags to be applied to the repository.
        :param upstreams: A list of upstream repositories to associate with the repository. The order of the upstream repositories in the list determines their priority order when AWS CodeArtifact looks for a requested package version. For more information, see `Working with upstream repositories <https://docs.aws.amazon.com/codeartifact/latest/ug/repos-upstream.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codeartifact as codeartifact
            
            # permissions_policy_document: Any
            
            cfn_repository_props = codeartifact.CfnRepositoryProps(
                domain_name="domainName",
                repository_name="repositoryName",
            
                # the properties below are optional
                description="description",
                domain_owner="domainOwner",
                external_connections=["externalConnections"],
                permissions_policy_document=permissions_policy_document,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                upstreams=["upstreams"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a663da476a8eeef8747014cec56da0310cd19e445d2521a3b2e7203298321cf)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domain_owner", value=domain_owner, expected_type=type_hints["domain_owner"])
            check_type(argname="argument external_connections", value=external_connections, expected_type=type_hints["external_connections"])
            check_type(argname="argument permissions_policy_document", value=permissions_policy_document, expected_type=type_hints["permissions_policy_document"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument upstreams", value=upstreams, expected_type=type_hints["upstreams"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
            "repository_name": repository_name,
        }
        if description is not None:
            self._values["description"] = description
        if domain_owner is not None:
            self._values["domain_owner"] = domain_owner
        if external_connections is not None:
            self._values["external_connections"] = external_connections
        if permissions_policy_document is not None:
            self._values["permissions_policy_document"] = permissions_policy_document
        if tags is not None:
            self._values["tags"] = tags
        if upstreams is not None:
            self._values["upstreams"] = upstreams

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''The name of the domain that contains the repository.

        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-domainname
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_name(self) -> builtins.str:
        '''The name of an upstream repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-repositoryname
        '''
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A text description of the repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_owner(self) -> typing.Optional[builtins.str]:
        '''The 12-digit account number of the AWS account that owns the domain that contains the repository.

        It does not include dashes or spaces.

        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-domainowner
        '''
        result = self._values.get("domain_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_connections(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of external connections associated with the repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-externalconnections
        '''
        result = self._values.get("external_connections")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permissions_policy_document(self) -> typing.Any:
        '''The document that defines the resource policy that is set on a repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-permissionspolicydocument
        '''
        result = self._values.get("permissions_policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of tags to be applied to the repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def upstreams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of upstream repositories to associate with the repository.

        The order of the upstream repositories in the list determines their priority order when AWS CodeArtifact looks for a requested package version. For more information, see `Working with upstream repositories <https://docs.aws.amazon.com/codeartifact/latest/ug/repos-upstream.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-upstreams
        '''
        result = self._values.get("upstreams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDomain",
    "CfnDomainProps",
    "CfnRepository",
    "CfnRepositoryProps",
]

publication.publish()

def _typecheckingstub__46bd830d13f2252bff0b03ae80230bad9057d3635d220b46f1c480f1172f021f(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    domain_name: builtins.str,
    encryption_key: typing.Optional[builtins.str] = None,
    permissions_policy_document: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca70bafd86e74bed544d264e027b8f2916766699cd0d66b71e8503577ea238fe(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83570d56280d96e991aebc0c405daeb30de1056c5726e1396fe5a54838b3cb2a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62ed2d6ff457b8e42a55cf060b3a311cc9db25830f4af807d42f3e72e04ce487(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb90e3f7a3c6f10b4017ba1865fdc3adf14646378fa7bd725691c85d41cec0ef(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af4a6722e40e9a10b357d9f56a1f8830f71a73eadf6c433c95ab87ef3f35c76(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8526022dc29bf048819bd5107de54c31efeb0533b3f66d97b700da23aadfdcaf(
    *,
    domain_name: builtins.str,
    encryption_key: typing.Optional[builtins.str] = None,
    permissions_policy_document: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4beda843f7cd85c507b77f13f8108ca6903d38b5fd30a22540ff5c94e5bc1e9a(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    domain_name: builtins.str,
    repository_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    domain_owner: typing.Optional[builtins.str] = None,
    external_connections: typing.Optional[typing.Sequence[builtins.str]] = None,
    permissions_policy_document: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    upstreams: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3ad9a87b5c518d7de036221c6b719bd98bbbd1553c73482b1004ccc6965cad(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df6f1708c7c3f287e5f742ae660465434b90d0a16c4123f1d1d62baa7afede25(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4bc436178cb5d88df038bce563f5a73547f15191897783655e01dea20daecec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f1f5bf7d528c7441228961473c2aed8489f8480fd6d02701abffc14580491e(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76fc4bad794ceb2c53f7683ed3b2626166cd9ea3df536dc3d9b797219c4d8876(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f018e2994306d33f8838eca5917efe41939ee4caca2bc5e9bea5a840b84592(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88037ea7e4f977db784470653a701189c8bfa00ccea03fe4b32af961677876f4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e06cfd4d9c08109aa9ec478c7d9392c836ab21a90d92ee1bc68022226387f54(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f65776d300caddb09b3c6764062172885fe51b5ded337d12cd5340835c02db(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a663da476a8eeef8747014cec56da0310cd19e445d2521a3b2e7203298321cf(
    *,
    domain_name: builtins.str,
    repository_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    domain_owner: typing.Optional[builtins.str] = None,
    external_connections: typing.Optional[typing.Sequence[builtins.str]] = None,
    permissions_policy_document: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    upstreams: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
