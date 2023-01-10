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


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/aws-arch.aws_arch.ArrowFormat",
    jsii_struct_bases=[],
    name_mapping={
        "color": "color",
        "head": "head",
        "style": "style",
        "tail": "tail",
        "width": "width",
    },
)
class ArrowFormat:
    def __init__(
        self,
        *,
        color: typing.Union[builtins.str, builtins.bool],
        head: builtins.str,
        style: builtins.str,
        tail: builtins.str,
        width: jsii.Number,
    ) -> None:
        '''(experimental) Theme arrow format definition.

        :param color: 
        :param head: 
        :param style: 
        :param tail: 
        :param width: 

        :stability: experimental
        '''
        if __debug__:
            def stub(
                *,
                color: typing.Union[builtins.str, builtins.bool],
                head: builtins.str,
                style: builtins.str,
                tail: builtins.str,
                width: jsii.Number,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument color", value=color, expected_type=type_hints["color"])
            check_type(argname="argument head", value=head, expected_type=type_hints["head"])
            check_type(argname="argument style", value=style, expected_type=type_hints["style"])
            check_type(argname="argument tail", value=tail, expected_type=type_hints["tail"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[str, typing.Any] = {
            "color": color,
            "head": head,
            "style": style,
            "tail": tail,
            "width": width,
        }

    @builtins.property
    def color(self) -> typing.Union[builtins.str, builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("color")
        assert result is not None, "Required property 'color' is missing"
        return typing.cast(typing.Union[builtins.str, builtins.bool], result)

    @builtins.property
    def head(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("head")
        assert result is not None, "Required property 'head' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def style(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("style")
        assert result is not None, "Required property 'style' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tail(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("tail")
        assert result is not None, "Required property 'tail' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def width(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("width")
        assert result is not None, "Required property 'width' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArrowFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/aws-arch.aws_arch.AwsCategoryDefinition",
    jsii_struct_bases=[],
    name_mapping={
        "fill_color": "fillColor",
        "gradient_color": "gradientColor",
        "id": "id",
        "name": "name",
        "font_color": "fontColor",
        "variants": "variants",
    },
)
class AwsCategoryDefinition:
    def __init__(
        self,
        *,
        fill_color: builtins.str,
        gradient_color: builtins.str,
        id: builtins.str,
        name: builtins.str,
        font_color: typing.Optional[builtins.str] = None,
        variants: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Category definition.

        :param fill_color: 
        :param gradient_color: 
        :param id: 
        :param name: 
        :param font_color: 
        :param variants: 

        :stability: experimental
        '''
        if __debug__:
            def stub(
                *,
                fill_color: builtins.str,
                gradient_color: builtins.str,
                id: builtins.str,
                name: builtins.str,
                font_color: typing.Optional[builtins.str] = None,
                variants: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument fill_color", value=fill_color, expected_type=type_hints["fill_color"])
            check_type(argname="argument gradient_color", value=gradient_color, expected_type=type_hints["gradient_color"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument font_color", value=font_color, expected_type=type_hints["font_color"])
            check_type(argname="argument variants", value=variants, expected_type=type_hints["variants"])
        self._values: typing.Dict[str, typing.Any] = {
            "fill_color": fill_color,
            "gradient_color": gradient_color,
            "id": id,
            "name": name,
        }
        if font_color is not None:
            self._values["font_color"] = font_color
        if variants is not None:
            self._values["variants"] = variants

    @builtins.property
    def fill_color(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("fill_color")
        assert result is not None, "Required property 'fill_color' is missing"
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
    def id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def font_color(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("font_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variants(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("variants")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsCategoryDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-prototyping-sdk/aws-arch.aws_arch.DarkPalette")
class DarkPalette(enum.Enum):
    '''(experimental) Dark theme color palette.

    :stability: experimental
    '''

    PUBLIC = "PUBLIC"
    '''
    :stability: experimental
    '''
    PRIVATE = "PRIVATE"
    '''
    :stability: experimental
    '''
    GENERIC = "GENERIC"
    '''
    :stability: experimental
    '''
    PRIMARY = "PRIMARY"
    '''
    :stability: experimental
    '''
    SECONDARY = "SECONDARY"
    '''
    :stability: experimental
    '''
    TERTIARY = "TERTIARY"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-prototyping-sdk/aws-arch.aws_arch.DrawioAws4ParentShapes")
class DrawioAws4ParentShapes(enum.Enum):
    '''(experimental) Draiwio aws4 parent shapes enum.

    :stability: experimental
    '''

    RESOURCE_ICON = "RESOURCE_ICON"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/aws-arch.aws_arch.DrawioAwsShapeStyleBase",
    jsii_struct_bases=[],
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
    },
)
class DrawioAwsShapeStyleBase:
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
    ) -> None:
        '''(experimental) Base definition of drawio aws shape style.

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

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DrawioAwsShapeStyleBase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/aws-arch.aws_arch.GroupFormat",
    jsii_struct_bases=[],
    name_mapping={
        "bgcolor": "bgcolor",
        "border_color": "borderColor",
        "border_style": "borderStyle",
        "color": "color",
        "icon_png": "iconPng",
        "label_location": "labelLocation",
    },
)
class GroupFormat:
    def __init__(
        self,
        *,
        bgcolor: typing.Union[builtins.str, builtins.bool],
        border_color: typing.Union[builtins.str, builtins.bool],
        border_style: builtins.str,
        color: typing.Union[builtins.str, builtins.bool],
        icon_png: typing.Optional[builtins.str] = None,
        label_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Theme group format definition.

        :param bgcolor: 
        :param border_color: 
        :param border_style: 
        :param color: 
        :param icon_png: 
        :param label_location: 

        :stability: experimental
        '''
        if __debug__:
            def stub(
                *,
                bgcolor: typing.Union[builtins.str, builtins.bool],
                border_color: typing.Union[builtins.str, builtins.bool],
                border_style: builtins.str,
                color: typing.Union[builtins.str, builtins.bool],
                icon_png: typing.Optional[builtins.str] = None,
                label_location: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument bgcolor", value=bgcolor, expected_type=type_hints["bgcolor"])
            check_type(argname="argument border_color", value=border_color, expected_type=type_hints["border_color"])
            check_type(argname="argument border_style", value=border_style, expected_type=type_hints["border_style"])
            check_type(argname="argument color", value=color, expected_type=type_hints["color"])
            check_type(argname="argument icon_png", value=icon_png, expected_type=type_hints["icon_png"])
            check_type(argname="argument label_location", value=label_location, expected_type=type_hints["label_location"])
        self._values: typing.Dict[str, typing.Any] = {
            "bgcolor": bgcolor,
            "border_color": border_color,
            "border_style": border_style,
            "color": color,
        }
        if icon_png is not None:
            self._values["icon_png"] = icon_png
        if label_location is not None:
            self._values["label_location"] = label_location

    @builtins.property
    def bgcolor(self) -> typing.Union[builtins.str, builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("bgcolor")
        assert result is not None, "Required property 'bgcolor' is missing"
        return typing.cast(typing.Union[builtins.str, builtins.bool], result)

    @builtins.property
    def border_color(self) -> typing.Union[builtins.str, builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("border_color")
        assert result is not None, "Required property 'border_color' is missing"
        return typing.cast(typing.Union[builtins.str, builtins.bool], result)

    @builtins.property
    def border_style(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("border_style")
        assert result is not None, "Required property 'border_style' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def color(self) -> typing.Union[builtins.str, builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("color")
        assert result is not None, "Required property 'color' is missing"
        return typing.cast(typing.Union[builtins.str, builtins.bool], result)

    @builtins.property
    def icon_png(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("icon_png")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def label_location(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("label_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-prototyping-sdk/aws-arch.aws_arch.LightPalette")
class LightPalette(enum.Enum):
    '''(experimental) Light theme color palette.

    :stability: experimental
    '''

    PUBLIC = "PUBLIC"
    '''
    :stability: experimental
    '''
    PRIVATE = "PRIVATE"
    '''
    :stability: experimental
    '''
    GENERIC = "GENERIC"
    '''
    :stability: experimental
    '''
    PRIMARY = "PRIMARY"
    '''
    :stability: experimental
    '''
    SECONDARY = "SECONDARY"
    '''
    :stability: experimental
    '''
    TERTIARY = "TERTIARY"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/aws-arch.aws_arch.ParsedAssetKey",
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


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/aws-arch.aws_arch.Theme",
    jsii_struct_bases=[],
    name_mapping={
        "arrows": "arrows",
        "backgrounds": "backgrounds",
        "groups": "groups",
        "id": "id",
        "text": "text",
    },
)
class Theme:
    def __init__(
        self,
        *,
        arrows: typing.Union["ThemeArrows", typing.Dict[str, typing.Any]],
        backgrounds: typing.Union["ThemeBackgrounds", typing.Dict[str, typing.Any]],
        groups: typing.Union["ThemeGroups", typing.Dict[str, typing.Any]],
        id: builtins.str,
        text: typing.Union["ThemeText", typing.Dict[str, typing.Any]],
    ) -> None:
        '''(experimental) Theme definition.

        :param arrows: 
        :param backgrounds: 
        :param groups: 
        :param id: 
        :param text: 

        :stability: experimental
        '''
        if isinstance(arrows, dict):
            arrows = ThemeArrows(**arrows)
        if isinstance(backgrounds, dict):
            backgrounds = ThemeBackgrounds(**backgrounds)
        if isinstance(groups, dict):
            groups = ThemeGroups(**groups)
        if isinstance(text, dict):
            text = ThemeText(**text)
        if __debug__:
            def stub(
                *,
                arrows: typing.Union[ThemeArrows, typing.Dict[str, typing.Any]],
                backgrounds: typing.Union[ThemeBackgrounds, typing.Dict[str, typing.Any]],
                groups: typing.Union[ThemeGroups, typing.Dict[str, typing.Any]],
                id: builtins.str,
                text: typing.Union[ThemeText, typing.Dict[str, typing.Any]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument arrows", value=arrows, expected_type=type_hints["arrows"])
            check_type(argname="argument backgrounds", value=backgrounds, expected_type=type_hints["backgrounds"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[str, typing.Any] = {
            "arrows": arrows,
            "backgrounds": backgrounds,
            "groups": groups,
            "id": id,
            "text": text,
        }

    @builtins.property
    def arrows(self) -> "ThemeArrows":
        '''
        :stability: experimental
        '''
        result = self._values.get("arrows")
        assert result is not None, "Required property 'arrows' is missing"
        return typing.cast("ThemeArrows", result)

    @builtins.property
    def backgrounds(self) -> "ThemeBackgrounds":
        '''
        :stability: experimental
        '''
        result = self._values.get("backgrounds")
        assert result is not None, "Required property 'backgrounds' is missing"
        return typing.cast("ThemeBackgrounds", result)

    @builtins.property
    def groups(self) -> "ThemeGroups":
        '''
        :stability: experimental
        '''
        result = self._values.get("groups")
        assert result is not None, "Required property 'groups' is missing"
        return typing.cast("ThemeGroups", result)

    @builtins.property
    def id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def text(self) -> "ThemeText":
        '''
        :stability: experimental
        '''
        result = self._values.get("text")
        assert result is not None, "Required property 'text' is missing"
        return typing.cast("ThemeText", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Theme(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/aws-arch.aws_arch.ThemeArrows",
    jsii_struct_bases=[],
    name_mapping={
        "child": "child",
        "default": "default",
        "dependency": "dependency",
        "reference": "reference",
    },
)
class ThemeArrows:
    def __init__(
        self,
        *,
        child: typing.Union[ArrowFormat, typing.Dict[str, typing.Any]],
        default: typing.Union[ArrowFormat, typing.Dict[str, typing.Any]],
        dependency: typing.Union[ArrowFormat, typing.Dict[str, typing.Any]],
        reference: typing.Union[ArrowFormat, typing.Dict[str, typing.Any]],
    ) -> None:
        '''(experimental) Theme arrow dictionary.

        :param child: 
        :param default: 
        :param dependency: 
        :param reference: 

        :stability: experimental
        '''
        if isinstance(child, dict):
            child = ArrowFormat(**child)
        if isinstance(default, dict):
            default = ArrowFormat(**default)
        if isinstance(dependency, dict):
            dependency = ArrowFormat(**dependency)
        if isinstance(reference, dict):
            reference = ArrowFormat(**reference)
        if __debug__:
            def stub(
                *,
                child: typing.Union[ArrowFormat, typing.Dict[str, typing.Any]],
                default: typing.Union[ArrowFormat, typing.Dict[str, typing.Any]],
                dependency: typing.Union[ArrowFormat, typing.Dict[str, typing.Any]],
                reference: typing.Union[ArrowFormat, typing.Dict[str, typing.Any]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument child", value=child, expected_type=type_hints["child"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument dependency", value=dependency, expected_type=type_hints["dependency"])
            check_type(argname="argument reference", value=reference, expected_type=type_hints["reference"])
        self._values: typing.Dict[str, typing.Any] = {
            "child": child,
            "default": default,
            "dependency": dependency,
            "reference": reference,
        }

    @builtins.property
    def child(self) -> ArrowFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("child")
        assert result is not None, "Required property 'child' is missing"
        return typing.cast(ArrowFormat, result)

    @builtins.property
    def default(self) -> ArrowFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("default")
        assert result is not None, "Required property 'default' is missing"
        return typing.cast(ArrowFormat, result)

    @builtins.property
    def dependency(self) -> ArrowFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("dependency")
        assert result is not None, "Required property 'dependency' is missing"
        return typing.cast(ArrowFormat, result)

    @builtins.property
    def reference(self) -> ArrowFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("reference")
        assert result is not None, "Required property 'reference' is missing"
        return typing.cast(ArrowFormat, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ThemeArrows(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/aws-arch.aws_arch.ThemeBackgrounds",
    jsii_struct_bases=[],
    name_mapping={
        "base": "base",
        "generic": "generic",
        "private": "private",
        "public": "public",
    },
)
class ThemeBackgrounds:
    def __init__(
        self,
        *,
        base: builtins.str,
        generic: builtins.str,
        private: builtins.str,
        public: builtins.str,
    ) -> None:
        '''(experimental) Theme background dictionary.

        :param base: 
        :param generic: 
        :param private: 
        :param public: 

        :stability: experimental
        '''
        if __debug__:
            def stub(
                *,
                base: builtins.str,
                generic: builtins.str,
                private: builtins.str,
                public: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument base", value=base, expected_type=type_hints["base"])
            check_type(argname="argument generic", value=generic, expected_type=type_hints["generic"])
            check_type(argname="argument private", value=private, expected_type=type_hints["private"])
            check_type(argname="argument public", value=public, expected_type=type_hints["public"])
        self._values: typing.Dict[str, typing.Any] = {
            "base": base,
            "generic": generic,
            "private": private,
            "public": public,
        }

    @builtins.property
    def base(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("base")
        assert result is not None, "Required property 'base' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generic(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("generic")
        assert result is not None, "Required property 'generic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def private(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("private")
        assert result is not None, "Required property 'private' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def public(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("public")
        assert result is not None, "Required property 'public' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ThemeBackgrounds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/aws-arch.aws_arch.ThemeGroups",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_group": "autoScalingGroup",
        "availability_zone": "availabilityZone",
        "aws_account": "awsAccount",
        "aws_io_t_greengrass": "awsIoTGreengrass",
        "aws_io_t_greengrass_deployment": "awsIoTGreengrassDeployment",
        "aws_step_functions_workflow": "awsStepFunctionsWorkflow",
        "cloud": "cloud",
        "cloud_alt": "cloudAlt",
        "corporate_data_center": "corporateDataCenter",
        "ec2_instance_contents": "ec2InstanceContents",
        "elastic_beanstalk_container": "elasticBeanstalkContainer",
        "generic": "generic",
        "generic_alt": "genericAlt",
        "private_subnet": "privateSubnet",
        "public_subnet": "publicSubnet",
        "region": "region",
        "security_group": "securityGroup",
        "server_contents": "serverContents",
        "spot_fleet": "spotFleet",
        "vpc": "vpc",
    },
)
class ThemeGroups:
    def __init__(
        self,
        *,
        auto_scaling_group: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
        availability_zone: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
        aws_account: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
        aws_io_t_greengrass: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
        aws_io_t_greengrass_deployment: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
        aws_step_functions_workflow: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
        cloud: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
        cloud_alt: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
        corporate_data_center: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
        ec2_instance_contents: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
        elastic_beanstalk_container: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
        generic: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
        generic_alt: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
        private_subnet: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
        public_subnet: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
        region: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
        security_group: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
        server_contents: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
        spot_fleet: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
        vpc: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
    ) -> None:
        '''(experimental) Theme group dicionary.

        :param auto_scaling_group: 
        :param availability_zone: 
        :param aws_account: 
        :param aws_io_t_greengrass: 
        :param aws_io_t_greengrass_deployment: 
        :param aws_step_functions_workflow: 
        :param cloud: 
        :param cloud_alt: 
        :param corporate_data_center: 
        :param ec2_instance_contents: 
        :param elastic_beanstalk_container: 
        :param generic: 
        :param generic_alt: 
        :param private_subnet: 
        :param public_subnet: 
        :param region: 
        :param security_group: 
        :param server_contents: 
        :param spot_fleet: 
        :param vpc: 

        :stability: experimental
        '''
        if isinstance(auto_scaling_group, dict):
            auto_scaling_group = GroupFormat(**auto_scaling_group)
        if isinstance(availability_zone, dict):
            availability_zone = GroupFormat(**availability_zone)
        if isinstance(aws_account, dict):
            aws_account = GroupFormat(**aws_account)
        if isinstance(aws_io_t_greengrass, dict):
            aws_io_t_greengrass = GroupFormat(**aws_io_t_greengrass)
        if isinstance(aws_io_t_greengrass_deployment, dict):
            aws_io_t_greengrass_deployment = GroupFormat(**aws_io_t_greengrass_deployment)
        if isinstance(aws_step_functions_workflow, dict):
            aws_step_functions_workflow = GroupFormat(**aws_step_functions_workflow)
        if isinstance(cloud, dict):
            cloud = GroupFormat(**cloud)
        if isinstance(cloud_alt, dict):
            cloud_alt = GroupFormat(**cloud_alt)
        if isinstance(corporate_data_center, dict):
            corporate_data_center = GroupFormat(**corporate_data_center)
        if isinstance(ec2_instance_contents, dict):
            ec2_instance_contents = GroupFormat(**ec2_instance_contents)
        if isinstance(elastic_beanstalk_container, dict):
            elastic_beanstalk_container = GroupFormat(**elastic_beanstalk_container)
        if isinstance(generic, dict):
            generic = GroupFormat(**generic)
        if isinstance(generic_alt, dict):
            generic_alt = GroupFormat(**generic_alt)
        if isinstance(private_subnet, dict):
            private_subnet = GroupFormat(**private_subnet)
        if isinstance(public_subnet, dict):
            public_subnet = GroupFormat(**public_subnet)
        if isinstance(region, dict):
            region = GroupFormat(**region)
        if isinstance(security_group, dict):
            security_group = GroupFormat(**security_group)
        if isinstance(server_contents, dict):
            server_contents = GroupFormat(**server_contents)
        if isinstance(spot_fleet, dict):
            spot_fleet = GroupFormat(**spot_fleet)
        if isinstance(vpc, dict):
            vpc = GroupFormat(**vpc)
        if __debug__:
            def stub(
                *,
                auto_scaling_group: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
                availability_zone: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
                aws_account: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
                aws_io_t_greengrass: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
                aws_io_t_greengrass_deployment: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
                aws_step_functions_workflow: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
                cloud: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
                cloud_alt: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
                corporate_data_center: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
                ec2_instance_contents: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
                elastic_beanstalk_container: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
                generic: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
                generic_alt: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
                private_subnet: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
                public_subnet: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
                region: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
                security_group: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
                server_contents: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
                spot_fleet: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
                vpc: typing.Union[GroupFormat, typing.Dict[str, typing.Any]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument auto_scaling_group", value=auto_scaling_group, expected_type=type_hints["auto_scaling_group"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument aws_account", value=aws_account, expected_type=type_hints["aws_account"])
            check_type(argname="argument aws_io_t_greengrass", value=aws_io_t_greengrass, expected_type=type_hints["aws_io_t_greengrass"])
            check_type(argname="argument aws_io_t_greengrass_deployment", value=aws_io_t_greengrass_deployment, expected_type=type_hints["aws_io_t_greengrass_deployment"])
            check_type(argname="argument aws_step_functions_workflow", value=aws_step_functions_workflow, expected_type=type_hints["aws_step_functions_workflow"])
            check_type(argname="argument cloud", value=cloud, expected_type=type_hints["cloud"])
            check_type(argname="argument cloud_alt", value=cloud_alt, expected_type=type_hints["cloud_alt"])
            check_type(argname="argument corporate_data_center", value=corporate_data_center, expected_type=type_hints["corporate_data_center"])
            check_type(argname="argument ec2_instance_contents", value=ec2_instance_contents, expected_type=type_hints["ec2_instance_contents"])
            check_type(argname="argument elastic_beanstalk_container", value=elastic_beanstalk_container, expected_type=type_hints["elastic_beanstalk_container"])
            check_type(argname="argument generic", value=generic, expected_type=type_hints["generic"])
            check_type(argname="argument generic_alt", value=generic_alt, expected_type=type_hints["generic_alt"])
            check_type(argname="argument private_subnet", value=private_subnet, expected_type=type_hints["private_subnet"])
            check_type(argname="argument public_subnet", value=public_subnet, expected_type=type_hints["public_subnet"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument server_contents", value=server_contents, expected_type=type_hints["server_contents"])
            check_type(argname="argument spot_fleet", value=spot_fleet, expected_type=type_hints["spot_fleet"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[str, typing.Any] = {
            "auto_scaling_group": auto_scaling_group,
            "availability_zone": availability_zone,
            "aws_account": aws_account,
            "aws_io_t_greengrass": aws_io_t_greengrass,
            "aws_io_t_greengrass_deployment": aws_io_t_greengrass_deployment,
            "aws_step_functions_workflow": aws_step_functions_workflow,
            "cloud": cloud,
            "cloud_alt": cloud_alt,
            "corporate_data_center": corporate_data_center,
            "ec2_instance_contents": ec2_instance_contents,
            "elastic_beanstalk_container": elastic_beanstalk_container,
            "generic": generic,
            "generic_alt": generic_alt,
            "private_subnet": private_subnet,
            "public_subnet": public_subnet,
            "region": region,
            "security_group": security_group,
            "server_contents": server_contents,
            "spot_fleet": spot_fleet,
            "vpc": vpc,
        }

    @builtins.property
    def auto_scaling_group(self) -> GroupFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("auto_scaling_group")
        assert result is not None, "Required property 'auto_scaling_group' is missing"
        return typing.cast(GroupFormat, result)

    @builtins.property
    def availability_zone(self) -> GroupFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("availability_zone")
        assert result is not None, "Required property 'availability_zone' is missing"
        return typing.cast(GroupFormat, result)

    @builtins.property
    def aws_account(self) -> GroupFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("aws_account")
        assert result is not None, "Required property 'aws_account' is missing"
        return typing.cast(GroupFormat, result)

    @builtins.property
    def aws_io_t_greengrass(self) -> GroupFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("aws_io_t_greengrass")
        assert result is not None, "Required property 'aws_io_t_greengrass' is missing"
        return typing.cast(GroupFormat, result)

    @builtins.property
    def aws_io_t_greengrass_deployment(self) -> GroupFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("aws_io_t_greengrass_deployment")
        assert result is not None, "Required property 'aws_io_t_greengrass_deployment' is missing"
        return typing.cast(GroupFormat, result)

    @builtins.property
    def aws_step_functions_workflow(self) -> GroupFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("aws_step_functions_workflow")
        assert result is not None, "Required property 'aws_step_functions_workflow' is missing"
        return typing.cast(GroupFormat, result)

    @builtins.property
    def cloud(self) -> GroupFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("cloud")
        assert result is not None, "Required property 'cloud' is missing"
        return typing.cast(GroupFormat, result)

    @builtins.property
    def cloud_alt(self) -> GroupFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("cloud_alt")
        assert result is not None, "Required property 'cloud_alt' is missing"
        return typing.cast(GroupFormat, result)

    @builtins.property
    def corporate_data_center(self) -> GroupFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("corporate_data_center")
        assert result is not None, "Required property 'corporate_data_center' is missing"
        return typing.cast(GroupFormat, result)

    @builtins.property
    def ec2_instance_contents(self) -> GroupFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("ec2_instance_contents")
        assert result is not None, "Required property 'ec2_instance_contents' is missing"
        return typing.cast(GroupFormat, result)

    @builtins.property
    def elastic_beanstalk_container(self) -> GroupFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("elastic_beanstalk_container")
        assert result is not None, "Required property 'elastic_beanstalk_container' is missing"
        return typing.cast(GroupFormat, result)

    @builtins.property
    def generic(self) -> GroupFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("generic")
        assert result is not None, "Required property 'generic' is missing"
        return typing.cast(GroupFormat, result)

    @builtins.property
    def generic_alt(self) -> GroupFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("generic_alt")
        assert result is not None, "Required property 'generic_alt' is missing"
        return typing.cast(GroupFormat, result)

    @builtins.property
    def private_subnet(self) -> GroupFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("private_subnet")
        assert result is not None, "Required property 'private_subnet' is missing"
        return typing.cast(GroupFormat, result)

    @builtins.property
    def public_subnet(self) -> GroupFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("public_subnet")
        assert result is not None, "Required property 'public_subnet' is missing"
        return typing.cast(GroupFormat, result)

    @builtins.property
    def region(self) -> GroupFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(GroupFormat, result)

    @builtins.property
    def security_group(self) -> GroupFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_group")
        assert result is not None, "Required property 'security_group' is missing"
        return typing.cast(GroupFormat, result)

    @builtins.property
    def server_contents(self) -> GroupFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("server_contents")
        assert result is not None, "Required property 'server_contents' is missing"
        return typing.cast(GroupFormat, result)

    @builtins.property
    def spot_fleet(self) -> GroupFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("spot_fleet")
        assert result is not None, "Required property 'spot_fleet' is missing"
        return typing.cast(GroupFormat, result)

    @builtins.property
    def vpc(self) -> GroupFormat:
        '''
        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(GroupFormat, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ThemeGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/aws-arch.aws_arch.ThemeText",
    jsii_struct_bases=[],
    name_mapping={
        "default": "default",
        "primary": "primary",
        "secondary": "secondary",
        "tertiary": "tertiary",
    },
)
class ThemeText:
    def __init__(
        self,
        *,
        default: builtins.str,
        primary: builtins.str,
        secondary: builtins.str,
        tertiary: builtins.str,
    ) -> None:
        '''(experimental) Theme text dictionary.

        :param default: 
        :param primary: 
        :param secondary: 
        :param tertiary: 

        :stability: experimental
        '''
        if __debug__:
            def stub(
                *,
                default: builtins.str,
                primary: builtins.str,
                secondary: builtins.str,
                tertiary: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument primary", value=primary, expected_type=type_hints["primary"])
            check_type(argname="argument secondary", value=secondary, expected_type=type_hints["secondary"])
            check_type(argname="argument tertiary", value=tertiary, expected_type=type_hints["tertiary"])
        self._values: typing.Dict[str, typing.Any] = {
            "default": default,
            "primary": primary,
            "secondary": secondary,
            "tertiary": tertiary,
        }

    @builtins.property
    def default(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("default")
        assert result is not None, "Required property 'default' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("primary")
        assert result is not None, "Required property 'primary' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secondary(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("secondary")
        assert result is not None, "Required property 'secondary' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tertiary(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("tertiary")
        assert result is not None, "Required property 'tertiary' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ThemeText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/aws-arch.aws_arch.DrawioAwsResourceIconStyleBase",
    jsii_struct_bases=[DrawioAwsShapeStyleBase],
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
    },
)
class DrawioAwsResourceIconStyleBase(DrawioAwsShapeStyleBase):
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
    ) -> None:
        '''(experimental) Based style definition for drawio aws resource icon.

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

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DrawioAwsResourceIconStyleBase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ArrowFormat",
    "AwsCategoryDefinition",
    "DarkPalette",
    "DrawioAws4ParentShapes",
    "DrawioAwsResourceIconStyleBase",
    "DrawioAwsShapeStyleBase",
    "GroupFormat",
    "LightPalette",
    "ParsedAssetKey",
    "Theme",
    "ThemeArrows",
    "ThemeBackgrounds",
    "ThemeGroups",
    "ThemeText",
    "drawio_spec",
    "pricing_manifest",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import drawio_spec
from . import pricing_manifest
