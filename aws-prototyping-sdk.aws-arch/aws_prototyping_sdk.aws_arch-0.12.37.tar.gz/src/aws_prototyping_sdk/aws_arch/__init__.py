'''
## aws-arch (AWS Architecture)

Library to provide metadata for AWS Services and AWS Resources.

This package generates mappings between [@aws-cdk/cfnspec](https://github.com/aws/aws-cdk/blob/main/packages/%40aws-cdk/cfnspec) and [AWS Architecture Icons](https://aws.amazon.com/architecture/icons/), and resolves resource metadata between these systems to infer a normalized definition of an `AwsService` and `AwsResource`.

The primary aim of this package is to provide a consistent mechanism for other libraries to retrieve naming and assets associated with CloudFormation resources, and by extension CDK resources.

### Get Started

```sh
yarn add '@aws-prototyping-sdk/aws-arch'
```

```python
import { AwsArchitecture } from "@aws-prototyping-sdk/aws-arch";

const s3Bucket = AwsArchitecture.getResource("AWS::S3::Bucket");
const s3Service = AwsArchitecture.getService(s3Bucket.service);

console.log(s3Bucket);
console.log(s3Service);
```

```js
// => console.log(s3Bucket);
{
	"name": "Amazon Simple Storage Service Bucket",
	"cfnType": "AWS::S3::Bucket",
	"awsAssetName": "Amazon-Simple-Storage-Service_Bucket",
	"awsAssetIcon": "resources/Amazon-Simple-Storage-Service_Bucket.png",
	"service": "S3"
}

// => console.log(s3Service);
{
	"provider": "AWS",
	"name": "Amazon Simple Storage Service",
	"cfnName": "S3",
	"awsAssetIcon": "services/Amazon-Simple-Storage-Service.png",
	"awsAssetName": "Amazon-Simple-Storage-Service"
}
```

### Aws Achritecture Icons

Retrieve **category**, **service**, and **resource** [AWS Architecture Icons](https://aws.amazon.com/architecture/icons/).

> Icon methods return relative asset key paths, as most frameworks have the concept of a base path (imagepaths). Use `AwsArchitecture.resolveAssetPath(...)` to get absolute path.

#### Retrieve icon based on CloudFormation Resource Type

**Resource Icon**

```python
const s3Bucket = AwsArchitecture.getResource("AWS::S3::Bucket");

const s3BucketPng = s3Bucket.icon("png"); // => "storage/s3/bucket.png"
const s3BucketSvg = s3Bucket.icon("svg"); // => "storage/s3/bucket.svg"

// Resolve absolute path for icons
AwsArchitecture.resolveAssetPath(s3BucketPng); // => /User/example/.../node_modules/@aws-prototyping-sdk/aws-arc/assets/storage/s3/bucket.png
```

**Service Icon**

```python
const s3Service = AwsArchitecture.getResource("AWS::S3::Bucket").service;
// equivalent to: `AwsArchitecture.getService("S3")`

const s3ServicePng = s3Service.icon("png"); // => "storage/s3/service_icon.png"
const s3ServiceSvg = s3Service.icon("svg"); // => "storage/s3/service_icon.svg"

// Resolve absolute path for icons
AwsArchitecture.resolveAssetPath(s3ServicePng); // => /User/example/.../node_modules/@aws-prototyping-sdk/aws-arc/assets/storage/s3/service_icon.png
```

**Category Icon**

```python
const storageCategory =
  AwsArchitecture.getResource("AWS::S3::Bucket").service.category;
// equivalent to: `AwsArchitecture.getCategory("storage")`

const storageCategoryPng = storageCategory.icon("png"); // => "storage/category_icon.png"
const storageCategorySvg = storageCategory.icon("svg"); // => "storage/category_icon.svg"

// Resolve absolute path for icons
AwsArchitecture.resolveAssetPath(storageCategoryPng); // => /User/example/.../node_modules/@aws-prototyping-sdk/aws-arc/assets/storage/category_icon.png
```

### Development

This package auto-generates many types and asset files from external sources,
which are then auto mapped based on common patterns and explict mappings for edge-cases.

The auto-generation is handled by `/scripts` files which can be run via corresponding
package scripts (eg: `npx projen generate:assets` => `/scripts/generate-assets.ts`).

There is an implicit sequential order the scripts must be called in due to dependencies,
which is handled by `npx projen generate` script. The `generate` script is also invoked
prior to `npx projen build` if generated asset directory does not exist.

For local development of packages that depend on `aws-arch` package, you will need to
call `npx projen generate && npx projen compile` (or `npx projen build`) prior to locally
importing this package.

To update [AWS Architecture Icons](https://aws.amazon.com/architecture/icons/), change the url in [ASSET_PACKAGE_ZIP_URL](packages/aws-arch/scripts/generate-assets.ts).
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

from .aws_arch import (
    DrawioAws4ParentShapes as _DrawioAws4ParentShapes_a140e9a5,
    DrawioAwsResourceIconStyleBase as _DrawioAwsResourceIconStyleBase_9b406fcd,
)
from .aws_arch.drawio_spec.aws4 import ShapeNames as _ShapeNames_b18b2fa9
from .aws_arch.pricing_manifest import Service as _Service_4bf9f4e8


class AwsArchitecture(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/aws-arch.AwsArchitecture",
):
    '''(experimental) AwsArchitecture provides an interface for retrieving the inferred normalization between `@aws-cdk/cfnspec <https://github.com/aws/aws-cdk/blob/main/packages/%40aws-cdk/cfnspec>`_ and `AWS Architecture Icons <https://aws.amazon.com/architecture/icons/>`_ systems for all CloudFormation "services" and "resources".

    :stability: experimental
    '''

    @jsii.member(jsii_name="formatAssetPath")
    @builtins.classmethod
    def format_asset_path(
        cls,
        qualified_asset_key: builtins.str,
        format: builtins.str,
        theme: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''(experimental) Gets formatted asset path including extension and theme.

        :param qualified_asset_key: The qualified asset key (eg: compute/ec2/service_icon, storage/s3/bucket).
        :param format: The format to return (eg: png, svg).
        :param theme: - (Optional) The theme to use, if not specific or now matching asset for the them, the default theme is used.

        :return: Relative asset file path

        :stability: experimental
        '''
        if __debug__:
            def stub(
                qualified_asset_key: builtins.str,
                format: builtins.str,
                theme: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument qualified_asset_key", value=qualified_asset_key, expected_type=type_hints["qualified_asset_key"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "formatAssetPath", [qualified_asset_key, format, theme]))

    @jsii.member(jsii_name="getCategory")
    @builtins.classmethod
    def get_category(cls, category: builtins.str) -> "AwsCategory":
        '''(experimental) Get specific category based on id.

        :param category: -

        :see: {@link AwsCategory.getCategory}
        :stability: experimental
        '''
        if __debug__:
            def stub(category: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
        return typing.cast("AwsCategory", jsii.sinvoke(cls, "getCategory", [category]))

    @jsii.member(jsii_name="getInstanceTypeIcon")
    @builtins.classmethod
    def get_instance_type_icon(
        cls,
        instance_type: builtins.str,
        format: typing.Optional[builtins.str] = None,
        theme: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''(experimental) Get icon for EC2 instance type.

        :param instance_type: - The {@link AwsAsset.InstanceType} to get icon for.
        :param format: - The format of icon.
        :param theme: - Optional theme.

        :return: Returns relative asset icon path

        :stability: experimental
        '''
        if __debug__:
            def stub(
                instance_type: builtins.str,
                format: typing.Optional[builtins.str] = None,
                theme: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getInstanceTypeIcon", [instance_type, format, theme]))

    @jsii.member(jsii_name="getRdsInstanceTypeIcon")
    @builtins.classmethod
    def get_rds_instance_type_icon(
        cls,
        instance_type: builtins.str,
        format: typing.Optional[builtins.str] = None,
        theme: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''(experimental) Get icon for RDS instance type.

        :param instance_type: - The {@link AwsAsset.RdsInstanceType} to get icon for.
        :param format: - The format of icon.
        :param theme: - Optional theme.

        :return: Returns relative asset icon path

        :stability: experimental
        '''
        if __debug__:
            def stub(
                instance_type: builtins.str,
                format: typing.Optional[builtins.str] = None,
                theme: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getRdsInstanceTypeIcon", [instance_type, format, theme]))

    @jsii.member(jsii_name="getResource")
    @builtins.classmethod
    def get_resource(cls, cfn_type: builtins.str) -> "AwsResource":
        '''(experimental) Get resource based on Cfn Resource Type (eg: AWS::S3::Bucket).

        :param cfn_type: -

        :see: {@link AwsResource.getResource}
        :stability: experimental
        '''
        if __debug__:
            def stub(cfn_type: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument cfn_type", value=cfn_type, expected_type=type_hints["cfn_type"])
        return typing.cast("AwsResource", jsii.sinvoke(cls, "getResource", [cfn_type]))

    @jsii.member(jsii_name="getService")
    @builtins.classmethod
    def get_service(cls, identifier: builtins.str) -> "AwsService":
        '''(experimental) Get specific service based on identifier (eg: S3, AWS::S3, AWS::S3::Bucket).

        :param identifier: -

        :see: {@link AwsSerfice.getService}
        :stability: experimental
        '''
        if __debug__:
            def stub(identifier: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
        return typing.cast("AwsService", jsii.sinvoke(cls, "getService", [identifier]))

    @jsii.member(jsii_name="parseAssetPath")
    @builtins.classmethod
    def parse_asset_path(cls, asset_path: builtins.str) -> "ParsedAssetKey":
        '''(experimental) Parse assets path into part descriptor.

        :param asset_path: - Absolute or relative asset file path to parse.

        :stability: experimental
        '''
        if __debug__:
            def stub(asset_path: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument asset_path", value=asset_path, expected_type=type_hints["asset_path"])
        return typing.cast("ParsedAssetKey", jsii.sinvoke(cls, "parseAssetPath", [asset_path]))

    @jsii.member(jsii_name="resolveAssetPath")
    @builtins.classmethod
    def resolve_asset_path(cls, asset_path: builtins.str) -> builtins.str:
        '''(experimental) Resolve relative asset path to absolute asset path.

        :param asset_path: - The relative asset path to resolve.

        :return: Absolute asset path

        :stability: experimental
        :throws: Error if asset path is not relative
        '''
        if __debug__:
            def stub(asset_path: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument asset_path", value=asset_path, expected_type=type_hints["asset_path"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "resolveAssetPath", [asset_path]))

    @jsii.member(jsii_name="resolveAssetSvgDataUrl")
    @builtins.classmethod
    def resolve_asset_svg_data_url(cls, svg_asset_path: builtins.str) -> builtins.str:
        '''(experimental) Resolve relative asset path as SVG `Data URL <https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs>`_.

        ``data:image/svg+xml;base64,...``

        :param svg_asset_path: - The relative path of svg asset to resolve.

        :return: SVG `Data URL <https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs>`_

        :stability: experimental
        :throws: Error if path is not svg
        '''
        if __debug__:
            def stub(svg_asset_path: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument svg_asset_path", value=svg_asset_path, expected_type=type_hints["svg_asset_path"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "resolveAssetSvgDataUrl", [svg_asset_path]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="assetDirectory")
    def asset_directory(cls) -> builtins.str:
        '''(experimental) The absolute directory where `AWS Architecture Icons <https://aws.amazon.com/architecture/icons/>`_ are stored and retrieved.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "assetDirectory"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="categories")
    def categories(cls) -> typing.Mapping[builtins.str, "AwsCategory"]:
        '''(experimental) Get all categories.

        :see: {@link AwsCategory.categories}
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, "AwsCategory"], jsii.sget(cls, "categories"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="resources")
    def resources(cls) -> typing.Mapping[builtins.str, "AwsResource"]:
        '''(experimental) Get all resources.

        :see: {@link AwsResource.resources}
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, "AwsResource"], jsii.sget(cls, "resources"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="services")
    def services(cls) -> typing.Mapping[builtins.str, "AwsService"]:
        '''(experimental) Get all services.

        :see: {@link AwsService.services}
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, "AwsService"], jsii.sget(cls, "services"))


class AwsCategory(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/aws-arch.AwsCategory",
):
    '''(experimental) AwsCategory class provides an interface for normalizing category metadata between mapped systems.

    :stability: experimental
    '''

    @jsii.member(jsii_name="getCategory")
    @builtins.classmethod
    def get_category(cls, id: builtins.str) -> "AwsCategory":
        '''(experimental) Get {@link AwsCategory} based on {@link AwsCategoryId}.

        :param id: The id of the category to retrieve.

        :return: Returns the category with the id

        :stability: experimental
        '''
        if __debug__:
            def stub(id: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("AwsCategory", jsii.sinvoke(cls, "getCategory", [id]))

    @jsii.member(jsii_name="categoryServices")
    def category_services(self) -> typing.List["AwsService"]:
        '''(experimental) Gets a list of all services within this category.

        :stability: experimental
        '''
        return typing.cast(typing.List["AwsService"], jsii.invoke(self, "categoryServices", []))

    @jsii.member(jsii_name="icon")
    def icon(
        self,
        format: builtins.str,
        theme: typing.Optional[builtins.str] = None,
    ) -> typing.Optional[builtins.str]:
        '''(experimental) Retrieves a well-formatted relative path to the icon for this given category in the specified format.

        :param format: -
        :param theme: -

        :stability: experimental
        '''
        if __debug__:
            def stub(
                format: builtins.str,
                theme: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "icon", [format, theme]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="categories")
    def categories(cls) -> typing.Mapping[builtins.str, "AwsCategory"]:
        '''(experimental) Get record of all categories keyed by category id.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, "AwsCategory"], jsii.sget(cls, "categories"))

    @builtins.property
    @jsii.member(jsii_name="fillColor")
    def fill_color(self) -> builtins.str:
        '''(experimental) Fill color for the category.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fillColor"))

    @builtins.property
    @jsii.member(jsii_name="fontColor")
    def font_color(self) -> builtins.str:
        '''(experimental) Font color for the category.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fontColor"))

    @builtins.property
    @jsii.member(jsii_name="gradientColor")
    def gradient_color(self) -> builtins.str:
        '''(experimental) Gradien color for the category.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "gradientColor"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) The unique id of the category.

        :stability: experimental

        Example::

            "security_identity_compliance"
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The proper name of the category.

        :stability: experimental

        Example::

            "Security, Identity, & Compliance"
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="variants")
    def variants(self) -> typing.List[builtins.str]:
        '''(experimental) Alternative names used to identity this category.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "variants"))

    @builtins.property
    @jsii.member(jsii_name="drawioStyles")
    def drawio_styles(self) -> typing.Optional["AwsCategoryDrawioStyles"]:
        '''(experimental) Drawio style definition for this category.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["AwsCategoryDrawioStyles"], jsii.get(self, "drawioStyles"))


class AwsCategoryDrawioStyles(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/aws-arch.AwsCategoryDrawioStyles",
):
    '''(experimental) AwsCategoryDrawioStyles is a utility class for constructing drawio shape styles for services and resources.

    :stability: experimental
    '''

    def __init__(
        self,
        category_shape: _ShapeNames_b18b2fa9,
        *,
        fill_color: builtins.str,
        font_color: builtins.str,
        gradient_color: builtins.str,
        align: builtins.str,
        aspect: builtins.str,
        dashed: jsii.Number,
        font_size: jsii.Number,
        font_style: typing.Union[builtins.str, jsii.Number],
        gradient_direction: builtins.str,
        html: jsii.Number,
        outline_connect: jsii.Number,
        stroke_color: builtins.str,
        vertical_align: builtins.str,
        vertical_label_position: builtins.str,
        pointer_event: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param category_shape: -
        :param fill_color: 
        :param font_color: 
        :param gradient_color: 
        :param align: 
        :param aspect: 
        :param dashed: 
        :param font_size: 
        :param font_style: 
        :param gradient_direction: 
        :param html: 
        :param outline_connect: 
        :param stroke_color: 
        :param vertical_align: 
        :param vertical_label_position: 
        :param pointer_event: 

        :stability: experimental
        '''
        if __debug__:
            def stub(
                category_shape: _ShapeNames_b18b2fa9,
                *,
                fill_color: builtins.str,
                font_color: builtins.str,
                gradient_color: builtins.str,
                align: builtins.str,
                aspect: builtins.str,
                dashed: jsii.Number,
                font_size: jsii.Number,
                font_style: typing.Union[builtins.str, jsii.Number],
                gradient_direction: builtins.str,
                html: jsii.Number,
                outline_connect: jsii.Number,
                stroke_color: builtins.str,
                vertical_align: builtins.str,
                vertical_label_position: builtins.str,
                pointer_event: typing.Optional[jsii.Number] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument category_shape", value=category_shape, expected_type=type_hints["category_shape"])
        base = _DrawioAwsResourceIconStyleBase_9b406fcd(
            fill_color=fill_color,
            font_color=font_color,
            gradient_color=gradient_color,
            align=align,
            aspect=aspect,
            dashed=dashed,
            font_size=font_size,
            font_style=font_style,
            gradient_direction=gradient_direction,
            html=html,
            outline_connect=outline_connect,
            stroke_color=stroke_color,
            vertical_align=vertical_align,
            vertical_label_position=vertical_label_position,
            pointer_event=pointer_event,
        )

        jsii.create(self.__class__, self, [category_shape, base])

    @jsii.member(jsii_name="getResourceStyle")
    def get_resource_style(
        self,
        resource_shape: _ShapeNames_b18b2fa9,
    ) -> "AwsDrawioShapeStyle":
        '''(experimental) Gets the drawio style for a resource based on the category style.

        :param resource_shape: The resource shape to style based on category.

        :return: The style drawio style definition for the resource based on category style.

        :stability: experimental
        '''
        if __debug__:
            def stub(resource_shape: _ShapeNames_b18b2fa9) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument resource_shape", value=resource_shape, expected_type=type_hints["resource_shape"])
        return typing.cast("AwsDrawioShapeStyle", jsii.invoke(self, "getResourceStyle", [resource_shape]))

    @jsii.member(jsii_name="getServiceStyle")
    def get_service_style(
        self,
        service_shape: _ShapeNames_b18b2fa9,
    ) -> "AwsDrawioResourceIconStyle":
        '''(experimental) Gets the drawio style for a service based on the category style.

        :param service_shape: The service shape to style based on category.

        :return: The style drawio style definition for the resource based on category style.

        :stability: experimental
        '''
        if __debug__:
            def stub(service_shape: _ShapeNames_b18b2fa9) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument service_shape", value=service_shape, expected_type=type_hints["service_shape"])
        return typing.cast("AwsDrawioResourceIconStyle", jsii.invoke(self, "getServiceStyle", [service_shape]))

    @builtins.property
    @jsii.member(jsii_name="base")
    def base(self) -> _DrawioAwsResourceIconStyleBase_9b406fcd:
        '''
        :stability: experimental
        '''
        return typing.cast(_DrawioAwsResourceIconStyleBase_9b406fcd, jsii.get(self, "base"))

    @builtins.property
    @jsii.member(jsii_name="categoryShape")
    def category_shape(self) -> _ShapeNames_b18b2fa9:
        '''
        :stability: experimental
        '''
        return typing.cast(_ShapeNames_b18b2fa9, jsii.get(self, "categoryShape"))

    @builtins.property
    @jsii.member(jsii_name="categoryStyle")
    def category_style(self) -> "AwsDrawioResourceIconStyle":
        '''(experimental) Get the drawio style for this category.

        :stability: experimental
        '''
        return typing.cast("AwsDrawioResourceIconStyle", jsii.get(self, "categoryStyle"))


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/aws-arch.AwsDrawioResourceIconStyle",
    jsii_struct_bases=[_DrawioAwsResourceIconStyleBase_9b406fcd],
    name_mapping={
        "align": "align",
        "aspect": "aspect",
        "dashed": "dashed",
        "font_size": "fontSize",
        "font_style": "fontStyle",
        "gradient_direction": "gradientDirection",
        "html": "html",
        "outline_connect": "outlineConnect",
        "stroke_color": "strokeColor",
        "vertical_align": "verticalAlign",
        "vertical_label_position": "verticalLabelPosition",
        "pointer_event": "pointerEvent",
        "fill_color": "fillColor",
        "font_color": "fontColor",
        "gradient_color": "gradientColor",
        "res_icon": "resIcon",
        "shape": "shape",
    },
)
class AwsDrawioResourceIconStyle(_DrawioAwsResourceIconStyleBase_9b406fcd):
    def __init__(
        self,
        *,
        align: builtins.str,
        aspect: builtins.str,
        dashed: jsii.Number,
        font_size: jsii.Number,
        font_style: typing.Union[builtins.str, jsii.Number],
        gradient_direction: builtins.str,
        html: jsii.Number,
        outline_connect: jsii.Number,
        stroke_color: builtins.str,
        vertical_align: builtins.str,
        vertical_label_position: builtins.str,
        pointer_event: typing.Optional[jsii.Number] = None,
        fill_color: builtins.str,
        font_color: builtins.str,
        gradient_color: builtins.str,
        res_icon: _ShapeNames_b18b2fa9,
        shape: _DrawioAws4ParentShapes_a140e9a5,
    ) -> None:
        '''(experimental) Drawio resource icon style definition for AWS Resources.

        :param align: 
        :param aspect: 
        :param dashed: 
        :param font_size: 
        :param font_style: 
        :param gradient_direction: 
        :param html: 
        :param outline_connect: 
        :param stroke_color: 
        :param vertical_align: 
        :param vertical_label_position: 
        :param pointer_event: 
        :param fill_color: 
        :param font_color: 
        :param gradient_color: 
        :param res_icon: 
        :param shape: 

        :stability: experimental
        '''
        if __debug__:
            def stub(
                *,
                align: builtins.str,
                aspect: builtins.str,
                dashed: jsii.Number,
                font_size: jsii.Number,
                font_style: typing.Union[builtins.str, jsii.Number],
                gradient_direction: builtins.str,
                html: jsii.Number,
                outline_connect: jsii.Number,
                stroke_color: builtins.str,
                vertical_align: builtins.str,
                vertical_label_position: builtins.str,
                pointer_event: typing.Optional[jsii.Number] = None,
                fill_color: builtins.str,
                font_color: builtins.str,
                gradient_color: builtins.str,
                res_icon: _ShapeNames_b18b2fa9,
                shape: _DrawioAws4ParentShapes_a140e9a5,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument align", value=align, expected_type=type_hints["align"])
            check_type(argname="argument aspect", value=aspect, expected_type=type_hints["aspect"])
            check_type(argname="argument dashed", value=dashed, expected_type=type_hints["dashed"])
            check_type(argname="argument font_size", value=font_size, expected_type=type_hints["font_size"])
            check_type(argname="argument font_style", value=font_style, expected_type=type_hints["font_style"])
            check_type(argname="argument gradient_direction", value=gradient_direction, expected_type=type_hints["gradient_direction"])
            check_type(argname="argument html", value=html, expected_type=type_hints["html"])
            check_type(argname="argument outline_connect", value=outline_connect, expected_type=type_hints["outline_connect"])
            check_type(argname="argument stroke_color", value=stroke_color, expected_type=type_hints["stroke_color"])
            check_type(argname="argument vertical_align", value=vertical_align, expected_type=type_hints["vertical_align"])
            check_type(argname="argument vertical_label_position", value=vertical_label_position, expected_type=type_hints["vertical_label_position"])
            check_type(argname="argument pointer_event", value=pointer_event, expected_type=type_hints["pointer_event"])
            check_type(argname="argument fill_color", value=fill_color, expected_type=type_hints["fill_color"])
            check_type(argname="argument font_color", value=font_color, expected_type=type_hints["font_color"])
            check_type(argname="argument gradient_color", value=gradient_color, expected_type=type_hints["gradient_color"])
            check_type(argname="argument res_icon", value=res_icon, expected_type=type_hints["res_icon"])
            check_type(argname="argument shape", value=shape, expected_type=type_hints["shape"])
        self._values: typing.Dict[str, typing.Any] = {
            "align": align,
            "aspect": aspect,
            "dashed": dashed,
            "font_size": font_size,
            "font_style": font_style,
            "gradient_direction": gradient_direction,
            "html": html,
            "outline_connect": outline_connect,
            "stroke_color": stroke_color,
            "vertical_align": vertical_align,
            "vertical_label_position": vertical_label_position,
            "fill_color": fill_color,
            "font_color": font_color,
            "gradient_color": gradient_color,
            "res_icon": res_icon,
            "shape": shape,
        }
        if pointer_event is not None:
            self._values["pointer_event"] = pointer_event

    @builtins.property
    def align(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("align")
        assert result is not None, "Required property 'align' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aspect(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("aspect")
        assert result is not None, "Required property 'aspect' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dashed(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("dashed")
        assert result is not None, "Required property 'dashed' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def font_size(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("font_size")
        assert result is not None, "Required property 'font_size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def font_style(self) -> typing.Union[builtins.str, jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("font_style")
        assert result is not None, "Required property 'font_style' is missing"
        return typing.cast(typing.Union[builtins.str, jsii.Number], result)

    @builtins.property
    def gradient_direction(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("gradient_direction")
        assert result is not None, "Required property 'gradient_direction' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def html(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("html")
        assert result is not None, "Required property 'html' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def outline_connect(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("outline_connect")
        assert result is not None, "Required property 'outline_connect' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def stroke_color(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("stroke_color")
        assert result is not None, "Required property 'stroke_color' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vertical_align(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("vertical_align")
        assert result is not None, "Required property 'vertical_align' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vertical_label_position(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("vertical_label_position")
        assert result is not None, "Required property 'vertical_label_position' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pointer_event(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("pointer_event")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fill_color(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("fill_color")
        assert result is not None, "Required property 'fill_color' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def font_color(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("font_color")
        assert result is not None, "Required property 'font_color' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gradient_color(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("gradient_color")
        assert result is not None, "Required property 'gradient_color' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def res_icon(self) -> _ShapeNames_b18b2fa9:
        '''
        :stability: experimental
        '''
        result = self._values.get("res_icon")
        assert result is not None, "Required property 'res_icon' is missing"
        return typing.cast(_ShapeNames_b18b2fa9, result)

    @builtins.property
    def shape(self) -> _DrawioAws4ParentShapes_a140e9a5:
        '''
        :stability: experimental
        '''
        result = self._values.get("shape")
        assert result is not None, "Required property 'shape' is missing"
        return typing.cast(_DrawioAws4ParentShapes_a140e9a5, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsDrawioResourceIconStyle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/aws-arch.AwsDrawioShapeStyle",
    jsii_struct_bases=[_DrawioAwsResourceIconStyleBase_9b406fcd],
    name_mapping={
        "align": "align",
        "aspect": "aspect",
        "dashed": "dashed",
        "font_size": "fontSize",
        "font_style": "fontStyle",
        "gradient_direction": "gradientDirection",
        "html": "html",
        "outline_connect": "outlineConnect",
        "stroke_color": "strokeColor",
        "vertical_align": "verticalAlign",
        "vertical_label_position": "verticalLabelPosition",
        "pointer_event": "pointerEvent",
        "fill_color": "fillColor",
        "font_color": "fontColor",
        "gradient_color": "gradientColor",
        "shape": "shape",
    },
)
class AwsDrawioShapeStyle(_DrawioAwsResourceIconStyleBase_9b406fcd):
    def __init__(
        self,
        *,
        align: builtins.str,
        aspect: builtins.str,
        dashed: jsii.Number,
        font_size: jsii.Number,
        font_style: typing.Union[builtins.str, jsii.Number],
        gradient_direction: builtins.str,
        html: jsii.Number,
        outline_connect: jsii.Number,
        stroke_color: builtins.str,
        vertical_align: builtins.str,
        vertical_label_position: builtins.str,
        pointer_event: typing.Optional[jsii.Number] = None,
        fill_color: builtins.str,
        font_color: builtins.str,
        gradient_color: builtins.str,
        shape: _ShapeNames_b18b2fa9,
    ) -> None:
        '''(experimental) Drawio shape based style definition.

        :param align: 
        :param aspect: 
        :param dashed: 
        :param font_size: 
        :param font_style: 
        :param gradient_direction: 
        :param html: 
        :param outline_connect: 
        :param stroke_color: 
        :param vertical_align: 
        :param vertical_label_position: 
        :param pointer_event: 
        :param fill_color: 
        :param font_color: 
        :param gradient_color: 
        :param shape: 

        :stability: experimental
        '''
        if __debug__:
            def stub(
                *,
                align: builtins.str,
                aspect: builtins.str,
                dashed: jsii.Number,
                font_size: jsii.Number,
                font_style: typing.Union[builtins.str, jsii.Number],
                gradient_direction: builtins.str,
                html: jsii.Number,
                outline_connect: jsii.Number,
                stroke_color: builtins.str,
                vertical_align: builtins.str,
                vertical_label_position: builtins.str,
                pointer_event: typing.Optional[jsii.Number] = None,
                fill_color: builtins.str,
                font_color: builtins.str,
                gradient_color: builtins.str,
                shape: _ShapeNames_b18b2fa9,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument align", value=align, expected_type=type_hints["align"])
            check_type(argname="argument aspect", value=aspect, expected_type=type_hints["aspect"])
            check_type(argname="argument dashed", value=dashed, expected_type=type_hints["dashed"])
            check_type(argname="argument font_size", value=font_size, expected_type=type_hints["font_size"])
            check_type(argname="argument font_style", value=font_style, expected_type=type_hints["font_style"])
            check_type(argname="argument gradient_direction", value=gradient_direction, expected_type=type_hints["gradient_direction"])
            check_type(argname="argument html", value=html, expected_type=type_hints["html"])
            check_type(argname="argument outline_connect", value=outline_connect, expected_type=type_hints["outline_connect"])
            check_type(argname="argument stroke_color", value=stroke_color, expected_type=type_hints["stroke_color"])
            check_type(argname="argument vertical_align", value=vertical_align, expected_type=type_hints["vertical_align"])
            check_type(argname="argument vertical_label_position", value=vertical_label_position, expected_type=type_hints["vertical_label_position"])
            check_type(argname="argument pointer_event", value=pointer_event, expected_type=type_hints["pointer_event"])
            check_type(argname="argument fill_color", value=fill_color, expected_type=type_hints["fill_color"])
            check_type(argname="argument font_color", value=font_color, expected_type=type_hints["font_color"])
            check_type(argname="argument gradient_color", value=gradient_color, expected_type=type_hints["gradient_color"])
            check_type(argname="argument shape", value=shape, expected_type=type_hints["shape"])
        self._values: typing.Dict[str, typing.Any] = {
            "align": align,
            "aspect": aspect,
            "dashed": dashed,
            "font_size": font_size,
            "font_style": font_style,
            "gradient_direction": gradient_direction,
            "html": html,
            "outline_connect": outline_connect,
            "stroke_color": stroke_color,
            "vertical_align": vertical_align,
            "vertical_label_position": vertical_label_position,
            "fill_color": fill_color,
            "font_color": font_color,
            "gradient_color": gradient_color,
            "shape": shape,
        }
        if pointer_event is not None:
            self._values["pointer_event"] = pointer_event

    @builtins.property
    def align(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("align")
        assert result is not None, "Required property 'align' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aspect(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("aspect")
        assert result is not None, "Required property 'aspect' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dashed(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("dashed")
        assert result is not None, "Required property 'dashed' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def font_size(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("font_size")
        assert result is not None, "Required property 'font_size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def font_style(self) -> typing.Union[builtins.str, jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("font_style")
        assert result is not None, "Required property 'font_style' is missing"
        return typing.cast(typing.Union[builtins.str, jsii.Number], result)

    @builtins.property
    def gradient_direction(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("gradient_direction")
        assert result is not None, "Required property 'gradient_direction' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def html(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("html")
        assert result is not None, "Required property 'html' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def outline_connect(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("outline_connect")
        assert result is not None, "Required property 'outline_connect' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def stroke_color(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("stroke_color")
        assert result is not None, "Required property 'stroke_color' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vertical_align(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("vertical_align")
        assert result is not None, "Required property 'vertical_align' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vertical_label_position(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("vertical_label_position")
        assert result is not None, "Required property 'vertical_label_position' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pointer_event(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("pointer_event")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fill_color(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("fill_color")
        assert result is not None, "Required property 'fill_color' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def font_color(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("font_color")
        assert result is not None, "Required property 'font_color' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gradient_color(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("gradient_color")
        assert result is not None, "Required property 'gradient_color' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def shape(self) -> _ShapeNames_b18b2fa9:
        '''
        :stability: experimental
        '''
        result = self._values.get("shape")
        assert result is not None, "Required property 'shape' is missing"
        return typing.cast(_ShapeNames_b18b2fa9, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsDrawioShapeStyle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AwsResource(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/aws-arch.AwsResource",
):
    '''(experimental) AwsResource class provides an interface for normalizing resource metadata between mapped systems.

    :stability: experimental
    '''

    @jsii.member(jsii_name="findResource")
    @builtins.classmethod
    def find_resource(cls, value: builtins.str) -> typing.Optional["AwsResource"]:
        '''(experimental) Find {@link AwsResource} associated with given value.

        :param value: - The value to match {@link AwsResource}; can be id, asset key, full name, etc.

        :stability: experimental
        :throws: Error is no resource found
        '''
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(typing.Optional["AwsResource"], jsii.sinvoke(cls, "findResource", [value]))

    @jsii.member(jsii_name="getResource")
    @builtins.classmethod
    def get_resource(cls, cfn_resource_type: builtins.str) -> "AwsResource":
        '''(experimental) Get {@link AwsResource} by CloudFormation resource type.

        :param cfn_resource_type: - Fully qualifief CloudFormation resource type (eg: AWS:S3:Bucket).

        :stability: experimental
        :throws: Error is no resource found
        '''
        if __debug__:
            def stub(cfn_resource_type: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument cfn_resource_type", value=cfn_resource_type, expected_type=type_hints["cfn_resource_type"])
        return typing.cast("AwsResource", jsii.sinvoke(cls, "getResource", [cfn_resource_type]))

    @jsii.member(jsii_name="drawioStyle")
    def drawio_style(self) -> typing.Optional[AwsDrawioShapeStyle]:
        '''(experimental) Gets the draiwio style for the resource.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[AwsDrawioShapeStyle], jsii.invoke(self, "drawioStyle", []))

    @jsii.member(jsii_name="getCategoryIcon")
    def get_category_icon(
        self,
        format: builtins.str,
        theme: typing.Optional[builtins.str] = None,
    ) -> typing.Optional[builtins.str]:
        '''(experimental) Gets the category icon for the resource.

        This maybe different than {@link AwsResource.service.category.icon} based on mappings overrides, which
        if do not exist will fallback to {@link AwsResource.service.category.icon}.

        :param format: - The format of icon.
        :param theme: - Optional theme.

        :return: Returns relative asset icon path

        :see: {@link AwsService.icon}
        :stability: experimental
        '''
        if __debug__:
            def stub(
                format: builtins.str,
                theme: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "getCategoryIcon", [format, theme]))

    @jsii.member(jsii_name="getGeneralIcon")
    def get_general_icon(
        self,
        format: builtins.str,
        theme: typing.Optional[builtins.str] = None,
    ) -> typing.Optional[builtins.str]:
        '''(experimental) Gets the general icon for the resource if available.

        :param format: - The format of icon.
        :param theme: - Optional theme.

        :return: Returns relative asset icon path or undefined if does not have general icon

        :stability: experimental
        '''
        if __debug__:
            def stub(
                format: builtins.str,
                theme: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "getGeneralIcon", [format, theme]))

    @jsii.member(jsii_name="getResourceIcon")
    def get_resource_icon(
        self,
        format: builtins.str,
        theme: typing.Optional[builtins.str] = None,
    ) -> typing.Optional[builtins.str]:
        '''(experimental) Gets the resource specific icon for the resource.

        :param format: - The format of icon.
        :param theme: - Optional theme.

        :return: Returns relative asset icon path or undefined if does not have resource icon

        :stability: experimental
        '''
        if __debug__:
            def stub(
                format: builtins.str,
                theme: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "getResourceIcon", [format, theme]))

    @jsii.member(jsii_name="getServiceIcon")
    def get_service_icon(
        self,
        format: builtins.str,
        theme: typing.Optional[builtins.str] = None,
    ) -> typing.Optional[builtins.str]:
        '''(experimental) Gets the service icon for the resource.

        This maybe different than {@link AwsResource.service.icon} based on mappings overrides, which
        if do not exist will fallback to {@link AwsResource.service.icon}.

        :param format: - The format of icon.
        :param theme: - Optional theme.

        :return: Returns relative asset icon path

        :see: {@link AwsService.icon}
        :stability: experimental
        '''
        if __debug__:
            def stub(
                format: builtins.str,
                theme: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "getServiceIcon", [format, theme]))

    @jsii.member(jsii_name="icon")
    def icon(
        self,
        format: builtins.str,
        theme: typing.Optional[builtins.str] = None,
    ) -> typing.Optional[builtins.str]:
        '''(experimental) Gets the best icon match for the resource following the order of: 1.

        explicit resource icon
        2. general icon
        3. service icon

        :param format: - The format of icon.
        :param theme: - Optional theme.

        :return: Returns relative asset icon path

        :stability: experimental
        '''
        if __debug__:
            def stub(
                format: builtins.str,
                theme: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "icon", [format, theme]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="resources")
    def resources(cls) -> typing.Mapping[builtins.str, "AwsResource"]:
        '''(experimental) Get record of all resources keyed by resource id.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, "AwsResource"], jsii.sget(cls, "resources"))

    @builtins.property
    @jsii.member(jsii_name="cfnResourceType")
    def cfn_resource_type(self) -> builtins.str:
        '''(experimental) Fully-qualified CloudFormation resource type (eg: "AWS:S3:Bucket").

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "cfnResourceType"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> "AwsService":
        '''(experimental) The {@link AwsService} the resource belongs to.

        :stability: experimental
        '''
        return typing.cast("AwsService", jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="drawioShape")
    def drawio_shape(self) -> typing.Optional[_ShapeNames_b18b2fa9]:
        '''(experimental) The drawio shape mapped to this resource, or undefined if no mapping.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_ShapeNames_b18b2fa9], jsii.get(self, "drawioShape"))

    @builtins.property
    @jsii.member(jsii_name="fullName")
    def full_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The proper full name of the resource.

        :stability: experimental

        Example::

            "Bucket", "Amazon S3 on Outposts"
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fullName"))


class AwsService(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/aws-arch.AwsService",
):
    '''(experimental) AwsService class provides an interface for normalizing service metadata between mapped systems.

    :stability: experimental
    '''

    @jsii.member(jsii_name="findService")
    @builtins.classmethod
    def find_service(cls, value: builtins.str) -> typing.Optional["AwsService"]:
        '''(experimental) Finds the {@link AwsService} associated with a given value.

        :param value: Value to match {@link AwsService}, which can be ``id``, ``assetKey``, ``fullName``, etc.

        :return: Returns matching {@link AwsService} or ``undefined`` if not found

        :stability: experimental
        :throws: Error if service not found
        '''
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(typing.Optional["AwsService"], jsii.sinvoke(cls, "findService", [value]))

    @jsii.member(jsii_name="getService")
    @builtins.classmethod
    def get_service(cls, cfn_service: builtins.str) -> "AwsService":
        '''(experimental) Get {@link AwsService} by CloudFormation "service" name, where service name is expressed as ``<provider>::<service>::<resource>``.

        :param cfn_service: The service name to retrieve {@link AwsService} for.

        :return: Returns the {@link AwsService} associated with the ``cfnService`` provided

        :stability: experimental
        :throws: Error is service not found
        '''
        if __debug__:
            def stub(cfn_service: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument cfn_service", value=cfn_service, expected_type=type_hints["cfn_service"])
        return typing.cast("AwsService", jsii.sinvoke(cls, "getService", [cfn_service]))

    @jsii.member(jsii_name="drawioStyle")
    def drawio_style(self) -> typing.Optional[AwsDrawioResourceIconStyle]:
        '''(experimental) Get drawio style for this service.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[AwsDrawioResourceIconStyle], jsii.invoke(self, "drawioStyle", []))

    @jsii.member(jsii_name="icon")
    def icon(
        self,
        format: builtins.str,
        theme: typing.Optional[builtins.str] = None,
    ) -> typing.Optional[builtins.str]:
        '''(experimental) Get relative asset icon for the service for a given format and optional theme.

        :param format: - The format of icon.
        :param theme: - Optional theme.

        :return: Returns relative asset icon path

        :stability: experimental
        '''
        if __debug__:
            def stub(
                format: builtins.str,
                theme: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "icon", [format, theme]))

    @jsii.member(jsii_name="serviceResources")
    def service_resources(self) -> typing.List[AwsResource]:
        '''(experimental) List all resources of this service.

        :stability: experimental
        '''
        return typing.cast(typing.List[AwsResource], jsii.invoke(self, "serviceResources", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="services")
    def services(cls) -> typing.Mapping[builtins.str, "AwsService"]:
        '''(experimental) Get record of all {@link AwsService}s keyed by ``id``.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, "AwsService"], jsii.sget(cls, "services"))

    @builtins.property
    @jsii.member(jsii_name="cfnProvider")
    def cfn_provider(self) -> builtins.str:
        '''(experimental) The CloudFormation "provider" for the service, as expressed by ``<provicer>::<service>::<resource>``.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "cfnProvider"))

    @builtins.property
    @jsii.member(jsii_name="cfnService")
    def cfn_service(self) -> builtins.str:
        '''(experimental) The CloudFormation "service" for the service, as expressed by ``<provicer>::<service>::<resource>``.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "cfnService"))

    @builtins.property
    @jsii.member(jsii_name="fullName")
    def full_name(self) -> builtins.str:
        '''(experimental) The proper full name of the service.

        :stability: experimental

        Example::

            "AWS Glue", "Amazon S3"
        '''
        return typing.cast(builtins.str, jsii.get(self, "fullName"))

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> typing.Optional[AwsCategory]:
        '''(experimental) The category the service belongs to, or undefined if does not belong to a category.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[AwsCategory], jsii.get(self, "category"))

    @builtins.property
    @jsii.member(jsii_name="drawioShape")
    def drawio_shape(self) -> typing.Optional[_ShapeNames_b18b2fa9]:
        '''(experimental) Drawio shape associated with this service, or undefined if service not mapped to draiwio shape.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_ShapeNames_b18b2fa9], jsii.get(self, "drawioShape"))

    @builtins.property
    @jsii.member(jsii_name="pricingMetadata")
    def pricing_metadata(self) -> typing.Optional[_Service_4bf9f4e8]:
        '''(experimental) Get service pricing metadata.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_Service_4bf9f4e8], jsii.get(self, "pricingMetadata"))

    @builtins.property
    @jsii.member(jsii_name="pricingServiceCode")
    def pricing_service_code(self) -> typing.Optional[builtins.str]:
        '''(experimental) The pricing ``serviceCode`` associated with this service, or undefined if service not mapped to pricing.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pricingServiceCode"))


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/aws-arch.ParsedAssetKey",
    jsii_struct_bases=[],
    name_mapping={
        "asset_key": "assetKey",
        "basename": "basename",
        "category": "category",
        "instance_type": "instanceType",
        "iot_thing": "iotThing",
        "resource": "resource",
        "service": "service",
    },
)
class ParsedAssetKey:
    def __init__(
        self,
        *,
        asset_key: builtins.str,
        basename: builtins.str,
        category: builtins.str,
        instance_type: typing.Optional[builtins.str] = None,
        iot_thing: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Parsed asset key.

        :param asset_key: (experimental) Reference to the full key that was parsed.
        :param basename: (experimental) The last segment of the key (which is the nested icon). For instances and things this includes the dir prefix.
        :param category: (experimental) Category id.
        :param instance_type: (experimental) The instance type if key is for an ec2 instance.
        :param iot_thing: (experimental) The iot thing if key is for an iot thing.
        :param resource: (experimental) Resource id if key is for a resource.
        :param service: (experimental) Service id if key is partitioned by resource.

        :stability: experimental
        '''
        if __debug__:
            def stub(
                *,
                asset_key: builtins.str,
                basename: builtins.str,
                category: builtins.str,
                instance_type: typing.Optional[builtins.str] = None,
                iot_thing: typing.Optional[builtins.str] = None,
                resource: typing.Optional[builtins.str] = None,
                service: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument asset_key", value=asset_key, expected_type=type_hints["asset_key"])
            check_type(argname="argument basename", value=basename, expected_type=type_hints["basename"])
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument iot_thing", value=iot_thing, expected_type=type_hints["iot_thing"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[str, typing.Any] = {
            "asset_key": asset_key,
            "basename": basename,
            "category": category,
        }
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if iot_thing is not None:
            self._values["iot_thing"] = iot_thing
        if resource is not None:
            self._values["resource"] = resource
        if service is not None:
            self._values["service"] = service

    @builtins.property
    def asset_key(self) -> builtins.str:
        '''(experimental) Reference to the full key that was parsed.

        :stability: experimental
        '''
        result = self._values.get("asset_key")
        assert result is not None, "Required property 'asset_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def basename(self) -> builtins.str:
        '''(experimental) The last segment of the key (which is the nested icon).

        For instances and things this includes the dir prefix.

        :stability: experimental
        '''
        result = self._values.get("basename")
        assert result is not None, "Required property 'basename' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def category(self) -> builtins.str:
        '''(experimental) Category id.

        :stability: experimental
        '''
        result = self._values.get("category")
        assert result is not None, "Required property 'category' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) The instance type if key is for an ec2 instance.

        :stability: experimental
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iot_thing(self) -> typing.Optional[builtins.str]:
        '''(experimental) The iot thing if key is for an iot thing.

        :stability: experimental
        '''
        result = self._values.get("iot_thing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''(experimental) Resource id if key is for a resource.

        :stability: experimental
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''(experimental) Service id if key is partitioned by resource.

        :stability: experimental
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParsedAssetKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsArchitecture",
    "AwsCategory",
    "AwsCategoryDrawioStyles",
    "AwsDrawioResourceIconStyle",
    "AwsDrawioShapeStyle",
    "AwsResource",
    "AwsService",
    "ParsedAssetKey",
    "aws_arch",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import aws_arch
