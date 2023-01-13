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

import aws_cdk.aws_certificatemanager
import aws_cdk.aws_route53
import constructs


class Domain(metaclass=jsii.JSIIMeta, jsii_type="cdk-extensions.route53.Domain"):
    def __init__(
        self,
        zone: aws_cdk.aws_route53.IHostedZone,
        is_public: builtins.bool,
        *,
        certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate] = None,
        subdomain: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param zone: -
        :param is_public: -
        :param certificate: 
        :param subdomain: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Domain.__init__)
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
            check_type(argname="argument is_public", value=is_public, expected_type=type_hints["is_public"])
        options = DomainOptions(certificate=certificate, subdomain=subdomain)

        jsii.create(self.__class__, self, [zone, is_public, options])

    @jsii.member(jsii_name="visit")
    def visit(self, node: constructs.IConstruct) -> None:
        '''
        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Domain.visit)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))

    @builtins.property
    @jsii.member(jsii_name="fqdn")
    def fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqdn"))

    @builtins.property
    @jsii.member(jsii_name="isPublic")
    def is_public(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "isPublic"))

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> aws_cdk.aws_route53.IHostedZone:
        return typing.cast(aws_cdk.aws_route53.IHostedZone, jsii.get(self, "zone"))

    @builtins.property
    @jsii.member(jsii_name="zoneName")
    def zone_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneName"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(
        self,
    ) -> typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]:
        return typing.cast(typing.Optional[aws_cdk.aws_certificatemanager.ICertificate], jsii.get(self, "certificate"))

    @builtins.property
    @jsii.member(jsii_name="subdomain")
    def subdomain(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdomain"))


@jsii.enum(jsii_type="cdk-extensions.route53.DomainDiscovery")
class DomainDiscovery(enum.Enum):
    ALL = "ALL"
    NONE = "NONE"
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"


class DomainManager(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.route53.DomainManager",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="isDnsResolvable")
    @builtins.classmethod
    def is_dns_resolvable(cls, node: constructs.IConstruct) -> builtins.bool:
        '''
        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DomainManager.is_dns_resolvable)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isDnsResolvable", [node]))


@jsii.data_type(
    jsii_type="cdk-extensions.route53.DomainOptions",
    jsii_struct_bases=[],
    name_mapping={"certificate": "certificate", "subdomain": "subdomain"},
)
class DomainOptions:
    def __init__(
        self,
        *,
        certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate] = None,
        subdomain: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param certificate: 
        :param subdomain: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DomainOptions.__init__)
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument subdomain", value=subdomain, expected_type=type_hints["subdomain"])
        self._values: typing.Dict[str, typing.Any] = {}
        if certificate is not None:
            self._values["certificate"] = certificate
        if subdomain is not None:
            self._values["subdomain"] = subdomain

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]:
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[aws_cdk.aws_certificatemanager.ICertificate], result)

    @builtins.property
    def subdomain(self) -> typing.Optional[builtins.str]:
        result = self._values.get("subdomain")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Domains(metaclass=jsii.JSIIMeta, jsii_type="cdk-extensions.route53.Domains"):
    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, scope: constructs.IConstruct) -> "Domains":
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Domains.of)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("Domains", jsii.sinvoke(cls, "of", [scope]))

    @jsii.member(jsii_name="add")
    def add(
        self,
        hosted_zone: aws_cdk.aws_route53.IHostedZone,
        is_public: builtins.bool,
        *,
        certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate] = None,
        subdomain: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hosted_zone: -
        :param is_public: -
        :param certificate: 
        :param subdomain: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Domains.add)
            check_type(argname="argument hosted_zone", value=hosted_zone, expected_type=type_hints["hosted_zone"])
            check_type(argname="argument is_public", value=is_public, expected_type=type_hints["is_public"])
        options = DomainOptions(certificate=certificate, subdomain=subdomain)

        return typing.cast(None, jsii.invoke(self, "add", [hosted_zone, is_public, options]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ROOT")
    def ROOT(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "ROOT"))


@jsii.interface(jsii_type="cdk-extensions.route53.IDnsResolvable")
class IDnsResolvable(constructs.IConstruct, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="domainDiscovery")
    def domain_discovery(self) -> DomainDiscovery:
        ...

    @jsii.member(jsii_name="registerDomain")
    def register_domain(self, domain: Domain) -> None:
        '''
        :param domain: -
        '''
        ...


class _IDnsResolvableProxy(
    jsii.proxy_for(constructs.IConstruct), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.route53.IDnsResolvable"

    @builtins.property
    @jsii.member(jsii_name="domainDiscovery")
    def domain_discovery(self) -> DomainDiscovery:
        return typing.cast(DomainDiscovery, jsii.get(self, "domainDiscovery"))

    @jsii.member(jsii_name="registerDomain")
    def register_domain(self, domain: Domain) -> None:
        '''
        :param domain: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IDnsResolvable.register_domain)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
        return typing.cast(None, jsii.invoke(self, "registerDomain", [domain]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDnsResolvable).__jsii_proxy_class__ = lambda : _IDnsResolvableProxy


__all__ = [
    "Domain",
    "DomainDiscovery",
    "DomainManager",
    "DomainOptions",
    "Domains",
    "IDnsResolvable",
]

publication.publish()
