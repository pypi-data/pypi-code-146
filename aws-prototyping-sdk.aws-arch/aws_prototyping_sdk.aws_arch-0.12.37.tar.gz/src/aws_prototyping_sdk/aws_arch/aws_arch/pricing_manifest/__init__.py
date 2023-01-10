import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ..._jsii import *


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/aws-arch.aws_arch.PricingManifest.Service",
    jsii_struct_bases=[],
    name_mapping={
        "comparable_terms": "comparableTerms",
        "description": "description",
        "is_active": "isActive",
        "name": "name",
        "regions": "regions",
        "search_keywords": "searchKeywords",
        "service_code": "serviceCode",
        "service_definition_location": "serviceDefinitionLocation",
        "type": "type",
        "bulk_import_enabled": "bulkImportEnabled",
        "c2e": "c2e",
        "disable_configure": "disableConfigure",
        "disable_region_support": "disableRegionSupport",
        "has_data_transfer": "hasDataTransfer",
        "link_url": "linkUrl",
        "mvp_support": "mvpSupport",
        "parent_service_code": "parentServiceCode",
        "slug": "slug",
        "sub_type": "subType",
        "templates": "templates",
    },
)
class Service:
    def __init__(
        self,
        *,
        comparable_terms: typing.Sequence[builtins.str],
        description: builtins.str,
        is_active: builtins.str,
        name: builtins.str,
        regions: typing.Sequence[builtins.str],
        search_keywords: typing.Sequence[builtins.str],
        service_code: builtins.str,
        service_definition_location: builtins.str,
        type: builtins.str,
        bulk_import_enabled: typing.Optional[builtins.bool] = None,
        c2e: typing.Optional[builtins.bool] = None,
        disable_configure: typing.Optional[builtins.bool] = None,
        disable_region_support: typing.Optional[builtins.bool] = None,
        has_data_transfer: typing.Optional[builtins.bool] = None,
        link_url: typing.Optional[builtins.str] = None,
        mvp_support: typing.Optional[builtins.bool] = None,
        parent_service_code: typing.Optional[builtins.str] = None,
        slug: typing.Optional[builtins.str] = None,
        sub_type: typing.Optional[builtins.str] = None,
        templates: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Pricing manifest service definition.

        :param comparable_terms: (experimental) List of normalized comparable terms to consider equivalent to this service. Used for lookups and matching between systems.
        :param description: (experimental) Service descriptoin.
        :param is_active: 
        :param name: (experimental) Proper full name of the service.
        :param regions: (experimental) List of regions where the service is available.
        :param search_keywords: (experimental) List of keywords for searching services.
        :param service_code: (experimental) Unique code for service definition in pricing manifest.
        :param service_definition_location: 
        :param type: (experimental) Type of service definition.
        :param bulk_import_enabled: 
        :param c2e: 
        :param disable_configure: 
        :param disable_region_support: 
        :param has_data_transfer: 
        :param link_url: (experimental) Url link to related product documentation.
        :param mvp_support: 
        :param parent_service_code: (experimental) Service code of the parent for ``subService`` services.
        :param slug: (experimental) Unique slug for given resource.
        :param sub_type: (experimental) Sub type of service definition.
        :param templates: 

        :stability: experimental
        '''
        if __debug__:
            def stub(
                *,
                comparable_terms: typing.Sequence[builtins.str],
                description: builtins.str,
                is_active: builtins.str,
                name: builtins.str,
                regions: typing.Sequence[builtins.str],
                search_keywords: typing.Sequence[builtins.str],
                service_code: builtins.str,
                service_definition_location: builtins.str,
                type: builtins.str,
                bulk_import_enabled: typing.Optional[builtins.bool] = None,
                c2e: typing.Optional[builtins.bool] = None,
                disable_configure: typing.Optional[builtins.bool] = None,
                disable_region_support: typing.Optional[builtins.bool] = None,
                has_data_transfer: typing.Optional[builtins.bool] = None,
                link_url: typing.Optional[builtins.str] = None,
                mvp_support: typing.Optional[builtins.bool] = None,
                parent_service_code: typing.Optional[builtins.str] = None,
                slug: typing.Optional[builtins.str] = None,
                sub_type: typing.Optional[builtins.str] = None,
                templates: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument comparable_terms", value=comparable_terms, expected_type=type_hints["comparable_terms"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument is_active", value=is_active, expected_type=type_hints["is_active"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument search_keywords", value=search_keywords, expected_type=type_hints["search_keywords"])
            check_type(argname="argument service_code", value=service_code, expected_type=type_hints["service_code"])
            check_type(argname="argument service_definition_location", value=service_definition_location, expected_type=type_hints["service_definition_location"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument bulk_import_enabled", value=bulk_import_enabled, expected_type=type_hints["bulk_import_enabled"])
            check_type(argname="argument c2e", value=c2e, expected_type=type_hints["c2e"])
            check_type(argname="argument disable_configure", value=disable_configure, expected_type=type_hints["disable_configure"])
            check_type(argname="argument disable_region_support", value=disable_region_support, expected_type=type_hints["disable_region_support"])
            check_type(argname="argument has_data_transfer", value=has_data_transfer, expected_type=type_hints["has_data_transfer"])
            check_type(argname="argument link_url", value=link_url, expected_type=type_hints["link_url"])
            check_type(argname="argument mvp_support", value=mvp_support, expected_type=type_hints["mvp_support"])
            check_type(argname="argument parent_service_code", value=parent_service_code, expected_type=type_hints["parent_service_code"])
            check_type(argname="argument slug", value=slug, expected_type=type_hints["slug"])
            check_type(argname="argument sub_type", value=sub_type, expected_type=type_hints["sub_type"])
            check_type(argname="argument templates", value=templates, expected_type=type_hints["templates"])
        self._values: typing.Dict[str, typing.Any] = {
            "comparable_terms": comparable_terms,
            "description": description,
            "is_active": is_active,
            "name": name,
            "regions": regions,
            "search_keywords": search_keywords,
            "service_code": service_code,
            "service_definition_location": service_definition_location,
            "type": type,
        }
        if bulk_import_enabled is not None:
            self._values["bulk_import_enabled"] = bulk_import_enabled
        if c2e is not None:
            self._values["c2e"] = c2e
        if disable_configure is not None:
            self._values["disable_configure"] = disable_configure
        if disable_region_support is not None:
            self._values["disable_region_support"] = disable_region_support
        if has_data_transfer is not None:
            self._values["has_data_transfer"] = has_data_transfer
        if link_url is not None:
            self._values["link_url"] = link_url
        if mvp_support is not None:
            self._values["mvp_support"] = mvp_support
        if parent_service_code is not None:
            self._values["parent_service_code"] = parent_service_code
        if slug is not None:
            self._values["slug"] = slug
        if sub_type is not None:
            self._values["sub_type"] = sub_type
        if templates is not None:
            self._values["templates"] = templates

    @builtins.property
    def comparable_terms(self) -> typing.List[builtins.str]:
        '''(experimental) List of normalized comparable terms to consider equivalent to this service.

        Used for lookups and matching between systems.

        :stability: experimental
        :virtual: true
        '''
        result = self._values.get("comparable_terms")
        assert result is not None, "Required property 'comparable_terms' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def description(self) -> builtins.str:
        '''(experimental) Service descriptoin.

        :stability: experimental

        Example::

            "Amazon API Gateway is a fully managed service that..."
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_active(self) -> builtins.str:
        '''
        :stability: experimental

        Example::

            "true"
        '''
        result = self._values.get("is_active")
        assert result is not None, "Required property 'is_active' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) Proper full name of the service.

        :stability: experimental

        Example::

            "Amazon API Gateway"
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def regions(self) -> typing.List[builtins.str]:
        '''(experimental) List of regions where the service is available.

        :stability: experimental

        Example::

            ["us-gov-west-1","us-gov-east-1","af-south-1","ap-east-1","ap-south-1","ap-northeast-2","ap-northeast-3",...]
        '''
        result = self._values.get("regions")
        assert result is not None, "Required property 'regions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def search_keywords(self) -> typing.List[builtins.str]:
        '''(experimental) List of keywords for searching services.

        :stability: experimental

        Example::

            ["API", "api", "Rest", "websocket", "messages"]
        '''
        result = self._values.get("search_keywords")
        assert result is not None, "Required property 'search_keywords' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def service_code(self) -> builtins.str:
        '''(experimental) Unique code for service definition in pricing manifest.

        :stability: experimental

        Example::

            "amazonApiGateway"
        '''
        result = self._values.get("service_code")
        assert result is not None, "Required property 'service_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_definition_location(self) -> builtins.str:
        '''
        :stability: experimental

        Example::

            "https://d1qsjq9pzbk1k6.cloudfront.net/data/amazonApiGateway/en_US.json"
        '''
        result = self._values.get("service_definition_location")
        assert result is not None, "Required property 'service_definition_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''(experimental) Type of service definition.

        :stability: experimental

        Example::

            "AWSService"
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bulk_import_enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental

        Example::

            true
        '''
        result = self._values.get("bulk_import_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def c2e(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental

        Example::

            false
        '''
        result = self._values.get("c2e")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def disable_configure(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental

        Example::

            false
        '''
        result = self._values.get("disable_configure")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def disable_region_support(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental

        Example::

            false
        '''
        result = self._values.get("disable_region_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def has_data_transfer(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental

        Example::

            false
        '''
        result = self._values.get("has_data_transfer")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def link_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) Url link to related product documentation.

        :stability: experimental

        Example::

            "https://aws.amazon.com/api-gateway/"
        '''
        result = self._values.get("link_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mvp_support(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental

        Example::

            false@variationMVPSupport
        '''
        result = self._values.get("mvp_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def parent_service_code(self) -> typing.Optional[builtins.str]:
        '''(experimental) Service code of the parent for ``subService`` services.

        :stability: experimental
        :virtual: true
        '''
        result = self._values.get("parent_service_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slug(self) -> typing.Optional[builtins.str]:
        '''(experimental) Unique slug for given resource.

        :stability: experimental

        Example::

            "APIGateway"
        '''
        result = self._values.get("slug")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sub_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) Sub type of service definition.

        :stability: experimental

        Example::

            "subService"
        '''
        result = self._values.get("sub_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def templates(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental

        Example::

            ["chimeCostAnalysis", "chimeBusinessCallingAnalysis"]
        '''
        result = self._values.get("templates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Service(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Service",
]

publication.publish()
