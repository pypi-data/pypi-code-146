'''
# Amazon GuardDuty Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_guardduty as guardduty
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for GuardDuty construct libraries](https://constructs.dev/search?q=guardduty)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::GuardDuty resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_GuardDuty.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::GuardDuty](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_GuardDuty.html).

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

from ._jsii import *

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnDetector(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-guardduty.CfnDetector",
):
    '''A CloudFormation ``AWS::GuardDuty::Detector``.

    The ``AWS::GuardDuty::Detector`` resource specifies a new  detector. A detector is an object that represents the  service. A detector is required for  to become operational.

    :cloudformationResource: AWS::GuardDuty::Detector
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_guardduty as guardduty
        
        cfn_detector = guardduty.CfnDetector(self, "MyCfnDetector",
            enable=False,
        
            # the properties below are optional
            data_sources=guardduty.CfnDetector.CFNDataSourceConfigurationsProperty(
                kubernetes=guardduty.CfnDetector.CFNKubernetesConfigurationProperty(
                    audit_logs=guardduty.CfnDetector.CFNKubernetesAuditLogsConfigurationProperty(
                        enable=False
                    )
                ),
                malware_protection=guardduty.CfnDetector.CFNMalwareProtectionConfigurationProperty(
                    scan_ec2_instance_with_findings=guardduty.CfnDetector.CFNScanEc2InstanceWithFindingsConfigurationProperty(
                        ebs_volumes=False
                    )
                ),
                s3_logs=guardduty.CfnDetector.CFNS3LogsConfigurationProperty(
                    enable=False
                )
            ),
            finding_publishing_frequency="findingPublishingFrequency",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        enable: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        data_sources: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetector.CFNDataSourceConfigurationsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        finding_publishing_frequency: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::GuardDuty::Detector``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param enable: Specifies whether the detector is to be enabled on creation.
        :param data_sources: Describes which data sources will be enabled for the detector.
        :param finding_publishing_frequency: Specifies how frequently updated findings are exported.
        :param tags: The tags to be added to a new detector resource. Each tag consists of a key and an optional value, both of which you define. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77536b4016d0000a3ec5d841855bd35c8890cfe93b05262ce314dac200b4d14a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDetectorProps(
            enable=enable,
            data_sources=data_sources,
            finding_publishing_frequency=finding_publishing_frequency,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b3b1797c98a169731fa785dbb77635d594307c5439542a7e72fc4b362404c56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcc3101308c71dfa647260f809ede76130fc43193badcdb96bd18b2327369262)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags to be added to a new detector resource.

        Each tag consists of a key and an optional value, both of which you define.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html#cfn-guardduty-detector-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="enable")
    def enable(self) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
        '''Specifies whether the detector is to be enabled on creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html#cfn-guardduty-detector-enable
        '''
        return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "enable"))

    @enable.setter
    def enable(
        self,
        value: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fffa26e75fe8ccc31f2d77af268fa458b1a87403bc811d9230e27f3946e8a63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value)

    @builtins.property
    @jsii.member(jsii_name="dataSources")
    def data_sources(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.CFNDataSourceConfigurationsProperty"]]:
        '''Describes which data sources will be enabled for the detector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html#cfn-guardduty-detector-datasources
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.CFNDataSourceConfigurationsProperty"]], jsii.get(self, "dataSources"))

    @data_sources.setter
    def data_sources(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.CFNDataSourceConfigurationsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91510a99b1a7ef7cf8356fc2b0f342a928df97f39c261446ca410ac68440d54a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSources", value)

    @builtins.property
    @jsii.member(jsii_name="findingPublishingFrequency")
    def finding_publishing_frequency(self) -> typing.Optional[builtins.str]:
        '''Specifies how frequently updated findings are exported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html#cfn-guardduty-detector-findingpublishingfrequency
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "findingPublishingFrequency"))

    @finding_publishing_frequency.setter
    def finding_publishing_frequency(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__592b51676ab440626d5c83a56d08469fb8472602e17553a1cff2f2308e4b2577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "findingPublishingFrequency", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-guardduty.CfnDetector.CFNDataSourceConfigurationsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kubernetes": "kubernetes",
            "malware_protection": "malwareProtection",
            "s3_logs": "s3Logs",
        },
    )
    class CFNDataSourceConfigurationsProperty:
        def __init__(
            self,
            *,
            kubernetes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetector.CFNKubernetesConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            malware_protection: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetector.CFNMalwareProtectionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_logs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetector.CFNS3LogsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes whether S3 data event logs, Kubernetes audit logs, or Malware Protection will be enabled as a data source when the detector is created.

            :param kubernetes: Describes which Kuberentes data sources are enabled for a detector.
            :param malware_protection: Describes whether Malware Protection will be enabled as a data source.
            :param s3_logs: Describes whether S3 data event logs are enabled as a data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfndatasourceconfigurations.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_guardduty as guardduty
                
                c_fNData_source_configurations_property = guardduty.CfnDetector.CFNDataSourceConfigurationsProperty(
                    kubernetes=guardduty.CfnDetector.CFNKubernetesConfigurationProperty(
                        audit_logs=guardduty.CfnDetector.CFNKubernetesAuditLogsConfigurationProperty(
                            enable=False
                        )
                    ),
                    malware_protection=guardduty.CfnDetector.CFNMalwareProtectionConfigurationProperty(
                        scan_ec2_instance_with_findings=guardduty.CfnDetector.CFNScanEc2InstanceWithFindingsConfigurationProperty(
                            ebs_volumes=False
                        )
                    ),
                    s3_logs=guardduty.CfnDetector.CFNS3LogsConfigurationProperty(
                        enable=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__899d70aec6c1966b8f837326e7dd896ba686a50324252598deb760b15865a3cc)
                check_type(argname="argument kubernetes", value=kubernetes, expected_type=type_hints["kubernetes"])
                check_type(argname="argument malware_protection", value=malware_protection, expected_type=type_hints["malware_protection"])
                check_type(argname="argument s3_logs", value=s3_logs, expected_type=type_hints["s3_logs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kubernetes is not None:
                self._values["kubernetes"] = kubernetes
            if malware_protection is not None:
                self._values["malware_protection"] = malware_protection
            if s3_logs is not None:
                self._values["s3_logs"] = s3_logs

        @builtins.property
        def kubernetes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.CFNKubernetesConfigurationProperty"]]:
            '''Describes which Kuberentes data sources are enabled for a detector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfndatasourceconfigurations.html#cfn-guardduty-detector-cfndatasourceconfigurations-kubernetes
            '''
            result = self._values.get("kubernetes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.CFNKubernetesConfigurationProperty"]], result)

        @builtins.property
        def malware_protection(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.CFNMalwareProtectionConfigurationProperty"]]:
            '''Describes whether Malware Protection will be enabled as a data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfndatasourceconfigurations.html#cfn-guardduty-detector-cfndatasourceconfigurations-malwareprotection
            '''
            result = self._values.get("malware_protection")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.CFNMalwareProtectionConfigurationProperty"]], result)

        @builtins.property
        def s3_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.CFNS3LogsConfigurationProperty"]]:
            '''Describes whether S3 data event logs are enabled as a data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfndatasourceconfigurations.html#cfn-guardduty-detector-cfndatasourceconfigurations-s3logs
            '''
            result = self._values.get("s3_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.CFNS3LogsConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CFNDataSourceConfigurationsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-guardduty.CfnDetector.CFNKubernetesAuditLogsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enable": "enable"},
    )
    class CFNKubernetesAuditLogsConfigurationProperty:
        def __init__(
            self,
            *,
            enable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Describes which optional data sources are enabled for a detector.

            :param enable: Describes whether Kubernetes audit logs are enabled as a data source for the detector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnkubernetesauditlogsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_guardduty as guardduty
                
                c_fNKubernetes_audit_logs_configuration_property = guardduty.CfnDetector.CFNKubernetesAuditLogsConfigurationProperty(
                    enable=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1f801c88c3face68f7b9ade62f2e213a61c43eed1fd35d54e6d529a19080fd1b)
                check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable is not None:
                self._values["enable"] = enable

        @builtins.property
        def enable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Describes whether Kubernetes audit logs are enabled as a data source for the detector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnkubernetesauditlogsconfiguration.html#cfn-guardduty-detector-cfnkubernetesauditlogsconfiguration-enable
            '''
            result = self._values.get("enable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CFNKubernetesAuditLogsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-guardduty.CfnDetector.CFNKubernetesConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"audit_logs": "auditLogs"},
    )
    class CFNKubernetesConfigurationProperty:
        def __init__(
            self,
            *,
            audit_logs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetector.CFNKubernetesAuditLogsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes which Kubernetes protection data sources are enabled for the detector.

            :param audit_logs: Describes whether Kubernetes audit logs are enabled as a data source for the detector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnkubernetesconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_guardduty as guardduty
                
                c_fNKubernetes_configuration_property = guardduty.CfnDetector.CFNKubernetesConfigurationProperty(
                    audit_logs=guardduty.CfnDetector.CFNKubernetesAuditLogsConfigurationProperty(
                        enable=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9b31a054708ad2712642d201fc2ab2fef8e1a456c7be69e0baaa26fa99ac05b3)
                check_type(argname="argument audit_logs", value=audit_logs, expected_type=type_hints["audit_logs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if audit_logs is not None:
                self._values["audit_logs"] = audit_logs

        @builtins.property
        def audit_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.CFNKubernetesAuditLogsConfigurationProperty"]]:
            '''Describes whether Kubernetes audit logs are enabled as a data source for the detector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnkubernetesconfiguration.html#cfn-guardduty-detector-cfnkubernetesconfiguration-auditlogs
            '''
            result = self._values.get("audit_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.CFNKubernetesAuditLogsConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CFNKubernetesConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-guardduty.CfnDetector.CFNMalwareProtectionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "scan_ec2_instance_with_findings": "scanEc2InstanceWithFindings",
        },
    )
    class CFNMalwareProtectionConfigurationProperty:
        def __init__(
            self,
            *,
            scan_ec2_instance_with_findings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetector.CFNScanEc2InstanceWithFindingsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes whether Malware Protection will be enabled as a data source.

            :param scan_ec2_instance_with_findings: Describes the configuration of Malware Protection for EC2 instances with findings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnmalwareprotectionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_guardduty as guardduty
                
                c_fNMalware_protection_configuration_property = guardduty.CfnDetector.CFNMalwareProtectionConfigurationProperty(
                    scan_ec2_instance_with_findings=guardduty.CfnDetector.CFNScanEc2InstanceWithFindingsConfigurationProperty(
                        ebs_volumes=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b3f33ae807e3a1e855943086c0ea1273e3dcc13697d79b6cf383c45ad26669b4)
                check_type(argname="argument scan_ec2_instance_with_findings", value=scan_ec2_instance_with_findings, expected_type=type_hints["scan_ec2_instance_with_findings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if scan_ec2_instance_with_findings is not None:
                self._values["scan_ec2_instance_with_findings"] = scan_ec2_instance_with_findings

        @builtins.property
        def scan_ec2_instance_with_findings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.CFNScanEc2InstanceWithFindingsConfigurationProperty"]]:
            '''Describes the configuration of Malware Protection for EC2 instances with findings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnmalwareprotectionconfiguration.html#cfn-guardduty-detector-cfnmalwareprotectionconfiguration-scanec2instancewithfindings
            '''
            result = self._values.get("scan_ec2_instance_with_findings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.CFNScanEc2InstanceWithFindingsConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CFNMalwareProtectionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-guardduty.CfnDetector.CFNS3LogsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enable": "enable"},
    )
    class CFNS3LogsConfigurationProperty:
        def __init__(
            self,
            *,
            enable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Describes whether S3 data event logs will be enabled as a data source when the detector is created.

            :param enable: The status of S3 data event logs as a data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfns3logsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_guardduty as guardduty
                
                c_fNS3_logs_configuration_property = guardduty.CfnDetector.CFNS3LogsConfigurationProperty(
                    enable=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__130b6edd74713a4b38ec25eca790f24b43c231a8472ebfc84d9cb69693048f0d)
                check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable is not None:
                self._values["enable"] = enable

        @builtins.property
        def enable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''The status of S3 data event logs as a data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfns3logsconfiguration.html#cfn-guardduty-detector-cfns3logsconfiguration-enable
            '''
            result = self._values.get("enable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CFNS3LogsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-guardduty.CfnDetector.CFNScanEc2InstanceWithFindingsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"ebs_volumes": "ebsVolumes"},
    )
    class CFNScanEc2InstanceWithFindingsConfigurationProperty:
        def __init__(
            self,
            *,
            ebs_volumes: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Describes whether Malware Protection for EC2 instances with findings will be enabled as a data source.

            :param ebs_volumes: Describes the configuration for scanning EBS volumes as data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnscanec2instancewithfindingsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_guardduty as guardduty
                
                c_fNScan_ec2_instance_with_findings_configuration_property = guardduty.CfnDetector.CFNScanEc2InstanceWithFindingsConfigurationProperty(
                    ebs_volumes=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d903e1c3d6c92e4d4f84b4c82fdcfa8ebad493d4cd2d16944680874255d6a15)
                check_type(argname="argument ebs_volumes", value=ebs_volumes, expected_type=type_hints["ebs_volumes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ebs_volumes is not None:
                self._values["ebs_volumes"] = ebs_volumes

        @builtins.property
        def ebs_volumes(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Describes the configuration for scanning EBS volumes as data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnscanec2instancewithfindingsconfiguration.html#cfn-guardduty-detector-cfnscanec2instancewithfindingsconfiguration-ebsvolumes
            '''
            result = self._values.get("ebs_volumes")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CFNScanEc2InstanceWithFindingsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-guardduty.CfnDetectorProps",
    jsii_struct_bases=[],
    name_mapping={
        "enable": "enable",
        "data_sources": "dataSources",
        "finding_publishing_frequency": "findingPublishingFrequency",
        "tags": "tags",
    },
)
class CfnDetectorProps:
    def __init__(
        self,
        *,
        enable: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        data_sources: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetector.CFNDataSourceConfigurationsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        finding_publishing_frequency: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDetector``.

        :param enable: Specifies whether the detector is to be enabled on creation.
        :param data_sources: Describes which data sources will be enabled for the detector.
        :param finding_publishing_frequency: Specifies how frequently updated findings are exported.
        :param tags: The tags to be added to a new detector resource. Each tag consists of a key and an optional value, both of which you define. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_guardduty as guardduty
            
            cfn_detector_props = guardduty.CfnDetectorProps(
                enable=False,
            
                # the properties below are optional
                data_sources=guardduty.CfnDetector.CFNDataSourceConfigurationsProperty(
                    kubernetes=guardduty.CfnDetector.CFNKubernetesConfigurationProperty(
                        audit_logs=guardduty.CfnDetector.CFNKubernetesAuditLogsConfigurationProperty(
                            enable=False
                        )
                    ),
                    malware_protection=guardduty.CfnDetector.CFNMalwareProtectionConfigurationProperty(
                        scan_ec2_instance_with_findings=guardduty.CfnDetector.CFNScanEc2InstanceWithFindingsConfigurationProperty(
                            ebs_volumes=False
                        )
                    ),
                    s3_logs=guardduty.CfnDetector.CFNS3LogsConfigurationProperty(
                        enable=False
                    )
                ),
                finding_publishing_frequency="findingPublishingFrequency",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__910648eac4ef910754ec562e293d771a83bbc84331cd78e3f5b0be01863b3df5)
            check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
            check_type(argname="argument data_sources", value=data_sources, expected_type=type_hints["data_sources"])
            check_type(argname="argument finding_publishing_frequency", value=finding_publishing_frequency, expected_type=type_hints["finding_publishing_frequency"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable": enable,
        }
        if data_sources is not None:
            self._values["data_sources"] = data_sources
        if finding_publishing_frequency is not None:
            self._values["finding_publishing_frequency"] = finding_publishing_frequency
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def enable(self) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
        '''Specifies whether the detector is to be enabled on creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html#cfn-guardduty-detector-enable
        '''
        result = self._values.get("enable")
        assert result is not None, "Required property 'enable' is missing"
        return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def data_sources(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDetector.CFNDataSourceConfigurationsProperty]]:
        '''Describes which data sources will be enabled for the detector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html#cfn-guardduty-detector-datasources
        '''
        result = self._values.get("data_sources")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDetector.CFNDataSourceConfigurationsProperty]], result)

    @builtins.property
    def finding_publishing_frequency(self) -> typing.Optional[builtins.str]:
        '''Specifies how frequently updated findings are exported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html#cfn-guardduty-detector-findingpublishingfrequency
        '''
        result = self._values.get("finding_publishing_frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags to be added to a new detector resource.

        Each tag consists of a key and an optional value, both of which you define.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html#cfn-guardduty-detector-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDetectorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnFilter(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-guardduty.CfnFilter",
):
    '''A CloudFormation ``AWS::GuardDuty::Filter``.

    The ``AWS::GuardDuty::Filter`` resource specifies a new filter defined by the provided ``findingCriteria`` .

    :cloudformationResource: AWS::GuardDuty::Filter
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_guardduty as guardduty
        
        # criterion: Any
        
        cfn_filter = guardduty.CfnFilter(self, "MyCfnFilter",
            action="action",
            description="description",
            detector_id="detectorId",
            finding_criteria=guardduty.CfnFilter.FindingCriteriaProperty(
                criterion=criterion,
                item_type=guardduty.CfnFilter.ConditionProperty(
                    eq=["eq"],
                    equal_to=["equalTo"],
                    greater_than=123,
                    greater_than_or_equal=123,
                    gt=123,
                    gte=123,
                    less_than=123,
                    less_than_or_equal=123,
                    lt=123,
                    lte=123,
                    neq=["neq"],
                    not_equals=["notEquals"]
                )
            ),
            name="name",
            rank=123,
        
            # the properties below are optional
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        action: builtins.str,
        description: builtins.str,
        detector_id: builtins.str,
        finding_criteria: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFilter.FindingCriteriaProperty", typing.Dict[builtins.str, typing.Any]]],
        name: builtins.str,
        rank: jsii.Number,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::GuardDuty::Filter``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param action: Specifies the action that is to be applied to the findings that match the filter.
        :param description: The description of the filter. Valid special characters include period (.), underscore (_), dash (-), and whitespace. The new line character is considered to be an invalid input for description.
        :param detector_id: The ID of the detector belonging to the GuardDuty account that you want to create a filter for.
        :param finding_criteria: Represents the criteria to be used in the filter for querying findings.
        :param name: The name of the filter. Valid characters include period (.), underscore (_), dash (-), and alphanumeric characters. A whitespace is considered to be an invalid character.
        :param rank: Specifies the position of the filter in the list of current filters. Also specifies the order in which this filter is applied to the findings. The minimum value for this property is 1 and the maximum is 100. By default, filters may not be created in the same order as they are ranked. To ensure that the filters are created in the expected order, you can use an optional attribute, `DependsOn <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ , with the following syntax: ``"DependsOn":[ "ObjectName" ]`` .
        :param tags: The tags to be added to a new filter resource. Each tag consists of a key and an optional value, both of which you define. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d59704e18b0438fbe06d1aa6d1337a08321e4ec1ec59a65399fef149c29c0c4b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFilterProps(
            action=action,
            description=description,
            detector_id=detector_id,
            finding_criteria=finding_criteria,
            name=name,
            rank=rank,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a02a31a137ef6f396e06fdc129a6afffe6888df2e369316b7dfa688974ded35f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ed63e15ef42c37e2721fa35aa591455f0a9b26655796dfed317adbd9774ad25)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags to be added to a new filter resource.

        Each tag consists of a key and an optional value, both of which you define.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        '''Specifies the action that is to be applied to the findings that match the filter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-action
        '''
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9860df724d8812fbaac988873987339e7924d0cdb0bee5a3bfe36a07e511530b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''The description of the filter.

        Valid special characters include period (.), underscore (_), dash (-), and whitespace. The new line character is considered to be an invalid input for description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-description
        '''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af7c5bcc380a3ba3477a6d89e689c1a85f7674be7f868ec8d09b8b65bc1f9529)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="detectorId")
    def detector_id(self) -> builtins.str:
        '''The ID of the detector belonging to the GuardDuty account that you want to create a filter for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-detectorid
        '''
        return typing.cast(builtins.str, jsii.get(self, "detectorId"))

    @detector_id.setter
    def detector_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__598af88e12698c7eb203e95b500a02cc6affed65caf848b84719d25814b0ae74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectorId", value)

    @builtins.property
    @jsii.member(jsii_name="findingCriteria")
    def finding_criteria(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFilter.FindingCriteriaProperty"]:
        '''Represents the criteria to be used in the filter for querying findings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-findingcriteria
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFilter.FindingCriteriaProperty"], jsii.get(self, "findingCriteria"))

    @finding_criteria.setter
    def finding_criteria(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFilter.FindingCriteriaProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da3d708938c37f389813647c1b9ee1421888ab05d928b6aa659d6065c92c2c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "findingCriteria", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the filter.

        Valid characters include period (.), underscore (_), dash (-), and alphanumeric characters. A whitespace is considered to be an invalid character.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30de47e862af84c0151c97875a4777e753003af9fae2160c03341c6ae6ec92d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="rank")
    def rank(self) -> jsii.Number:
        '''Specifies the position of the filter in the list of current filters.

        Also specifies the order in which this filter is applied to the findings. The minimum value for this property is 1 and the maximum is 100.

        By default, filters may not be created in the same order as they are ranked. To ensure that the filters are created in the expected order, you can use an optional attribute, `DependsOn <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ , with the following syntax: ``"DependsOn":[ "ObjectName" ]`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-rank
        '''
        return typing.cast(jsii.Number, jsii.get(self, "rank"))

    @rank.setter
    def rank(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25265e33ad28230aafb3875758d9ef44cfca92021c8b2e4ca1033dca7e26ba49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rank", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-guardduty.CfnFilter.ConditionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "eq": "eq",
            "equal_to": "equalTo",
            "greater_than": "greaterThan",
            "greater_than_or_equal": "greaterThanOrEqual",
            "gt": "gt",
            "gte": "gte",
            "less_than": "lessThan",
            "less_than_or_equal": "lessThanOrEqual",
            "lt": "lt",
            "lte": "lte",
            "neq": "neq",
            "not_equals": "notEquals",
        },
    )
    class ConditionProperty:
        def __init__(
            self,
            *,
            eq: typing.Optional[typing.Sequence[builtins.str]] = None,
            equal_to: typing.Optional[typing.Sequence[builtins.str]] = None,
            greater_than: typing.Optional[jsii.Number] = None,
            greater_than_or_equal: typing.Optional[jsii.Number] = None,
            gt: typing.Optional[jsii.Number] = None,
            gte: typing.Optional[jsii.Number] = None,
            less_than: typing.Optional[jsii.Number] = None,
            less_than_or_equal: typing.Optional[jsii.Number] = None,
            lt: typing.Optional[jsii.Number] = None,
            lte: typing.Optional[jsii.Number] = None,
            neq: typing.Optional[typing.Sequence[builtins.str]] = None,
            not_equals: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies the condition to apply to a single field when filtering through  findings.

            :param eq: Represents the equal condition to apply to a single field when querying for findings.
            :param equal_to: Represents an *equal* ** condition to be applied to a single field when querying for findings.
            :param greater_than: Represents a *greater than* condition to be applied to a single field when querying for findings.
            :param greater_than_or_equal: Represents a *greater than or equal* condition to be applied to a single field when querying for findings.
            :param gt: Represents a *greater than* condition to be applied to a single field when querying for findings.
            :param gte: Represents the greater than or equal condition to apply to a single field when querying for findings.
            :param less_than: Represents a *less than* condition to be applied to a single field when querying for findings.
            :param less_than_or_equal: Represents a *less than or equal* condition to be applied to a single field when querying for findings.
            :param lt: Represents the less than condition to apply to a single field when querying for findings.
            :param lte: Represents the less than or equal condition to apply to a single field when querying for findings.
            :param neq: Represents the not equal condition to apply to a single field when querying for findings.
            :param not_equals: Represents a *not equal* ** condition to be applied to a single field when querying for findings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_guardduty as guardduty
                
                condition_property = guardduty.CfnFilter.ConditionProperty(
                    eq=["eq"],
                    equal_to=["equalTo"],
                    greater_than=123,
                    greater_than_or_equal=123,
                    gt=123,
                    gte=123,
                    less_than=123,
                    less_than_or_equal=123,
                    lt=123,
                    lte=123,
                    neq=["neq"],
                    not_equals=["notEquals"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f9fc54e5cf7ac155ee7cfc65abf59eb2b3c0cbf3836e8f6d026adf79285b31f1)
                check_type(argname="argument eq", value=eq, expected_type=type_hints["eq"])
                check_type(argname="argument equal_to", value=equal_to, expected_type=type_hints["equal_to"])
                check_type(argname="argument greater_than", value=greater_than, expected_type=type_hints["greater_than"])
                check_type(argname="argument greater_than_or_equal", value=greater_than_or_equal, expected_type=type_hints["greater_than_or_equal"])
                check_type(argname="argument gt", value=gt, expected_type=type_hints["gt"])
                check_type(argname="argument gte", value=gte, expected_type=type_hints["gte"])
                check_type(argname="argument less_than", value=less_than, expected_type=type_hints["less_than"])
                check_type(argname="argument less_than_or_equal", value=less_than_or_equal, expected_type=type_hints["less_than_or_equal"])
                check_type(argname="argument lt", value=lt, expected_type=type_hints["lt"])
                check_type(argname="argument lte", value=lte, expected_type=type_hints["lte"])
                check_type(argname="argument neq", value=neq, expected_type=type_hints["neq"])
                check_type(argname="argument not_equals", value=not_equals, expected_type=type_hints["not_equals"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if eq is not None:
                self._values["eq"] = eq
            if equal_to is not None:
                self._values["equal_to"] = equal_to
            if greater_than is not None:
                self._values["greater_than"] = greater_than
            if greater_than_or_equal is not None:
                self._values["greater_than_or_equal"] = greater_than_or_equal
            if gt is not None:
                self._values["gt"] = gt
            if gte is not None:
                self._values["gte"] = gte
            if less_than is not None:
                self._values["less_than"] = less_than
            if less_than_or_equal is not None:
                self._values["less_than_or_equal"] = less_than_or_equal
            if lt is not None:
                self._values["lt"] = lt
            if lte is not None:
                self._values["lte"] = lte
            if neq is not None:
                self._values["neq"] = neq
            if not_equals is not None:
                self._values["not_equals"] = not_equals

        @builtins.property
        def eq(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Represents the equal condition to apply to a single field when querying for findings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-eq
            '''
            result = self._values.get("eq")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def equal_to(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Represents an *equal* ** condition to be applied to a single field when querying for findings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-equals
            '''
            result = self._values.get("equal_to")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def greater_than(self) -> typing.Optional[jsii.Number]:
            '''Represents a *greater than* condition to be applied to a single field when querying for findings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-greaterthan
            '''
            result = self._values.get("greater_than")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def greater_than_or_equal(self) -> typing.Optional[jsii.Number]:
            '''Represents a *greater than or equal* condition to be applied to a single field when querying for findings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-greaterthanorequal
            '''
            result = self._values.get("greater_than_or_equal")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def gt(self) -> typing.Optional[jsii.Number]:
            '''Represents a *greater than* condition to be applied to a single field when querying for findings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-gt
            '''
            result = self._values.get("gt")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def gte(self) -> typing.Optional[jsii.Number]:
            '''Represents the greater than or equal condition to apply to a single field when querying for findings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-gte
            '''
            result = self._values.get("gte")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def less_than(self) -> typing.Optional[jsii.Number]:
            '''Represents a *less than* condition to be applied to a single field when querying for findings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-lessthan
            '''
            result = self._values.get("less_than")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def less_than_or_equal(self) -> typing.Optional[jsii.Number]:
            '''Represents a *less than or equal* condition to be applied to a single field when querying for findings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-lessthanorequal
            '''
            result = self._values.get("less_than_or_equal")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def lt(self) -> typing.Optional[jsii.Number]:
            '''Represents the less than condition to apply to a single field when querying for findings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-lt
            '''
            result = self._values.get("lt")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def lte(self) -> typing.Optional[jsii.Number]:
            '''Represents the less than or equal condition to apply to a single field when querying for findings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-lte
            '''
            result = self._values.get("lte")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def neq(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Represents the not equal condition to apply to a single field when querying for findings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-neq
            '''
            result = self._values.get("neq")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def not_equals(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Represents a *not equal* ** condition to be applied to a single field when querying for findings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-notequals
            '''
            result = self._values.get("not_equals")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-guardduty.CfnFilter.FindingCriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={"criterion": "criterion", "item_type": "itemType"},
    )
    class FindingCriteriaProperty:
        def __init__(
            self,
            *,
            criterion: typing.Any = None,
            item_type: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFilter.ConditionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents a map of finding properties that match specified conditions and values when querying findings.

            :param criterion: Represents a map of finding properties that match specified conditions and values when querying findings. For a mapping of JSON criterion to their console equivalent see `Finding criteria <https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_filter-findings.html#filter_criteria>`_ . The following are the available criterion: - accountId - region - confidence - id - resource.accessKeyDetails.accessKeyId - resource.accessKeyDetails.principalId - resource.accessKeyDetails.userName - resource.accessKeyDetails.userType - resource.instanceDetails.iamInstanceProfile.id - resource.instanceDetails.imageId - resource.instanceDetails.instanceId - resource.instanceDetails.outpostArn - resource.instanceDetails.networkInterfaces.ipv6Addresses - resource.instanceDetails.networkInterfaces.privateIpAddresses.privateIpAddress - resource.instanceDetails.networkInterfaces.publicDnsName - resource.instanceDetails.networkInterfaces.publicIp - resource.instanceDetails.networkInterfaces.securityGroups.groupId - resource.instanceDetails.networkInterfaces.securityGroups.groupName - resource.instanceDetails.networkInterfaces.subnetId - resource.instanceDetails.networkInterfaces.vpcId - resource.instanceDetails.tags.key - resource.instanceDetails.tags.value - resource.resourceType - service.action.actionType - service.action.awsApiCallAction.api - service.action.awsApiCallAction.callerType - service.action.awsApiCallAction.errorCode - service.action.awsApiCallAction.remoteIpDetails.city.cityName - service.action.awsApiCallAction.remoteIpDetails.country.countryName - service.action.awsApiCallAction.remoteIpDetails.ipAddressV4 - service.action.awsApiCallAction.remoteIpDetails.organization.asn - service.action.awsApiCallAction.remoteIpDetails.organization.asnOrg - service.action.awsApiCallAction.serviceName - service.action.dnsRequestAction.domain - service.action.networkConnectionAction.blocked - service.action.networkConnectionAction.connectionDirection - service.action.networkConnectionAction.localPortDetails.port - service.action.networkConnectionAction.protocol - service.action.networkConnectionAction.localIpDetails.ipAddressV4 - service.action.networkConnectionAction.remoteIpDetails.city.cityName - service.action.networkConnectionAction.remoteIpDetails.country.countryName - service.action.networkConnectionAction.remoteIpDetails.ipAddressV4 - service.action.networkConnectionAction.remoteIpDetails.organization.asn - service.action.networkConnectionAction.remoteIpDetails.organization.asnOrg - service.action.networkConnectionAction.remotePortDetails.port - service.additionalInfo.threatListName - service.archived When this attribute is set to TRUE, only archived findings are listed. When it's set to FALSE, only unarchived findings are listed. When this attribute is not set, all existing findings are listed. - service.resourceRole - severity - type - updatedAt Type: ISO 8601 string format: YYYY-MM-DDTHH:MM:SS.SSSZ or YYYY-MM-DDTHH:MM:SSZ depending on whether the value contains milliseconds.
            :param item_type: Specifies the condition to be applied to a single field when filtering through findings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-findingcriteria.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_guardduty as guardduty
                
                # criterion: Any
                
                finding_criteria_property = guardduty.CfnFilter.FindingCriteriaProperty(
                    criterion=criterion,
                    item_type=guardduty.CfnFilter.ConditionProperty(
                        eq=["eq"],
                        equal_to=["equalTo"],
                        greater_than=123,
                        greater_than_or_equal=123,
                        gt=123,
                        gte=123,
                        less_than=123,
                        less_than_or_equal=123,
                        lt=123,
                        lte=123,
                        neq=["neq"],
                        not_equals=["notEquals"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3c360e91d559446b5c6a87b00db6959dff4f0618cce047315001e88dab0e4a74)
                check_type(argname="argument criterion", value=criterion, expected_type=type_hints["criterion"])
                check_type(argname="argument item_type", value=item_type, expected_type=type_hints["item_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if criterion is not None:
                self._values["criterion"] = criterion
            if item_type is not None:
                self._values["item_type"] = item_type

        @builtins.property
        def criterion(self) -> typing.Any:
            '''Represents a map of finding properties that match specified conditions and values when querying findings.

            For a mapping of JSON criterion to their console equivalent see `Finding criteria <https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_filter-findings.html#filter_criteria>`_ . The following are the available criterion:

            - accountId
            - region
            - confidence
            - id
            - resource.accessKeyDetails.accessKeyId
            - resource.accessKeyDetails.principalId
            - resource.accessKeyDetails.userName
            - resource.accessKeyDetails.userType
            - resource.instanceDetails.iamInstanceProfile.id
            - resource.instanceDetails.imageId
            - resource.instanceDetails.instanceId
            - resource.instanceDetails.outpostArn
            - resource.instanceDetails.networkInterfaces.ipv6Addresses
            - resource.instanceDetails.networkInterfaces.privateIpAddresses.privateIpAddress
            - resource.instanceDetails.networkInterfaces.publicDnsName
            - resource.instanceDetails.networkInterfaces.publicIp
            - resource.instanceDetails.networkInterfaces.securityGroups.groupId
            - resource.instanceDetails.networkInterfaces.securityGroups.groupName
            - resource.instanceDetails.networkInterfaces.subnetId
            - resource.instanceDetails.networkInterfaces.vpcId
            - resource.instanceDetails.tags.key
            - resource.instanceDetails.tags.value
            - resource.resourceType
            - service.action.actionType
            - service.action.awsApiCallAction.api
            - service.action.awsApiCallAction.callerType
            - service.action.awsApiCallAction.errorCode
            - service.action.awsApiCallAction.remoteIpDetails.city.cityName
            - service.action.awsApiCallAction.remoteIpDetails.country.countryName
            - service.action.awsApiCallAction.remoteIpDetails.ipAddressV4
            - service.action.awsApiCallAction.remoteIpDetails.organization.asn
            - service.action.awsApiCallAction.remoteIpDetails.organization.asnOrg
            - service.action.awsApiCallAction.serviceName
            - service.action.dnsRequestAction.domain
            - service.action.networkConnectionAction.blocked
            - service.action.networkConnectionAction.connectionDirection
            - service.action.networkConnectionAction.localPortDetails.port
            - service.action.networkConnectionAction.protocol
            - service.action.networkConnectionAction.localIpDetails.ipAddressV4
            - service.action.networkConnectionAction.remoteIpDetails.city.cityName
            - service.action.networkConnectionAction.remoteIpDetails.country.countryName
            - service.action.networkConnectionAction.remoteIpDetails.ipAddressV4
            - service.action.networkConnectionAction.remoteIpDetails.organization.asn
            - service.action.networkConnectionAction.remoteIpDetails.organization.asnOrg
            - service.action.networkConnectionAction.remotePortDetails.port
            - service.additionalInfo.threatListName
            - service.archived

            When this attribute is set to TRUE, only archived findings are listed. When it's set to FALSE, only unarchived findings are listed. When this attribute is not set, all existing findings are listed.

            - service.resourceRole
            - severity
            - type
            - updatedAt

            Type: ISO 8601 string format: YYYY-MM-DDTHH:MM:SS.SSSZ or YYYY-MM-DDTHH:MM:SSZ depending on whether the value contains milliseconds.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-findingcriteria.html#cfn-guardduty-filter-findingcriteria-criterion
            '''
            result = self._values.get("criterion")
            return typing.cast(typing.Any, result)

        @builtins.property
        def item_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFilter.ConditionProperty"]]:
            '''Specifies the condition to be applied to a single field when filtering through findings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-findingcriteria.html#cfn-guardduty-filter-findingcriteria-itemtype
            '''
            result = self._values.get("item_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFilter.ConditionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FindingCriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-guardduty.CfnFilterProps",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "description": "description",
        "detector_id": "detectorId",
        "finding_criteria": "findingCriteria",
        "name": "name",
        "rank": "rank",
        "tags": "tags",
    },
)
class CfnFilterProps:
    def __init__(
        self,
        *,
        action: builtins.str,
        description: builtins.str,
        detector_id: builtins.str,
        finding_criteria: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFilter.FindingCriteriaProperty, typing.Dict[builtins.str, typing.Any]]],
        name: builtins.str,
        rank: jsii.Number,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnFilter``.

        :param action: Specifies the action that is to be applied to the findings that match the filter.
        :param description: The description of the filter. Valid special characters include period (.), underscore (_), dash (-), and whitespace. The new line character is considered to be an invalid input for description.
        :param detector_id: The ID of the detector belonging to the GuardDuty account that you want to create a filter for.
        :param finding_criteria: Represents the criteria to be used in the filter for querying findings.
        :param name: The name of the filter. Valid characters include period (.), underscore (_), dash (-), and alphanumeric characters. A whitespace is considered to be an invalid character.
        :param rank: Specifies the position of the filter in the list of current filters. Also specifies the order in which this filter is applied to the findings. The minimum value for this property is 1 and the maximum is 100. By default, filters may not be created in the same order as they are ranked. To ensure that the filters are created in the expected order, you can use an optional attribute, `DependsOn <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ , with the following syntax: ``"DependsOn":[ "ObjectName" ]`` .
        :param tags: The tags to be added to a new filter resource. Each tag consists of a key and an optional value, both of which you define. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_guardduty as guardduty
            
            # criterion: Any
            
            cfn_filter_props = guardduty.CfnFilterProps(
                action="action",
                description="description",
                detector_id="detectorId",
                finding_criteria=guardduty.CfnFilter.FindingCriteriaProperty(
                    criterion=criterion,
                    item_type=guardduty.CfnFilter.ConditionProperty(
                        eq=["eq"],
                        equal_to=["equalTo"],
                        greater_than=123,
                        greater_than_or_equal=123,
                        gt=123,
                        gte=123,
                        less_than=123,
                        less_than_or_equal=123,
                        lt=123,
                        lte=123,
                        neq=["neq"],
                        not_equals=["notEquals"]
                    )
                ),
                name="name",
                rank=123,
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__576d2dc9e3d4e5d9678611cb75e1927147505427b11719347876376cc7a3938f)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument detector_id", value=detector_id, expected_type=type_hints["detector_id"])
            check_type(argname="argument finding_criteria", value=finding_criteria, expected_type=type_hints["finding_criteria"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rank", value=rank, expected_type=type_hints["rank"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "description": description,
            "detector_id": detector_id,
            "finding_criteria": finding_criteria,
            "name": name,
            "rank": rank,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def action(self) -> builtins.str:
        '''Specifies the action that is to be applied to the findings that match the filter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-action
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> builtins.str:
        '''The description of the filter.

        Valid special characters include period (.), underscore (_), dash (-), and whitespace. The new line character is considered to be an invalid input for description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def detector_id(self) -> builtins.str:
        '''The ID of the detector belonging to the GuardDuty account that you want to create a filter for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-detectorid
        '''
        result = self._values.get("detector_id")
        assert result is not None, "Required property 'detector_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def finding_criteria(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFilter.FindingCriteriaProperty]:
        '''Represents the criteria to be used in the filter for querying findings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-findingcriteria
        '''
        result = self._values.get("finding_criteria")
        assert result is not None, "Required property 'finding_criteria' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFilter.FindingCriteriaProperty], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the filter.

        Valid characters include period (.), underscore (_), dash (-), and alphanumeric characters. A whitespace is considered to be an invalid character.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rank(self) -> jsii.Number:
        '''Specifies the position of the filter in the list of current filters.

        Also specifies the order in which this filter is applied to the findings. The minimum value for this property is 1 and the maximum is 100.

        By default, filters may not be created in the same order as they are ranked. To ensure that the filters are created in the expected order, you can use an optional attribute, `DependsOn <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ , with the following syntax: ``"DependsOn":[ "ObjectName" ]`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-rank
        '''
        result = self._values.get("rank")
        assert result is not None, "Required property 'rank' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags to be added to a new filter resource.

        Each tag consists of a key and an optional value, both of which you define.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFilterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnIPSet(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-guardduty.CfnIPSet",
):
    '''A CloudFormation ``AWS::GuardDuty::IPSet``.

    The ``AWS::GuardDuty::IPSet`` resource specifies a new ``IPSet`` . An ``IPSet`` is a list of trusted IP addresses from which secure communication is allowed with AWS infrastructure and applications.

    :cloudformationResource: AWS::GuardDuty::IPSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_guardduty as guardduty
        
        cfn_iPSet = guardduty.CfnIPSet(self, "MyCfnIPSet",
            activate=False,
            detector_id="detectorId",
            format="format",
            location="location",
        
            # the properties below are optional
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        activate: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        detector_id: builtins.str,
        format: builtins.str,
        location: builtins.str,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::GuardDuty::IPSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param activate: Indicates whether or not uses the ``IPSet`` .
        :param detector_id: The unique ID of the detector of the GuardDuty account that you want to create an IPSet for.
        :param format: The format of the file that contains the IPSet.
        :param location: The URI of the file that contains the IPSet.
        :param name: The user-friendly name to identify the IPSet. Allowed characters are alphanumerics, spaces, hyphens (-), and underscores (_).
        :param tags: The tags to be added to a new IP set resource. Each tag consists of a key and an optional value, both of which you define. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c134d35f291b37ac2047795a554de0411cf347c953853187814e810bcbbd0ff)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnIPSetProps(
            activate=activate,
            detector_id=detector_id,
            format=format,
            location=location,
            name=name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32f332f7fef9c05011c9733212834fe89df441c417428ed49fb840e328ad0197)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7365800f2af5d67a70011e0e351be07580e61655127e31ec2167da3cf0c398a4)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags to be added to a new IP set resource.

        Each tag consists of a key and an optional value, both of which you define.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="activate")
    def activate(
        self,
    ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
        '''Indicates whether or not  uses the ``IPSet`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-activate
        '''
        return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "activate"))

    @activate.setter
    def activate(
        self,
        value: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f58e93d0f7732e7f62d41ec80bdc68b189e7c8c78ed8b7e4e40cfeaa09be331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activate", value)

    @builtins.property
    @jsii.member(jsii_name="detectorId")
    def detector_id(self) -> builtins.str:
        '''The unique ID of the detector of the GuardDuty account that you want to create an IPSet for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-detectorid
        '''
        return typing.cast(builtins.str, jsii.get(self, "detectorId"))

    @detector_id.setter
    def detector_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1fe4a135ecbf5dba641a09e0227041e2718d812c15ec254f5e3f5ec26b99285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectorId", value)

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        '''The format of the file that contains the IPSet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-format
        '''
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @format.setter
    def format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00ffd1cd8b1da508c98aab6d97522699268ea5e85d470b124629b912aaa23c82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "format", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        '''The URI of the file that contains the IPSet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-location
        '''
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57225703288cbac1baa8bf095f82e841fb1c54fff68a20b45b66f39b102ce407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The user-friendly name to identify the IPSet.

        Allowed characters are alphanumerics, spaces, hyphens (-), and underscores (_).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3db771dea1fa969488c477dce62dc4a10d5498937a07148dc72e674dca84f99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-guardduty.CfnIPSetProps",
    jsii_struct_bases=[],
    name_mapping={
        "activate": "activate",
        "detector_id": "detectorId",
        "format": "format",
        "location": "location",
        "name": "name",
        "tags": "tags",
    },
)
class CfnIPSetProps:
    def __init__(
        self,
        *,
        activate: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        detector_id: builtins.str,
        format: builtins.str,
        location: builtins.str,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnIPSet``.

        :param activate: Indicates whether or not uses the ``IPSet`` .
        :param detector_id: The unique ID of the detector of the GuardDuty account that you want to create an IPSet for.
        :param format: The format of the file that contains the IPSet.
        :param location: The URI of the file that contains the IPSet.
        :param name: The user-friendly name to identify the IPSet. Allowed characters are alphanumerics, spaces, hyphens (-), and underscores (_).
        :param tags: The tags to be added to a new IP set resource. Each tag consists of a key and an optional value, both of which you define. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_guardduty as guardduty
            
            cfn_iPSet_props = guardduty.CfnIPSetProps(
                activate=False,
                detector_id="detectorId",
                format="format",
                location="location",
            
                # the properties below are optional
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ec9911f0a94679b251896b402da0fea72a925976e842d59f3c6edf39ec67e31)
            check_type(argname="argument activate", value=activate, expected_type=type_hints["activate"])
            check_type(argname="argument detector_id", value=detector_id, expected_type=type_hints["detector_id"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "activate": activate,
            "detector_id": detector_id,
            "format": format,
            "location": location,
        }
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def activate(
        self,
    ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
        '''Indicates whether or not  uses the ``IPSet`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-activate
        '''
        result = self._values.get("activate")
        assert result is not None, "Required property 'activate' is missing"
        return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def detector_id(self) -> builtins.str:
        '''The unique ID of the detector of the GuardDuty account that you want to create an IPSet for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-detectorid
        '''
        result = self._values.get("detector_id")
        assert result is not None, "Required property 'detector_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def format(self) -> builtins.str:
        '''The format of the file that contains the IPSet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-format
        '''
        result = self._values.get("format")
        assert result is not None, "Required property 'format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The URI of the file that contains the IPSet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-location
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The user-friendly name to identify the IPSet.

        Allowed characters are alphanumerics, spaces, hyphens (-), and underscores (_).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags to be added to a new IP set resource.

        Each tag consists of a key and an optional value, both of which you define.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIPSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnMaster(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-guardduty.CfnMaster",
):
    '''A CloudFormation ``AWS::GuardDuty::Master``.

    You can use the ``AWS::GuardDuty::Master`` resource in a  member account to accept an invitation from a  administrator account. The invitation to the member account must be sent prior to using the ``AWS::GuardDuty::Master`` resource to accept the administrator account's invitation. You can invite a member account by using the ``InviteMembers`` operation of the  API, or by creating an ``AWS::GuardDuty::Member`` resource.

    :cloudformationResource: AWS::GuardDuty::Master
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-master.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_guardduty as guardduty
        
        cfn_master = guardduty.CfnMaster(self, "MyCfnMaster",
            detector_id="detectorId",
            master_id="masterId",
        
            # the properties below are optional
            invitation_id="invitationId"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        detector_id: builtins.str,
        master_id: builtins.str,
        invitation_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::GuardDuty::Master``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param detector_id: The unique ID of the detector of the GuardDuty member account.
        :param master_id: The AWS account ID of the account designated as the administrator account.
        :param invitation_id: The ID of the invitation that is sent to the account designated as a member account. You can find the invitation ID by using the ListInvitation action of the API.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4193b2d1c1a68e693da4f5009d8303d28c0f45442262fe975cb7eb24ba22fd4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMasterProps(
            detector_id=detector_id, master_id=master_id, invitation_id=invitation_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed8533b9c9e277cac8a57e94b0bbfc6889143a795ad3ea63eaa08ba6f3bacf6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__215bc73a3c255ceea2df130b26e0928f92ef4936147e04e4fc11c3bf2c1dad1a)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="detectorId")
    def detector_id(self) -> builtins.str:
        '''The unique ID of the detector of the GuardDuty member account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-master.html#cfn-guardduty-master-detectorid
        '''
        return typing.cast(builtins.str, jsii.get(self, "detectorId"))

    @detector_id.setter
    def detector_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53ab188fe442680b4c5a8413e9b30fc0efef5dc15e303f9b8196056f6c9a4911)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectorId", value)

    @builtins.property
    @jsii.member(jsii_name="masterId")
    def master_id(self) -> builtins.str:
        '''The AWS account ID of the account designated as the  administrator account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-master.html#cfn-guardduty-master-masterid
        '''
        return typing.cast(builtins.str, jsii.get(self, "masterId"))

    @master_id.setter
    def master_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa93d3d1cbe4d0323979532889f48d8df8fb97dc9e4c66c8019d95c5fca8d3cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterId", value)

    @builtins.property
    @jsii.member(jsii_name="invitationId")
    def invitation_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the invitation that is sent to the account designated as a member account.

        You can find the invitation ID by using the ListInvitation action of the  API.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-master.html#cfn-guardduty-master-invitationid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "invitationId"))

    @invitation_id.setter
    def invitation_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ef7c7e43502d62803ce46ca4bafe78d7cedc12ec46d8ad08ce50043251d151c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invitationId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-guardduty.CfnMasterProps",
    jsii_struct_bases=[],
    name_mapping={
        "detector_id": "detectorId",
        "master_id": "masterId",
        "invitation_id": "invitationId",
    },
)
class CfnMasterProps:
    def __init__(
        self,
        *,
        detector_id: builtins.str,
        master_id: builtins.str,
        invitation_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnMaster``.

        :param detector_id: The unique ID of the detector of the GuardDuty member account.
        :param master_id: The AWS account ID of the account designated as the administrator account.
        :param invitation_id: The ID of the invitation that is sent to the account designated as a member account. You can find the invitation ID by using the ListInvitation action of the API.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-master.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_guardduty as guardduty
            
            cfn_master_props = guardduty.CfnMasterProps(
                detector_id="detectorId",
                master_id="masterId",
            
                # the properties below are optional
                invitation_id="invitationId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39ec70907fefe6bbe9cfc2ec6afadb2691e055563fa205856a650323b2984d7)
            check_type(argname="argument detector_id", value=detector_id, expected_type=type_hints["detector_id"])
            check_type(argname="argument master_id", value=master_id, expected_type=type_hints["master_id"])
            check_type(argname="argument invitation_id", value=invitation_id, expected_type=type_hints["invitation_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "detector_id": detector_id,
            "master_id": master_id,
        }
        if invitation_id is not None:
            self._values["invitation_id"] = invitation_id

    @builtins.property
    def detector_id(self) -> builtins.str:
        '''The unique ID of the detector of the GuardDuty member account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-master.html#cfn-guardduty-master-detectorid
        '''
        result = self._values.get("detector_id")
        assert result is not None, "Required property 'detector_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def master_id(self) -> builtins.str:
        '''The AWS account ID of the account designated as the  administrator account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-master.html#cfn-guardduty-master-masterid
        '''
        result = self._values.get("master_id")
        assert result is not None, "Required property 'master_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def invitation_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the invitation that is sent to the account designated as a member account.

        You can find the invitation ID by using the ListInvitation action of the  API.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-master.html#cfn-guardduty-master-invitationid
        '''
        result = self._values.get("invitation_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMasterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnMember(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-guardduty.CfnMember",
):
    '''A CloudFormation ``AWS::GuardDuty::Member``.

    You can use the ``AWS::GuardDuty::Member`` resource to add an AWS account as a  member account to the current  administrator account. If the value of the ``Status`` property is not provided or is set to ``Created`` , a member account is created but not invited. If the value of the ``Status`` property is set to ``Invited`` , a member account is created and invited. An ``AWS::GuardDuty::Member`` resource must be created with the ``Status`` property set to ``Invited`` before the ``AWS::GuardDuty::Master`` resource can be created in a  member account.

    :cloudformationResource: AWS::GuardDuty::Member
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_guardduty as guardduty
        
        cfn_member = guardduty.CfnMember(self, "MyCfnMember",
            detector_id="detectorId",
            email="email",
            member_id="memberId",
        
            # the properties below are optional
            disable_email_notification=False,
            message="message",
            status="status"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        detector_id: builtins.str,
        email: builtins.str,
        member_id: builtins.str,
        disable_email_notification: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        message: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::GuardDuty::Member``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param detector_id: The ID of the detector associated with the service to add the member to.
        :param email: The email address associated with the member account.
        :param member_id: The AWS account ID of the account to designate as a member.
        :param disable_email_notification: Specifies whether or not to disable email notification for the member account that you invite.
        :param message: The invitation message that you want to send to the accounts that you're inviting to GuardDuty as members.
        :param status: You can use the ``Status`` property to update the status of the relationship between the member account and its administrator account. Valid values are ``Created`` and ``Invited`` when using an ``AWS::GuardDuty::Member`` resource. If the value for this property is not provided or set to ``Created`` , a member account is created but not invited. If the value of this property is set to ``Invited`` , a member account is created and invited.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86576183cd779e31397efc3214fe8619b3206152cbcd7c026b9dedc40bfcc9b5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMemberProps(
            detector_id=detector_id,
            email=email,
            member_id=member_id,
            disable_email_notification=disable_email_notification,
            message=message,
            status=status,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d880e12c1a84f8e8308edca29c3ced1f46aab4bc8502dbd17c013a23676568c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60b1a52a48c201281fd4afc7e7f1263c9e6f576cdb14f961073f41384ee990a5)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="detectorId")
    def detector_id(self) -> builtins.str:
        '''The ID of the detector associated with the  service to add the member to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-detectorid
        '''
        return typing.cast(builtins.str, jsii.get(self, "detectorId"))

    @detector_id.setter
    def detector_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8339f80f0e01951781a056b00357b1127d3179a9ce808e477216048ed4810b88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectorId", value)

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        '''The email address associated with the member account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-email
        '''
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b23703deb50847c5ad8c5c7d13671d84b7820f896d8e6ecc45c214d27f0a046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value)

    @builtins.property
    @jsii.member(jsii_name="memberId")
    def member_id(self) -> builtins.str:
        '''The AWS account ID of the account to designate as a member.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-memberid
        '''
        return typing.cast(builtins.str, jsii.get(self, "memberId"))

    @member_id.setter
    def member_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ae417ae702147e45c433a0bbd3374d639e4586fe102da50938df681598c794f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberId", value)

    @builtins.property
    @jsii.member(jsii_name="disableEmailNotification")
    def disable_email_notification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether or not to disable email notification for the member account that you invite.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-disableemailnotification
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "disableEmailNotification"))

    @disable_email_notification.setter
    def disable_email_notification(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1435af17a6ae9e18043c957bc1925777d18ba2f8265e2f60749aaede7a6a4d0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableEmailNotification", value)

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> typing.Optional[builtins.str]:
        '''The invitation message that you want to send to the accounts that you're inviting to GuardDuty as members.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-message
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "message"))

    @message.setter
    def message(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51da13f7ee4eec5a6c8ecbcaaa8575aae6e691cc4318712d2a093641b3495b85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        '''You can use the ``Status`` property to update the status of the relationship between the member account and its administrator account.

        Valid values are ``Created`` and ``Invited`` when using an ``AWS::GuardDuty::Member`` resource. If the value for this property is not provided or set to ``Created`` , a member account is created but not invited. If the value of this property is set to ``Invited`` , a member account is created and invited.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-status
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "status"))

    @status.setter
    def status(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d5411717d4d7d067d7966b837af85b6905300d0022d9b5059de6dbf307acbe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-guardduty.CfnMemberProps",
    jsii_struct_bases=[],
    name_mapping={
        "detector_id": "detectorId",
        "email": "email",
        "member_id": "memberId",
        "disable_email_notification": "disableEmailNotification",
        "message": "message",
        "status": "status",
    },
)
class CfnMemberProps:
    def __init__(
        self,
        *,
        detector_id: builtins.str,
        email: builtins.str,
        member_id: builtins.str,
        disable_email_notification: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        message: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnMember``.

        :param detector_id: The ID of the detector associated with the service to add the member to.
        :param email: The email address associated with the member account.
        :param member_id: The AWS account ID of the account to designate as a member.
        :param disable_email_notification: Specifies whether or not to disable email notification for the member account that you invite.
        :param message: The invitation message that you want to send to the accounts that you're inviting to GuardDuty as members.
        :param status: You can use the ``Status`` property to update the status of the relationship between the member account and its administrator account. Valid values are ``Created`` and ``Invited`` when using an ``AWS::GuardDuty::Member`` resource. If the value for this property is not provided or set to ``Created`` , a member account is created but not invited. If the value of this property is set to ``Invited`` , a member account is created and invited.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_guardduty as guardduty
            
            cfn_member_props = guardduty.CfnMemberProps(
                detector_id="detectorId",
                email="email",
                member_id="memberId",
            
                # the properties below are optional
                disable_email_notification=False,
                message="message",
                status="status"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64c2d3e45638693e505e7393b8becba39c645a858836d01265393aae9ec17b03)
            check_type(argname="argument detector_id", value=detector_id, expected_type=type_hints["detector_id"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument member_id", value=member_id, expected_type=type_hints["member_id"])
            check_type(argname="argument disable_email_notification", value=disable_email_notification, expected_type=type_hints["disable_email_notification"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "detector_id": detector_id,
            "email": email,
            "member_id": member_id,
        }
        if disable_email_notification is not None:
            self._values["disable_email_notification"] = disable_email_notification
        if message is not None:
            self._values["message"] = message
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def detector_id(self) -> builtins.str:
        '''The ID of the detector associated with the  service to add the member to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-detectorid
        '''
        result = self._values.get("detector_id")
        assert result is not None, "Required property 'detector_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def email(self) -> builtins.str:
        '''The email address associated with the member account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-email
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def member_id(self) -> builtins.str:
        '''The AWS account ID of the account to designate as a member.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-memberid
        '''
        result = self._values.get("member_id")
        assert result is not None, "Required property 'member_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disable_email_notification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether or not to disable email notification for the member account that you invite.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-disableemailnotification
        '''
        result = self._values.get("disable_email_notification")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''The invitation message that you want to send to the accounts that you're inviting to GuardDuty as members.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-message
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''You can use the ``Status`` property to update the status of the relationship between the member account and its administrator account.

        Valid values are ``Created`` and ``Invited`` when using an ``AWS::GuardDuty::Member`` resource. If the value for this property is not provided or set to ``Created`` , a member account is created but not invited. If the value of this property is set to ``Invited`` , a member account is created and invited.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMemberProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnThreatIntelSet(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-guardduty.CfnThreatIntelSet",
):
    '''A CloudFormation ``AWS::GuardDuty::ThreatIntelSet``.

    The ``AWS::GuardDuty::ThreatIntelSet`` resource specifies a new ``ThreatIntelSet`` . A ``ThreatIntelSet`` consists of known malicious IP addresses.  generates findings based on the ``ThreatIntelSet`` when it is activated.

    :cloudformationResource: AWS::GuardDuty::ThreatIntelSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_guardduty as guardduty
        
        cfn_threat_intel_set = guardduty.CfnThreatIntelSet(self, "MyCfnThreatIntelSet",
            activate=False,
            detector_id="detectorId",
            format="format",
            location="location",
        
            # the properties below are optional
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        activate: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        detector_id: builtins.str,
        format: builtins.str,
        location: builtins.str,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::GuardDuty::ThreatIntelSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param activate: A Boolean value that indicates whether GuardDuty is to start using the uploaded ThreatIntelSet.
        :param detector_id: The unique ID of the detector of the GuardDuty account that you want to create a threatIntelSet for.
        :param format: The format of the file that contains the ThreatIntelSet.
        :param location: The URI of the file that contains the ThreatIntelSet.
        :param name: A user-friendly ThreatIntelSet name displayed in all findings that are generated by activity that involves IP addresses included in this ThreatIntelSet.
        :param tags: The tags to be added to a new threat list resource. Each tag consists of a key and an optional value, both of which you define. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef313af210a091dae0e4f4d85fa5d62ab21735a19927293f05b681150a424b01)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnThreatIntelSetProps(
            activate=activate,
            detector_id=detector_id,
            format=format,
            location=location,
            name=name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c1e9cb47f723efed8e88101a2ccfe564fc6d0cbb3be28b31813b65f2298082b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae86d367fee12780822a2265854d029d36e9994d4cdad091a2ab3529b0d05dc9)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags to be added to a new threat list resource.

        Each tag consists of a key and an optional value, both of which you define.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="activate")
    def activate(
        self,
    ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
        '''A Boolean value that indicates whether GuardDuty is to start using the uploaded ThreatIntelSet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-activate
        '''
        return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "activate"))

    @activate.setter
    def activate(
        self,
        value: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d606c79bca1d7857cd56be66b3484b15a6ca8efaea29eacc16e837f496e8f4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activate", value)

    @builtins.property
    @jsii.member(jsii_name="detectorId")
    def detector_id(self) -> builtins.str:
        '''The unique ID of the detector of the GuardDuty account that you want to create a threatIntelSet for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-detectorid
        '''
        return typing.cast(builtins.str, jsii.get(self, "detectorId"))

    @detector_id.setter
    def detector_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e57d7ba7a08b74c2d8baae6f76eb04ffe741e9d814c3bd883e64750c2d6ce3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectorId", value)

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        '''The format of the file that contains the ThreatIntelSet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-format
        '''
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @format.setter
    def format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35bbaf65b8ce1eb696a22aacbb14ab3fa9a574bedb0d4ae2f4a07948481cde0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "format", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        '''The URI of the file that contains the ThreatIntelSet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-location
        '''
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3130088f67e644d2b188c6a05c5a5ab691b5e6d553a254391d5a903f98b0b612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''A user-friendly ThreatIntelSet name displayed in all findings that are generated by activity that involves IP addresses included in this ThreatIntelSet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea87a9d5df3b3b658012827e13619642532ab706ec16c6bccbe4a6d0f1f0f809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-guardduty.CfnThreatIntelSetProps",
    jsii_struct_bases=[],
    name_mapping={
        "activate": "activate",
        "detector_id": "detectorId",
        "format": "format",
        "location": "location",
        "name": "name",
        "tags": "tags",
    },
)
class CfnThreatIntelSetProps:
    def __init__(
        self,
        *,
        activate: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        detector_id: builtins.str,
        format: builtins.str,
        location: builtins.str,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnThreatIntelSet``.

        :param activate: A Boolean value that indicates whether GuardDuty is to start using the uploaded ThreatIntelSet.
        :param detector_id: The unique ID of the detector of the GuardDuty account that you want to create a threatIntelSet for.
        :param format: The format of the file that contains the ThreatIntelSet.
        :param location: The URI of the file that contains the ThreatIntelSet.
        :param name: A user-friendly ThreatIntelSet name displayed in all findings that are generated by activity that involves IP addresses included in this ThreatIntelSet.
        :param tags: The tags to be added to a new threat list resource. Each tag consists of a key and an optional value, both of which you define. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_guardduty as guardduty
            
            cfn_threat_intel_set_props = guardduty.CfnThreatIntelSetProps(
                activate=False,
                detector_id="detectorId",
                format="format",
                location="location",
            
                # the properties below are optional
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baa837379e547542b52edb27b5af7ca6535f16b6d99635086a83ba87179a8d69)
            check_type(argname="argument activate", value=activate, expected_type=type_hints["activate"])
            check_type(argname="argument detector_id", value=detector_id, expected_type=type_hints["detector_id"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "activate": activate,
            "detector_id": detector_id,
            "format": format,
            "location": location,
        }
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def activate(
        self,
    ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
        '''A Boolean value that indicates whether GuardDuty is to start using the uploaded ThreatIntelSet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-activate
        '''
        result = self._values.get("activate")
        assert result is not None, "Required property 'activate' is missing"
        return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def detector_id(self) -> builtins.str:
        '''The unique ID of the detector of the GuardDuty account that you want to create a threatIntelSet for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-detectorid
        '''
        result = self._values.get("detector_id")
        assert result is not None, "Required property 'detector_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def format(self) -> builtins.str:
        '''The format of the file that contains the ThreatIntelSet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-format
        '''
        result = self._values.get("format")
        assert result is not None, "Required property 'format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The URI of the file that contains the ThreatIntelSet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-location
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A user-friendly ThreatIntelSet name displayed in all findings that are generated by activity that involves IP addresses included in this ThreatIntelSet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags to be added to a new threat list resource.

        Each tag consists of a key and an optional value, both of which you define.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnThreatIntelSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDetector",
    "CfnDetectorProps",
    "CfnFilter",
    "CfnFilterProps",
    "CfnIPSet",
    "CfnIPSetProps",
    "CfnMaster",
    "CfnMasterProps",
    "CfnMember",
    "CfnMemberProps",
    "CfnThreatIntelSet",
    "CfnThreatIntelSetProps",
]

publication.publish()

def _typecheckingstub__77536b4016d0000a3ec5d841855bd35c8890cfe93b05262ce314dac200b4d14a(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    enable: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    data_sources: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetector.CFNDataSourceConfigurationsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    finding_publishing_frequency: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3b1797c98a169731fa785dbb77635d594307c5439542a7e72fc4b362404c56(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc3101308c71dfa647260f809ede76130fc43193badcdb96bd18b2327369262(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fffa26e75fe8ccc31f2d77af268fa458b1a87403bc811d9230e27f3946e8a63(
    value: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91510a99b1a7ef7cf8356fc2b0f342a928df97f39c261446ca410ac68440d54a(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDetector.CFNDataSourceConfigurationsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__592b51676ab440626d5c83a56d08469fb8472602e17553a1cff2f2308e4b2577(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899d70aec6c1966b8f837326e7dd896ba686a50324252598deb760b15865a3cc(
    *,
    kubernetes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetector.CFNKubernetesConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    malware_protection: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetector.CFNMalwareProtectionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_logs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetector.CFNS3LogsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f801c88c3face68f7b9ade62f2e213a61c43eed1fd35d54e6d529a19080fd1b(
    *,
    enable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b31a054708ad2712642d201fc2ab2fef8e1a456c7be69e0baaa26fa99ac05b3(
    *,
    audit_logs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetector.CFNKubernetesAuditLogsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f33ae807e3a1e855943086c0ea1273e3dcc13697d79b6cf383c45ad26669b4(
    *,
    scan_ec2_instance_with_findings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetector.CFNScanEc2InstanceWithFindingsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__130b6edd74713a4b38ec25eca790f24b43c231a8472ebfc84d9cb69693048f0d(
    *,
    enable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d903e1c3d6c92e4d4f84b4c82fdcfa8ebad493d4cd2d16944680874255d6a15(
    *,
    ebs_volumes: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__910648eac4ef910754ec562e293d771a83bbc84331cd78e3f5b0be01863b3df5(
    *,
    enable: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    data_sources: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetector.CFNDataSourceConfigurationsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    finding_publishing_frequency: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d59704e18b0438fbe06d1aa6d1337a08321e4ec1ec59a65399fef149c29c0c4b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    action: builtins.str,
    description: builtins.str,
    detector_id: builtins.str,
    finding_criteria: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFilter.FindingCriteriaProperty, typing.Dict[builtins.str, typing.Any]]],
    name: builtins.str,
    rank: jsii.Number,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02a31a137ef6f396e06fdc129a6afffe6888df2e369316b7dfa688974ded35f(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed63e15ef42c37e2721fa35aa591455f0a9b26655796dfed317adbd9774ad25(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9860df724d8812fbaac988873987339e7924d0cdb0bee5a3bfe36a07e511530b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7c5bcc380a3ba3477a6d89e689c1a85f7674be7f868ec8d09b8b65bc1f9529(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__598af88e12698c7eb203e95b500a02cc6affed65caf848b84719d25814b0ae74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da3d708938c37f389813647c1b9ee1421888ab05d928b6aa659d6065c92c2c9(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFilter.FindingCriteriaProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30de47e862af84c0151c97875a4777e753003af9fae2160c03341c6ae6ec92d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25265e33ad28230aafb3875758d9ef44cfca92021c8b2e4ca1033dca7e26ba49(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fc54e5cf7ac155ee7cfc65abf59eb2b3c0cbf3836e8f6d026adf79285b31f1(
    *,
    eq: typing.Optional[typing.Sequence[builtins.str]] = None,
    equal_to: typing.Optional[typing.Sequence[builtins.str]] = None,
    greater_than: typing.Optional[jsii.Number] = None,
    greater_than_or_equal: typing.Optional[jsii.Number] = None,
    gt: typing.Optional[jsii.Number] = None,
    gte: typing.Optional[jsii.Number] = None,
    less_than: typing.Optional[jsii.Number] = None,
    less_than_or_equal: typing.Optional[jsii.Number] = None,
    lt: typing.Optional[jsii.Number] = None,
    lte: typing.Optional[jsii.Number] = None,
    neq: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_equals: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c360e91d559446b5c6a87b00db6959dff4f0618cce047315001e88dab0e4a74(
    *,
    criterion: typing.Any = None,
    item_type: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFilter.ConditionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__576d2dc9e3d4e5d9678611cb75e1927147505427b11719347876376cc7a3938f(
    *,
    action: builtins.str,
    description: builtins.str,
    detector_id: builtins.str,
    finding_criteria: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFilter.FindingCriteriaProperty, typing.Dict[builtins.str, typing.Any]]],
    name: builtins.str,
    rank: jsii.Number,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c134d35f291b37ac2047795a554de0411cf347c953853187814e810bcbbd0ff(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    activate: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    detector_id: builtins.str,
    format: builtins.str,
    location: builtins.str,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f332f7fef9c05011c9733212834fe89df441c417428ed49fb840e328ad0197(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7365800f2af5d67a70011e0e351be07580e61655127e31ec2167da3cf0c398a4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f58e93d0f7732e7f62d41ec80bdc68b189e7c8c78ed8b7e4e40cfeaa09be331(
    value: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1fe4a135ecbf5dba641a09e0227041e2718d812c15ec254f5e3f5ec26b99285(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ffd1cd8b1da508c98aab6d97522699268ea5e85d470b124629b912aaa23c82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57225703288cbac1baa8bf095f82e841fb1c54fff68a20b45b66f39b102ce407(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3db771dea1fa969488c477dce62dc4a10d5498937a07148dc72e674dca84f99(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ec9911f0a94679b251896b402da0fea72a925976e842d59f3c6edf39ec67e31(
    *,
    activate: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    detector_id: builtins.str,
    format: builtins.str,
    location: builtins.str,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4193b2d1c1a68e693da4f5009d8303d28c0f45442262fe975cb7eb24ba22fd4(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    detector_id: builtins.str,
    master_id: builtins.str,
    invitation_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed8533b9c9e277cac8a57e94b0bbfc6889143a795ad3ea63eaa08ba6f3bacf6(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__215bc73a3c255ceea2df130b26e0928f92ef4936147e04e4fc11c3bf2c1dad1a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ab188fe442680b4c5a8413e9b30fc0efef5dc15e303f9b8196056f6c9a4911(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa93d3d1cbe4d0323979532889f48d8df8fb97dc9e4c66c8019d95c5fca8d3cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ef7c7e43502d62803ce46ca4bafe78d7cedc12ec46d8ad08ce50043251d151c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39ec70907fefe6bbe9cfc2ec6afadb2691e055563fa205856a650323b2984d7(
    *,
    detector_id: builtins.str,
    master_id: builtins.str,
    invitation_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86576183cd779e31397efc3214fe8619b3206152cbcd7c026b9dedc40bfcc9b5(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    detector_id: builtins.str,
    email: builtins.str,
    member_id: builtins.str,
    disable_email_notification: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    message: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d880e12c1a84f8e8308edca29c3ced1f46aab4bc8502dbd17c013a23676568c3(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b1a52a48c201281fd4afc7e7f1263c9e6f576cdb14f961073f41384ee990a5(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8339f80f0e01951781a056b00357b1127d3179a9ce808e477216048ed4810b88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b23703deb50847c5ad8c5c7d13671d84b7820f896d8e6ecc45c214d27f0a046(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae417ae702147e45c433a0bbd3374d639e4586fe102da50938df681598c794f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1435af17a6ae9e18043c957bc1925777d18ba2f8265e2f60749aaede7a6a4d0d(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51da13f7ee4eec5a6c8ecbcaaa8575aae6e691cc4318712d2a093641b3495b85(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d5411717d4d7d067d7966b837af85b6905300d0022d9b5059de6dbf307acbe0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c2d3e45638693e505e7393b8becba39c645a858836d01265393aae9ec17b03(
    *,
    detector_id: builtins.str,
    email: builtins.str,
    member_id: builtins.str,
    disable_email_notification: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    message: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef313af210a091dae0e4f4d85fa5d62ab21735a19927293f05b681150a424b01(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    activate: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    detector_id: builtins.str,
    format: builtins.str,
    location: builtins.str,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1e9cb47f723efed8e88101a2ccfe564fc6d0cbb3be28b31813b65f2298082b(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae86d367fee12780822a2265854d029d36e9994d4cdad091a2ab3529b0d05dc9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d606c79bca1d7857cd56be66b3484b15a6ca8efaea29eacc16e837f496e8f4d(
    value: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e57d7ba7a08b74c2d8baae6f76eb04ffe741e9d814c3bd883e64750c2d6ce3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35bbaf65b8ce1eb696a22aacbb14ab3fa9a574bedb0d4ae2f4a07948481cde0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3130088f67e644d2b188c6a05c5a5ab691b5e6d553a254391d5a903f98b0b612(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea87a9d5df3b3b658012827e13619642532ab706ec16c6bccbe4a6d0f1f0f809(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baa837379e547542b52edb27b5af7ca6535f16b6d99635086a83ba87179a8d69(
    *,
    activate: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    detector_id: builtins.str,
    format: builtins.str,
    location: builtins.str,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
